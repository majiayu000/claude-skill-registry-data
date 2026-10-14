---
name: code-review-inline-skill
description: >-
  In-session code-review delegate — loads reviewer-baseline-skill first, then
  the deployed code-review-subagent.md as its checklist, and runs the
  severity-gated diff review inline. Thin wrapper: the agent file stays the
  single checklist source; never spawns a subagent. Triggers: inline code
  review, review diff in-session, v2 pipeline Step 9.
license: Apache-2.0
compatibility: opencode
metadata:
  mirrors: code-review-subagent
category: Code Quality
---

# Code Review (inline)

You are executing the code-review delegate's workflow **in this session**. The
subagent's isolation (fresh context, `edit: deny` sandbox, read-only git
allowlist) is replaced by the discipline below — advisory, but the pipeline's
verdict citation depends on it.

**You are a wrapper, not a copy.** The review checklist — severity rubric,
Direct-Caller Verification gate, ponytail lens, Return Contract — lives in the
deployed `agents/code-review-subagent.md` and is loaded as-is. Never
re-implement it from memory; never paraphrase it into this file's authority.

## Decision tree

1. **Skip check — checklist resolution (blocking):** resolve the deployed
   `code-review-subagent.md` (§Checklist resolution). Unresolvable → report
   `Status: failed`, "review unavailable — checklist not found", and STOP.
   Never run a review without its checklist; never spawn a subagent in its
   place.
2. **Baseline first:** load `reviewer-baseline-skill` — its Prompt Defense,
   Epistemic Honesty, Mandatory Post-Review Learning Gate, and Web-lookups
   policy apply in full.
3. **Load the checklist:** read the resolved `code-review-subagent.md` body
   and follow its Review Checklist, Scope Assessment, Risk-Based Depth,
   Severity Scoring Rubric, Direct-Caller Verification, and Return Contract.
4. **Scope (diff-only):** review the caller-supplied diff — a formatted diff
   plus `--stat` — not the whole codebase. For worktree-based runs the caller
   passes the repo and range; compute `git -C <repo> diff
   origin/<base>...feat/<KEY>` yourself only when the caller names the range.
   Read touched files only, at the paths the caller scopes.
5. **Findings:** severity-gated (BLOCK/WARN/NOTE) per the checklist's rubric;
   every Critical/Major carries a one-line Business Impact.
6. **LEARNINGS:** you have write access the subagent lacks — write qualifying
   candidates directly (`LEARNINGS/<category>/<slug>.md` + `_index.md` entry),
   deduped against existing entries. List written files in Output.
7. **Fix loop (only when the caller grants fix authority):** fix findings
   severity ≥ Major (Minor by judgment), max **2 fix-and-re-review
   iterations**. Fixes landing after a green exit gate re-enter the **full**
   gate before push per `verification-loop-skill` — the final pushed SHA must
   carry a green `tier=full` memo.

## No-subagent pin

This skill runs fully in-session. Do NOT delegate the review, or any part of
it, to a subagent — no Task calls, no child sessions. The isolated-child
variant is a different invocation (`code-review-subagent` via the v1
pipeline or direct delegation), not an escalation path available here.

## Checklist resolution

Capability binding (per the portability contract — the agent self-selects
its row; unknown harnesses fall through to the fallback):
- OpenCode: `~/.config/opencode/agents/code-review-subagent.md` (deploy-mode
  CLI path)
- Claude Code: `~/.claude/agents/code-review-subagent.md`
- Other/none: unresolvable → the Step-1 skip rule (report unavailable,
  stop) — never proceed checklist-less, never spawn in its place

## Scope bounds

- Review the diff and its direct callers; transitive blast radius belongs to
  the architecture review — note suspicions under Issues instead of
  traversing them.
- Fixes (when granted) touch only files in the reviewed diff.
- PLAN atomicity is not checked here — note "PLAN atomicity not checked" per
  the checklist's scope rule.

## Enforcement deltas (vs code-review-subagent)

| Subagent enforcement | Inline discipline (you) |
|---|---|
| Fresh context window | State the reviewed diff range + file list before starting so scope drift is visible |
| `edit: deny` + read-only git allowlist | You MAY write — restrict writes to LEARNINGS entries and granted fix commits; list every write in Output; every LEARNINGS write lands in the run's single end-of-ticket `chore(learnings)` commit — never in fix commits, never left dirty past the ruling commit step |
| Isolated fix-report loop | Fixes land in the working tree directly; re-gate rule above is mandatory, not orchestrator-enforced |
| Tier model | Same model as the caller — flag uncertainty instead of suppressing findings |

## Output contract

**Status:** [success | partial | failed] — `partial` if direct-caller coverage is incomplete, per the checklist's gate rule
**Output:** issue count by severity + file list + LEARNINGS files written (or `LEARNINGS candidates: 0`)
**Summary:** ≤3 sentences, plain language per the checklist's Voice section
**Issues:** blockers, warnings, uninspected callers, or "None"
**Requirements Gaps:** `[{source, blocked_check, suggested_question, recommended_answer}]` — required, `[]` if none
**Patterns applied/violated:** `[{id, status, evidence}]` — required, `[]` if none
