<template>
  <div id="app">
    <NavBar />
    <div class="main-content">
      <router-view/>
    </div>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'
import { EventBus } from './bus/event-bus'

export default {
  name: 'App',
  components: {
    NavBar
  },
  created() {
    // If token exists in local storage, set auth header
    const token = this.$store.state.token;
    if (token) {
        this.$http.defaults.headers.common['Authorization'] = 'Bearer ' + token;
    }

    // Global Event Listeners
    EventBus.$on('project-created', (project) => {
      this.$bvToast.toast(`Project "${project.name}" created successfully!`, {
        title: 'Success',
        variant: 'success',
        solid: true
      })
    })

    EventBus.$on('project-deleted', () => {
      this.$bvToast.toast(`Project deleted successfully`, {
        title: 'Deleted',
        variant: 'danger',
        solid: true
      })
    })

    EventBus.$on('task-updated', (task) => {
      this.$bvToast.toast(`Task "${task.title}" updated`, {
        title: 'Task Update',
        variant: 'info',
        solid: true
      })
    })
  }
}
</script>

<style>
/* Global Neo-Brutalism Theme - Retro Grid Edition */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700;900&display=swap');

:root {
  --nb-bg: #fffdf5; /* Warm White */
  --nb-primary: #FAFF00; /* Neon Yellow from image */
  --nb-secondary: #ff006e; /* Pink Dot */
  --nb-accent: #3a86ff; /* Blue Square */
  --nb-dark: #000000;
  --nb-border: 3px solid var(--nb-dark);
  --nb-bold: 700;
  --nb-shadow: 4px 4px 0 var(--nb-dark);
  --nb-shadow-hover: 6px 6px 0 var(--nb-dark);
  --nb-font: 'Space Grotesk', sans-serif;
}

body {
  font-family: var(--nb-font) !important;
  background-color: var(--nb-bg) !important;
  color: var(--nb-dark) !important;
  /* Dot Grid Pattern */
  background-image: radial-gradient(var(--nb-dark) 1px, transparent 1px) !important;
  background-size: 30px 30px !important;
}

#app {
  min-height: 100vh;
}

/* Typography Utilities */
.text-outline {
    color: transparent;
    -webkit-text-stroke: 2px var(--nb-dark);
    font-weight: 900;
    letter-spacing: 2px;
}

.text-bold {
    font-weight: 900 !important;
}

/* Navbar Styling */
.navbar {
    border-bottom: var(--nb-border) !important;
    background-color: #fff !important;
    padding: 1rem 2rem !important;
    box-shadow: var(--nb-shadow);
}

.navbar-brand {
    font-weight: 900 !important;
    text-transform: uppercase !important;
    background-color: var(--nb-dark);
    color: #fff !important;
    padding: 5px 15px !important;
    transform: rotate(-2deg); /* Slight tilt for style */
}

.nav-link {
    font-weight: 700 !important;
    color: var(--nb-dark) !important;
    text-transform: uppercase !important;
    position: relative;
}

.nav-link:hover {
    background-color: var(--nb-primary);
    box-shadow: 2px 2px 0 var(--nb-dark);
    color: var(--nb-dark) !important;
}

/* Button Overrides */
.btn {
  border-radius: 0 !important;
  border: var(--nb-border) !important;
  box-shadow: var(--nb-shadow) !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  transition: all 0.1s !important;
  margin-right: 10px;
}

/* Black Button (Primary Action) */
.btn-primary {
  background-color: var(--nb-dark) !important;
  color: #fff !important;
  border-color: var(--nb-dark) !important;
}

.btn-primary:hover {
  background-color: #333 !important;
  transform: translate(-2px, -2px);
  box-shadow: var(--nb-shadow-hover) !important;
}

/* Yellow Button (Secondary Action) */
.btn-success, .btn-warning {
    background-color: var(--nb-primary) !important;
    color: var(--nb-dark) !important;
    border-color: var(--nb-dark) !important;
}

/* Outline Button */
.btn-outline-primary, .btn-outline-secondary, .btn-outline-dark {
    background-color: #fff !important;
    color: var(--nb-dark) !important;
    border-color: var(--nb-dark) !important;
}

.btn:active {
  transform: translate(2px, 2px) !important;
  box-shadow: none !important;
}

/* Cards */
.card {
  border-radius: 0 !important;
  border: var(--nb-border) !important;
  box-shadow: var(--nb-shadow) !important;
  background-color: #fff !important;
}

.form-control, .form-select {
  border-radius: 0 !important;
  border: var(--nb-border) !important;
  background-color: #fff !important;
  box-shadow: 2px 2px 0 rgba(0,0,0,0.1) !important;
}

.form-control:focus {
    box-shadow: var(--nb-shadow) !important;
    border-color: var(--nb-dark) !important;
    background-color: var(--nb-primary) !important; /* Yellow focus */
}

/* Modal */
.modal-content {
    border-radius: 0 !important;
    border: var(--nb-border) !important;
    box-shadow: 10px 10px 0 var(--nb-dark) !important;
}
.modal-header {
    background-color: var(--nb-primary) !important;
    border-bottom: var(--nb-border) !important;
}
.modal-footer {
    border-top: var(--nb-border) !important;
}

/* Badges */
.badge {
    border: 2px solid var(--nb-dark) !important;
    border-radius: 0 !important;
    color: var(--nb-dark) !important;
    background-color: #fff !important;
    box-shadow: 2px 2px 0 var(--nb-dark);
}
</style>
