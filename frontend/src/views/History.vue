<template>
  <div class="history-container">
    <van-nav-bar
      title="Browsing History"
      left-text="Back"
      left-arrow
      @click-left="onClickLeft"
      right-text="Clear"
      @click-right="onClickClear"
      fixed
    />
    
    <div class="history-list" v-if="historyStore.getHistory.length">
      <div class="history-item" v-for="item in historyStore.getHistory" :key="item.id">
        <van-cell @click="goToNewsDetail(item.id)" :border="false">
          <template #title>
            <div class="news-item">
              <div class="news-image" v-if="item.image">
                <img :src="item.image" :alt="item.title">
              </div>
              <div class="news-info">
                <div class="news-title">{{ item.title }}</div>
                <div class="news-meta">
                  <span>{{ item.author }}</span>
                  <span>{{ item.publishTime }}</span>
                  <span>Viewed at: {{ item.viewTime }}</span>
                </div>
              </div>
            </div>
          </template>
        </van-cell>
        <van-button 
          class="delete-btn" 
          type="danger" 
          size="mini" 
          icon="cross"
          @click="confirmDelete(item.historyId || item.id)"
        ></van-button>
      </div>
    </div>
    
    <van-empty v-else description="No browsing history" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useHistoryStore } from '../store/modules/history';
import { showDialog } from 'vant';

const router = useRouter();
const historyStore = useHistoryStore();

const onClickLeft = () => {
  router.back();
};

const goToNewsDetail = (id) => {
  router.push(`/news/detail/${id}`);
};

const removeHistory = async (id) => {
  try {
    const result = await historyStore.removeHistoryApi(id);
    console.log('Delete history result:', result);
    
    // 如果API请求失败且不是本地操作，则显示错误提示
    if (!result.success && !result.isLocal) {
      showDialog({
        title: 'Notice',
        message: result.message || 'Failed to delete. Please try again later.',
      });
    }
  } catch (error) {
    console.error('Failed to delete history:', error);
    // historyStore.removeHistory(id);
  }
};

const confirmDelete = (id) => {
  showDialog({
    title: 'Notice',
    message: 'Delete this browsing history entry?',
    showCancelButton: true,
  }).then((action) => {
    if (action === 'confirm') {
      removeHistory(id);
    }
  });
};

const onClickClear = async () => {
  showDialog({
    title: 'Notice',
    message: 'Clear all browsing history?',
    showCancelButton: true,
  }).then(async (action) => {
    if (action === 'confirm') {
      try {
        const result = await historyStore.clearHistoryApi();
        console.log('Clear history result:', result);
        
        // 如果API请求失败且不是本地操作，则显示错误提示
        if (!result.success && !result.isLocal) {
          showDialog({
            title: 'Notice',
            message: result.message || 'Failed to clear. Please try again later.',
          });
        }
      } catch (error) {
        console.error('Failed to clear history:', error);
        // 出错时仍然尝试本地清空
        // historyStore.clearHistory();
      }
    }
  });
};

onMounted(async () => {
  try {
    const result = await historyStore.getHistoryListApi();
    console.log('Browsing history API result:', result);
    
    if (!result || !result.success) {
      historyStore.loadHistory();
    }
  } catch (error) {
    console.error('Browsing history API request failed:', error);
    historyStore.loadHistory();
  }
});
</script>

<style scoped>
.history-container {
  padding-top: 46px;
  padding-bottom: 20px;
  background-color: #f7f8fa;
  min-height: 100vh;
}

.history-list {
  padding: 10px;
}

.news-item {
  display: flex;
  padding: 10px 0;
}

.news-image {
  width: 120px;
  height: 80px;
  margin-right: 12px;
  flex-shrink: 0;
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.news-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.news-title {
  font-size: 16px;
  font-weight: bold;
  line-height: 1.4;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.news-meta {
  font-size: 12px;
  color: #999;
  display: flex;
  flex-wrap: wrap;
}

.news-meta span {
  margin-right: 10px;
}

.delete-button {
  width: 20px;
  height: 20px;
  background-color: #ee0a24;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
}

.delete-btn {
  height: 100%;
  width: 65px;
}

.van-swipe-cell {
  margin-bottom: 8px;
}

.history-item {
  position: relative;
  margin-bottom: 10px;
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.delete-btn {
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  z-index: 10;
  width: 24px;
  height: 24px;
  padding: 0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-icon {
  position: absolute;
  top: 50%;
  right: 15px;
  transform: translateY(-50%);
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f2f3f5;
  border-radius: 50%;
  z-index: 2;
}
</style>
