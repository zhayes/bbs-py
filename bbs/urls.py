"""bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from blog import views

from django.views.static import serve
from bbs.settings import MEDIA_ROOT
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^admin', admin.site.urls),

    url(r'^reg$', views.registerPage, name='register'),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^user/create$', views.CreateUser.as_view()),
    url(r'^login$', views.Login.as_view(), name='login'),
    url(r'^logout$', views.Logout.as_view(), name='logout'),
    url(r'^$', views.HomePage.as_view(), name='home'),
    url(r'^write$', views.WritePage.as_view()),
    url(r'^article/([\d]+)$', views.ArticleDetail.as_view()),
    url(r'^upload/img$', csrf_exempt(views.UploadImg.as_view())),
    url(r'^expression/create$', views.PublishExpression.as_view())
]
