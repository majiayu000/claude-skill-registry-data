---
name: ai-short-drama-bible
description: 为 AI 短剧建立或修订故事总纲、结局、人物弧线、世界规则和资产设定集。用于故事开发、人设设计及改编设定；逐集拆分使用分集规划技能。用于该阶段的综合任务或多个子步骤组合；单一细项优先使用对应子技能。
---

# G1 故事与人物设定

## 按需读取

先读共同约定，再按本阶段指定章节读取：模板第2节；标准第一、四、五节。

资料入口：[共同约定](../ai-short-drama-writing/references/common.md)、[模板](../ai-short-drama-writing/assets/templates.md)、[标准](../ai-short-drama-writing/references/standards.md)、[流程](../ai-short-drama-writing/references/workflow.md)。

## 输入

项目简报或等价要求、可读原作、已有设定与资产；修订时还需旧版本及已有分集和正文依赖。

## 执行

本入口负责阶段内组合；单一细项任务优先直接使用下表子技能。按实际依赖选择，不要求全部执行；旧有材料可直接复用。只读取当前子技能及其所需资料，不默认加载所有子技能。

| 建议顺序 | 子技能 | 职责 |
| --- | --- | --- |
| 1 | [ai-short-drama-plot](../ai-short-drama-plot/SKILL.md) | 故事因果与结局 |
| 2 | [ai-short-drama-characters](../ai-short-drama-characters/SKILL.md) | 人物欲望与弧线 |
| 3 | [ai-short-drama-relationships](../ai-short-drama-relationships/SKILL.md) | 关系与秘密网络 |
| 4 | [ai-short-drama-world-rules](../ai-short-drama-world-rules/SKILL.md) | 世界规则与时间线 |
| 5 | [ai-short-drama-asset-bible](../ai-short-drama-asset-bible/SKILL.md) | 叙事资产设定 |

顺序是常用依赖顺序，不是逐步批准要求。输入缺失时先补最小前提并标假设；上游变化影响已存在的下游内容时，标为待复核而非重做整个项目。

## 交付与通过条件

bible.md：一句话故事、完整总纲、人物卡、关系与弧线、规则、资产表及适用的改编映射。结局与关键选择有前提，身份无冲突，预算冲突有说明。

向 G2 传递版本、结局、节点、不可改变项和初始状态。关键结局尚未确定时标为提案，依赖它的分集只能暂定。

本阶段入口可直接调用，无需先执行总入口；依赖上述子技能及相邻的 `ai-short-drama-writing` 共享目录，分发时保留相对路径。只完成本次授权阶段及必要前提，不自动开展后续阶段。
