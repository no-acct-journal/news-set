import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import pinia from './store'

// Import Vant components.
import { 
  Button, 
  NavBar, 
  Tabbar, 
  TabbarItem, 
  Tab, 
  Tabs, 
  List, 
  PullRefresh, 
  Cell, 
  CellGroup,
  Grid,
  GridItem,
  Empty,
  Form,
  Field,
  Image,
  Toast,
  Icon,
  Popup,
  Radio,
  RadioGroup
} from 'vant'

import 'vant/lib/index.css'

import './style.css'

const app = createApp(App)

app.use(Button)
app.use(NavBar)
app.use(Tabbar)
app.use(TabbarItem)
app.use(Tab)
app.use(Tabs)
app.use(List)
app.use(PullRefresh)
app.use(Cell)
app.use(CellGroup)
app.use(Grid)
app.use(GridItem)
app.use(Empty)
app.use(Form)
app.use(Field)
app.use(Image)
app.use(Toast)
app.use(Icon)
app.use(Popup)
app.use(Radio)
app.use(RadioGroup)

app.use(router)
app.use(pinia)

app.mount('#app')

// Initialize theme.
import { useThemeStore } from './store/theme'
const themeStore = useThemeStore()
themeStore.initTheme()
