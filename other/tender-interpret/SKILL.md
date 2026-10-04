---
name: tender_interpret
description: 15维度招标文件解读
category: interpret
version: "1.0.0"
license: MIT
metadata:
  author: BidMaster Pro
  triggers:
    - 解读
    - 招标解读
    - 分析招标文件
---

# 招标文件解读技能

## 触发条件
当用户需要解读招标文件、提取关键信息时触发。

## 工作流程
1. 接收招标文件文本
2. 按关键词提取相关上下文
3. 15个维度并发调用LLM解读
4. 聚合结果返回

## 输出格式
JSON格式的15维度解读结果，每个维度包含提取的关键信息。
