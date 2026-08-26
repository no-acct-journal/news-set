import { defineStore } from 'pinia';

export const useThemeStore = defineStore('theme', {
  state: () => ({
    currentTheme: localStorage.getItem('theme') || 'light',
    themes: {
      light: {
        name: 'Light',
        backgroundColor: '#f5f6f8',
        textColor: '#161616',
        primaryColor: '#c1121f',
        secondaryColor: '#f0f2f5',
        surfaceColor: '#ffffff',
      },
      dark: {
        name: 'Dark',
        backgroundColor: '#121212',
        textColor: '#ffffff',
        primaryColor: '#ff4d5a',
        secondaryColor: '#2d2d2d',
        surfaceColor: '#1d1d1f',
      },
      blue: {
        name: 'Blue',
        backgroundColor: '#f4f7fb',
        textColor: '#172033',
        primaryColor: '#2557a7',
        secondaryColor: '#e7edf7',
        surfaceColor: '#ffffff',
      },
      green: {
        name: 'Green',
        backgroundColor: '#f4f7f5',
        textColor: '#17231c',
        primaryColor: '#1f7a4d',
        secondaryColor: '#e5f0ea',
        surfaceColor: '#ffffff',
      }
    }
  }),
  
  getters: {
    getCurrentTheme: (state) => state.currentTheme,
    getThemeConfig: (state) => state.themes[state.currentTheme],
    getAllThemes: (state) => Object.keys(state.themes).map(key => ({
      id: key,
      name: state.themes[key].name,
      primaryColor: state.themes[key].primaryColor
    }))
  },
  
  actions: {
    setTheme(themeName) {
      if (this.themes[themeName]) {
        this.currentTheme = themeName;
        localStorage.setItem('theme', themeName);
        this.applyTheme();
      }
    },
    
    applyTheme() {
      const theme = this.themes[this.currentTheme];
      document.documentElement.style.setProperty('--background-color', theme.backgroundColor);
      document.documentElement.style.setProperty('--text-color', theme.textColor);
      document.documentElement.style.setProperty('--primary-color', theme.primaryColor);
      document.documentElement.style.setProperty('--secondary-color', theme.secondaryColor);
      document.documentElement.style.setProperty('--muted-surface-color', theme.secondaryColor);
      document.documentElement.style.setProperty('--surface-color', theme.surfaceColor);
    },
    
    initTheme() {
      this.applyTheme();
    }
  }
});
