---
name: reflection
description: Use when the user invokes $reflection or asks for an independent, concise post-task audit of whether Codex overthought a completed request, used too many tools, or should persist a project-scoped workflow lesson.
---

# Reflection

Audit the observable execution of completed tasks. Optimize for lower latency and fewer
tool calls without removing work required for correctness, safety, or applicable
instructions.

## Resolve the task

- With no explicit scope, audit the substantive user request immediately before the
  reflection request and the complete Codex execution that answered it.
- Treat clarifications and corrections made before that answer as part of the same task.
- If the user names tasks or asks for the last N tasks, audit exactly that scope.
- Do not count the reflection request itself as part of the task.
- If no completed task is available, say so. Do not invent a trace.

## Gather evidence

Use the inherited conversation and tool trace first. Review only observable evidence:
requests, commentary, tool calls and outputs, file changes, checks, errors, retries, and
the final answer. Never request or reconstruct hidden chain-of-thought.

Do not open the raw session trace by default. Inspect it only when the user requests exact
timing or tool counts, or when a material claim cannot be resolved from the inherited
trace. Resolve the current session unambiguously; never assume the newest session file is
the right one. If it cannot be resolved, mark the exact measurement as unknown.

## Delegate the audit

Spawn exactly one independent subagent with:

- model: `gpt-5.6-sol`
- reasoning effort: `medium`
- the smallest inherited turn range that contains the full task trace
- a prompt containing the scope, raw observable evidence, and the report contract below

Do not give the subagent the main agent's diagnosis or suggested findings.

Tell the subagent to:

- remain read-only and make no external changes;
- spawn no further agents;
- avoid tools unless one targeted read is essential to interpret evidence already in the
  trace;
- compare effort with task complexity;
- distinguish avoidable work from checks required by safety, correctness, user
  instructions, `AGENTS.md`, or an active skill;
- identify root causes rather than isolated symptoms;
- answer in the user's language.

If an independent subagent is unavailable, fail closed and explain that an independent
reflection could not be produced. Do not substitute the main agent's self-review.

## Return the report

Return the subagent's findings after checking only for unsupported claims, secrets, and
scope violations. Do not run a second audit.

Keep the report to roughly 300 to 500 Chinese characters, or comparable length in another
language, using this structure:

```markdown
## 结论

合理 | 轻度过度 | 严重过度。One sentence relating task complexity to execution cost.

## 核心浪费

- Observable evidence -> root cause -> shortest better path.
```

Include at most three waste findings. Then add:

```markdown
## 不可削减项

- Work that was justified by correctness, safety, or binding instructions.

## 可固化规则

- 当 <trigger> 时，应 <minimal action>；除非 <exception>。
```

Include at most three persistence candidates. Do not use numeric scores. If the trace
contains no material inefficiency:

- write `未发现核心浪费` under `核心浪费`;
- write `未发现值得固化的问题` under `可固化规则`;
- do not turn successful behavior into generic persistence candidates.

## Persist only on explicit request

`$reflection` is read-only. Do not change memory, skills, `AGENTS.md`, configuration, or
project files unless the user explicitly asks to persist or promote a selected finding.

### Project memory

When the user explicitly asks to persist a finding:

1. Resolve the exact project root with `git rev-parse --show-toplevel`. If there is no
   project root, ask for the intended scope before writing.
2. Search the current ARC Rule/Learning state, memory registry, and pending ad-hoc notes
   once for an equivalent rule.
   If one already covers it, report that and do not duplicate it.
3. If the project has a versioned `.research/VERSION` and one committed Project,
   call the installed `research-op/scripts/record_project_learning.py` helper with
   the selected observation, candidate rule, applicable ARC actions, owning skills,
   and package scope. This writes a non-binding ARC Learning with a
   content-addressed NOTE EvidenceRef. Do not also write an ad-hoc memory note.
4. Otherwise, write one small update note named `<timestamp>-<short-slug>.md`
   through the supported memory-update mechanism. On the local Codex filesystem,
   use `${CODEX_HOME:-$HOME/.codex}/memories/extensions/ad_hoc/notes/`.
5. Bind an ad-hoc fallback rule to the exact project root:

```markdown
# Project reflection rule: <short name>

scope: <project and task class>
applies_to: cwd=<absolute git root>
observed_pattern: <one sentence>
rule: When <trigger>, <minimal action>; unless <exception>.
evidence: <date and short task description>
```

Persist only the selected reusable rule. Do not store the full report, raw transcript,
secrets, volatile metrics, or one-off frustration. Never hand-edit generated memory
summaries, registries, ARC state, or projections. Report the ARC Learning id and note
reference, or the ad-hoc note path. Do not claim that background consolidation has
completed unless it was verified.

### Stronger enforcement

Project memory is a recall layer. If the same problem recurs or the user explicitly asks
to enforce it, recommend the narrowest durable owner:

- nearest applicable `AGENTS.md` for mandatory project behavior;
- the owning skill for a reusable workflow rule;
- an explicitly admitted ARC Project Rule for governed cross-session context;
- a test or hook for deterministic enforcement.

Do not modify any of these surfaces without an explicit user request.
