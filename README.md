# yjy-blog

Cloudflare Pages 项目，一个仓库两用：

- **`/`** → VitePress 博客《Claude Code 核心机制剖析》（12 篇 + 首页）
- **`/redis`** → 302 跳转到微信公众号 Redis 文章专辑（`functions/redis.js`）

## 路由原理

Cloudflare Pages **Functions 优先于静态资源**：

- 访问 `/redis`：先命中 `functions/redis.js`，服务端 302 跳公众号（不经过博客）。
- 访问 `/`、`/guide/*`：无对应函数 → 由 VitePress 构建产物（静态）提供。

以后要加更多公众号短链，只需在 `functions/` 下新增 `<名字>.js`（照抄 `redis.js`，换 `target`），即得 `/<名字>` 跳转。

## 目录

```
yjy-blog/
├── functions/
│   └── redis.js          # /redis → 公众号（保留）
├── .vitepress/
│   ├── config.mts        # 侧边栏/主题/Mermaid/中文/搜索/srcExclude
│   ├── linkify.py        # 交叉引用转链接 + 编号平移
│   └── escape_angles.py  # 散文裸 < 转义
├── guide/                # 12 篇（由 sync.sh 从 analysis 生成，勿手改）
├── index.md              # 博客首页
├── sync.sh               # 从内容源重生 guide/
└── package.json
```

## 本地开发

```bash
npm install
npm run docs:dev       # 博客预览 http://localhost:5173
npm run docs:build     # 构建到 .vitepress/dist
```

同时联测博客 + `/redis` 跳转（需 wrangler）：

```bash
npm run docs:build
npx wrangler pages dev .vitepress/dist   # 会自动挂载 functions/
# 访问 http://localhost:8788/ 看博客，/redis 测跳转
```

## 内容更新

正文只在内容源仓库 `claude-code-learn/analysis/` 改，然后：

```bash
bash sync.sh           # 从 analysis 重新拷贝 + 平移编号 + 转义（勿手改 guide/）
npm run docs:build
```

> `sync.sh` 默认从 `/Users/jieyongyang/work/claude-code-learn/analysis` 取源，可用 `ANALYSIS_SRC=... bash sync.sh` 覆盖。

## Cloudflare Pages 设置（从纯跳转站迁到博客时改这几项）

| 设置项 | 旧值 | 新值 |
|--------|------|------|
| Build command | 留空 | `npm run docs:build` |
| Build output directory | `public` | `.vitepress/dist` |
| 环境变量 | — | `NODE_VERSION = 20` |

`functions/` 在仓库根，Cloudflare 自动识别，不受 output 目录变化影响。改完设置并 push 到主分支即自动重建。

## 说明（原跳转仓库遗留）

- `/redis` 只是"中转跳转"，最终打开的仍是 `mp.weixin.qq.com`；目标链接含 `sessionid`/`pass_ticket` 等参数，后续可能失效，建议换更稳定的原始微信链接。