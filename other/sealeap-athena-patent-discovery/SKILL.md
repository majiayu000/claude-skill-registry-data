---
name: sealeap-athena-patent-discovery
description: "按关键词、结构化条件或图像线索定位专利，核对文献身份并取得可访问文件。区分外观与技术专利、文字与视觉检索能力。"
---

# 专利检索与文献获取

按关键词、结构化条件或图像线索定位专利，核对文献身份并取得可访问文件。区分外观与技术专利、文字与视觉检索能力。

## 选择任务模式

从用户目标与已有上下文选择下表中需要的模式，只读取对应能力指南；多步骤任务可组合少数相关模式。

| 模式 | 何时选择 |
|---|---|
| [专利关键词检索](references/capabilities/patent-keyword-search/workflow.md) | 构建同义词和分类检索，筛出候选专利并核对原始公开号 |
| [专利检索式设计](references/capabilities/patent-structured-search/workflow.md) | 构建布尔检索式，按目标数据库语法执行并记录每轮收敛原因 |
| [专利文献身份核对](references/capabilities/patent-identity-resolution/workflow.md) | 标准化号码和文献种类码，逐项核对标题、申请人和日期 |
| [外观专利视觉检索](references/capabilities/design-patent-visual-search/workflow.md) | 先识别外观类别和显著特征，再通过获准视觉或分类检索筛出候选设计 |
| [技术专利图像线索检索](references/capabilities/technical-patent-visual-search/workflow.md) | 从结构图提取部件关系，构建技术检索词并核对候选附图与权利要求 |
| [专利公开文件获取](references/capabilities/patent-document-download/workflow.md) | 从官方或可验证公开来源获取 PDF，核对标题、公开号和页数 |

## 执行与交付

1. 确认对象、平台/地区、数据期间和具体任务，优先复用同口径材料。
2. 阅读匹配模式的指南及其工具路由，使用当前真实可用的工具、官方连接或授权导出；没有能力时说明缺口。
3. 按该模式的执行手册处理。文字与视觉检索区分外观/技术专利；先确认文献身份和访问能力。
4. 保留实际来源、时间、范围和 `FACT / ESTIMATE / ASSUMPTION / UNKNOWN`；未知值不填零，不混算不同市场与粒度。
5. 核对会话已有授权，已覆盖的动作继续执行并回读；缺失或扩大范围才补充确认。分析请求本身不授权下单、发布、退款或预算变更。
6. 交付模式要求的结果、证据和实际完成状态；将草稿、提交、最终生效与 `READY / HOLD / STOP` 分开报告。

共同执行约定见 [执行手册](references/playbook.md)，按能力查找工具见 [路由索引](references/tool-routing.md)。模式索引也保存在 `references/capabilities.json`，供本地搜索定位原名称。
