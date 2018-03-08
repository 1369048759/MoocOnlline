# -*- coding: UTF-8 -*-
# Author:Xiao Di

from django import forms

import re

from users.models import UserProfile
from .models import UserAsk

class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}&'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号非法', code='invalid')


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)


class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birday', 'address', 'mobile']

        def clean_mobile(self):
            mobile = self.cleaned_data['mobile']
            REGEX_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}&'
            p = re.compile(REGEX_MOBILE)
            if p.match(mobile):
                return mobile
            else:
                raise forms.ValidationError(u'手机号非法', code='invalid')