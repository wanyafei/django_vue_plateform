import request from '@/utils/request'

export function login(data) {
  return request({
    // url: '/vue-admin-template/user/login',
    url:'/api/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url:'/api/info',
    method: 'get',
    params: { token }
  })
} 
export function getuser(val) {
  return request({
    url:'/api/getuser?user='+val,
    method: 'get',
  })
}
export function logout() {
  return request({
    url: '/api/logout',
    method: 'get'
  })
}
