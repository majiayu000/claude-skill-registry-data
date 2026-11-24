---
name: ai-short-drama-continuity-update
description: 用于 AI 短剧的依据已写正文更新实际连续性台账。交付正文状态与伏笔记账的专项结果；综合阶段任务使用 ai-short-drama-episode，不自动执行其他子步骤。
---

# G3 正文-5 正文状态与伏笔记账

## 输入与范围

指定版本正文、已有台账和计划。

先读[共同约定](../ai-short-drama-writing/references/common.md)，再按需读标准第二至五节与模板第4、5节。入口：[标准](../ai-short-drama-writing/references/standards.md)、[流程](../ai-short-drama-writing/references/workflow.md)、[模板](../ai-short-drama-writing/assets/templates.md)。

## 执行

1. 提取实际发生的知情、持物、伤势、服饰、关系和资源变化，附动作/对白来源。
2. 对照伏笔计划登记实际投放或回收，不把计划直接复制为已发生。
3. 更新本集末状态和下一集入口，列计划偏差及受影响后续内容。

## 产物与写入边界

continuity/<集>-<版本>.md 的实际记录：对象ID、集场、入场、事件证据、出场、计划偏差；伏笔实际状态。

默认在已有项目文件的对应章节维护；无文件时可先交付同结构文本。只修改上述产物及用户明确要求的必要关联内容，其他问题列影响与返工建议。每次标明输入版本、输出版本、覆盖范围和未决项。

## 验收与返工

每条实际变化可回查正文；无证据不补记成事实。

发现矛盾交连续性审核，不默改正文来让台账看似一致。

本步骤完成后停止，除非用户已要求后续步骤。可通过[阶段入口](../ai-short-drama-episode/SKILL.md)衔接；直接调用无需先执行阶段入口。共享资料与父入口需要保留相邻目录。

## 多集索引

需要可查询的连续性或伏笔对照时，读取[结构化记录](../ai-short-drama-writing/references/structured-records.md)。在本技能负责的原产物内维护记录，登记新版本后执行 index；冲突和缺失保留为待复核，不为通过检查编造状态。
