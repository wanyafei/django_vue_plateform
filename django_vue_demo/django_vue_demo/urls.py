"""django_vue_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^project/', include(('apps.project.urls','project'), namespace='project')),  # 项目模块
    url(r'^env/', include(('apps.env.urls','env'), namespace='env')),  # 环境管理模块
    url(r'^apitest/', include(('apps.apitest.urls', 'apitest'), namespace='apitest')),  # 环境管理模块
    url(r'^api/', include(('apps.demo.urls','demo'),namespace='demo')), #demo
    url(r'^taste_user/', include(('apps.taste_user.urls', 'taste_user'), namespace='taste_user')),  # 测试任务
    url(r'^$', TemplateView.as_view(template_name="index.html")),
]
