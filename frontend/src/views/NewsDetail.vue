<template>
  <div class="news-detail">
    <van-nav-bar
      title="News Detail"
      left-text="Back"
      left-arrow
      @click-left="onClickLeft"
      fixed
    />
    
    <div class="detail-content" v-if="newsStore.newsDetail.id">
      <div class="title-container">
        <div class="article-kicker">{{ newsStore.newsDetail.author || 'News Set' }}</div>
        <h1 class="title">{{ newsStore.newsDetail.title }}</h1>
        <van-button 
          class="favorite-btn" 
          :icon="isFavorite ? 'star' : 'star-o'" 
          :class="{ 'is-favorite': isFavorite }"
          @click="toggleFavorite"
        />
      </div>
      
      <div class="info">
        <span>{{ formatDateTime(newsStore.newsDetail.publishTime) }}</span>
        <span class="dot"></span>
        <span>{{ newsStore.newsDetail.views }} views</span>
      </div>
      
      <div class="cover" v-if="newsStore.newsDetail.image">
        <img :src="newsStore.newsDetail.image" :alt="newsStore.newsDetail.title">
      </div>
      
      <div class="content">
        <p v-for="(paragraph, index) in contentParagraphs" :key="index">
          {{ paragraph }}
        </p>
      </div>
      
      <div class="related-news" v-if="newsStore.newsDetail.relatedNews?.length">
        <h3>Related News</h3>
        <div class="related-list">
          <div 
            class="related-item" 
            v-for="item in newsStore.newsDetail.relatedNews" 
            :key="item.id"
            @click="goToRelatedNews(item.id)"
          >
            <div class="related-image">
              <img :src="item.image" :alt="item.title">
            </div>
            <div class="related-title">{{ item.title }}</div>
          </div>
        </div>
      </div>
    </div>
    
    <van-empty v-else description="Loading..." />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNewsStore } from '../store/modules/news'
import { useHistoryStore } from '../store/modules/history'
import { useFavoriteStore } from '../store/modules/favorite'
import { useUserStore } from '../store/user'
import { showToast } from 'vant'
import { formatDateTime } from '../utils/date'

const route = useRoute()
const router = useRouter()
const newsStore = useNewsStore()
const historyStore = useHistoryStore()
const favoriteStore = useFavoriteStore()
const userStore = useUserStore()

const newsId = computed(() => Number(route.params.id))

const contentParagraphs = computed(() => {
  if (!newsStore.newsDetail.content) return []
  return newsStore.newsDetail.content.split('\n\n').filter(p => p.trim())
})

const onClickLeft = () => {
  router.back()
}

const goToRelatedNews = (id) => {
  router.push(`/news/detail/${id}`)
}

const isFavorite = computed(() => {
  return favoriteStore.isFavorite(newsId.value)
})

const toggleFavorite = async () => {
  if (!userStore.getLoginStatus) {
    showToast({
      message: 'Please log in before adding favorites',
      position: 'bottom',
    })
    router.push('/login')
    return
  }
  
  const status = await favoriteStore.toggleFavorite(newsStore.newsDetail)
  
  if (status === true) {
    showToast({
      message: 'Added to favorites',
      position: 'bottom',
    })
  } else if (status === false) {
    showToast({
      message: 'Removed from favorites',
      position: 'bottom',
    })
  } else {
    showToast({
      message: 'Operation failed. Please try again later',
      position: 'bottom',
    })
  }
}

onMounted(async () => {
  await newsStore.getNewsDetail(newsId.value)
  
  if (newsStore.newsDetail.id) {
    if (userStore.getLoginStatus) {
      try {
        const result = await historyStore.addHistoryApi(newsStore.newsDetail.id);
        console.log('Add browsing history result:', result);
      } catch (error) {
        console.error('Failed to add browsing history:', error);
      }
    }
    
    // 无论API是否成功，都添加到本地浏览历史
    // historyStore.addHistory(newsStore.newsDetail);
  }
  
  favoriteStore.loadFavorites()
  
  if (userStore.getLoginStatus && newsStore.newsDetail.id) {
    const result = await favoriteStore.checkFavoriteStatusApi(newsStore.newsDetail.id)
    if (result.success && !result.isLocal) {
      if (result.isFavorite && !favoriteStore.isFavorite(newsStore.newsDetail.id)) {
        favoriteStore.addFavorite(newsStore.newsDetail)
      } else if (!result.isFavorite && favoriteStore.isFavorite(newsStore.newsDetail.id)) {
        favoriteStore.removeFavorite(newsStore.newsDetail.id)
      }
    }
  }
})
</script>

<style scoped>
.news-detail {
  padding-top: 46px;
  background-color: var(--surface-color);
  min-height: 100vh;
}

.detail-content {
  padding: 22px 18px 36px;
}

.title-container {
  position: relative;
  margin-bottom: 10px;
  padding-right: 42px;
}

.article-kicker {
  margin-bottom: 8px;
  color: var(--primary-color);
  font-size: 12px;
  font-weight: 800;
  line-height: 1;
  text-transform: uppercase;
}

.title {
  color: var(--text-color);
  font-family: Georgia, "Times New Roman", serif;
  font-size: 30px;
  font-weight: 700;
  line-height: 1.12;
  margin: 0;
}

.favorite-btn {
  position: absolute;
  top: -6px;
  right: 0;
  padding: 0;
  width: 34px;
  height: 34px;
  border: 1px solid var(--border-color);
  border-radius: 50%;
  background-color: var(--surface-color);
}

.favorite-btn.is-favorite {
  color: var(--primary-color);
}

.info {
  align-items: center;
  display: flex;
  font-size: 12px;
  color: var(--text-color-lighter);
  font-weight: 600;
  margin-bottom: 18px;
}

.info span {
  margin-right: 8px;
}

.dot {
  width: 3px;
  height: 3px;
  background-color: var(--text-color-lighter);
  border-radius: 50%;
}

.cover {
  margin: 0 -18px 22px;
  background-color: var(--muted-surface-color);
}

.cover img {
  width: 100%;
  display: block;
}

.content {
  color: var(--text-color);
  font-family: Georgia, "Times New Roman", serif;
  font-size: 18px;
  line-height: 1.72;
}

.content p {
  margin-bottom: 18px;
}

.related-news {
  margin: 30px -18px 0;
  padding: 20px 18px 0;
  border-top: 8px solid var(--background-color);
}

.related-news h3 {
  color: var(--text-color);
  font-size: 16px;
  font-weight: 800;
  margin: 0 0 16px;
  text-transform: uppercase;
}

.related-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.related-item {
  display: flex;
  align-items: center;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color);
}

.related-image {
  width: 80px;
  height: 60px;
  margin-right: 12px;
  flex-shrink: 0;
}

.related-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 3px;
}

.related-title {
  color: var(--text-color);
  font-family: Georgia, "Times New Roman", serif;
  font-size: 15px;
  font-weight: 700;
  line-height: 1.3;
  flex: 1;
}
</style>
