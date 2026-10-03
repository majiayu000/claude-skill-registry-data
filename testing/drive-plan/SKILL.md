---
name: drive-plan
description: Use when the user says "/drive-plan", "drive a plan", "drive this feature end-to-end with planning", "let's build feature X properly", "kick off this change with planning rigour", or asks Claude to drive a substantial change all the way through planning, implementation, and review in one composed workflow. Calls /plan-change interactively to produce ADR + Gherkin spec, then /implement-change to translate spec into code, then /review-change to audit and dispatch fixes via the agent pipeline; recommends /open-pr at the end. Use /drive-plan for substantial changes warranting planning rigour; use /drive-change for quick changes that don't need formal planning; use /drive-pr to iterate an already-open PR. Confirms with the user at each phase boundary because this skill writes a lot of state.
allowed-tools: Bash(gh:*), Bash(git:*), Bash(npm:*), Bash(yarn:*), Bash(pnpm:*), Bash(bun:*), Bash(npx:*), Bash(go:*), Bash(cargo:*), Bash(pytest:*), Bash(vitest:*), Bash(jest:*), Bash(playwright:*), Bash(just:*), Bash(make:*), Read, Edit, Write, Grep, Glob, Skill, Task
---

# drive-plan

The end-to-end "make this feature happen with planning rigour" workhorse. Composes three skills in order: `/plan-change` (produce ADR + spec), `/implement-change` (translate spec into code), `/review-change` (audit and dispatch fixes). Recommends `/open-pr` at the end without auto-opening.

This skill writes a lot of state — code, docs, commits — so it confirms with the user at every phase boundary. The cost of an unwanted commit or a half-written feature is higher than the cost of one extra "proceed?" question.

## When to use this vs other drivers

- **`/drive-plan`** — substantial change warranting an ADR + Gherkin spec before writing code. Multi-step features, architecture changes, anything where "what is the right shape" needs discussion before implementation.
- **`/drive-change`** — clear or quick change where the implementation can be derived from conversation without formal planning. Bug fixes, small enhancements, "fix the typo" work.
- **`/drive-pr`** — iterate an already-open PR to merge-ready state.

## Phase 0 — Intent and scope gate

Confirm the change warrants planning rigour. If the user describes a one-line bug fix, redirect to `/drive-change` rather than spinning up the full pipeline.

Ask:
- What's the change about? (one sentence)
- Is there an existing ADR or spec to update, or is this net-new?
- What's the target scope — files, directories, components?

If the answer is "tiny change, no, one file", recommend `/drive-change` and stop. If the answer is "substantial, net-new, multiple domains", proceed.

## Phase 1 — Planning via /plan-change

Invoke `/plan-change` via the `Skill` tool. `/plan-change` is interactive — it holds a discussion with the user to extract context, decisions, scenarios, edge cases. Output is an ADR file and a Gherkin `.feature` spec file.

Carry-forward state: record the paths of the ADR and spec files produced.

**Confirm before proceeding to Phase 2.** Show the user:
- ADR path + one-line summary
- Spec path + count of scenarios

Ask: "Plan looks right? Proceed to implementation?"

If the user wants iteration, re-invoke `/plan-change` or branch back to discussion. Do not proceed without explicit confirmation.

## Phase 2 — Implementation via /implement-change

Invoke `/implement-change` via the `Skill` tool, passing the ADR and spec paths from Phase 1.

`/implement-change` reads the contract, maps the touched surface (LSP-preferred), proposes a file-by-file plan, confirms with the user, writes the implementation, and runs the spec's scenarios as smoke tests. For large multi-domain implementations, `/implement-change` itself uses the agent pipeline (`orchestrate-slice` to partition, parallel fix-applier workers in implement mode) — that's its concern, not yours.

Carry-forward state: list of files touched in this phase, commit SHAs (if `/implement-change` committed per scenario).

**Confirm before proceeding to Phase 3.** Show the user:
- Touched files (count + top-level paths)
- Scenarios passing / failing
- Commit log since Phase 1

Ask: "Implementation looks right? Proceed to audit + fix?"

## Phase 3 — Audit + fix via /review-change loop

Invoke `/review-change` via the `Skill` tool. `/review-change` runs the full agent pipeline (slice → fan-out to specialists → merge → verify) read-only over the working tree and produces findings in the [`finding-format.md`](../../references/finding-format.md) schema, partitioned into single-file work packets with sensitivity annotations.

The findings drive a fix-applier dispatch loop:

1. For each work packet in `/review-change`'s output, invoke `agents/fix-applier.md` via the `Task` tool:
   - `Read` the agent file once.
   - Pass `{ packet_id, files, findings, suggested_model }` as the `## Input` block.
   - Set the Task `model:` parameter to `packet.suggested_model` (verbatim — no second judgment).
   - Set `subagent_type: "general-purpose"`.
   - Dispatch all packets **in parallel** (the merger guarantees file-partition, so no write collisions).
2. After all fix-appliers return, re-run `/review-change` to see if new findings emerged.
3. Loop until findings reach steady state (no new P0/P1) or the user calls it done.

`judgment_findings` from `/review-change` (findings with `decide:` prefixes) go straight to the user — never dispatched to fix-applier. Surface them as "decisions to make" and let the user respond.

**Confirm before proceeding to Phase 4.** Show the user:
- Findings applied (count by severity)
- Findings unappliable (count + per-finding reason)
- Findings escalated as judgment calls
- Drifted reviewers (if any) — flag for follow-up

Ask: "Audit + fix looks good? Recommend opening the PR?"

## Phase 4 — Recommend /open-pr

Do **not** auto-open the PR. Print:

> Ready for `/open-pr`. Suggested PR title: `<derived from ADR>`. Suggested base branch: `<current upstream>`. Touched files: `<count>`. Use `/open-pr` to package and push.

The user runs `/open-pr` when ready. After that they'd typically use `/drive-pr` to drive the PR to mergeable.

## Operating rules

- **Phase-boundary confirmation is non-negotiable.** This skill writes the most state of any in the plugin; checkpointing matters.
- **Never skip ahead.** Phase 2 cannot run without a spec from Phase 1. Phase 3 cannot run without an implementation from Phase 2. If the user wants to skip planning, redirect to `/drive-change`.
- **Never auto-open the PR.** Phase 4 ends with a recommendation, not a `gh pr create` call.
- **The agent pipeline is for `/review-change` to dispatch.** `/drive-plan` itself does not call `orchestrate-slice` / `orchestrate-merge` / `orchestrate-verify` directly — it composes the higher-level skills that do.

## Composing with other skills

- Calls: `/plan-change`, `/implement-change`, `/review-change` (in sequence) via `Skill`.
- Invokes: `agents/fix-applier.md` via `Task` (during the Phase 3 loop).
- Recommends: `/open-pr` at the end.
- Sibling: `/drive-change` (no-plan workhorse), `/drive-pr` (PR iteration).

## Carry-forward state shape

Maintain a working block at the top of state so the workflow can resume if interrupted:

```
## Drive-plan state
- ADR: <path> (from Phase 1)
- Spec: <path> (from Phase 1, N scenarios)
- Touched files: <count> (from Phase 2)
- Commits since Phase 1 start: <count>
- Last /review-change run: <timestamp>, <P0/P1/P2/P3 counts>
- Current phase: <0|1|2|3|4>
```
