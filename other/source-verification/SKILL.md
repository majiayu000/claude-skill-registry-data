---
name: source-verification
description: 验证信源可信度的研究过程知识，指导 agent 在涉及事实声明时交叉核验信源
allowed-tools:
  - web_search
  - browse_page
enabled: true
related-skills: []
---

# Source Verification

## 何时使用
研究涉及事实声明、统计数据、引用或任何需要可信背书的信息时。不适用于纯推理或用户主观偏好类问题。

## 核心原则
**任何事实声明在写入 observation 前，至少需一个独立信源交叉核验。** 单一信源的可信度不足以支撑结论。

## 步骤

1. **识别声明**：从研究问题或中间结论中抽出需验证的事实声明。
2. **定位信源**：用 `web_search` 找 2 个以上独立来源（不同机构/作者/时间）。优先一手来源（官方报告、论文原文）而非二手转述。
3. **核验一致性**：用 `browse_page` 读全文（非 snippet），比对关键数字/日期/结论是否一致。
4. **记录可信度**：在 observation 标注信源可信度（高/中/低）+ 不一致点。低可信度声明降级为"待证"。

## 失败模式（避免）
- 只看 search snippet 就采信（snippet 常断章取义）
- 两个来源实际互引（非独立）
- 一手来源被二手来源误读（回溯原文）
- 把"无法证伪"当"为真"
