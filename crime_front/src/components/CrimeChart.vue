<template>
    <div>
      <canvas id="crime-chart" width="400" height="200"></canvas>
    </div>
  </template>
  
  <script>
  import { Chart, registerables } from 'chart.js';
  
  Chart.register(...registerables);
  
  export default {
    name: "CrimeChart",
    props: {
      labels: Array,      // X轴标签，如月份
      dataPoints: Array,  // Y轴数据，如每月犯罪数量
      chartTitle: String  // 图表标题
    },
    mounted() {
      // 创建图表实例
      new Chart(document.getElementById("crime-chart"), {
        type: "bar", // 这里可以选择 "line", "bar" 等类型
        data: {
          labels: this.labels,
          datasets: [{
            label: this.chartTitle,
            data: this.dataPoints,
            backgroundColor: "rgba(54, 162, 235, 0.6)"
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: true
            },
            title: {
              display: true,
              text: this.chartTitle
            }
          }
        }
      });
    }
  };
  </script>
  
  <style scoped>
  canvas {
    max-width: 100%;
    height: auto;
  }
  </style>
  