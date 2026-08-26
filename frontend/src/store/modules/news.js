import { defineStore } from 'pinia'
import axios from 'axios'
import { apiConfig } from '../../config/api'

const PAGE_SIZE = 10

const fallbackCategories = [
  { id: 1, name: 'Top Stories' },
  { id: 2, name: 'World' },
  { id: 3, name: 'Technology' },
  { id: 4, name: 'Business' },
  { id: 5, name: 'Sports' },
  { id: 6, name: 'Entertainment' },
  { id: 7, name: 'Science' },
  { id: 8, name: 'Health' },
]

export const useNewsStore = defineStore('news', {
  state: () => ({
    newsList: [],
    newsDetail: {},
    categories: [],
    currentCategory: 1,
    loading: false,
    refreshing: false,
    finished: false,
    categoriesLoading: false,
  }),

  actions: {
    async getCategories() {
      if (this.categoriesLoading) return

      this.categoriesLoading = true

      try {
        const response = await axios.get(`${apiConfig.baseURL}/api/news/categories`)

        if (response.data?.code === 200) {
          this.categories = [...response.data.data, { id: 'more', name: 'More' }]

          if (!this.currentCategory && this.categories.length > 0) {
            this.currentCategory = this.categories[0].id
          }
        }
      } catch (error) {
        console.error('Failed to get news categories:', error)
        this.categories = [...fallbackCategories, { id: 'more', name: 'More' }]
      } finally {
        this.categoriesLoading = false
      }
    },

    async changeCategory(categoryId) {
      if (categoryId === 'more' || this.currentCategory === categoryId) return

      this.currentCategory = categoryId
      this.newsList = []
      this.finished = false
      await this.getNewsList(true)
    },

    async getNewsList(isRefresh = false) {
      if (this.loading && !isRefresh) return

      if (isRefresh) {
        this.refreshing = true
        this.newsList = []
        this.finished = false
      }

      if (this.finished && !isRefresh) return

      this.loading = true

      try {
        const params = {
          categoryId: this.currentCategory,
          page: isRefresh ? 1 : Math.floor(this.newsList.length / PAGE_SIZE) + 1,
          pageSize: PAGE_SIZE,
        }

        const response = await axios.get(`${apiConfig.baseURL}/api/news/list`, { params })

        if (response.data?.code === 200) {
          const newsData = response.data.data.list || []

          this.newsList = isRefresh ? newsData : [...this.newsList, ...newsData]
          this.finished = response.data.data.hasMore === false || newsData.length < PAGE_SIZE
        }
      } catch (error) {
        console.error('Failed to get news list:', error)
      } finally {
        this.loading = false
        this.refreshing = false
      }
    },

    async getNewsDetail(id) {
      this.newsDetail = {}

      try {
        const response = await axios.get(`${apiConfig.baseURL}/api/news/detail`, {
          params: { id },
        })

        if (response.data?.code === 200) {
          this.newsDetail = response.data.data
        } else {
          console.error('Failed to get news detail: API returned an error')
        }
      } catch (error) {
        console.error('Failed to get news detail:', error)
      }
    },

    getCategoryName(categoryId) {
      const category = this.categories.find(item => item.id === categoryId)
      return category ? category.name : 'Unknown'
    },
  },
})
