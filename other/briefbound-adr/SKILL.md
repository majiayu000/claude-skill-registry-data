---
name: briefbound-adr
description: Use when the user asks to record a settled architecture or technology decision as an ADR（写 ADR、记录决策、技术选型定案存档）, or a "why" trail is needed for a chosen design, an old decision must be superseded, or new work conflicts with a prior decision; do not use for options still under discussion, project status snapshots, or README writing.
license: MIT
---

# Briefbound ADR 决策记录

## 目标

把已拍板的架构/技术决策落成可追溯的 ADR：为什么这么定、放弃过哪些选项、带来什么后果。MADR 风格（背景、决策、备选方案、后果）＋状态流转与决策债务提示，让未来维护者读到"当时为什么"，而不是只有"现在是什么"。

## Briefbound task contract

- Context Boundary: 定案决策及其动机、被否选项、相关会话结论与 git diff、项目 ADR 目录约定（默认 `docs/adr/`）；不重做方案设计。
- Output Contract: 单条 ADR（编号、状态、日期、背景、决策、备选方案、后果）+ 索引更新 + 状态流转记录 + Route Out。
- Allowed Action: 直接写 `docs/adr/`（或项目约定目录）下的 markdown；读 git diff、会话与既有文档取证；不改业务代码。
- Success Evidence: 决策、背景、备选、后果四要素齐备且可溯源；索引计数与条目一致；superseded 条目互链新旧。
- Stop Condition: 方案未拍板、事实源不足无法还原动机、或用户要的是状态盘点而非决策留痕。
- Route Out: 未拍板讨论回 `briefbound-planning`；状态快照归 `briefbound-project-memory`；验证后残留 `briefbound-development-cleanup`；`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文、保留技术字面量；Route Out 仅以 Briefbound task contract 为准；有自然闸门（需用户裁决、批准或被阻塞）时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。

## 激活闸门

任一：用户要求记录决策或写 ADR；技术选型刚定案要存档；"为什么这么设计"需要留痕；要 supersede 旧决策；新工作与已接受决策冲突需梳理。排除：仍在讨论未拍板（回 `briefbound-planning` 或 `briefbound-router`）、项目状态盘点（`briefbound-project-memory`）、契约设计本身（`briefbound-api-contract`）。

## 记录方法

- 一条决策一个文件：`NNNN-<标题>.md`，序号递增不复用；状态 `proposed → accepted → superseded`，上下文变化只改状态，不改历史结论。
- 四要素：背景（约束与动机）、决策（定案与理由）、备选方案（被否选项及否决理由）、后果（收益、代价、风险）。
- 取证：从会话结论提炼理由，从 git diff 还原实施范围；无证据的推断标 `TODO(待核实)`，不编造动机。
- supersede：新条目链接旧条目，旧条目只改状态并指回新条目；不删除、不改写已接受内容。
- 决策债务：后续工作与 accepted 决策冲突时，先提示债务（哪条决策、冲突点、建议路径），由用户裁决后走 supersede，不静默绕开。

## 与相邻 owner 的边界

- `briefbound-project-memory` 记现在是什么样（状态快照）；本技能记当时为什么这么定（决策时间线）。同一事件两边可各记一笔，互不替代。
- `briefbound-planning` 做方案讨论与任务拆解；方案拍板后的留痕动作归本技能。
- `briefbound-api-contract` 产出契约设计；设计构成重大决策时本技能为其落 ADR，不重复设计。
- `briefbound-readme-optimization` 面向新读者讲怎么用；ADR 面向未来维护者讲为什么。

## 致谢

记录结构参考 MADR 模板（github.com/adr/madr，MIT OR CC0-1.0），表述全部重写；取证与留痕工作流借鉴 anthropics/skills 的 doc-coauthoring（Apache-2.0）。

## 输出

```text
结论: <新落 ADR 或状态流转的条目与编号>
验证: <索引一致性、链接与四要素核对结果>
下一步建议: <一个具体动作；否则声明继续已授权工作>
```
