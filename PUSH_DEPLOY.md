# 一键部署说明（推送到 GitHub → Cloudflare 自动更新）

本地代码已打好 **1 个提交**，只差推送到 GitHub。

## 方式一：在 Cursor 里推送（推荐）

1. 左侧点 **Source Control**（分支图标）
2. 确认显示 `main`，有 **1 commit to push**
3. 点 **Push** / **Sync**
4. 若提示登录 GitHub，用浏览器完成授权

## 方式二：终端推送

在终端执行（会提示登录 GitHub）：

```bash
cd /Users/buaichifan/Desktop/gift_site_fixed
git push origin main
```

若 HTTPS 失败，可改用 SSH（需先在 GitHub 添加 SSH 公钥）：

```bash
git remote set-url origin git@github.com:faisalhalim4637733624-sketch/cixiangift-website.git
git push origin main
```

## 推送成功后

1. 打开 [GitHub 仓库](https://github.com/faisalhalim4637733624-sketch/cixiangift-website/commits/main) 确认最新提交
2. Cloudflare → **Workers & Pages** → 你的项目 → **Deployments**，等待 **Success**（约 1–3 分钟）
3. 检查网站：
   - https://cixiangift.com/
   - 页面源代码里 canonical 应为 `https://cixiangift.com/`
   - https://cixiangift.com/products （约 22 个产品）

## 若 Cloudflare 没有自动部署

确认项目已连接该仓库的 **main** 分支，且 **Build command 为空**、输出目录为 `/`。

## 以后更新流程

1. 本地 `http://localhost:8899/admin.html` 改产品 → Save → Generate Website  
2. `git add -A && git commit -m "更新产品" && git push`
