from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin
from .models import Course, CourseRescource, Video, Lesson


# Create your views here.

class CourseListView(View):
    def get(self, request):
        courses = Course.objects.all().order_by('add_time')
        hot_courses = courses.order_by('-student_nums')[:3]

        keywords = request.GET.get('keywords', '')
        if keywords:
            courses = courses.filter(
                Q(name__icontains=keywords)|
                Q(desc__icontains=keywords)|
                Q(detail__icontains=keywords)
            )

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                courses = courses.order_by('-click_nums')
            if sort == 'students':
                courses = courses.order_by('student_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(courses, 9, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'courses' : courses,
            'hot_courses' : hot_courses,
            'sort' : sort
        })


class CourseDetailView(View):
    def get(self,request, course_id):
        try:
            course = Course.objects.get(id=int(course_id))
            category = course.category
            org_id = course.org.id
            recommend_courses = Course.objects.filter(category=category).order_by('-click_nums')[:3]
            course.click_nums += 1
            course.save()
            has_fav_course = False
            has_fav_org = False
            if request.user.is_authenticated():
                if UserFavorite.objects.filter(user=request.user, fav_id=int(course_id), fav_type=1):
                    has_fav_course = True
                if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                    has_fav_org = True

            return render(request, 'course-detail.html', {
                'course' : course,
                'recomment_courses' : recommend_courses,
                'has_fav_course' : has_fav_course,
                'has_fav_org' : has_fav_org
            })
        except Exception as  e:
            None


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        try :
            course = Course.objects.get(id=int(course_id))
            user_course = UserCourse.objects.filter(user=request.user, course_id=int(course_id))
            if not user_course:
                user_course = UserCourse(user=request.user, course_id=int(course_id))
                user_course.save()
                course.student_nums += 1
                course.save()

            user_courses = UserCourse.objects.filter(course=course)
            user_ids = [user_course.user_id for user_course in user_courses]
            user_courses = UserCourse.objects.filter(user_id__in=user_ids)
            course_ids = [user_course.course_id for user_course in user_courses]
            relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]

            course_rescources = CourseRescource.objects.filter(course_id=int(course_id))
            return render(request, 'course-video.html', {
                'course' : course,
                'course_rescources' : course_rescources,
                'relate_courses': relate_courses
            })
        except Exception as  e:
            None


class CourseCommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=int(course_id))
            course_rescources = CourseRescource.objects.filter(course_id=int(course_id))
            user_comments = CourseComments.objects.filter(course_id=int(course_id)).all().order_by('-add_time')

            user_courses = UserCourse.objects.filter(course=course)
            user_ids = [user_course.user_id for user_course in user_courses]
            user_courses = UserCourse.objects.filter(user_id__in=user_ids)
            course_ids = [user_course.course_id for user_course in user_courses]
            relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:3]

            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(user_comments, 10, request=request)
            user_comments = p.page(page)

            return render(request, 'course-comment.html', {
                'course' : course,
                'course_rescources' : course_rescources,
                'user_comments' : user_comments,
                'relate_courses' : relate_courses
            })
        except Exception as e:
            None


class CourseVideoPlayView(LoginRequiredMixin, View):
    def get(self, request, video_id):
        try:
            video = Video.objects.get(id=int(video_id))
            course = video.lesson.course
            course_rescources = CourseRescource.objects.filter(course_id=course.id)
            user_comments = CourseComments.objects.filter(course_id=course.id).all().order_by('-add_time')
            return render(request, 'course-play.html', {
                'course': course,
                'course_rescources': course_rescources,
                'user_comments': user_comments,
                'video' : video
            })
        except Exception as e:
            None



