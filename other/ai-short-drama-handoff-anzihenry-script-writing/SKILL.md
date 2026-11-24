---
name: ai-short-drama-handoff
description: 将指定版本的 AI 短剧剧本整理为分镜、美术与声音交接包，提取场次、对白、资产、状态及按需 JSON。用于制作交接和结构化导出；不负责重写剧情或生成视频。用于该阶段的综合任务或多个子步骤组合；单一细项优先使用对应子技能。
---

# G5 制作交接与结构化导出

## 按需读取

先读共同约定，再按本阶段指定章节读取：交接协议全文；模板第7节；流程中的状态与版本。

资料入口：[共同约定](../ai-short-drama-writing/references/common.md)、[模板](../ai-short-drama-writing/assets/templates.md)、[标准](../ai-short-drama-writing/references/standards.md)、[流程](../ai-short-drama-writing/references/workflow.md)。 [交接协议](../ai-short-drama-writing/references/handoff.md)。

## 输入

指定稿件、设定与台账版本、审核结果、现有资产和下游格式要求。正式交接使用 reviewed/locked；用户要求整理 draft 可输出草稿预交接并醒目标明未审核。

## 执行

本入口负责阶段内组合；单一细项任务优先直接使用下表子技能。按实际依赖选择，不要求全部执行；旧有材料可直接复用。只读取当前子技能及其所需资料，不默认加载所有子技能。

| 建议顺序 | 子技能 | 职责 |
| --- | --- | --- |
| 1 | [ai-short-drama-delivery-baseline](../ai-short-drama-delivery-baseline/SKILL.md) | 交付版本与清单 |
| 2 | [ai-short-drama-scene-handoff](../ai-short-drama-scene-handoff/SKILL.md) | 场次与导演约束交接 |
| 3 | [ai-short-drama-audio-handoff](../ai-short-drama-audio-handoff/SKILL.md) | 对白与声音交接 |
| 4 | [ai-short-drama-asset-handoff](../ai-short-drama-asset-handoff/SKILL.md) | 美术资产需求交接 |
| 5 | [ai-short-drama-structured-export](../ai-short-drama-structured-export/SKILL.md) | 结构化导出与交付核对 |

先确定基线，再按需要提取场次、声音与资产；最后核对清单。没有机器读取需求时不导出 JSON。缺少审核只能按用户请求给出明确标记的预交接。

## 交付与通过条件

handoff/<集>-<版本>.md，包含场次、对白、资产需求、状态、声音/文字、时间及未决项；需要时另交同版本 JSON。

下游能定位每个引用与版本，信息与正文一致，质量状态透明。未锁定注明仅供预制作；未实际接收不代填。完成交接不触发生成、发布或对外沟通。

本阶段入口可直接调用，无需先执行总入口；依赖上述子技能及相邻的 `ai-short-drama-writing` 共享目录，分发时保留相对路径。只完成本次授权阶段及必要前提，不自动开展后续阶段。
