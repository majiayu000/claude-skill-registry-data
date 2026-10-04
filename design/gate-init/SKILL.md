---
name: gate-init
description: "项目初始化 / Project scaffolding. Scaffolds a new Next.js project step by step. Use when the user confirms they want to build a new site or start a new app."
trigger: 需求已明确，需要初始化项目
input: 需求文档
output: 项目脚手架
next: gate-frontend
dependencies: 无
---

用户说"好，开始搭"。直接执行：

1. 建项目：
   ```
   npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
   ```
   告诉用户："正在搭架子——用的 Next.js 是目前最流行的网站框架，Tailwind 负责样式，TypeScript 让代码更健壮。"

2. 装 UI 组件：
   ```
   npx shadcn@latest init -d
   npx shadcn@latest add button card dialog form input sheet tabs toast
   ```
   告诉用户："装好了一套现成的 UI 组件库，按钮、弹窗、表单这些不用自己从头写了。"

3. 配好工具函数 `src/lib/utils.ts`（cn 合并样式类）

4. `git init && git add . && git commit -m "chore: scaffold"`
   告诉用户："代码已经用 Git 管起来了，以后改了什么一目了然。"

5. `npm run build` 确认能跑
   告诉用户："项目搭好了，跑了一遍构建没报错。接下来你想做什么页面？"
