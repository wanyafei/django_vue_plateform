from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
class diango_task():
    def __init__(self):
        try:
            # 实例化调度器
            self.scheduler = BackgroundScheduler()
            # self.scheduler = BlockingScheduler()
            # 调度器使用DjangoJobStore()
            self.scheduler.add_jobstore(DjangoJobStore(), "default")
        except Exception as e:
            print(e)
            # 有错误就停止运行
            self.scheduler.shutdown()
    def addtask(self,fun,uuid,hour,minute,user,task):
        '''添加job'''
        return self.scheduler.add_job(fun,"cron", id=uuid,hour=hour,minute=minute,args=[user,task])
    def starttask(self):
        '''开启job'''
        # register_events(self.scheduler)
        self.scheduler.start()
    def gettasks(self):
        self.scheduler.get_jobs()
    def pausejob(self,job_name):
        '''暂停job'''
        self.scheduler.pause_job(job_name)
    def resumejob(self,job_name):
        '''重启job'''
        self.scheduler.resume_job(job_name)
    def removejob(self,job_name):
        '''删除任job'''
        self.scheduler.remove_job(job_name)