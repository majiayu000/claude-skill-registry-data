---
name: facilitate-design-it-twice
kind: skill
status: ready
provenance:
  principles:
  - P030
  - P011
  - P028
  - P027
  claims:
  - C00116
  - C00280
  - C00303
  - C00304
  - C00305
  - C00306
  - C00307
  - C00308
  - C00311
  - C00312
  - C00313
  - C00314
  - C00325
  - C00327
  - C00328
  - C00329
  source_anchors:
  - 5e67c59e0e18-c0001
  - aca1f3444508-c0000
  authored_from_digest: 31c9a8517794adba0487fabf442e3eacf5083d1b54752ccc7127f45cd044f07a
---

# Facilitate Design It Twice

## Purpose

Run the *design it twice* discipline: for a consequential interface or module, drive the team to
produce two or more substantially different design alternatives and compare them before
committing, because comparing alternatives reliably yields a better design than adopting the
first idea (PRC-020; clm-018). This skill is the engine of the reviewer's **compare** mode: it
turns a single proposed design into a ranked side-by-side decision, naming the preferred option
and the specific advantage that earns it the top rank.

The comparison is not a matter of taste. Each alternative is scored on principled axes —
value over future maintenance effort (PRC-002), module depth and interface simplicity (PRC-005),
information hiding (PRC-006), user value (PRC-003), and freedom from speculative complexity
(PRC-007) — so the recommendation is traceable to named principles rather than preference.

## When to use

- A consequential interface, module boundary, or class is being designed and only one idea is on
  the table.
- Two or more design alternatives already exist and the team wants them compared and ranked
  before committing.
- A first design is about to be adopted by default, with no alternative considered.
- A significant redesign has been triggered by a review finding and needs a structured choice
  between competing directions.

Do **not** invoke this skill when the decision is trivial, easily reversible, and low-impact —
generating alternatives for such a choice is wasted effort (PRC-020 *does_not_apply_when*). If
only one design has been proposed for a consequential interface, the first job of this skill is
to require a genuine second alternative before any comparison begins.

## Procedure

### Step 1 — Confirm the decision warrants design-it-twice

Check that the decision is **consequential**: a hard-to-reverse interface, a module boundary
that many callers will depend on, or a structure expected to live a long time. The quality a
design deserves rises with how long the system will be used (clm-028).

If the decision is trivial and easily reversible, stop and record that design-it-twice is not
warranted; recommend proceeding with the single design. Otherwise continue.

### Step 2 — State the problem and the present known requirements

Write the design problem in one or two sentences, framed by **what it must do for its users** —
the purpose of software is to help people, and every alternative will ultimately be judged by
how well it serves that purpose (clm-026; PRC-003).

List the **present known requirements** only. Do not admit speculative future needs into the
problem statement: designing for a predicted future is the most common and costly design error
(clm-030; PRC-007). These requirements become the fixed yardstick every alternative is measured
against.

### Step 3 — Generate two or more *substantially different* alternatives

Produce at least two alternatives that differ in their fundamental approach — not cosmetic
variants of one idea (PRC-020; clm-018). Useful ways to force real divergence:

- **Different decomposition** — split responsibilities along different seams (e.g. by
  information owned vs by operation performed).
- **Different interface shape** — a narrow specialised interface vs a slightly more
  general-purpose one covering the present family of needs.
- **Different placement of complexity** — expose a configuration point to callers vs absorb it
  inside the module (the pull-complexity-downward choice, clm-015).
- **Different hiding boundary** — change which design decision each module encapsulates
  (clm-010).

For each alternative, write a short sketch of its interface and its internal decomposition. A
sketch is a structural description, not implementation code.

If the caller supplied only one design, treat producing the second genuine alternative as a
required output of this step.

### Step 4 — Score each alternative on the comparison axes

Evaluate every alternative against the five axes below. Record a short judgement and the
governing principle for each cell; do not collapse to a single number without the reasoning.

| Axis | Question | Grounding |
|---|---|---|
| **Value over maintenance effort** | Which alternative delivers the required value for the least *future* maintenance effort? Maintenance effort dominates a long-lived system's cost, so it is weighted most heavily | PRC-002; clm-027; clm-028 |
| **Module depth / interface simplicity** | Which has the simpler interface relative to the functionality it provides — i.e. the deeper module? A simple interface matters more than a simple implementation | PRC-005; clm-007; clm-015 |
| **Information hiding** | Which better encapsulates the decisions most likely to change, and which leaks a decision across boundaries or follows execution order rather than information ownership? | PRC-006; clm-010; clm-011; clm-012 |
| **User value / purpose** | Which more directly helps users accomplish the software's purpose? | PRC-003; clm-026 |
| **No speculative complexity** | Which stays bounded to present known requirements, adding no generality, configuration, or abstraction that no present requirement demands? | PRC-007; clm-030; clm-034 |

### Step 5 — Compare side by side and rank

Lay the alternatives against the axes in a single comparison table. Rank them primarily by
**value over future maintenance effort** (PRC-002; clm-028), using **module depth and
information hiding** as the decisive structural tie-breakers (PRC-005; PRC-006). An alternative
that wins on present implementation ease but loses on future maintenance effort does **not**
rank first — present implementation effort is the lesser cost (clm-027; clm-028).

Watch for a **hybrid**: comparing two designs often exposes the strengths of each and reveals a
third option that combines them (clm-018). If a hybrid is clearly superior on the axes, propose
it as a named third alternative and rank it too — but hold it to the same speculative-complexity
gate (PRC-007).

### Step 6 — Name the preferred option and its advantage

State the winner in one sentence, citing the axis on which it wins and the principle behind that
axis. Name the concrete advantage it holds over the runner-up (for example, "Option B is the
deeper module: it hides the storage-format decision that Option A leaks to three callers —
PRC-006"). Note any axis on which the winner is weaker and why that weakness is acceptable given
the present known requirements.

### Step 7 — Hand off the decision

Deliver the ranked comparison to the engineer or tech lead who owns the design; that person
holds the final decision (see `profile.yaml handoff_rules`). The skill recommends; it does not
decide unilaterally or produce replacement code.

## Inputs

| Field | Required | Description |
|---|---|---|
| `problem` | Yes | The consequential design problem, framed by what it must do for its users |
| `requirements` | Yes | The present known requirements; speculative future needs are excluded |
| `alternatives` | No | One or more proposed designs. If fewer than two are supplied, the skill generates the missing genuine alternative(s) |
| `lifetime` | No | Anticipated system lifetime; calibrates how much the maintenance-effort axis dominates |
| `team_conventions` | No | Legitimate local constraints that may favour one alternative for consistency |

## Output

A ranked design comparison containing, in order:

1. **Verdict** — one sentence naming the preferred alternative and the principal axis (and
   principle) on which it wins.
2. **Problem and requirements** — the design problem framed by user purpose, and the present
   known requirements used as the yardstick.
3. **Alternatives** — a short structural sketch of each substantially different option (at least
   two), plus any hybrid surfaced by the comparison.
4. **Comparison table** — every alternative scored across the five axes, each cell carrying a
   short judgement and the governing principle.
5. **Preferred option and advantage** — the winner, its concrete advantage over the runner-up,
   and any accepted weakness with its justification.

The minimum useful output is the verdict sentence plus the one axis-and-principle reason the
preferred alternative wins.

## References

- [`../../references/equation-of-software-design-summary.md`](../../references/equation-of-software-design-summary.md) —
  the value-over-effort axis and why future maintenance effort dominates (PRC-002).
- [`../../references/ousterhout-red-flags-catalogue.md`](../../references/ousterhout-red-flags-catalogue.md) —
  module depth, information hiding, leakage, and temporal decomposition, used as the structural
  tie-breaker axes (PRC-005, PRC-006).
- [`../../principles/principles.yaml`](../../principles/principles.yaml) —
  PRC-020 (design it twice), PRC-002 (the Equation), PRC-005 (deep modules), PRC-006
  (information hiding), PRC-003 (purpose: help people), PRC-007 (no speculative generality).

## Provenance

Derived from principle PRC-020 (design it twice) and its supporting claim clm-018, with the
comparison axes grounded in PRC-002, PRC-005, PRC-006, PRC-003, and PRC-007 and their claims
(clm-027, clm-028, clm-007, clm-015, clm-010, clm-011, clm-012, clm-026, clm-030, clm-034) as
recorded in `principles/principles.yaml` and `analysis/claims.jsonl`. Grounded in source anchors
from *A Philosophy of Software Design* (`a-philosophy-of-soft-5e67c59e`: design-it-twice h0267,
module depth h0033/h0037, pull-complexity-down h0157, information hiding h0064–h0068) and *Code
Simplicity* (`code-simplicity-the-aca1f344`: purpose h0020/h0021, the Equation h0024/h0028,
maintenance dominance h0038/h0042, do-not-predict-the-future h0047, over-generality h0068/h0069).

**Rights notice:** both source texts are `distillation-only`. All content in this skill has been
paraphrased into original language; no verbatim runs of source wording appear anywhere in this
file.
