<template>
  <div>
    <b-navbar toggleable="lg" type="light" variant="warning" class="nb-navbar mb-4">
      <b-navbar-brand to="/" class="font-weight-bold ml-3" style="font-size: 1.5rem;">PROJECT MANAGER</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse" class="border-black"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto mr-3">
          <template v-if="!isAuthenticated">
             <b-nav-item to="/login" class="nb-nav-link">Login</b-nav-item>
             <b-nav-item to="/register" class="nb-nav-link">Register</b-nav-item>
          </template>
          <template v-else>
            <b-nav-item to="/dashboard" class="nb-nav-link">Dashboard</b-nav-item>
            <b-nav-item-dropdown right>
              <template #button-content>
                <b-avatar size="sm" variant="dark"></b-avatar> 
                <span class="font-weight-bold ml-2">{{ user ? user.username : 'User' }}</span>
              </template>
              <b-dropdown-item @click="logout" class="text-danger font-weight-bold">Sign Out</b-dropdown-item>
            </b-nav-item-dropdown>
          </template>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import { mapGetters, mapState } from 'vuex';

export default {
  computed: {
    ...mapGetters(['isAuthenticated']),
    ...mapState(['user'])
  },
  methods: {
    logout() {
      this.$store.dispatch('logout');
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.nb-navbar {
    border-bottom: 3px solid #000;
    padding: 1rem;
    background-color: #ffffff !important; /* White background */
    box-shadow: 0 4px 0 #000;
}

.nb-nav-link a {
    font-weight: 700;
    text-transform: uppercase;
    color: #000 !important;
    position: relative;
    z-index: 10;
}

.nb-nav-link a:hover {
    text-decoration: none;
    background-color: #FAFF00; /* Neon Yellow Highlight */
    box-shadow: 2px 2px 0 #000;
}

.border-black {
    border: 3px solid #000 !important;
    border-radius: 0 !important;
}
</style>
