<template>
  <div class="event-detail">
    <h2>案件详情</h2>
    <div class="detail-section">
      <h3>基本信息</h3>
      <p><strong>案件编号:</strong> {{ this.$route.params.id }}</p>
      <p><strong>案件描述:</strong> {{ event.crimeDesc }}</p>
      <p><strong>案发时间:</strong> {{ formatDateTime(event.timeOccurred) }}</p>
      <p><strong>报案时间:</strong> {{ formatDateTime(event.timeReported) }}</p>
      <p><strong>当前状态:</strong> {{ event.curStatus }}</p>
      <p><strong>最后更新:</strong> {{ formatDateTime(event.updatedAt) }}</p>
    </div>

    <div class="detail-section">
      <h3>案件类型</h3>
      <div v-for="type in event.types" :key="type.type_code">
        <p><strong>类型名称:</strong> {{ type.type_name }}</p>
        <p><strong>类型描述:</strong> {{ type.type_description }}</p>
      </div>
    </div>

    <div class="detail-section">
      <h3>涉案人员</h3>
      <div v-if="event.persons">
        <div v-if="event.persons.suspects && event.persons.suspects.length">
          <p><strong>嫌疑人:</strong></p>
          <ul>
            <li v-for="suspect in event.persons.suspects" :key="suspect.person_id">
              <router-link :to="`/residents/${suspect.person_id}`">{{ suspect.name }}</router-link>
            </li>
          </ul>
        </div>
        <div v-if="event.persons.criminals && event.persons.criminals.length">
          <p><strong>罪犯:</strong></p>
          <ul>
            <li v-for="criminal in event.persons.criminals" :key="criminal.person_id">
              <router-link :to="`/residents/${criminal.person_id}`">{{ criminal.name }}</router-link>
            </li>
          </ul>
        </div>
        <div v-if="event.persons.victims && event.persons.victims.length">
          <p><strong>受害人:</strong></p>
          <ul>
            <li v-for="victim in event.persons.victims" :key="victim.person_id">
              <router-link :to="`/residents/${victim.person_id}`">{{ victim.name }}</router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="detail-section">
      <h3>作案工具</h3>
      <div v-for="weapon in event.weapons" :key="weapon.weapon_code">
        <p><strong>工具描述:</strong> {{ weapon.weapon_description }}</p>
        <p><strong>详细信息:</strong> {{ weapon.weapon_detail }}</p>
      </div>
    </div>

    <div class="detail-section">
      <h3>案发地点</h3>
      <p><strong>位置:</strong> {{ event.location }}</p>
      <p><strong>街区:</strong> {{ event.blockName }}</p>
      <p><strong>区域描述:</strong> {{ event.blockDescription }}</p>
      <p><strong>经纬度:</strong> {{ event.latitude }}, {{ event.longitude }}</p>
    </div>

    <div class="detail-section">
      <h3>负责警官</h3>
      <div v-for="(officer, index) in event.officers" :key="index">
        <p>
          <strong>姓名:</strong>
          <router-link :to="`/residents/${officer.person_id}`">{{ officer.name }}</router-link>
        </p>
        <p><strong>职级:</strong> {{ officer.rank }}</p>
        <p><strong>等级:</strong> {{ officer.level }}</p>
      </div>
    </div>

    <div class="actions">
      <el-button type="primary" @click="goBack">
        返回上一页
      </el-button>
      
      <!-- 只有警官及以上权限可以更新案件进展 -->
      <el-button 
        type="success" 
        @click="viewProgress"
        v-if="hasPermission('update_progress')"
      >
        更新案件进展
      </el-button>
      
      <!-- 所有用户都可以提交线索 -->
      <el-button 
        type="warning" 
        @click="submitClue"
        v-if="hasPermission('submit_clues')"
      >
        提交线索
      </el-button>
      
      <!-- 只有刑侦人员和管理员可以管理案件 -->
      <el-button 
        type="danger" 
        @click="editCase"
        v-if="hasPermission('manage_cases')"
      >
        编辑案件
      </el-button>
    </div>
  </div>
</template>

<script>
import { getCrimeEventById } from '@/services/crimeEventService';
import { Message } from 'element-ui';
import { getCurrentUser } from '@/services/authService';
import { hasPermission } from '@/store/modules/auth';

export default {
  name: 'CrimeEventDetail',
  data() {
    return {
      user: null,
      event: {}
    };
  },
  methods: {
    formatDateTime(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString('zh-CN');
    },
    goBack() {
      this.$router.go(-1);
    },
    viewProgress() {
      this.$router.push(`/progress/${this.$route.params.id}`);
    },
    hasPermission(permission) {
      return this.user && hasPermission(this.user.role, permission);
    }
  },
  async created() {
    const eventId = this.$route.params.id;
    try {
      this.event = await getCrimeEventById(eventId);
      console.log("event:", this.event);
    } catch (error) {
      console.error(`获取案件详情失败,ID ${eventId}:`, error);
      Message.error("加载案件详情失败，请稍后重试。");
    }
    this.user = getCurrentUser();
  }
};
</script>

<style scoped>
.event-detail {
  padding: 2em;
  max-width: 800px;
  margin: 0 auto;
}

.detail-section {
  margin-bottom: 2em;
  padding: 1em;
  border: 1px solid #eee;
  border-radius: 4px;
}

.detail-section h3 {
  margin-top: 0;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5em;
}

.detail-section p {
  margin: 0.5em 0;
}

.detail-section ul {
  list-style: none;
  padding-left: 20px;
}

.detail-section a {
  color: #409EFF;
  text-decoration: none;
}

.detail-section a:hover {
  text-decoration: underline;
}

.actions {
  margin-top: 2em;
  text-align: center;
}

.actions .el-button {
  margin: 0 10px;
}
</style>