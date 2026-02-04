---
name: fractal-docs
description: |
  Automatically add or update documentation following the Fractal Docs Protocol.
  自动添加或更新符合分形文档协议的文档。

  Use when:
  - Creating new source files (add [IN]/[OUT]/[POS] headers)
  - Creating new folders (add .folder.md)
  - Modifying existing files (update headers and .folder.md)
  - Running documentation audit
  - User mentions "fractal", "doc protocol", "add headers", "补全文档"
---

# Fractal Docs Protocol Skill / 分形文档协议技能

> **设计思路 / Design Notes**:
> 1. `description` 明确列出功能和触发词（fractal, doc protocol, 补全文档等）
> 2. 提供完整模板，减少 Claude 的猜测
> 3. 分步骤指令，确保执行顺序正确

## Overview / 概述

This skill helps maintain the Fractal Docs Protocol - a self-describing documentation system.
此技能帮助维护分形文档协议 - 一个自描述的文档系统。

## Instructions / 指令

### When Creating/Modifying Source Files / 创建或修改源文件时

1. **Check if file has header / 检查文件是否有头注释**
2. **Add or update the 3-line header / 添加或更新 3 行头注释**:

```typescript
// [IN]: <dependencies> / <依赖说明>
// [OUT]: <exports> / <导出说明>
// [POS]: <position in system> / <系统定位>
// Protocol: When updating me, sync this header + parent folder's .folder.md
// 协议：更新本文件时，同步更新此头注释及所属文件夹的 .folder.md
```

3. **Update parent folder's .folder.md / 更新父文件夹的 .folder.md**

### When Creating Folders / 创建文件夹时

Create `.folder.md` with this template / 使用此模板创建 `.folder.md`：

```markdown
# Folder: <path>

> Trigger: When this folder's structure/responsibilities/file list changes, update this document.
> 触发条件：当本文件夹的结构/职责/文件列表变化时，更新此文档。

<Line 1: Responsibility / 职责>
<Line 2: Boundary / 边界>
<Line 3: Key invariant / 关键不变量>

## Files
- `<file>`: <position> - <description EN> / <description CN>
```

### Header Content Guidelines / 头注释内容指南

| Tag | Content | Example |
|-----|---------|---------|
| `[IN]` | Dependencies, imports | `@repo/db, ../orpc / 依赖数据库和 oRPC` |
| `[OUT]` | Exports, side effects | `postRouter object / 导出文章路由` |
| `[POS]` | Layer, responsibility | `API layer - Post handlers / API 层 - 文章处理器` |

### Validation / 验证

After completing changes, run:
```bash
pnpm doc-lint
```

## Reference / 参考

- Full protocol: [docs/protocols_fractal-docs.md](../../docs/protocols_fractal-docs.md)
- Lint guide: [docs/doc-lint-guide.md](../../docs/doc-lint-guide.md)
