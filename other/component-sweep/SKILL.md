---
name: component-sweep
description: Fast breadth-first TRIAGE across many Certus components — property inventory and spec-vs-code divergence list only, no proving. Produces the three property YAMLs per component (the same files `component-verify` Step 2 consumes) plus a cross-component divergence report, in hours rather than the days a full prover pass costs. Use it to decide WHERE to spend prover time, and to get the property denominators for every component. It never proves, never scores, never touches a branch. It is NOT a substitute for `component-verify` and produces no scoring page.
argument-hint: "<component>[,<component>...] | --all-unverified [--jobs N]"
---

## Why this exists, and what it deliberately is NOT

Verifying one component properly costs days, dominated by Kani. Measured on
eviction-policy-optimized: a Kani stage of 5h17m, against a Creusot stage of minutes. Spending that
per component before knowing which components matter is how a programme gets lost in its first few.

**The key observation this skill is built on:** every one of the 10 Certus defects found so far was
first identified by the BLIND CODE EXTRACTION and the spec-vs-code reconciliation — Role 1. The
provers then *confirmed* them and produced witnesses. Role 1 is agent work with essentially no prover
time, so the defect-finding half of the value is available at a small fraction of the cost.

**This skill is TRIAGE, not delivery.** It is not a faster `component-verify`:
- it produces **no proofs**, so every tool column is empty and there is **no scoring page** — the
  deliverable renderer correctly refuses to emit one, and you must not hand-make it;
- a component is **not verified** because it has been swept. Saying so would be exactly the
  "not attempted ≠ a rating" error the pipeline exists to prevent;
- it writes **nothing** to any `verif/*` branch and pushes nothing.

**`component-verify` remains the only path to a verified component.** Do not modify it, its Role-2
skills, or the gate to speed up a sweep. If a sweep needs something the full pipeline has, copy the
behaviour here; never weaken the gate.

## What it produces, per component

Under `<run-dir>/<component>/verif/` — **exactly the files `component-verify` Step 1 produces**, so a
sweep is a completed Step 1 and the full pipeline can pick up at Step 2 with no rework:
- `spec_properties.yaml`, `code_properties.yaml` — the two blind extractions
- `unified_properties.yaml` — reconciled, with **empty** `creusot: {}` / `kani: {}` blocks

Plus, once per sweep, `<run-dir>/DIVERGENCES.md`: every `origin: divergent` obligation across all
components, with its spec pointer, code pointer and the disagreement in one line. **This is the
output that earns the sweep** — it is the ranked list of defect candidates.

## Step 0 — cheap preflight, per component, FAIL FAST (seconds)

Do this before spending any agent time. Each check is seconds, and each one has cost a real run:
1. `components/<c>/` exists and holds `src/*.rs`.
2. Resolve the interface: the component's own `use interfaces::{…}` and `impl I<X> for`, then confirm
   the `component_macros::define_interface!` block in `components/interfaces/src/i<x>.rs`. The
   filename is **not** always a transform of the component name. `N` = the `fn` count in that block.
   If you cannot locate the block, **skip the component and say so** — never guess.
3. Full `cargo metadata` with cwd = `components/<c>/` — **not** `--no-deps`, which returns 0 on the
   fault this catches. A component cargo cannot read is not swept; it is reported.
4. Note the spec of record (`components/<c>/specs/**/spec.md` or the interface doc if there is none).
   A component with no spec can still be swept — the extraction is then code-only and every property
   lands as `code-only`, which is itself a finding worth reporting.

Print one line per component: `<c>: interface I<X> N=<n> | spec <path|none> | cargo ok | SWEEP|SKIP(reason)`.

## Step 1 — two BLIND extractions, then reconcile (per component)

Same discipline as `build-property-inventory`; read that skill and follow it. The blindness is the
whole point and is not negotiable:
- the spec agent may read the spec bundle and the interface declaration, and **must not** open
  `src/**`;
- the code agent may read `src/**`, `tests/**` and the interface declaration, and **must not** open
  `specs/**`, `README.md`, `info/` — nor the other agent's `spec_properties.yaml`, which will already
  be sitting in the same directory.

If either agent peeks, the divergence list — the only reason to run a sweep — becomes worthless.

**Reconcile with the two-stage protocol** (it is in `build-property-inventory`; use it, it was built
after two agents were lost to timeouts): digest both lists into one compact file, have the agent emit
an incremental JSONL pairing table appended after each subject group, then assemble
`unified_properties.yaml` **deterministically with a script**. Then run the mechanical completeness
check and FAIL on any violation:
- every spec id and every code id appears in exactly one `paired_from`;
- no id used twice, no id that exists in neither source;
- `paired + spec_only + code_only + divergent == counts.unified`;
- **no record carries a non-empty `creusot:`/`kani:` block or any `status`.**

That last one matters beyond tidiness: a sweep that wrote a status would poison the gate when the
component is later verified for real.

## Step 2 — validate EARLY, not at the end

The rule this skill adds, learned from a 5-hour run whose setup was wrong from the first minute:
**check the result is sound in the first minutes, on a sample, before committing the batch.** For a
sweep that means running the completeness check on the FIRST component before launching the rest. If
it fails there, the recipe is wrong and every later component would fail the same way.

## Step 3 — the divergence report

Append to `<run-dir>/DIVERGENCES.md`, grouped by component, one line per divergent obligation:
`<id> | <subject> | spec: <FR-…> | code: <file:line> | <what the spec promises vs what the code does>`

Then a short ranking: which components have the most divergences, and which divergences share a root
cause **across** components. That cross-component pattern is the highest-value output a sweep can
produce — two independent implementations of `IEvictionPolicy` shared one handle-design flaw, which
pointed at the shared interface rather than at either implementation. A single-component run cannot
see that.

## Step 4 — hand-off report

Per component: `N`, `spec_total`, `code_total`, `M`, and the split
paired/spec-only/code-only/divergent. Then, across the sweep: total divergences, shared root causes,
and a recommendation of which components to send through `component-verify` first and why.

State plainly, in the report: **no component in this sweep is verified.** The YAMLs are a completed
Step 1 awaiting Role 2.

## Anti-patterns

- ❌ Rendering a scoring page from a sweep. There are no proofs; the page would be all-pending and the
  renderer refuses it. Do not hand-make one.
- ❌ Writing any `status`, `symbol`, `evidence` or fidelity. Scorers own those, and a swept YAML is a
  future gate's input.
- ❌ Committing sweep output to a `verif/*` branch, or pushing anything.
- ❌ Calling a swept component "verified", or counting it in a verified total.
- ❌ Letting an extraction agent see the other source to "improve" the pairing.
- ❌ Weakening `component-verify`, a Role-2 skill, or the gate so a sweep runs faster.
