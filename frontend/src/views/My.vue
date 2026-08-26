<template>
  <div class="my-container">
    <van-nav-bar title="My" />
    <div class="profile-panel" @click="goToProfile" v-if="isLogin">
      <div class="avatar">
        <van-image
          round
          width="80"
          height="80"
          src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
        />
      </div>
      <div class="info">
        <div class="username">{{ userInfo?.username || 'Not logged in' }}</div>
        <div class="desc" v-if="isLogin">{{ userBio || 'Bio' }}</div>
      </div>
      <van-icon name="arrow" class="arrow-icon" />
    </div>
    <div class="profile-panel" v-else>
      <div class="avatar">
        <van-image
          round
          width="80"
          height="80"
          src="https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
        />
      </div>
      <div class="info">
        <div class="username">Not logged in</div>
        <div class="auth-actions">
          <van-button type="primary" size="small" @click="goToLogin">Login</van-button>
          <van-button type="default" size="small" @click="goToRegister">Register</van-button>
        </div>
      </div>
    </div>

    <div class="menu-list">
      <van-cell-group inset>
        <van-cell title="My Favorites" is-link @click="goToFavorite" />
        <van-cell title="Browsing History" is-link @click="goToHistory" />
        <van-cell title="Notifications" is-link />
        <van-cell title="Settings" is-link @click="goToSettings" />
        <van-cell v-if="isLogin" title="Logout" @click="handleLogout" />
      </van-cell-group>
    </div>
    <tab-bar />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useUserStore } from '../store/user';
import { useRouter } from 'vue-router';
import { computed } from 'vue';
import { showDialog, showToast } from 'vant';
import TabBar from '../components/TabBar.vue';

const userStore = useUserStore();
const router = useRouter();

const userInfo = computed(() => userStore.userInfo);
const isLogin = computed(() => userStore.getLoginStatus);
const userBio = computed(() => userStore.getUserBio || 'Bio');

const goToLogin = () => {
  router.push('/login');
};

const goToRegister = () => {
  router.push('/register');
};

const goToProfile = () => {
  if (isLogin.value) {
    router.push('/profile');
  }
};

const goToHistory = () => {
  if (isLogin.value) {
    router.push('/history');
  } else {
    showToast('Please log in');
    router.push('/login');
  }
};

const goToFavorite = () => {
  if (isLogin.value) {
    router.push('/favorite');
  } else {
    showToast('Please log in');
    router.push('/login');
  }
};

const goToSettings = () => {
  router.push('/settings');
};

const handleLogout = () => {
  showDialog({
    title: 'Confirm',
    message: 'Logout?',
    showCancelButton: true,
  }).then((action) => {
    if (action === 'confirm') {
      userStore.logout();
      router.push('/login');
    }
  });
};

onMounted(async () => {
  try {
    await userStore.getUserInfoDetail();
  } catch (error) {
    console.error('Failed to get user information:', error);
  }
});
</script>

<style scoped>
.my-container {
  padding-top: 46px;
  padding-bottom: 50px;
  background-color: var(--background-color);
  color: var(--text-color);
  min-height: 100vh;
  box-sizing: border-box;
}

.van-nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 999;
}

.profile-panel {
  display: flex;
  align-items: center;
  padding: 18px 16px;
  background-color: var(--surface-color);
  color: var(--text-color);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  margin: 16px;
  position: relative;
  box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
}

.arrow-icon {
  position: absolute;
  right: 16px;
  color: var(--text-color-lighter);
}

.avatar {
  margin-right: 16px;
}

.info {
  flex: 1;
}

.username {
  color: var(--text-color);
  font-size: 20px;
  font-weight: 800;
  margin-bottom: 4px;
}

.desc {
  font-size: 14px;
  color: var(--text-color-light);
}

.auth-actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}

.menu-list {
  margin: 0 16px;
}

:deep(.van-cell-group--inset) {
  margin: 0;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  overflow: hidden;
}

:deep(.van-cell) {
  align-items: center;
  color: var(--text-color);
  font-weight: 700;
}

:deep(.van-cell::after) {
  border-color: var(--border-color);
}
</style>
