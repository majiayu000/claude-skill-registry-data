---
name: sealeap-athena-commerce-copywriting
description: "生成基于产品事实的电商文案，或核对 Amazon 标题质量。按平台、语言、关键词和当前规则区分草稿写作与标题检查。"
---

# 电商文案与标题质检

生成基于产品事实的电商文案，或核对 Amazon 标题质量。按平台、语言、关键词和当前规则区分草稿写作与标题检查。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [电商文本草稿](references/capabilities/commerce-copy-draft/workflow.md) | 根据事实组织标题、卖点或营销文案，并逐句核对可证实性 |
| [Amazon 标题质量核对](references/capabilities/amazon-title-audit/workflow.md) | 检查相关性、信息顺序、重复、可读性与当前类目要求，给出改稿 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。通用草稿与 Amazon 标题核验分模式；保留平台语言、产品事实和规则。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
