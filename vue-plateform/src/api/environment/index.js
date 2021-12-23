import request from '@/utils/request'

// 环境列表的数据
export function getenv(data) {
    return request({
      url:'/env/get_env',
      method: 'post',
      data
    })
  }
export function detail(env_id) {
    return request({
      url:'/env/get_env',
      method: 'get',
      params:{env_id}
    })
  }
export function del(env_id){
    return request({
        url:'/env/delete_env?env_id='+env_id,
        method:'get'
    })
}
export function update(env_id,data){
    return request({
        url:'/env/update_env?env_id='+env_id,
        method:'post',
        data
    })
}
export function add(data){
    return request({
        url:'/env/add_env',
        method:'post',
        data
    })
}