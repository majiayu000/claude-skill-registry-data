---
name: seo-checklist
description: SEO 完整检查清单。网站上线前或 SEO 整改后加载。自动逐项检查，只问用户不知道的内容（关键词、网站描述）。
trigger: 需要进行 SEO 检查
input: 网站信息
output: SEO 检查报告
next: 无
dependencies: 无
---

# SEO 完整检查清单

用户不需要懂 SEO。问 2 个问题：
1. "用哪几个关键词？" — 用户说 3-5 个核心词
2. "网站一句话介绍？" — 用户描述

然后在后台逐项检查并修复。

---

## 🔴 P0 — 关键项（必须通过）

### 1. 每页 metadata
- [ ] 所有 page.tsx 导出 `metadata` — 使用 `generateSiteMetadata(site, { ... })` 语法
- [ ] 法律页（privacy / disclaimer / tos）**也**用 `generateSiteMetadata` — 不要手写原始 `Metadata`
- [ ] 首页有独立 `metadata` 导出——不依赖 layout.tsx 默认值

### 2. 品牌一致性
- [ ] 所有 pageTitle 中品牌名**拼写正确**（MECCHA 不是 MECCA 等）
- [ ] 页面正文中也无品牌拼写错误

### 3. Title 格式
- [ ] 含品牌名，50-65 字符
- [ ] 分隔符统一：em dash（`—`）前后各一个空格
- [ ] 尾部年份 `(2026)`（或当前年份）

### 4. Description 长度
- [ ] 目标 150-155 字符，不超过 160 字符
- [ ] 不低于 100 字符
- [ ] 是一段完整通顺的话，含 2-3 个关键词

## 🟡 P1 — 重要项

### 5. 结构化数据
- [ ] 首页：VideoGame schema（含 `aggregateRating` + `offers` + `operatingSystem`）
- [ ] FAQ 页：FAQPage schema（所有问答对）
- [ ] 评测页：Review schema
- [ ] 购买页：Product + Offer schema
- [ ] 所有内容页：BreadcrumbList schema
- [ ] 其他页面（平台/需求/模式指南）：VideoGame schema
- [ ] **关键**：VideoGame JSON-LD 必须含 `aggregateRating`（触发星级评分）和 `offers`（触发价格标签）

### 6. canonical / OG / Twitter
- [ ] 所有 content 页面设置 `canonicalPath`
- [ ] OG title + OG description + OG image 存在（通过 `generateSiteMetadata` 自动获得）
- [ ] Twitter Card 存在（通过 `generateSiteMetadata` 自动获得）

### 7. 内部链接
- [ ] 指南类页面互相交叉链接（guide → classes → items → tier 互链）
- [ ] 平台/购买/需求页之间有链接
- [ ] FAQ 答案文本嵌有指向详细页面的链接
- [ ] 首页有链接到主要子页

### 8. 标题/描述文本质量
- [ ] em dash 前后有空格（`— Word` 而非 `—Word`）
- [ ] 页面描述各不相同，不重复
- [ ] 页面标题包含页面主题关键词

## 🟢 P2 — 加分项

### 9. Sitemap
- [ ] 所有可索引页面在 sitemap 中
- [ ] noindex 页面（privacy/tos/disclaimer）在 sitemap 中有但 priority 低
- [ ] `/jump` 不在 sitemap 中
- [ ] sitemap 中 changeFrequency + priority 合理分级

### 10. Robots
- [ ] `allow: "/"`
- [ ] `disallow: ["/jump", "/api/"]`
- [ ] sitemap URL 正确

### 11. 技术项
- [ ] 每页一个 `<h1>`，层级不乱（h1 → h2 → h3）
- [ ] HTML lang 属性正确（`<html lang="en">`）
- [ ] favicon 存在（至少 SVG）
- [ ] theme-color meta 标签存在

### 12. 页面内容
- [ ] 每页正文 >= 300 字
- [ ] 图片有 alt 文本
- [ ] 没有占位文本或重复内容

## 📋 输出格式

检查完后，按以下格式输出：

```
## SEO 检查结果

### ✅ 全部通过（N 项）
列出已通过的项

### ⚠️ 建议项（N 项）
列出需要用户决策的项（关键词选择、页面方向等）

### ❌ 技术问题（N 项）
列出自动修复的问题
```

不需要展示技术细节给用户。只汇报状态和需要用户决定的点。
