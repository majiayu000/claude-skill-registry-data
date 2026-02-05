---
# 元数据 (必填)
name: text-summary
version: "1.0.0"
description: 将长文本压缩为简洁摘要，支持多种语言
author: ExoProtocolDemo

# 定价 (必填)
pricing:
  model: per_call
  price_lamports: 10000

# 运行时要求 (必填)
runtime:
  docker_image: exo-runtime-python-3.11
  docker_image_hash: sha256:abc123def456...
  entrypoint: scripts/main.py
  timeout_seconds: 30

# 输入输出 Schema (必填)
io:
  input_schema:
    type: object
    properties:
      text:
        type: string
        description: 需要摘要的原始文本
        maxLength: 100000
      max_length:
        type: integer
        description: 摘要最大字数
        default: 200
        minimum: 50
        maximum: 1000
      language:
        type: string
        description: 输出语言
        enum: ["zh", "en", "auto"]
        default: "auto"
    required:
      - text
    additionalProperties: false
    maxProperties: 20
  output_schema:
    type: object
    properties:
      summary:
        type: string
        description: 生成的摘要文本
      word_count:
        type: integer
        description: 摘要字数
      compression_ratio:
        type: number
        description: 压缩比 (原文/摘要)

# Tool Annotations - 行为注解
annotations:
  readOnlyHint: true
  destructiveHint: false
  idempotentHint: true
  openWorldHint: false
---

# Text Summary Skill

## 功能描述

将长文本智能压缩为简洁摘要，保留核心信息。支持中文、英文及自动检测语言模式。

**适用场景**:
- 文档快速预览
- 新闻/文章摘要
- 会议记录提炼
- 研究论文概要

## 使用示例

**输入**:
```json
{
  "text": "人工智能（AI）是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统...(长文本)",
  "max_length": 100,
  "language": "zh"
}
```

**输出**:
```json
{
  "summary": "人工智能是计算机科学分支，旨在创建执行需人类智能任务的系统，包括学习、推理和自我修正能力。",
  "word_count": 42,
  "compression_ratio": 15.2
}
```

## 注意事项

- 输入文本最大 100KB
- 摘要长度范围 50-1000 字
- 纯文本输入，不支持 HTML/Markdown 解析
