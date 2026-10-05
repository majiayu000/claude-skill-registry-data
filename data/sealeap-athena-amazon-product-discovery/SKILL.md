---
name: sealeap-athena-amazon-product-discovery
description: "按关键词、图片、价格、需求、评价或历史条件检索 Amazon 候选商品，明确样本与变体口径。用于找产品、商品库筛选和候选池建立。"
---

# Amazon 商品检索与筛选

按关键词、图片、价格、需求、评价或历史条件检索 Amazon 候选商品，明确样本与变体口径。用于找产品、商品库筛选和候选池建立。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Amazon 商品检索](references/capabilities/amazon-product-search/workflow.md) | 先定义筛选口径，再检索并按 child ASIN 去重，核对与需求的匹配程度 |
| [Amazon 图片找商品](references/capabilities/amazon-visual-discovery/workflow.md) | 先识别可见属性，再使用可用视觉搜索或属性检索找到候选并逐项比图 |
| [Amazon 市场条件筛选](references/capabilities/amazon-opportunity-screen/workflow.md) | 先做可调整的初筛，再核实边界样本与新品机会，报告命中和淘汰理由 |
| [Amazon 历史表现筛选](references/capabilities/amazon-history-product-screen/workflow.md) | 在指定历史时点筛选商品，再核对当前状态与期间变化 |
| [Amazon 指标选品](references/capabilities/amazon-metric-product-screen/workflow.md) | 先筛可比商品，再核对临界值、异常点与供应成本 |
| [Amazon 商品库条件筛选](references/capabilities/amazon-product-database-screen/workflow.md) | 按明确条件筛选商品并保留命中与排除记录 |
| [Amazon 需求导向检索](references/capabilities/amazon-sales-product-query/workflow.md) | 按已验证的需求指标查询商品并对边界条件复查 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。关键词、图片、条件和历史筛选按需路由；保留不同数据源的样本与筛选语义。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
