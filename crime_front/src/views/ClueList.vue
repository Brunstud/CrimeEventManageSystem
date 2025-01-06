<template>
  <div class="clue-list">
    <h2>线索列表</h2>
    <!-- 搜索框 -->
    <div class="search-box">
      <input
        type="text"
        v-model="searchKeyword"
        placeholder="输入关键词搜索线索..."
        @input="handleSearch"
      >
    </div>
    <ul>
      <li v-for="clue in clues" :key="clue.clue_code">
        <div class="clue-item">
          <h3>线索编号: {{ clue.clue_code }}</h3>
          <p>
            案件描述: 
            <router-link :to="`/events/${clue.event_id}`">
              {{ clue.crime_description }}
            </router-link>
          </p>
          <p>线索类型: {{ clue.clue_type }}</p>
          <p>线索描述: {{ clue.clue_description }}</p>
          <p>提交人: {{ clue.submitted_by }}</p>
          <p>提交时间: {{ formatDate(clue.submitted_at) }}</p>
          <p>是否作为证据: {{ clue.chosen_as_evidence ? '是' : '否' }}</p>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { getAllClues, searchClues } from '@/services/clueService';
import debounce from 'lodash/debounce';
import { Message } from 'element-ui';

export default {
  name: 'ClueList',
  data() {
    return {
      clues: [],
      searchKeyword: ''
    };
  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleString('zh-CN');
    },
    handleSearch: debounce(async function() {
      if (!this.searchKeyword.trim()) {
        await this.fetchAllClues();
        return;
      }
      try {
        const searchData = await searchClues(this.searchKeyword);
        this.clues = searchData;
      } catch (error) {
        console.error('搜索线索失败:', error);
        Message.error('搜索失败，请稍后重试');
      }
    }, 500),
    async fetchAllClues() {
      try {
        const response = await getAllClues();
        console.log("clues:", response);
        this.clues = response;
      } catch (error) {
        console.error('获取所有线索失败:', error);
        Message.error('获取线索列表失败，请稍后重试');
      }
    }
  },
  async created() {
    await this.fetchAllClues();
  }
};
</script>

<style scoped>
.clue-list {
  padding: 1em;
}

.search-box {
  margin-bottom: 1em;
}

.search-box input {
  width: 300px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.clue-item {
  border: 1px solid #ddd;
  margin: 10px 0;
  padding: 15px;
  border-radius: 4px;
}

.clue-item h3 {
  margin-top: 0;
  color: #333;
}

.clue-item p {
  margin: 5px 0;
}

.clue-item a {
  color: #409EFF;
  text-decoration: none;
}

.clue-item a:hover {
  text-decoration: underline;
}
</style>