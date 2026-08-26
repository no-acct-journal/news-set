<template>
  <div class="category">
    <van-nav-bar 
      title="All Categories" 
      left-text="Back"
      left-arrow
      @click-left="onClickLeft"
      fixed 
    />
    
    <div class="category-container">
      <van-grid :column-num="3" :border="false">
        <van-grid-item 
          v-for="category in displayCategories" 
          :key="category.id"
          :text="getCategoryTranslation(category.name)"
          icon="newspaper-o"
          @click="goToCategoryNews(category.id)"
        />
      </van-grid>
    </div>
    
    <tab-bar />
  </div>
</template>

<script setup>
import { useNewsStore } from '../store/modules/news'
import { useRouter } from 'vue-router'
import TabBar from '../components/TabBar.vue'
import { computed, onMounted } from 'vue'

const newsStore = useNewsStore()
const router = useRouter()

const displayCategories = computed(() => {
  return newsStore.categories.filter(category => category.name !== 'More');
})

onMounted(() => {
  if (newsStore.categories.length === 0) {
    newsStore.getCategories()
  }
})

const onClickLeft = () => {
  router.back()
}

const goToCategoryNews = (categoryId) => {
  newsStore.changeCategory(categoryId)
  
  router.push({
    path: '/home',
    query: { categoryId: categoryId }
  })
}

const getCategoryTranslation = (categoryName) => {
  const categoryMap = {
    '头条': 'Headlines',
    '社会': 'Society',
    '国内': 'Domestic',
    '国际': 'International',
    '娱乐': 'Entertainment',
    '体育': 'Sports',
    '军事': 'Military',
    '科技': 'Technology',
    '财经': 'Finance',
    '更多': 'More',
  };
  
  return categoryMap[categoryName] || categoryName;
}
</script>

<style scoped>
.category {
  padding-top: 46px;
  padding-bottom: 50px;
  background-color: #f7f8fa;
  min-height: 100vh;
}

.category-container {
  padding: 16px;
  background-color: #fff;
  margin-top: 12px;
  border-radius: 8px;
}

:deep(.van-grid-item__content) {
  background-color: #f5f7fa;
  border-radius: 8px;
  padding: 20px 0;
}

:deep(.van-grid-item__icon) {
  font-size: 28px;
  color: #1989fa;
}

:deep(.van-grid-item__text) {
  margin-top: 8px;
  color: #333;
  font-size: 14px;
}
</style>
