from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from utils.mixin_utils import LoginRequiredMixin
from users.views import UserProfile, send_email_r
from users.models import EmailVerifyRecord
from courses.models import Course, CourseOrg, Teacher
from .models import UserFavorite, CourseComments, UserCourse, UserMessage
from .forms import  UserAskForm, UploadImageForm, ModifyPwdForm, UserInfoForm

import json
# Create your views here.

class UserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"请正确填写咨询信息"}', content_type='application/json')

def minus_fav_num(fav_type, fav_id):
        if fav_type == 1:
            try:
                course = Course.objects.get(id=fav_id)
                if course.fav_nums > 0:
                    course.fav_nums -= 1
                    course.save()
            except Exception as e:
               None

        if fav_type == 2:
            try:
                course_org = CourseOrg.objects.get(id=fav_id)
                if course_org.fav_nums > 0:
                    course_org.fav_nums -= 1
                    course_org.save()
            except Exception as e:
                None

        if fav_type == 3:
            try:
                teacher = Teacher.objects.get(id=fav_id)
                if teacher.fav_nums > 0:
                    teacher.fav_nums -= 1
                    teacher.save()
            except Exception as e:
                None

def add_fav_num(fav_type, fav_id):
        if fav_type == 1:
            try:
                course = Course.objects.get(id=fav_id)
                course.fav_nums += 1
                course.save()
            except Exception as e:
               None

        if fav_type == 2:
            try:
                course_org = CourseOrg.objects.get(id=fav_id)
                course_org.fav_nums += 1
                course_org.save()
            except Exception as e:
                None

        if fav_type == 3:
            try:
                teacher = Teacher.objects.get(id=fav_id)
                teacher.fav_nums += 1
                teacher.save()
            except Exception as e:
                None

class AddFavView(View):

    def post(self, request):
        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type', 0))
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登入"}', content_type='application/json')
        else:
            exist_record = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if exist_record:
                exist_record.delete()
                minus_fav_num(fav_type, fav_id)
                return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
            else:
                if fav_id > 0 and fav_type > 0:
                    user_fav = UserFavorite()
                    user_fav.user = request.user
                    user_fav.fav_id = fav_id
                    user_fav.fav_type = fav_type
                    user_fav.save()
                    add_fav_num(fav_type, fav_id)
                    return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')
                else :
                    return HttpResponse('{"status":"fail","msg":"异常"}', content_type='application/json')


class AddCourseCommentView(LoginRequiredMixin, View):
    def post(self, request):
        course_id = int(request.POST.get('course_id', 0))
        comments = request.POST.get('comments', '')
        if course_id > 0 and comments:
            course_comment = CourseComments()
            course_comment.user = request.user
            course_comment.course_id = course_id
            course_comment.comments = comments
            course_comment.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {

        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class ModifyPwdView(LoginRequiredMixin, View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"两次密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            pass
            return HttpResponse(json.dumps(modify_form.errors))


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已注册"}', content_type='application/json')
        else:
            status = send_email_r(email, 'update')
            if status:
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email' ,'')
        code = request.POST.get('code', '')
        existed_code = EmailVerifyRecord.objects.filter(email=email, code=code)
        if existed_code:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误"}', content_type='application/json')


class UserCourseView(LoginRequiredMixin, View):
    def get(self, request):
        courses = []
        user_courses = UserCourse.objects.filter(user=request.user)
        for user_course in user_courses:
            course = user_course.course
            courses.append(course)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(courses, 8, request=request)
        courses = p.page(page)

        return render(request, 'usercenter-mycourse.html', {
            'courses' : courses
        })


class UserFavCourse(LoginRequiredMixin, View):
    def get(self, request):
        courses = []
        user_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for user_course in user_courses:
            try:
                course = Course.objects.get(id=user_course.fav_id)
                courses.append(course)
            except Exception as e:
                None

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(courses, 8, request=request)
        courses = p.page(page)

        return render(request, 'usercenter-fav-course.html', {
            'courses': courses,
            'tag': ''
        })


class UserFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        course_orgs = []
        user_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for user_org in user_orgs:
            try:
                org = CourseOrg.objects.get(id=user_org.fav_id)
                course_orgs.append(org)
            except Exception as e:
                None

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(course_orgs, 4, request=request)
        course_orgs = p.page(page)

        return render(request, 'usercenter-fav-org.html', {
            'course_orgs': course_orgs,
            'tag': 'org'
        })


class UserFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teachers = []
        user_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for user_teacher in user_teachers:
            try:
                teacher = Teacher.objects.get(id=user_teacher.fav_id)
                teachers.append(teacher)
            except Exception as e:
                None

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(teachers, 4, request=request)
        teachers = p.page(page)

        return render(request, 'usercenter-fav-teacher.html', {
            'teachers': teachers,
            'tag': 'teacher'
        })


class UserMessageView(LoginRequiredMixin, View):
    def get(self, request):

        user_messages_all = UserMessage.objects.filter(user=request.user)
        all_message_nums = user_messages_all.count()
        sort = request.GET.get('sort' ,'')
        if sort == 'has_read':
            user_messages = user_messages_all.filter(has_read=True)
            has_read_nums = user_messages.count()
            no_read_nums = all_message_nums - has_read_nums
        else :
            user_messages = user_messages_all.filter(has_read=False)
            no_read_nums = user_messages.count()
            has_read_nums = all_message_nums - no_read_nums
            for message in user_messages:
                message.has_read = True
                message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(user_messages, 5, request=request)
        user_messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'user_messages' : user_messages,
            'has_read_nums' : has_read_nums,
            'no_read_nums' : no_read_nums,
            'sort' : sort
        })











