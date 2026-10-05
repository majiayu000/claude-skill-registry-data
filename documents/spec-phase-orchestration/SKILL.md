---
name: spec-phase-orchestration
description: Run the spec-first document phase of a project and gate implementation on it. Use when starting a project that needs a spec before code, deciding which documents the spec phase produces and in what order, choosing whether a section may advance while a prerequisite is unconfirmed, judging whether implementation code may start yet, or when asked "design or foundations first", "which documents go in the spec phase", "can we code before plan.md is approved". Does NOT own where stray ideas are parked (backlog-routing-by-topic) nor the per-section review rounds (subagent-review-cycles).
---

# Spec Phase Orchestration

## When to invoke

- Starting a new project and deciding which documents the spec phase produces.
- Multiple documents / sections are in flight and you need to decide the order of progress.
- User asks "design or foundations first", "can we proceed with prerequisites unresolved".

## Default decisions

### 5 files + `meetings/` directory

```
<repo>/
├── README.md                  # Project entry point
├── docs/
│   ├── foundations.md         # Engineering substrate (language version, modules, CI, L10n, secrets)
│   ├── design.md              # Product spec §What + technical design §How (unified)
│   ├── plan.md                # TDD-ordered checklist
│   └── methodology.md         # Claude agent application practices (living doc)
└── meetings/
    └── {YYYY-MM-DD}_{topic}.md
```

Default: these live in the same repo as the code. A separate `<project>-spec` repo is a
deviation for teams that need spec review gated independently of the code repo — not the
default.

Don't split further:
- No separate spec.md / rfc.md / tasks.md (folded into design.md / plan.md)
- No `adr/` directory; major decisions land directly in design.md or foundations.md (open one only if real need arises)

### Progression order

```
foundations.md §1..§N (one section at a time) →
design.md §What (product spec) →
design.md §How (technical design) →
plan.md (TDD-ordered) →
implementation phase begins
```

**Rule**: don't write §How before design.md §What passes; don't write implementation code before plan.md passes.

### Section-by-section approval

- The Leader advances one section at a time, waiting for user / review approval before moving on.
- Multiple sub-agent rounds may happen within a single section (see `subagent-review-cycles`).
- Section order is non-skippable: §What before §How, §1 before §2.

### Prerequisite checklist (Unconfirmed / Resolved gates)

Any proposal depending on external tools / APIs / third-party packages **must** include a prerequisite checklist:

```markdown
**Prerequisites**:
- [ ] Package `XYZLib` supports Swift 6 strict concurrency mode — **Unconfirmed** (verified in plan.md step N)
- [x] ~~Xcode Cloud hook naming~~ — **Resolved** (Code Review round N, date): adopt `ci_post_clone.sh`
```

- Unconfirmed items **block Leader approval** — the section stays DRAFT until each item is Resolved.
- Resolved items are checked off with their decision basis + date. (`ci_post_clone.sh` above is a real Xcode Cloud hook name — see [Writing custom build scripts](https://developer.apple.com/documentation/xcode/writing-custom-build-scripts).)

### No implementation code before design + plan approved

- Before design.md §What + §How pass and plan.md is written and approved, **no implementation code is written**.
- Exception: a pure exploratory spike — must be logged under `meetings/` as a spike; its output doesn't land on main.

### Backlog sections

Every living doc carries a §Backlog; route stray ideas there by topic — see `backlog-routing-by-topic`.

## Rationale

- 5 docs + meetings dir is the "enough to record, not redundant" sweet spot for solo / small teams; 8 files is over-structured, 4 lacks room for foundations / methodology.
- Section-by-section avoids the high cost of "send the whole doc back".
- Prerequisite gates force "assumptions" to become "items to verify"; CLI trial-and-error is not the default answer.
- Spec-first: "no spec, no code" is a fundamental premise of AI agent collaboration (otherwise prompts are vague and output diverges).

## Deviation considerations

| Project shape | Keep | Drop |
|---|---|---|
| Tiny utility / 1-day project | README.md + meeting log | foundations.md, design.md, plan.md (design inlined in the README) |
| Adding a feature to an existing codebase | design.md, plan.md | foundations.md (lean on existing conventions instead) |
| Multi-person collaboration | A master `plan.md` listing dependencies | A single flat plan.md (split into `plan/<feature>.md` instead) |
| Full outsourcing / contractor | An RFC + tasks split | This skill's 5-doc default (solo / small-team only) |

## Verification checklist

- 5 docs + meetings dir structure in place (README + 4 docs + meetings dir).
- design.md contains §What and §How; §How is only filled after §What passes.
- foundations.md sections carry Status (DRAFT / FINAL / OBSOLETE) + Open items (if any).
- plan.md steps are TDD-ordered (test step precedes implementation step).
- Every prerequisite item is explicitly marked Unconfirmed / Resolved.

## Related skills

- `backlog-routing-by-topic`: rules for placing stray ideas.
- `subagent-review-cycles`: round structure inside spec sections.
- `leader-developer-handoff-contract`: dispatch contract when handing sections to a sub-agent.
- `session-to-meeting-log`: persisting each spec session.
