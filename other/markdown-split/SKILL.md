---
name: markdown-split
description: Intelligently split a large Markdown document into multiple files based on heading level. Automatically detects the optimal split level or allows manual specification. Use this skill when you need to break down a large document into smaller, organized files.
---

# Markdown Split Skill

智能拆分大型 Markdown 文档。自动分析文档结构，选择最佳拆分级别。

## 使用方法

```bash
python3 .codebuddy/skills/markdown-split/scripts/split_markdown.py <input_file> [options]
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `input_file` | 是 | 输入的 Markdown 文件路径 |
| `--output-dir`, `-o` | 否 | 输出目录，默认为输入文件所在目录下的 `split_output/` |
| `--level`, `-l` | 否 | 拆分的标题级别 (1-6)，不指定则自动检测 |
| `--prefix`, `-p` | 否 | 输出文件名前缀，默认为空 |
| `--no-index` | 否 | 不生成索引文件 |

## 示例

```bash
# 自动检测拆分级别（推荐）
python3 scripts/split_markdown.py docs/features.md --output-dir docs/design

# 手动指定按二级标题拆分
python3 scripts/split_markdown.py docs/features.md --level 2 -o docs/design

# 按三级标题拆分
python3 scripts/split_markdown.py docs/guide.md -l 3

# 添加文件名前缀
python3 scripts/split_markdown.py docs/guide.md -o ./chapters -p "chapter_"
```

## 智能检测逻辑

脚本会自动分析文档的标题结构，按以下策略选择拆分级别：

1. 统计各级标题数量 (H1-H6)
2. 选择数量在 2-15 之间的最高级别标题
3. 如果最高级别只有 1 个，自动选择下一级别

例如，对于以下文档：
```markdown
# 游戏设计文档        ← H1: 1 个（作为文档标题，不适合拆分）
### 1. 游戏概述       ← H3: 5 个（自动选择此级别拆分）
### 2. 核心机制
### 3. 游戏对象
...
```

输出：
```
文档标题结构分析:
  H1 (#): 1 个
  H3 (###): 5 个
自动检测拆分级别: H3 (###)
找到 5 个章节
```

## 输出说明

假设输入文件包含以下结构（H3 作为主要章节）：

```markdown
# 游戏设计文档

### 1. 游戏概述
内容...

### 2. 核心机制
内容...

### 3. 游戏对象
内容...
```

将生成以下文件：

```
docs/design/
├── index.md              # 索引文件
├── 00_前言.md            # H3 标题前的内容
├── 01_1_游戏概述.md
├── 02_2_核心机制.md
└── 03_3_游戏对象.md
```

## 特性

- **智能检测**：自动分析文档结构，选择最佳拆分级别
- **手动覆盖**：支持 `--level` 参数手动指定拆分级别
- **代码块保护**：正确处理代码块中的 `#` 符号
- **自动序号**：文件名自动添加序号
- **索引生成**：自动生成目录索引文件
