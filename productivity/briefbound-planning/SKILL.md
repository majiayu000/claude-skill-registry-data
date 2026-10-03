---
name: briefbound-planning
description: "Use when aligned requirements need a persistent or reviewable implementation plan, including a compact task graph only when independent deliverables, owners, dependencies, risk gates, or verification contracts make splitting valuable."
license: MIT
---

# Briefbound 实施规划

## 目标

把已对齐需求整理成最小可实施方案。规划/任务图只防具体风险；可直接验证的任务留给 owner。

## Briefbound task contract

- Context Boundary: 已确认意图、相关代码/文档/测试、owning surface、保护边界、已有决策和会改变方案的外部证据。
- Output Contract: 推荐实施路径、影响面、顺序、风险决策、验证策略，以及必要时同一方案内的最小任务图。
- Allowed Action: 只读分析与方案编写；不修改业务代码，不扩大用户范围，不替专项 owner 执行。
- Success Evidence: 方案能映射到具体文件、行为、依赖和验证，且下一执行者无需重新猜测关键取舍。
- Stop Condition: 需求仍有高影响分叉、owning surface 不清、关键证据缺失、高风险动作未确认或方案不能安全实施。
- Route Out: 当前 owner 或专项 owner 直接实施、`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文，完成只报状态、产出、证据和剩余风险；代码、命令、路径、错误原文、API/协议、skill 名和枚举保留原样；Route Out 仅以 Briefbound task contract 为准；有自然闸门时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。

## 进入闸门

只在规划 artifact 会被审阅、复用、交接或防止具体错误时进入本 skill，例如：

- 存在会改变行为、架构、兼容性或成本的真实设计选择；
- 涉及跨模块契约、状态迁移、数据、权限、安全、发布或回滚顺序；
- 需要多个 owner、多人/agent 或跨会话协作；
- 用户明确要求先看方案。

以下情况不进入：明确机械修改、单一 owning surface、低风险可逆修复、当前 owner 已能直接实施和验证。

## 规划方法

1. 继承 Briefbound Router 的可观察结果、非目标、约束和成功证据，不重新发明需求。
2. 只读检查会改变方案的文件、接口、状态、测试、日志和项目规则。
3. 先查项目内和平台原生；新能力没有同样实现时用 `briefbound-feature-reuse-research` 做 QUICK，已有模式不进入。
4. 选择最小充分路径，说明影响文件、关键行为/数据流、实施顺序、保护边界和验证方式。
5. 只有 Briefbound Router 判为 `PROFILE` 才携带主指标、负载、baseline/测量和停止目标；`FAST/CHECK` 不增加性能章节。
6. 只有真实取舍才给 2-3 个方案；否则给一个推荐路径。
7. 内部从 1-3 个最相关视角检查需求覆盖、实施可行性、验证和风险。没有 finding 不输出矩阵；发现缺口直接修订方案。
8. 根据剩余工作选择 `DIRECT_IMPLEMENTATION`、`COMPACT_PLAN`、`TASK_GRAPH` 或 `BLOCKED`；不要再增加一个仅重复拆分判定的流程阶段。

## 路由判定

默认 `DIRECT_IMPLEMENTATION`；需要持久方案但无需真实拆分时使用 `COMPACT_PLAN`。满足以下条件即可由当前 owner 连续实施和验证：

- 一个主题、一个主要 owner，能放入同一推理上下文；
- 顺序可以在内部维护，不需要独立交付或逐项用户验收；
- 风险和验证可以由同一执行契约覆盖。

只有任一条件成立才在当前方案内使用 `TASK_GRAPH`：

- 存在多个独立交付物或 owner；
- 有真实先后依赖，后续任务必须消费前一任务的 artifact；
- 某个高风险步骤需要独立验收、回滚或权限闸门；
- 需要并行、分 PR、跨会话交接，或不同任务需要不同验证契约；
- 用户明确要求拆分。

多个文件、较长描述、同机制机械替换、需要测试或普通跨模块修改，本身不触发拆分。`NO_SPLIT` 是 Briefbound Router/Planning 的内部结论，不需要独立 skill 来证明无需拆分。

## TASK_GRAPH 模式

任务图与实施方案一次完成：

- 一个任务只对应一个独立交付物、owner、依赖 artifact、风险闸门或验证契约；测试、文档和配置并入所属功能任务。
- 共享写入面、顺序依赖或共享验证保持串行；只有范围和证据真正独立才并行。
- Critical Path 只保留完成目标必需的任务；可选优化进入 Deferred，不生成当前任务卡。
- 每个任务自行选择 `SIMPLE` 或 `BDD_TDD`。只有确定性行为存在重大回归、状态、数据、权限、迁移或公共契约风险时才使用 `briefbound-bdd-tdd-development`。
- 实验 metric lane 路由 `briefbound-score-loop`；metric 未提升不等于 TDD RED。
- 默认连续执行 Critical Path，已有执行许可时不逐任务询问。

紧凑任务卡只保留会被执行者消费的字段：

```text
Task N: <可观察产出>
- Owner/Boundary:
- Dependency:
- Mode: SIMPLE / BDD_TDD
- Verification/Stop:
```

## 输出

默认使用紧凑方案：

```text
实施方案:
- 目标与范围:
- 推荐路径:
- 影响面与保护边界:
- 关键顺序/依赖:
- 风险决策:
- 验证与成功证据:
- 模式: DIRECT_IMPLEMENTATION / COMPACT_PLAN / TASK_GRAPH / BLOCKED
- 路由原因:
下一步建议: <由当前 owner 直接连续实施，或处理阻塞>
```

`TASK_GRAPH` 时在紧凑方案后追加拆分理由、Critical Path、并行/串行边界和必要任务卡，不重复目标、风险或验证章节。

只有跨会话、正式审阅或高风险方案才增加：备选路径、复用决策、假设、回滚、详细影响面和 ledger 增量。不要输出“无新增影响面”“无真实缺口”等占位式自审字段。

## 高风险补强

权限、安全、删除、迁移、发布、公共 API 或难回滚变更必须明确：受影响对象、兼容/迁移策略、失败检测、回滚路径和授权闸门。只有这些证据仍有缺口时才读取 `references/plan-document-reviewer-prompt.md` 做专项审查。

## 延续

用户原始目标含执行许可且没有自然闸门时，方案完成后直接按推荐路由推进，不再询问下一阶段。

只有跨会话、正式交接、Deferred 项或高风险决策需要持久状态时才更新 Workflow Ledger；普通规划把必要上下文放进紧凑方案即可。
