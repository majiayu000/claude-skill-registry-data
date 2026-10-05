---
name: sealeap-athena-amazon-market-assessment
description: "从关键词或 ASIN 定义 Amazon 细分市场，评估需求、容量、竞争和相邻产品机会。用于市场研究、细分方向比较及选品机会判断。"
---

# Amazon 细分市场与机会评估

从关键词或 ASIN 定义 Amazon 细分市场，评估需求、容量、竞争和相邻产品机会。用于市场研究、细分方向比较及选品机会判断。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Amazon 关键词市场机会](references/capabilities/amazon-keyword-opportunity/workflow.md) | 把关键词需求、季节性、竞品集中度与单位经济放在相同口径下评估 |
| [Amazon 细分市场评估](references/capabilities/amazon-niche-assessment/workflow.md) | 冻结样本后分析需求、集中度、新品与利润约束 |
| [Amazon 类目机会发现](references/capabilities/amazon-market-discovery/workflow.md) | 按市场维度发现候选类目，确认类目节点和统计样本 |
| [Amazon 市场统计核对](references/capabilities/amazon-market-statistics/workflow.md) | 分析品牌集中、价格带、上架 cohort 与商品构成并核对分母 |
| [关键词定义细分市场](references/capabilities/amazon-niche-from-keyword/workflow.md) | 先定义需求边界，再识别相关类目与直接竞品，剔除异类流量 |
| [ASIN 定位细分市场](references/capabilities/amazon-niche-from-asin/workflow.md) | 从商品属性与实际流量词构建相邻竞品池，再确认直接竞争关系 |
| [细分需求找产品](references/capabilities/amazon-niche-product-discovery/workflow.md) | 按场景与经济性发现产品，解释匹配依据及淘汰条件 |
| [Amazon 相邻竞品扩展](references/capabilities/amazon-niche-asin-expansion/workflow.md) | 从种子商品提取用途和词群，扩展并人工核对相邻 ASIN |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。保留关键词/ASIN 两类市场入口、样本冻结、容量与竞争口径。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
