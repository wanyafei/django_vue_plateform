import request from '@/utils/request'

// 列表数据
export function getproject(data) {
    return request({
      url:'/project/get_Projects',
      method: 'post',
      data
    })
  }
// 修改弹框反显的数据
export function detail(pro_id){
  return request({
    url:'/project/get_Projects',
    method: 'get',
    params:{pro_id}
  })
}
// 修改接口
export function update(prj_id,data){
  return request({
    url:'/project/update_Projects?prj_id='+prj_id,
    method:'post',
    data
  })
}
// 添加接口
export function add(data){
  return request({
    url:'/project/add_Projects',
    method:'post',
    data
  })
}
//删除接口
export function del(prj_id){
  return request({
    url:'/project/delete_Projects?prj_id='+prj_id,  
    method:'get'
  })
}