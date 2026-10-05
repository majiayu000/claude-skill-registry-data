---
name: sealeap-athena-temu-product-pricing
description: "处理 Temu 美国区、欧洲区或全球区的商品草稿、商品管理与价格变更。先确定地区，再读取对应地区的流程、字段和权限，避免跨区复用。"
---

# Temu 商品与价格管理

处理 Temu 美国区、欧洲区或全球区的商品草稿、商品管理与价格变更。先确定地区，再读取对应地区的流程、字段和权限，避免跨区复用。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Temu 美国区 新商品草稿与发布](references/capabilities/temu-us-add-product/workflow.md) | 确认当前类目必填字段与资格，生成本地草稿并预检；已授权发布时提交并核对商品状态 |
| [Temu 美国区 商品管理](references/capabilities/temu-us-product/workflow.md) | 读取商品现状与当前类目 schema，生成字段级变更预览，验证后执行授权范围并回读 |
| [Temu 美国区 价格核对与变更](references/capabilities/temu-us-pricing/workflow.md) | 读取现价和促销叠加，测算授权价格变化后逐 SKU 提交并回读生效值 |
| [Temu 欧洲区 商品管理](references/capabilities/temu-eu-product/workflow.md) | 读取商品现状与当前类目 schema，生成字段级变更预览，验证后执行授权范围并回读 |
| [Temu 欧洲区 价格核对与变更](references/capabilities/temu-eu-pricing/workflow.md) | 读取现价和促销叠加，测算授权价格变化后逐 SKU 提交并回读生效值 |
| [Temu 全球区 商品管理](references/capabilities/temu-global-product/workflow.md) | 读取商品现状与当前类目 schema，生成字段级变更预览，验证后执行授权范围并回读 |
| [Temu 全球区 价格核对与变更](references/capabilities/temu-global-pricing/workflow.md) | 读取现价和促销叠加，测算授权价格变化后逐 SKU 提交并回读生效值 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。先确定美国/欧洲/全球区，再读取地区流程与 schema；不跨区复用端点或账号。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
