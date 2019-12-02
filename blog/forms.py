
"""
    对blog接口字段进行校验
"""

from django import forms
from blog import models


class RegisterForm(forms.Form):
    '''
        校验注册用户提交表单
    '''

    name = forms.CharField(
        required=True,
        min_length=3,
        max_length=20,
        error_messages={
            "required": "用户名不能为空",
            "min_length": "用户名至少为三个字符",
            "max_length": "用户名最长为20个字符"
        }
    )

    email = forms.CharField(
        required=True,
        error_messages={
            "required": "注册邮箱不能为空"
        }
    )

    password = forms.CharField(
        required=True,
        min_length=6,
        error_messages={
            "required": "注册密码不能为空",
            "min_length": "注册密码字符长度不能小于6"
        }
    )

    r_password = forms.CharField(
        required=True,
        error_messages={
            "required": "重复密码不能为空"
        }
    )

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            user = models.User.objects.filter(name=name).first()
            if user:
                raise forms.ValidationError("该用户名字已存在")

        return name

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email:
            user = models.User.objects.filter(email=email).first()
            if user:
                raise forms.ValidationError("该邮箱已存在")

        return email

    def clean(self):
        password = self.cleaned_data.get("password")
        r_password = self.cleaned_data.get("r_password")

        if password != r_password:
            self.add_error('r_password', '两次密码不一致')

        return self.cleaned_data


class LoginForm(forms.Form):
    '''
        校验登录字段
    '''
    name = forms.CharField(
        required=True,
        min_length=3,
        max_length=20,
        error_messages={
            "required": "用户名不能为空",
            "max_length": "用户名最长为20位",
            "min_length": "用户名最短为3位字符"
        }
    )

    password = forms.CharField(
        required=True,
        min_length=6,
        error_messages={
            "required": "密码不能为空",
            "min_length": "密码至少为6位字符"
        }
    )

    def clean(self):
        name = self.cleaned_data.get("name")
        password = self.cleaned_data.get("password")

        user = models.User.objects.filter(name=name, password=password).first()

        if not user:
            raise forms.ValidationError("账户或密码错误")
        else:
            self.cleaned_data['id'] = user.id
            self.cleaned_data['avatar'] = user.avatar
        return self.cleaned_data


class WriteArticleForm(forms.Form):
    '''
        校验发布文章字段
    '''
    title = forms.CharField(
        required=True,
        max_length=100,
        min_length=2,
        error_messages={
            "required": "文章标题不能为空",
            "max_length": "文章标题字符数不能超过100位",
            "min_length": "文章标题字符数至上为2位"
        }
    )

    content = forms.CharField(
        required=True,
        error_messages={
            "required": "文章内容不能为空"
        }
    )

    author_id = forms.CharField(
        required=True,
        error_messages={
            "required": "作者id不能为空"
        }
    )

    author_name = forms.CharField(
        required=False,
        max_length=20
    )

    def clean(self):
        author_name = self.cleaned_data.get("author_name")
        author_id = self.cleaned_data.get("author_id")

        if id and not author_name:
            user = models.User.objects.filter(id=author_id).first()
            if user:
                self.cleaned_data["author_name"] = user.name
            else:
                raise forms.ValidationError("用户不存在")

        return self.cleaned_data


class WriteExpression(forms.Form):
    content = forms.CharField(
        required=True,
        max_length=200,
        error_messages={
            "required": "短文内容不能为空",
            "max_length": "短文字数不能超过200"
        }
    )

    author_id = forms.CharField(
        required=True,
        error_messages={
            "required": "作者id不能为空"
        }
    )

    urls = forms.CharField()
