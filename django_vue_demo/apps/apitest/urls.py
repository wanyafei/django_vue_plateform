"""daily URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.conf.urls import url
from apps.apitest.views import get_interface,get_project_parm,add_interface,delete_interface,update_interface,download_file
from apps.apitest.views import upload_interface_templete,get_interface_contnet
from apps.apitest.views import get_testcase,add_testcase,del_testcase,get_project_interface_case_byprjid,case_run,get_case
from apps.apitest.views import get_plan,add_plan,update_plan,delete_plan,getenv,run_plan,get_report,getreport,delete_report
urlpatterns = [
    #接口URL
    url(r'^get_project$',get_project_parm.as_view(), name='get_project_parm'),  # 获取项目参数
    url(r'^get_interface$',get_interface.as_view(),name='get_interface'),   #获取接口列表
    url(r'^add_interface$',add_interface.as_view(), name='add_interface'),  # 添加接口
    url(r'^del_interface$',delete_interface.as_view(),name='delete_interface'),   #删除接口
    url(r'^update_interface$',update_interface.as_view(),name='update_interface'),   #编辑接口
    url(r'^download_file$',download_file.as_view(),name='download_file'),   #下载接口
    url(r'^upload_interface_templete$',upload_interface_templete.as_view(),name='upload_interface_templete'), #上传接口
    url(r'^get_interface_contnet$',get_interface_contnet.as_view(), name='get_interface_contnet'),  #获取contents内容接口
    url(r'^get_project_interface_case_byprjid$', get_project_interface_case_byprjid.as_view(), name='get_interface_contnet'),  # 获取contents内容接口

    #用例URL
    url(r'^get_testcase$', get_testcase.as_view(), name='get_testcase'),  # 获取用例列表数据
    url(r'^add_testcase$', add_testcase.as_view(), name='add_testcase'),  # 添加测试用例
    url(r'^del_testcase$', del_testcase.as_view(), name='del_testcase'),  # 删除测试用例
    url(r'^update_interface$', update_interface.as_view(), name='update_interface'),  # 修改测试用例
    url(r'^case_run$', case_run.as_view(), name='case_run'),  # 案例运行接口
    url(r'^get_case$', get_case.as_view(), name='get_case'),  # 获取所有的测试用例

    #测试计划URL
    url(r'^get_plan$', get_plan.as_view(), name='get_plan'),  # 获取测试计划列表数据
    url(r'^add_plan$', add_plan.as_view(), name='add_plan'),  # 添加测试计划
    url(r'^update_plan$', update_plan.as_view(), name='update_plan'),  # 修改测试计划
    url(r'^delete_plan$', delete_plan.as_view(), name='delete_plan'),  # 删除测试计划
    url(r'^getenv$', getenv.as_view(), name='getenv'),  # 删除测试计划
    url(r'^run_plan$', run_plan.as_view(), name='run_plan'),  # 运行测试计划

    #测试报告URL
    url(r'^get_report$', get_report.as_view(), name='get_report'),  # 获取测试报告
    url(r'^getreport$', getreport.as_view(), name='getreport'),  # 报告列表获取测试报告
    url(r'^delete_report$', delete_report.as_view(), name='delete_report'),  # 报告列表获取测试报告

]
