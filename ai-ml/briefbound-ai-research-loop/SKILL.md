---
name: briefbound-ai-research-loop
description: "Use when AI/ML research engineering needs baseline reproduction, hypothesis-driven experiments, ablations, evaluation design, findings synthesis, research direction selection, plateau recovery, or a reproducible loop from a paper/repository/research question to evidence-backed results, or coordinating cross-stage research competitions and benchmarks."
license: MIT
---

# AI 研究工程循环

## 目标

把 AI 研究从“不断尝试代码”变成两个相互连接的轻量循环：

```text
内层：可信 baseline -> 可证伪假设 -> 最小实验 -> 评估 -> 接受/拒绝/保留
外层：汇总多轮证据 -> 提炼规律 -> 更新假设组合 -> 继续/分支/转向/停止
```

本 skill 是 AI 研究工程的主 owner。`briefbound-score-loop` 只承接一条可量化实验 lane；跨阶段竞赛/benchmark 按需读 [竞赛阶段参考](references/competition-lifecycle.md)。

## Briefbound task contract

- Context Boundary: 研究问题、代码和数据来源、active baseline、评价协议、允许修改面、计算预算、实验记录和当前证据。
- Output Contract: baseline 复现结论、假设组合、实验 lane、证据综合、研究方向决策或可复现交接。
- Allowed Action: 在已锁定的可编辑面和预算内复现、修改、运行、评估和记录；不静默改变数据划分、metric、baseline 或研究目标。
- Success Evidence: 可复现命令、baseline 指纹、metric 与方差、diff/config、实验 artifact、对照/消融结果以及有来源的研究结论。
- Stop Condition: baseline 不可信、评价协议漂移、数据泄漏、预算或权限不足、结果不可复现、关键假设无法区分，或继续实验已无信息价值。
- Route Out: `briefbound-score-loop`、`briefbound-feature-reuse-research`、`briefbound-bug-review`、`briefbound-research-rigor-review`、`briefbound-development-cleanup`、完成交接或 BLOCKED。
- Support 图解：研究汇报复杂时自动加载 `briefbound-diagram-design` 配图（不夺所有权）；短状态不配图。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文，完成只报状态、产出、证据和剩余风险；代码、命令、路径、错误原文、API/协议、skill 名和枚举保留原样；Route Out 仅以 Briefbound task contract 为准，末行 `下一步建议: <一个具体动作>`，且限于决策类建议（推荐方向、优先级或需拍板的选项），不把可自行完成的执行步骤包装成建议交回。

## 所有权判断

- 用户要推进一个 AI/ML 研究问题、复现论文、做消融或从多轮实验中决定方向：本 skill 主责。
- 用户已经给出明确 baseline、metric 和单个低成本候选：本 owner 可直接比较；只有反复晋升、榜单反馈或持久 score lane 才路由 `briefbound-score-loop`。
- 主要问题是训练脚本、metric、数据 schema、seed、shape、NaN 或环境的确定性故障：临时路由 `briefbound-bug-review`，修复后返回研究循环。
- 跨阶段竞赛或 benchmark：读取 [竞赛阶段参考](references/competition-lifecycle.md)，统筹规则、数据、证据与提交；单阶段仍由最具体 owner 执行。纯工程问题不启动研究实验。
- 需要搜索论文、仓库、模型或可复用实现且结果会改变方案：使用 `briefbound-feature-reuse-research`；研究 owner 保留方向决策权。

## 启动快照

先从仓库、论文、日志和配置读取已有事实，只补会改变研究决策的缺口：

- 研究问题与可观察成功标准；
- baseline 来源、版本、命令和已知结果；
- 数据版本、split、metric、seed 与评估预算；
- 可编辑面、保护面和算力/时间限制；
- 已尝试方向、失败证据和当前最可信结论。

缺少正式工件时可先运行可逆 probe，不因模板不全阻塞探索。只有 baseline、metric 或数据边界不清会让实验失去解释性时才暂停询问。

## 自适应流程

按当前研究不确定性选择最低充分重量：

- `QUICK`：可信 baseline 上的 1-2 个低成本假设；内部维护短记录，直接实验和汇报。
- `STANDARD`：需要多轮消融、多个候选或跨会话延续；维护紧凑研究契约和 append-only 实验记录。
- `DEEP`：高成本训练、结论将用于论文/发布、数据或评价风险高；增加协议冻结、复现检查、严谨性审查和明确停止预算。

不按文件数或描述长度升级。不强制每轮新建 worktree、派子代理、写规划文档或使用 BDD/TDD。并行且会相互污染的实验才隔离工作区。

## Baseline Gate

研究实验开始前确认：

1. baseline 能在当前环境运行，或已明确记录不可复现原因；
2. 代码、数据、配置、依赖和评价命令可定位；
3. 结果与已知值的偏差有解释或被标记为风险；
4. 后续候选使用同一评价协议，除非研究目标就是改变协议。

baseline 未通过时，当前产出是复现诊断，不把候选分数解释为研究结论。

## 内层实验循环

每条 lane 只要求一个能区分结果的主假设：

1. 写出机制、预期信号和最早否证条件。
2. 先找项目内复用；外部候选可能改变实现时再研究。
3. 选择能推翻或支持假设的最小充分 evaluation。
4. 可在当前上下文完成的简单比较直接执行；反复晋升、leaderboard 或持久 lane 才交给 `briefbound-score-loop`。
5. 区分 metric 结果、实现故障、环境故障和评价设计故障。
6. 保留失败实验的差异、命令和教训，不用 TDD RED/GREEN 描述实验结果。

一次可顺序完成的实验不拆任务。只有独立假设、写入边界和资源允许时才并行。

## 外层综合与转向

出现以下任一信号时，从单次分数跳到证据综合：

- 完成一组相关实验或关键消融；
- 连续候选没有信息增益；
- 结果相互矛盾或对 seed/split/规模敏感；
- 当前解释无法预测下一结果；
- 准备晋升 baseline、形成 claim 或投入高成本训练。

综合时回答：哪些机制得到支持、哪些被否证、哪些仍不可区分；结果适用范围是什么；下一实验能减少哪项关键不确定性。然后只选一个决策：

- `CONTINUE`：同一方向仍有高信息价值实验；
- `BRANCH`：两个独立解释都值得有界验证；
- `PIVOT`：当前假设族收益低，切换机制或表示；
- `CONSOLIDATE`：补复现、消融、统计和 artifact；
- `STOP`：目标已满足、预算到达或没有合理的新变量。

重要 baseline 晋升、论文级结论或反直觉结果先进入 `briefbound-research-rigor-review`。普通失败 lane 不增加正式审查。

## 证据纪律

- 区分观测、解释和推测，不把相关性写成机制证明。
- 保留 negative result，但压缩重复失败；记录可复用 lesson 和触发条件。
- 指标提升必须关联 baseline、数据、协议、seed 和 artifact；不能只引用聊天结论。
- smoke/proxy 用于淘汰和排序，不替代目标评估。
- 外部论文或仓库只提供先验，当前项目证据决定是否晋升。
- 不运行无限循环；每轮必须受实验数量、时间、算力或信息增益停止条件约束。

## 输出与延续

用户可见输出默认中文。普通一轮只报告：当前判断、关键证据、决策、下一实验；不展示完整内部账本。

跨会话、高成本或需要交接时，读取 [research-contract.md](references/research-contract.md) 并维护最小契约。目标未变时，用户说“继续”就从 active baseline、未决假设和推荐实验续接，不重开需求对齐。

正文末尾输出：`下一步建议: <信息价值最高的方向或优先实验>`。
