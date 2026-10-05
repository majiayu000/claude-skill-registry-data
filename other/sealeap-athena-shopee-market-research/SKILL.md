---
name: sealeap-athena-shopee-market-research
description: "研究 Shopee 市场商品与公开商品详情，核对规格、价格和样本覆盖。用于竞品与选品线索，不以市场数据替代商家账户权限。"
---

# Shopee 市场与商品研究

研究 Shopee 市场商品与公开商品详情，核对规格、价格和样本覆盖。用于竞品与选品线索，不以市场数据替代商家账户权限。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Shopee 市场商品搜索](references/capabilities/shopee-market-product-search/workflow.md) | 检索商品并按国家和变体拆开价格、销量估计和评价 |
| [Shopee 公开商品详情](references/capabilities/shopee-public-product-detail/workflow.md) | 核对商品与变体、价格、销量估计和评价信息 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。保持公开研究与商家账户管理的权限区别。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
