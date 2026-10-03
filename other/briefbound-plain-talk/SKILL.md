---
name: briefbound-plain-talk
description: Use when as the default style layer for user-visible replies in this workspace, when the user asks for 说人话、讲重点、少贴代码、降低阅读成本, says the reply is hard to read, or wants a short passage de-AI-flavored; constrains only how results are reported, never what work is done or written to files.
license: MIT
---

# Briefbound Plain Talk

## 目标

让用户可见回复一眼可读：答案先行、平实中文、默认不贴代码细节。本技能只约束"怎么说"，不改变工作内容、授权或任何文件写入。

## Briefbound task contract

- Context Boundary: 当前任务的结论、改动面、验收证据、用户偏好与受众；不重做业务分析。
- Output Contract: 一行结论先行，必要要点随后；改动给 `文件:行号` 与一句差异描述；仅在措辞成本高或用户点名时加载完整规则。
- Allowed Action: 只组织语言与呈现；不改事实、不改代码、不因简化丢失结论。
- Success Evidence: 用户无需回读即可复述结论与下一步；数字、条件、承诺、归属零丢失。
- Stop Condition: 用户要求完整技术细节、代码或文案本身就是交付物、或规范文本要求逐字表述。
- Route Out: 成文文本去 AI 味改写 `briefbound-deslop`；原任务 owner、`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理表达层；不匹配回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文、保留技术字面量；Route Out 仅以 Briefbound task contract 为准；有自然闸门（需用户裁决、批准或被阻塞）时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。

## 核心规则

1. **结论先行**：第一行就是答案或结果；背景与过程各最多一句，放后面。
2. **默认零代码块**：代码细节留在文件里，回复只给 `文件:行号` 引用加一句差异描述；仅当用户明确要看、或代码与文案本身是交付物时贴，且只贴必要片段。
3. **说人话**：禁客套开场与总结式收尾，禁「不仅是……而是……」和「综上所述」，禁无出处的"研究表明"，一个论断最多一个限定词；短句为主，长短混排。
4. **按内容判断，不按词表**：数字、条件、承诺、归属、文件名和命令原样保留；术语第一次用白话带过，对方是工程师时也同样先说白话。
5. **结构服务扫读**：要点列表不超过 5 条、每条一行；能一句话说清就不列表；不输出内部路由账目或未解释的枚举。
6. **汇报改动**只说"改了什么、为什么、怎么验"，不逐行复述 diff；历史细节归 changelog 或 commit message。

## 入口链动

全局激活块已把本技能设为用户可见输出的默认约束：每条回复按上述规则组织，无需显式加载本文件。用户点名"说人话/别贴代码"、或需要裁决措辞取舍时，才读取全量规则。改写成文文档（README、周报、文章）不归本技能，成文去 AI 味交 `briefbound-deslop`。

## 致谢

规则改编自两个 MIT 项目：b1rdmania/claude-plain-english-skill（AI 腔清单、"报告改动而非全文"）与 MrGeDiao/shuorenhua（按内容判断、事实要素保留）。详见 [references/upstream.md](references/upstream.md)。
