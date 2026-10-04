---
name: gate-animate
description: "动效优化 / Animation. Adds motion, transitions, and UI animations. Use when the user wants to add animation effects to their site."
trigger: 需要添加动效
input: 动效需求
output: 动效实现
next: 无
dependencies: gate-optimize
---

问："想在哪加动效？比如页面切换、滚动渐入、按钮反馈。"

实现后告诉用户：
"加了滚动渐入效果——用户往下翻的时候内容会平滑地出现，不会那么突兀。按钮加了悬停变色反馈——鼠标放上去会有轻微变化，用户知道这个可以点。"

优先 CSS 实现，不够用 Framer Motion。尊重 `prefers-reduced-motion`（有些用户不喜欢动效，系统设置里关了就不会显示）。
