import DefaultTheme from 'vitepress/theme'
import Layout from './Layout.vue'
import './custom.css'

// 继承默认主题（保留 Mermaid 等一切增强），仅替换 Layout 以加"全宽"开关
export default {
  extends: DefaultTheme,
  Layout,
}