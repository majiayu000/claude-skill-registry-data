---
name: evolution-engine
description: 将 .codex/evolution/signals.local.jsonl 或兼容旧队列中的纠偏信号整理成需要用户批准的 harness 演进提案。用于会话开始、用户反复纠正之后，或规则/技能显得陈旧、重复、缺失时。
---

# 演进引擎

把纠偏信号转化为精确提案，用于改进或退役 harness 规则。

## 何时使用

当 `.codex/evolution/signals.local.jsonl` 或兼容旧队列 `.codex/evolution/signals.jsonl` 中存在待处理信号、用户要求改进工作流，或重复失败表明某条规则缺失/陈旧时使用此技能。

不要直接应用变更。所有提案都需要用户批准。

## 必要输入

- `.codex/evolution/signals.local.jsonl`（本地纠偏信号，默认是脱敏元数据）
- `.codex/evolution/signals.jsonl`（兼容旧队列或脱敏样例）
- `.codex/evolution/proposals.md`
- `AGENTS.md`
- Relevant `.agents/skills/*/SKILL.md`
- 当信号涉及确定性门禁或 sub-agent 行为时，读取相关 `.codex/hooks.json` 或 `.codex/agents/*.toml`

## 原则

- 提出能防止失败的最小规则变更。
- 添加新规则前，优先考虑强化、合并或退役已有规则。
- 区分通用 harness 经验和项目特定偏好。
- 将可复用的一般行为放入 `AGENTS.md` 或技能；将仅属于项目的事实放入项目文档，而不是框架。
- 规则可以双向调整：添加有用约束，也可以退役过时或重复的约束。
- 保留用户决策权。每个提案在编辑文件前都要请求批准。
- 如果信号中没有原始 `text` 字段，只能基于摘要、hash、时间和当前可见上下文提出提案；不要编造用户原话。

## 验收标准

演进提案满足以下条件时才可接受：

- 引用触发提案的信号、摘要或脱敏证据。
- 指明精确目标文件或技能。
- 说明变更类型是 add、edit、retire 还是 new-skill。
- 解释它能防止的失败，或能降低的规则负担。
- 无需重新解释整段对话即可执行。

## 产出

按 `.codex/EVOLUTION.md` 定义的格式更新或起草 `.codex/evolution/proposals.md` 条目。

用户批准后，只应用已批准的提案，并移除已消费的信号。如果用户拒绝某个提案，除非用户要求保留，否则移除该提案及其已消费信号。
