<template>
  <div class="user-profile">
    <el-card class="detail-card">
      <div slot="header" class="card-header">
        <h1>个人资料</h1>
      </div>

      <div v-if="isLoading" class="loading">
        <i class="el-icon-loading"></i>
        <span>正在加载...</span>
      </div>

      <div v-if="error" class="error">
        <i class="el-icon-warning"></i>
        <span>{{ error }}</span>
      </div>

      <div v-if="profile" class="info-container">
        <div class="info-section">
          <h3>基本信息</h3>
          <div class="info-item">
            <i class="el-icon-user"></i>
            <strong>姓名：</strong>{{ profile.fullname }}
          </div>
          <div class="info-item">
            <i class="el-icon-message"></i>
            <strong>邮箱：</strong>{{ profile.email }}
          </div>
          <div class="info-item">
            <i class="el-icon-s-custom"></i>
            <strong>角色：</strong>{{ profile.role }}
          </div>
        </div>

        <div class="info-section">
          <h3>联系信息</h3>
          <div class="info-item">
            <i class="el-icon-phone"></i>
            <strong>联系方式：</strong>{{ profile.contact }}
          </div>
          <div class="info-item">
            <i class="el-icon-location"></i>
            <strong>地址：</strong>{{ profile.address }}
          </div>
        </div>
      </div>

      <div class="actions">
        <el-button type="primary" @click="goBack" icon="el-icon-back">
          返回首页
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { Message } from 'element-ui';
import axiosInstance from '@/services/axiosInstance';

export default {
  name: 'UserProfile',
  data() {
    return {
      profile: null,
      isLoading: false,
      error: null
    };
  },
  created() {
    this.fetchUserProfile();
  },
  methods: {
    async fetchUserProfile() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await axiosInstance.get('/auth/profile/');
        console.log(response.data);
        this.profile = response.data;
      } catch (error) {
        this.error = '获取用户信息失败，请重新登录';
        console.error('获取用户信息失败:', error);
        Message.error(this.error);
        this.$router.push('/login');
      } finally {
        this.isLoading = false;
      }
    },
    goBack() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.user-profile {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.detail-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.card-header {
  padding-bottom: 20px;
}

.card-header h1 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.info-container {
  padding: 20px 0;
}

.info-section {
  margin-bottom: 30px;
}

.info-section h3 {
  font-size: 18px;
  color: #303133;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #EBEEF5;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  padding: 10px;
}

.info-item i {
  font-size: 20px;
  color: #409EFF;
  margin-right: 10px;
}

.info-item strong {
  margin-right: 10px;
  color: #606266;
}

.loading, .error {
  text-align: center;
  padding: 20px;
}

.loading i, .error i {
  margin-right: 10px;
}

.error {
  color: #F56C6C;
}

.actions {
  margin-top: 20px;
  text-align: center;
}
</style>
