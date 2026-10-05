---
name: sealeap-athena-amazon-keyword-traffic
description: "研究 Amazon ABA、ASIN 反查、关键词拓展、搜索需求趋势、SERP 与品牌可见度。用于关键词库、搜索流量结构或 AI 购物回答观察，保留各指标与数据通道差异。"
---

# Amazon 关键词与搜索流量研究

研究 Amazon ABA、ASIN 反查、关键词拓展、搜索需求趋势、SERP 与品牌可见度。用于关键词库、搜索流量结构或 AI 购物回答观察，保留各指标与数据通道差异。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [Amazon ABA 搜索词分析](references/capabilities/amazon-aba-research/workflow.md) | 对齐完整周或完整月，分析搜索频率排名与点击和转化份额变化 |
| [Amazon 流量词拆解](references/capabilities/amazon-traffic-keywords/workflow.md) | 反查流量关键词并区分自然和广告代理信号，按相关性整理词群 |
| [Amazon 关键词竞争度](references/capabilities/amazon-keyword-competition/workflow.md) | 对齐搜索需求与结果样本，比较相关竞品密度和竞争格局 |
| [Amazon 反查词交叉核验](references/capabilities/amazon-reverse-keyword-check/workflow.md) | 反查搜索曝光词并与同窗已有词表比对，解释来源差异 |
| [Amazon 长尾关键词拓展](references/capabilities/amazon-keyword-expansion/workflow.md) | 拓展关键词后按需求、相关性和使用场景分组 |
| [Amazon 搜索需求历史](references/capabilities/amazon-keyword-history/workflow.md) | 核对历史需求和排名趋势，标注旺淡季与数据缺口 |
| [Amazon 品牌搜索可见度](references/capabilities/amazon-brand-search-visibility/workflow.md) | 在固定 SERP 样本内统计各品牌出现占比，核对品牌归属 |
| [Amazon 关键词需求洞察](references/capabilities/amazon-keyword-demand-insight/workflow.md) | 把需求趋势、相关商品和竞争样本合并为可检验机会假设 |
| [ASIN 搜索词反查](references/capabilities/amazon-asin-keywords/workflow.md) | 通过已授权 SIF 直连反查关键词，再核对自然和广告位置与商品相关性 |
| [ASIN 搜索曝光概览](references/capabilities/amazon-serp-footprint/workflow.md) | 读取搜索页面占位与曝光代理分布，解释自然和广告的差异 |
| [关键词下竞品流量结构](references/capabilities/amazon-keyword-traffic-mix/workflow.md) | 先取得关键词结果，再关联竞品曝光数据并分自然与已验证广告位 |
| [Amazon 对话购物结果核验](references/capabilities/amazon-shopping-answer-audit/workflow.md) | 将购物需求拆为条件，观察实际可访问的问答结果并回查商品事实 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。保留 ABA、反查、拓词、趋势、SERP 与 AI 回答观察的独立指标定义；不把可见度当点击份额。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
