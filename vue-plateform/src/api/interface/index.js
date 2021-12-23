import request from '@/utils/request'

// 列表接口数据
export function getinterface(data) {
    return request({
      url:'/apitest/get_interface',
      method: 'post',
      data
    })
  }
//获取下拉框项目参数
export function getprj() {
    return request({
      url:'/apitest/get_project',
      method: 'get'
    })
  }
// 修改弹框反显的数据
export function detail(if_id) {
    return request({
      url:'apitest/get_interface',
      method: 'get',
      params:{if_id}
    })
  }
// 更新操作
export function update(interface_id,data) {
    return request({
      url:'/apitest/update_interface?interface_id='+interface_id,
      method: 'post',
      data
    })
  }
// 添加操作
export function add(data) {
    return request({
      url:'/apitest/add_interface',
      method: 'post',
      data
    })
  }
// 删除操作
export function del(if_ids) {
    return request({
      url:'/apitest/del_interface?interface_ids='+if_ids,
      method: 'get'
    })
  }   
// 通过项目ID取接口、环境大接口
export function get_project_interface_case_all(prj_id,type) {
  return request({
    url:'/apitest/get_project_interface_case_byprjid?prj_id='+prj_id+'&type='+type,
    method: 'get'
  })
} 


// 上传模板接口，暂时未用
// export function uploadapi(formData){
//   return request({
//     url:'/apitest/upload_interface_templete',
//     method:'post',
//     data:formData,
//     headers: {
//       'Content-Type': 'multipart/form-data'
//      }
//   })
// }