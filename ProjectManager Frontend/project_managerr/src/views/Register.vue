<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card p-0" style="border: 3px solid #000; box-shadow: 8px 8px 0 #000;">
          <div class="card-header border-bottom-0 text-center py-4" style="background-color: #FAFF00; border-bottom: 3px solid #000 !important;">
              <h2 class="font-weight-black m-0 p-0 text-uppercase" style="letter-spacing: -1px; font-size: 2.5rem;">NEW USER PROTOCOL</h2>
          </div>
          
          <div class="card-body p-4 bg-white">
            <b-form @submit.prevent="onSubmit">
              <b-form-group label="CHOOSE IDENTIFIER" class="font-weight-bold">
                <b-form-input v-model="form.username" required placeholder="USERNAME" class="py-2" style="border: 2px solid #000; background: #fff;"></b-form-input>
              </b-form-group>
              
              <b-form-group label="EMAIL ADDRESS" class="font-weight-bold">
                <b-form-input type="email" v-model="form.email" required placeholder="CONTACT EMAIL" class="py-2" style="border: 2px solid #000; background: #fff;"></b-form-input>
              </b-form-group>
              
              <b-form-group label="SECURITY CODE" class="font-weight-bold">
                <b-form-input type="password" v-model="form.password" required placeholder="********" class="py-2" style="border: 2px solid #000; background: #fff;"></b-form-input>
              </b-form-group>

              <b-form-group label="CONFIRM CODE" class="font-weight-bold">
                 <b-form-input type="password" v-model="form.password_confirm" required placeholder="********" class="py-2" style="border: 2px solid #000; background: #fff;"></b-form-input>
              </b-form-group>

              <b-alert v-if="error" show variant="danger" class="border-black font-weight-bold">{{ error }}</b-alert>
              
              <b-button type="submit" variant="primary" block size="lg" class="mt-4 border-0" style="background: #000; color: #FAFF00;">ESTABLISH ACCOUNT</b-button>
            </b-form>

             <div class="text-center mt-4">
                <router-link to="/login" class="font-weight-bold text-dark text-uppercase" style="text-decoration: underline;">Return to Login</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        password_confirm: ''
      },
      error: null
    }
  },
  methods: {
    async onSubmit() {
      if (this.form.password !== this.form.password_confirm) {
        this.error = "Passwords do not match!";
        return;
      }
      try {
        await this.$store.dispatch('register', this.form);
        this.$router.push('/dashboard');
      } catch (err) {
        this.error = err.response && err.response.data.detail ? err.response.data.detail : 'Registration failed';
      }
    }
  }
}
</script>

<style scoped>
.font-weight-black {
    font-weight: 900;
}
</style>
