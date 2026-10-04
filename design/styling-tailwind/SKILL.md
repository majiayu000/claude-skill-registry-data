---
name: styling-tailwind
description: Tailwind CSS v4 实践。写样式时加载。用 cn()、语义色值、mobile-first 响应式、dark mode。
trigger: 需要用 Tailwind CSS 写样式
input: 组件结构
output: 样式代码
next: 无
dependencies: component-design
---

Style with these patterns:

**cn() 合并类** — `cn("base", variant === "primary" && "bg-blue-500", className)`
**语义 token** — `brand-500` 优于 `blue-500`，在 tailwind.config 里定义
**Mobile-first** — `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`（不是 max-md）
**Dark mode** — `bg-white dark:bg-gray-950`（配合 `darkMode: "class"`）
**常见布局：** 居中内容 `mx-auto max-w-7xl px-4`、粘性 header `sticky top-0 z-50 backdrop-blur`、卡片网格 `grid gap-4 sm:grid-cols-2 lg:grid-cols-3`
