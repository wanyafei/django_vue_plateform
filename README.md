#django_vue_platform
## 技术栈：
        后台：python+dajngo
        数据库：mysql
        前端：vue+element-ui+vuex+vue-route
----------------------------------------------------------------------------------------
## 实现功能：
    restful风格接口的自动化运行、测试报告生成、邮件推送、定时任务等
    
## 后台build:
	# clone the project
	git clone https://github.com/wanyafei/django_vue_plateform.git
    	
	# Install dependent packages
	pip3 install -r requirements.txt
	
	# Database migration
	python3 manage.py makemigrations
	python3 manage.py migrate
	
	# Start project
	python3  manage.py runserver 127.0.0.1:8000

## 前端build
	# clone the project
	git clone https://github.com/wanyafei/django_vue_plateform.git

	# enter the project directory
	cd vue-admin-template

	# install dependency
	npm install

	# develop
	npm run dev
