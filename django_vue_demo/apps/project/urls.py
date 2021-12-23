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
from apps.project.views import get_Projects,add_Projects,delete_Projects,update_Projects,search_Projects
urlpatterns = [
    #项目
    url(r'^get_Projects$',get_Projects.as_view(),name='get_Projects'),   #获取项目列表
    url(r'^add_Projects$',add_Projects.as_view(),name='add_Projects'),   #get获取添加项目页面，post添加项目信息
    url(r'^delete_Projects$',delete_Projects.as_view(),name='delete_Projects'),   #删除项目
    url(r'^update_Projects$',update_Projects.as_view(),name='update_Projects'),   #编辑项目
    url(r'^search_Projects$',search_Projects.as_view(),name='search_Projects')   #搜索项目接口

]
