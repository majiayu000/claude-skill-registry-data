---
name: prompting-opus-5
description: Use when adapting, migrating, or writing a prompt or agent contract that will run on Claude Opus 5 (API id claude-opus-5) — legacy Opus/Sonnet prompts, coding, refactor, review, long-context, or multi-agent prompts; tuning effort, verbosity, progress cadence, subagent fan-out, or verification instructions; or diagnosing an unexpected refusal on a permitted internal task with route and context controls before any packet rewrite.
---

# Prompting Opus 5

**Required background:** the `prompt-engineering` skill ([../prompt-engineering/SKILL.md](../prompt-engineering/SKILL.md)) owns the base task contract and its replacement patterns. This skill is the Opus-5 delta only; do not restate it. Sources and URLs: [references/official-guidance.md](references/official-guidance.md).

## Migration workflow

Compile a legacy prompt into an Opus-5 contract, in order:

1. Confirm it is a `prompt-engineering` task contract; if not, convert first. The deltas overlay a contract, they do not replace one.
2. **Delete** blanket verification, double-check, and self-correction blocks. Opus 5 self-verifies; duplicates waste tokens. **Preserve** task-specific proof (the exact command, file, or scenario that must pass) in the contract.
3. Remove forced chain-of-thought narration ("think step by step"); reasoning stays internal.
4. Set the four output controls below.
5. Add scope discipline, the subagent cap, and the correction-narration rule.
6. For a review prompt, apply review behavior.
7. Keep thinking enabled; add the disabled fallback only if the runtime forces it off.

## Output controls

- **Effort.** Defaults to `high` (API and Claude Code). `low`/`medium` often hold quality at lower cost; `xhigh` for demanding coding or agentic work. Start high, calibrate down with evals.
- **Verbosity.** Effort tunes thinking depth, not answer length; constrain visible response length explicitly.
- **Progress.** One short sentence before a tool batch; further updates only on important findings or a direction change; the final message opens with the outcome.
- **Document length.** Fit each artifact to its purpose; no filler, redundant summaries, or boilerplate.

## Scope

Narrow tasks: make routine decisions without asking; ask only when a reading is materially different; flag a better path once, then execute the requested scope. Never silently widen, narrow, or transform it.

## Subagents

Spawn only for genuinely independent, sizeable tracks. Do not fan out small tasks or spawn an agent to verify routine work.

## Review prompts

Ask for every real issue, then filter severity in a separate step. Requesting only severe or "conservative" findings suppresses useful ones.

## Unexpected refusal on a permitted task

Treat an unexpected refusal as a route-or-context defect to diagnose, not as proof that the permitted task is impossible and not as a word-filter to evade.

1. Capture the exact provider/model route, reasoning setting, request, refusal, intended outcome, and approximate context size. Do not loop the same packet.
2. Confirm the objective is actually permitted. If it is not, stop; prompt rewriting never changes the action boundary.
3. Before blaming request wording, run one context-free fixed-output control through the exact same route only when the task action boundary, policy, and spend allow that provider call. If any gate disallows it, record `control_status: NOT_CHECKED` and do not rewrite the packet on that evidence alone; inspect already-available session context or route the permitted task to another admitted reviewer. If the control also refuses, classify the incident as a route/session safeguard: stop rewriting the task, inspect always-on context for unrelated high-risk catalogs, and either trim those catalogs behind on-demand loading or switch to another admitted route. Record the resolved provider/model and reasoning setting in the receipt; an agent label alone is not route evidence.
4. Only when the control passes but the task refuses, minimize the packet to the owned target, relevant artifacts, allowed operations, and expected evidence. Remove unrelated transcripts, speculative branches, and domain material supplied by the packet.
5. Replace colorful or metaphorical wording with the literal engineering operation it was standing in for: compare, trace, reproduce, run a named negative case, classify, or report. This is semantic correction, not synonym rotation.
6. State ownership or authorization once when relevant, then state the operational boundary: for example, read-only review, no provider calls, or no external action.
7. Retry once with the corrected packet. If it still refuses, capture the result and route the permitted work to another admitted reviewer rather than escalating wording tricks.

Do not maintain a trigger-word blacklist. A bare word list is brittle and destroys task meaning. Never use encoding, euphemisms, misspellings, or synonym rotation to conceal an impermissible objective.

Example review packet:

```markdown
## Objective
Review PR #33 in our repository for contradictions between `CLAUDE.md` and `_SYSTEM/yuri-origin.md`.

## Boundary
Read-only. Inspect only the committed diff, the two named files, and PR metadata. Make no repository or external changes.

## Evidence
For each finding, cite the file and line range. Return `CLEAR` if no contradiction is found; otherwise return the smallest correction.
```

## Thinking-disabled fallback

Prefer `low` effort over disabling thinking. If a runtime forces it off: allow one brief pre-tool sentence, require admitting when no available tool fits, and forbid emitting internal or system XML tags.

## Opus-5 contract overlay

Add to the `prompt-engineering` template:

```markdown
## Effort
[high | xhigh for demanding coding/agentic | low or medium to cut cost]

## Response Controls
- Visible length: [explicit bound]
- Progress: pre-tool sentence; updates on findings or direction changes; outcome-first final
- Artifact length: [purpose-fit; no filler]

## Scope Discipline
- Routine: decide. Materially different: ask. Better path: flag once, then execute requested scope.

## Subagents
- [independent sizeable tracks only, or none]

## Corrections
- Narrate only corrections that change the user's code, conclusions, or decisions.

## Proof Requirements
- [task-specific checks only; no blanket self-verification]
```

## Anti-patterns

- Blanket "verify / double-check your work" blocks; Opus 5 already self-verifies.
- Forced "think step by step" narration.
- Unconditional fan-out, or spawning agents to verify routine work.
- Asking a reviewer for only severe or critical findings.
- Relying on effort to shorten the visible answer.
- Disabling thinking as a first resort.
- Filler, boilerplate, or redundant closing summaries.
- Silently widening or narrowing task scope.
- Narrating trivial corrections.

## Model prompting is not fleet admission

Official Opus 5 availability does not make any local route executable. Prompt design and dispatch eligibility are separate: the local provider route registry plus the latest canary decide whether `claude-opus-5` can run here. Tuning a prompt never implies a runnable local route.
