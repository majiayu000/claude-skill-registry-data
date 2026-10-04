---
name: gate-a11y
description: "无障碍优化 / Accessibility optimization. Fixes WCAG issues, ARIA, semantic HTML, and keyboard navigation. Use when the user wants to improve accessibility."
trigger: 需要提升网站可访问性
input: 可访问性审计报告
output: 可访问性优化方案
next: 无
dependencies: gate-optimize
---

检查并修复：

1. **键盘能用吗？** — Tab 挨个走一遍，所有按钮都能用键盘操作
2. **屏幕阅读器能读吗？** — 图片有文字说明，表单有标签
3. **颜色看得清吗？** — 文字和背景对比度够不够
4. **焦点对吗？** — 弹窗打开时焦点锁定在里面，关掉时回到原来位置

修完后告诉用户：
"做了无障碍优化。现在用键盘 Tab 键可以浏览整个网站，屏幕阅读器能正确读出内容，颜色对比度也调整了——视力不好的用户也能看清。"
