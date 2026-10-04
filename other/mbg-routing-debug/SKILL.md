---
name: mbg-routing-debug
description: Traces nets, inspects vias and metal-layer usage, and detects shorts, opens, and route conflicts using the DesignContext grid router and internal connectivity checker. Use when a route failed, a net looks shorted or open, or you need to verify physical connectivity against the SPICE netlist before external DRC/LVS signoff. Do not use it to change the router implementation or to run external Magic/netgen signoff — that is mbg-ic-verify.
---
<!-- GENERATED FILE — do not edit by hand. Source: .ai/skills/mbg-routing-debug/SKILL.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

# MBG Routing Debug

## Purpose

Diagnose routing failures and internal connectivity problems using the
`DesignContext` grid router in
`src/mbg/router.py` and the connectivity
checker in `core/connectivity.py`. Read both files before relying on any
claim below — this is a map for orienting a debugging session, not a
substitute for the current source.

Note: `core/router.py` is the newer of two routing implementations (see
`mbg-repo-analysis`). `core/routing.py`'s `auto_router` — a fixed I/L/Z/U
shape-catalogue router — is what the currently-used design-script path
(`spice_to_gds` / `spice_to_gds_with_checks`) actually calls; confirm which
path produced the routing you are debugging before applying this skill's
findings, since the two engines have different failure models entirely.

## When to Use

- A net failed to route, or the router reports fewer routed nets than
  expected.
- You suspect a short (two different nets electrically merged) or an open
  (a net's committed geometry is not one connected piece).
- You need to check via legality or metal-layer policy compliance before
  handing a layout to external DRC/LVS.
- You want to verify physical connectivity against the SPICE netlist as a
  fast internal pre-check.

## When Not to Use

- Explaining why a device ended up somewhere or why a channel was too
  narrow — that is placement, not routing; use `mbg-placement-debug`.
- Running external Magic DRC or netgen LVS — use `mbg-ic-verify`;
  `mbg.connectivity.verify` is a fast *internal* check that signoff then
  confirms, not a replacement for it.
- Changing router weights or algorithm behavior — this skill explains, it
  does not modify `core/router.py` (owned by Huda).

## Required Inputs

- A `DesignContext` (`ctx`) after routing has run (`GridRouter(ctx,
  cfg).run()` and `realize(ctx, component, cfg)`), so that `ctx.segments`,
  `ctx.vias`, `ctx.routed_nets`, and `ctx.failures` are populated.

## Preconditions

- Routing must have actually executed; inspecting a context with no
  segments/vias only tells you what was planned, not what happened.

## Workflow

### 1. Net tracing

`ctx.routed_nets` is a dict of `RoutedNet` (`net`, `plans: List[RoutePlan]`,
`complete: bool`). Each `RoutePlan` holds `segments: List[Segment]` and
`vias: List[Via]`, plus `detour_factor` and `manhattan_min` for judging
route quality (`RouterConfig.detour_limit`, default 4.0, is the threshold
`place_with_routability` uses to flag `excessive_detours`). A net is only
reported complete when its **committed geometry is actually one connected
conductor** — `GridRouter._confirm_connectivity()` runs
`connectivity.build_physical_graph` after routing specifically to catch a
stranded terminal that the search alone would have reported as success;
trust `RoutedNet.complete`, not just whether a `RoutePlan` exists.

### 2. Via inspection

Every `Via` (`net`, `x`, `y`, `lower`, `upper`, `size`) always carries its
owning net — never treat an anonymous via as safe (see
`connectivity.check_anonymous_geometry`, which reports any segment or via
with no net owner as a `PORT_MISMATCH` violation). `connectivity
.check_via_legality` checks two things independently: enclosure (`v.size`
against the PDK's required cut pad from `rules.via_stack_between`) and
cut-to-cut spacing against vias of a *different* net within the PDK's
`cut_spacing`. A via failing enclosure and a via failing spacing are
different `DRCViolation.rule` values (`*_ENCLOSURE` vs. `VIA_SPACING`) —
report which one actually fired.

### 3. Metal-layer policy

`RouterConfig.routing_layers` (default `["met3", "met4", "met5"]`) and
`access_layer` (default `"met3"`) are the explicit layer policy: general
routing deliberately stays off device-local metals unless a layer is
listed here. If you see routing on an unexpected layer, check whether
`routing_layers` was overridden for that run before assuming a bug.
`power_width_multiplier` (default 2.0) widens power/ground routes relative
to `width_multiplier` (default 1.0) for signal nets — a "wide trace" on
VDD/VSS is expected, not evidence of a stuck config.

### 4. Occupancy and negotiated congestion

`OccupancyDB` tracks, per `(layer, cell)`, hard blockage (`is_hard`,
`hard_owner_of`), soft claims by net (`claim`, `owner`, `blocked_for`), and
a cost model (`cost_of`) that factors in current + historical congestion
(`bump_history`, `penalise`). `GridRouter.run()` performs up to
`RouterConfig.ripup_iterations` (default 8) negotiation sweeps: after each
failed sweep it penalizes the blocking region on every layer and
bumps history, then reorders so nets that failed get first pick next
sweep. Reading `ctx.failures` after only the *first* sweep will
overstate how bad the routing actually is — check `result["iterations_used"]`
and look at the final `best_plans`/`best_failures`, not an intermediate
sweep.

### 5. Detecting shorts and opens with `mbg.connectivity.verify`

```python
from core import connectivity

result = connectivity.verify(ctx, stage="routing", spacing=True, vias=True)
# result: {opens, shorts, anonymous, drc, clean,
#          open_details, short_details, drc_details}
consistency = connectivity.compare_with_netlist(ctx)
```

- **Opens** (`check_opens`) — a net whose committed geometry does not form
  one connected physical cluster.
- **Shorts** (`check_shorts`) — two or more *different* nets whose geometry
  lands in the same connected cluster (built by
  `connectivity.build_physical_graph`, which unions touching shapes
  regardless of declared net).
- **Anonymous geometry** (`check_anonymous_geometry`) — any segment or via
  with no net owner; always a bug, never expected.
- `verify()` also records every finding onto `ctx` via `ctx.add_violation`
  so a later pass can see accumulated violations, not just this call's
  return value.

This is a fast internal check, not a substitute for Magic/netgen signoff —
route `ctx` through `mbg-ic-verify` for the authoritative DRC/LVS result
once internal `verify()` is clean.

### 6. The overlap-or-clear rule — same-net proximity is NOT automatically DRC-clean

`connectivity.check_spacing`'s own comment states the rule precisely: for
two pieces of *different-net* metal on the same layer, proximity below the
PDK's `rules.min_spacing(layer)` is a real `*_SPACING` violation. For
*same-net* metal, merging (i.e., actual physical overlap/connection) is
legal by design — but that does **not** mean any same-net proximity is
automatically fine. `check_spacing` explicitly skips the pair only when
`neti == netj`; it does not skip a same-layer pair that merely happens to
be close if any part of the comparison involves a different net, and it
does not, by itself, tell you whether a "merge" was intentional routing
geometry or an accidental short that got mis-attributed to one net during
obstacle harvesting (see `mbg-placement-debug`'s note on
`harvest_obstacles` net attribution — ambiguous same-region multi-net
metal is deliberately left unattributed rather than guessed). Always cross-
check a same-net "clean" result against `check_shorts`' cluster analysis
rather than assuming same-net proximity alone proves correctness.

## Outputs

- Whether a net's `RoutedNet.complete` reflects one truly connected
  conductor, with the `RoutingFailure.cause` and `suggested_action` for any
  net that failed.
- Which `DRCViolation.rule` (spacing vs. via enclosure vs. via spacing) or
  `LVSViolation.kind` (`OPEN`, `SHORT`, `PORT_MISMATCH`) applies, with the
  specific nets and layer involved.
- The result of `connectivity.verify()` and `compare_with_netlist()`,
  reported field-by-field — never collapse this to a bare "clean"/"not
  clean" without the counts.
- Which routing-layer policy was in effect for the run being debugged.

## Failure Modes

- Reporting a net as routed because a `RoutePlan` exists, without checking
  `RoutedNet.complete` (which `_confirm_connectivity` can flip to `False`
  after the fact).
- Treating same-net metal proximity as proof of correctness without running
  `check_shorts` — see the overlap-or-clear rule above.
- Reading `ctx.failures` after an early negotiation sweep instead of the
  final result from `GridRouter.run()`.
- Confusing this skill's fast internal `connectivity.verify()` with actual
  DRC/LVS signoff — always route final claims through `mbg-ic-verify`.
- Applying findings from the DesignContext router (`core/router.py`) to a
  layout that was actually produced by the legacy shape router
  (`core/routing.py`'s `auto_router`) — the two have unrelated failure
  models; confirm which one ran first (`mbg-repo-analysis`).
