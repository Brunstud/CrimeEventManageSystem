<template>
  <div class="resident-list">
    <div class="header">
      <h1>居民列表</h1>
    </div>

    <div v-if="isLoading" class="loading">
      <i class="el-icon-loading"></i>
      <span>正在加载...</span>
    </div>

    <div v-if="error" class="error-message">
      <i class="el-icon-warning"></i>
      {{ error }}
    </div>

    <div class="residents-container" v-if="residents.length > 0">
      <el-card v-for="resident in residents" 
               :key="resident.person_id" 
               class="resident-card"
               @click.native="viewDetails(resident.person_id)">
        <div class="resident-info">
          <div class="resident-header">
            <h3>{{ resident.first_name }} {{ resident.last_name }}</h3>
          </div>
          <div class="resident-details">
            <p>
              <i class="el-icon-user"></i>
              <span>性别：{{ resident.gender }}</span>
            </p>
            <p>
              <i class="el-icon-office-building"></i>
              <span>职业：{{ resident.occupation }}</span>
            </p>
            <p>
              <i class="el-icon-phone"></i>
              <span>联系方式：{{ resident.contact }}</span>
            </p>
            <p>
              <i class="el-icon-location"></i>
              <span>区块：{{ resident.block }}</span>
            </p>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { getAllResidents } from '@/services/residentService';
import { Message } from 'element-ui';

export default {
  data() {
    return {
      residents: [],
      isLoading: false,
      error: null,
    };
  },
  created() {
    this.fetchResidents();
  },
  methods: {
    async fetchResidents() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await getAllResidents();
        this.residents = response;
      } catch (err) {
        this.error = '无法获取居民列表，请稍后重试。';
        console.error('获取居民列表失败:', err);
        Message.error(this.error);
      } finally {
        this.isLoading = false;
      }
    },
    viewDetails(residentId) {
      this.$router.push(`/residents/${residentId}`);
    },
  },
};
</script>

<style scoped>
.resident-list {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  margin-bottom: 2rem;
  text-align: center;
}

.header h1 {
  color: #303133;
  font-size: 2rem;
  font-weight: 600;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #909399;
}

.loading i {
  margin-right: 0.5rem;
}

.error-message {
  background-color: #fef0f0;
  color: #f56c6c;
  padding: 1rem;
  border-radius: 4px;
  margin: 1rem 0;
  display: flex;
  align-items: center;
}

.error-message i {
  margin-right: 0.5rem;
  font-size: 1.2rem;
}

.residents-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  padding: 1rem 0;
}

.resident-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.resident-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

.resident-info {
  padding: 0.5rem;
}

.resident-header {
  margin-bottom: 1rem;
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 0.5rem;
}

.resident-header h3 {
  margin: 0;
  color: #303133;
  font-size: 1.2rem;
}

.resident-details p {
  margin: 0.8rem 0;
  color: #606266;
  display: flex;
  align-items: center;
}

.resident-details i {
  margin-right: 0.5rem;
  color: #409EFF;
  width: 1.2rem;
}
</style>
