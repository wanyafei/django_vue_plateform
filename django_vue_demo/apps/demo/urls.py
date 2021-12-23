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
from django.conf.urls import url
from .views import logout,login,info,getuser



urlpatterns = [
    # url(r'add_book$', add_book, ),
    # url(r'show_books$', show_books, ),
    url(r'login$', login.as_view(),name='login', ),   # 登陆
    url(r'info$', info.as_view(),name='info', ),      #info信息
    url(r'^logout',logout.as_view(),name='logout'),   #退出登陆
    url(r'^getuser', getuser.as_view(), name='getuser'),  # 退出登陆
]

