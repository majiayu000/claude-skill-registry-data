---
name: ai-short-drama-review
description: 审核 AI 短剧已有稿的因果、人物、节奏、时长、连续性及可制作性，定位问题并按请求修订复核。用于审稿、诊断与返工；仅要求审核时不修改正文。用于该阶段的综合任务或多个子步骤组合；单一细项优先使用对应子技能。
---

# G4 剧本审核与修订

## 按需读取

先读共同约定，再按本阶段指定章节读取：标准全文；流程中的版本与返工；模板第6、8节。

资料入口：[共同约定](../ai-short-drama-writing/references/common.md)、[模板](../ai-short-drama-writing/assets/templates.md)、[标准](../ai-short-drama-writing/references/standards.md)、[流程](../ai-short-drama-writing/references/workflow.md)。

## 输入

指定版本与范围、项目约束、相关设定/分集/前文/台账和反馈；先区分只审核、直接修订、修后复核。

## 执行

本入口负责阶段内组合；单一细项任务优先直接使用下表子技能。按实际依赖选择，不要求全部执行；旧有材料可直接复用。只读取当前子技能及其所需资料，不默认加载所有子技能。

| 建议顺序 | 子技能 | 职责 |
| --- | --- | --- |
| 1 | [ai-short-drama-story-audit](../ai-short-drama-story-audit/SKILL.md) | 叙事与人物审核 |
| 2 | [ai-short-drama-continuity-audit](../ai-short-drama-continuity-audit/SKILL.md) | 连续性与知情审核 |
| 3 | [ai-short-drama-production-audit](../ai-short-drama-production-audit/SKILL.md) | 时长与可制作性审核 |
| 4 | [ai-short-drama-revision](../ai-short-drama-revision/SKILL.md) | 问题修订与影响更新 |
| 5 | [ai-short-drama-regression-review](../ai-short-drama-regression-review/SKILL.md) | 修后复核与审核结论 |

只审核时选择前三个适用审计子技能并汇总覆盖范围，不进入修订。用户要求修订时才执行 revision，随后 regression-review；后者可汇总已有审计结果，但没有修订记录时不得声称做了修后复核。

## 交付与通过条件

reviews/<范围>-<版本>-review.md；请求修订时另交新稿、台账和 changes.md。各问题有状态，各维度分别为通过/需修订/未验证。

无未解决 P0，P1 已修或有实际接受依据，必要信息完整才可判本范围通过。未验证项仍需披露；仅在用户要求交接时继续 G5。

本阶段入口可直接调用，无需先执行总入口；依赖上述子技能及相邻的 `ai-short-drama-writing` 共享目录，分发时保留相对路径。只完成本次授权阶段及必要前提，不自动开展后续阶段。

## 多集工作

处理多集节奏、知情一致性或范围/全季审查时，按需读取[多集诊断与审核](../ai-short-drama-writing/references/season-review.md)。沿用本技能的写入边界；范围审核不冒充全季通过，修改后复核新增问题。
