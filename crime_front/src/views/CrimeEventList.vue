<template>
  <div class="event-list">
    <div class="header">
      <h2>犯罪事件列表</h2>
    </div>
    <!-- 搜索框 -->
    <div class="search-box">
      <input 
        type="text" 
        v-model="searchKeyword"
        placeholder="输入关键词搜索案件..."
        @input="handleSearch"
      >
    </div>
    <!-- 表格显示犯罪事件 -->
    <table border="1" cellspacing="0" cellpadding="8">
      <thead>
        <tr>
          <th>案件描述</th>
          <th>主要类型</th>
          <th>主要犯罪嫌疑人</th>
          <th>主要受害人</th>
          <th>主要作案工具</th>
          <th>案发地点</th>
          <th>当前状态</th>
          <th>操作</th>
          <th>案发时间</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="event in events" :key="event.id">
          <td>{{ event.crimeDesc }}</td>
          <td>{{ event.mainType }}</td>
          <td>{{ event.mainCriminal }}</td>
          <td>{{ event.mainVictim }}</td>
          <td>{{ event.mainWeapon }}</td>
          <td>{{ event.block }}</td>
          <td>{{ event.curStatus }}</td>
          <td>
            <router-link :to="'/events/' + event.id">查看详情</router-link>
          </td>
          <td>{{ formatDateTime(event.timeOccurred) }}</td>
        </tr>
      </tbody>
    </table>
    <!-- 分页控件 -->
    <div class="pagination">
      <button :disabled="currentPage === 1" @click="fetchEvents(currentPage - 1)">上一页</button>
      <span>第 {{ currentPage }} 页 / 共 {{ totalPages }} 页</span>
      <button :disabled="currentPage >= totalPages" @click="fetchEvents(currentPage + 1)">下一页</button>
    </div>
    <!-- 添加事件按钮 -->
    <div class="add-event-button">
      <el-button type="primary" @click="$router.push('/events-new')">添加事件</el-button>
    </div>
  </div>
</template>

<script>
import { getAllCrimeEvents, searchCrimeEvents } from '@/services/crimeEventService';
import { Message } from 'element-ui';
import debounce from 'lodash/debounce';

export default {
  name: 'CrimeEventList',
  data() {
    return {
      events: [], // 存储当前页的犯罪事件数据
      currentPage: 1, // 当前页码
      pageSize: 10, // 每页显示的数据条数
      hasNextPage: false, // 是否有下一页数据
      totalPages: 1, // 添加总页数属性
      searchKeyword: '', // 搜索关键词
    };
  },
  methods: {
    async fetchEvents(page = 1) {
      try {
        const crimeData = await getAllCrimeEvents(page, this.pageSize);
        console.log("crimeData:", crimeData);
        this.events = crimeData.results; // 获取当前页的犯罪事件数据
        this.currentPage = page; // 更新当前页码
        this.hasNextPage = !!crimeData.next; // 判断是否存在下一页
        // 计算总页数
        if (crimeData.count) {
          this.totalPages = Math.ceil(crimeData.count / this.pageSize);
        }
      } catch (error) {
        console.error("获取事件列表失败:", error);
        Message.error("加载犯罪事件列表失败，请稍后重试。");
      }
    },
    // 添加日期格式化方法
    formatDateTime(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    },
    // 搜索方法
    handleSearch: debounce(async function() {
      if (!this.searchKeyword.trim()) {
        await this.fetchEvents(1);
        return;
      }
      try {
        const searchData = await searchCrimeEvents(this.searchKeyword);
        this.events = searchData.results;
        this.totalPages = Math.ceil(searchData.count / this.pageSize);
        this.currentPage = 1;
      } catch (error) {
        console.error("搜索失败:", error);
        Message.error("搜索失败，请稍后重试。");
      }
    }, 500),
  },
  async created() {
    await this.fetchEvents(); // 初次加载第一页数据
  },
};
</script>

<style scoped>
.event-list {
  padding: 1em;
}
.action-bar {
  margin-bottom: 1em;
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
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1em;
}
th, td {
  text-align: left;
  padding: 0.5em;
}
th {
  background-color: #f4f4f4;
}
a {
  color: #3498db;
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
.pagination {
  margin-top: 1em;
  display: flex;
  justify-content: center;
  gap: 1em;
}
button {
  padding: 0.5em 1em;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
  cursor: pointer;
}
button:disabled {
  background-color: #e0e0e0;
  cursor: not-allowed;
}
.add-event-button {
  margin-top: 2em;
  text-align: center;
}
</style>
