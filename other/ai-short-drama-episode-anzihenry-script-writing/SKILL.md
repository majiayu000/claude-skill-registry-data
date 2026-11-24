---
name: ai-short-drama-episode
description: 根据大纲与设定撰写 AI 短剧单集或批次分场剧本，完成动作、对白、时间预算和连续性更新。用于试写、续写及正文创作；已有稿的系统诊断优先使用审核技能。用于该阶段的综合任务或多个子步骤组合；单一细项优先使用对应子技能。
---

# G3 单集与批次剧本写作

## 按需读取

先读共同约定，再按本阶段指定章节读取：模板第4、5节；写作标准全文；需要格式示范时读完整单集示例。

资料入口：[共同约定](../ai-short-drama-writing/references/common.md)、[模板](../ai-short-drama-writing/assets/templates.md)、[标准](../ai-short-drama-writing/references/standards.md)、[流程](../ai-short-drama-writing/references/workflow.md)。 [完整单集示例](../ai-short-drama-writing/references/example.md)。

## 输入

指定集数范围、大纲与设定、资产、相关前文和连续性台账。只给创意要求试写时，先列最小暂定设定和本集变化，不额外写完整季策划。

## 执行

本入口负责阶段内组合；单一细项任务优先直接使用下表子技能。按实际依赖选择，不要求全部执行；旧有材料可直接复用。只读取当前子技能及其所需资料，不默认加载所有子技能。

| 建议顺序 | 子技能 | 职责 |
| --- | --- | --- |
| 1 | [ai-short-drama-scene-plan](../ai-short-drama-scene-plan/SKILL.md) | 分场与场次目标 |
| 2 | [ai-short-drama-action-writing](../ai-short-drama-action-writing/SKILL.md) | 可视行动与表演 |
| 3 | [ai-short-drama-dialogue-writing](../ai-short-drama-dialogue-writing/SKILL.md) | 对白与角色口吻 |
| 4 | [ai-short-drama-timing](../ai-short-drama-timing/SKILL.md) | 时长编排与压缩 |
| 5 | [ai-short-drama-continuity-update](../ai-short-drama-continuity-update/SKILL.md) | 正文状态与伏笔记账 |

顺序是常用依赖顺序，不是逐步批准要求。输入缺失时先补最小前提并标假设；上游变化影响已存在的下游内容时，标为待复核而非重做整个项目。

## 交付与通过条件

episodes/EPxxx-版本.md 和相关 continuity/<集>-<版本>.md 更新，附时间预算、假设及下集入口。关键内容可演可听、对白有说话者、引用资产存在、状态可衔接。

向 G4 传递稿件与依赖版本。写完不自动等于 reviewed；有实际自审时记录范围、方法与结论。不得自动续写请求以外的整季。

本阶段入口可直接调用，无需先执行总入口；依赖上述子技能及相邻的 `ai-short-drama-writing` 共享目录，分发时保留相对路径。只完成本次授权阶段及必要前提，不自动开展后续阶段。
