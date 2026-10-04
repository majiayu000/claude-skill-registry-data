---
name: obsidian
description: Read, search, and create notes in the Obsidian vault. 支持 Hermes-Wiki 知识库工作流。
triggers:
  - "obsidian"
  - "知识库"
  - "笔记"
  - "创建概念"
  - "创建 MOC"
---

# Obsidian Vault

**Location:** 
- Set via `OBSIDIAN_VAULT_PATH` environment variable
- Or use `WIKI_PATH` for Hermes-Wiki (defaults to `~/Hermes-Wiki`)

## Hermes-Wiki 配置

```bash
# 环境变量
export WIKI_PATH="$HOME/Hermes-Wiki"  # 默认位置
export OBSIDIAN_VAULT_PATH="$HOME/Hermes-Wiki"  # Obsidian vault
```

### 目录结构

```
Hermes-Wiki/
├── SCHEMA.md          # 规范文档
├── index.md           # 首页
├── log.md             # 更新日志
├── raw/               # 原始资料
│   ├── articles/      # 文章
│   ├── papers/        # 论文
│   ├── transcripts/   # 文字稿
│   └── assets/        # 资源
├── concepts/          # 概念页面 (lowercase-with-hyphens.md)
├── entities/          # 实体页面 (Entity-Name.md)
├── comparisons/       # 对比分析
├── queries/           # 问答
├── moc/               # 主题地图 (moc-topic-name.md)
└── drafts/            # 草稿
```

## Read a note

```bash
WIKI="${WIKI_PATH:-$HOME/Hermes-Wiki}"
cat "$WIKI/Note Name.md"
```

## List notes

```bash
WIKI="${WIKI_PATH:-$HOME/Hermes-Wiki}"

# 所有笔记
find "$WIKI" -name "*.md" -type f

# 指定目录
ls "$WIKI/concepts/"
ls "$WIKI/moc/"
```

## Search

```bash
WIKI="${WIKI_PATH:-$HOME/Hermes-Wiki}"

# 按文件名
find "$WIKI" -name "*.md" -iname "*keyword*"

# 按内容
grep -rli "keyword" "$WIKI" --include="*.md"
```

## Create a note

### 概念页面 (concepts/)

```bash
WIKI="${WIKI_PATH:-$HOME/Hermes-Wiki}"

cat > "$WIKI/concepts/concept-name.md" << 'EOF'
---
tags:
  - concept
created: 2026-05-05
---

# Concept Name

## 定义

概念的定义。

## 核心要点

- 要点1
- 要点2

## 相关概念

- [[other-concept]]
- [[moc-topic-name]]

## 相关实体

- [[Entity-Name]]
EOF
```

### 实体页面 (entities/)

```bash
WIKI="${WIKI_PATH:-$HOME/Hermes-Wiki}"

cat > "$WIKI/entities/Entity-Name.md" << 'EOF'
---
tags:
  - entity
  - software
created: 2026-05-05
---

# Entity Name

## 简介

实体的简要介绍。

## 核心特性

1. 特性1
2. 特性2

## 使用场景

- 场景1
- 场景2

## 相关

- [[concept-name]]
EOF
```

### MOC 页面 (moc/)

```bash
WIKI="${WIKI_PATH:-$HOME/Hermes-Wiki}"

cat > "$WIKI/moc/moc-topic-name.md" << 'EOF'
---
tags:
  - moc
created: 2026-05-05
---

# Topic Name MOC

## 概述

本 MOC 整理 Topic 相关内容。

## 核心概念

- [[concept-1]]
- [[concept-2]]

## 详细笔记

### 概念

- [[concept-a]]
- [[concept-b]]

### 实体

- [[Entity-X]]
- [[Entity-Y]]

## 外部资源

- [链接](url)
EOF
```

## Append to a note

```bash
WIKI="${WIKI_PATH:-$HOME/Hermes-Wiki}"
echo "
New content here." >> "$WIKI/Existing Note.md"
```

## Wikilinks

Obsidian 使用 `[[Note Name]]` 语法创建双向链接。

- 链接到概念：`[[concept-name]]`
- 链接到实体：`[[Entity-Name]]`
- 链接到 MOC：`[[moc-topic-name]]`

## Hermes 工作流

```
1. 放入文章 → raw/articles/
2. Hermes 读取 raw/
3. 自动生成 → concepts/, entities/, moc/
4. Obsidian 打开 → 查看双链网络
```

## 同步到 GitHub

```bash
WIKI="${WIKI_PATH:-$HOME/Hermes-Wiki}"
cd "$WIKI"
git add .
git commit -m "update: 描述"
git push
```
