---
name: topic-bookmarks-reorganizer-cn
description: 当用户需要按主题整理浏览器书签导出、URL 去重并生成可导入 HTML 时使用。
license: MIT
---

# Topic Bookmarks Reorganizer（中文）

## Overview

把浏览器书签导出文件中的用户指定主题目录重整为更清晰、可导入的新 Netscape HTML 文件。流程会分析源文件、提取目标主题目录、重新归类链接和子目录、按 URL 去重，并保持输出可直接导入浏览器。

## 何时使用

当用户有以下需求时使用本技能：
- 分析一个书签导出 HTML，并定位用户指定的主题目录
- 重新分门别类该目录下的链接与子目录
- 按 URL 去重
- 输出只包含该主题目录的可导入 HTML

## 不要使用

以下场景不应使用本技能：
- 输入不是浏览器书签导出 HTML
- 用户仅需要文字建议，不需要处理文件
- 用户需求与书签整理无关（如纯 JSON/PDF/Docx 处理）

## 使用说明

1. 先向用户确认必要参数：
- 输入书签文件路径
- 主题目录名称
- 输出文件路径

2. 先跑分析与预览：

```bash
python3 scripts/reorganize_topic_bookmarks.py \
  --input /path/to/bookmarks.html \
  --output /tmp/topic-preview.html \
  --topic-folder "<topic-folder-name>" \
  --mode auto \
  --lang zh \
  --report /tmp/topic-report.json \
  --print-report
```

3. 视情况调整参数：
- `--mode auto`：自动选择分类策略
- `--mode generic`：使用通用分类策略
- `--no-dedupe-url`：不做 URL 去重

4. 生成最终文件：

```bash
python3 scripts/reorganize_topic_bookmarks.py \
  --input /path/to/bookmarks.html \
  --output /path/to/topic-bookmarks-reorganized.html \
  --topic-folder "<topic-folder-name>" \
  --mode auto \
  --lang zh
```

5. 交付前检查并汇报：
- 确认输出文件存在
- 汇总输入链接数、输出链接数、去重移除数
- 确认输出仅包含一个顶层目录（目标主题目录）

## 输出要求

- 输出必须是 Netscape 书签格式，可直接导入浏览器
- 输出仅保留目标主题目录
- 尽量保留原 `<A ...>` 属性（如 add-date/icon）
- 目录结构按高层分类重组，便于后续维护
