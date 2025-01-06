<template>
  <div id="app">
    <!-- <AdminNav />         后台管理专用导航组件，仅在开发模式显示 -->
    <AppHeader />        <!-- 应用头部 -->
    <router-view />      <!-- 主视图内容 -->
    <AppFooter />        <!-- 应用底部 -->
  </div>
</template>

<script>
import AppHeader from '@/components/Header.vue';
import AppFooter from '@/components/Footer.vue';
// import AdminNav from '@/components/AdminNav.vue';

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter,
    // AdminNav
  },
  // 网页图片预加载
  beforeCreate() {
    const imgs = [
      require('@/assets/background1.png'), // 使用 require 导入图片
      require('@/assets/background2.png'),
      require('@/assets/boy_fly_lattern.jpg'),
      require('@/assets/girl_fly_lattern.jpg'),
      require('@/assets/girl_dusk.jpg'),
      require('@/assets/latterns_building.jpg'),
      require('@/assets/latterns_night_sky.jpg')
    ];
    for (let img of imgs) {
      let image = new Image();
      image.src = img; // 设置图片的 src 属性以进行预加载
    }
  }
};
</script>

<style>
/* 全局样式 */
#app {
  font-family: Arial, sans-serif;
  color: #333;
}
</style>
