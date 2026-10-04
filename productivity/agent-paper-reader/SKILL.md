---
name: agent-paper-reader
description: Use when reading, explaining, reviewing, comparing, or extending one or more AI agent, LLM agent, tool-use, planning, memory, multi-agent, RAG-agent, web-agent, GUI-agent, coding-agent, GUI automation, or agent benchmark papers. Focus on problem framing, prior-method gaps, agent-loop mechanisms, evaluation credibility, limitations, reproducibility, cross-paper comparison, and follow-up research ideas.
---

# Agent Paper Reader

Use this skill to turn AI agent papers into clear research judgment, not just summaries.

## Language Policy

Default to Chinese when the user writes in Chinese or the source task is for Chinese research notes. Keep paper titles, method names, benchmarks, datasets, model names, and short technical terms in English when that is clearer.

Do not output English section headings by default for Chinese users. Use headings such as:

- 阅读假设
- 这篇论文解决什么问题
- 已有方法为什么不够
- 作者怎么解决
- 优势与证据
- 缺点与隐含假设
- 我们能在它基础上做什么
- 一句话判断

Only use English as the main output language when the user asks in English or explicitly requests English notes.

The default reading frame is:

1. 这篇论文解决什么问题？
2. 已有方法为什么不够？
3. 这篇论文是怎么解决的？
4. 它的方法有什么优势，证据是否充分？
5. 明显或潜在的缺点是什么？
6. 我们能在它基础上做什么？

## Depth Policy

Default to a detailed explanation unless the user explicitly asks for "quick", "brief", "overview", "速览", or "简单总结".

- Single paper: use detailed mode by default.
- 2-3 papers: use `deep-per-paper` by default, then add a shorter cross-paper synthesis.
- 4-6 papers: use `balanced` mode by default.
- More than 6 papers: use cluster/triage mode unless the user asks for full detail.

Detailed mode means the answer should teach the paper, not only label it. For each important mechanism, explain:

- 它是什么。
- 为什么需要它。
- 它在 agent loop 的哪个位置起作用。
- 论文用什么证据证明它有用。
- 它没有证明什么。
- 如果我们复现，最小实现要做哪些模块。

Read `references/detailed-reading.md` when the user asks for detailed interpretation, when the paper is important, or when the output feels too shallow.

## Source Handling

If the paper is provided as PDF, LaTeX, DOCX, screenshots, or extracted text, first obtain reliable paper content with the appropriate file-reading skill or tool. For PDFs, prefer page/figure/table locators when possible. Do not rely only on the abstract if the full paper is available.

Use external search only when the user asks for latest context, related work beyond the paper, repository status, citations, or current benchmark rankings.

## Paper Type

Classify the paper before explaining details:

- Method paper: new agent mechanism, algorithm, prompting policy, training method, or search strategy.
- System paper: multiple components assembled into an agent framework or workflow.
- Benchmark paper: dataset, task suite, environment, metric, or evaluation protocol.
- Analysis paper: failure modes, scaling behavior, tool-use behavior, or capability diagnosis.
- Survey paper: taxonomy and field map.
- Position paper: claims or agenda with limited direct evidence.

Read `references/agent-taxonomy.md` when the agent type or component structure is unclear.

## Single-Paper Output Contract

For a normal paper-reading request, produce this structure in the user's language:

```text
阅读假设
- 论文类型、阅读目标、使用了哪些证据来源。

1. 这篇论文解决什么问题
- 它解决的是哪个 agent 问题？
- 任务设置、输入、输出、环境、成功标准是什么？
- 这个问题为什么重要？

2. 已有方法为什么不够
- 作者认为旧方法哪里不够？
- 这个不足是真问题、窄问题、被夸大的问题，还是只在本文设定下成立？

3. 作者怎么解决
- 用直白语言解释核心想法。
- 拆成 agent loop：
  Task/Input -> State/Memory -> Planner/Reasoner -> Tool/Action -> Observation -> Critic/Reflection -> Next step/Final answer
- 找出让论文成立的最小关键机制。

4. 优势与证据
- 作者声称的方法优势是什么？
- 哪些实验、图表、表格或消融支持这些 claim？
- 证据没有证明什么？

5. 缺点与隐含假设
- 作者明确承认的局限。
- 关于模型、工具、prompt、环境、数据、benchmark、成本或用户行为的隐含假设。
- 失败模式和复现风险。

6. 我们能在它基础上做什么
- 直接改进方法本身。
- 迁移到新任务或新领域。
- 设计更严格的评测或消融。
- 组合进实际 agent 系统。
- 最小复现版本和第一组实验。

一句话判断
- 一段话说明这篇论文是否重要、可信、可复用、值得继续跟进。
```

Do not force every sub-bullet when the paper is short or the user asks for a concise answer. Preserve the six top-level questions unless the user requests another format. In detailed mode, each of the six sections should include explanation, evidence, and interpretation rather than only bullets.

## Multi-Paper Comparison Mode

When the user provides, names, or asks about multiple agent papers, do not only summarize them one by one and do not skip single-paper analysis. First identify the comparison goal:

- Field orientation: understand a topic or literature cluster.
- Method comparison: decide which mechanism is stronger or more reusable.
- Research planning: find gaps and follow-up ideas.
- Reproduction planning: choose which paper to implement first.
- Evaluation audit: judge which claims are best supported.

Use one of three depth modes:

- `deep-per-paper` default for 2-3 papers: each paper gets a detailed single-paper analysis before the cross-paper comparison.
- `balanced` default for 4-6 papers: each paper gets a compact but substantive mini-review before the cross-paper comparison.
- `quick-scan`: only use one-line verdicts and a comparison table when the user explicitly asks for a quick overview.

For the default `deep-per-paper` mode with 2-3 papers, produce this structure:

```text
比较假设
- 比较了哪些论文、使用了哪些证据、比较目标是什么。

1. 逐篇深读
对每篇论文分别使用单篇六问结构：
- 这篇论文解决什么问题？
- 已有方法为什么不够？
- 作者怎么解决？核心机制和 agent loop 是什么？
- 优势与证据：实验/图表/消融分别证明了什么？
- 缺点与隐含假设：哪些 claim 还没有被证明？
- 我们能在它基础上做什么：复现 MVP、改进点、实验设计。

2. 横向综合
- 共同研究问题。
- 方法差异表。
- 证据与评测对比。
- 互补与冲突。
- 研究空白。
- 下一步行动。

总判断
- 一段话综合说明这组论文真正教会了我们什么。
```

For `balanced` mode with 4-6 papers, produce this structure:

```text
比较假设
- 比较了哪些论文、使用了哪些证据、比较目标是什么。

1. 每篇论文的 mini-review
对每篇论文分别保留这 5 项，不要只给一句话：
- 问题：它要解决什么？
- 缺口：已有方法为什么不够？
- 方法：核心机制是什么？
- 证据：实验或论证支撑了什么，没有支撑什么？
- 可延展点：我们能基于它做什么？

2. 共同研究问题
- 这些论文共同面对哪个 agent 问题？
- 它们的问题定义有什么差异？

3. 方法差异表
- 比较 agent 类型、核心机制、agent loop、memory、planning、tools、verifier、训练/推理设置和人类参与。

4. 证据与评测对比
- 比较 benchmarks、baselines、ablations、成本报告、失败分析和可复现性。
- 哪篇证据最强？哪篇证据最弱？

5. 互补与冲突
- 哪些想法可以组合？
- 哪些假设或结论互相冲突？
- 哪些论文解决的是同一个大问题的不同部分？

6. 研究空白
- 把它们合起来看，仍然没有解决什么？
- 哪些是方法层、评测层、工程层或理论层 gap？

7. 下一步行动
- 最值得深读哪篇？
- 最值得先复现哪篇？
- 最值得做的 extension idea 是什么？按可行性和研究价值排序。

总判断
- 一段话综合说明这组论文真正教会了我们什么。
```

Read `references/multi-paper-comparison.md` for detailed comparison patterns and table fields.

## Agent-Specific Reading Rules

- Distinguish agent capability from LLM capability. If the gain may come from a stronger backbone model, better prompt, more tool calls, or higher cost, say so.
- Separate mechanism from packaging. Do not treat a renamed workflow as a new algorithm unless the paper provides a real mechanism or evidence.
- For system papers, identify components, data flow, control flow, state, stopping condition, and where errors enter the loop.
- For benchmark papers, focus on task validity, metric design, leakage risk, baseline fairness, and whether the benchmark predicts real-world agent usefulness.
- For coding, web, GUI, or tool-use agents, check environment determinism, sandboxing, tool schema, observation representation, action space, and evaluator reliability.
- For multi-agent papers, check whether multiple agents provide measurable benefit over one agent with equivalent context, calls, and budget.

Read `references/evaluation-audit.md` for detailed experiment and benchmark checks.
Read `references/detailed-reading.md` when the answer needs deeper explanation or when comparing 2-3 papers.
Read `references/reproduction-checklist.md` when the user asks whether the paper can be implemented or reproduced.
Read `references/extension-patterns.md` when the user asks what research or product work can be built on top of the paper.
Read `references/multi-paper-comparison.md` when the user provides multiple papers or asks how papers relate.

## Evidence Discipline

- Cite paper evidence with section names, page numbers, figure/table IDs, algorithm IDs, equations, or appendix references when available.
- Clearly separate: paper says, evidence shows, and my interpretation.
- Do not claim state of the art, generality, open-source availability, statistical significance, or reproducibility unless the paper supports it.
- If the paper omits prompts, code, hyperparameters, tool definitions, or evaluation details, treat that as a substantive limitation for agent papers.

## Failure Recovery

If the answer feels too generic, revise by adding:

- A deeper background bridge before the method.
- A concrete agent-loop diagram in text.
- A claim-evidence table.
- A figure/table explanation section.
- A baseline fairness audit.
- A reproduction MVP.
- A cross-paper comparison table.
- Three follow-up ideas ranked by feasibility and research value.
