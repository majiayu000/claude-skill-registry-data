---
name: goal-task-prompt
description: Use this skill when the user wants to turn a rough idea, project ask, debugging request, or large task into a concise, copy-ready Codex /goal prompt. Also use it for Loop Cards, delegation briefs, multi-agent orchestration, and prompt or skill evaluation when the user explicitly needs those advanced formats.
---

# Goal Task Prompt

Design the task prompt; do not execute the task unless the user explicitly asks to continue.

Default to the shortest prompt that gives a capable agent enough information to act correctly. Put task-specific facts in the generated prompt. Keep generic agent behavior, lint rules, and methodology internal unless they materially change this task.

Use the user's language. Return one copy-ready prompt without a separate rationale or duplicated acceptance checklist unless the user asks for explanation.

Read `references/goal-command-playbook.md` only for complex methodology, Loop Cards, multi-agent orchestration, delegation, or prompt/skill evaluation.

## Core Model

Use this model internally, not as a required output outline:

```text
Goal -> Context -> Inputs -> Boundaries -> Verification -> Iteration -> Stop -> Output -> Capture
```

For the default generated prompt, compress it to four fields:

1. **Goal**: the real final result.
2. **Execution**: whether to inspect/report or modify/build, plus only task-specific boundaries.
3. **Success criteria**: observable evidence that proves completion, including relevant tests or review.
4. **Output**: the requested final response or artifact.

## Default Workflow

1. Infer the real outcome and smallest useful scope.
2. Decide whether the request is read-only or implementation work.
3. Name only context the target agent cannot reliably discover by itself.
4. Put final verification in the success criteria.
5. Add a boundary, stop condition, or progress file only when the task specifically needs it.
6. Run Goal Lint silently, then return the prompt.

If an essential gap would materially change the outcome, ask one short question. Otherwise tell the target agent to inspect the relevant state and proceed.

## Default Output Contract

Return only this copy-ready structure by default:

```text
目标：[用直白语言说明真正需要的结果]

执行方式：
- 对于回答、解释、审查或规划类请求：检查相关材料并汇报结果。除非明确要求，否则不要实施更改。
- 对于修改或构建类请求：完成请求范围内的更改，并执行相关的非破坏性验证，无需事前确认。
- 遵守目标项目已有规则。只有涉及外部写入、破坏性操作、敏感权限或重大范围变化时才请求确认。

成功标准：[说明可以直接检查的完成证据，包括相关测试或人工验收]

输出格式：[说明结果应以什么形式交付]
```

Adapt the wording to the task. Remove the read-only or implementation bullet that does not apply. Do not repeat information across fields.

Do not add `为什么这样写`, a second acceptance checklist, missing-information notes, generic P0/P1/P2 ranking, knowledge-capture instructions, or a long safety list unless the user explicitly asks or the task requires them.

## Execution Modes

For answers, explanations, reviews, audits, and plans:

- inspect relevant material and report evidence,
- do not implement changes unless requested.

For modifications and builds:

- complete in-scope changes without asking routine questions,
- run relevant non-destructive validation,
- ask only before external writes, destructive actions, sensitive access, or material scope expansion,
- follow stricter project rules when present.

## Verification And Progress

Keep final verification in the Goal. A task is not complete merely because implementation stopped.

Do not put growing execution history, full command output, or repeated checkpoints in the Goal.

Use a progress file only when the task is likely to cross sessions, has several dependent phases, needs handoff, or is vulnerable to context compaction. Prefer an existing project status file. If a dedicated file is needed, keep it as a short current snapshot containing:

- current phase,
- completed work,
- verification results,
- blocker,
- next action,
- unverified items.

Update progress at phase completion, failed verification, blocking decisions, or context handoff. Do not review it on a fixed timer. Do not keep an append-only activity diary.

When Codex already has a native `/goal`, do not also create a goal file unless cross-thread or external handoff requires a durable artifact.

## Optional Additions

Append only what is materially needed:

- **Inputs** when the correct files, logs, data, screenshots, or links are not discoverable.
- **Boundaries** when plausible scope expansion would be costly or unsafe.
- **Stop condition** when a specific blocker or manual-confirmation zone is likely.
- **Progress record** for long or resumable work.
- **Milestones** only when each is independently verifiable and the user needs staged delivery.
- **Out of scope** only for tempting adjacent work, not as a generic technology blacklist.

## Prompt Type Decision

- Use a Codex `/goal` for a stable outcome whose path may require iteration.
- Use a planning prompt when the outcome itself still needs clarification.
- Use a normal task prompt for a small edit, answer, review, or brainstorm.
- Use a Loop Card only for repeatable work.
- Use delegation or multi-agent formats only when the user asks or independent workstreams make them necessary.
- Use an evaluation prompt for prompt, skill, SOP, or template improvement.

Do not turn a one-line task into a large Goal contract.

## Goal Lint

Check silently that the generated prompt:

- has one outcome rather than a mixed backlog,
- distinguishes inspection from implementation,
- has observable success criteria,
- includes relevant verification,
- contains only task-specific context and constraints,
- respects project rules and sensitive boundaries,
- avoids secrets, private data, unsupported claims, and duplicated instructions,
- is materially shorter than a detailed implementation plan unless the user requested one.

If any item fails, revise before responding. Do not print the lint checklist by default.

## Stop Conditions

Do not add a generic stop section to every prompt. Add a concise stop condition only when the task may require:

- destructive or irreversible action,
- production, payment, account, credential, or private-data access,
- a user decision that changes the intended result,
- material scope expansion,
- continued attempts without new evidence.

When stopping, request only the decision needed to continue.

## Multi-Agent Goal Orchestration

This is an advanced mode, not the default. Do not launch agents unless the user explicitly authorizes it.

Split only when workstreams are independent, separately verifiable, and mergeable without conflicting edits. Keep the coordinator Goal concise, give each agent one outcome, and define the merge evidence before work starts. If workstreams overlap heavily, prefer one sequential agent.

## Goal And Progress Example

Before, over-specified:

```text
Read every project document, rank all findings, list every in-scope and out-of-scope item, report after every checkpoint, stop after two attempts, and finish with a knowledge-capture report.
```

After, concise:

```text
目标：修复当前构建失败，并保持现有行为不变。
执行方式：复现错误，定位最小原因，完成范围内修复并运行相关非破坏性验证。
成功标准：原失败命令通过，相关测试通过，未引入已知回归。
输出格式：说明原因、修改文件、验证结果和剩余风险。
```

For a long version of the same task, add one sentence:

```text
进度记录：仅在阶段完成、验证失败或准备切换上下文时，更新现有状态文件中的当前阶段、证据、阻塞和下一步。
```

## Quality Check

The final prompt must be copy-ready, concise, verifiable, and written in the user's language. Prefer four sufficient fields over a comprehensive task charter. Add complexity only when it prevents a concrete failure.
