<template>
  <div class="login-page">
    <section class="login-hero">
      <div class="brand-row">
        <van-image
          width="44"
          height="44"
          src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
          round
        />
        <div>
          <div class="brand-name">News Set</div>
          <div class="brand-subtitle">Daily news, saved reads, AI answers</div>
        </div>
      </div>

      <div class="headline">
        <h1>Stay current without the noise.</h1>
        <p>Sign in to continue your personalized news feed.</p>
      </div>
    </section>

    <main class="login-container">
      <section class="login-panel">
        <div class="panel-header">
          <h2>Welcome back</h2>
          <p>Sync favorites, reading history, and AI chat across your account.</p>
        </div>

        <van-form @submit="onSubmit" class="login-form">
          <van-cell-group inset class="field-group">
            <van-field
              v-model="username"
              name="username"
              label="Username"
              placeholder="Enter username"
              left-icon="user-o"
              :rules="[{ required: true, message: 'Please enter your username' }]"
            />
            <van-field
              v-model="password"
              type="password"
              name="password"
              label="Password"
              placeholder="Enter password"
              left-icon="lock"
              :rules="[{ required: true, message: 'Please enter your password' }]"
            />
          </van-cell-group>

          <div class="submit-btn">
            <van-button round block type="primary" native-type="submit" size="large">
              Login
            </van-button>
          </div>

          <div class="login-footer">
            <span>New to News Set?</span>
            <button type="button" @click="goToRegister">Create account</button>
          </div>
        </van-form>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { showToast } from 'vant';
import { useUserStore } from '../store/user';

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const username = ref('');
const password = ref('');

const onSubmit = async () => {
  showToast({
    type: 'loading',
    message: 'Logging in...',
    forbidClick: true,
    duration: 0
  });

  try {
    const result = await userStore.login({
      username: username.value,
      password: password.value
    });

    if (result.success) {
      showToast({
        type: 'success',
        message: result.message
      });

      router.replace(route.query.redirect || '/home');
    } else {
      showToast({
        type: 'fail',
        message: result.message
      });
    }
  } catch (error) {
    showToast({
      type: 'fail',
      message: 'Login failed. Please try again later'
    });
  }
};

const goToRegister = () => {
  router.push('/register');
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background:
    linear-gradient(180deg, rgba(25, 137, 250, 0.12), transparent 34%),
    var(--background-color);
  color: var(--text-color);
  overflow: hidden;
}

.login-hero {
  padding: 32px 24px 28px;
  background: #172033;
  color: #fff;
}

.brand-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-name {
  font-size: 18px;
  font-weight: 800;
  line-height: 1.2;
}

.brand-subtitle {
  color: rgba(255, 255, 255, 0.68);
  font-size: 12px;
  margin-top: 2px;
}

.headline {
  margin-top: 38px;
}

.headline h1 {
  font-size: 30px;
  line-height: 1.18;
  margin: 0;
  max-width: 320px;
}

.headline p {
  color: rgba(255, 255, 255, 0.72);
  font-size: 15px;
  line-height: 1.5;
  margin: 12px 0 0;
}

.login-container {
  padding: 18px 16px 32px;
}

.login-panel {
  background: var(--white);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: 0 14px 30px rgba(23, 32, 51, 0.08);
  padding: 20px 0 18px;
}

.panel-header {
  padding: 0 20px 14px;
}

.panel-header h2 {
  color: var(--text-color);
  font-size: 22px;
  line-height: 1.3;
  margin: 0;
}

.panel-header p {
  color: var(--text-color-light);
  font-size: 14px;
  line-height: 1.5;
  margin: 6px 0 0;
}

.login-form {
  width: 100%;
}

.field-group {
  margin: 0 12px;
}

.submit-btn {
  margin: 22px 20px 0;
}

.login-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: var(--text-color-light);
  margin-top: 18px;
}

.login-footer button {
  border: 0;
  background: transparent;
  color: var(--primary-color);
  font: inherit;
  font-weight: 700;
  padding: 0;
}
</style>
