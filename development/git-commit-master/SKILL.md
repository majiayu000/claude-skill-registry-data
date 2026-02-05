---
name: git-commit-master
description: 按照 Conventional Commits 规范执行高质量的 git 提交，处理暂存、消息生成及钩子修复。
---

## 核心逻辑

1. **分析变更**: 必须运行 `git diff --cached` 分析已暂存内容。若无暂存，先询问用户是否全选。
2. **规范化消息**: 严格执行 `<type>(<scope>): <subject>` 格式。
   - `feat`: 新功能
   - `fix`: 修补 bug
   - `docs`: 文档变更
   - `refactor`: 重构
   - `chore`: 其他更改
3. **需要用户检查**:
   - 执行前询问用户确认变更。

## 使用场景

- 用户输入 "commit", "提交", "保存更改"。
- 完成一个独立的功能模块后建议使用。
