---
name: sealeap-athena-web-demand-research
description: "使用公开网页、关键词兴趣趋势、近期热点和搜索 AI 回答研究需求线索，区分不同证据类型、时间与来源。"
---

# 公开搜索、热点与需求趋势

使用公开网页、关键词兴趣趋势、近期热点和搜索 AI 回答研究需求线索，区分不同证据类型、时间与来源。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [关键词搜索兴趣趋势](references/capabilities/keyword-interest-trends/workflow.md) | 在相同地区、时间窗和搜索类型下比较趋势并标记季节性 |
| [近期搜索热点观察](references/capabilities/daily-search-topics/workflow.md) | 查看可访问的趋势页面，核对发布日期、事件发生时间和电商相关性 |
| [搜索 AI 回答观察](references/capabilities/search-answer-observation/workflow.md) | 记录真实可见回答和引用，回查引用是否支持商品或品牌陈述 |
| [公开网页证据检索](references/capabilities/web-evidence-search/workflow.md) | 拆解查询并优先定位原始文档，交叉检查日期与支持范围 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。检索、搜索兴趣和 AI 回答观察按证据类型区分，保留时间与来源。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
