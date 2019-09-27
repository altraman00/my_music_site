# -*- coding: utf-8 -*-
'''
Created by admin at 2019-07-28  
desc:
'''


from django.contrib.auth.forms import UserCreationForm
from user.models import MyUser
from django import forms


class MyUserCreationForm(UserCreationForm):
    # 重写初始化函数，设置自定义字段password1和password2的样式和属性
    def __init(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'txt tabInput', 'placeholder': '密码，4-16位数字/字母，特殊字符（空格除外'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'txt tabInput', 'placeholder': '重复密码'})

    class Meta(UserCreationForm.Meta):
        model = MyUser
        # 在注册界面添加模型字段：手机号和密码
        fields = UserCreationForm.Meta.fields + ('mobile',)
        # 设置模型字段的样式和属性
        widgets = {
            'mobile': forms.widgets.TextInput(attrs={'class': 'txt tabInput', 'placeholder': '手机号'}),
            'username': forms.widgets.TextInput(attrs={'class': 'txt TabInput', 'placeholder': '用户名'}),
        }