<template>
  <div class="login-page">
    <van-nav-bar
      title="Login"
      left-arrow
      @click-left="onClickLeft"
      fixed
    />
    
    <div class="login-container">
      <div class="login-logo">
        <van-image
          width="80"
          height="80"
          src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
          round
        />
        <h2>News Set</h2>
      </div>
      
      <van-form @submit="onSubmit" class="login-form">
        <van-cell-group inset>
          <van-field
            v-model="username"
            name="username"
            label="Username"
            placeholder="Enter username"
            :rules="[{ required: true, message: 'Please enter your username' }]"
          />
          <van-field
            v-model="password"
            type="password"
            name="password"
            label="Password"
            placeholder="Enter password"
            :rules="[{ required: true, message: 'Please enter your password' }]"
          />
        </van-cell-group>
        
        <div class="submit-btn">
          <van-button round block type="primary" native-type="submit" size="large">
            Login
          </van-button>
        </div>
        
        <div class="login-tips">
          <p>Use your registered account to sign in.</p>
        </div>
      </van-form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { showToast } from 'vant';
import { useUserStore } from '../store/user';

const router = useRouter();
const userStore = useUserStore();

const username = ref('');
const password = ref('');

const onSubmit = async (values) => {
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
      
      router.push('/');
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

const onClickLeft = () => {
  router.back();
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background-color: #f7f8fa;
}

.login-container {
  padding-top: 56px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-logo {
  margin: 40px 0;
  text-align: center;
}

.login-logo h2 {
  margin-top: 16px;
  color: #323233;
  font-size: 22px;
}

.login-form {
  width: 100%;
  padding: 0 16px;
}

.submit-btn {
  margin: 24px 16px;
}

.login-tips {
  text-align: center;
  color: #969799;
  font-size: 14px;
  margin-top: 16px;
}

.login-tips p {
  margin: 8px 0;
}
</style>
