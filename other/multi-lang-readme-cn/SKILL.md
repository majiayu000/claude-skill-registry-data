---
name: multi-lang-readme-cn
description: 当用户需要基于现有 README 创建中英或多语言 README，并保持 Markdown 结构时使用。
---

# Multi-Lang README（中文）

## Overview

将现有 README 翻译为多语言版本，并保持 Markdown 结构、链接、代码块和语言切换导航稳定。流程支持中英双语和多语言 README 集合，不处理与 README 无关的通用文档改写。

## 何时使用

当用户提出以下需求时使用：
- 创建双语 README（如中英）
- 创建多语言 README
- 将现有 README 翻译为指定语言
- 统一 README 的语言切换链接

## 不要使用

以下场景不应使用本技能：
- 翻译非 README 的通用文档
- 与 README 无关的内容创作任务
- 法律/合同等高风险文档翻译

## 使用说明

1. 定位要翻译的 README 源文件（有歧义时先问用户）。
2. 确认目标语言与主 README 语言策略。
3. 在保留 Markdown 结构前提下完成翻译。
4. 按语言后缀规范写入目标文件。
5. 在各语言 README 顶部补齐语言切换链接。
6. 交付前检查路径、链接和格式一致性。

## 支持语言

| 代码 | 语言 |
|------|------|
| en | English |
| de | German |
| ja | Japanese |
| ko | Korean |
| zh-CN | Chinese |

## 工作流程

### 第一步：定位 README

查找待翻译 README：
- 默认先检查根目录 `README.md`
- 如果存在多个 README，先让用户指定目标文件

### 第二步：读取内容

读取完整内容，包括：
- 标题与徽章
- 各章节（Features、Installation、Usage、Contributing、License 等）
- 代码块
- 链接

### 第三步：确认目标语言

询问用户目标语言。默认策略：
- `README.md` 作为英文主版本
- 如果当前主 README 非英文，先转为英文主版本
- 再按需求生成其他语言版本

若用户只说“做双语 README”但未指定语言，默认：
- 先生成英文 `README.md`
- 再生成中文 `README.zh-CN.md`

### 第四步：执行翻译

翻译要求：
- 保留 Markdown 结构
- 代码块不翻译
- 标题与正文翻译为目标语言
- 相对链接路径保持不变
- 外链锚文本可按目标语言优化

### 第五步：写入目标文件

推荐命名：
- 英文：`README.md`
- 德语：`README.de.md`
- 日语：`README.ja.md`
- 韩语：`README.ko.md`
- 中文：`README.zh-CN.md`

### 第六步：补充语言切换

在 README 顶部（标题或徽章后）加入语言切换，例如：

```markdown
**English** | [中文](README.zh-CN.md) | [Deutsch](README.de.md) | [日本語](README.ja.md) | [한국어](README.ko.md)
```

### 第七步：更新互链

在翻译文件中增加返回主文档或多语言互链，避免孤立文档。

## 触发示例

- “帮我创建中英 README”
- “帮我创建多语言 README”
- “把 README 翻译成日语”
- “新增 README.zh-CN.md”
- “create bilingual README”
