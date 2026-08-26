<template>
  <div class="home">
    <van-nav-bar title="News" fixed />
    
    <div class="more-options">
      <div class="more-tab" @click="goToCategory">
        More <van-icon name="arrow" />
      </div>
    </div>
    
    <div class="category-tabs">
      <van-tabs v-model:active="activeTab" sticky swipeable animated @change="onTabChange">
        <van-tab 
          v-for="category in displayCategories" 
          :key="category.id" 
          :title="getCategoryTranslation(category.name)"
        >
          <van-pull-refresh v-model="newsStore.refreshing" @refresh="onRefresh">
            <van-list
              v-model:loading="newsStore.loading"
              :finished="newsStore.finished"
              finished-text="No more"
              @load="onLoad"
            >
              <news-item 
                v-for="item in newsStore.newsList" 
                :key="item.id" 
                :news="item" 
              />
            </van-list>
          </van-pull-refresh>
        </van-tab>
      </van-tabs>
    </div>
    
    <tab-bar />
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed, onBeforeUnmount } from 'vue'
import { useNewsStore } from '../store/modules/news'
import { useRouter, useRoute } from 'vue-router'
import NewsItem from '../components/NewsItem.vue'
import TabBar from '../components/TabBar.vue'

const newsStore = useNewsStore()
const router = useRouter()
const route = useRoute()
const activeTab = ref(0)
const tabsTop = ref(0)

const displayCategories = computed(() => {
  return newsStore.categories.filter(category => category.name !== 'More');
})

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
    

const goToCategory = () => {
  router.push('/category')
}

const updateTabsPosition = () => {
  const tabsElement = document.querySelector('.van-tabs__wrap')
  if (tabsElement) {
    tabsTop.value = tabsElement.getBoundingClientRect().top
  }
}

const handleScroll = () => {
  updateTabsPosition()
}

const syncCategoryFromRoute = async () => {
  const categoryId = Number(route.query.categoryId)
  if (!categoryId) return false

  const index = displayCategories.value.findIndex(category => category.id === categoryId)
  if (index === -1) return false

  activeTab.value = index
  if (newsStore.currentCategory === categoryId) {
    if (newsStore.newsList.length === 0) {
      await newsStore.getNewsList(true)
    }
  } else {
    await newsStore.changeCategory(categoryId)
  }
  return true
}

onMounted(async () => {
  await newsStore.getCategories()
  const synced = await syncCategoryFromRoute()

  if (!synced && newsStore.newsList.length === 0) {
    await newsStore.getNewsList(true)
  }

  setTimeout(updateTabsPosition, 300)
  window.addEventListener('scroll', handleScroll)
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll)
})

watch(
  () => route.query.categoryId,
  () => {
    syncCategoryFromRoute()
  }
)

const onTabChange = (index) => {
  const category = displayCategories.value[index]
  if (!category) return
  newsStore.changeCategory(category.id)
}

const onRefresh = () => {
  newsStore.getNewsList(true)
}

const onLoad = () => {
  newsStore.getNewsList()
}
</script>

<style scoped>
.home {
  padding-top: 46px;
  padding-bottom: 50px;
  background-color: #f7f8fa;
  min-height: 100vh;
}

.category-tabs {
  margin-bottom: 10px;
  position: relative;
}

:deep(.van-tabs__wrap) {
  background-color: #fff;
}

:deep(.van-tab) {
  font-size: 14px;
}

:deep(.van-tab--active) {
  font-weight: bold;
  color: #1989fa;
}

.more-options {
  position: fixed;
  right: 0;
  background-color: #fff;
  padding: 0;
  border-radius: 4px 0 0 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  top: v-bind('tabsTop + "px"');
  height: 44px;
  display: flex;
  align-items: center;
}

.more-tab {
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #1989fa;
  font-weight: bold;
  height: 100%;
  padding: 0 10px;
}

.dropdown-menu {
  position: absolute;
  right: 15px;
  top: 40px;
  min-width: 100px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  border-radius: 4px;
  z-index: 999;
}

.dropdown-item {
  padding: 10px 15px;
  text-align: center;
  border-bottom: 1px solid #f5f5f5;
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
}
</style>
