<template>
  <div class="resident-details">
    <el-card class="detail-card">
      <div slot="header" class="card-header">
        <h1>居民详细信息</h1>
      </div>

      <div v-if="isLoading" class="loading">
        <i class="el-icon-loading"></i>
        <span>正在加载...</span>
      </div>

      <div v-if="error" class="error">
        <i class="el-icon-warning"></i>
        <span>{{ error }}</span>
      </div>

      <div v-if="resident" class="info-container">
        <div class="info-section">
          <h3>基本信息</h3>
          <div class="info-item">
            <i class="el-icon-user"></i>
            <strong>姓名：</strong>{{ resident.first_name }} {{ resident.last_name }}
          </div>
          <div class="info-item">
            <i class="el-icon-male"></i>
            <strong>性别：</strong>{{ resident.gender }}
          </div>
          <div class="info-item">
            <i class="el-icon-date"></i>
            <strong>生日：</strong>{{ resident.birthday }}
          </div>
          <div class="info-item">
            <i class="el-icon-office-building"></i>
            <strong>职业：</strong>{{ resident.occupation }}
          </div>
        </div>

        <div class="info-section">
          <h3>联系信息</h3>
          <div class="info-item">
            <i class="el-icon-phone"></i>
            <strong>联系方式：</strong>{{ resident.contact }}
          </div>
          <div class="info-item">
            <i class="el-icon-location"></i>
            <strong>地址：</strong>{{ resident.address }}
          </div>
        </div>

        <div class="info-section">
          <h3>区块信息</h3>
          <div class="info-item">
            <i class="el-icon-map-location"></i>
            <strong>区块：</strong>{{ resident.block }}
          </div>
          <div class="info-item">
            <i class="el-icon-info"></i>
            <strong>区块描述：</strong>{{ resident.block_description }}
          </div>
        </div>
      </div>

      <div class="actions">
        <el-button type="primary" @click="goBack" icon="el-icon-back">
          返回上一页
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { getResidentDetail } from '@/services/residentService';
import { Message } from 'element-ui';

export default {
  data() {
    return {
      resident: null,
      isLoading: false,
      error: null,
    };
  },
  created() {
    this.fetchResidentDetail();
  },
  methods: {
    async fetchResidentDetail() {
      this.isLoading = true;
      this.error = null;
      const residentId = this.$route.params.residentId;
      try {
        this.resident = await getResidentDetail(residentId);
      } catch (err) {
        this.error = '无法获取居民详细信息，请稍后重试。';
        console.error('获取居民详情失败:', err);
        Message.error(this.error);
      } finally {
        this.isLoading = false;
      }
    },
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>

<style scoped>
.resident-details {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.detail-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-header h1 {
  margin: 0;
  font-size: 1.8rem;
  color: #303133;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #909399;
}

.loading i {
  margin-right: 0.5rem;
}

.error {
  padding: 1rem;
  background-color: #fef0f0;
  border-radius: 4px;
  color: #f56c6c;
  display: flex;
  align-items: center;
}

.error i {
  margin-right: 0.5rem;
}

.info-container {
  padding: 1rem;
}

.info-section {
  margin-bottom: 2rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.info-section h3 {
  margin-top: 0;
  color: #409EFF;
  border-bottom: 2px solid #409EFF;
  padding-bottom: 0.5rem;
}

.info-item {
  margin: 1rem 0;
  display: flex;
  align-items: center;
}

.info-item i {
  margin-right: 0.5rem;
  color: #409EFF;
}

.info-item strong {
  margin-right: 0.5rem;
  color: #606266;
}

.actions {
  text-align: center;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #EBEEF5;
}
</style>
