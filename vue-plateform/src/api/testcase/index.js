import request from '@/utils/request'

// 列表数据
export function getinterfacecontent_by_prj_id(data) {
    return request({
      url:'/apitest/get_interface_contnet',
      method: 'post',
      data
    })
  }
  
// 列表接口数据
export function gettestcase(data) {
  return request({
    url:'/apitest/get_testcase',
    method: 'post',
    data
  })
}
// 添加测试用例
export function add(data) {
  return request({
    url:'/apitest/add_testcase',
    method: 'post',
    data
  })
}
// 删除单个测试用例
export function del(testcase_ids) {
  return request({
    url:'/apitest/del_testcase?testcase_ids='+testcase_ids,
    method: 'get',
  })
}
// 修改弹框反显的数据
export function detail(testcase_id) {
  return request({
    url:'apitest/get_testcase',
    method: 'get',
    params:{testcase_id}
  })
}
// 修改操作
export function update(testcase_id,data) {
  return request({
    url:'/apitest/update_interface?testcase_id='+testcase_id,
    method: 'post',
    data
  })
}
//调试运行接口  
export function case_run(data) {
  return request({
    url:'/apitest/case_run',
    method: 'post',
    data
  })
}
