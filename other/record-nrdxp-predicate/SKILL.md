---
name: record
description: |
  Durable categorized record-keeping for any predicate-enabled walk.
  Trigger when:
  - Classifying a step's output for recording (decision, finding, debt, feedback).
  - Promoting a scratch artifact to the ledger, to repo/docs, or to a category
    home (.ledger/tech-debt/, .ledger/process-feedback/).
  - Auditing whether a draft is structurally ready for its destination.
  - Running a zero-context sensibility read before committing to promotion.
  - Recording a known limitation as a tech-debt entry (not prose in the log).
  - Recording a friction, miss, improvement, or process amendment.
  - Prompt contains: /record, record-keeping, promote, ledger note, zettelkasten,
    scratch-to-ledger, zero-context read, over-strip, classification trigger,
    tech-debt, process-feedback, amendment.
---

# Record — Durable Categorized Records

**Ambient** — applies to every predicate-enabled walk, not campaign-only.

The RECORD primitive manages durable artifacts across three complementary
substrates. What distinguishes it from generic note-taking is the
**category model**: each category of durable artifact has a defined
contract (machine-checkable shape), a `.ledger` home, and a trigger
(when to record into it).

---

## Category model

**Who holds the pen.** One writer per node-kind-and-namespace, whoever it
is (the pen law — [`docs/entries.md`](../../docs/entries.md)): **testimony**
is signed by the walker who witnessed it and committed by that walker,
append-only, into `.ledger/deposits/<topic>/<signer>/`; **synthesis,
decision, and narrative** nodes — and every promotion — are the composer's.
In a **solo** predicate walk there is no composer: the walker signs
everything and executes this skill directly. Two writers interleaving one
namespace is how a zettelkasten becomes a shoebox.

Each category = **{contract, .ledger home, trigger}**. Categories are
extensible: adding a fourth later is cheap — add the contract, home,
and trigger row.

| category | contract | .ledger home | trigger |
| :--- | :--- | :--- | :--- |
| **flight-log** | narrative; no formal contract | `.ledger/log/` | at every significant step: decision, pivot, finding |
| **tech-debt** | `skills/record/tech_debt.ncl` | `.ledger/tech-debt/` | when a limitation is accepted rather than fixed |
| **process-feedback** | `skills/record/process_feedback.ncl` | `.ledger/process-feedback/` | when friction, a miss, an improvement, or a live process amendment is identified |

### The flight-log category (existing)

Narrative zettelkasten — linked, curated trail of *how the space was
explored*: decisions, pivots, adjustments. NOT exhaustive; navigable
graph. See [Recording (continuous)](#recording-continuous) and
[Promotion](#promotion) for the full flight-log model.

### The tech-debt category (new)

A first-class, machine-shaped entry for a known limitation or deferred
decision — absorbs the campaign's "accepted limitations / tail" so they
are trackable and actionable rather than buried in prose log entries.

**Fields:** `id` (unique), `claim` (falsifiable statement), `location`
(file:line, gate, or component), `severity` (critical|high|medium|low),
`why_deferred`, `signpost` (what would resolve or invalidate it).

**Instance format:** YAML, validated via:
```bash
nickel export <file>.yaml --apply-contract skills/record/tech_debt_apply.ncl
```

**Trigger:** when you accept a limitation rather than fix it — record
it here, not in prose. A `signpost` is required so the debt is not just
named but actionable.

### The process-feedback category (new)

Captures friction, missed signals, improvements, and AMENDMENTS. An
AMENDMENT is the highest-stakes kind: the agent changed a live process
rule and it was a good idea. This makes process changes durable rather
than living only in conversation recall.

**Fields:** `id` (unique), `kind`
(friction|miss|improvement|amendment), `context` (situation that
triggered it), `outcome` (what changed or what it means).

**Instance format:** YAML, validated via:
```bash
nickel export <file>.yaml --apply-contract skills/record/process_feedback_apply.ncl
```

**Trigger:** when friction surfaces, a signal is missed, the process
improved, or a live rule was amended. AMENDMENT kind requires that the
rule change was nrd-approved or demonstrably beneficial — it is a record
of accepted change, not a unilateral rewrite.

---

## Three substrates with distinct roles

| substrate | role | character |
| :-- | :-- | :-- |
| `scratch` | exhaustive working detail; coherent context being built | default ephemeral; sometimes a draft staged for promotion |
| `ledger` (`.ledger/`) | all category homes: flight-log, tech-debt, process-feedback | curated, linked, durable; each category in its own home dir |
| `repo/docs/` | promoted durable artifacts (a design that graduated) | permanent |

**Promotion** is the combinator `promote(from, to)` over `{scratch, ledger, repo}`.
The destination is routed by purpose, not by artifact type.

---

## Recording (continuous)

At each significant step, classify the output and record it — this is a
**classification trigger**, not a rulebook. Ask: what kind of thing just happened?

| what happened | where it goes | minimum record |
| :-- | :-- | :-- |
| **decision / pivot / adjustment** | linked ledger note (flight-log) | what, why, which `[[decisions/KUs]]` it changes; link to superseded/resolved notes |
| **finding** (new R/I/U item) | update the live R/I/U tracker; ledger note if it pivots direction | tracker entry with grounding + last\_validated + signpost |
| **accepted limitation** | `.ledger/tech-debt/<id>.yaml` | tech-debt record validated against `tech_debt.ncl` |
| **process friction / miss / improvement / amendment** | `.ledger/process-feedback/<id>.yaml` | process-feedback record validated against `process_feedback.ncl` |
| **working detail / draft** | scratch | no ceremony; stage for promotion when ready |

**Linking discipline (flight-log).** Ledger notes are a zettelkasten: each note
links (`supersedes`, `resolves`, `blocks`, `see-also`) to the nodes it affects.
The ledger is a navigable graph, not a flat append log. Every-touch-commit
([Sketch Commit Discipline](../../ambient.md#planning-invariants)) keeps the graph
linear and reconstructable.

---

## Promotion

### Destination routing (the combinator's dispatch table)

`promote(from, to)` routes by the artifact's **purpose**:

- needed to reconstruct *how/why* but not general documentation →
  **ledger** (zettelkasten; future agents in this exploration)
- a durable artifact useful to someone who never saw the exploration →
  **repo/docs** (a user / zero-context agent)
- cross-cases: `scratch → ledger`, `scratch → repo`, `ledger → repo`

The "stranger" for the zero-context sensibility read is parameterized by the
destination's audience. The over-strip line moves with the destination:

- **ledger stranger** — a future agent reconstructing this campaign; still
  needs decisions + why
- **repo stranger** — a user who never saw the exploration; needs none of the
  session context

### Gate 1 — structural readiness (machine-checkable)

The artifact must conform to its destination's contract before promotion:

- a tech-debt record must pass `nickel export ... --apply-contract tech_debt_apply.ncl`
- a process-feedback record must pass `nickel export ... --apply-contract process_feedback_apply.ncl`
- a draft IBC must pass `worker_ibc.ncl` export
- a DAG node must export cleanly against `dag.ncl`
- a skill draft must carry valid YAML frontmatter (this file's own gate)
- a doc must have valid local links and header structure

Does not export / does not conform → **not ready**. Do not proceed to Gate 2.
This makes "structurally ready" machine-checkable rather than a judgment call.

### Gate 2 — sensibility (zero-context multi-round read)

A quality mechanism, not a box to tick. Read the draft as a stranger with
**only its stated purpose**; surface everything that is only meaningful in-session:

- references to "what we discussed" or "as above"
- implicit assumptions the reader cannot recover
- scratch-isms (abbreviations, shorthand, agent-internal labels)

Strip or make-explicit each; iterate until a context-free read is fully sensible.

**Over-strip guard** — strip only what is session-meaningful AND not needed for
the stated purpose. Before stripping anything, ask:

> *Does a stranger with the stated purpose need this to understand / use the
> artifact?*

Yes → keep and make explicit. "Merely discussed in session" → strip.
**Never strip load-bearing rationale.** A sensibility read that removes
rationale is a context-destroyer, not a quality pass.

Depth scales with stakes and destination:
- routine scratch note → ledger: self-administered flush-read
- architectural or doctrine artifact → repo: decorrelated agent review
  ([refine](../refine/SKILL.md) REVIEW semantics)

### Gate 3 — role authorization (privileged)

Promotion is role-gated:

| artifact class | who may promote |
| :-- | :-- |
| testimony (deposits, assessments, findings) → ledger | the witnessing walker, signed |
| narrative / synthesis / promotion notes → ledger | the composer (solo: the walker) |
| full architecture / spec → repo/docs | architect-tier |
| doctrine edits (rules.md, ambient.md, formalism) | **Reserved halt** — human approval required before merge |

A worker cannot unilaterally promote to durable doctrine. On doctrine promotion,
emit the draft and halt for human review before touching the destination.

### On promote: link the durable artifact

After promotion:

1. Strip ephemera (Gate 2 already handled this).
2. Write a ledger note recording the promotion: what was promoted, where it
   landed, and why it graduated. This keeps the zettelkasten honest about the
   artifact's provenance.

---

## Project-local validation

A project (predicate-self-hosting + downstream) records its own tech-debt and
process-feedback through the project-local gate mechanism. Register a gate
script in `.ledger/gates/` that validates the records:

```bash
#!/usr/bin/env bash
# .ledger/gates/10-validate-records.sh
# Validates all tech-debt and process-feedback YAML instances.
set -euo pipefail
root="${1:-}"
skill_dir="$root/skills/record"

for f in "$root/.ledger/tech-debt"/*.yaml 2>/dev/null; do
  [[ -f "$f" ]] || continue
  nickel export "$f" --apply-contract "$skill_dir/tech_debt_apply.ncl" >/dev/null \
    || { echo "tech-debt record failed: $f" >&2; exit 1; }
done

for f in "$root/.ledger/process-feedback"/*.yaml 2>/dev/null; do
  [[ -f "$f" ]] || continue
  nickel export "$f" --apply-contract "$skill_dir/process_feedback_apply.ncl" >/dev/null \
    || { echo "process-feedback record failed: $f" >&2; exit 1; }
done
```

The `project-gates.sh` runner discovers and executes this script automatically
on each commit when a walk is registered. Projects with no `.ledger/gates/`
directory incur zero overhead (the runner is a clean no-op).

---

## Adaptive extension

This skeleton fleshes against the concrete R/I/U at hand. Minimum floor:

- **Recording:** classify the step; write the minimum record for its class.
- **Promotion:** pass structural readiness (Gate 1) before touching Gate 2.

Extend selectively when not converged: add rounds to the sensibility read when
the artifact is high-stakes or the over-strip risk is real; add a decorrelated
reviewer when promoting doctrine; tighten the linking discipline when the ledger
is the primary reconstruction surface.

The skeleton supports shape AND flexibility — it does not prevent movement. Do
not inflate it into an exhaustive script.

---

## Two-purpose inheritance

Following P-GROUND's two-purpose principle:

- **Recording** — formal gate: did you classify and record the step? (presence-
  checkable); substantive gate: is the trail reconstructable? (closed by review).
- **Promotion** — formal gate: does the artifact pass structural readiness?
  (machine-checkable via contract conformance); substantive gate: is the
  zero-context read fully sensible? (closed by the multi-round read + role-gated
  reviewer, depth-to-stakes).

The contract is the "did-they-try" floor that feeds the review; the review is
where substance is judged. Do not fake a smarter contract.
