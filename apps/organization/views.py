from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from courses.models import Course
from operation.models import UserFavorite
from .models import CourseOrg, City, Teacher, OrgImage


# Create your views here.

class CourseOrgListView(View):
    def get(self, request):
        citys = City.objects.all()[:8]

        course_orgs = CourseOrg.objects.all()
        hot_orgs = course_orgs.order_by('-click_nums')[:4]
        org_nums = course_orgs.count()

        category = request.GET.get('ct', '')
        city_id = request.GET.get('city', '')
        sort = request.GET.get('sort', '')

        keywords = request.GET.get('keywords', '')
        if keywords:
            course_orgs = course_orgs.filter(
                Q(name__icontains=keywords)|
                Q(desc__icontains=keywords)
            )

        if category:
            course_orgs = course_orgs.filter(category=category)

        if city_id:
            course_orgs = course_orgs.filter(city_id=city_id)

        if sort:
            if sort == 'fav_nums':
                course_orgs = course_orgs.order_by('-fav_nums')
            if sort == 'click_nums':
                course_orgs = course_orgs.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(course_orgs, 5, request=request)
        course_orgs = p.page(page)

        return render(request, 'org-list.html', {
            'course_orgs' : course_orgs,
            'hot_orgs' : hot_orgs,
            'citys' : citys,
            'org_nums' : org_nums,
            'city_id' : city_id,
            'ct' : category,
            'sort' : sort
        })


class CourseOrgHomeView(View):
    def get(self, request, org_id):
        try:
            course_org = CourseOrg.objects.get(id=int(org_id))
            courses = course_org.course_set.all()[:3]
            teachers = course_org.teacher_set.all()[:1]
            course_org.click_nums += 1
            course_org.save()
            has_fav = False
            if request.user.is_authenticated():
                if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                    has_fav = True
            return render(request, 'org-detail-homepage.html', {
                'course_org' : course_org,
                'courses' : courses,
                'teachers' : teachers,
                'has_fav' : has_fav
            })
        except Exception as e:
            None

    def post(self,request):
        pass


class CourseOrgCourseView(View):
    def get(self, request, org_id):
        try:
            course_org = CourseOrg.objects.get(id=int(org_id))
            courses = course_org.course_set.all()
            has_fav = False
            if request.user.is_authenticated():
                if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                    has_fav = True
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(courses, 8, request=request)

            courses = p.page(page)
            return render(request, 'org-detail-course.html',{
                'course_org' : course_org,
                'has_fav' : has_fav,
                'courses' : courses
            })
        except Exception as e:
            None


class CourseOrgDescView(View):
    def get(self, request, org_id):
        try:

            course_org = CourseOrg.objects.get(id=int(org_id))
            org_images = OrgImage.objects.filter(org_id=int(org_id)).order_by('index')
            has_fav = False
            if request.user.is_authenticated():
                if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                    has_fav = True
            return render(request, 'org-detail-desc.html', {
                'course_org' : course_org,
                'has_fav' : has_fav,
                'org_images' : org_images
            })
        except Exception as e:
            None


class CourseOrgTeacherView(View):
    def get(self, request, org_id):
        try:
            course_org = CourseOrg.objects.get(id=int(org_id))
            teachers = course_org.teacher_set.all()
            has_fav = False
            if request.user.is_authenticated():
                if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                    has_fav = True
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1

            p = Paginator(teachers, 5, request=request)
            teachers = p.page(page)

            return render(request, 'org-detail-teachers.html', {
                'course_org' : course_org,
                'has_fav' : has_fav,
                'teachers' : teachers
            })
        except Exception as e:
            None


class TeacherListView(View):
    def get(self, request):
        teachers = Teacher.objects.all()
        teacher_nums = teachers.count()
        hot_teachers = teachers.order_by('-click_nums')[:5]

        keywords = request.GET.get('keywords', '')
        if keywords:
            teachers = teachers.filter(
                Q(name__icontains=keywords)|
                Q(work_position__icontains=keywords)|
                Q(work_company__icontains=keywords)
            )

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            teachers = teachers.order_by('-fav_nums')

        if sort == 'years':
            teachers = teachers.order_by('-work_years')

        if sort == 'click':
            teachers = teachers.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teachers, 5, request=request)
        teachers = p.page(page)


        return render(request, 'teachers-list.html', {
            'teachers' : teachers,
            'teacher_nums' : teacher_nums,
            'hot_teachers' : hot_teachers,
            'sort' : sort
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_courses = teacher.course_set.all()
            hot_teachers = Teacher.objects.all().order_by('-click_nums')[:5]
            teacher.click_nums += 1
            teacher.save()

            has_fav_teacher = False
            has_fav_org = False

            if request.user.is_authenticated():
                if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                    has_fav_teacher = True
                if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                    has_fav_org = True

            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(teacher_courses, 8, request=request)
            teacher_courses = p.page(page)

            return render(request ,'teacher-detail.html', {
                'teacher' : teacher,
                'hot_teachers' : hot_teachers,
                'teacher_courses' : teacher_courses,
                'has_fav_teacher' : has_fav_teacher,
                'has_fav_org' : has_fav_org
            })
        except Exception as e:
            None


