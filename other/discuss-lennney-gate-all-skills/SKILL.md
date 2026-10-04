---
name: gate-discuss
description: "需求探讨 / Discovery discussion. Asks 3 questions to clarify project scope. Use when the user wants to build a new site but isn't sure what they need."
disable-model-invocation: true
trigger: 用户想搭建新网站，但不确定具体需求
input: 用户的模糊想法
output: 明确的需求文档
next: gate-init
dependencies: 无
---

用户不知道要做什么。问 3 个问题，一次一个：

1. **这个网站是给谁看的？** — 用户群体？他们来找什么？
2. **核心功能是什么？** — 最少要有什么才能上线？
3. **内容准备好了吗？** — 文案、图片、Logo 有没有？

问题问完，你总结成一句话需求。然后问用户：开始搭？

> 用户说好 → `/gate-init`（你在后台把项目建好）
