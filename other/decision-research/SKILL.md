---
name: decision-research
description: >
  决策调研 / Decision-Driven Research：当用户面对一个具体决策需要找信息时使用——「有没有现成方案」
  「怎么接入 X 平台」「这个技术可行吗」「业界怎么做 Y」「选 A 还是 B」「桌面端应该怎么定位」
  「高级版和基础版怎么拉开差异」「这个产品方向对不对」。
  核心行为：先框定研究层级和问题类型，再锚定决策问题，枚举竞争假设，主动找反对证据，
  用排除逻辑给出有立场的结论。支持技术选型、产品策略、商业判断、竞品定位等所有需要做决定的调研。
  可用中文唤起：「帮我调研」「有没有现成方案」「这个怎么接」「技术上可行吗」「帮我选一个」
  「这个产品方向对不对」「我们应该怎么定位」「行业怎么做」。
  与 research-topic-compiler 的边界：需要最终选择、推荐、排除理由、置信度和颠覆条件时用这个；
  如果目标是长期学习、候选池沉淀或 Research Project，用 research-topic-compiler，再把 Candidate Backlog 交回本 Skill 做最终决策。
  只有发现一个会实质改变结论、可研究且可关闭的证据 gap 时，才向 research-topic-compiler 发出精确 Return Request。
  不用于：问题还没定义清楚时（先用 ai-collaboration-calibration L4-fuzzy 脑暴）。
---

# 决策调研 Skill（decision-research）

## 中文速查

- 中文名：决策调研 / 决策驱动调研
- 英文稳定名：`decision-research`
- 分类：研究学习 / 认知与协作
- 你可以这样叫我：`帮我调研`、`有没有现成方案`、`这个怎么接`、`技术上可行吗`、`帮我选一个`、`业界怎么做`、`这个方向对不对`、`应该怎么定位`
- 适合：面对一个具体决策需要找信息——单次、即时、调研完直接进入下一步；也可消费 research-topic-compiler 产出的 Candidate Backlog / Cross-Session Handoff 来给最终推荐
- 不适合：问题还没想清楚（先用 ai-calibration L4-fuzzy 脑暴）；需要系统学习或沉淀知识库（用 research-topic-compiler）
- 与 research-topic-compiler 的一句话区别：**调研是为了做一个决定**（decision-research）vs **调研是为了建立对某个领域的认知**（research-topic-compiler）

## 核心原则

**调研是服务于决策的，不是服务于信息完整性的。**

本 Skill 拥有最终推荐、排除理由、置信度和颠覆条件，也拥有当前 `decision_question` 内为选择服务的有界取证与反证搜索；不拥有开放式知识工程，不执行已经通过 Research Return Request 明确交给 Research 的证据 gap，也不拥有方案设计、Critic clearance 或 readiness 审批。

去掉所有图表和术语，剩下的结论能不能让用户敢于立刻做决定？如果不能，问题出在信息太浅，或者决策问题本身还没定义清楚。

调研的骨架：

```
研究框定 → 决策锚定 → 假设显式化 → 竞争假设枚举 → 反对证据搜索 → 三角收敛 → 有立场结论
```

## Startup Gate

搜索前先完成四件事。详细规则按需读取 `references/research-framing-gate.md`、`references/research-map-template.md` 和 `references/mode-routing.md`。

1. 判断输入是问题、现象还是解法，并把它提升成一句 `decision_question`。
2. 判断研究层级和类型：技术选型、平台接入、可行性、产品策略、商业模型、竞品判断或行业格局。
3. 显式列出当前假设、已知事实、暗知识缺口和停止条件。
4. 输出 Research Map；如果来自 `research-topic-compiler` 的 Candidate Backlog，先纳入候选、权重和已排除项。

推荐确认句：

> 你的问题属于 [类型]，层级在 [X]。我理解核心决策是 [Y]。调研结束时需要能判断 [停止条件]。这个理解对吗？

如果问题还没定义清楚，先转 `ai-collaboration-calibration`。如果目标是长期知识沉淀或候选池，转 `research-topic-compiler`。

## Mode Routing

按问题类型只加载必要资产：

| Mode | Use When | Read |
| --- | --- | --- |
| `technical-selection` | 选库、框架、模型、服务或实现路径 | `references/modes/technical-selection.md` |
| `platform-integration` | 接 API、Bot、平台、SDK、开放能力 | `references/modes/platform-integration.md` |
| `product-strategy` | 产品定位、用户群、差异化、方向判断 | `references/modes/product-strategy.md` |
| `business-model` | 定价、版本分层、商业包装、升级触发 | `references/modes/business-model.md` |
| `competitive-decision` | 竞品证据已经收集完，需要做最终判断 | `references/channel-guide.md` + `references/conclusion-template.md` |

当用户明确需要“持续推进一个决策”“保存状态”“下一轮继续”或“更新结论”时读取 `references/decision-loop-contract.md`。Loop 只围绕同一个 decision_question 迭代；如果目标变成研究知识库，转 `research-topic-compiler`。

## Workflow

1. **Frame the decision**：完成 Startup Gate，输出 Research Map。
2. **Enumerate competing hypotheses**：至少 2 个互斥假设；不能单假设调研。
3. **Choose channels**：按 `references/channel-guide.md` 选择 3-6 个高价值渠道；动态信息必须实时核验。
4. **Search for disconfirming evidence**：对每个假设构造“如果它错了会出现什么证据”，主动找反例。
5. **Run scope drift checks**：每轮信息收集后按 `references/scope-drift-checkpoint.md` 判断是否仍在回答 Research Map 的问题。
6. **Record user corrections**：用户纠偏时按 `references/assumption-ledger.md` 记录旧假设、新 framing 和影响。
7. **Stop deliberately**：满足三角收敛、信息饱和、暗知识缺口、PoC 更便宜或 ROI 熔断时停止。
8. **Give a position**：按 `references/conclusion-template.md` 输出推荐、置信度、排除理由、前提、颠覆条件和待验证项。

## Core Loop Handoff

消费 Research Evidence Pack、精确退回一个证据 gap、把已定决策约束交给 `brainstorming`，或消费 Critic 的选择标准 gap 时，读取 `references/core-loop-decision-handoff.md`。

- 单点调用在一个 Decision outcome 后停止；只有用户或调用方已授权串联时才消费下游 handoff。
- Research return 必须同时满足 material、researchable、closable，并包含一个 gap、closure criterion、preserved items、resume point 与 effort budget；否则选择 `poc-needed`、`human-decision-required` 或 `low-roi-stop`。
- Evidence Delta 返回后只恢复原 Decision artifact 的受影响位置，不重开已确认内容。
- 交给 `brainstorming` 的是版本化 Decision 约束，不替 Maker 创建方案。
- 同一 gap 完成两轮回流后仍未关闭或缩小时，停止自动回流并进入 Human Gate。

## Evidence Rules

- 来源层级：`L1` 官方/原始资料，`L2` 独立研究/可信技术报告，`L3` 社区主流实现，`L4` 从业经验/二手摘要。
- 判断性质：`[Evidence]`、`[Local Context]`、`[Inference]`、`[Judgment]`、`[Open]`。
- 置信度高：至少 2 个独立 L1/L2 来源且没有重大反证。
- 置信度中：有 L1/L2 支撑但竞争假设未完全排除。
- 置信度低：主要来自 L3/L4 或核心假设未验证。
- 用户明确要矩阵时可以输出矩阵，但矩阵后仍要给立场。

---

## 和其他 Skill 的边界

| | ai-calibration (L4-fuzzy) | decision-research | research-topic-compiler | grill-me |
|---|---|---|---|---|
| 前提 | 问题还没定义 | 问题已定义或可快速框定，需要最终选择 | 需要长期知识沉淀或候选池 | 方案已成形 |
| 时间尺度 | 单次对话 | 单次对话 | 可跨会话 | 单次对话 |
| 输出 | 真实问题陈述 | 最终推荐 + 排除理由 + 颠覆条件 | Research Project / Candidate Backlog / handoff | 决策记录 |
| 终止条件 | Done Signal 三问 | 三角收敛 / 信息饱和 / 暗知识缺口 | 信息饱和 / 用户确认 | 关键分支已探索 |
| 新增覆盖 | — | 消费 RTC 候选池并给最终决策 | 产品决策型候选池、handoff | — |

---

## 资源指南

- Decision Research Loop 合约：`references/decision-loop-contract.md`
- Core Loop handoff：`references/core-loop-decision-handoff.md`
- 模式路由：`references/mode-routing.md`
- 技术选型：`references/modes/technical-selection.md`
- 平台接入：`references/modes/platform-integration.md`
- 产品策略：`references/modes/product-strategy.md`
- 商业模型：`references/modes/business-model.md`
- 研究框定门：`references/research-framing-gate.md`
- Research Map 模板：`references/research-map-template.md`
- 自上而下产品研究模式：`references/top-down-product-mode.md`
- 纠偏日志：`references/assumption-ledger.md`
- 范围漂移检查：`references/scope-drift-checkpoint.md`
- 调研规则详述：`references/research-rules.md`
- 渠道选择手册：`references/channel-guide.md`
- 有立场结论模板：`references/conclusion-template.md`
- 输出检查脚本：`scripts/check_decision_report.py`

## Definition of Done

调研完成需满足：

1. 研究层级和类型已通过 R00 框定
2. 决策问题已锚定，终止条件已预先定义
3. Research Map 已输出
4. 竞争假设已枚举（≥2 个）
5. 反对证据已主动搜索
6. 满足三个终止条件之一
7. 输出包含：推荐 + 置信度 + 排除理由 + 颠覆条件
8. 所有来源已标注层级（L1-L4）
9. 关键判断已标注来源性质（Evidence/Inference/Judgment/Open）
10. 如有用户纠偏，Assumption Ledger 已记录

## Evaluation

Smoke prompts:

- `有没有工具能帮我把文字转成结构化任务？`
- `微信有没有官方的 Bot API 可以接入？`
- `我们要选一个移动端推送方案，有哪些选项？`
- `技术上能不能做到实时语音转文字？`

Product strategy prompts (应触发 Top-Down Mode):

- `我们想做一个桌面端 Agent，你帮我调研一下应该怎么做。`
  期望：先识别为产品形态问题，输出 Research Map，追问产品目标和差异化假设。
- `我们要给服装 ODM 客户做本地款式资产治理，你调研一下方案。`
  期望：先上提一层——本地款式资产治理是不是更大方向中的一个能力切片。
- `我们想接 Computer Use 到桌面端里，行业上都是怎么做的？`
  期望：先区分执行能力、授权浏览器、本地工具、人审边界，不把 Computer Use 当目标。
- `高级版和基础版怎么拉开差异？`
  期望：识别为商业模型问题，从用户价值倒推，不从功能列表开始。

Non-trigger prompts:

- `帮我想想这个产品的方向对不对。`（问题未定义，应用 ai-calibration L4-fuzzy）
- `系统研究一下 AI Agent 的内存机制。`（知识沉淀，应用 research-topic-compiler）
- `拷问我的这个技术方案。`（方案已成形，应用 grill-me）
