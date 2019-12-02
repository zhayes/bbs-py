from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from blog import models, forms
import os
import time
import json
import re

# 存放上传头像图片的文件夹
AVATAR_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'media',
    'avatar'
)

ARTICLE_IMG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'media',
    'article_imgs'
)

# Create your views here.

# 返回注册页面


def registerPage(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        return HttpResponse('page is losted')


# 注册用户
class CreateUser(View):

    def post(self, request):

        obj = forms.RegisterForm(request.POST)

        valid_result = obj.is_valid()

        status = {"code": -1}

        if valid_result:
            file = request.FILES.get('avatar', None)
            avatar = self.write_avatar(file)

            name = obj.cleaned_data.get("name")
            email = obj.cleaned_data.get("email")
            password = obj.cleaned_data.get("password")

            models.User.objects.create(
                name=name, email=email, password=password, avatar=avatar)

            status["code"] = 0
            status["msg"] = "注册成功"

        else:
            error_str = obj.errors.as_json()
            error_str = json.loads(error_str, encoding="utf-8")

            status["msg"] = '；'.join(
                [error_str[error][0]['message'] for error in error_str])

        return JsonResponse(status, json_dumps_params={'ensure_ascii': False})

    # 把上传的头像写到特定的文件夹后返回图片名称

    def write_avatar(self, file):
        url_path = None
        if file:
            file_name = file.name
            url_path = str(int(round(time.time() * 1000)))+'_'+file_name
            avatar_path = os.path.join(AVATAR_DIR, url_path)

            with open(avatar_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)

        return url_path


# 登录
class Login(View):
    def post(self, request):
        obj = forms.LoginForm(request.POST)
        status = {"code": -1}

        if obj.is_valid():
            status['code'] = 0
            status['msg'] = '登录成功'

            # 在session里保存当前登录的用户信息
            request.session['user_name'] = obj.cleaned_data.get('name')
            request.session['user_id'] = obj.cleaned_data.get('id')
            request.session['user_avatar'] = obj.cleaned_data.get('avatar')

        else:
            error_str = obj.errors.as_json()
            error_str = json.loads(error_str, encoding="utf-8")
            status["msg"] = '；'.join(
                [error_str[error][0]['message'] for error in error_str])

        return JsonResponse(status)

    def get(self, request):
        return render(request, 'login.html')


# 退出
class Logout(View):
    def get(self, request):
        name = request.GET.get('name')
        id = request.GET.get('id')

        user = models.User.objects.filter(name=name, id=id).first()

        if user:
            del request.session['user_name']
            del request.session['user_id']

            return redirect(reverse('home'))
        else:
            return HttpResponse('<h2>退出失败</h2>')


# 首页
class HomePage(View):
    def get(self, request):

        article_list = models.Article.objects.all()

        return render(request, 'index.html', {"article_list": article_list})


class ArticleList(View):
    def get(self, request):
        page_num = request.GET.get('page_num', 1)
        page_size = request.GET.get('page_size', 10)

        article_list = models.Article.objects.all()

        #p = Paginator(objects,3)


# 编写文章页面
class WritePage(View):
    def get(self, request):
        return render(request, 'write.html')

    def post(self, request):
        obj = forms.WriteArticleForm(json.loads(request.body))

        status = {"code": -1}
        status["msg"] = "发布失败"

        if obj.is_valid():
            user = models.User.objects.filter(
                id=obj.cleaned_data['author_id']).first()
            obj.cleaned_data['author_id'] = user

            models.Article.objects.create(**obj.cleaned_data)
            status["code"] = 0
            status["msg"] = "发布成功"
        else:
            error_str = obj.errors.as_json()
            print(error_str)
            error_str = json.loads(error_str, encoding="utf-8")
            status["msg"] = '；'.join(
                [error_str[error][0]['message'] for error in error_str])

        return JsonResponse(status)


# 查看文章详情
class ArticleDetail(View):
    def get(self, request, article_id):
        article_obj = models.Article.objects.filter(id=article_id).first()
        article_list = models.Article.objects.all()

        print(article_obj)

        return render(request, 'article_detail.html', {"article": article_obj, "article_list": article_list})


# 发文上传图片接口

class UploadImg(View):
    def post(self, request):
        try:
            file = request.FILES.get('file')

            if file:
                file_type = file.__dict__.get('content_type')
                img_pattern = 'image/.'
                if not re.match(img_pattern,file_type) :
                    return JsonResponse({"code": -1, "msg": "上传失败，不是图片类型"})

                file_name = str(int(round(time.time() * 1000))
                                ) + '_' + file.name
                file_path = os.path.join(ARTICLE_IMG_DIR, file_name)
                with open(file_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)

                return JsonResponse({"code": 0, "msg": "上传成功", "data": {"url": f'/media/article_imgs/{file_name}'}})
            else:
                return JsonResponse({"code": -1, "msg": "图片上传失败"})
        except Exception as error:
            print(f'\033[0;31m{error}\033[0m')
            return JsonResponse({"code": -1, "msg": "图片上传失败"})

# 发布短文


class PublishExpression(View):
    def post(self, request):
        obj = forms.WriteExpression(request.POST)

        if obj.is_valid():
            content = obj.cleaned_data.get('content')
            author_id = obj.cleaned_data.get('author_id')
            user = models.User.objects.filter(id=author_id).first()
            urls = obj.cleaned_data.get('urls', '').split(',')

            expression = models.Expression.objects.create(
                content=content, author_id=user)

            for url in urls:
                models.ExpressionImage.objects.create(
                    expression_id=expression, url=url)

            return JsonResponse({"code": 0, "msg": "发布成功"})
        else:
            error_str = obj.errors.as_json()
            print(error_str)
            error_str = json.loads(error_str, encoding="utf-8")
            error_str = '；'.join(
                [error_str[error][0]['message'] for error in error_str])
            return JsonResponse({"code": -1, "msg": error_str})


class ExpressionList(View):
    def get(self, request):
        pass
