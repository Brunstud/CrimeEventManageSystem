import Vue from 'vue';
import Vuex from 'vuex';
import user from './modules/user';
import crimeEvent from './modules/crimeEvent';
import clue from './modules/clue';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    user,
    crimeEvent,
    clue
  }
});
