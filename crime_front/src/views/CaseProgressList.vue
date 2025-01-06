<template>
  <div class="progress-list">
    <h2>案件进展</h2>
    
    <div class="case-info-section">
      <h3>案件基本信息</h3>
      <div class="info-item">
        <p><strong>案件编号:</strong> {{ this.$route.params.eventId }}</p>
        <p><strong>案件类型:</strong> {{ event.types[0].type_name }}</p>
        <p><strong>案件描述:</strong> {{ event.crimeDesc }}</p>
        <p><strong>发生时间:</strong> {{ formatDateTime(event.timeOccurred) }}</p>
        <p><strong>发生地点:</strong> {{ event.location }}</p>
        <p><strong>案件状态:</strong> {{ event.curStatus }}</p>
      </div>
    </div>

    <div class="progress-section">
      <h3>案件进展记录</h3>
      <div class="search-box">
        <el-input
          v-model="progressKeyword"
          placeholder="搜索案件进展..."
          @input="handleProgressSearch"
          clearable>
        </el-input>
      </div>
      <ul>
        <li v-for="progress in progresses" :key="progress.progress_code">
          <div class="progress-item">
            <p><strong>状态:</strong> {{ progress.status }}</p>
            <p><strong>说明:</strong> {{ progress.notes }}</p>
            <p><strong>时间:</strong> {{ formatDateTime(progress.time_progress) }}</p>
          </div>
        </li>
      </ul>
    </div>

    <div class="clues-section">
      <h3>案件线索</h3>
      <div class="search-box">
        <el-input
          v-model="clueKeyword"
          placeholder="搜索案件线索..."
          @input="handleClueSearch"
          clearable>
        </el-input>
      </div>
      <ul>
        <li v-for="clue in clues" :key="clue.clue_code">
          <div class="clue-item">
            <p><strong>线索类型:</strong> {{ clue.clue_type }}</p>
            <p><strong>线索描述:</strong> {{ clue.clue_description }}</p>
            <p><strong>是否作为证据:</strong> {{ clue.chosen_as_evidence ? '是' : '否' }}</p>
          </div>
        </li>
      </ul>
    </div>

    <div class="actions">
      <el-button type="primary" @click="goBack" icon="el-icon-back">
        返回案件详情
      </el-button>
      <el-button type="success" @click="addProgress" icon="el-icon-plus">
        更新进展
      </el-button>
      <el-button type="warning" @click="addClue" icon="el-icon-plus">
        提交线索
      </el-button>
    </div>
  </div>
</template>

<script>
import { getCaseProgress, searchCaseProgress } from '@/services/caseService';
import { getCluesByEventId, searchClues } from '@/services/clueService';
import { getCrimeEventById } from '@/services/crimeEventService';
import { Message } from 'element-ui';
import debounce from 'lodash/debounce';

export default {
  name: 'CaseProgressList',
  data() {
    return {
      event: {},
      progresses: [],
      clues: [],
      progressKeyword: '',
      clueKeyword: ''
    };
  },
  methods: {
    formatDateTime(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString('zh-CN');
    },
    goBack() {
      this.$router.push(`/events/${this.$route.params.eventId}`);
    },
    addProgress() {
      this.$router.push(`/progress/${this.$route.params.eventId}/new/`);
    },
    addClue() {
      this.$router.push(`/clues/${this.$route.params.eventId}/upload/`);
    },
    handleProgressSearch: debounce(async function() {
      const eventId = this.$route.params.eventId;
      if (!this.progressKeyword.trim()) {
        const progressData = await getCaseProgress(eventId);
        this.progresses = progressData.results;
        return;
      }
      try {
        const searchData = await searchCaseProgress(eventId, this.progressKeyword);
        this.progresses = searchData.results;
      } catch (error) {
        console.error("搜索案件进展失败:", error);
        Message.error("搜索案件进展失败，请稍后重试。");
      }
    }, 500),
    handleClueSearch: debounce(async function() {
      const eventId = this.$route.params.eventId;
      if (!this.clueKeyword.trim()) {
        const cluesData = await getCluesByEventId(eventId);
        this.clues = cluesData.results;
        return;
      }
      try {
        const searchData = await searchClues(this.clueKeyword, eventId);
        this.clues = searchData.results;
      } catch (error) {
        console.error("搜索案件线索失败:", error);
        Message.error("搜索案件线索失败，请稍后重试。");
      }
    }, 500)
  },
  async created() {
    const eventId = this.$route.params.eventId;
    try {
      // 获取案件基本信息
      this.event = await getCrimeEventById(eventId);
      
      // 获取案件进展
      const progressData = await getCaseProgress(eventId);
      this.progresses = progressData.results;
      
      // 获取案件线索
      const cluesData = await getCluesByEventId(eventId);
      this.clues = cluesData.results;
    } catch (error) {
      console.error(`获取案件ID ${eventId} 的信息失败:`, error);
      Message.error("加载案件信息失败，请稍后重试。");
    }
  }
};
</script>

<style scoped>
.progress-list {
  padding: 2em;
  max-width: 800px;
  margin: 0 auto;
}

.case-info-section, .progress-section, .clues-section {
  margin-bottom: 2em;
}

.info-item, .progress-item, .clue-item {
  border: 1px solid #ddd;
  margin: 10px 0;
  padding: 15px;
  border-radius: 4px;
}

h3 {
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5em;
  margin-top: 1em;
}

ul {
  list-style: none;
  padding: 0;
}

p {
  margin: 5px 0;
}

.actions {
  margin-top: 2em;
  text-align: center;
}

.search-box {
  margin: 1em 0;
}
</style>