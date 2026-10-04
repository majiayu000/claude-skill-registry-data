---
name: layouts-routing
description: Next.js App Router 布局模式。设计页面结构、路由组织、布局嵌套时加载。
trigger: 需要设计页面布局和路由
input: 页面结构需求
output: 布局和路由代码
next: 无
dependencies: 无
---

Use these App Router patterns:

**Route groups**(`(name)`) — 组织页面不影响 URL。适合分 marketing/dashboard/auth 区域
**Layout nesting** — `layout.tsx` 跨导航保持，只有 `children` 重新渲染
**Loading/Error** — 每段路由可单独配 `loading.tsx` 和 `error.tsx`（error 必须是 Client Component）
**Parallel routes**(`@slot`) — 一个布局显示多个独立页面
**Intercepting routes**(`(.)`) — 从列表进入时弹 modal，直接访问进正常页面

Default to Server Components. Push Client boundaries down — 只在需要交互的部分包 `'use client'`。
