---
name: ai-short-drama-outline
description: 将 AI 短剧总纲拆成分集大纲，规划各集目标、变化、回报、衔接和伏笔回收。用于全季拆集、集数调整及跨集结构重排；不负责完整场次对白。用于该阶段的综合任务或多个子步骤组合；单一细项优先使用对应子技能。
---

# G2 分集规划与伏笔设计

## 按需读取

先读共同约定，再按本阶段指定章节读取：模板第3、5节；标准第一、五节；流程中的批量生产。

资料入口：[共同约定](../ai-short-drama-writing/references/common.md)、[模板](../ai-short-drama-writing/assets/templates.md)、[标准](../ai-short-drama-writing/references/standards.md)、[流程](../ai-short-drama-writing/references/workflow.md)。

## 输入

简报规格、总纲和结局、人物规则及资产、已有集的锁定情况。集数未定时提出有依据的工作集数并标为建议，不暗改指定集数。

## 执行

本入口负责阶段内组合；单一细项任务优先直接使用下表子技能。按实际依赖选择，不要求全部执行；旧有材料可直接复用。只读取当前子技能及其所需资料，不默认加载所有子技能。

| 建议顺序 | 子技能 | 职责 |
| --- | --- | --- |
| 1 | [ai-short-drama-season-arc](../ai-short-drama-season-arc/SKILL.md) | 全季结构与篇幅分配 |
| 2 | [ai-short-drama-episode-beats](../ai-short-drama-episode-beats/SKILL.md) | 单集事件节拍 |
| 3 | [ai-short-drama-hooks](../ai-short-drama-hooks/SKILL.md) | 开场吸引与结尾回报 |
| 4 | [ai-short-drama-foreshadow](../ai-short-drama-foreshadow/SKILL.md) | 伏笔投放与回收 |
| 5 | [ai-short-drama-episode-bridges](../ai-short-drama-episode-bridges/SKILL.md) | 跨集连接与状态计划 |

顺序是常用依赖顺序，不是逐步批准要求。输入缺失时先补最小前提并标假设；上游变化影响已存在的下游内容时，标为待复核而非重做整个项目。

## 交付与通过条件

outline.md 的伏笔计划与跨集计划状态。每集有实际变化、前后因果成立、关键回收有铺垫，篇幅及资产冲突已处理或明确列出。

向 G3 传递本集大纲版本、前情、人物状态、伏笔要求和预算。局部拆集只交付本范围及相邻连接，不宣称全季检查通过。

本阶段入口可直接调用，无需先执行总入口；依赖上述子技能及相邻的 `ai-short-drama-writing` 共享目录，分发时保留相对路径。只完成本次授权阶段及必要前提，不自动开展后续阶段。
