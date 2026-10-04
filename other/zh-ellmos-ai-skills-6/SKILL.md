---
name: migrate-rename
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: 使用包装文件进行渐进式文件重命名。无缝重命名，防止硬性中断 — 引用会在日常使用中有机地自动更新。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [migration, renaming, wrapper, evolutionary, refactoring]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/migrate-rename.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="migrate-rename banner">

> **中文** — `migrate-rename` 官方中文版本。


# 使用包装器重命名文件（渐进式迁移）(中文)

> 支持在没有硬中断的情况下重命名文件。引用会在日常使用中自动且有机地得到更新。

---

## 原理：渐进式迁移

```
BEFORE:                          AFTER:
old_file.md                      new_file.md (renamed)
   |                                |
   +-- Reference A                  +-- old_file.md (wrapper)
   +-- Reference B                         |
   +-- Reference C                         +-- Log table
                                           +-- Instructions
                                           +-- Link to new_file.md
```

当有人访问旧路径时：
1. 到达包装器文件
2. 在日志中添加一条记录
3. 修正引导其访问该位置的引用
4. 转到实际文件

---

## 分步指南

### 1. 重命名文件

```bash
mv old_file.md new_file.md
```

### 2. 创建包装器文件

创建包含以下内容的 `old_file.md`：

```markdown
# OLD_FILE.md - REDIRECTED (Deutsch)

**Status:** This file has been renamed to `new_file.md`

---

## Migration Log

| Date | Who | Origin | Reference corrected? |
|------|-----|--------|---------------------|
| YYYY-MM-DD | [Name] | Initial migration | n/a (wrapper created) |

---

## Instructions

1. **Leave a log entry** (in table above)
2. **Check origin**: What sent you here?
3. **Correct reference**: Change `old_file.md` -> `new_file.md`
4. **Go to the actual file**: `new_file.md`

---

**Target file:** `new_file.md`
```

### 3. 立即修正关键引用
- 帮助文件（主要文档）
- 系统提示词中的引用
- 直接使用该路径的 CLI 代码

### 4. 渐进式迁移其余引用
其余部分会在使用过程中自动完成修正。

---

## 何时使用包装器方法？

**是 - 包装器适用情况：**
- 存在许多潜在的引用
- 文件被多个合作伙伴/工具所引用
- 不是关键的系统文件

**否 - 直接全部修改：**
- 仅有少数已知的引用
- 关键系统文件（配置、数据库模式）
- 性能关键路径

---

## 清理

在约 30 天后，或当日志中不再增加新条目时：
1. 将包装器文件移动至 `_archive/deprecated/`
2. 或者完全删除（若不再产生条目）

---

## 变更日志

### 1.0.0 (2026-03-15)
- 从 BACH v3.8.0 移植

---

*从 BACH v3.8.0 移植 | 独立版本*
