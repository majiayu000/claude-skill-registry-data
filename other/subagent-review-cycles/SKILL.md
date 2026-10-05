---
name: subagent-review-cycles
description: Structure a multi-round Leader / Developer / Code-Reviewer review of a document or code change. Use when planning how many review rounds to run, dispatching a Code Reviewer subagent and deciding which tools and review criteria it carries, adjudicating a reviewer's BLOCKER / MAJOR / MINOR findings, or when asked "how many review rounds", "may the Code Reviewer run CLI", "what counts as a rejection". Does NOT own the dispatch prompt's required elements (leader-developer-handoff-contract) nor pre-dispatch worktree conflict checks (subagent-conflict-detection).
---

# Subagent Review Cycles

## When to invoke

- About to dispatch a sub-agent to draft a technical document / design section.
- The first version of a document is ready and a Code Reviewer should audit technical correctness.
- User asks "how many review rounds", "should Code Reviewer run CLI", "what counts as rejection".

## The triad

| Role | Job |
|---|---|
| **Leader** (main agent) | Dispatch, integrate review results, accept / reject, communicate with the user |
| **Developer** (subagent) | Draft / revise document sections; works after Leader replies with rejection. (May be dispatched as any implementer-type subagent when the task is architectural in nature; the role name in this skill remains "Developer".) |
| **Code Reviewer** (subagent) | Audits Developer output for technical / API correctness and logic gaps; CLI is forbidden for probing API/runtime behavior (build, run, simctl, trial-and-error); read-only search (grep, rg, git log, git show) is allowed |

The Leader **never** writes the implementation / drafts a section directly — that's the Developer's job. The Leader **never** does the review either — that's the Code Reviewer's job.

## Round structure

```
round N:
  Leader → Developer: dispatch (scope + skills + inputs + return format + criteria)
  Developer → Leader: draft
  Leader → Code Reviewer: dispatch (review criteria + must use WebSearch, no CLI)
  Code Reviewer → Leader: BLOCKER / MAJOR / MINOR list
  Leader: ACCEPT / REJECT each item with explicit reason
  if accepted_count == total: done
  if N == limit: pause, report to user
  else: round N+1 with feedback
```

`limit(N)` is typically 3–5. **If the limit is reached without convergence**: pause, report to the user, wait for direction.

## The "round-1 cosmetic" pragmatic rule

| Signal | Leader inline-edits | Dispatch round N+1 to Developer |
|---|---|---|
| Fix scope | Spelling / formatting / paragraph order / string typo only | Any semantic or content change |
| Time to fix | ≤ 5 minutes | > 5 minutes |
| New decisions required | None | Any |

Still record inline fixes in the meeting log. Reasoning: "limit is an upper bound, not a requirement"; burning a whole round just for typos is uneconomical.

## Dispatch contract for Code Reviewer

Every Code Reviewer dispatch prompt must include:

1. **Target file / section scope** (explicit file + section)
2. **Forbidden tools**: CLI is forbidden for probing API/runtime behavior (build, run, simctl, trial-and-error); read-only search (grep, rg, git log, git show) is allowed
3. **Allowed tools**: WebSearch / WebFetch (for verifying Apple APIs, library behaviour)
4. **Review criteria** (4 dimensions + domain-specific checklist):
   - Technical correctness (API name, behaviour, version)
   - Logical consistency (internal contradictions, cross-section conflicts)
   - Completeness (missing edge case, error handling, prerequisite)
   - Efficiency (algorithm, CI / build / runtime cost)
5. **Return format**: BLOCKER / MAJOR / MINOR three-level classification; each item with location (file + section) + suggestion. An **absence claim** ("the spec doesn't define this", "nothing covers this case") must include the grep/search command run and its zero-hit output — an absence claim with no evidence attached doesn't count as a finding.

## Accept / Reject reply style

For each review finding the Leader gives:

- **ACCEPT + reason**: accepted; specify who fixes it this round
- **REJECT + reason**: rejected with a technical reason (not just "no")
- **DEFER**: acknowledged but deferred (goes to backlog / open items)

REJECT must cite specific evidence (API doc, prior decision, design constraint); pure preference is not acceptable.

## Anti-patterns

- **Using CLI to probe Apple API behaviour**: forbidden. Use official docs / WebSearch instead.
- **Repeatedly rejecting the same point in the same section**: more than 2 identical rejections counts as a communication failure; pause and clarify with the user.
- **ACCEPT without a reason**: every ACCEPT should still have a one-line note of why it adds value.
- **Leader drafting sections themselves**: violates the role separation; only allowed for cosmetic-grade fixes.

## Verification checklist

- Every absence claim ("not defined", "no coverage") in a review finding cites the grep/search command and its zero-hit output — otherwise it doesn't count as a finding.
- Each round has an explicit dispatch prompt (all 5 items of §Dispatch contract for Code Reviewer present, on top of the 6 elements from `leader-developer-handoff-contract`).
- Each review finding has an explicit accept / reject label + reason.
- When limit(N) is reached without convergence, pause; don't keep iterating indefinitely.
- Cosmetic fixes are inline-edited by the Leader; don't burn a round on them.
- The round-summary is recorded in the meeting log (not a verbatim copy of review content).

## Phase TODO sweep checklist

A separate close-the-loop activity that fires **once per phase** (not once per review round), so it's not part of the round structure above. Before the Leader signs off on a phase-completion PR, run a sweep against the phase's diff scope to catch deferred-and-forgotten debt.

For the full sweep procedure, command, disposition rule, and anti-pattern, read `references/phase-todo-sweep.md`.

## Related skills

- `leader-developer-handoff-contract`: details the 6 required elements of every dispatch prompt.
- `spec-phase-orchestration`: review cycles are usually embedded in the spec phase.
- `methodology-pattern-extractor`: "round-1 cosmetic inline edit" is a codifiable pattern.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
