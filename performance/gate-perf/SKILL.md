---
name: gate-perf
description: "性能优化 / Performance optimization. Optimizes site speed, Core Web Vitals, and load times. Use when the site is slow or the user wants to speed things up."
trigger: 网站加载速度慢
input: 性能数据
output: 性能优化方案
next: 无
dependencies: gate-optimize
---

直接做：

1. 跑 Lighthouse 记下分数
2. 检查哪些拖慢了速度：大图片？太多代码？字体加载慢？
3. 优化：图片压缩、按需加载、字体预加载
4. 再跑一次 Lighthouse

告诉用户：
"优化完了。之前首页加载需要 X 秒，现在只要 Y 秒。主要做了三件事：图片压缩了但不影响画质、不着急的代码等需要时才加载、字体提前准备好。Lighthouse 分数从 X 提到了 Y。"
