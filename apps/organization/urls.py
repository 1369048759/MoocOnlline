# -*- coding: UTF-8 -*-
# Author:Xiao Di

from django.conf.urls import url

from .views import CourseOrgListView, CourseOrgHomeView, \
    CourseOrgCourseView, CourseOrgDescView, CourseOrgTeacherView, \
    TeacherListView,TeacherDetailView

urlpatterns = [
    url(r'^list/org/$', CourseOrgListView.as_view(), name='org_list'),
    url(r'^home/(?P<org_id>.*)$', CourseOrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>.*)$', CourseOrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>.*)$', CourseOrgDescView.as_view(), name='org_desc'),
    url(r'^teacher/(?P<org_id>.*)$', CourseOrgTeacherView.as_view(), name='org_teacher'),

    url(r'^list/teacher/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^detail/teacher/(?P<teacher_id>.*)$', TeacherDetailView.as_view(), name='teacher_detail')
]