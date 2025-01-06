import axios from 'axios';
import { Message } from 'element-ui';

// 创建一个 Axios 实例
const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api', // 后端 API 的基础路径
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器 - 添加授权令牌
axiosInstance.interceptors.request.use(
  (config) => {
    console.log("正在添加令牌");
    if (!config.url.includes('login') && !config.url.includes('register')) {
      const token = JSON.parse(localStorage.getItem('token'));
      console.log("发送令牌:", token);
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器 - 统一处理错误
axiosInstance.interceptors.response.use(
  (response) => response, // 请求成功时返回响应
  (error) => {
    // 检查响应是否有状态码
    if (error.response) {
      const { status } = error.response;

      // 处理 403 Forbidden 错误
      if (status === 403) {
        Message.error("访问被拒绝：您没有执行此操作的权限");
      }

      // 处理 401 Unauthorized 错误 - 未授权，可能是登录过期或未登录
      else if (status === 401) {
        Message.error("需要身份验证，请先登录");
        // 未授权时自动跳转到登录页面
        window.location = '/login';
      }

      // 处理其他错误 - 例如服务器错误或网络错误
      else {
        Message.error(`发生错误：${error.response.statusText || '请稍后重试'}`);
      }
    } else {
      // 处理没有响应的错误（例如网络问题）
      Message.error("网络错误：请检查您的网络连接");
    }

    // 将错误传递到调用代码，以便调用处根据需要处理
    return Promise.reject(error);
  }
);

export default axiosInstance;
