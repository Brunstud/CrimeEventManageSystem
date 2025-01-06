<template>
    <div id="crime-map" style="height: 400px;"></div>
  </template>
  
  <script>
  import L from 'leaflet';
  import 'leaflet/dist/leaflet.css';
  
  export default {
    name: "CrimeMap",
    props: {
      events: Array // 接收一个事件数据数组
    },
    mounted() {
      // 初始化地图
      this.map = L.map("crime-map").setView([40.7128, -74.0060], 12); // 默认定位在纽约
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map);
  
      // 根据传入的事件数据绘制热点
      this.events.forEach(event => {
        L.marker([event.latitude, event.longitude])
          .addTo(this.map)
          .bindPopup(`<b>${event.crimeDesc}</b><br>${event.location}`);
      });
    }
  };
  </script>
  
  <style scoped>
  #crime-map {
    width: 100%;
    height: 100%;
  }
  </style>
  