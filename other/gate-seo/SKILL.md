---
name: gate-seo
description: SEO 阶段。前端完成后加载。先问 2 个简单问题，然后按 P0→P1→P2 顺序执行完整的 SEO 检查与修复。
trigger: 前端开发完成，需要优化 SEO
input: 前端代码
output: SEO 优化后的代码
next: gate-optimize
dependencies: gate-frontend
---

用户不需要懂 SEO。只需问 2 个问题：

1. "你的网站用一句话怎么介绍？" → 用作搜索结果描述
2. "你觉得用户会搜什么词找到你？" → 列出 3-5 个核心词

然后在后台加载 `/seo-copywriting`、`/seo-checklist` 和 `/seo-metadata`，按以下顺序执行：

## 执行顺序（严格 P0 → P1 → P2）

### P0 — 关键项（自动修复）

1. **用 seo-copywriting 生成每页的 title + description**
   - 加载 `/seo-copywriting`，传入页面主题 + 目标关键词
   - 为每个页面生成优化的 title（50-65字符）和 description（150-155字符）
   - 确保品牌名统一、关键词前置

2. **检查所有 page.tsx 的 metadata 导出**
   - 使用 `generateSiteMetadata`，不是手写 Metadata 对象
   - 法律页（privacy、disclaimer）也必须用 `generateSiteMetadata`
   - 首页必须有独立的 `metadata` export

3. **检查品牌拼写**
   - 搜索所有页面 metadata 的 `pageTitle`，确认品牌拼写正确
   - 搜索页面正文，修正拼写错误

4. **检查 Title 格式**
   - em dash 前后加空格
   - 长度 50-65 字符
   - 含品牌名 + 页面主题 + 年份

5. **检查 Description 长度**
   - 裁剪到 150-155 字符
   - 含 2-3 个目标关键词

### P1 — 重要项（自动修复）

6. **检查结构化数据**
   - 每个页面有对应的 JSON-LD schema
   - VideoGame schema 必须含 `aggregateRating` + `offers`
   - 共享包有 `generateVideoGameJsonLd` 或手写完整版

7. **检查 canonical/OG**
   - 所有页面设置 `canonicalPath`
   - `generateSiteMetadata` 自动生成 OG + Twitter Card

7. **检查内部链接网络**
   - 指南页交叉链接（guide/classes/items/tier）
   - FAQ 答案嵌指向详细页面的链接
   - 平台/购买/需求页之间有链接

8. **检查 Sitemap + Robots**
   - 所有可索引页面在 sitemap
   - 新增页面同步更新 sitemap 数组

### P2 — 加分项（检查并建议）

9. 检查 favicon 完整性
10. 检查图片 alt 文本
11. 检查 h1 层级
12. 建议 OG 图片独立化
13. 建议 hreflang（如多语言）
14. 检查图片格式（WebP 推荐）

## 大白话解释给用户

每做完一步，用一句话告诉用户做了什么：

- "我用标题公式和强力词库给每页写了标题和描述，点击率会更高。"
- "我在每页加了标题和描述，用户在 Google 看到的就是这些。"
- "我检查了品牌名有没有写错——全站统一了。"
- "我配好了结构化数据，Google 能看到你的评分和价格标签。"
- "我补了内部链接，让搜索引擎能爬到所有页面。"
- "我给网站生成了 Sitemap，告诉 Google 你的网站有哪些页面。"

完成后汇报状态："SEO 全部没问题 ✅" 或 "有几个建议项 ⚠️"

然后建议下一步：`/gate-optimize`