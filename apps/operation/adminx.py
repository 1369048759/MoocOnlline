# -*- coding: UTF-8 -*-
# Author:Xiao Di

import xadmin

from .models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse

class UserAskXadmin(object):
    list_display = ['name', 'mobile', 'course', 'add_time']
    search_fields = ['name', 'mobile', 'course']
    list_filter = ['name', 'mobile', 'course']
    show_detail_fields = ['name']
    readonly_fields = ['name', 'mobile', 'course', 'add_time']
    refresh_time = [3, 5]
    model_icon = 'fa fa-cloud-upload'



class CourseCommentsXadmin(object):
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'comments']
    list_filter = ['user', 'add_time']
    readonly_fields = ['user', 'course', 'comments', 'add_time']
    refresh_times = [3, 5]
    model_icon = 'fa fa-comments'


class UserFavoriteXadmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']
    readonly_fields = ['user', 'fav_id', 'fav_type', 'add_time']
    refresh_times = [3, 5]
    model_icon = 'fa fa-bookmark'


class UserMessageXadmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message']
    list_filter = ['user', 'message', 'has_read', 'add_time']
    model_icon = 'fa fa-envelope'


class UserCourseXadmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user']
    list_filter = ['user', 'add_time']
    readonly_fields = ['user', 'course', 'add_time']
    model_icon = 'fa fa-flag'


xadmin.site.register(UserAsk, UserAskXadmin)
xadmin.site.register(CourseComments, CourseCommentsXadmin)
xadmin.site.register(UserFavorite, UserFavoriteXadmin)
xadmin.site.register(UserMessage, UserMessageXadmin)
xadmin.site.register(UserCourse, UserCourseXadmin)