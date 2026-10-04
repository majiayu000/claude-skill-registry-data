---
name: review-change
user-invocable: true
version: 3.9.0
argument-hint: <path-or-glob> [--adversarial N] [--synthesize]
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Review a change with only applicable internal axes, classify every finding,
  persist fix-now work, and return one evidence-backed decision. Findings only;
  --adversarial N uses isolated reviewers; --synthesize fuses supplied reviewer
  tables. Triggers: "review-change", "review this change", "adversarial review".
---

# Review Change

Quality gate: run every applicable review and skip the rest, then synthesize and
classify one report. **Findings only; never edit or refactor.**

## Turn contract

Load and verify the **canonical** [Turn contract](.claude/skills/orchestration-envelope/references/TURN_CONTRACT.md) (11 boxes) before ending every turn. Skill-specific additions (receipt closeout, isolation rule, applicability) live here and in [REVIEW_PROCESS.md](references/REVIEW_PROCESS.md). Missing reference → STOP.

For a final PR review, the turn is incomplete until this additional box passes:

```text
✓ Decision: REVIEW-PASS + PR exists →
  `bun scripts/review-receipt.mjs emit --pr <N> --head "$(git rev-parse HEAD)" …`
  RUN and exited 0 — the script posts the SHA-bound comment, re-reads the PR
  comments, and exits non-zero unless the newest exact-HEAD
  `review-change:pass` marker is confirmed, so its exit code IS this box
```

The receipt closeout is a precondition of the report, not a follow-up: do not
print the fixed report block on a non-zero exit. A clean report without a
current receipt must not recommend `/audit-pr`.

For `REVIEW-FAIL` or `NEEDS-DECISION`, list every open finding ID in the closing
recommendation, joined with ` + `; the review must never hand off only the first
finding.

## Review-end turn boundary

On `REVIEW-FAIL` or `NEEDS-DECISION`, this skill **ends at the report**: it
never invokes `/fold-findings`, `/execute-phase`, `/unit-lane` or
`/triage-issue` — those are separate user-initiated invocations,
run in a fresh turn (a programmatic outer driver may compose the same
sequence in-turn, per `REVIEW_PROCESS.md`). The review's only mutations are the
ledger commit (persist step 11) and, on `REVIEW-PASS` with a PR, the
receipt comment (persist step 12); it never folds a finding, executes a phase,
or edits code. A `REVIEW-FAIL`/`NEEDS-DECISION` turn closes when the report
block is printed (report step 13).

Consume the internal [verification contract](<../verification-contract/SKILL.md>);
the reviewer checks the same frozen `ACCEPTANCE.md` blob as the executor before
mapping candidate evidence.

## When to use

- **Mandatory before every merge.** Review in a context that did not implement
  the change; if it did, stop and hand off to a fresh one. `execute-phase` may
  also recommend optional checkpoints at layer boundary, accumulation or
  sensitivity (`#77`).
- Use when you need applicable reviews without irrelevant passes.

## Scope

Default target is the **current change** (branch diff vs the default branch);
accept a path/glob to widen or narrow. State the scope at the top of the report.

## Review charter — dismantle the claim

The workflow's job is to demonstrate that what works, works — **and works
well**: programmatically, engineering-wise, decision-wise, and against user
expectation. This review exists to **try to dismantle that claim**; if it
survives the attempt, that survival *is* the review outcome. So:

- **In-scope defects are this review's job — never “out of scope”.** A bug, a
  security issue, or a guard skip inside the current feature's scope is a
  `review-change` finding: a feature is not complete while it has one. The
  reward is not delivery, it is meeting the acceptance criteria, adequate
  engineering without over-engineering, meeting **other features' requirements**
  (a page that needs auth verifies the session *and* the permission; a change to
  another table that a requirement depends on stays in scope even if it “looks”
  out of scope), and above all the user's expectation.
- **Ask, don't infer — the whole expectation surface.** Where the plan, the diff
  or the requirement leaves the user's expectation unclear, surface it as a
  question in non-technical terms (a technical user asks for an app; a
  non-technical user asks for “an app to measure my heart rate”) — never as an
  assumed intent. This extends ask-don't-infer from acceptance criteria to every
  expectation the change is judged against.
- **Repo-wide hunting is not this review.** Open-ended bug hunting, security
  research and broken-version investigation *across the repository* belong to
  `product-audit`, where the sweep is scoped and budgeted; this review stays on
  the change at hand.

## Step 0 — Discover the project & the change (always first)

Per Workflow conventions + documentation map, decide axes from:

1. **Project nature:** UI (`docs/frontend/`), web/mobile/CLI/library/backend,
   and optional recorded platform skills (extras only).
2. **Footprint:** what the diff touches (UI, API, infra, domain). An axis applies
   only when both project and footprint support it.

## Applicability matrix (default; the project's docs refine it)

Every axis maps to a skill of the workflow's **own internal review pack**
(`skills/review-*` — installed with the workflow, so none can be missing):

| Axis — internal pack skill | Web | Mobile | Console/CLI | Lib/SDK | Backend/Infra |
|---|---|---|---|---|---|
| `review-code` (correctness, simplification, dead code, duplication, arch) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `review-security` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `review-verify` (run it, confirm real behavior, tests) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `review-design` (UI/UX) | ✓ | ✓ | TUI only | ✗ | ✗ |
| `review-a11y` | ✓ | ✓ | rare | ✗ | ✗ |
| `review-brand` (voice/copy) | ✓ | ✓ | output text | ✗ | ✗ |
| `review-perf` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `review-seo` | ✓ | ✗ | ✗ | ✗ | ✗ |
| API ergonomics / usage docs (inline pass) | if API | if API | flags/help | ✓✓ | ✓ |

> `review-implementation` (the single classifier over the synthesized table —
> process step 8) and `review-debt` (the debt transform over the classified
> table — process step 9) are not axis finders: they run once per review, not
> per axis.

## Isolation rule (default — every pass, not only adversarial)

Each applicable pass, the verification pass (step 6), the classifier (step 8), and debt transform (step 9) runs
**isolated/context-clean** and returns only its fixed findings table plus
`PASS | FAIL`—never diff or prose. Spawn one fresh subagent/headless run per
pass; without those, use a fresh conversation. Pass only scope, its checklist,
and Step 0 docs; cap full non-diff reads at 10 (targeted ≤50-line reads/greps
excluded). The orchestrator retains tables, not sources, and fuses them in step
7. Inline fallback is sequential table reduction. A pass runs at its own tier or
stronger, never weaker.


## Progressive loading — choose one review route

After applicability and isolation are established:

The reference allowlist is exactly the seven linked paths below. Never invent or
read another `references/` path.

| Invocation route | LOAD in this order | SKIP |
|---|---|---|
| Default review | [review process](references/REVIEW_PROCESS.md) → [adversarial recommendation](references/ADVERSARIAL_RECOMMENDATION.md) → [persist and decide](references/PERSIST_AND_DECIDE.md) → [output and guardrails](references/OUTPUT_AND_GUARDRAILS.md) | synthesis, portability, adversarial setup |
| `--adversarial N` | review process → [adversarial setup](references/ADVERSARIAL_SETUP.md) before reviewers → [adversarial synthesis](references/ADVERSARIAL_SYNTHESIS.md) before fusion → persist/decide → output/guardrails | portability |
| `--synthesize` | review process → [adversarial synthesis](references/ADVERSARIAL_SYNTHESIS.md) plus the supplied reviewer tables → persist/decide → output/guardrails | adversarial setup, portability |
| legacy `--merge` | print the fixed migration refusal below and stop — zero git/forge mutation | everything |

**Legacy `--merge` is removed — not an alias.** Calling `/review-change --merge` prints this fixed **migration refusal** and stops **before any git or forge mutation command runs**:

```
migration: --merge is removed. Table fusion is --synthesize: pass the fixed
reviewer tables the same way and the synthesis contract fuses them. No
repository merge is performed by this skill.
```

Active review paths use only `--synthesize`/fusion language. Add
[portability](references/PORTABILITY.md) only when contexts, parallelism, slash
commands or tier controls are unavailable. `docs/workflow/REPOSITORY_STATE.md`
is evidence for output/guardrails, not a skill reference; that route owns NRS and
Architectural invariants rules.

Resources are one hop from this file. Fixed reviewer/synthesis/output contracts are
literal. Missing required resource → stop; never approximate a review contract.

## Portability

Keep reviewer contexts isolated. Use [portability](references/PORTABILITY.md) for
sequential/headless fallbacks; never collapse independent adversarial passes.

## Relationship to other skills

Orchestrates internal finders (`review-code`, `review-security`, `review-verify`,
`review-design`, `review-a11y`, `review-brand`, `review-perf`, `review-seo`), then
one `review-implementation` classifier and `review-debt` transform, isolated by
default; installed platform packs are optional. `triage-issue` is user-invoked,
never auto-run (D3), for independent proposals, audit findings, and
`--prioritize-now` runs. It is Stage 4: checkpoint reviews are
optional, the end review is mandatory and fresh. `fix-now` is routed to the
unit's fold cycle — a separate `/fold-findings` invocation, never run by this review;
`replan-in-unit` adds user-confirmed phases, and independent work becomes
proposals. `audit-pr` consumes
only the verified PR-comment receipt, never the
chat report; `product-audit` is the periodic sweep. On `REVIEW-FAIL` the manual
correction path is `/fold-findings`, then re-run `/review-change` on the changed
HEAD (bounded at two cycles — a third cycle never starts without an explicit
user instruction, per `REVIEW_PROCESS.md`); a programmatic outer driver may run
the same review→fold sequence.

## Done when

- One synthesized/classified table covers every applicable axis, lists skipped
  axes with reasons, and includes manual checks. Every finding has a destination:
  fold, confirmed replan phase, surfaced decision, or user-routed proposal; none
  is silently lost and review creates no backlog (D3). Print the closing
  `→ Next:` block (clean → `/audit-pr`; recurring drift → `/product-audit`) and
  change no code.
