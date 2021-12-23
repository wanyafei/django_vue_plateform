import logging
logger = logging.getLogger("环境管理")
import json
from django.shortcuts import render,redirect
from django.urls import reverse
from django.db.models import Q
from django.core import serializers
from db.mixin import LoginRequiredMixin
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import View
from apps.project.models import Project
from apps.env.models import Environment
from django.contrib import messages
from django.http import JsonResponse

#环境相关
class get_env(View):
    def get(self, requests):
        '''前端detail路由，弹框中环境信息试图'''
        res = {}
        env_id = requests.GET.get("env_id")
        env = Environment.objects.filter(env_id=env_id)
        try:
            res['data'] = json.loads(serializers.serialize('json', env))
            res['message'] = 'success'
            res["code"] = 20000
        except Exception as e:
            res['message'] = str(e)
            res['code'] = 1
        return JsonResponse(res)

    def post(self, requests):
        '''获取项目列表视图'''
        response = {}
        res = {}
        # 获取前端传入的参数，并进行格式化处理
        env_data_parm = json.loads(requests.body.decode())
        env_name = env_data_parm.get("env_name")
        project=env_data_parm.get("project")
        if env_name and env_name != "undefined" and project and project !="undefined":
            env = Environment.objects.filter(env_name=env_name,project_id=project)
        elif env_name and env_name != "undefined":
            env = Environment.objects.filter(env_name=env_name)
        elif project and project !="undefined":
            env = Environment.objects.filter(project_id=project)
        else:
            env = Environment.objects.filter()
        page = env_data_parm.get("page")  # 前端请求的哪一页
        limit = env_data_parm.get("limit")  # 前段传入的每页显示的条数
        paginator = Paginator(env, limit)  # 创建分页实例
        response["totalCount"] = paginator.count  # 数据的总条数
        response["totalPage"] = paginator.num_pages  # 数据总页数
        response["numPerPage"] = limit  # 每页显示的条数
        ## 获取指定页码的数据
        try:
            env_object = paginator.page(page)
        except PageNotAnInteger:  # 如果传入的页面参数不为整数走该分支
            env_object = paginator.page(1)
        except EmptyPage:  # 如果传入的页面参数为空走该分支
            env_object = paginator.page(paginator.num_pages)
        response["pageNum"] = env_object.number  # 当前页面是第几页
        try:
            response['data'] = json.loads(serializers.serialize("json", env_object.object_list))
            res["data"] = response
            res['message'] = 'success'
            res["code"] = 20000
        except  Exception as e:
            res['message'] = str(e)
            res['code'] = 1
        return JsonResponse(res)
class add_env(View):
    def post(self,requests):
        '''新增环境类视图'''
        response={}
        env_parms=json.loads(requests.body.decode())
        url=env_parms.get("url")                    #url
        project_id=env_parms.get("project")
        project=Project.objects.get(prj_id=project_id)
        env_obj=Environment.objects.filter(url=url,project=project)
        env_name=env_parms.get("env_name")           #环境名称
        description=env_parms.get("description")     #环境描述
        status=1 if env_parms.get("status")=="true" else 0 #环境状态
        if env_obj:
            response["message"] = "该环境已经存在!"
            response["code"] = 00000
        else:
            try:
                env=Environment(env_name=env_name,url=url,description=description,status=status,project=project)
                env.save()
                response["code"]=20000
                response["message"] = "环境新增成功!",
            except Exception as e:
                response["code"]=10000
                response["message"]=str(e)
        return JsonResponse(response)
class delete_env(View):
    def get(self, requests):
        '''删除环境(传入项目id)'''
        response = {}
        env_id = requests.GET.get('env_id')
        Environment.objects.filter(env_id=env_id).delete()
        response['message'] = "删除成功"
        response['code'] = 20000
        return JsonResponse(response)
class update_env(View):
    def post(self,requests):
        '''环境修改类视图'''
        response = {}
        env_id=requests.GET.get("env_id")
        env=Environment.objects.filter(env_id=env_id)
        env_parms = json.loads(requests.body.decode())
        url = env_parms.get("url")  # url
        project_id = env_parms.get("project")
        project = Project.objects.get(prj_id=project_id)
        env_obj = Environment.objects.filter(Q(url=url)&Q(project=project))
        env_name = env_parms.get("env_name")  # 环境名称
        description = env_parms.get("description")  # 环境描述
        status = 1 if env_parms.get("status") == "true" else 0  # 环境状态
        if env_obj and url!=env[0].url and project_id!=env[0].project_id:
            response["message"] = "该环境已经存在!"
            response["code"] = 00000
        else:
            try:
                env.update(env_name=env_name,url=url,description=description,status=status,project=project)
                response["code"] = 20000
                response["message"] = "环境新增成功!",
            except Exception as e:
                response["code"]=10000
                response["message"]=str(e)
        return JsonResponse(response)















