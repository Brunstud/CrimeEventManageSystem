import { getAllClues, getCluesByEventId, uploadClue } from '@/services/clueService';

const state = {
  clues: []
};

const mutations = {
  SET_CLUES(state, clues) {
    state.clues = clues;
  },
  ADD_CLUE(state, clue) {
    state.clues.push(clue);
  }
};

const actions = {
  async fetchAllClues({ commit }) {
    try {
      const clues = await getAllClues();
      commit('SET_CLUES', clues);
    } catch (error) {
      console.error('获取所有线索失败:', error);
    }
  },
  async fetchCluesByEventId({ commit }, eventId) {
    try {
      const clues = await getCluesByEventId(eventId);
      commit('SET_CLUES', clues);
    } catch (error) {
      console.error(`获取案件ID ${eventId} 的线索失败:`, error);
    }
  },
  async uploadClue({ commit }, clueData) {
    try {
      const clue = await uploadClue(clueData);
      commit('ADD_CLUE', clue);
    } catch (error) {
      console.error('提交线索失败:', error);
      throw error;
    }
  }
};

const getters = {
  clues: (state) => state.clues
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};
