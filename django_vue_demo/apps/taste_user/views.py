from django.shortcuts import render
import json,datetime,time
from lib.common import get_time_by_nexttime,time_add,split_nextrun_time
from django.views.generic import View
from django.http import JsonResponse
from lib.sendtaskemail import send_email
from lib.execute import Execute
from django.db.models import Q
from lib.task import diango_task
from django.core import serializers
from apps.taste_user.models import Taste,User
from apps.project.models import Project
from apps.env.models import Environment
from apps.apitest.models import Plan,Report,Case
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
class get_task(View):
    def get(self,requests):
        res = {}
        task_id=requests.GET.get("task_id")
        if task_id:
            try:
                task = Taste.objects.filter(taste_id=task_id)
                res['data'] = json.loads(serializers.serialize("json", task))
                # res['data'] = response
                res['message'] = 'success'
                res["code"] = 20000
            except Exception as e:
                res['message'] = str(e)
                res['code'] = 1
        else:
            try:
                res['data'] = list(Taste.objects.all().values('taste_id', 'taste_name'))
                res['message'] = 'success'
                res['code'] = 20000
            except Exception as e:
                res['message'] = str(e)
                res['code'] = 1
        return JsonResponse(res)
    def post(self,requests):
        '''获取定时任务列表视图'''
        response = {}
        res = {}
        # 获取前端传入的参数，并进行格式化处理
        task_data_parm = json.loads(requests.body.decode())
        tesk_name = task_data_parm.get("taskname")
        project = task_data_parm.get("project")
        if tesk_name and tesk_name != "undefined" and project and project != "undefined":
            task = Taste.objects.filter(taste_name=tesk_name, project_id=project)
        elif tesk_name and tesk_name != "undefined":
            task = Taste.objects.filter(taste_name=tesk_name)
        elif project and project != "undefined":
            task = Taste.objects.filter(project_id=project)
        else:
            task = Taste.objects.filter()
        page = task_data_parm.get("page")  # 前端请求的哪一页
        limit = task_data_parm.get("limit")  # 前段传入的每页显示的条数
        paginator = Paginator(task, limit)  # 创建分页实例
        response["totalCount"] = paginator.count  # 数据的总条数
        response["totalPage"] = paginator.num_pages  # 数据总页数
        response["numPerPage"] = limit  # 每页显示的条数
        ## 获取指定页码的数据
        try:
            task_object = paginator.page(page)
        except PageNotAnInteger:  # 如果传入的页面参数不为整数走该分支
            task_object = paginator.page(1)
        except EmptyPage:  # 如果传入的页面参数为空走该分支
            task_object = paginator.page(paginator.num_pages)
        response["pageNum"] = task_object.number  # 当前页面是第几页
        try:
            response['data'] = json.loads(serializers.serialize("json", task_object.object_list))
            for item in response['data']:
                item["fold"] = True
            res["data"] = response
            res['message'] = 'success'
            res["code"] = 20000
        except  Exception as e:
            res['message'] = str(e)
            res['code'] = 1
        return JsonResponse(res)
class add_task(View):
    def post(self,requests):
        '''添加测试任务的视图'''
        response = {}
        # 获取前端传入的参数，并进行格式化处理
        testtask_data_parm = json.loads(requests.body.decode())
        task_name=testtask_data_parm.get("taste_name") #任务名称
        project=testtask_data_parm.get("project")  # 项目
        env=testtask_data_parm.get("env")  # 环境
        plan_list=testtask_data_parm.get("plans")  # 计划
        task_obj=Taste.objects.filter(taste_name=task_name,project_id=project,env_id=env,plans=plan_list)
        if task_obj:
            response["message"] = '项目名称重复了'
            response["code"] = 00000
        else:
            try:
                start_time=testtask_data_parm.get("taste_time")  # 执行时间
                description = testtask_data_parm.get("description")  # 描述
                task_obj = Taste(taste_name=task_name, project_id=project, env_id=env, plans=plan_list,taste_time=start_time,description=description)
                task_obj.save()
                response["code"] = 20000
                response["message"] = '添加成功'
            except Exception as e:
                response['message'] = str(e)
                response["code"] = 10000
        return JsonResponse(response)
class delete_task(View):
    def get(self, requests):
        '''删除接口(传入任务ID列表)'''
        response = {}
        task_ids = requests.GET.get('task_ids')
        task_ids=task_ids.split(',')
        for item in task_ids:
            Taste.objects.filter(taste_id=item).delete()
        response['message'] = "删除成功"
        response['code'] = 20000
        return JsonResponse(response)
class update_task(View):
    def post(self, requests):
        '''更新接口'''
        response = {}
        task_id=requests.GET.get("task_id")
        task_obj=Taste.objects.filter(taste_id=task_id)
        task_parms=json.loads(requests.body.decode())
        taste_name=task_parms.get("taste_name")  #任务名称
        project_id=task_parms.get("project")     #项目
        project_obj = Project.objects.get(prj_id=project_id)
        env_id=task_parms.get("env")             #环境
        env_obj = Environment.objects.get(env_id=env_id)
        description=task_parms.get("description") #描述
        taste_time=task_parms.get("taste_time")   #任务时间
        plans=task_parms.get("plans")   #任务对应的测试计划
        try:
            task_obj.update(taste_name=taste_name, project=project_obj, env=env_obj, plans=plans,taste_time=taste_time,description=description)
            response["code"]=20000
            response["message"]='更新成功'
        except Exception as e:
            response["code"]=10000
            response["message"]=str(e)
        return JsonResponse(response)
class get_next_runtime(View):
    '''获取下次运行日期'''
    def get(self,requests):
        task_id=requests.GET.get("task_id")
        task_obj=Taste.objects.filter(taste_id=task_id).values("taste_time")
        cron=list(task_obj)[0].get("taste_time")
        status = Taste.objects.filter(taste_id=task_id).values("status")
        if list(status)[0].get("status")==0 or list(status)[0].get("status")==2:
            num = get_time_by_nexttime(cron)
            new_date = split_nextrun_time(time_add(cron, datetime.timedelta(days=num)))
            return JsonResponse({'code':20000,"message":"现在启动后下次的运行时间为："+new_date})
        elif list(status)[0].get("status")==1 or list(status)[0].get("status")==3:
            num = get_time_by_nexttime(cron)
            new_date = split_nextrun_time(time_add(cron,datetime.timedelta(days=num)))
            return JsonResponse({'code':20000,"message":new_date})
        else:
            return JsonResponse({'code':10000,"message":"获取下次运行时间失败!!!"})
class run_once(View):
    def get(self,requests):
        '''运行一次'''
        user = requests.GET.get("user")  # 用户ID
        task_id = requests.GET.get("task_id")  # 任务ID
        task_obj = Taste.objects.get(taste_id=task_id)  # 任务对象
        task_report_obj = run_task(user, task_obj)
        # 有错误报告则发送邮件
        if task_report_obj.fail_num > 0 or task_report_obj.error_num > 0:
            return JsonResponse({"code": 20000, "message": "有失败或者错误的批次任务,请移至邮件查看详情！！！"})
        else:
            return JsonResponse({"code": 20000, "message": "测试报告已经生成,可在测试报告管理模块查看。"})
def run_task(user_id,task_obj):
    '''
    运行测试任务，生成对应的report
    :param task_id: 任务ID
    :return: 实例化后的report对象
    '''
    user_obj = User.objects.get(user_id=user_id)
    # task_obj = Taste.objects.get(taste_id=task_id)  # 任务对象
    env_id = task_obj.env.env_id  # 任务对象对应的环境
    plans = eval(task_obj.plans)  # 任务对应的计划list
    case_nums = 0  # 用例总数
    pass_num = 0  # 用例通过数
    fail_num = 0  # 用例失败数
    error_num = 0  # 用例错误数
    case_list = []  # 用例结果大list
    plan_obj_zanshi = None
    for plan in plans:
        plan_obj = Plan.objects.get(plant_id=plan)
        cases = eval(plan_obj.content)
        case_nums += len(cases)
        for case in cases:
            execute_obj = Execute(case, env_id)
            run_result = execute_obj.run_case()
            case_list.append(run_result)
            if run_result["result"] == "pass":
                pass_num += 1
            elif run_result["result"] == "fail":
                fail_num += 1
            else:
                error_num += 1
    report_name = task_obj.taste_name + "-" + time.strftime("%Y%m%d%H%M%S")
    task_report_obj = Report(report_name=report_name, plant=plan_obj_zanshi, content=case_list, case_num=case_nums,
                             pass_num=pass_num, fail_num=fail_num, error_num=error_num, task=task_obj)
    task_report_obj.save()
    send_email(user_obj.email, "http://127.0.0.1:9529/", task_report_obj.task_id)
    return task_report_obj
class run(View):
    def post(self,requests):
        '''
        开启、关闭、重启 任务
        :param requests:1开启、2和4暂停、3重启    models:(0,'STOP'),(1,'RUNNING'),(2, 'PAUSE'),(3,'RESUME')
        :return: 返回message信息供前台弹框展示
        :return:
        '''
        data_parm = json.loads(requests.body.decode())
        status_flag =data_parm.get("flag")
        user = data_parm.get("user")  # 用户ID
        task_id = data_parm.get("task_id")  # 任务ID
        task_obj = Taste.objects.get(taste_id=task_id)  # 任务对象
        time_obj = str(task_obj.taste_time).split(" ")
        hour=time_obj[1].split(':')[0]
        minute = time_obj[1].split(':')[1]
        # 任务对象
        uuid = "定时任务" + str(task_id)
        task = diango_task()  # 实例化定时任务对象
        task.addtask(run_task, uuid, hour, minute, user, task_obj)
        if status_flag == 1:
            task.starttask()  # 开始定时执行
            Taste.objects.filter(taste_id=task_id).update(status=1)  # 更改状态为running
            return JsonResponse({"code": 20000,"message":"定时任务启动成功！"})
        elif status_flag == 2 or status_flag == 4:
            task.pausejob(uuid)  # 暂停任务
            Taste.objects.filter(taste_id=task_id).update(status=2)  # 更改状态pause
            return JsonResponse({"code": 20000,"message":"定时任务已暂停！"})
        elif status_flag == 3:
            task.resumejob(uuid)  # 重启任务
            Taste.objects.filter(taste_id=task_id).update(status=3)  # 更改状态resume
            return JsonResponse({"code": 20000,"message":"定时任务已重启！"})
        else:
            task.removejob(uuid)
            return JsonResponse({"code": 20000,"message":"定时任务操作失败！"})

#--------------------------首页----------------------
class getnumber_prj_env_case_report(View):
    def get(self,requests):
        response={}
        res={}
        try:
            prj_num=Project.objects.all().count()
            res["project_num"] = prj_num
            env_num=Environment.objects.all().count()
            res["env_num"] = env_num
            case_num=Case.objects.all().count()
            res["case_num"] = case_num
            report_num=Report.objects.all().count()
            res["report_num"]=report_num
            response["data"]=res
            response["code"] = 20000
            response["message"] = "查询完成"
        except Exception as e:
            response["code"]=10000
            response["message"]=str(e)
        return JsonResponse(response)
class get_num_byechart(View):
    def get(self,requests):
        res={}
        response={}
        month=[]
        pass_num = []
        fail_num = []
        error_num = []
        try:
            if Report.objects.filter(Q(task_id__isnull=False) & Q(report_name__contains="-202105")).count() >0:
                month.append("五月")
                num1=Report.objects.filter(Q(task_id__isnull=False) & Q(report_name__contains="-202105") & Q(error_num__exact=0) & Q(fail_num__exact=0)).count()
                pass_num.append(num1)
                num2 = Report.objects.filter(Q(task_id__isnull=False) & Q(report_name__contains="-202105") & Q(fail_num__gte=1)).count()
                fail_num.append(num2)
                num3 = Report.objects.filter(Q(task_id__isnull=False) & Q(report_name__contains="-202105") & Q(error_num__gte=1)).count()
                error_num.append(num3)
            if Report.objects.filter(Q(task_id__isnull=False) & Q(report_name__contains="-202106")).count() >0:
                month.append("六月")
                num1=Report.objects.filter(Q(task_id__isnull=False) & Q(report_name__contains="-202106") & Q(error_num__exact=0) & Q(fail_num__exact=0)).count()
                pass_num.append(num1)
                num2 = Report.objects.filter(Q(task_id__isnull=False) & Q(report_name__contains="-202106") & Q(fail_num__gte=1)).count()
                fail_num.append(num2)
                num3 = Report.objects.filter(Q(task_id__isnull=False) & Q(report_name__contains="-202106") & Q(error_num__gte=1)).count()
                error_num.append(num3)
            if Report.objects.filter(Q(task_id__isnull=False) & Q(report_name__contains="-202107")).count() >0:
                month.append("七月")
                num1=Report.objects.filter(Q(task_id__isnull=False) & Q(report_name__contains="-202107") & Q(error_num__exact=0) & Q(fail_num__exact=0)).count()
                pass_num.append(num1)
                num2 = Report.objects.filter(Q(task_id__isnull=False) & Q(report_name__contains="-202107") & Q(fail_num__gte=1)).count()
                fail_num.append(num2)
                num3 = Report.objects.filter(Q(task_id__isnull=False) & Q(report_name__contains="-202107") & Q(error_num__gte=1)).count()
                error_num.append(num3)
            res["month"]=month
            res["pass_num"] = pass_num
            res["fail_num"] = fail_num
            res["error_num"] = error_num
            response["data"]=res
            response["code"]=20000
        except Exception as e:
            response["data"] = str(e)
            response["code"] = 10000
        return JsonResponse(response)









