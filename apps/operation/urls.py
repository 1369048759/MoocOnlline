# -*- coding: UTF-8 -*-
# Author:Xiao Di

from django.conf.urls import url

from .views import AddFavView, UserAskView, AddCourseCommentView, \
    UserInfoView, UploadImageView, ModifyPwdView, SendEmailCodeView, \
    UpdateEmailView, UserCourseView, UserFavCourse, UserFavOrgView, \
    UserFavTeacherView, UserMessageView


urlpatterns = [
    url(r'^user/ask/$', UserAskView.as_view(), name='user_ask'),
    url(r'^add/fav/$', AddFavView.as_view(), name='add_fav'),
    url(r'^add/comment/$', AddCourseCommentView.as_view(), name='add_comment'),

    url(r'^user/info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^upload/image/$', UploadImageView.as_view(), name='upload_image'),
    url(r'^modifyPwd/$', ModifyPwdView.as_view(), name='update_pwd'),
    url(r'^send/emailcode/$', SendEmailCodeView.as_view(), name='send_emailcode'),
    url(r'^update/email/$', UpdateEmailView.as_view(), name='update_email'),

    url(r'^user/course/$', UserCourseView.as_view(), name='user_course'),

    url(r'^user/fav/course/$', UserFavCourse.as_view(), name='user_fav_course'),
    url(r'^user/fav/org/$', UserFavOrgView.as_view(), name='user_fav_org'),
    url(r'^user/fav/teacher/$', UserFavTeacherView.as_view(), name='user_fav_teacher'),

    url(r'^user/message/$', UserMessageView.as_view(), name='user_message')
]