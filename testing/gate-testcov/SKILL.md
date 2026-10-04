---
name: gate-testcov
description: "测试覆盖 / Test coverage. Adds tests for core functionality. Use when the user wants to add test coverage to their project."
trigger: 需要添加测试覆盖
input: 项目代码
output: 测试代码
next: 无
dependencies: 无
---

分析网站核心路径：首页 → 导航到各个页面 → 关键操作。

写 E2E 测试覆盖这些路径，跑通。

告诉用户：
"写了 X 个自动化测试，覆盖了首页加载、菜单导航、表单提交这些核心功能。以后改代码的时候跑一下测试，就知道有没有改坏东西——相当于有个机器人在帮你做回归检查。"
