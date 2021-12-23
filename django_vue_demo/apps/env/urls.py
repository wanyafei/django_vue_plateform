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
from apps.env.views import get_env,add_env,delete_env,update_env

urlpatterns = [
    #环境
    url(r'^get_env',get_env.as_view(),name='get_env'),   #获取环境列表
    url(r'^add_env$',add_env.as_view(),name='add_env'),   #get获取添加环境页面，post添加环境信息
    url(r'^update_env$', update_env.as_view(), name='update_env'),  # 编辑环境
    url(r'^delete_env$', delete_env.as_view(), name='delete_env'),  # 删除环境

]
