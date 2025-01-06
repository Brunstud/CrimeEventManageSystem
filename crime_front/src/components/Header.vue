<template>
    <header class="header">
      <nav class="navbar">
        <router-link to="/" class="logo-container">
          <img src="/favicon.ico" alt="标志" class="logo">
          <h1 class="navbar-title">城市犯罪管理系统</h1>
        </router-link>
        <ul class="navbar-links">
          <li><router-link to="/"><i class="fas fa-home"></i> 首页</router-link></li>
          <li><router-link to="/events"><i class="fas fa-exclamation-triangle"></i> 犯罪事件</router-link></li>
          <li><router-link to="/profile" v-if="isAuthenticated"><i class="fas fa-user"></i> 个人资料</router-link></li>
          <li>
            <router-link v-if="!isAuthenticated" to="/login">
              <i class="fas fa-sign-in-alt"></i> 登录
            </router-link>
            <a v-else href="#" @click.prevent="handleLogout">
              <i class="fas fa-sign-out-alt"></i> 退出登录
            </a>
          </li>
        </ul>
      </nav>
    </header>
  </template>
  
  <script>
  import { mapGetters } from 'vuex';

  export default {
    name: 'AppHeader',
    computed: {
      ...mapGetters('user', ['isAuthenticated']),
      // 监听全局状态变化
      authStatus() {
        return this.$store.state.user.isAuthenticated;
      }
    },
    watch: {
      // 监听认证状态变化
      authStatus(newVal) {
        if(this.isAuthenticated !== newVal) {
          this.$store.commit('user/SET_USER', newVal ? this.$store.state.user.currentUser : null);
        }
      }
    },
    methods: {
      async handleLogout() {
        try {
          const loadingInstance = this.$loading({
            lock: true,
            text: '正在退出登录...',
            spinner: 'el-icon-loading',
            background: 'rgba(0, 0, 0, 0.7)'
          });
          
          await this.$store.dispatch('user/logout');
          
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          
          loadingInstance.close();
          
          await this.$router.push('/login');
          this.$message({
            type: 'success',
            message: '退出登录成功'
          });
        } catch (error) {
          console.error('退出登录错误:', error);
          this.$message({
            type: 'error',
            message: `退出登录失败: ${error.message || '未知错误'}`
          });
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .header {
    background-color: #3b5998;
    color: white;
    padding: 1em;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-bottom: 3px solid #2d4373;
  }
  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
  }
  .logo-container {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: white;
    transition: all 0.3s ease;
  }
  .logo-container:hover {
    transform: scale(1.02);
    opacity: 0.9;
  }
  .logo {
    height: 40px;
    margin-right: 1em;
    filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.2));
  }
  .navbar-title {
    font-size: 1.5em;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
  }
  .navbar-links {
    list-style: none;
    display: flex;
    gap: 2em;
    margin: 0;
    padding: 0;
  }
  .navbar-links li {
    color: white;
  }
  .navbar-links a {
    color: white;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5em;
  }
  .navbar-links a:hover {
    opacity: 0.8;
    transform: translateY(-2px);
  }
  .navbar-links i {
    font-size: 1.1em;
  }
  </style>