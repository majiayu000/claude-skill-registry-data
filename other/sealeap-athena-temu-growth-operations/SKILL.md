---
name: sealeap-athena-temu-growth-operations
description: "处理 Temu 各地区的促销与广告任务，按美国、欧洲或全球区选择相应流程，核对优惠条件、预算和用户已授权的动作。"
---

# Temu 促销与广告管理

处理 Temu 各地区的促销与广告任务，按美国、欧洲或全球区选择相应流程，核对优惠条件、预算和用户已授权的动作。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Temu 美国区 促销管理](references/capabilities/temu-us-promotion/workflow.md) | 核对当前活动与资格，计算折扣叠加、库存和毛利影响，提交授权配置后回读 |
| [Temu 美国区 广告管理](references/capabilities/temu-us-ads/workflow.md) | 先读广告实体与同窗报表，形成出价、预算或状态差异，执行已授权对象并回读 |
| [Temu 欧洲区 促销管理](references/capabilities/temu-eu-promotion/workflow.md) | 核对当前活动与资格，计算折扣叠加、库存和毛利影响，提交授权配置后回读 |
| [Temu 欧洲区 广告管理](references/capabilities/temu-eu-ads/workflow.md) | 先读广告实体与同窗报表，形成出价、预算或状态差异，执行已授权对象并回读 |
| [Temu 全球区 促销管理](references/capabilities/temu-global-promotion/workflow.md) | 核对当前活动与资格，计算折扣叠加、库存和毛利影响，提交授权配置后回读 |
| [Temu 全球区 广告管理](references/capabilities/temu-global-ads/workflow.md) | 先读广告实体与同窗报表，形成出价、预算或状态差异，执行已授权对象并回读 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。地区、促销类型与广告预算仍分别验证，保留各动作授权。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
