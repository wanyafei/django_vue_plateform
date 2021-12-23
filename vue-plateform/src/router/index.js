import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/get_report',
    name:'report',
    component: () => import('@/views/report/index'),

  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/homepage',
    children: [{
      path: 'homepage',
      name: '首页概览',
      component: () => import('@/views/homepage/index'),
      meta: { title: '首页概览', icon: 'el-icon-s-home' }
    }]
  },
  {
    path: '/project',
    component: Layout,
    redirect: '/project/index',
    children: [{
      path: 'project',
      name: '项目管理',
      component: () => import('@/views/project/index'),
      meta: { title: '项目管理', icon: 'homepage' }
    }]
  },
  {
    path: '/environment',
    component: Layout,
    redirect: '/environment/index',
    children: [{
      path: 'environment',
      name: '环境管理',
      component: () => import('@/views/environment/index'),
      meta: { title: '环境管理', icon: 'el-icon-s-order' }
    }]
  },
  // {
  //   path: '/apitest',
  //   component: () => import('@/views/interface/interface_manage'),
  //   hidden: true
  // },
  {
    path: '/apitest',
    component: Layout,
    redirect: '/apitest/index',
    name: '接口测试',
    meta: { title: '接口测试', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'interface',
        name: '接口管理',
        component: () => import('@/views/interface/interface_manage/index'),
        meta: { title: '接口管理', icon: 'table' }
      },
      {
        path: 'testcase',
        name: '用例管理',
        component: () => import('@/views/interface/testcase/index'),
        meta: { title: '用例管理', icon: 'el-icon-document' }
      },
      {
        path: 'testplan',
        name: '测试计划管理',
        component: () => import('@/views/interface/testplan/index'),
        meta: { title: '测试计划管理', icon: 'tree' }
      },
    ]
  },
  {
    path: '/task',
    component: Layout,
    redirect: '/task/index',
    children: [{
      path: 'task',
      name: '任务管理',
      component: () => import('@/views/task/index'),
      meta: { title: '任务管理', icon: 'el-icon-alarm-clock' }
    }]
  },
  //------------------------外链路由----------
  // {
  //   path:'external-link',
  //   component:Layout,
  //   children:[
  //       {
  //         path:"http://www.baidu.com",
  //         meta: { title: '哈哈', icon: 'el-icon-alarm-clock' }
  //       }
  //   ]
  // },
  // {
  //   path: '/user',
  //   component: Layout,
  //   children: [
  //     {
  //       path: 'user',
  //       name: '用户管理',
  //       component: () => import('@/views/form/index'),
  //       meta: { title: '用户管理', icon: 'el-icon-s-custom' }
  //     }
  //   ]
  // },

  // {
  //   path: '/nested',
  //   component: Layout,
  //   redirect: '/nested/menu1',
  //   name: 'Nested',
  //   meta: {
  //     title: 'Nested',
  //     icon: 'nested'
  //   },
  //   children: [
  //     {
  //       path: 'menu1',
  //       component: () => import('@/views/nested/menu1/index'), // Parent router-view
  //       name: 'Menu1',
  //       meta: { title: 'Menu1' },
  //       children: [
  //         {
  //           path: 'menu1-1',
  //           component: () => import('@/views/nested/menu1/menu1-1'),
  //           name: 'Menu1-1',
  //           meta: { title: 'Menu1-1' }
  //         },
  //         {
  //           path: 'menu1-2',
  //           component: () => import('@/views/nested/menu1/menu1-2'),
  //           name: 'Menu1-2',
  //           meta: { title: 'Menu1-2' },
  //           children: [
  //             {
  //               path: 'menu1-2-1',
  //               component: () => import('@/views/nested/menu1/menu1-2/menu1-2-1'),
  //               name: 'Menu1-2-1',
  //               meta: { title: 'Menu1-2-1' }
  //             },
  //             {
  //               path: 'menu1-2-2',
  //               component: () => import('@/views/nested/menu1/menu1-2/menu1-2-2'),
  //               name: 'Menu1-2-2',
  //               meta: { title: 'Menu1-2-2' }
  //             }
  //           ]
  //         },
  //         {
  //           path: 'menu1-3',
  //           component: () => import('@/views/nested/menu1/menu1-3'),
  //           name: 'Menu1-3',
  //           meta: { title: 'Menu1-3' }
  //         }
  //       ]
  //     },
  //     {
  //       path: 'menu2',
  //       component: () => import('@/views/nested/menu2/index'),
  //       name: 'Menu2',
  //       meta: { title: 'menu2' }
  //     }
  //   ]
  // },

  {
    path: '/testreport',
    component: Layout,
    redirect: '/testreport',
    children: [{
      path: 'testreport',
      name: '测试报告',
      component: () => import('@/views/testreport/index'),
      meta: { title: '测试报告', icon: 'el-icon-message' }
    }]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
