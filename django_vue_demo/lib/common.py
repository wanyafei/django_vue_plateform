import datetime
def get_time_by_nexttime(task_time):
    '''获取定时任务运行时间下次执行日期'''
    num=datetime.datetime.now()
    numss=num-datetime.datetime.strptime(task_time,"%Y-%m-%d %H:%M")
    day = int(numss.days % 365)
    if day>=100:
        return 0
    else:
        return day + 1
def time_add(current_data,num):
    '''日期相加的方法'''
    if isinstance(current_data,str):
        current_data=datetime.datetime.strptime(current_data,"%Y-%m-%d %H:%M")
    return current_data+num
def split_nextrun_time(nextrun_time):
    '''下次运行时间的字符串截取'''
    split_before=str(nextrun_time).split(' ')
    split_after=split_before[1].split(':')
    return split_before[0]+" "+split_after[0]+":"+split_after[1]