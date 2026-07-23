<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import { ref, onMounted } from 'vue'

const { Layout } = DefaultTheme
const wide = ref(false)

function apply(v: boolean) {
  if (typeof document !== 'undefined') {
    document.documentElement.classList.toggle('wide-mode', v)
  }
}
function toggle() {
  wide.value = !wide.value
  apply(wide.value)
  try {
    localStorage.setItem('vp-wide-mode', wide.value ? '1' : '0')
  } catch {}
}
onMounted(() => {
  try {
    wide.value = localStorage.getItem('vp-wide-mode') === '1'
  } catch {}
  apply(wide.value)
})
</script>

<template>
  <Layout>
    <!-- 导航栏右侧加一个全宽开关：点一下收起左右目录、正文铺满，再点恢复 -->
    <template #nav-bar-content-after>
      <button
        class="wide-toggle"
        type="button"
        :title="wide ? '显示左右目录' : '隐藏左右目录，正文全宽'"
        @click="toggle"
      >
        {{ wide ? '↤ 目录' : '⛶ 全宽' }}
      </button>
    </template>
  </Layout>
</template>

<style scoped>
.wide-toggle {
  margin-left: 8px;
  padding: 0 10px;
  height: 32px;
  line-height: 30px;
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
  font-size: 13px;
  color: var(--vp-c-text-2);
  background: transparent;
  cursor: pointer;
  transition: color 0.2s, border-color 0.2s;
  white-space: nowrap;
}
.wide-toggle:hover {
  color: var(--vp-c-brand-1);
  border-color: var(--vp-c-brand-1);
}
/* 窄屏本来就是抽屉式目录，隐藏这个开关避免重复 */
@media (max-width: 959px) {
  .wide-toggle { display: none; }
}
</style>