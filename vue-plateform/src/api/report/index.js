import request from '@/utils/request'
//测试报告列表
  export function getreport(data) {
    return request({
      url:'/apitest/getreport',
      method: 'post',
      data
    })
  }
// 删除操作
export function del(report_ids) {
  return request({
    url:'/apitest/delete_report?report_ids='+report_ids,
    method: 'get'
  })
}  
//获取测试报告
export function get_report(flag,id) {
  return request({
    url:'/apitest/get_report?flag='+flag+'&id='+id,
    method: 'get'
  })
}