---
name: gz-airlock
persona: main-session
description: Use to read a target's seam map before touching it (gz airlock in), account for what a transit disturbed (gz airlock out), or enter ad hoc (gz permitted-entry).
category: governance-infrastructure
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
model: haiku
gz_command: airlock
metadata:
  skill-version: "1.2.1"
---

# gz airlock

## Overview

The airlock is gzkit's entry/exit **membrane** (ADR-0.33.0): the reason for
entry selects the door, but it never decides *whether* the gate fires — every
unit of work crosses it. This skill wields the airlock's operator-facing doors
directly, for the two moments the pipeline and mx doors don't already own:

- **Inspect a target on the way IN** — `gz airlock in` runs the three-beat
  (DECLARE → PING the hull via `gz ontology reach` → RECONCILE) and reports the
  acknowledge-and-decide readout plus the two-layer seam-map (declared bodies ·
  computed push/pull edges · **un-accounted** seams).
- **Account on the way OUT** — `gz airlock out` computes the drift-diff (what a
  transit disturbed vs. what the intent declared) behind a closed decision menu.
- **Ad-hoc / spurious entry** — `gz permitted-entry` crosses the airlock for
  reconnaissance-for-comprehension (light repair at most), so the formerly
  membrane-less ad-hoc surface now leaves an accountable `airlock_in` /
  `airlock_out` L2 transit record instead of silently bypassing.

The airlock is **diagnostic-only**: a NO-GO or a surfaced drift is *reported*,
never a hard block — it always exits 0. It **never writes L1 canon**; it
proposes governed, attested amendments only. Its acknowledge-and-decide gate is
**never** a Gate-5 completion attestation.

## Three subjects (operator ruling, verbatim canon)

Keep three subjects distinct: transit is ecosystem movement through the airlock (ADR-0.33.0); exchange is one block’s occupancy (ADR-0.0.41); handoff is session memory (ADR-0.0.65). Classify by the citing event type, never a shared field name or path. Token blocks implement features through the airlock’s Build door. The airlock provides awareness and synthetic memory, controls project movement, keeps the agent focused and watches for contamination, and monitors results/disturbance; it is not a verification gate. ADR-0.33.0 incompletely captures those purposes; silence does not revoke them. Transit supplies current ecosystem orientation and handoff carries the prior session model; they cooperate, and neither alone supplies a resident project model.

> Carried verbatim from root `AGENTS.md` § Operator Doctrine on 2026-09-17 (GHI #921), and into this surface on 2026-09-24 (GHI #1091, sweep findings S07/S08), where transit, exchange and lock work happens. The corpus `.gzkit/corpus/AGENTS.md.jsonl` keeps the ruling's history.

## When to Use

- Before starting ad-hoc work in an unfamiliar area — cross via
  `gz permitted-entry --recon` to image the seam-map before you touch anything.
- Before/after a transit — inspect a target OBPI's seam-map (`airlock in`) or
  read what the work disturbed (`airlock out`).
- To check whether a target's blast radius carries **un-accounted** seams (a
  real push/pull edge absent from the declared set) before committing to work.

## When NOT to Use

- The pipeline door (`gz obpi pipeline` Stage 1/5) and the mx door
  (`gz mx enter`/`exit`, via the `gz-mx` skill) already call the airlock — do
  not re-cross it manually for those transits.
- To image structural lineage without entering — that is the `gz-ontology`
  sonar (`gz ontology sense/trace/reach`), which this skill's PING beat consumes.

## Output Contract

Human-readable decision + seam-map counts (or drift-diff findings + decision
menu) by default; `--json` for the machine-readable projection. `--dry-run`
previews the membrane WITHOUT booking an L2 transit.

## Workflow

1. Inspect a target OBPI on the way in (preview, no transit booked):

   ```bash
   uv run gz airlock in --target <OBPI-ID> --dry-run
   uv run gz airlock in --target <OBPI-ID> --dry-run --json   # machine-readable
   ```

   `decision: proceed` with `unaccounted=0` means GO is reachable. Any
   `unaccounted` seam makes GO structurally unreachable — the readout names the
   exact seam, its provenance, and a one-command re-sense.

2. Make a governed ad-hoc reconnaissance entry (default; no mutation):

   ```bash
   uv run gz permitted-entry --target <path> --recon
   ```

   The acknowledge-and-decide gate fires on every entry (BI-2). Reconnaissance
   yields a comprehension report and mutates nothing.

3. Light repair is the ceiling — a within-ceiling intent is admitted; anything
   beyond it SURFACES a fresh-transit recommendation (pipeline or mx door) and
   is never smuggled inline:

   ```bash
   uv run gz permitted-entry --target <path> --repair "<light-repair intent>"
   ```

4. Account for what a transit disturbed on the way out:

   ```bash
   uv run gz airlock out --target <OBPI-ID> --dry-run
   ```

   Read the drift-diff verdict, findings + recommendations, and the closed
   decision menu (`leave_it_be | modify | repair | adjust_maps`). Discovered
   corrections route as a FRESH transit through the right door — never inline.

## Boundaries

- **Diagnostic-only FOR NOW — a staged posture, not the contract.** Every verb
  exits 0; a NO-GO or drift is surfaced rather than blocking. That is because
  production reach yields an empty seam-map, so a fail-closed gate would be
  vacuous (parent ADR § Calibration frontier, operator-attested 2026-07-10;
  calibration is "a named successor increment"). The declared end state BLOCKS —
  BI-4, *"an un-accounted seam makes GO structurally unreachable."* Do not read
  the current posture as the design. § Negative #5 governs the *shape* of a
  refusal (name the seam, its provenance, a one-command re-sense; logged and
  revocable override), never whether one blocks; BI-2 governs that the gate
  always fires, never that it always passes.
- **Never writes L1 canon.** The exit membrane proposes attested amendments; it
  never mutates an ADR, invariant, or canon file (BI-1).
- **The gate is acknowledge-and-decide, never completion attestation** (BI-3) —
  it books `airlock_in` / `airlock_out` L2 encounter events only.
- `--dry-run` books no L2 transit — use it for a pure preview.
- Per-door ceremony-weight calibration (tight/corrective/permissive) is an
  attested deferred frontier; today all doors call the one shared primitive in
  the same diagnostic posture.

## Reference

- Manpage: [`gz airlock`](../../docs/user/manpages/airlock.md),
  [`gz permitted-entry`](../../docs/user/manpages/permitted-entry.md)
- Parent ADR: `ADR-0.33.0-airlock-membrane`
- Sibling: `gz-ontology` (the hull sonar the PING beat queries),
  `gz-mx` (the mx door), `gz-obpi-pipeline` (the pipeline door)
