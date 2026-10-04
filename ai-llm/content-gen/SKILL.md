---
name: content_gen
description: 正文生成(四模式)
category: generate
version: "1.0.0"
license: MIT
metadata:
  author: BidMaster Pro
  triggers:
    - 生成
    - 撰写
    - 写内容
---

# 正文生成技能

## 模式说明
- **A模式(AI撰写)**: LLM根据大纲+招标要求直接撰写
- **B模式(材料组装)**: 从知识库检索相关材料→组装成章节
- **C模式(模板填充)**: 选择历史标书模板→填充项目信息
- **D模式(外部采集)**: 从外部数据源采集内容→整合成章节

## 输出格式
JSON: `{"content": "章节正文", "word_count": 实际字数}`
