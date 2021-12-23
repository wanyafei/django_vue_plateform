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
from apps.taste_user.views import get_task,add_task,delete_task,update_task,get_next_runtime,run_once,run
from apps.taste_user.views import getnumber_prj_env_case_report,get_num_byechart
urlpatterns = [
    #任务
    url(r'^get_task$',get_task.as_view(),name='get_task'),   #获取任务列表
    url(r'^add_task$', add_task.as_view(), name='add_task'),  # 添加任务
    url(r'^delete_task$', delete_task.as_view(), name='delete_task'),  # 删除任务
    url(r'^update_task$', update_task.as_view(), name='update_task'),  # 更新任务
    url(r'^get_next_runtime$', get_next_runtime.as_view(), name='get_next_runtime'),  # 更新任务
    url(r'^run_once$', run_once.as_view(), name='run_once'),  # 运行一次
    url(r'^run$',run.as_view(), name='run'),  # 运行
    #首页概览接口
    url(r'^getnumber_prj_env_case_report$',getnumber_prj_env_case_report.as_view(), name='getnumber_prj_env_case_report'),  # 获取首页概览处的项目、环境、用例、报告数量
    url(r'^get_num_byechart$', get_num_byechart.as_view(),name='get_num_byechart'),  # 获取以x轴为纬度统计每日的通过、失败、错误的报告数


]
