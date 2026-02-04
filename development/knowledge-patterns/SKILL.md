---
name: knowledge-patterns
description: PR Review 修复模式库。在处理 PR Review 评论时自动查阅，寻找已知问题模式和解决方案。
---

# PR Review 知识模式库

当处理 PR Review 评论时，先查阅此模式库寻找已知解决方案，避免重复分析相同问题。

## 使用场景

1. **comment-classifier agent**：分类评论时，匹配已知模式提高置信度
2. **fix-coordinator agent**：修复前查阅推荐方案
3. **人类开发者**：学习常见问题和最佳修复实践

## 快速索引

<!-- INDEX_START -->
| 模式 ID | 标题 | 技术栈 | 严重度 | 实例数 | 标签 |
|---------|------|--------|--------|--------|------|
| _example-silent-error-handling | [示例] 错误处理静默失败 | backend | P1 | 1 | error-handling, try-catch, silent-failure, example |
<!-- INDEX_END -->

> 带 `_example-` 前缀的是示例模式，展示格式规范。实际模式由 `knowledge-writer` agent 在 fix-pr-review 流程中自动沉淀。

## 按技术栈分类

### Backend

<!-- BACKEND_START -->
- [_example-silent-error-handling](patterns/_example-silent-error-handling.md) - [示例] 错误处理静默失败
<!-- BACKEND_END -->

### Frontend

<!-- FRONTEND_START -->
_暂无模式_
<!-- FRONTEND_END -->

### E2E

<!-- E2E_START -->
_暂无模式_
<!-- E2E_END -->

## 模式文件格式

每个模式文件位于 `patterns/` 目录，包含：

```yaml
---
id: pattern-id           # 唯一标识符
title: 模式标题          # 人类可读标题
tags: [tag1, tag2]       # 用于相似度匹配的标签
stack: backend           # 技术栈: backend/frontend/e2e
severity: P0             # 严重度: P0/P1/P2/P3
created: 2025-12-01      # 创建日期
updated: 2025-12-01      # 最后更新日期
instances: 1             # 实例数量
---
```

## 如何查阅

### AI Agent 查阅

1. 读取此 SKILL.md 获取索引
2. 根据评论关键词和技术栈筛选候选模式
3. 读取候选模式文件获取详细信息
4. 参考"推荐修复"部分制定方案

### 人类开发者查阅

1. 浏览上方索引表找到相关模式
2. 点击链接查看模式详情
3. 参考"实例记录"了解历史修复

## 知识沉淀触发条件

以下修复会自动沉淀到此库：

- **优先级**：P0 或 P1
- **置信度**：≥ 85%
- **状态**：修复成功

沉淀由 `knowledge-writer` agent 执行，支持智能合并：
- 相似度 ≥ 70：追加到现有模式
- 相似度 40-69：询问用户
- 相似度 < 40：创建新模式
