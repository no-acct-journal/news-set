<template>
  <van-tabbar v-model="active" route>
    <van-tabbar-item to="/home" icon="home-o">Home</van-tabbar-item>
    <van-tabbar-item to="/aichat" icon="chat-o">AI Chat</van-tabbar-item>
    <van-tabbar-item to="/my" icon="user-o">My</van-tabbar-item>
  </van-tabbar>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const active = ref(0)

const setActiveTab = () => {
  const path = route.path
  if (path.includes('/home')) {
    active.value = 0
  } else if (path.includes('/aichat')) {
    active.value = 1
  } else if (path.includes('/my')) {
    active.value = 2
  }
}

setActiveTab()
</script>

<style scoped>
</style>
