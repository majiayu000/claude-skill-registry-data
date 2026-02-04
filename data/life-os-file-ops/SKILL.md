---
name: life-os-file-ops
description: life-os/ 目录的文件读写规范。处理 Markdown 笔记、YAML frontmatter、wiki-links、模板变量。当需要在 life-os/ 目录中创建、编辑、查找笔记时使用此技能。
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Life OS 文件操作

适用范围：`life-os/` 目录

## 目录结构

```
life-os/
├── CLAUDE.md           # Vault 上下文（首先读取）
├── Daily Notes/        # YYYY-MM-DD.md 格式
├── Goals/              # 目标级联文件
├── Projects/           # 项目文件夹
├── Templates/          # 可复用模板
├── Inbox/              # GTD 待处理区
└── Archives/           # 已完成/归档
```

## 文件操作

### 读取
1. 先读取 `life-os/CLAUDE.md` 获取上下文
2. 使用 Glob 查找：`life-os/**/*.md`
3. 检查 wiki-links 找到相关笔记

### 创建
1. 检查笔记是否已存在
2. 使用模板（`life-os/Templates/`）
3. 添加 YAML frontmatter
4. 插入相关 wiki-links

### 编辑
- 保留 YAML frontmatter 结构
- 维护现有 wiki-links
- 使用一致的标题层级

## Wiki-Link 格式

```markdown
[[Note Name]]                    # 链接到笔记
[[Note Name|显示文本]]            # 带别名
[[Note Name#Section]]            # 链接到章节
[[Folder/Note Name]]             # 带路径
```

## YAML Frontmatter

```yaml
---
date: 2024-01-15
tags: [tag1, tag2]
status: active
---
```

## 模板变量

替换规则：
- `{{date}}` → 今天（YYYY-MM-DD）
- `{{date-1}}` → 昨天
- `{{date+1}}` → 明天
- `{{time}}` → 当前时间

## 标签规范

- 优先级：`#priority/high`, `#priority/medium`, `#priority/low`
- 状态：`#active`, `#waiting`, `#completed`, `#archived`
- 场景：`#work`, `#personal`, `#health`, `#learning`

## 相关规范

→ `docs/references/life-os/markdown-standards.md`
→ `docs/references/life-os/productivity-workflow.md`
→ `docs/references/life-os/project-management.md`
