import { getAllCrimeEvents, getCrimeEventById, createCrimeEvent } from '@/services/crimeEventService';

const state = {
  events: [],
  currentEvent: null
};

const mutations = {
  SET_EVENTS(state, events) {
    state.events = events;
  },
  SET_CURRENT_EVENT(state, event) {
    state.currentEvent = event;
  }
};

const actions = {
  async fetchEvents({ commit }) {
    try {
      const events = await getAllCrimeEvents();
      commit('SET_EVENTS', events);
    } catch (error) {
      console.error("Failed to fetch events:", error);
    }
  },
  async fetchEventById({ commit }, eventId) {
    try {
      const event = await getCrimeEventById(eventId);
      commit('SET_CURRENT_EVENT', event);
    } catch (error) {
      console.error(`Failed to fetch event with ID ${eventId}:`, error);
    }
  },
  async createEvent({ dispatch }, eventData) {
    try {
      await createCrimeEvent(eventData);
      dispatch('fetchEvents'); // 重新获取事件列表
    } catch (error) {
      console.error("Failed to create event:", error);
      throw error;
    }
  }
};

const getters = {
  events: (state) => state.events,
  currentEvent: (state) => state.currentEvent
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
};
