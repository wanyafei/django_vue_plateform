import request from '@/utils/request'
//获取全部的任务
export function get_task() {
    return request({
      url:'/taste_user/get_task',
      method: 'get',
    })
  } 
  
  export function getTask(data) {
    return request({
      url:'/taste_user/get_task',
      method: 'post',
      data
    })
  } 
  //添加路由
  export function add(data) {
    return request({
      url:'/taste_user/add_task',
      method: 'post',
      data
    })
  }  detail
//获取对象详情
export function detail(task_id) {
  return request({
    url:'/taste_user/get_task',
    method: 'get',
    params:{task_id}
  })
} 
//删除路由
export function del(task_ids) {
  return request({
    url:'/taste_user/delete_task?task_ids='+task_ids,
    method: 'get',
  })
} 
//获取对象详情
export function update(task_id,data) {
  return request({
    url:'/taste_user/update_task?task_id='+task_id,
    method: 'post',
    data
  })
} 
export function get_next_runtime(task_id) {
  return request({
    url:'/taste_user/get_next_runtime?task_id='+task_id,
    method: 'get',
  })
} 

export function get_user_byprj(type,task_id) {
  return request({
    url:'/apitest/get_project_interface_case_byprjid?task_id='+task_id+'&type='+type,
    method: 'get'
  })
} 
//运行一次路由
export function runonceurl(user,task) {
  return request({
    url:'/taste_user/run_once?user='+user+'&task_id='+task,
    method: 'get',
  })
} 
//执行定时任务的路由 
export function run_route(data) {
  return request({
    url:'/taste_user/run',
    method: 'post',
    data
  })
} 
