# yjy-blog

这是一个最小可部署的 Cloudflare Pages 项目，用来把短路径 `/redis` 跳转到一条很长的微信公众号文章专辑链接。

## 项目结构

- `public/index.html`：静态首页，用作兜底展示
- `functions/index.js`：访问根路径 `/` 时，自动跳转到 `/redis`
- `functions/redis.js`：访问 `/redis` 时，返回 `302` 跳转到目标微信链接

## 部署到 Cloudflare Pages

1. 把当前仓库推到 GitHub、GitLab 或 Cloudflare 可连接的代码仓库。
2. 在 Cloudflare 后台创建一个新的 Pages 项目，并绑定这个仓库。
3. 构建命令留空。
4. Build output directory 设置为 `public`。
5. 完成部署后，访问 `https://你的项目.pages.dev/` 或 `https://你的项目.pages.dev/redis`。

## 本地预览

如果本机已经安装 `wrangler`，可以在项目根目录执行：

```bash
wrangler pages dev public
```

启动后访问 `http://127.0.0.1:8788/redis` 即可测试跳转。

## 说明

- 这只是一个“中转跳转”，不是把微信链接真正替换成你的域名，最终打开的仍然是 `mp.weixin.qq.com`。
- 目标链接里包含 `sessionid`、`pass_ticket` 这类参数，后续可能失效。
- 这个链接对应的是微信公众号“文章专辑/合集”类型，不是图片相册。
- 如果要长期使用，建议换成更稳定的原始微信链接。
- 正式使用时，通常自定义域名会比 `*.pages.dev` 更稳。
