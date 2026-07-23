import { withMermaid } from 'vitepress-plugin-mermaid'

// A 方案编号：00 全景 → 01 工具·调用·权限 → 02 Agent → … → 11 Bash 安全
const guide = [
  { text: '00 · 全景与主循环', link: '/guide/00-overview' },
  { text: '01 · 工具·调用·权限系统', link: '/guide/01-tool-call-authority' },
  { text: '02 · Agent 系统', link: '/guide/02-agent' },
  { text: '03 · Skill 系统', link: '/guide/03-skill' },
  { text: '04 · 会话管理与压缩', link: '/guide/04-session-compaction' },
  { text: '05 · MCP 协议与认证', link: '/guide/05-mcp' },
  { text: '06 · Plugin 系统', link: '/guide/06-plugin' },
  { text: '07 · Hooks 扩展系统', link: '/guide/07-hooks' },
  { text: '08 · 上下文装配与 system-reminder', link: '/guide/08-context-assembly' },
  { text: '09 · 启动与性能', link: '/guide/09-bootstrap-performance' },
  { text: '10 · 权限规则系统', link: '/guide/10-permission-rules' },
  { text: '11 · Bash / 命令安全、沙箱与分类器', link: '/guide/11-bash-security' },
]

export default withMermaid({
  lang: 'zh-Hans',
  title: 'Claude Code 核心机制剖析',
  description: '基于源码求证的 Claude Code 子系统机制解读，配 Mermaid 图。',
  lastUpdated: true,
  cleanUrls: true,
  // 仓库根的非站点 md 不要变成页面（redis 跳转仓库自带的说明文件）
  srcExclude: ['README.md', '改造.md'],
  // 部署在 yjy-blog.pages.dev 根路径
  base: '/',

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '开始阅读', link: '/guide/00-overview' },
    ],
    sidebar: {
      '/guide/': [{ text: '章节', items: guide }],
    },
    outline: { level: [2, 3], label: '本页目录' },
    docFooter: { prev: '上一篇', next: '下一篇' },
    darkModeSwitchLabel: '主题',
    sidebarMenuLabel: '菜单',
    returnToTopLabel: '回到顶部',
    lastUpdatedText: '最后更新',
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' },
          modal: {
            noResultsText: '无匹配结果',
            resetButtonTitle: '清除',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' },
          },
        },
      },
    },
  },

  mermaid: {},
})
