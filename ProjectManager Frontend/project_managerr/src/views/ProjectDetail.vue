<template>
  <div class="project-detail container mt-5">
    <div v-if="loading" class="text-center">
      <b-spinner label="Loading..." type="grow"></b-spinner>
    </div>

    <div v-else-if="error" class="text-center text-danger">
      <b-alert show variant="danger" class="border-black shadow-hard">{{ error }}</b-alert>
      <b-button to="/dashboard" variant="outline-dark">Return to Dashboard</b-button>
    </div>

    <div v-else>
      <div class="mb-5">
        <b-button to="/dashboard" variant="link" class="text-dark font-weight-bold mb-3 pl-0 text-uppercase" style="text-decoration: none;">&larr; Back to Base</b-button>
        <div class="d-flex justify-content-between align-items-start border-bottom pb-4" style="border-bottom: 3px solid #000 !important;">
            <div>
                <h1 class="font-weight-black text-uppercase display-3" style="letter-spacing: -2px;">{{ project.name }}</h1>
                <p class="lead font-weight-bold" style="font-family: monospace;">{{ project.description }}</p>
            </div>
            <b-button variant="danger" @click="deleteProject">DELETE PROJECT</b-button>
        </div>
      </div>

      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="font-weight-black text-uppercase text-outline" style="font-size: 3rem;">TASKS</h2>
        <b-button @click="openCreateTaskModal" variant="success" size="lg">ADD TASK +</b-button>
      </div>

      <!-- Task Lists -->
      <div v-if="tasks.length === 0" class="p-5 text-center bg-white" style="border: 3px solid #000; box-shadow: 6px 6px 0 #000;">
          <h4 class="font-weight-bold">NO TASKS IN QUEUE.</h4>
      </div>
      
      <b-list-group v-else class="retro-list">
        <b-list-group-item 
          v-for="task in tasks" 
          :key="task.id" 
          class="d-flex justify-content-between align-items-center border-bottom-black p-4 mb-3 bg-white"
          style="border: 3px solid #000; box-shadow: 4px 4px 0 #000;"
        >
          <div>
            <h4 class="mb-1 font-weight-bold text-uppercase">{{ task.title }}</h4>
            <div class="d-flex align-items-center">
                <b-badge :variant="getStatusVariant(task.status)" class="mr-3">{{ task.status }}</b-badge>
                <small class="text-muted" style="font-family: monospace;">{{ task.description }}</small>
            </div>
          </div>
          <div class="d-flex align-items-center">
            
            <!-- Status Dropdown -->
            <b-dropdown size="sm" variant="outline-dark" text="UPDATE STATUS" class="mr-2">
              <b-dropdown-item @click="updateStatus(task, 'Todo')">Todo</b-dropdown-item>
              <b-dropdown-item @click="updateStatus(task, 'In Progress')">In Progress</b-dropdown-item>
              <b-dropdown-item @click="updateStatus(task, 'Done')">Done</b-dropdown-item>
            </b-dropdown>

            <b-button variant="outline-primary" size="sm" class="mr-2" @click="openEditTaskModal(task)">Edit</b-button>
            <b-button variant="outline-danger" size="sm" @click="deleteTask(task.id)">X</b-button>
          </div>
        </b-list-group-item>
      </b-list-group>
    </div>

    <!-- Modal use global styles now -->
    <b-modal id="modal-task" :title="isEditingTask ? 'EDIT TASK' : 'NEW TASK'" @ok="handleTaskSubmit" @hidden="resetTaskModal">
      <b-form-group label="TASK TITLE" class="font-weight-bold">
        <b-form-input v-model="taskForm.title" required class="py-2"></b-form-input>
      </b-form-group>
      <b-form-group label="DETAILS" class="font-weight-bold">
        <b-form-textarea v-model="taskForm.description" rows="3" class="py-2"></b-form-textarea>
      </b-form-group>
      <b-form-group label="STATUS" class="font-weight-bold">
        <b-form-select v-model="taskForm.status" :options="['Todo', 'In Progress', 'Done']"></b-form-select>
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
      project: {},
      tasks: [],
      loading: true,
      error: null,
      isEditingTask: false,
      editingTaskId: null,
      taskForm: {
        title: '',
        description: '',
        status: 'Todo'
      }
    }
  },
  async created() {
    await this.fetchProjectDetails();
    await this.fetchTasks();
  },
  methods: {
    async fetchProjectDetails() {
      try {
        const response = await axios.get(`/projects/${this.$route.params.id}/`);
        this.project = response.data;
      } catch (err) {
        this.error = "Failed to load project details.";
        console.error(err);
      }
    },
    async fetchTasks() {
      try {
        const response = await axios.get(`/projects/${this.$route.params.id}/tasks/`);
        this.tasks = response.data.results;
      } catch (err) {
        console.error("Failed to load tasks", err);
      } finally {
        this.loading = false;
      }
    },
    openCreateTaskModal() {
        this.isEditingTask = false;
        this.resetTaskModal();
        this.$bvModal.show('modal-task');
    },
    openEditTaskModal(task) {
        this.isEditingTask = true;
        this.editingTaskId = task.id;
        this.taskForm.title = task.title;
        this.taskForm.description = task.description;
        this.taskForm.status = task.status;
        this.$bvModal.show('modal-task');
    },
    resetTaskModal() {
        this.taskForm.title = '';
        this.taskForm.description = '';
        this.taskForm.status = 'Todo';
        this.editingTaskId = null;
    },
    async handleTaskSubmit(bvModalEvt) {
      if (!this.taskForm.title) {
        alert('Task title is required');
        bvModalEvt.preventDefault();
        return;
      }
      try {
        if (this.isEditingTask) {
             const response = await axios.put(`/projects/tasks/${this.editingTaskId}/`, this.taskForm);
             const updatedTask = response.data;
             // Update local list directly or fetch
             const index = this.tasks.findIndex(t => t.id === this.editingTaskId);
             if (index !== -1) {
                 this.$set(this.tasks, index, updatedTask);
             }
             EventBus.$emit('task-updated', updatedTask);
        } else {
             await axios.post(`/projects/${this.$route.params.id}/tasks/`, this.taskForm);
             await this.fetchTasks(); 
        }
        this.resetTaskModal();
      } catch (err) {
        alert('Failed to save task');
        console.error(err);
      }
    },
    async updateStatus(task, newStatus) {
      try {
        await axios.put(`/projects/tasks/${task.id}/`, { ...task, status: newStatus });
        task.status = newStatus;
        EventBus.$emit('task-updated', task);
      } catch (err) {
        alert('Failed to update status');
      }
    },
    async deleteTask(taskId) {
      if(!confirm("Are you sure?")) return;
      try {
        await axios.delete(`/projects/tasks/${taskId}/`);
        this.tasks = this.tasks.filter(t => t.id !== taskId);
        EventBus.$emit('task-updated', { title: 'Task Deleted' }); // Reusing task-updated for generic notification or create a new one
      } catch (err) {
        alert('Failed to delete task');
      }
    },
    async deleteProject() {
      if(!confirm("Are you sure you want to delete this project? This cannot be undone.")) return;
      try {
        await axios.delete(`/projects/${this.project.id}/`);
        EventBus.$emit('project-deleted');
        this.$router.push('/dashboard');
      } catch (err) {
        alert('Failed to delete project');
      }
    },
    getStatusVariant(status) {
      switch(status) {
        case 'Todo': return 'secondary';
        case 'In Progress': return 'primary';
        case 'Done': return 'success';
        default: return 'light';
      }
    }
  },
  beforeRouteLeave (to, from, next) {
    if (this.taskForm.title || this.taskForm.description) {
      const answer = window.confirm('Do you really want to leave? You have unsaved changes in the task form.')
      if (answer) {
        next()
      } else {
        next(false)
      }
    } else {
      next()
    }
  }
}
</script>

<style scoped>
.font-weight-black {
    font-weight: 900;
}
.text-outline {
    color: transparent;
    -webkit-text-stroke: 2px #000;
}
</style>
