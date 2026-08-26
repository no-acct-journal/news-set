<template>
  <div class="settings-container">
    <van-nav-bar
      title="Settings"
      left-arrow
      @click-left="onClickLeft"
    />
    
    <div class="settings-list">
      <van-cell-group inset title="Personalization">
        <van-cell title="Theme Customization" is-link @click="showThemePopup = true" />
      </van-cell-group>
      
      <van-cell-group inset title="Account">
        <van-cell title="Privacy Settings" is-link />
        <van-cell title="Notification Settings" is-link />
        <van-cell title="About Us" is-link />
      </van-cell-group>
    </div>
    
    <van-popup
      v-model:show="showThemePopup"
      position="bottom"
      round
      :style="{ height: '40%' }"
    >
      <div class="popup-title">Select Theme</div>
      <div class="theme-list">
        <div 
          v-for="theme in themeList" 
          :key="theme.id" 
          class="theme-item"
          :class="{ active: currentTheme === theme.id }"
          @click="changeTheme(theme.id)"
        >
          <div class="theme-color" :style="{ backgroundColor: theme.primaryColor }"></div>
          <div class="theme-name">{{ theme.name }}</div>
        </div>
      </div>
    </van-popup>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { showToast } from 'vant';
import { useThemeStore } from '../store/theme';

const router = useRouter();
const themeStore = useThemeStore();

const onClickLeft = () => {
  router.back();
};

const showThemePopup = ref(false);
const themeList = computed(() => themeStore.getAllThemes);
const currentTheme = computed(() => themeStore.getCurrentTheme);

const changeTheme = (themeId) => {
  themeStore.setTheme(themeId);
  showToast('Theme changed');
  showThemePopup.value = false;
};
</script>

<style scoped>
.settings-container {
  min-height: 100vh;
  background-color: var(--background-color);
  color: var(--text-color);
  padding-top: 46px;
  padding-bottom: 20px;
}

.settings-list {
  margin-top: 20px;
}

.popup-title {
  text-align: center;
  padding: 16px;
  font-size: 16px;
  font-weight: bold;
  border-bottom: 1px solid #eee;
}

.theme-list {
  display: flex;
  flex-wrap: wrap;
  padding: 16px;
}

.theme-item {
  width: 25%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 16px;
  cursor: pointer;
}

.theme-color {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-bottom: 8px;
  border: 2px solid transparent;
}

.theme-item.active .theme-color {
  border-color: #1989fa;
}

.theme-name {
  font-size: 12px;
}

</style>
