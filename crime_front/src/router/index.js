import Vue from 'vue';
import Router from 'vue-router';
import { getCurrentUser } from '@/services/authService';
import { hasPermission } from '@/store/modules/auth';
import { Message } from 'element-ui';

// 导入视图组件
import Dashboard from '@/views/Dashboard.vue';
import UserLogin from '@/views/UserLogin.vue';
import UserRegistration from '@/views/UserRegistration.vue';
import UserProfile from '@/views/UserProfile.vue';
import CrimeEventList from '@/views/CrimeEventList.vue';
import CrimeEventDetail from '@/views/CrimeEventDetail.vue';
import CrimeEventForm from '@/views/CrimeEventForm.vue';
import CaseProgressList from '@/views/CaseProgressList.vue';
import CaseProgressForm from '@/views/CaseProgressForm.vue';
import ClueList from '@/views/ClueList.vue';
import ClueUpload from '@/views/ClueUpload.vue';
import ResidentList from '@/views/ResidentList.vue';
import ResidentDetail from '@/views/ResidentDetail.vue';

Vue.use(Router);

// 配置路由规则
const routes = [
  {
    path: '/',
    name: 'UserDashboard',
    component: Dashboard,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: UserLogin
  },
  {
    path: '/register',
    name: 'Register',
    component: UserRegistration
  },
  {
    path: '/profile',
    name: 'Profile',
    component: UserProfile,
    meta: { requiresAuth: true }
  },
  {
    path: '/events',
    name: 'CrimeEventList',
    component: CrimeEventList,
    meta: { requiresAuth: true }
  },
  {
    path: '/events/:id',
    name: 'CrimeEventDetail',
    component: CrimeEventDetail,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/events-new',
    name: 'CrimeEventForm',
    component: CrimeEventForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/progress/:eventId',
    name: 'CaseProgressList',
    component: CaseProgressList,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/progress/:eventId/new',
    name: 'CaseProgressForm',
    component: CaseProgressForm,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/clues',
    name: 'ClueList',
    component: ClueList,
    meta: { requiresAuth: true }
  },
  {
    path: '/clues/:eventId/upload',
    name: 'ClueUpload',
    component: ClueUpload,
    meta: { requiresAuth: true }
  },
  {
    path: '/residents',
    name: 'ResidentList',
    component: ResidentList,
  },
  {
    path: '/residents/:residentId',
    name: 'ResidentDetail',
    component: ResidentDetail,
  },
  {
    path: '*',
    redirect: '/'
  }
];

// 创建并导出路由实例
const router = new Router({
  mode: 'history', // 使用 HTML5 History 模式，消除哈希 #
  routes
});

// 导航守卫：检查路由元信息中的 requiresAuth
router.beforeEach((to, from, next) => {
  const user = getCurrentUser();
  
  // 检查路由是否需要权限
  if (to.meta.requiresPermission) {
    if (!user) {
      next('/login');
    } else if (!hasPermission(user.role, to.meta.requiresPermission)) {
      Message.error('您没有权限访问该页面');
      next(from.path);
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
