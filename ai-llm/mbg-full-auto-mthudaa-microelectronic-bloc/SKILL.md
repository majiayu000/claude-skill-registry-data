---
name: mbg-full-auto
description: Fully automated analog design from one request — the /mbg-full-auto command. Parses the specification, runs pre-layout optimization, layout, DRC, LVS, PEX extraction, PEX simulation and PEX-aware fine-tuning, with Devil and Angel reviewers at every stage, then a tapeout-ready sign-off gate and an automatic design report. Use when the user gives a design request and wants it carried through autonomously. Do not use for a single isolated stage (use the stage skills), or for layout with no performance target (use mbg-spice-to-gds).
---
<!-- GENERATED FILE — do not edit by hand. Source: .ai/skills/mbg-full-auto/SKILL.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

# `/mbg-full-auto` — Fully Automated Design

Canonical definitions: `.ai/knowledge/FULL_AUTOMATE.md` and
`.ai/knowledge/DESIGN_FLOW.md`. Read them before deviating.

## Before you read anything: context economy

This repository is big enough that *how* you gather information decides
whether you finish. A measured session here spent **87% of a 1 MB
conversation on tool output** — one file re-read 22 times, `git status`
polled 27+ times, and 33 KB spent searching `$HOME` for a repo whose path
was already in `$MBG_ROOT`. Read `mbg-context-economy` first. The short
version: resolve the repo from `$MBG_ROOT`, index a file before opening it,
never re-read what is already in context, do not poll git state, and climb
the verification ladder cheapest-first. Reading less is the goal; **checking
less is not**.

## Command

```text
/mbg-full-auto "Design a 5T OTA in GF180 with VDD=3.3 V, gain >= 40 dB,
bandwidth >= 100 MHz, phase margin >= 60 deg, power <= 1 mW, CL = 1 pF.
Produce a tapeout-ready package and design report."
```

**All MBG slash commands use `/mbg-*`.** Do not expose generic names for MBG
work: never `/full-auto`, never `/full-design`, never `/review`, never
`/signoff`, never `/report`, never `/status`. Use `/mbg-review`,
`/mbg-signoff`, `/mbg-report`, `/mbg-status` instead.

## What you do

One request in; a tapeout-ready package or a diagnosed failure out. No
stage-by-stage prompting from the user.

1. **Parse the specification.** Track provenance: `given`, `inferred`,
   `defaulted`, `missing`. **Never invent a performance target.** No target
   at all ⇒ `CONFIGURATION_FAILURE` — ask, do not guess.
2. Review the specification (Devil + Angel) *before* designing.
3. **LOOP A** — pre-layout simulate → evaluate → fine-tune → repeat, bounded
   by `max_pre_iterations`. Review each evaluation.
4. Generate layout only once pre-layout passes.
5. **DRC → LVS → PEX extraction.** A failure upstream `SKIP`s everything
   downstream. Review.
6. **PEX simulation** — separate from extraction. Evaluate against the *same*
   targets. Review.
7. **LOOP B** — on a PEX spec miss: read the degradation (worst first),
   choose circuit and/or layout changes, regenerate, re-verify, re-simulate.
   Bounded by `max_pex_iterations` and `patience`.
8. **Final sign-off gate**, then package artifacts and write the report.

## Running it

```python
from mbg import Spec, make_hooks
from mbg.full_auto import run_full_auto, FullAutoConfig, SignoffGate

hooks = make_hooks(cell="ota_5t", in_node="inp", out_node="out",
                   supplies={"vdd": 3.3, "vss": 0.0},
                   spec_names=["gain_db", "bw_hz"])
res = run_full_auto(user_request, hooks,
                    config=FullAutoConfig(outdir="outputs/ota_5t"))

res.status          # SUCCESS | NOT_CONVERGED | BLOCKED | TOOL_FAILURE | ...
res.tapeout_ready   # only True when every gate condition PASSed
res.signoff.table() # the gate, condition by condition
res.report_path     # design report, or non-convergence report
```

## Do not stop after one or two failed attempts

A spec miss starts a **search**, not a shutdown. Continue through the
configured budget until a legitimate termination condition is reached:
all specs pass, budget exhausted, no improvement for `patience` iterations,
every feasible move exhausted, or a tool failure.

Each iteration:

1. propose **several distinct candidates** from the same baseline — different
   hypotheses, not one guessed edit;
2. build and measure each **independently**, so the improvement is
   attributable to one change;
3. promote the winner, archive the near-misses, reject the regressions;
4. if nothing beat the incumbent, **roll back to the best design** and widen
   the search rather than compounding a bad edit.

Size steps from measured sensitivity where it exists, continue a direction
that worked, and bracket it — the design space is not monotonic, and pushing
one metric can break another. Never extrapolate past a measurement.

`FullAutoConfig.for_effort("normal" | "high" | "exhaustive")` sets the budget.

## DRC is dual-engine, automatically

Layout is checked by **both** engines on the same GDS: KLayout (GF180 foundry
deck — the sign-off authority) and Magic (independent complementary check).
You do not request KLayout separately; `spice_to_gds_with_checks` runs both
and records the reconciled verdict.

`PASS` needs both clean and agreeing. `DRC_DISAGREEMENT` (Magic fails,
KLayout clean) blocks sign-off and must be investigated. A missing KLayout or
missing rule deck is `CONFIGURATION_FAILURE` — full sign-off is not possible
without it.

## Complex circuits use the same flow, not a reduced one

There is no separate "simple" path to fall back to. `spice_to_gds_with_checks`
drives the DesignContext flow for every design: constraint-aware placement
with a placement–routing feedback loop, a congestion-aware multi-layer grid
router with rip-up and negotiation, internal connectivity verification, then
dual-engine DRC and LVS. A larger circuit gets more iterations of that, not a
different algorithm.

What to actually do when a design is large:

* **Read the structural metrics before theorising.**
  `tests/test_complexity_ladder.py` prints device count, net count, max net
  degree, matched groups and how many distinct (W, L) pairs the design uses.
  Device count is a poor predictor: the 11-MOS StrongArm comparator and the
  12-MOS clocked comparator have the SAME maximum net degree, and only the
  latter exposed a boundary. Device-size heterogeneity — seven distinct
  (W, L) pairs against one — is what made its floorplan hard.
* **Let the loops run.** `place_with_routability` re-places when routing
  reports unroutable nets, and the router negotiates over
  `ripup_iterations` sweeps. Both are bounded. Raising a timeout is not a
  fix; if the router is not making progress across sweeps, the diagnosis is
  in `ctx.failures` (`cause`, `blocking_instances`, `suggested_action`), not
  in the clock.
* **Read a partial route as partial.** A net may have real geometry and
  still be incomplete: check `RoutedNet.complete` and `RoutePlan.partial`,
  not merely whether segments exist.
* **Internal connectivity gates the expensive tools.** `opens`, `shorts`
  AND `missing_access` must all be zero before Magic, KLayout and netgen are
  worth running. If the internal check already knows the layout is wrong,
  report that — do not spend a DRC/LVS cycle rediscovering it.
* **Preserve the evidence on failure.** Normalised topology, placement
  coordinates, routing failures, internal connectivity report, both DRC
  reports, the extracted netlist and the LVS mismatch. A complex design that
  failed must be diagnosable without re-running it.

Escalation order when a complex design will not route, all bounded:
reroute → alternate layers → placement legalisation → re-placement → broader
search. Report which rung it reached.

## The sign-off gate

`SUCCESS` requires **all** configured conditions to be `PASS`: pre-layout
specs, PEX specs, DRC clean, LVS match, PEX extraction, final GDS, final PEX
netlist, no unresolved `CRITICAL` finding, reviews complete, design report.
PVT corners and Monte Carlo only when configured.

A condition that was not evaluated reads **`NOT RUN`** and fails the gate. It
is never counted as passed, and you must not claim an analysis that did not
run.

## Reviewers cannot be talked around

Precedence: incomplete review ⇒ `ESCALATE`; hard gate failure outranks
everything; unresolved `CRITICAL` blocks; measured evidence outranks
sentiment; reviewer verdicts last. **Critics can block; they cannot approve
past a failed gate.**

## Reporting the outcome

On `SUCCESS`: package + design report, and say `TAPEOUT_READY`.

Otherwise report truthfully — status, failure category, best iteration, which
specs remain unmet and by how much, unresolved CRITICAL findings, which
recommendations were tried and whether they helped, and what manual
intervention you recommend. A well-diagnosed non-convergence is a correct
result; a fabricated success is not.

## Never

- declare success after pre-layout, after DRC/LVS, or because PEX extraction
  completed;
- treat a tool crash as a specification failure;
- present a reviewer's opinion as a verification result;
- invent a specification the user did not state;
- run unbounded;
- use a non-`/mbg-*` command name for MBG functionality.
