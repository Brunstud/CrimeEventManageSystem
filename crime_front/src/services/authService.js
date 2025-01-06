import axiosInstance from './axiosInstance';
import { Message } from 'element-ui';

const API_URL = '/auth/';

/**
 * 用户登录
 * @param {string} email - 用户邮箱
 * @param {string} password - 用户密码
 * @returns {Promise<Object>} - 返回包含用户信息和 JWT 令牌的对象
 */
export const login = async (email, password) => {
  try {
    // 发送登录请求到服务器
    const response = await axiosInstance.post(`${API_URL}login/`, {
      email,
      password
    });

    // 打印响应以确认 token 是否正确返回
    console.log('Login response:', response.data);

    // 如果登录成功，服务器会返回 token，将 token 保存到本地存储中
    if (response.data.token) {
      localStorage.setItem('token', JSON.stringify(response.data.token));
      console.log('Save token');
    }
    if (response.data.user) {
      console.log('Save user');
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }

    return response.data;
  } catch (error) {
    if (error.response) {
      console.error("Error response:", error.response.data);
      Message.error(error.response.data.detail || "登录失败,请重试。");
    } else {
      Message.error("无法连接到服务器。");
    }
    throw error;
  }
};

/**
 * 注销用户
 */
export const logout = () => {
  // 从本地存储中移除用户数据，注销后清除本地 token
  localStorage.removeItem('user');
  localStorage.removeItem('token');
};

/**
 * 用户注册
 * @param {string} fullname - 用户全名
 * @param {string} email - 用户邮箱
 * @param {string} password - 用户密码
 * @param {string} contact - 联系方式
 * @param {string} address - 地址
 * @param {string} role - 角色
 * @returns {Promise<Object>} - 返回包含用户信息的对象
 */
export const register = async (fullname, email, password, contact = '', address = '', role = 'Officer') => {
  try {
    // 发送注册请求到服务器
    const response = await axiosInstance.post(`${API_URL}register/`, {
      fullname,
      email,
      password,
      contact,
      address,
      role
    });

    return response.data; // 返回注册成功的用户信息
  } catch (error) {
    console.error("Registration failed:", error); // 打印错误信息
    throw error;
  }
};

/**
 * 获取当前登录用户信息
 * @returns {Object|null} - 返回当前用户信息或 null
 */
export const getCurrentUser = () => {
  // 从本地存储中获取用户信息并解析为对象
  return JSON.parse(localStorage.getItem('user'));
};

/**
 * 绑定身份信息
 * @param {boolean} is_police - 是否为警察
 * @param {number} person_id - 人员ID
 * @param {number} officer_id - 警官ID
 * @returns {Promise<Object>} - 返回绑定结果
 */
export const bindIdentity = async (is_police, person_id, officer_id) => {
  try {
    const response = await axiosInstance.post(`${API_URL}bind-identity/`, {
      is_police,
      person_id,
      officer_id
    });
    return response.data;
  } catch (error) {
    console.error("Identity binding failed:", error);
    throw error;
  }
};
