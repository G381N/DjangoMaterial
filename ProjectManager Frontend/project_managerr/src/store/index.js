import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

// Set base URL for axios
axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';

export default new Vuex.Store({
    state: {
        token: localStorage.getItem('token') || '',
        user: JSON.parse(localStorage.getItem('user')) || null
    },
    mutations: {
        auth_success(state, { token, user }) {
            state.token = token
            state.user = user
        },
        logout(state) {
            state.token = ''
            state.user = null
        }
    },
    actions: {
        async login({ commit }, userCreds) {
            const response = await axios.post('/auth/login/', userCreds);
            const token = response.data.access;
            const user = response.data.user;

            localStorage.setItem('token', token);
            localStorage.setItem('user', JSON.stringify(user));
            // Set default header for future requests
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;

            commit('auth_success', { token, user });
            return response;
        },
        async register({ commit }, userData) {
            const response = await axios.post('/auth/register/', userData);
            const token = response.data.access;
            const user = response.data.user;

            localStorage.setItem('token', token);
            localStorage.setItem('user', JSON.stringify(user));
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;

            commit('auth_success', { token, user });
            return response;
        },
        logout({ commit }) {
            commit('logout');
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            delete axios.defaults.headers.common['Authorization'];
        }
    },
    getters: {
        isAuthenticated: state => !!state.token,
        user: state => state.user
    }
})
