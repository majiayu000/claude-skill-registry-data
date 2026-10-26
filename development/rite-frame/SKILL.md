---
name: rite-frame
description: Frame an ad-hoc ask before coding, then audit the diff. Use for underspecified imperative asks, raw-diff self-audits, or `/rite-quick` setup. Not a lifecycle gate.
argument-hint: "[task to frame | diff to audit]"
user-invocable: true
---

<!-- loads: {"always":["devrites-lib/reference/standards/core.md","rite-frame/reference/failure-modes.md"],"triggers":{"principles":["devrites-lib/reference/standards/principles.md"],"simplify":["devrites-lib/reference/standards/coding-style.md","devrites-lib/reference/standards/patterns.md"],"testing":["devrites-lib/reference/standards/testing.md"]},"workspace":[]} -->
> Read-set manifest: `devrites-engine context <slug> --phase frame` bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.


# /rite-frame: frame the goal, audit the diff

LLMs reliably get four things wrong: they **assume** silently, **overcomplicate**, edit
**out of scope**, and run on an **unverifiable** "make it work". The full DevRites
lifecycle catches all four at its gates (spec readiness, the Spec Drift Guard,
`touched-files.md` + diff review, `/rite-seal`). But the express lane and plain
"just do X" requests **skip those gates**, and a raw diff has no gate at all.

`rite-frame` is the gate's reflex made portable. Two moves, no workspace required:

- **FRAME** (before code): turn the imperative ask into a falsifiable success criterion
  and the command that proves it. *"Give it success criteria and watch it go."*
- **AUDIT** (after the change): read the diff against the four failure modes; route each
  finding to the DevRites cure that already exists for it.

It is a self-applied lens, not a subagent and not a phase. Light enough to run at the top
of a one-line fix; the heavy guns (`devrites-doubt`, `devrites-audit`, the seal) stay where
they are.

## When to use
At the top of `/rite-quick` · before a plain "just do X" / "quick fix" / "tiny tweak" edit
that won't go through the lifecycle · to self-review a raw `git diff` before you commit ·
any time you're about to act on an imperative without a written success criterion.

**When not:** a real feature (use `/rite-spec`) · a single high-stakes decision that wants
an adversarial second read (`devrites-doubt`) · a fresh-context axis review of an active
feature (`devrites-audit <security|perf|simplify>`) · the final GO/NO-GO (`/rite-seal`).
rite-frame is the *inline* reflex; those are the *gates*. Don't use it to dodge one.

## FRAME: before you touch code

Restate the ask as a check, not a chore. Convert the verb into a condition that can be
**false**:

| Imperative ask | Falsifiable success criterion |
|---|---|
| "Add validation" | "Inputs `{empty, oversize, wrong-type}` are rejected with a 4xx + message: a test asserts each, and fails today." |
| "Fix the bug" | "A test reproduces the bug (red now), and turns green after the fix: nothing else changes." |
| "Make it faster" | "Operation X drops from `<measured baseline>` to `<target>` on `<named benchmark>`." |
| "Refactor X" | "The existing suite is green before and after; behavior is byte-identical." |
| "Clean this up" | *(no falsifiable criterion → the ask is ambiguous → mode 1 → ask what "clean" means, or route to `/rite-spec`)* |

Checklist (copy it):

- [ ] **Criterion**: one sentence: *"Done WHEN `<observable, falsifiable check>`."* If you
      can't write one that could be false, the ask is ambiguous: **stop, name it, ask** (that
      is failure mode 1, surfaced early instead of after the diff).
- [ ] **Verify command**: the exact test / build / runtime / screenshot that decides it.
      No command → no proof → you're about to confidence-assert. Name it now.
- [ ] **Scope boundary**: the files/areas you will **not** touch. Anything outside is mode 3.
- [ ] **Loop**, with a falsifiable criterion you can iterate to green unattended; with a weak
      one ("make it work") you'll need the user every few minutes. Sharpen the criterion until
      it can drive the loop.

## AUDIT: after the change

Read the diff (or `$ARGUMENTS`) against the four modes. One line per finding, severity-tagged
(`Critical / Important / Suggestion / Nit / FYI`), each routed to its existing cure. Full
map + worked examples: [`reference/failure-modes.md`](reference/failure-modes.md).

- [ ] **1 · Silent assumption**: did I pick one reading of an ambiguous ask and run with it?
      Any value, contract, or behavior I *guessed*? → surface it; route material ones through
      the Spec Drift Guard ([`core.md`](../devrites-lib/reference/standards/core.md) #4; surface per #2/#3).
- [ ] **2 · Overcomplication**: an abstraction / flag / indirection nobody asked for? 200 lines
      where 50 would do? A defensive check inside trusted code? → apply the **deletion test**;
      simplify ([`coding-style.md`](../devrites-lib/reference/standards/coding-style.md), [`patterns.md`](../devrites-lib/reference/standards/patterns.md), `devrites-audit simplify`).
- [ ] **3 · Out-of-scope edit**: did I touch code, comments, or formatting outside the ask?
      "While I'm here" refactors? → revert to the boundary; record the rest as an FYI follow-up
      ([`core.md`](../devrites-lib/reference/standards/core.md) #7, `touched-files.md`).
- [ ] **4 · Unverifiable goal**: is there a command that proves this, run, with output? Or am
      I asserting "it works"? Tautological test that can't fail? → run the FRAME verify command;
      record command + output ([`testing.md`](../devrites-lib/reference/standards/testing.md), evidence-over-confidence).
- [ ] **Principle check**, if `.devrites/principles.md` exists, does the change break a declared
      invariant? A violation with no recorded, human-approved exception is a **Critical**: the
      express lane is not a way around a project gate; escalate it, don't ship it ([`principles.md`](../devrites-lib/reference/standards/principles.md)).

The test for each changed line: **it traces directly to the criterion, and the criterion can
be proven false.** A line that fails either is a finding.

## Escalation

If FRAME can't produce a falsifiable criterion, or AUDIT surfaces a mode-1 / mode-3 issue that
is a hidden design decision (new dependency, data model, second design system, an
auth/migration/public-API touch), or a **declared-principle violation** with no recorded
exception → **STOP and route to `/rite-spec`** (a needed exception is a human-approved decision,
not an inline call). Same drift guard the express lane enforces: don't quietly grow an unframed
ask into unreviewed work.

## Rules
- Self-applied and inline. No subagent, no `.devrites/` workspace required. For an adversarial
  fresh-context read of one decision use `devrites-doubt`; for a fresh-context axis audit of an
  active feature use `devrites-audit`.
- FRAME before code, AUDIT after. Running AUDIT without having framed the criterion first means
  mode 4 has nothing to check against.
- A criterion that can't be false isn't a criterion. It's a wish. Rewrite it or ask.
- Feature/ask scope only. Out-of-scope findings become FYI follow-ups, never silent fixes.

```
Done: frame complete for <task>; criterion and boundary are explicit.
Changed: workspace only
Evidence: verify command <cmd | not run yet>; audit findings <none|n>
Open: <none | assumptions | escalation reason>
Next: <single recommended command>
Record: <.devrites/work/<slug>/decisions.md | not applicable>
↻ Hygiene: /clear if no workspace; otherwise follow the active phase hygiene
```

If it routes to `/rite-spec`, that phase owns the durable workspace from there.
