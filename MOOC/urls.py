"""MOOC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
#from django.contrib import admin
from django.views.static import serve
import  xadmin

from .settings import MEDIA_ROOT

from users.views import IndexView, LinkBrokenView, page_not_found, page_error, permission_denied, TestView

urlpatterns = [

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^xadmin', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^ueditor/',include('DjangoUeditor.urls')),

    url(r'^media/(?P<path>.*)$', serve, {'document_root' : MEDIA_ROOT}),
    url(r'^linkbroken$', LinkBrokenView.as_view(), name='expired'),

    url(r'^user/', include('users.urls', namespace='user')),
    url(r'^org/', include('organization.urls', namespace='org')),
    url(r'^operate/', include('operation.urls', namespace='operate')),
    url(r'^course/', include('courses.urls', namespace='course')),

    url(r'^test/$',TestView.as_view(), name='test')
]

handler404 = page_not_found
handler500 = page_error
handler505 = permission_denied

