---
name: sealeap-athena-1688-sourcing-research
description: "通过图片、关键词、供货热度和商品详情寻找 1688 货源，对齐 SKU、规格、MOQ 与阶梯价并比较候选供应商。用于找货源和比价，采购下单使用采购与履约入口。"
---

# 1688 货源发现与规格比价

通过图片、关键词、供货热度和商品详情寻找 1688 货源，对齐 SKU、规格、MOQ 与阶梯价并比较候选供应商。用于找货源和比价，采购下单使用采购与履约入口。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [1688 图片找货源](references/capabilities/1688-image-sourcing/workflow.md) | 从图片发现候选货源，再逐个确认材质、尺寸、包装数量与起订量 |
| [1688 货源详情核对](references/capabilities/1688-offer-detail/workflow.md) | 按 SKU 展开阶梯价、库存、起订量、包装和供应条件 |
| [1688 供货热度筛选](references/capabilities/1688-sales-ranking/workflow.md) | 获取可用销量估计并在已获取样本内排序，再确认阶梯价和 MOQ |
| [1688 关键词找货源](references/capabilities/1688-keyword-sourcing/workflow.md) | 逐步收敛同用途货源，按规格和数量统一比价，再筛查供应条件 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。以图、关键词与热度检索作为不同模式；规格、MOQ 和报价口径逐项核对。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
