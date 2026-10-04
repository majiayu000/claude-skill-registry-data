---
name: rss-ingest
description: "RSS 订阅与文档编译系统 - 从 RSS 源获取文章并自动整理到本地知识库。包含 RSS 订阅器和文档编译助手两个功能。Triggers: 'RSS feed', 'subscribe to blog', 'save RSS articles', 'OPML file', 'fetch latest articles', '文档编译', 'LLM wiki'"
---

# RSS 订阅与文档编译系统

## 功能概述

本系统包含两个核心组件：

1. **RSS 订阅器**：从 RSS 源获取文章并保存到本地文件夹
2. **文档编译助手**：将原始文档整理成结构化的知识库

---

## 组件 1: RSS 订阅器

### 何时使用此技能

**务必使用此技能当：**
- 用户要求从 RSS 订阅源获取最新内容
- 用户想要保存 RSS 文章到本地文件夹
- 用户提到 RSS 订阅、博客订阅、内容获取
- 用户想要按日期和标题整理 RSS 文章
- 用户提供一个 OPML 文件包含多个订阅源

**不要使用此技能当：**
- 用户只需要查看单个 URL 的内容（直接用 WebFetch）
- 用户想要获取非 RSS 格式的内容

### 使用方法

#### 基本用法 - 单个 RSS URL

```bash
python scripts/rss_subscriber.py "https://example.com/feed.rss"
```

#### 指定输出目录

```bash
python scripts/rss_subscriber.py "https://example.com/feed.rss" --output "./my_folder"
```

#### 使用 OPML 文件批量订阅

```bash
python scripts/rss_subscriber.py --opml "path/to/subscriptions.opml"
```

支持以下两种文件路径格式：
- 本地文件路径：`./my-feeds.opml` 或 `C:/Users/.../feeds.opml`
- URL 地址：`https://example.com/feeds.opml`

#### 使用默认订阅源

如果不提供任何参数，将自动使用技能目录下的默认 `feeds.opml` 文件，并将文章保存到**当前工作目录**的 `raw/` 文件夹：

```bash
python scripts/rss_subscriber.py
```

**注意**：输出目录取决于你**执行命令时所在的目录**。例如：

```bash
# 在 doc-writing-as-code 项目目录下执行
cd C:/Users/1/github/doc-writing-as-code
python /c/Users/1/github/skills/skills/rss-ingest/scripts/rss_subscriber.py --opml /c/Users/1/.claude/skills/rss-ingest/feeds.opml
# 文章将保存到：C:/Users/1/github/doc-writing-as-code/raw/
```

#### 避免在脚本目录生成配置目录

执行命令时，建议先 `cd` 到目标项目目录，这样可以避免在技能脚本目录下生成 `.claude` 配置目录和 `settings.local.json` 文件。

#### 日期过滤选项

**默认行为（只获取最近 1 年的文章）：**

```bash
python scripts/rss_subscriber.py --opml "feeds.opml"
```

这会过滤掉 1 年前的旧文章，专注于最新内容。

**获取所有历史文章：**

使用 `--get-all` 选项获取 RSS 源中的所有文章，包括 1 年前的：

```bash
python scripts/rss_subscriber.py --opml "feeds.opml" --get-all
```

### 输出格式

文章将保存为以下格式的 Markdown 文件：

```
raw/2025-01-06_Article-Title.md
```

每个文件包含：
- 文章标题
- 来源（RSS 域名）
- 发布日期
- 原文链接
- 摘要
- 正文内容

### 文件命名规则

- 格式：`YYYY-MM-DD_文章标题.md`
- 自动清理文件名中的非法字符
- 如果文件已存在，跳过保存

### 支持的格式

#### RSS 格式
- RSS 2.0
- RSS 1.0
- Atom 1.0

#### OPML 格式

支持标准的 OPML 1.0/2.0 格式，示例：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
  <body>
    <outline text="Tech Blogs" title="Tech Blogs">
      <outline type="rss" text="Martin Fowler" xmlUrl="https://martinfowler.com/feed.atom"/>
      <outline type="rss" text="Dev Blog" xmlUrl="https://devblog.com/feed.rss"/>
    </outline>
  </body>
</opml>
```

---

## 组件 2: 文档编译助手

### 角色

你是一个文档编译助手，负责将分散在 `raw/` 目录中的原始文档和摘录，整理成结构化的知识库。

### 目录结构

```
doc-writing-as-code/
├── raw/                    # 原始文档（只读，不要修改）
│   ├── 2026-03-10_The_First_Cohort.md
│   └── ...
├── wiki/                   # 编译后的知识库（可写）
│   ├── summaries/          # 每篇原始文档的总结
│   │   └── 2026-03-10_The First Cohort_summary.md
│   ├── concepts/           # 概念文章（提取自多篇文章）
│   │   ├── 职业教练.md
│   │   └── ...
│   ├── index.md            # 知识库总索引
│   └── log.md              # 操作日志（追加写入）
```

### 工作流程

#### 1. 扫描新文件（防重复处理）

当检测到 `raw/` 中有新的 `.md` 文件时，执行以下**三层去重检查**：

**方案 1：检查处理记录（快速）**

```bash
grep -q "^文件名.md$" wiki/.processed_files
```
- 如果已存在记录 → **跳过**

**方案 2：检查 summary 文件（双重确认）**

```bash
[ -f "wiki/summaries/文件名_summary.md" ]
```
- 如果 summary 已存在 → **跳过**（同时补充到处理记录）

**方案 3：通过脚本自动化检查**

```bash
python /c/Users/1/github/skills/skills/rss-ingest/scripts/process_raw_files.py
```

**重要**：脚本使用当前工作目录（`os.getcwd()`）作为项目根目录，因此**必须在项目目录下执行**：

```bash
cd C:/Users/1/github/doc-writing-as-code
python /c/Users/1/github/skills/skills/rss-ingest/scripts/process_raw_files.py
```

- 脚本会列出所有需要处理的新文件
- 自动跳过已处理的文件

#### 2. 生成总结文件

为每个新文件创建 `wiki/summaries/` 下的总结：

**文件名格式**：`YYYY-MM-DD_标题_summary.md`

**内容结构**：

```markdown
# [原标题]

**来源**: [来源名称]
**发布日期**: [日期]
**链接**: [URL]

---

## 核心观点

[2-4 个要点，每个要点用粗体概括，后跟 1-2 句解释]

---

## 关键概念

[提取 3-6 个关键概念，与概念文章链接关联]

---

## 引用金句

- "[引用 1]"
- "[引用 2]"

---

*汇总于 YYYY-MM-DD*
```

#### 3. 提取并创建概念文章

从文章中提取**可复用的概念**，创建或更新 `wiki/concepts/` 下的概念文章：

**命名规则**：
- 名词化，使用中文（如 `职业教练.md`）
- 避免动词短语（如 `如何做 X` → `X 的方法.md`）

**内容结构**：

```markdown
# [概念名称]

## 定义

[简洁的定义，1-2 段]

## 核心要素

- 要素 1
- 要素 2
- 要素 3

## 应用场景

[在什么情况下使用这个概念]

## 相关概念

- [[关联概念 1]]
- [[关联概念 2]]

## 参考资料

- [[2026-03-10_The First Cohort#DRI Your Career 课程]]
- [[其他相关文档]]

*概念由 [[2026-03-10_The First Cohort_summary]] 首次提出*
```

#### 4. 维护索引文件

**`wiki/index.md`（总索引）**：

```markdown
# 文档知识库

## 最新汇总

[[2026-03-10_The First Cohort_summary]] (2026-04-04)

## 概念库

- [[职业教练]]
- [[职业清晰度]]
- [[异步学习]]
```

---

## 注意事项

1. **不修改原始文件**：`raw/` 目录只做读取，所有整理工作写入 `wiki/`
2. **保持链接一致**：使用 Obsidian 原生链接语法 `[[文件路径]]`
3. **概念去重**：同名概念只创建一次，后续文章引用
4. **链接验证**：确保所有 `[[xxx]]` 链接的文件实际存在
5. **日期格式**：统一使用 `YYYY-MM-DD`
6. **防重复处理**：
   - 每次处理前先在项目目录下运行 `python /c/Users/1/github/skills/skills/rss-ingest/scripts/process_raw_files.py` 检查
   - 处理完成后，文件名会自动记录到 `wiki/.processed_files`
   - **说明**：`.processed_files` 中的记录会阻止脚本重复生成 summary
     - 如果只删除了 summary 文件（记录还在），脚本会跳过不会重新生成
     - 如果需要重新生成某个 summary，应同时从 `.processed_files` 中删除对应记录

---

## 依赖

- Python 3.6+
- 无外部依赖（使用标准库）

## 默认的 feeds.opml 文件

技能目录下包含一个默认的 `feeds.opml` 文件，不传任何参数时会自动使用。你可以在该文件中添加你的默认订阅源。

---

## 集成脚本

技能包含以下辅助脚本，用于文档编译工作流：

### `process_raw_files.py` - 检查新文件

检查 `raw/` 目录中的新文件并防止重复处理：

**注意**：此脚本使用**当前工作目录**作为项目根目录，因此必须在项目目录下执行：

```bash
cd C:/Users/1/github/doc-writing-as-code
python /c/Users/1/github/skills/skills/rss-ingest/scripts/process_raw_files.py
```

**功能：**
- 扫描 `raw/*.md` 文件
- 通过三层去重检查避免重复处理
- 列出需要处理的新文件
- 自动跟踪已处理的文件到 `.processed_files`

### `update_index.py` - 更新索引

更新 `wiki/index.md` 文件，添加新的 summary 链接：

**注意**：此脚本使用**当前工作目录**作为项目根目录，因此必须在项目目录下执行：

```bash
cd C:/Users/1/github/doc-writing-as-code
python /c/Users/1/github/skills/skills/rss-ingest/scripts/update_index.py
```

**功能：**
- 扫描 `wiki/summaries/` 目录
- 提取最新的 10 个 summary 文件
- 自动更新索引中的"最新汇总"部分
