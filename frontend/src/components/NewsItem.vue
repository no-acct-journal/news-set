<template>
  <div class="news-item" @click="goToDetail">
    <div class="news-content">
      <div class="news-source">{{ news.author || 'News Set' }}</div>
      <h3 class="news-title">{{ news.title }}</h3>
      <p class="news-desc">{{ news.description }}</p>
      <div class="news-info">
        <span>{{ formatDateTime(news.publishTime) }}</span>
        <span class="dot"></span>
        <span>{{ news.views }} views</span>
      </div>
    </div>
    <div class="news-image" v-if="news.image">
      <img :src="news.image" :alt="news.title">
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'
import { formatDateTime } from '../utils/date'

const props = defineProps({
  news: {
    type: Object,
    required: true
  }
})

const router = useRouter()

const goToDetail = () => {
  router.push(`/news/detail/${props.news.id}`)
}
</script>

<style scoped>
.news-item {
  display: flex;
  gap: 14px;
  padding: 16px;
  border-bottom: 1px solid var(--border-color);
  background-color: var(--surface-color);
  cursor: pointer;
}

.news-content {
  flex: 1;
  min-width: 0;
  margin-right: 0;
  overflow: hidden;
}

.news-source {
  margin-bottom: 5px;
  color: var(--primary-color);
  font-size: 11px;
  font-weight: 800;
  line-height: 1.2;
  text-transform: uppercase;
}

.news-title {
  margin: 0 0 6px;
  color: var(--text-color);
  font-family: Georgia, "Times New Roman", serif;
  font-size: 18px;
  font-weight: 700;
  line-height: 1.22;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.news-desc {
  margin: 0 0 10px;
  color: var(--text-color-light);
  font-size: 13px;
  line-height: 1.35;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.news-info {
  align-items: center;
  color: var(--text-color-lighter);
  display: flex;
  font-size: 12px;
  font-weight: 600;
  line-height: 1;
}

.news-info span {
  margin-right: 8px;
}

.dot {
  width: 3px;
  height: 3px;
  background-color: var(--text-color-lighter);
  border-radius: 50%;
}

.news-image {
  width: 112px;
  height: 84px;
  flex-shrink: 0;
  background-color: var(--muted-surface-color);
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 3px;
}
</style>
