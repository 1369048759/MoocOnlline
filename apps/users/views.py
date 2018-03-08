from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.db.models import Q

from random import Random
import json

from courses.models import Course, CourseOrg
from .models import Banner
from .forms import  LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm
from .models import UserProfile, EmailVerifyRecord
from MOOC.settings import EMAIL_FROM

# Create your views here.

def random_str(randomlength = 8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwSsYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def send_email_r(email, send_type):
    email_record = EmailVerifyRecord()
    if send_type == 'update':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''
    status = 1

    if send_type == 'register':
        email_title = 'MOOC Online 激活链接'
        email_body = '请点击下面链接激活你的账号 http://192.168.255.133:8000/user/active/{0}'.format(code)


    if send_type == 'forgetPwd':
        email_title = 'MOOC Online 密码重置'
        email_body = '请点击下面链接重置你的密码 http://192.168.255.133:8000/user/reset/{0}'.format(code)


    if send_type == 'update':
        email_title = 'MOOC Online 邮箱修改'
        email_body = '你的邮箱验证码为：{0}'.format(code)

    try:
        send_mail(email_title, email_body, EMAIL_FROM, [email])
    except Exception as e:
        status = 0
    return status


class IndexView(View):
    def get(self, request):
        all_banner = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner= False).order_by('-click_nums')[:6]
        banner_courses = Course.objects.filter(is_banner= True)[:3]
        course_orgs = CourseOrg.objects.all().order_by('-click_nums')[:15]
        return render(request, 'index.html', {
            'all_banner' : all_banner,
            'courses': courses,
            'banner_courses' : banner_courses,
            'course_orgs' : course_orgs
        })


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request ,'login.html', {

        })

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {
                        'msg' : '用户未激活'
                    })
            else:
                return render(request, 'login.html', {
                    'msg' : '用户名或者密码错误'
                })
        else:
            login_form_errors = json.loads(json.dumps(login_form.errors))
            if 'username' in login_form_errors.keys():
                if login_form_errors['username'][0] == '这个字段是必填项。':
                    return render(request, 'login.html', {
                        'login_form': login_form,
                        'msg' : '请输入用户名后再登入'
                    })
            if 'password' in login_form_errors.keys():
                if login_form_errors['password'][0] == '这个字段是必填项。':
                    return render(request, 'login.html', {
                        'login_form': login_form,
                        'msg' : '请输入密码后再登入'
                    })
            return render(request, 'login.html', {
                'login_form': login_form,
                'msg': '用户名或密码有误，请重新输入'
            })


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {
            'register_form' : register_form
        })

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')

            if UserProfile.objects.filter(email=email):
                return render(request, 'register.html', {
                    'msg' : '该邮箱已被注册',
                    'register_form': register_form
                })
            else:
                if send_email_r(email, 'register') == 0:
                    return render(request, 'register.html', {
                        'msg' : '邮箱不存在，请重新输入'
                    })
                else:
                    user_profile = UserProfile()
                    user_profile.username = email
                    user_profile.email = email
                    user_profile.password = make_password(password)
                    user_profile.is_active = False
                    user_profile.save()
                    return render(request, 'login.html', {
                        'msg' : '账号注册成功 打开邮箱激活账号'
                    })

        else:
            register_form_errors = json.loads(json.dumps(register_form.errors))
            if 'email' in register_form_errors.keys():
                if register_form_errors['email'][0] == '这个字段是必填项。':
                    return render(request, 'register.html', {
                        'register_form': register_form,
                        'msg': '请输入邮箱后注册'
                    })
                else:
                    return render(request, 'register.html', {
                        'register_form': register_form,
                        'msg': '输入一个有效的 Email 地址'
                    })

            if 'password' in register_form_errors.keys():
                if register_form_errors['password'][0] == '这个字段是必填项。':
                    return render(request, 'register.html', {
                        'register_form': register_form,
                        'msg': '请输入密码后注册'
                    })
                else:
                    return render(request, 'register.html', {
                        'register_form': register_form,
                        'msg': '密码格式为6-20非中文字符，请重新输入'
                    })

            if 'captcha' in register_form_errors.keys():
                if register_form_errors['captcha'][0] == '这个字段是必填项。':
                    return render(request, 'register.html', {
                        'register_form': register_form,
                        'msg': '输入验证码后注册'
                    })
                else:
                    return render(request, 'register.html', {
                        'register_form': register_form,
                        'msg': '验证码错误，请重新输入'
                    })


class ActiveView(View):
    def get(self, request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code, send_type='register')
        if all_records:
            for record in all_records:
                user = UserProfile.objects.get(email=record.email)
                user.is_active = True
                user.save()
                record.delete();
            return render(request, 'login.html', {
                'msg' : '账号激活成功 请继续登入'
            })
        else:
            return render(request, 'link-broken.html', {

            })


class ForgetPwdView(View):
    def get(self, request):
        forgetPwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html',{
            'forgetPwd_form' : forgetPwd_form
        })

    def post(self, request):

        forgetPwd_form = ForgetPwdForm(request.POST)
        if forgetPwd_form.is_valid():

            try:
                email = request.POST.get('email', '')
                UserProfile.objects.get(email=email)
                send_email_r(email, 'forgetPwd')
                return render(request, 'login.html', {

                })
            except Exception as e:
                return render(request, 'forgetpwd.html', {
                    'forgetPwd_form': forgetPwd_form,
                    'msg': '绑定该邮箱的用户不存在，请重新输入邮箱'
                })
        else:
            forgetPwd_form_errors = json.loads(json.dumps(forgetPwd_form.errors))

            if 'email' in forgetPwd_form_errors.keys():
                if forgetPwd_form_errors['email'][0] == '这个字段是必填项。':
                    return render(request, 'forgetpwd.html', {
                        'forgetPwd_form': forgetPwd_form,
                        'msg': '请先输入邮箱'
                    })
                else:
                    return render(request, 'forgetpwd.html', {
                        'forgetPwd_form': forgetPwd_form,
                        'msg': '邮箱格式有误，请重新输入'
                    })

            if 'captcha' in forgetPwd_form_errors.keys():
                if forgetPwd_form_errors['captcha'][0] == '这个字段是必填项。':
                    return render(request, 'forgetpwd.html', {
                        'forgetPwd_form': forgetPwd_form,
                        'msg': '输入验证码后注册'
                    })
                else:
                    return render(request, 'forgetpwd.html', {
                        'forgetPwd_form': forgetPwd_form,
                        'msg': '验证码错误，请重新输入'
                    })


class ResetView(View):
    def get(self, request, reset_code):
        all_record = EmailVerifyRecord.objects.filter(code=reset_code, send_type='forgetPwd')
        if all_record:
            for record in all_record:
                email = record.email
                record.delete()
                return render(request, 'password_reset.html',{
                    'email' : email
                })
        else:
            return render(request, 'link-broken.html', {
            })


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        email = request.POST.get('email', '')
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {
                    'msg' : '两次密码不一致',
                    'email' : email,
                    'modify_form': modify_form
                })
            else:
                try:
                    user = UserProfile.objects.get(email=email)
                    user.password = make_password(pwd2)
                    user.save()
                    return render(request, 'login.html', {

                    })
                except Exception as e:
                    return None
        else:
            return render(request, 'password_reset.html', {
                'msg': '请输入6-20位非中文字符',
                'modify_form': modify_form
            })


class LogoutView(View):
    def get(self, request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))


class LinkBrokenView(View):
    def get(self, request):
        return render(request, 'link-broken.html', {

        })


def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')


def permission_denied(request):
    return render(request, '403.html')

class TestView(View):
    def get(self, request):
        return render(request, 'hint.html', {

        })



