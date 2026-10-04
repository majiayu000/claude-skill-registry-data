---
name: gate-frontend
description: "前端开发 / Frontend development. Builds pages and components from project scaffold. Use when the project is initialized and the user wants to build the UI."
trigger: 项目已初始化，需要开发前端
input: 项目脚手架
output: 前端页面和组件
next: gate-seo
dependencies: gate-init
---

问用户："首页你想放什么？"

等用户描述完，你在后台建页面。每完成一部分用大白话解释：

**建页面时：**
"我建了一个首页，结构是：大标题区（展示你的产品名和一句话介绍）→ 功能介绍区 → 底部引导区。这样用户从上往下看，自然会被引导去行动。"

**写组件时：**
"每个功能块我拆成了独立组件，以后想换位置或者改样式，改一个地方就行，不会影响其他地方。"

**上样式时：**
"用的 Tailwind 做样式，手机和电脑上显示效果都 OK，自动适配。"

**加动效时：**
"加了滚动渐入效果，用户往下翻的时候内容会平滑出现，不会那么生硬。"

每做完一页让用户预览确认。全做完了说："页面都好了，下一步配搜索引擎，这样用户能在 Google 搜到你的网站。" → `/gate-seo`
