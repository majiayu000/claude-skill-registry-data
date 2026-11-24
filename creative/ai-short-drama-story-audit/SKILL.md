---
name: ai-short-drama-story-audit
description: 用于 AI 短剧的诊断剧情因果、人物动机、反转和表达。交付叙事与人物审核的专项结果；综合阶段任务使用 ai-short-drama-review，不自动执行其他子步骤。
---

# G4 审核-1 叙事与人物审核

## 输入与范围

待审稿、总纲人物设定、范围及反馈。

先读[共同约定](../ai-short-drama-writing/references/common.md)，再按需读标准及流程的版本/返工规则、模板第6、8节。入口：[标准](../ai-short-drama-writing/references/standards.md)、[流程](../ai-short-drama-writing/references/workflow.md)、[模板](../ai-short-drama-writing/assets/templates.md)。

## 执行

1. 固定版本和可读范围，区分违反约束与个人审美建议。
2. 检查因果、选择代价、反转前提、信息重复、口吻及本集回报。
3. 给每项问题附集场/对白定位、证据、等级和返工层级，不改正文。

## 产物与写入边界

reviews/<范围>-<版本>-review.md 的叙事问题：问题ID、等级、位置、证据、影响、建议、状态。

默认在已有项目文件的对应章节维护；无文件时可先交付同结构文本。只修改上述产物及用户明确要求的必要关联内容，其他问题列影响与返工建议。每次标明输入版本、输出版本、覆盖范围和未决项。

## 验收与返工

结论可复查，未检查内容不宣称通过。

缺关键前文标未验证；修订另由明确授权的修订步骤执行。

本步骤完成后停止，除非用户已要求后续步骤。可通过[阶段入口](../ai-short-drama-review/SKILL.md)衔接；直接调用无需先执行阶段入口。共享资料与父入口需要保留相邻目录。
