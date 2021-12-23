from django.shortcuts import render
from django.views.generic import View
import json,os,time
from django.http import FileResponse
from django_vue_demo.settings import BASE_DIR,UPLOAD_ROOT
from django.db.models import Q
from lib.execute import Execute
from django.core import serializers
from lib.excelmethod import excelOpern
from django.http import JsonResponse,HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from apps.apitest.models import Interface,Case,Plan,Report
from apps.project.models import Project
from apps.env.models import Environment
from apps.taste_user.models import Taste,User
#---------------------------接 口 管 理-------------------------
class get_project_parm(View):
    def get(self,requests):
        res={}
        try:
            res['data']=list(Project.objects.all().values('prj_id','prj_name'))
            res['message']='success'
            res['code']=20000
        except Exception as e:
            res['message'] = str(e)
            res['code'] = 1
        return JsonResponse(res)
class get_interface(View):
    def get(self,requests):
        res = {}
        if_id = requests.GET.get("if_id")
        try:
            interface = Interface.objects.filter(if_id=if_id)
            res['data'] = json.loads(serializers.serialize('json', interface))
            res['message'] = 'success'
            res["code"] = 20000
        except Exception as e:
            res['message'] = str(e)
            res['code'] = 1
        return JsonResponse(res)
    def post(self,requests):
        '''获取接口管理列表视图'''
        response = {}
        res = {}
        # 获取前端传入的参数，并进行格式化处理
        interface_data_parm = json.loads(requests.body.decode())
        interface_name = interface_data_parm.get("if_name")
        project = interface_data_parm.get("project")
        if interface_name and interface_name != "undefined" and project and project !="undefined":
            interface = Interface.objects.filter(if_name=interface_name,project_id=project)
        elif interface_name and interface_name != "undefined":
            interface = Interface.objects.filter(if_name=interface_name)
        elif project and project !="undefined":
            interface = Interface.objects.filter(project_id=project)
        else:
            interface = Interface.objects.filter()
        page = interface_data_parm.get("page")  # 前端请求的哪一页
        limit = interface_data_parm.get("limit")  # 前段传入的每页显示的条数
        paginator = Paginator(interface, limit)  # 创建分页实例
        response["totalCount"] = paginator.count  # 数据的总条数
        response["totalPage"] = paginator.num_pages  # 数据总页数
        response["numPerPage"] = limit  # 每页显示的条数
        ## 获取指定页码的数据
        try:
            interface_object = paginator.page(page)
        except PageNotAnInteger:  # 如果传入的页面参数不为整数走该分支
            interface_object = paginator.page(1)
        except EmptyPage:  # 如果传入的页面参数为空走该分支
            interface_object = paginator.page(paginator.num_pages)
        response["pageNum"] = interface_object.number  # 当前页面是第几页
        try:
            response['data'] = json.loads(serializers.serialize("json", interface_object.object_list))
            res["data"] = response
            res['message'] = 'success'
            res["code"] = 20000
        except  Exception as e:
            res['message'] = str(e)
            res['code'] = 1
        return JsonResponse(res)
class add_interface(View):
    def post(self,requests):
        '''接口添加'''
        response = {}
        interface_data = json.loads(requests.body.decode())
        if_name = interface_data.get("if_name")  # 接口名称
        prj_id = interface_data.get("project")  # 项目id
        project = Project.objects.get(prj_id=prj_id)  # 项目对象
        url = interface_data.get("if_url")  # 接口url
        exit_obj = Interface.objects.filter(Q(if_url=url) & Q(project=project))
        method = interface_data.get("method")  # 请求方法
        data_type = interface_data.get("data_type")  # 传输类型
        description = interface_data.get("description")  # 接口描述
        request_header_data = interface_data.get("request_header")  # 请求头对象
        request_body_data = interface_data.get("request_body")  # 请求体对象
        response_header_data = interface_data.get("response_header")  # 响应头对象
        response_body_data = interface_data.get("response_body")  # 相应体对象
        if exit_obj:
            response["message"] = '项目名称重复了'
            response["code"] = 00000
        else:
            try:
                if_obj = Interface(if_name=if_name, if_url=url, method=method, data_type=data_type, project=project,
                                   description=description,
                                   request_header_param=request_header_data, request_body_param=request_body_data,
                                   response_header_param=response_header_data, response_body_param=response_body_data
                                   )
                if_obj.save()
                response["code"] = 20000
                response["message"] = '添加成功'
            except Exception as e:
                response['message'] = str(e)
                response["code"] = 10000
        return JsonResponse(response)
class delete_interface(View):
    def get(self, requests):
        '''删除接口(传入接口ID列表)'''
        response = {}
        interface_ids = requests.GET.get('interface_ids')
        interface_ids=interface_ids.split(',')
        for item in interface_ids:
            Interface.objects.filter(if_id=item).delete()
        response['message'] = "删除成功"
        response['code'] = 20000
        return JsonResponse(response)
class update_interface(View):
    def post(self,requests):
        '''编辑接口'''
        response = {}
        interface_id=requests.GET.get("interface_id")  #接口ID
        if_obj=Interface.objects.filter(if_id=interface_id) #实例化的接口对象
        if_data=json.loads(requests.body.decode())   #对于前端传入的form中的数据做json解码处理
        project_id=if_data.get("project")  #项目ID
        project_obj=Project.objects.get(prj_id=project_id)
        url = if_data.get("if_url")  #URL
        exit_obj=Interface.objects.filter(Q(if_url=url)&Q(project=project_obj)) #判断修改后的数据是否已经存在（URL和项目对象）
        if exit_obj and url!=if_obj[0].if_url and project_id!=if_obj[0].project_id:
            response["message"] = "该项目名称已经存在"
            response["code"] = 00000
        else:
            try:
                if_name = if_data.get("if_name")  # 接口名称
                description=if_data.get("description") #描述
                method=if_data.get("method")  #请求方法
                data_type=if_data.get("data_type") #传输类型
                request_header=if_data.get("request_header") #请求头
                request_body = if_data.get("request_body")  # 请求体
                response_header = if_data.get("response_header")  #响应头
                response_body = if_data.get("response_body")  # 响应体
                if_obj.update(if_name=if_name, if_url=url, method=method, data_type=data_type, project=project_obj,
                                   description=description,
                                   request_header_param=request_header, request_body_param=request_body,
                                   response_header_param=response_header, response_body_param=response_body
                                   )
                response["message"] = "更新成功"
                response["code"] = 20000
            except Exception as e:
                response["message"] = str(e)
                response["code"] = 10000
        return JsonResponse(response)
class download_file(View):
    '''下载模版的接口'''
    def get(self,requests):
        file=open(os.path.join(BASE_DIR,'static/file','接口模版.xlsx'),'rb')
        response=FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition']='filename="template.xlsx"'
        return response
class upload_interface_templete(View):
    '''文件上传接口'''
    def post(self,requests):
        #1.先进行上传文件的获取
        file_obj=requests.FILES.get('file')
        if not os.path.exists(UPLOAD_ROOT):
            os.makedirs(UPLOAD_ROOT)
        #2.上传文件的读取然后写入制定位置，返回存放的该位置
        file_path=self.upload_file(file_obj)
        #3.文件解析、校验、写入数据库
        upload_file_obj=excelOpern(file_path,"接口")
        for file in upload_file_obj.read_excel_rows_dict():
            interface_name = file["接口名称"]
            prject_name = file["所属项目"]
            api = file["api地址"]
            method = file["请求方式"]
            contenttype = file["数据传输方式"]
            interface_desc = file["接口描述"]
            request_head = file["请求头"]
            # 重新组装请求头信息
            request_head_list = request_head.split(":")
            request_head_list_all = []
            request_head_dict = {}
            request_head_dict["var_name"] = request_head_list[0]
            request_head_dict["var_remark"] = request_head_list[1]
            request_head_list_all.append(request_head_dict)
            request_body = eval(file["请求体"])
            # 重新组装请求体信息
            request_body_list_all = []
            for body in request_body.items():
                request_body_dict = {}
                for item in range(len(body)):
                    if item == 0:
                        request_body_dict["var_name"] = body[item]
                    elif item == 1:
                        request_body_dict["var_remark"] = body[item]
                request_body_list_all.append(request_body_dict)
            response_body = eval(file["响应体"])
            # 重新组装相应体信息
            response_body_list_all = []
            for body in response_body.items():
                response_body_dict = {}
                for item in range(len(body)):
                    if item == 0:
                        response_body_dict["var_name"] = body[item]
                    elif item == 1:
                        response_body_dict["var_remark"] = body[item]
                response_body_list_all.append(response_body_dict)
            # 重新组装相应头信息，暂时为空
            response_head = file["响应头"]
            if not response_head:
                response_head=[]
            #把存的值入数据库
            if not all([interface_name, prject_name, api, method, contenttype, request_head_list_all,
                        response_body_list_all]):
                return JsonResponse({'code': 1, "message": "文件有必输项目为空"})
            try:
                project = Project.objects.get(prj_name=prject_name)  # 项目对象
            except Exception as e:
                return JsonResponse({'code': 1, "message": "文件中项目名称有误"})
            exit_obj = Interface.objects.filter(Q(if_url=api) & Q(project=project) & Q(if_name=interface_name))
            if exit_obj:
                return JsonResponse({'code': 1, "message": "接口已经存在"})

            if_obj = Interface(if_name=interface_name, if_url=api, method=method, data_type=contenttype,
                               project=project,
                               description=interface_desc,
                               request_header_param=json.dumps(request_head_list_all),
                               request_body_param=json.dumps(request_body_list_all),
                               response_header_param=json.dumps(response_head),
                               response_body_param=json.dumps(response_body_list_all)
                               )
            if_obj.save()
        return JsonResponse({'code': 0, "message": "文件导入成功！"})
    def upload_file(self,file_obj):
        if file_obj is None:
            return JsonResponse({'code': 1, "message": "上传的文件为空！"})
        # 循环二进制文件写入 chunk方法是块级读取写入文件
        file_path=os.path.join(BASE_DIR, UPLOAD_ROOT, file_obj.name)
        f = open(file_path, 'wb')
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        return file_path
class get_interface_contnet(View):
    def post(self,requests):
        res = {}
        interface_data = json.loads(requests.body.decode())
        if_id = interface_data.get("if_id")
        prj_id = interface_data.get("prj_id")
        if if_id and if_id!="undefined":
            res["if_id"] = if_id
            res["if_name"]=Interface.objects.get(if_id=if_id).if_name
            res["header"]=eval(Interface.objects.get(if_id=if_id).request_header_param)
            res["body"]=eval(Interface.objects.get(if_id=if_id).request_body_param)
            res["response_header"]=eval(Interface.objects.get(if_id=if_id).response_header_param)
            res["response_body"]=eval(Interface.objects.get(if_id=if_id).response_body_param)
            res["extract"]=[]
            res["validators"] = []
            res["code"] = 20000
            list(res)
        else:
            try:
                res['data'] = list(Interface.objects.filter(project_id=prj_id).values('if_id', 'if_name'))
                res["code"] = 20000
            except Exception as e:
                res['message'] = str(e)
                res['code'] = 1
        return JsonResponse(res)
#---------------------------用 例 管 理-------------------------
class get_testcase(View):
    def post(self,requests):
        '''获取用例管理列表视图'''
        response = {}
        res = {}
        # 获取前端传入的参数，并进行格式化处理
        testcase_data_parm = json.loads(requests.body.decode())
        case_name = testcase_data_parm.get("case_name")
        project = testcase_data_parm.get("project")
        if case_name and case_name != "undefined" and project and project !="undefined":
            testcase_obj = Case.objects.filter(case_name=case_name,project_id=project)
        elif case_name and case_name != "undefined":
            testcase_obj = Case.objects.filter(case_name=case_name)
        elif project and project !="undefined":
            testcase_obj = Case.objects.filter(project_id=project)
        else:
            testcase_obj = Case.objects.filter()
        page = testcase_data_parm.get("page")  # 前端请求的哪一页
        limit = testcase_data_parm.get("limit")  # 前段传入的每页显示的条数
        paginator = Paginator(testcase_obj, limit)  # 创建分页实例
        response["totalCount"] = paginator.count  # 数据的总条数
        response["totalPage"] = paginator.num_pages  # 数据总页数
        response["numPerPage"] = limit  # 每页显示的条数
        ## 获取指定页码的数据
        try:
            testcase_object = paginator.page(page)
        except PageNotAnInteger:  # 如果传入的页面参数不为整数走该分支
            testcase_object = paginator.page(1)
        except EmptyPage:  # 如果传入的页面参数为空走该分支
            testcase_object = paginator.page(paginator.num_pages)
        response["pageNum"] = testcase_object.number  # 当前页面是第几页
        try:
            response['data'] = json.loads(serializers.serialize("json", testcase_object.object_list))
            res["data"] = response
            res['message'] = 'success'
            res["code"] = 20000
        except  Exception as e:
            res['message'] = str(e)
            res['code'] = 1
        return JsonResponse(res)
    def get(self,requests):
        res = {}
        response={}
        testcase_id = requests.GET.get("testcase_id")
        try:
            testcase = Case.objects.get(case_id=testcase_id)
            response["testcase_id"]=testcase_id
            response["case_name"] = testcase.case_name
            response["description"] = testcase.description
            response["project"] = testcase.project_id
            response["content"] = eval(testcase.content)
            res['data'] =response
            res['message'] = 'success'
            res["code"] = 20000
        except Exception as e:
            res['message'] = str(e)
            res['code'] = 1
        return JsonResponse(res)
class add_testcase(View):
    def post(self,requests):
        '''接口用例'''
        response = {}
        testcase_data = json.loads(requests.body.decode())
        case_name = testcase_data.get("case_name")  # 用例名称
        prj_id = testcase_data.get("project")  # 项目id
        project = Project.objects.get(prj_id=prj_id)  # 项目对象
        description = testcase_data.get("description")  # 用例描述
        content = testcase_data.get("content")  # 用例content
        exit_obj = Case.objects.filter(case_name=case_name, project=project)
        if exit_obj:
            response["message"] = '项目名称重复了'
            response["code"] = 00000
        else:
            try:
                testcase_obj= Case(case_name=case_name,project=project,description=description,content=content)
                testcase_obj.save()
                response["code"] = 20000
                response["message"] = '添加成功'
            except Exception as e:
                response['message'] = str(e)
                response["code"] = 10000
        return JsonResponse(response)
class del_testcase(View):
    def get(self,requests):
        '''测试用例的删除接口，支持单个和批量删除'''
        response={}
        testcase_ids=requests.GET.get("testcase_ids")
        for item in testcase_ids.split(','):
            Case.objects.filter(case_id=item).delete()
        response['code']=20000
        response['message']="删除成功"
        return JsonResponse(response)
class update_interface(View):
    def post(self,requests):
        '''编辑接口'''
        response = {}
        testcase_id=requests.GET.get("testcase_id")
        testcase_obj=Case.objects.filter(case_id=testcase_id)
        testcase_data = json.loads(requests.body.decode())
        case_name = testcase_data.get("case_name")  # 用例名称
        prj_id = testcase_data.get("project")  # 项目id
        project = Project.objects.get(prj_id=prj_id)  # 项目对象
        description = testcase_data.get("description")  # 用例描述
        content = testcase_data.get("content")  # 用例content
        try:
            testcase_obj.update(case_name=case_name, project=project, description=description, content=content)
            response["code"] = 20000
            response["message"] = '添加成功'
        except Exception as e:
            response['message'] = str(e)
            response["code"] = 10000
        return JsonResponse(response)
class case_run(View):
    def post(self,requests):
        response={}
        case_data=json.loads(requests.body.decode())
        case_id=case_data.get('case_id')  #用例ID
        env_id = case_data.get('env_id')  # 环境ID
        try:
            execute = Execute(case_id, env_id)  # 实例化执行类得到execute()对象
            execute_result = execute.run_case()  # 执行后的结果
            response['data']=execute_result
            response['message'] = '调试完成'
            response["code"] = 20000
        except Exception as e:
            response['message'] = str(e)
            response["code"] = 10000
        return JsonResponse(response)
class get_case(View):
    def get(self, requests):
        res = {}
        try:
            res['data'] = list(Case.objects.all().values('case_id', 'case_name'))
            res['message'] = 'success'
            res['code'] = 20000
        except Exception as e:
            res['message'] = str(e)
            res['code'] = 1
        return JsonResponse(res)
#---------------------------get 环境、接口、项目-------------------------
class get_project_interface_case_byprjid(View):
    def get(self,requests):
        response={}
        request_type = requests.GET.get("type")
        prj_id = requests.GET.get("prj_id")
        # 通过项目ID查找项目下的接口
        if request_type == "get_if_by_prj_id":
            interface = Interface.objects.filter(project=Project.objects.get(prj_id=prj_id)).values()
            # 查询并将结果转换成json
            response['data'] = list(interface)
            response['code'] = 20000
            response['message'] = 'success'
            return JsonResponse(response,safe=False)
        # 通过项目ID查找项目下的环境
        elif request_type == "get_env_by_prj_id":
            env = Environment.objects.filter(Q(project=Project.objects.get(prj_id=prj_id)) & Q(status=1)).values('env_id','env_name')
            response['data'] = list(env)
            response['code'] = 20000
            response['message'] = 'success'
            return JsonResponse(response, safe=False)
        # 通过项目ID查找项目下的用例
        elif request_type == "get_tc_by_prj_id":
            tc = Case.objects.filter(project=Project.objects.get(prj_id=prj_id)).values('case_id','case_name')
            response['data'] = list(tc)
            response['code'] = 20000
            response['message'] = 'success'
            return JsonResponse(response, safe=False)
        elif request_type == "get_plan_by_prjandenv":
            env_id = requests.GET.get("env_id")
            plan=Plan.objects.filter(Q(project=Project.objects.get(prj_id=prj_id)) & Q(env=Environment.objects.get(env_id=env_id))).values('plant_id','plant_name')
            response['data'] = list(plan)
            response['code'] = 20000
            response['message'] = 'success'
            return JsonResponse(response, safe=False)
        elif request_type == "get_user_by_prj":
            task_id = requests.GET.get("task_id")
            task = Taste.objects.get(taste_id=task_id)
            # project_id=task.project.prj_id
            '''通过项目id查找对应的用户,基于双下划线的一对多反向查询'''
            # user_objs=Project.objects.filter(prj_id=prj_id).values("user__user_id","user__username")
            '''基于双下划线的一对多正向查询'''
            user_objs = User.objects.filter(project__prj_id=task.project_id).values("user_id", "username")
            response['data'] = list(user_objs)
            response['code'] = 20000
            response['message'] = 'success'
            return JsonResponse(response, safe=False)
#---------------------------测 试 计 划-----------------------------
class get_plan(View):
    def post(self,requests):
        '''获取计划管理列表视图'''
        response = {}
        res = {}
        # 获取前端传入的参数，并进行格式化处理
        testplan_data_parm = json.loads(requests.body.decode())
        testplan_name = testplan_data_parm.get("plan_name")
        project = testplan_data_parm.get("project")
        if testplan_name and testplan_name != "undefined" and project and project != "undefined":
            plan = Plan.objects.filter(plant_name=testplan_name, project_id=project)
        elif testplan_name and testplan_name != "undefined":
            plan = Plan.objects.filter(plant_name=testplan_name)
        elif project and project != "undefined":
            plan = Plan.objects.filter(project_id=project)
        else:
            plan = Plan.objects.filter()
        page = testplan_data_parm.get("page")  # 前端请求的哪一页
        limit = testplan_data_parm.get("limit")  # 前段传入的每页显示的条数
        paginator = Paginator(plan, limit)  # 创建分页实例
        response["totalCount"] = paginator.count  # 数据的总条数
        response["totalPage"] = paginator.num_pages  # 数据总页数
        response["numPerPage"] = limit  # 每页显示的条数
        ## 获取指定页码的数据
        try:
            plan_object = paginator.page(page)
        except PageNotAnInteger:  # 如果传入的页面参数不为整数走该分支
            plan_object = paginator.page(1)
        except EmptyPage:  # 如果传入的页面参数为空走该分支
            plan_object = paginator.page(paginator.num_pages)
        response["pageNum"] = plan_object.number  # 当前页面是第几页
        try:
            response['data'] = json.loads(serializers.serialize("json", plan_object.object_list))
            for item in response['data']:
                item["fold"]=True
            res["data"] = response
            res['message'] = 'success'
            res["code"] = 20000
        except  Exception as e:
            res['message'] = str(e)
            res['code'] = 1
        return JsonResponse(res)
    def get(self,requests):
        res = {}

        plan_id = requests.GET.get("plan_id")
        try:
            plan_obj = Plan.objects.filter(plant_id=plan_id)
            res['data'] = json.loads(serializers.serialize("json", plan_obj))
            # res['data'] = response
            res['message'] = 'success'
            res["code"] = 20000
        except Exception as e:
            res['message'] = str(e)
            res['code'] = 1
        return JsonResponse(res)
class add_plan(View):
    def post(self,requests):
        '''添加测试计划的视图'''
        response = {}
        # 获取前端传入的参数，并进行格式化处理
        testplan_data_parm = json.loads(requests.body.decode())
        testplan_name=testplan_data_parm.get("plant_name") #计划名称
        project_id=testplan_data_parm.get("project")        #项目
        project_obj=Project.objects.get(prj_id=project_id)
        env_id=testplan_data_parm.get("env")                #环境
        env_obj=Environment.objects.get(env_id=env_id)
        description=testplan_data_parm.get("description")   #描述
        case_list=testplan_data_parm.get("case_list")      #用例列表
        try:
            plan_obj=Plan(plant_name=testplan_name,project=project_obj,env=env_obj,description=description,content=case_list)
            plan_obj.save()
            response["code"] = 20000
            response["message"] = '添加成功'
        except Exception as e:
            response['message'] = str(e)
            response["code"] = 10000
        return JsonResponse(response)
class update_plan(View):
    def post(self, requests):
        '''编辑接口'''
        response = {}
        testplan_id = requests.GET.get("testplan_id")
        plan_obj = Plan.objects.filter(plant_id=testplan_id)
        testplan_data_parm = json.loads(requests.body.decode())
        testplan_name = testplan_data_parm.get("plant_name")  # 计划名称
        project_id = testplan_data_parm.get("project")  # 项目
        project_obj = Project.objects.get(prj_id=project_id)
        env_id = testplan_data_parm.get("env")  # 环境
        env_obj = Environment.objects.get(env_id=env_id)
        description = testplan_data_parm.get("description")  # 描述
        case_list = testplan_data_parm.get("case_list")  # 用例列表
        try:
            plan_obj.update(plant_name=testplan_name,project=project_obj,env=env_obj,description=description,content=case_list)
            response["code"] = 20000
            response["message"] = '更新成功'
        except Exception as e:
            response['message'] = str(e)
            response["code"] = 10000
        return JsonResponse(response)
class delete_plan(View):
    def get(self,requests):
        '''删除接口'''
        response={}
        testplan_id=requests.GET.get("testplan_id")
        Plan.objects.filter(plant_id=testplan_id).delete()
        response['message'] = "删除成功"
        response['code'] = 20000
        return JsonResponse(response)
class getenv(View):
    def get(self, requests):
        res = {}
        try:
            res['data'] = list(Environment.objects.all().values('env_id', 'env_name'))
            res['message'] = 'success'
            res['code'] = 20000
        except Exception as e:
            res['message'] = str(e)
            res['code'] = 1
        return JsonResponse(res)
class run_plan(View):
    def get(self,requests):
        response={}
        plan_id=requests.GET.get("plan_id")
        plan = Plan.objects.get(plant_id=plan_id)
        env = plan.env.env_id  # 计划对象对应的环境
        content = eval(plan.content)  # 计划对应的content
        case_num = len(content)  # 测试用例数
        pass_num = 0  # 用例通过数
        fail_num = 0  # 用例失败数
        error_num = 0  # 用例错误数
        case_list = []  # 测试计划中测试用例集
        try:
            for case_obj in content:
                execute_obj=Execute(case_obj,env)
                run_result = execute_obj.run_case()
                case_list.append(run_result)
                if run_result["result"] == "pass":
                    pass_num+=1
                elif run_result["result"] == "fail":
                    fail_num+=1
                else:
                    error_num += 1
            report_name = plan.plant_name + "-" + time.strftime("%Y%m%d%H%M%S")
            if Report.objects.filter(plant=plan):
               Report.objects.filter(plant=plan).update(report_name=report_name,plant=plan,content=case_list,case_num=case_num,
                                                         pass_num=pass_num,fail_num=fail_num,error_num=error_num,task=None)
            else:
               Report(report_name=report_name,plant=plan,content=case_list,case_num=case_num,
                       pass_num=pass_num,fail_num=fail_num,error_num=error_num,task=None).save()
            response['code'] = 20000
            response['message'] = "%s执行成功!"%plan.plant_name
        except Exception as e:
            response['message'] = str(e)
            response['code'] = 1
        return JsonResponse(response)

#---------------------------测 试 报 告-----------------------------
class get_report(View):
    def get(self,requests):
        res={}
        response={}
        flag=requests.GET.get('flag')    #测试报告对应的测试计划
        id=requests.GET.get('id')    #测试报告对应的测试计划
        if flag=="plan":
            plan = Plan.objects.get(plant_id=id)
            report = Report.objects.get(plant=plan)  # report对象
        elif flag=="report":
            report = Report.objects.get(report_id=id)  # report对象
        elif flag == "task":
            task_obj = Taste.objects.get(taste_id=id)
            report = Report.objects.filter(task=task_obj).order_by('-report_id').first()
        try:
            response["report_name"] = report.report_name
            response["content"] = eval(report.content)
            response["case_num"] = report.case_num
            response["pass_num"] = report.pass_num
            response["fail_num"] = report.fail_num
            response["error_num"] = report.error_num
            res['data'] = response
            res['message'] = 'success'
            res["code"] = 20000
            list(res)
        except Exception as e:
            res['message'] = str(e)
            res['code'] = 1
        return JsonResponse(res)
class getreport(View):
    def post(self,requests):
        response = {}
        res = {}
        # 获取前端传入的参数，并进行格式化处理
        report_data_parm = json.loads(requests.body.decode())
        planname=report_data_parm.get("planname")
        # plan = Plan.objects.filter(plant_name=planname)
        taskname = report_data_parm.get("taskname")
        task=Taste.objects.filter(taste_name=taskname).first()
        if planname and planname != "undefined" and taskname and taskname != "undefined":
            report_obj = Report.objects.filter(report_name=planname,task=task).order_by('-report_id')
        elif planname and planname != "undefined":
            report_obj = Report.objects.filter(report_name=planname).order_by('-report_id')
        elif taskname and taskname != "undefined":
            report_obj = Report.objects.filter(task=task).order_by('-report_id')
        else:
            report_obj = Report.objects.filter().order_by('-report_id')
        page = report_data_parm.get("page")  # 前端请求的哪一页
        limit = report_data_parm.get("limit")  # 前段传入的每页显示的条数
        paginator = Paginator(report_obj, limit)  # 创建分页实例
        response["totalCount"] = paginator.count  # 数据的总条数
        response["totalPage"] = paginator.num_pages  # 数据总页数
        response["numPerPage"] = limit  # 每页显示的条数
        ## 获取指定页码的数据
        try:
            testreport_object = paginator.page(page)
        except PageNotAnInteger:  # 如果传入的页面参数不为整数走该分支
            testreport_object = paginator.page(1)
        except EmptyPage:  # 如果传入的页面参数为空走该分支
            testreport_object = paginator.page(paginator.num_pages)
        response["pageNum"] = testreport_object.number  # 当前页面是第几页
        try:
            response['data'] = json.loads(serializers.serialize("json", testreport_object.object_list))
            res["data"] = response
            res['message'] = 'success'
            res["code"] = 20000
        except  Exception as e:
            res['message'] = str(e)
            res['code'] = 1
        return JsonResponse(res)
class delete_report(View):
    def get(self, requests):
        '''删除接口(传入接口ID列表)'''
        response = {}
        report_ids = requests.GET.get('report_ids')
        report_ids=report_ids.split(',')
        for item in report_ids:
            Report.objects.filter(report_id=item).delete()
        response['message'] = "删除成功"
        response['code'] = 20000
        return JsonResponse(response)


















