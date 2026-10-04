---
name: subagents
description: >
  Subagent spawning gates. MANDATORY before any spawn, any large
  context-gathering scan (codebase, DB, docs, memories), or any work
  splittable into parallel independent tasks.
---

## Required `<project-root>/docs` reads

Read these project-root spec files before spawning any subagent (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/code-navigation.md`

Discover profiles through the tool's native mechanism. Don't assume a fixed list or path.

## Dispatch Rationales

Spawn a subagent **only** when at least one holds. First two are strict — when in doubt, stay inline.

| Rationale | When to delegate |
|-----------|------------------|
| Parallel time win | **≥3 independent workstreams**, no shared writes. Below 3, coordination overhead eats the gain. |
| Context offloading | Task demands **project scanning** whose raw output is **verifiably large** (state the estimated token/line count before dispatch) AND the parent needs only a distilled brief, never the raw bytes. Speculative "might bloat" is not a rationale. |
| Explicit user request | User asks to spawn / delegate / parallelize. Honor even when neither gate fires. |

**Default to inline.**

## Pre-Spawn Checklist (mandatory, before every dispatch)

Before spawning, fill this inline in the reply. Any missing or "N/A" answer → stay inline.

1. **Rationale** — which of the three gates fires? (parallel-time-win / context-offloading / explicit-user-request). State it.
2. **Parallelism** — if parallel-time-win: list the ≥3 independent workstreams and confirm no shared writes.
3. **Offload size** — if context-offloading: state the estimated token/line count of the raw output and confirm the parent only needs the distilled brief.
4. **Profile** — name the subagent profile and confirm it matches the task shape (scout ≠ strong model, synthesis ≠ fast model).
5. **Foreground/background** — foreground by default; background only if all three background conditions hold (state them).

If you cannot fill all five, do not spawn. Do the work inline.

## Do NOT spawn for

- Anything answerable from context already in this session.
- A single file edit, single symbol lookup, or known file path + line range.
- A bounded next step where the parent holds all inputs.
- "Just in case" parallelism with <3 truly independent streams.
- Avoiding a thinking step you'd rather offload.
- **Invoking a skill workflow** (commit, push, PR-create, ship-changes, branch creation, etc.). Skills run inline in the parent unless a dispatch rationale above independently fires. The existence of the `spawn` skill is a mechanism, not a rationale — spawning a subagent *to invoke a skill* is the most common anti-pattern; invoke the skill inline instead.

## Foreground Preference

**Default to foreground.** Background subagents have reduced capabilities: unapproved tools auto-denied, `exec` unavailable, no new permission prompts. They often fail silently on tasks requiring tool approval.

Use background **only** when all hold:
- ≥3 truly independent workstreams benefit from parallelism
- Needed tools already pre-approved or read-only (grep, glob, read)
- Parent has productive work while waiting

Otherwise spawn foreground.

Verify profile availability before delegating. If missing, fall back to inline.

## Model Routing

Route by task shape. Strong models cost latency and tokens; weak models fail complex reasoning.

| Task shape | Tier | Rationale |
|---|---|---|
| Code exploration, scout brief, symbol trace | Fast / cheap | Bounded read, distilled return |
| Doc fetch, library/SDK lookup | Mid | Broad retrieval, moderate synthesis |
| Implementation on disjoint files, PR-fix, synthesis | Strong | Multi-step reasoning, code generation |
| Memory extraction, to-specs planning | Mid–strong | Judgment + structured output |
| Test suite execution | Fast | Mechanical run + report |

Discover via the tool's native profile/config system.

**Defaults:** no `model` set → inherit parent session model; tool auto-routes → trust the router, override only on clear task-shape mismatch; unsupported → inline or accept inheritance, never spawn a second subagent to work around it.

**Never** pin a strong model on a scout. **Never** pin a fast model on a synthesis step.

## Parallel Execution

**Don't parallelize** when: workstreams share file writes (serialize/merge), one stream feeds the next (serialize/fan-in), sync cost exceeds time saved, or the work is a bounded single stream.

Patterns: **Fan-out / fan-in** (N≥3 independent → wait all → optional synthesis subagent), **Pipeline** (A's output feeds B → serialize), **Scatter / gather** (N≥3 subagents, parent synthesizes inline when results are small).

## Dispatch Contract (applies to every spawn)

- Front-load all context (file paths, function names, what's known, what to return). Subagents are stateless — no mid-run clarifying questions.
- Define return shape explicitly. Vague prompts produce vague returns.
- State write vs. read-only. Mismatch is the most common delegation failure.
- Parent retains all git/gh and side-effecting operations unless explicitly authorized.

## Code Exploration

Read-only reconnaissance. Subagent returns a distilled brief; parent never reads raw traversal. Specify depth and return shape (brief, file:line citations, diagram, named symbol set). Pick profile by intent: orientation vs. targeted question vs. architectural friction.

Fallback on `BLOCKED`: if a subagent returns `BLOCKED` / `NO_*` / `UNAVAILABLE`, do that work inline. Don't retry.

## Offloading Exception (narrow)

Hard gate (overrides "default to inline"): if a task needs **more than 5 file reads AND spans more than 2 modules** for exploration/tracing, dispatch a read-only scout BEFORE any inline `read`/`grep`/code navigation query (see `<project-root>/docs/code-navigation.md` in the project root). The parent acts on the brief; raw file contents never enter parent context.

**Cold scan vs. warm read (decides inline vs. subagent):**

| State | Parent context | Scan shape | Action |
|---|---|---|---|
| Cold scan | Doesn't hold the target area yet | Multi-file / multi-module exploration | Subagent scout — raw output would bloat parent |
| Warm read | Already holds the bulk of context for the task | Small partial scan (a few lines, one symbol, one file) to confirm or double-check | Inline — offloading costs more in dispatch overhead than it saves |

Other exceptions (inline allowed): exact file path and line range already known; a single code navigation symbol lookup / reference trace call (see `<project-root>/docs/code-navigation.md` in the project root) answers it; target file under ~50 lines and fully isolated.
