import logging
logger = logging.getLogger("项目管理")
from django.shortcuts import render,redirect
from django.urls import reverse
from db.mixin import LoginRequiredMixin
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import View
from apps.project.models import Project
from django.contrib import messages
from django.core import serializers
from lib.baseresponse import BaseResponse
import json
from django.http import JsonResponse

# LoginRequiredMixin
class get_Projects(View):
    def get(self,requests):
        res=BaseResponse()
        pro_id=requests.GET.get("pro_id")
        project = Project.objects.filter(prj_id=pro_id)
        try:
            res.data=json.loads(serializers.serialize('json',project))
            res.message= 'success'
            res.code = 20000
        except Exception as e:
            res.message = str(e)
            res.code = 1
        return JsonResponse(res.dict)
    def post(self,requests):
        '''获取项目列表视图'''
        # logger.info("查询项目列表页数为：%s"%page_num)
        # user=requests.user
        # if user.is_superuser:
        #     pro_list = Project.objects.all()  #管理员对应的项目对象
        # else:
        #     pro_list=Project.objects.filter(user__user_id=user.user_id) #获取当前登陆的普通用户的的项目对象
        # pageitor=Paginator(pro_list,5)  #创建一页十条的分页对象
        # pages=pageitor.page(int(page_num))   #得到具体页数的页面对象
        # numbers=pages.number               #当前活动页数
        # new_pro_list=pages.object_list    #具体页数的页面数据
        # page_nums=pageitor.page_range  #数据可分为的页码数
        # #封装页面上下文
        # content={
        #     "pages":pages,
        #     "page_nums":page_nums,
        #     "pro_list":new_pro_list,
        #     "numbers":numbers,
        #     "user_obj":user
        # }
        # logger.info("获取项目列表视图的上下文content:%s"%content)
        # return render(requests,'project_env/index.html',content)
        response = {}
        res=BaseResponse()
        #获取前端传入的参数，并进行格式化处理
        project_data_parm=json.loads(requests.body.decode())
        project_name=project_data_parm.get("project_name")
        if project_name and project_name!="undefined":
            project = Project.objects.filter(prj_name=project_name)
        else:
            project = Project.objects.filter()
        page = project_data_parm.get("page")  #前端请求的哪一页
        limit=project_data_parm.get("limit")#前段传入的每页显示的条数
        paginator=Paginator(project,limit) #创建分页实例
        response["totalCount"]=paginator.count #数据的总条数
        response["totalPage"]=paginator.num_pages #数据总页数
        response["numPerPage"]=limit    #每页显示的条数
        ## 获取指定页码的数据
        try:
            prject_object=paginator.page(page)
        except PageNotAnInteger: #如果传入的页面参数不为整数走该分支
            prject_object=paginator.page(1)
        except EmptyPage:  #如果传入的页面参数为空走该分支
            prject_object=paginator.page(paginator.num_pages)
        response["pageNum"]=prject_object.number  #当前页面是第几页
        try:
            response['data'] = json.loads(serializers.serialize("json", prject_object.object_list))
            res.data=response
            res.message = 'success'
            res.code= 20000
        except  Exception as e:
            res.message =str(e)
            res.code = 1
        return JsonResponse(res.dict)
class add_Projects(View):
    def post(self,requests):
        '''增加项目'''
        response = {}
        #获取前端传入的入参，由于axious默认会将参数以json的格式传送，后端需要做解码格式化成字典形式json.loads(requests.body.decode())
        project_data=json.loads(requests.body.decode())
        # logger.info("添加项目参数为：%s" % project_data)
        prj_name=project_data.get('prj_name')  #项目名称
        #校验项目名称是否重复，重复的项目名称新增失败
        name=Project.objects.filter(prj_name=prj_name)
        pro_description = project_data.get('description')  # 项目描述
        prj_version = project_data.get('version')  # 项目版本
        pro_status =1 if project_data.get('status')=="true" else 0  # 项目状态
        if name:
            response["message"] = '项目名称重复了'
            response["code"] = 00000
        else:
            try:
            #项目实例化
                prj=Project(prj_name=prj_name,version=prj_version,description=pro_description,status=pro_status)
                prj.save()
                response["code"] = 20000
                response["message"] = '添加成功'
                logger.info("项目%s新增成功！！！" % prj)
            except Exception as e:
                response['message'] = str(e)
                response["code"] = 10000
        return JsonResponse(response)
        #     return redirect(reverse('project_env:get_Projects',kwargs={"page_num":1}))
        # return render(requests,'project_env/add.html',{"name":prj_name,"pro_description":pro_description,"prj_version":prj_version,"pro_status":pro_status,"message":"项目名称重复了"})
class delete_Projects(View):
    def get(self,requests):
        '''删除项目(传入项目name)'''
        response={}
        prj_id=requests.GET.get('prj_id')
        Project.objects.filter(prj_id=prj_id).delete()
        response['message']="删除成功"
        response['code'] = 20000
        logger.info("项目%s删除成功！！！" % prj_id)
        # return redirect(reverse('project_env:get_Projects',kwargs={"page_num":1}))
        return JsonResponse(response)
class update_Projects(View):
    def post(self,requests):
        '''编辑信息提交'''
        response={}
        prj_id=requests.GET.get("prj_id")
        pro_info=Project.objects.filter(prj_id=prj_id)
        project_data_parm=json.loads(requests.body.decode())
        logger.info("更新项目%s的更新参数为:%s" %(pro_info,project_data_parm))
        prj_name=project_data_parm.get("prj_name")           #修改 项目名称
        if Project.objects.filter(prj_name=prj_name) and prj_name!=pro_info[0].prj_name:
            response["message"]="该项目名称已经存在"
            response["code"]=00000
        else:
            try:
                description=project_data_parm.get("description")           #修改 项目描述
                prj_version=project_data_parm.get("version")           #修改 项目版本
                pro_status=1 if project_data_parm.get("status")=="true" else 0   #修改 项目状态
                pro_info.update(prj_name=prj_name,version=prj_version,description=description,status=pro_status)
                response["message"]="更新成功"
                response["code"]=20000
                logger.info("更新项目完成！！！")
            except Exception as e:
                response["message"]=str(e)
                response["code"] = 10000
        return JsonResponse(response)
        #     return redirect(reverse('project_env:get_Projects', kwargs={"page_num": 1}))
        # project = Project.objects.filter(prj_id=pro_id)[0]
        # return render(requests,'project_env/update.html',{"project":project,"message":"项目名称重复了"})
class search_Projects(LoginRequiredMixin,View):
    def get(self,requests):
        '''根据项目名称搜索接口'''
        project_name=requests.GET.get("project_name")
        logger.info("根据项目名称%s搜索接口" % project_name)
        user=requests.user
        if user.is_superuser:
            pro_list=Project.objects.filter(prj_name=project_name)  #实例化要查询的项目对象
        else:
            pro_list = Project.objects.filter(prj_name=project_name,user__user_id=user.user_id)
        content={
            "pro_list":pro_list,
            "user_obj": user
        }
        logger.info("根据项目名称搜索接口的返回值上下文:%s" % content)
        return render(requests,'project_env/index.html',content)