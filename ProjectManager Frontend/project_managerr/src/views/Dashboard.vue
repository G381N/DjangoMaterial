<template>
  <div class="dashboard container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-5">
      <h1 class="font-weight-black m-0 text-uppercase display-3" style="font-size: 4rem; letter-spacing: -2px;">
        MY <span class="text-outline">PROJECTS</span>
      </h1>
      <b-button @click="openCreateModal" variant="primary" size="lg" class="px-4 py-2">Create Project +</b-button>
    </div>

    <!-- Project List -->
    <div v-if="loading" class="text-center">
      <b-spinner label="Loading..." type="grow" style="width: 3rem; height: 3rem;"></b-spinner>
    </div>
    
    <div v-else-if="projects.length === 0" class="text-center p-5 border-black bg-white" style="border: 3px solid #000; box-shadow: 4px 4px 0 #000;">
      <h3 class="font-weight-bold">SYSTEM STATUS: EMPTY</h3>
      <p class="mb-4">No projects found in the database.</p>
      <b-button @click="openCreateModal" variant="primary">Initialize First Project</b-button>
    </div>

    <b-row v-else>
      <b-col md="6" lg="4" v-for="project in projects" :key="project.id" class="mb-5">
        <b-card
          tag="article"
          class="h-100 project-card"
          no-body
        >
          <div class="card-body d-flex flex-column">
              <h4 class="card-title font-weight-bold text-uppercase mb-3">{{ project.name }}</h4>
              <p class="card-text flex-grow-1 text-muted" style="font-family: monospace;">
                {{ project.description || '> No description provided.' }}
              </p>
          </div>
          <div class="card-footer bg-transparent border-top-0 pt-0 pb-3">
            <div class="d-flex justify-content-between align-items-center w-100">
                <b-button :to="'/projects/' + project.id" variant="outline-dark" size="sm" class="flex-grow-1 mr-2">ACCESS</b-button>
                <b-button @click="openEditModal(project)" variant="outline-secondary" size="sm">EDIT</b-button>
            </div>
          </div>
        </b-card>
      </b-col>
    </b-row>

    <!-- Modal use global styles -->
    <b-modal id="modal-project" :title="isEditing ? 'EDIT PROJECT' : 'NEW PROJECT'" @ok="handleProjectSubmit" @hidden="resetModal">
      <b-form-group label="PROJECT DESIGNATION" class="font-weight-bold">
        <b-form-input v-model="form.name" required placeholder="Project Name..." class="py-2"></b-form-input>
      </b-form-group>
      <b-form-group label="DESCRIPTION LOG" class="font-weight-bold">
        <b-form-textarea v-model="form.description" rows="3" placeholder="Enter details..." class="py-2"></b-form-textarea>
      </b-form-group>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import { EventBus } from '../bus/event-bus';

export default {
  data() {
    return {
      projects: [],
      loading: true,
      isEditing: false,
      editingId: null,
      form: {
        name: '',
        description: ''
      }
    }
  },
  async created() {
    await this.fetchProjects();
  },
  methods: {
    async fetchProjects() {
      this.loading = true;
      try {
        const response = await axios.get('/projects/');
        this.projects = response.data.results;
      } catch (error) {
        console.error("Error fetching projects", error);
      } finally {
        this.loading = false;
      }
    },
    openCreateModal() {
        this.isEditing = false;
        this.resetModal();
        this.$bvModal.show('modal-project');
    },
    openEditModal(project) {
        this.isEditing = true;
        this.editingId = project.id;
        this.form.name = project.name;
        this.form.description = project.description;
        this.$bvModal.show('modal-project');
    },
    resetModal() {
        this.form.name = '';
        this.form.description = '';
        this.editingId = null;
    },
    async handleProjectSubmit(bvModalEvt) {
      if (!this.form.name) {
        alert('Please enter a project name');
        bvModalEvt.preventDefault();
        return;
      }
      
      try {
        let response;
        if (this.isEditing) {
            response = await axios.put(`/projects/${this.editingId}/`, this.form);
            EventBus.$emit('project-updated', response.data); 
        } else {
            response = await axios.post('/projects/', this.form);
            EventBus.$emit('project-created', response.data);
        }
        
        await this.fetchProjects(); 
        this.resetModal();
      } catch (error) {
        console.error("Error saving project", error);
        alert('Failed to save project');
      }
    }
  }
}
</script>

<style scoped>
.project-card {
    transition: transform 0.1s;
    background-color: #fff;
    border: 3px solid #000;
}
.project-card:hover {
    transform: translate(-4px, -4px);
    box-shadow: 8px 8px 0 #000 !important;
    background-color: #FAFF00 !important; /* Neon Yellow hover */
}
</style>
