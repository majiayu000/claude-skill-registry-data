---
name: code-review-methodology
description: "Conduct two-stage code review: Stage 1 verifies spec compliance (criterion-to-code mapping), Stage 2 evaluates security, correctness, performance, and maintainability across 6 parallel facets with P1/P2/P3 synthesis and deduplication by file:line. For the Tests facet the reviewer derives expected behavior from the spec before reading the tests. Use when reviewing code changes or pull requests. This skill MUST be consulted because reviewing quality on broken logic is wasted effort, and unmet acceptance criteria must block merge."
allowed-tools: Read, Bash, Grep, Glob
context: fork
agent: Explore
---

# Code Review Methodology

## Contract

Iron law: verify it works before verifying it is good; never review quality on code that misses the acceptance criteria. Required by `/flow:review`, `/flow:pr`, `code-reviewer`, `security-reviewer`. Returns a P1/P2/P3 finding set (`references/finding-schema.md`), a requirements map, and APPROVE, COMMENT or REQUEST_CHANGES. Skips: Stage 2 when Stage 1 finds >3 unmet criteria; on the 3rd+ cycle, only new P1s.

## Two-stage review

**Stage 1, spec compliance.** Give each acceptance criterion one status: **Met** (implemented and testable), **Interpreted** (ambiguous; one reading implemented), **Partially Met**, **Not Addressed**. If Stage 1 fails, stop.

**Stage 2, code quality**, in priority order: security, correctness, performance, maintainability. Never flag maintainability while security or correctness findings stand.

## 6-facet review

Stage 1 on the main thread; facets fan out in parallel:

| Facet | Focus | Agent / Skill |
|---|---|---|
| **Security** | OWASP top 10, secrets, authz, input validation | security-reviewer |
| **Quality** | Logic, edge cases | code-reviewer |
| **Conventions** | Commit, branch, PR format | convention-checker |
| **Tests** | Coverage, quality commands, adequacy | test-runner |
| **Error handling** | Unhandled errors, silent failures | error-handler-inspector |
| **Claim verification** | Self-review claims vs files | holdout-validation |

**Tests facet rule:** derive the expected behavior from the spec BEFORE reading the tests, then check each expected value and input against it; an expectation copied from the implementation confirms nothing (`references/test-review-checklist.md`).

## Synthesis

1. Deduplicate by `file:line`, keeping the highest priority
2. Order P1, P2, P3 by file
3. Count per priority; counts must match the `Finding | Suggested Fix` rows (`references/finding-schema.md`)

## Confidence and signal

HIGH (ran code, a test or LSP) and MEDIUM (read the code path) decide at their priority. LOW (pattern match), any priority, goes to Needs investigation, outside the decision and the `FLOW_REVIEW_CYCLE` marker; own-PR handling: `commands/review.md` Phase 4 step 5. Absent or invalid confidence is MEDIUM. `bin/flow-finding-route.sh` applies it. Style is P3 at most; a finding with no `file:line` and no harm scenario is noise.

## Boy Scout recognition

APPROVE `improve:` commits passing the proximity test (already-modified file, self-evidently correct, <10 lines, no API change); else P2 "scope creep".

## Review cycle awareness

The cycle number counts prior `FLOW_REVIEW_CYCLE` markers. Review the delta only, verify each claimed resolution against `git diff`, and on the 3rd+ cycle raise only new P1s (`references/review-cycle-parsing.md`).

## Stop conditions

- >3 unmet criteria in Stage 1: REQUEST_CHANGES, skip Stage 2
- Files unrelated to the issue: out-of-context, ask for a split (`improve:` commits in modified files stay in context)
- Diff >500 lines, no test changes: P1 "untested large change"

## Review decision

| Findings | Decision |
|---|---|
| Any HIGH or MEDIUM P1 | REQUEST_CHANGES |
| Any HIGH or MEDIUM P2 | REQUEST_CHANGES |
| HIGH or MEDIUM P3 only | COMMENT; the author fixes every P3 in-PR, never "approve with nits" |
| None, or LOW only | APPROVE |
| Your own pull request | COMMENT at any priority — GitHub takes no verdict from an author |

Finding triage never triggers escalation (`skills/llm-operator-principles/SKILL.md`).

## Grounding pass (off by default)

`review.groundingCritic: on` inserts one step into a **Path B** fan-out, between
synthesis and display: `Agent(finding-critic)` answers each P1/P2 finding in a three-verdict
grammar, and on a disagreement the reviewer that raised it cites code or drops it.
**Path A is unchanged** and keeps its own challenge round; the grammar and both
placements are in `references/paired-review-protocol.md`. Default off until
`references/review-precision-eval.md`.

## Adversarial protocol

With agent teams enabled, apply `skills/team-coordination/SKILL.md`: independent reviewers, mutual challenge, disputed findings escalate.
