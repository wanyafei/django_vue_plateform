import request from '@/utils/request'

// 列表数据
export function getplan(data) {
    return request({
      url:'/apitest/get_plan',
      method: 'post',
      data
    })
  }
// 添加接口
export function add(data) {
    return request({
      url:'/apitest/add_plan',
      method: 'post',
      data
    })
  }
//修改接口
export function detail(plan_id) {
    return request({
      url:'/apitest/get_plan',
      method: 'get',
      params:{plan_id}
    })
  }
// 修改提交的接口
export function update(testplan_id,data) {
    return request({
      url:'/apitest/update_plan?testplan_id='+testplan_id,
      method: 'post',
      data
    })
  }
//删除接口
export function del(plan_id){
    return request({
        url:'/apitest/delete_plan?testplan_id='+plan_id,
        method: 'get'
      })
}

//获取所有环境接口
export function getenv(){
    return request({
        url:'/apitest/getenv',
        method: 'get'
      })
}
//获取所有用例接口
export function getcase(){
  return request({
      url:'/apitest/get_case',
      method: 'get'
    })
}

//运行测试计划
export function run_plan(plan_id){
  return request({
      url:'/apitest/run_plan',
      method: 'get',
      params:{plan_id}
    })
}
// 通过项目ID,环境ID取测试计划大接口
export function get_plan_by_proidandenvid(prj_id,env_id,type) {
  return request({
    url:'/apitest/get_project_interface_case_byprjid?prj_id='+prj_id+'&env_id='+env_id+'&type='+type,
    method: 'get'
  })
} 