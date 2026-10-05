---
name: sealeap-athena-patent-status-landscape
description: "核对专利法律事件、家族关系、被引文献及在先引用，保留时间、法域和引用方向。用于专利关系或状态研究，不替代专业 FTO。"
---

# 专利法律状态、家族与引用

核对专利法律事件、家族关系、被引文献及在先引用，保留时间、法域和引用方向。用于专利关系或状态研究，不替代专业 FTO。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [专利被引关系研究](references/capabilities/patent-cited-by/workflow.md) | 查找哪些后续文献引用目标专利，按文献和家族两种口径去重 |
| [专利在先文献引用](references/capabilities/patent-prior-art-references/workflow.md) | 读取目标文献引用的专利及非专利文献，并区分审查员与申请人引用（如可用） |
| [专利法律状态核对](references/capabilities/patent-legal-events/workflow.md) | 在当前官方登记或事件记录中核对申请、授权、失效与权利变更线索 |
| [专利家族关系整理](references/capabilities/patent-family-map/workflow.md) | 按共同优先权整理家族文献并明确简单家族与扩展家族定义 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。被引与在先引用方向、家族与法律状态独立保留，不把状态摘要当 FTO。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
