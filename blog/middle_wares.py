from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse

from django.utils.deprecation import MiddlewareMixin

#无登录的情况下不能访问的页面
BLACK_LIST = [
    '/write'
]


class AccessPageControlMiddle(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id')
        user_name = request.session.get('user_name')

        print(request.path)

        if (request.path in BLACK_LIST) and (not user_id or not user_name):
            return redirect(reverse('home'))
