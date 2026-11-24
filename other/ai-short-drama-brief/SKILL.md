---
name: ai-short-drama-brief
description: 将 AI 短剧创意、IP 或业务需求整理为立项简报，明确受众、叙事承诺、规格和制作约束。用于选题立项与需求梳理；不负责完整故事总纲或分集正文。用于该阶段的综合任务或多个子步骤组合；单一细项优先使用对应子技能。
---

# G0 立项与项目简报

## 按需读取

先读共同约定，再按本阶段指定章节读取：模板第1节；流程 G0。

资料入口：[共同约定](../ai-short-drama-writing/references/common.md)、[模板](../ai-short-drama-writing/assets/templates.md)、[标准](../ai-short-drama-writing/references/standards.md)、[流程](../ai-short-drama-writing/references/workflow.md)。

## 输入

创意或 IP 素材、受众、题材、时长和集数、画面形态、可用资产及成本约束。

## 执行

本入口负责阶段内组合；单一细项任务优先直接使用下表子技能。按实际依赖选择，不要求全部执行；旧有材料可直接复用。只读取当前子技能及其所需资料，不默认加载所有子技能。

| 建议顺序 | 子技能 | 职责 |
| --- | --- | --- |
| 1 | [ai-short-drama-intake](../ai-short-drama-intake/SKILL.md) | 需求澄清 |
| 2 | [ai-short-drama-source-map](../ai-short-drama-source-map/SKILL.md) | 素材盘点与改编边界 |
| 3 | [ai-short-drama-audience](../ai-short-drama-audience/SKILL.md) | 受众与叙事承诺 |
| 4 | [ai-short-drama-premise](../ai-short-drama-premise/SKILL.md) | 选题与一句话故事 |
| 5 | [ai-short-drama-constraints](../ai-short-drama-constraints/SKILL.md) | 规格与制作预算 |

顺序是常用依赖顺序，不是逐步批准要求。输入缺失时先补最小前提并标假设；上游变化影响已存在的下游内容时，标为待复核而非重做整个项目。

## 交付与通过条件

brief.md 或现有对应简报。内容能回答为谁写、看什么、做多长、什么形态、受哪些约束和本次做哪些内容；确认值与建议值清楚分开。

向 G1 传递简报版本、素材位置和不可改变项。通过表示需求足以开展开发，不等于商业立项获批。

本阶段入口可直接调用，无需先执行总入口；依赖上述子技能及相邻的 `ai-short-drama-writing` 共享目录，分发时保留相对路径。只完成本次授权阶段及必要前提，不自动开展后续阶段。
