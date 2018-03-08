# -*- coding: UTF-8 -*-
# Author:Xiao Di

from django.conf.urls import url

from .views import LoginView, RegisterView, ActiveView, ForgetPwdView,ResetView, ModifyPwdView, LogoutView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<active_code>.*)$', ActiveView.as_view(), name='active'),
    url(r'^forgetPwd/$', ForgetPwdView.as_view(), name='forgetPwd'),
    url(r'^reset/(?P<reset_code>.*)$', ResetView.as_view(), name='reset'),
    url(r'^modifyPwd/$', ModifyPwdView.as_view(), name='modify'),
    url(r'logout/$', LogoutView.as_view(), name='logout')
]