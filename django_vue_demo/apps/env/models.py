from django.db import models
class Environment(models.Model):
    '''环境模型类'''
    status_choice={
        (0, '失效'),
        (1, '有效')
    }
    env_id=models.AutoField(primary_key=True,null=False,verbose_name='环境id')
    env_name=models.CharField(max_length=50,verbose_name='环境名字')
    url=models.CharField(max_length=100,verbose_name='环境url')
    description=models.CharField(max_length=100,verbose_name='环境描述')
    status=models.SmallIntegerField(default=1,choices=status_choice,verbose_name='环境状态')
    project=models.ForeignKey('project.Project',on_delete=models.CASCADE,verbose_name='项目名称')

    def __str__(self):
        return self.env_name
