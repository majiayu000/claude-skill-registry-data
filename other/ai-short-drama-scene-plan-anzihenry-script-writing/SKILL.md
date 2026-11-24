---
name: ai-short-drama-scene-plan
description: 用于 AI 短剧的把单集大纲拆成可执行场次。交付分场与场次目标的专项结果；综合阶段任务使用 ai-short-drama-episode，不自动执行其他子步骤。
---

# G3 正文-1 分场与场次目标

## 输入与范围

本集大纲、前情、资产和时长预算。

先读[共同约定](../ai-short-drama-writing/references/common.md)，再按需读标准第二至五节与模板第4、5节。入口：[标准](../ai-short-drama-writing/references/standards.md)、[流程](../ai-short-drama-writing/references/workflow.md)、[模板](../ai-short-drama-writing/assets/templates.md)。

## 执行

1. 按地点/时间/戏剧目标切场，分配稳定场ID；插场不重排旧ID。
2. 每场写目标、阻力、必要信息、入场和出场变化。
3. 估计场次预算，合并仅重复信息的场；不给尚未设计的对白伪造ID。

## 产物与写入边界

episodes/<集>-<版本>.md 的分场结构：场ID、时地、人物资产、目标阻力、首尾状态、预算。

默认在已有项目文件的对应章节维护；无文件时可先交付同结构文本。只修改上述产物及用户明确要求的必要关联内容，其他问题列影响与返工建议。每次标明输入版本、输出版本、覆盖范围和未决项。

## 验收与返工

场次有叙事作用且总量可落入本集预算。

大纲事件无法容纳时回分集规划，不偷删必要转折。

本步骤完成后停止，除非用户已要求后续步骤。可通过[阶段入口](../ai-short-drama-episode/SKILL.md)衔接；直接调用无需先执行阶段入口。共享资料与父入口需要保留相邻目录。
