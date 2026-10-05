---
name: sealeap-athena-temu-market-research
description: "检索 Temu 商品、图片同款、店铺与类目，分析样本需求及竞争。用于公开市场研究和店铺对标，保留第三方估计与自有账户数据的差别。"
---

# Temu 市场、商品与店铺研究

检索 Temu 商品、图片同款、店铺与类目，分析样本需求及竞争。用于公开市场研究和店铺对标，保留第三方估计与自有账户数据的差别。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Temu 商品检索](references/capabilities/temu-product-discovery/workflow.md) | 筛选同用途商品并核对规格、包装数量、定价及需求估计 |
| [Temu 店铺公开画像](references/capabilities/temu-shop-profile/workflow.md) | 整理可查询的店铺信息与商品线索，标注每项数据来源 |
| [Temu 类目检索](references/capabilities/temu-category-map/workflow.md) | 确认类目层级，再查看可用类目统计与代表商品 |
| [Temu 商品市场分析](references/capabilities/temu-product-market-analysis/workflow.md) | 从检索到单商品趋势分析，结合规格和价格判断需求变化 |
| [Temu 店铺对标研究](references/capabilities/temu-shop-benchmark/workflow.md) | 核对店铺身份并比较可用经营指标和商品线索 |
| [Temu 类目需求研究](references/capabilities/temu-category-demand/workflow.md) | 确认类目后分析可用需求、价格带与竞争结构 |
| [Temu 图片找同款](references/capabilities/temu-visual-match/workflow.md) | 提取图片属性并用可用视觉搜索或商品关键词找候选，逐项核对差异 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。第三方样本与官方账户数据分开；图片相似不等于同规格。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
