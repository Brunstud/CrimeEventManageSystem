import { login, logout, register, getCurrentUser } from '@/services/authService';

const state = {
  currentUser: getCurrentUser() || null,
  isAuthenticated: !!getCurrentUser()
};

const mutations = {
  SET_USER(state, user) {
    state.currentUser = user;
    state.isAuthenticated = true;
  },
  CLEAR_USER(state) {
    state.currentUser = null;
    state.isAuthenticated = false;
  }
};

const actions = {
  async login({ commit }, { email, password }) {
    try {
      const user = await login(email, password);
      commit('SET_USER', user);
      return user;
    } catch (error) {
      console.error("Login failed:", error);
      throw error;
    }
  },
  async logout({ commit }) {
    try {
      // 调用导入的 logout 函数
      await logout();
      
      // 清除用户状态
      commit('CLEAR_USER');
      return true;
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  },
  async register({ commit }, { fullname, email, password }) {
    try {
      const user = await register(fullname, email, password);
      commit('SET_USER', user);
      return user;
    } catch (error) {
      console.error("Registration failed:", error);
      throw error;
    }
  }
};

const getters = {
  currentUser: (state) => state.currentUser,
  isAuthenticated: (state) => state.isAuthenticated
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};
