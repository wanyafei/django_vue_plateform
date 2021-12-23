from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.contrib import auth
from django.views.generic import View
from apps.taste_user.models import User
from lib.token import generatetoken
from django.http import JsonResponse
import json


from .models import Book

@require_http_methods(["GET"])
def add_book(request):
    response = {}
    try:
        book = Book(book_name=request.GET.get('book_name'))
        book.save()
        response['msg'] = 'success'
        response['error_num'] = 0
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
@require_http_methods(["GET"])
def show_books(request):
    response = {}
    try:
        books = Book.objects.filter()
        response['list'] = json.loads(serializers.serialize("json", books))
        response['message'] = 'success'
        response["code"]=20000
    except  Exception as e:
        response['message'] = str(e)
        response['code'] = 1
    return JsonResponse(response)
# @require_http_methods(["POST"])
# def login(request):
#     response = {}
#     token={}
#     username=request.POST.get("username")
#     password = request.POST.get("password")
#     token["token"]="admin_token"
#     response["code"]=20000
#     response["data"] = token
#     return JsonResponse(response)
class login(View):
    def post(self,requests):
        #定义返回响应体
        res={}
        token = {}
        login_parms = json.loads(requests.body.decode())
        username = login_parms.get("username")
        password = login_parms.get("password")
        if not all([username, password]):
            res["code"]=10000
            res["message"] = "用户名或者密码为必输项！"
        # 对用户名和密码进行正确性验证，若验证成功返回该登陆对象
        user_obj = auth.authenticate(username=username, password=password)
        if user_obj:
            # 记住用户登陆状态，将登录的用户封装到request.user中
            auth.login(requests, user_obj)
            token_obj=generatetoken()
            token["token"] =token_obj
            res["code"] = 20000
            res["message"] = "登陆成功"
            res["data"] = token
        else:
            res["code"] = 10000
            res["message"] = "用户名或者密码输入有误！"
        return JsonResponse(res)
#getinfo 登陆后的getinfo 接口
class info(View):
    def get(self,requests):
        response = {}
        res={}
        res["name"] = requests.user.username
        response['data']=res
        response["code"] = 20000
        return JsonResponse(response)
#退出登陆
class logout(View):
    def get(self,requests):
        res={}
        auth.logout(requests)
        res["code"]=20000
        res["message"]="退出登陆成功！"
        return JsonResponse(res)
#获取用户列表
class getuser(View):
    def get(self,requests):
        res={}
        # user_list=[]
        user=requests.GET.get("user")
        User_obj=User.objects.filter(username=user)
        if User_obj:
            res["code"] = 20000
            res["success"] = True
        else:
            res["code"] = 20000
            res["success"] = False
        return JsonResponse(res)

