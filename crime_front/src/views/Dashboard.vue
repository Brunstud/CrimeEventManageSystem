<template>
  <div class="dashboard">
    <div class="welcome-section">
      <!-- <div class="welcome-header">
        <h1>城市犯罪管理系统</h1>
        <div class="welcome-divider"></div>
      </div> -->
      <div class="welcome-banner">
        <h2>让城市更安全,让生活更美好</h2>
        <p>共建平安社区,共创和谐家园</p>
      </div>
    </div>
    <div class="dashboard-grid">
      <router-link to="/events" class="card-link" v-if="hasPermission('view_cases')">
        <el-card class="dashboard-card">
          <i class="el-icon-document"></i>
          <h3>案件列表</h3>
          <p>查看和管理所有犯罪案件</p>
        </el-card>
      </router-link>
      
      <router-link to="/residents" class="card-link" v-if="hasPermission('view_residents')">
        <el-card class="dashboard-card">
          <i class="el-icon-user"></i>
          <h3>居民列表</h3>
          <p>查看社区居民信息</p>
        </el-card>
      </router-link>

      <router-link to="/clues" class="card-link" v-if="hasPermission('submit_clues')">
        <el-card class="dashboard-card">
          <i class="el-icon-search"></i>
          <h3>线索管理</h3>
          <p>管理案件相关线索</p>
        </el-card>
      </router-link>

      <router-link to="/profile" class="card-link">
        <el-card class="dashboard-card">
          <i class="el-icon-setting"></i>
          <h3>个人中心</h3>
          <p>查看和编辑个人信息</p>
        </el-card>
      </router-link>
    </div>
    <div class="quick-stats">
      <el-card class="stat-card">
        <div class="stat-number">128</div>
        <div class="stat-label">本月案件</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-number">85%</div>
        <div class="stat-label">破案率</div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-number">1,254</div>
        <div class="stat-label">社区居民</div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { getCurrentUser } from '@/services/authService';
import { hasPermission } from '@/store/modules/auth';

export default {
  name: 'UserDashboard',
  data() {
    return {
      user: null
    };
  },
  created() {
    this.user = getCurrentUser();
    if (!this.user) {
      this.$router.push('/login');
    }
  },
  methods: {
    hasPermission(permission) {
      return this.user && hasPermission(this.user.role, permission);
    }
  }
};
</script>

<style scoped>
.dashboard {
  text-align: center;
  padding: 2em;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.dashboard h1 {
  color: #303133;
  margin-bottom: 1em;
  font-size: 2.5em;
}

.welcome-banner {
  background: linear-gradient(135deg, #3b5998, #4a90e2);
  color: white;
  padding: 2em;
  border-radius: 8px;
  margin-bottom: 2em;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.welcome-banner h2 {
  margin: 0;
  font-size: 1.8em;
}

.welcome-banner p {
  margin: 0.5em 0 0;
  opacity: 0.9;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2em;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1em;
}

.card-link {
  text-decoration: none;
}

.dashboard-card {
  transition: all 0.3s ease;
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.dashboard-card i {
  font-size: 3em;
  color: #409EFF;
  margin-bottom: 0.5em;
}

.dashboard-card h3 {
  color: #303133;
  margin: 0.5em 0;
}

.dashboard-card p {
  color: #909399;
  margin: 0;
  font-size: 0.9em;
}

.card-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #f56c6c;
  color: white;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8em;
}

.quick-stats {
  display: flex;
  justify-content: center;
  gap: 2em;
  margin-top: 3em;
}

.stat-card {
  width: 150px;
  padding: 1em;
  text-align: center;
}

.stat-number {
  font-size: 2em;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  color: #909399;
  margin-top: 0.5em;
  font-size: 0.9em;
}
</style>