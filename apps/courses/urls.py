# -*- coding: UTF-8 -*-
# Author:Xiao Di

from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseInfoView, \
    CourseCommentsView, CourseVideoPlayView

urlpatterns  = [
    url(r'list/$', CourseListView.as_view(), name='course_list'),
    url(r'detail/(?P<course_id>.*)$', CourseDetailView.as_view(), name='course_detail'),
    url(r'info/(?P<course_id>.*)$', CourseInfoView.as_view(), name='course_info'),
    url(r'comment/(?P<course_id>.*)$', CourseCommentsView.as_view(), name='course_comment'),
    url(r'play/(?P<video_id>.*)$', CourseVideoPlayView.as_view(), name='video_play'),
]