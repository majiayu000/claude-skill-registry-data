---
name: gate-ai
description: "AI 辅助路由。问用户在做什么，路由到对应的 ai-* 技能。Use when the user says '帮我写代码', '帮我审查代码', '帮我写测试', '帮我调试', '帮我重构', '帮我做 git 操作', or any general AI assistance request."
trigger: 需要 AI 辅助
input: 用户需求
output: AI 辅助结果
next: ai-coding-workflow / ai-code-review / ai-testing / ai-debugging / ai-refactoring / ai-git-workflow
dependencies: 无
---

问用户在做什么，然后路由：

- **写代码** → `ai-coding-workflow`
- **审查代码** → `ai-code-review`
- **写测试** → `ai-testing`
- **调试** → `ai-debugging`
- **重构** → `ai-refactoring`
- **Git 操作** → `ai-git-workflow`
