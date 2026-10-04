---
name: ai-work-assetization-diagnoser
description: >
  AI 工作资产化诊断器 / Assetization Router：当用户提供 AI 协作会话、重复任务、prompt、工作流描述、
  团队 AI 使用场景或一次成功交付过程，并要求判断应该沉淀成 Prompt、Context Pack、Workflow、Skill、
  Loop、System，或根本不值得沉淀时使用。它只做诊断、分层和下一步资产建议，不替代具体 Skill 创建、
  PRD 起草、调研、实现或自动化执行。不用于普通事实查询、一次性文案、trace 根因分析或高责任专业判断。
---

# AI 工作资产化诊断器

## 中文速查

- 中文名：AI 工作资产化诊断器 / 资产化路由器
- 英文稳定名：`ai-work-assetization-diagnoser`
- 分类：Skill/Agent 治理
- 你可以这样叫我：`这段工作是不是值得做成 Skill`、`这个 prompt 应该沉淀成 workflow 还是 Skill`、`帮我判断该资产化到哪层`、`这个 AI 工作流要不要做成 Loop`
- 适合：判断一段可重复 AI 工作应该沉淀到哪个资产层，给出最小下一步 artifact 和验证信号。
- 不适合：直接创建 Skill、直接实现自动化系统、普通日志根因定位、一次性事实查询、没有复用价值的闲聊。

## Overview

这个 Skill 是 Router / Gate，不是执行器。它回答三个问题：

1. 这段 AI 工作是否值得沉淀。
2. 如果值得，最小有用资产层是什么。
3. 为什么不是相邻层级。

默认输出应短、可执行、有证据。不要把所有重复任务都升级成 Skill，也不要把所有自动化想法都升级成 Loop。

## Asset Layers

| Layer | Use When | Example Artifact |
| --- | --- | --- |
| Do Not Assetize | 低频、一次性、强主观、输入不可稳定复用、风险高或验收口径不存在。 | 保留聊天记录或一次性笔记。 |
| Prompt | 步骤简单，主要复用表达方式。 | Prompt template, checklist prompt. |
| Context Pack | 关键难点是资料、约束、样例和反例组织。 | Context folder, source bundle, glossary. |
| Workflow | 有稳定步骤、角色、输入输出和人工推进点。 | SOP, runbook, workflow doc. |
| Skill | 高频可复用，有明确触发语、输入、输出、边界和验收方式。 | `SKILL.md` + references/scripts. |
| Loop | 需要多轮状态、恢复、触发器、检查点、重试或人工接管。 | Loop contract, state files, update log. |
| System | 多个 Skill/Loop/Agent 组合，涉及权限、成本、审计、评估或团队级运行。 | Product/system PRD, architecture plan. |

## Workflow

1. **Identify input shape**
   - AI conversation
   - repeated manual task
   - prompt or prompt pack
   - team workflow
   - successful delivery trace
   - failed or over-engineered asset proposal

2. **Extract evidence**
   - user goal and business context
   - input materials and constraints
   - repeated steps
   - output artifact
   - human decision points
   - validation or acceptance criteria
   - frequency and reuse audience
   - state, retry, handoff, or automation needs

3. **Score only what matters**
   - repeatability
   - input stability
   - output stability
   - validation clarity
   - context dependency
   - human judgment dependency
   - failure cost
   - reuse audience

4. **Recommend one primary asset layer**
   - Give the smallest layer that would create real reuse.
   - Explain why the lower layer is insufficient.
   - Explain why the higher layer is overkill.
   - Include do-not-assetize if that is the best answer.

5. **Name the smallest next artifact**
   - Prompt: one reusable prompt with slots.
   - Context Pack: file list and required metadata.
   - Workflow: step list and handoff format.
   - Skill: trigger description, non-triggers, output contract, references.
   - Loop: state files, stop conditions, Human Gate.
   - System: PRD / architecture / eval plan before implementation.

6. **Define reuse signal**
   - What would prove this asset is worth deepening?
   - What failure signal should stop further investment?

## Output Contract

Use this structure:

```markdown
## Assetization Diagnosis

- Current shape: <conversation / prompt / context / workflow / skill candidate / loop candidate / system candidate>
- Recommended layer: <Do Not Assetize / Prompt / Context Pack / Workflow / Skill / Loop / System>
- Confidence: <High / Medium / Low>

## Evidence
- ...

## Why This Layer
- ...

## Why Not Adjacent Layers
- Lower layer is insufficient because ...
- Higher layer is overkill because ...

## Smallest Next Artifact
- ...

## Reuse Signal To Watch
- ...

## Do Not Do
- ...
```

For batch scenarios, use a compact table with columns:

- Scenario
- Current shape
- Recommended layer
- Evidence
- Smallest next artifact
- Reuse signal
- Priority

## Boundary Rules

- If the user asks to create the actual Skill after diagnosis, hand off to `skill-creator`.
- If the user asks whether an idea is a good product, use `ai-collaboration-calibration` or `decision-research`.
- If the user asks to turn a product idea into a PRD, use `prd-architect`.
- If the user asks to review an existing Skill, use `skill-reviewer` when available.
- If the user provides trace/logs and wants root cause, use a trace/debug skill, not this one.
- If the work is high responsibility, such as medical, legal, financial, safety, hiring, or compliance decisions, recommend human review and avoid closed-loop automation.

## Non-Assetization Cases

Recommend not assetizing, or only a lightweight note, when:

- The task happened once and is unlikely to recur.
- The input varies so much that templates would mislead.
- The output depends on taste or senior judgment with no stable rubric.
- The cost of a wrong answer is high and no verification exists.
- The user cannot name a reuse audience.
- A simpler checklist would solve the problem.

## Definition Of Done

- The recommendation is one primary asset layer, not a vague list.
- Adjacent layers are explicitly accepted or rejected.
- The next artifact is small enough to create in one focused pass.
- The answer includes a reuse or failure signal.
- The diagnosis does not expose private context unless the user supplied and authorized it in this run.

## Resources

- `references/asset-layer-rubric.md`：当 Prompt / Context Pack / Workflow / Skill / Loop / System 边界不清时读取。
- `scripts/check_assetization_report.py`：检查资产化诊断报告是否包含推荐层级、证据、最小下一步和复用信号。

## Evaluation

Smoke prompts:

- `这段工作是不是值得做成 Skill？`
- `这个 prompt 应该沉淀成 workflow 还是 Skill？`
- `我们连续三次做了类似 AI 协作，帮我判断该资产化到哪层。`
- `这只是一次性任务，不要过度沉淀。`

Non-trigger prompts:

- `直接帮我创建一个 Skill。`
- `看下这个 trace，定位根因。`
- `帮我写一个 PRD。`
- `查一下今天的新闻。`
