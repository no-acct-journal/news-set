import { defineStore } from 'pinia';
import axios from 'axios';
import { apiConfig } from '../config/api';

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null,
    token: '',
    isLogin: false,
    userBio: 'This is my bio'
  }),
  
  getters: {
    getUserInfo: (state) => state.userInfo,
    getToken: (state) => state.token,
    getLoginStatus: (state) => state.isLogin,
    getUserBio: (state) => state.userInfo?.bio || state.userBio
  },
  
  actions: {
    async login(userData) {
      try {
        const response = await axios.post(`${apiConfig.baseURL}/api/user/login`, {
          username: userData.username,
          password: userData.password
        });
        
        if (response.data && response.data.code === 200) {
          const userInfo = response.data.data.userInfo;
          const token = response.data.data.token;
          
          this.userInfo = userInfo;
          this.token = token;
          this.isLogin = true;
          
          return {
            success: true,
            message: 'Login successful'
          };
        } else {
          return {
            success: false,
            message: response.data.message || 'Login failed'
          };
        }
      } catch (error) {
        console.error('Login request failed:', error);
        return {
          success: false,
          message: error.response?.data?.message || 'Login request failed. Please try again later'
        };
      }
    },
    
    async register(userData) {
      try {
        const response = await axios.post(`${apiConfig.baseURL}/api/user/register`, {
          username: userData.username,
          password: userData.password
        });
        
        if (response.data && response.data.code === 200) {
          const userInfo = response.data.data.userInfo;
          const token = response.data.data.token;
          
          this.userInfo = userInfo;
          this.token = token;
          this.isLogin = true;
          
          return {
            success: true,
            message: 'Registration successful'
          };
        } else {
          return {
            success: false,
            message: response.data.message || 'Registration failed'
          };
        }
      } catch (error) {
        console.error('Registration request failed:', error);
        return {
          success: false,
          message: error.response?.data?.message || 'Registration request failed. Please try again later'
        };
      }
    },
    
    logout() {
      this.userInfo = null;
      this.token = '';
      this.isLogin = false;
    },
    
    async getUserInfoDetail() {
      try {
        if (!this.token) {
          return {
            success: false,
            message: 'Not logged in'
          };
        }
        
        const response = await axios.get(`${apiConfig.baseURL}/api/user/info`, {
          headers: {
            Authorization: this.token
          }
        });
        
        if (response.data && response.data.code === 200) {
          this.userInfo = response.data.data;
          
          return {
            success: true,
            message: 'User information retrieved successfully',
            data: response.data.data
          };
        } else {
          return {
            success: false,
            message: response.data.message || 'Failed to get user information'
          };
        }
      } catch (error) {
        console.error('Get user information request failed:', error);
        return {
          success: false,
          message: error.response?.data?.message || 'Failed to get user information. Please try again later'
        };
      }
    },
    
    async updateUserBio(bio) {
      try {
        if (!this.token) {
          return {
            success: false,
            message: 'Not logged in'
          };
        }
        
        const response = await axios.put(`${apiConfig.baseURL}/api/user/update`, 
          { bio },
          {
            headers: {
              Authorization: this.token
            }
          }
        );
        
        if (response.data && response.data.code === 200) {
          this.userInfo = response.data.data || { ...(this.userInfo || {}), bio };
          
          return {
            success: true,
            message: 'Bio updated successfully'
          };
        } else {
          return {
            success: false,
            message: response.data.message || 'Failed to update bio'
          };
        }
      } catch (error) {
        console.error('Update bio request failed:', error);
        return {
          success: false,
          message: error.response?.data?.message || 'Failed to update bio. Please try again later'
        };
      }
    },
    
    async updatePassword(oldPassword, newPassword) {
      try {
        if (!this.token) {
          return {
            success: false,
            message: 'Not logged in'
          };
        }
        
        const response = await axios.put(`${apiConfig.baseURL}/api/user/password`, 
          { 
            oldPassword,
            newPassword 
          },
          {
            headers: {
              Authorization: this.token
            }
          }
        );
        
        if (response.data && response.data.code === 200) {
          return {
            success: true,
            message: 'Password changed successfully'
          };
        } else {
          return {
            success: false,
            message: response.data.message || 'Failed to change password'
          };
        }
      } catch (error) {
        console.error('Change password request failed:', error);
        return {
          success: false,
          message: error.response?.data?.message || 'Failed to change password. Please try again later'
        };
      }
    }
  },
  
  persist: {
    key: 'user-store',
    storage: localStorage,
    pick: ['userInfo', 'token', 'isLogin']
  }
});
