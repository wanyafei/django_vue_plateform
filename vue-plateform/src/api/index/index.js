import request from '@/utils/request'

// 获取首页概览处的项目、环境、用例、报告数量
export function getnumber_prj_env_case_report() {
    return request({
      url:'/taste_user/getnumber_prj_env_case_report',
      method: 'get',
    })
  }
export function get_num_byechart() {
    return request({
      url:'/taste_user/get_num_byechart',
      method: 'get'
    })
  }