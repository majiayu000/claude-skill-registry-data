---
name: gate-optimize
description: "网站优化 / Site optimization. Routes users to perf, a11y, or animation optimization. Use when the site is live and the user wants to improve it."
trigger: 网站已上线，需要优化
input: 已部署的网站
output: 优化建议
next: gate-perf / gate-a11y / gate-animate
dependencies: gate-seo
---

问："想让网站变得更好？选一个方向："

**速度慢？** → `/gate-perf`
"网站加载速度影响用户体验和搜索引擎排名。我帮你检查哪里慢了然后优化。"

**所有人能无障碍用？** → `/gate-a11y`
"让视力不好、只能用键盘的用户也能顺畅使用你的网站。"

**加自动化测试？** → `/gate-testcov`
"写一些自动测试，以后改代码的时候不怕改坏东西。"

**自动部署？** → `/gate-ci`
"每次你推送代码，网站自动更新上线，不用手动操作。"

**加动效？** → `/gate-animate`
"让网站用起来更流畅、更好看。"
