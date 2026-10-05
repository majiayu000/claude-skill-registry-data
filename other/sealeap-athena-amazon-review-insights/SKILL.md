---
name: sealeap-athena-amazon-review-insights
description: "分析 Amazon 商品评论、细分市场评论主题和已授权店铺反馈，核对样本、痛点与改进依据。公开评论和自家账户反馈使用各自权限及数据路径。"
---

# Amazon 评论与反馈分析

分析 Amazon 商品评论、细分市场评论主题和已授权店铺反馈，核对样本、痛点与改进依据。公开评论和自家账户反馈使用各自权限及数据路径。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Amazon 评论样本分析](references/capabilities/amazon-review-sample/workflow.md) | 按评论 ID 去重并分析使用场景、问题和可验证的改进方向 |
| [细分市场评论主题](references/capabilities/amazon-niche-review-themes/workflow.md) | 分商品采样、去重、聚类评论，并把痛点连接到可测试产品改进 |
| [Amazon 买家反馈分析](references/capabilities/amazon-account-feedback/workflow.md) | 读取获准反馈并按商品、履约和服务原因分类，匿名化引用与建议 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。公开评论、市场主题与自家账户反馈分模式，保留权限和采样差异。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
