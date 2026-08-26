<template>
  <div class="home">
    <van-nav-bar title="News Set" right-text="Sections" fixed :border="false" @click-right="goToCategory" />
    
    <div class="category-tabs">
      <van-tabs v-model:active="activeTab" sticky swipeable animated :offset-top="46" @change="onTabChange">
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
import { ref, onMounted, watch, computed } from 'vue'
import { useNewsStore } from '../store/modules/news'
import { useRouter, useRoute } from 'vue-router'
import NewsItem from '../components/NewsItem.vue'
import TabBar from '../components/TabBar.vue'

const newsStore = useNewsStore()
const router = useRouter()
const route = useRoute()
const activeTab = ref(0)

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
  background-color: var(--background-color);
  min-height: 100vh;
}

.category-tabs {
  margin-bottom: 12px;
  position: relative;
}

:deep(.van-tabs__wrap) {
  height: 44px;
  background-color: rgba(255, 255, 255, 0.96);
  border-bottom: 1px solid var(--border-color);
  backdrop-filter: blur(18px);
}

:deep(.van-tab) {
  flex: none;
  padding: 0 14px;
  color: var(--text-color-light);
  font-size: 13px;
  font-weight: 700;
}

:deep(.van-tab--active) {
  color: var(--text-color);
}

:deep(.van-tabs__line) {
  width: 22px;
  height: 3px;
  background: var(--primary-color);
  border-radius: 0;
}

:deep(.van-list) {
  background-color: var(--surface-color);
}
</style>
