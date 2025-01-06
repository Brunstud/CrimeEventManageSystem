<template>
  <div class="admin-nav">
    <h2 @click="toggleNav" class="nav-header">管理导航</h2>
    <ul v-show="isExpanded">
      <li><router-link to="/">控制台</router-link></li>
      <li><router-link to="/login">登录</router-link></li>
      <li><router-link to="/register">注册</router-link></li>
      <li><router-link to="/profile">个人资料</router-link></li>
      <li><router-link to="/events">案件列表</router-link></li>
      <li><router-link to="/events-new">新建案件</router-link></li>
      <li><router-link to="/progress/1">案件进展</router-link></li>
      <li><router-link to="/progress/1/new">新增进展</router-link></li>
      <li><router-link to="/clues">线索列表</router-link></li>
      <li><router-link to="/clues/1/upload">上传线索</router-link></li>
      <li><router-link to="/residents">居民列表</router-link></li>
      <li><router-link to="/residents/1">居民详情</router-link></li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "AdminNav",
  data() {
    return {
      showAdminNav: process.env.NODE_ENV !== 'production', // 仅在开发环境显示
      isExpanded: true
    };
  },
  methods: {
    toggleNav() {
      this.isExpanded = !this.isExpanded;
    }
  }
};
</script>

<style scoped>
.admin-nav {
  position: fixed;
  top: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.8);
  color: #fff;
  padding: 1em;
  z-index: 1000;
  width: 200px;
}
.admin-nav h2 {
  font-size: 1.2em;
  margin-bottom: 0.5em;
  cursor: pointer;
}
.admin-nav h2:hover {
  color: #ffd700;
}
.admin-nav ul {
  list-style: none;
  padding: 0;
}
.admin-nav li {
  margin: 0.5em 0;
}
.admin-nav a {
  color: #ffd700;
  text-decoration: none;
}
</style>