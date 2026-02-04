---
name: markdown-segment-translator
description: 长文档Markdown分段翻译技能（Agent自己翻译）
allowed-tools: ["Bash", "Read", "Write"]
triggers:
  - type: keyword
    keywords:
      - "分段翻译"
      - "markdown翻译"
      - "接力翻译"
      - "长文档翻译"
      - "完整翻译"
      - "段落翻译"
      - "分段处理翻译"
      - "逐段翻译"
      - "论文翻译"
---

# Markdown分段翻译技能

## ⚠️ 强制执行要求 - 3步翻译流程 ⚠️

当用户要求翻译markdown文件时，你**必须严格按照以下3个步骤**完成，不要跳过任何步骤！

---

## 📋 第1步: 文档分段

**工具**: `Bash`  
**命令格式**:
```bash
python3 workspace/skills/markdown-segment-translator/scripts/segment_tool.py segment --input [输入文件] --segment-size 1000 --max-segments 3
```

**作用**:
- 将大文档分成多个小段落
- 段落文件保存在 `output/segments/segment_1.md`, `segment_2.md`...
- 元数据保存在 `output/metadata/segments_info.json`

**示例**:
```bash
python3 workspace/skills/markdown-segment-translator/scripts/segment_tool.py segment --input workspace/2407.14333v5.md --segment-size 1000 --max-segments 3
```

---

## 📋 第2步: 翻译每个段落

**工具**: `Read` + **你自己的LLM能力** + `Write`

**重要**: 你要自己翻译，不要调用任何外部API！

**流程**:

对于每个分段文件：

1. **读取段落**: 使用 `Read` 读取 `output/segments/segment_1.md`
2. **你自己翻译**: 使用你自己的语言能力将内容从英文翻译为中文
3. **保存翻译**: 使用 `Write` 保存到 `output/translations/translated_segment_1.md`
4. **重复**: 处理 segment_2.md, segment_3.md...

**翻译要求**:
- 保持所有Markdown格式（标题、列表、代码块、表格等）
- 准确翻译学术术语
- 保持专业性和流畅性
- 不要翻译代码、公式、URL
- 保持段落结构

**翻译提示词模板**:
```
请将以下Markdown内容从英文翻译为中文：
- 保持所有Markdown格式标记
- 准确翻译学术术语
- 不要翻译代码块、数学公式、URL链接
- 保持专业性

[段落内容]
```

---

## 📋 第3步: 合并翻译结果

**工具**: `Bash`  
**命令**:
```bash
python3 workspace/skills/markdown-segment-translator/scripts/segment_tool.py merge
```

**作用**:
- 将所有翻译段落合并成完整文件
- 最终文件位于: `output/final/complete_translated_[原文件名].md`

---

## ✅ 完整示例

```
用户请求: 请翻译2407.14333v5.md文件

你的执行步骤:

【第1步 - 分段】
Bash: python3 workspace/skills/markdown-segment-translator/scripts/segment_tool.py segment --input workspace/2407.14333v5.md --segment-size 1000 --max-segments 3

输出: 创建 segment_1.md (1000行), segment_2.md (1000行), segment_3.md (700行)

【第2步 - 翻译】
循环处理每个段落:

Segment 1:
  Read: output/segments/segment_1.md
  [你自己翻译这段内容为中文]
  Write: output/translations/translated_segment_1.md (写入你的翻译)

Segment 2:
  Read: output/segments/segment_2.md
  [你自己翻译这段内容为中文]
  Write: output/translations/translated_segment_2.md

Segment 3:
  Read: output/segments/segment_3.md
  [你自己翻译这段内容为中文]
  Write: output/translations/translated_segment_3.md

【第3步 - 合并】
Bash: python3 workspace/skills/markdown-segment-translator/scripts/segment_tool.py merge

输出: output/final/complete_translated_2407.14333v5.md

【完成】
使用 Read 读取最终文件并向用户报告
```

---

## ❌ 严格禁止的操作

- ❌ 不要使用旧的 `segment_translator.py` 脚本（那个会自己调用API）
- ❌ 不要让Python脚本调用翻译API
- ❌ 不要跳过分段或合并步骤
- ❌ 不要尝试一次性翻译整个文档
- ❌ 不要在第2步使用Bash调用外部翻译程序

---

## ✅ 正确的工具调用序列

```
第1步: Bash (分段工具)
第2步: Read → [你自己翻译] → Write (循环N次)
第3步: Bash (合并工具)
第4步: Read (读取最终结果)
```

---

## 🎯 为什么要这样设计？

1. **分段**: 避免token限制，确保完整翻译
2. **Agent翻译**: 利用你的LLM能力，无需额外API调用
3. **逐段处理**: 保证质量和准确性
4. **合并**: 生成完整统一的翻译文档

---

## 技能功能概述

本技能专门解决长文档翻译中的token限制问题，通过智能分段和Agent自主翻译机制，确保100%完整翻译。

**核心优势**:
- 🔧 纯工具化分段/合并
- 🧠 Agent主导翻译
- 📊 完整性保证
- 🎨 格式保持
- 📝 术语一致性
