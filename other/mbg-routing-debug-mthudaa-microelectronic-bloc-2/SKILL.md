---
name: mbg-routing-debug
description: Traces nets, inspects vias and metal-layer usage, and detects shorts, opens, and route conflicts using the DesignContext grid router and internal connectivity checker. Use when a route failed, a net looks shorted or open, or you need to verify physical connectivity against the SPICE netlist before external DRC/LVS signoff. Do not use it to change the router implementation or to run external Magic/netgen signoff — that is mbg-ic-verify.
license: Apache-2.0
compatibility: opencode
metadata:
  owner: huda
  project: microelectronic-block-generator
  status: experimental
---
<!-- GENERATED FILE — do not edit by hand. Source: .ai/skills/mbg-routing-debug/SKILL.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

# MBG Routing Debug

## Purpose

Diagnose routing failures and internal connectivity problems using the
`DesignContext` grid router in
`src/mbg/router.py` and the connectivity
checker in `src/mbg/connectivity.py`. Read both files before relying on any
claim below — this is a map for orienting a debugging session, not a
substitute for the current source.

Note: there are two routing implementations. `src/mbg/router.py` — the
DesignContext grid router this skill describes — is what
`spice_to_gds_with_checks()` drives by default. `src/mbg/routing.py`'s
`auto_router`, a fixed I/L/Z/U shape-catalogue router, runs only when the
caller passes `legacy=True` or calls `spice_to_gds_with_checks_legacy()`.
The two have unrelated failure models, so confirm which one produced the
layout you are debugging before applying anything below.

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
  does not modify `src/mbg/router.py` (owned by Huda).

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
from mbg import connectivity

result = connectivity.verify(ctx, stage="routing", spacing=True, vias=True)
# result: {opens, shorts, anonymous, drc, missing_access, clean,
#          open_details, short_details, drc_details,
#          missing_access_details, netlist_consistency}
```

- **Opens** (`check_opens`) — a net whose committed geometry does not form
  one connected physical cluster.
- **Shorts** (`check_shorts`) — two or more *different* nets whose geometry
  lands in the same connected cluster (built by
  `connectivity.build_physical_graph`, which unions touching shapes
  regardless of declared net).
- **Anonymous geometry** (`check_anonymous_geometry`) — any segment or via
  with no net owner; always a bug, never expected.
- **Missing access points** (`compare_with_netlist`, folded into `verify()`)
  — a SPICE terminal the layout never gave a `PinAccessPoint` to. It produces
  no shape, so it joins no cluster, so `check_opens` cannot see it: opens can
  read 0 while a device terminal is entirely unconnected. `verify()` counts
  it and `clean` is False when it is non-zero. Report `missing_access`
  alongside opens and shorts; a "0 opens" claim without it is incomplete.
- `verify()` also records every finding onto `ctx` via `ctx.add_violation`
  so a later pass can see accumulated violations, not just this call's
  return value.

This is a fast internal check, not a substitute for signoff — route `ctx`
through `mbg-ic-verify` for the authoritative result, which is dual-engine:
KLayout running the GF180 foundry deck is the DRC sign-off authority, Magic
is the independent complementary check, and netgen does LVS. A clean
internal `verify()` is a precondition for spending time on those tools, not
a substitute for them; equally, never report DRC from Magic alone.

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

### 7. Complexity: what changes as circuits get larger

The framework's first hard complexity boundary was found with a 12-MOS
two-stage clocked comparator (`tests/netlists/cmp_2stage_clk.spice`). The
lessons generalise, and the mechanisms below are the ones to check first
when a bigger circuit misbehaves.

**Device count and net degree do not predict difficulty.** The 11-MOS
StrongArm comparator has the same maximum net degree — 12 device terminals
on `vdd`, 16 counting the power-rail taps — as the 12-MOS clocked comparator
that failed, and it passed throughout. What separated them was device
GEOMETRY: every other reference block uses one or two distinct (W, L) pairs,
while the clocked comparator uses seven across twelve devices. Heterogeneous
sizing produces heterogeneous tap rings and row heights, and it was that
placement in which some `body` terminals could find no legal via landing.
Do not reach for "too many devices" as an explanation; measure.

**Multi-terminal nets are the normal case, not the exception.** A supply net
gains a terminal per device, so `vdd` on a 12-MOS block is a 16-terminal net
before the power-rail taps are counted. `route_net()` grows a Steiner-like
tree: it seeds from one terminal group and attaches each remaining group to
the nearest point already on the tree, so the net ends as ONE connected
conductor rather than a bundle of independent point-to-point routes that
could overlap each other. `terminal_groups(net)` is what enumerates them;
one logical terminal contributes one group, not one per N/E/S/W port.

**A net is no longer all-or-nothing.** `route_net()` returns
`(plan, failure)` and BOTH may be set. A terminal that cannot be reached —
whether it has no legal via landing or the A* search is blocked — leaves the
rest of the net routed, the net marked `complete=False`, and the failure
recorded. Before this, one unreachable terminal discarded every terminal of
the net, so the blast radius scaled with net degree, which is what scales
with circuit size. When debugging, check `RoutePlan.partial`: real geometry
with `complete=False` means a partial route, not a clean one.

**Same-net proximity has a precise rule, not a blanket one.** See §6 for the
general statement. The refinement that matters at scale: metal that
OVERLAPS a same-net shape merges with it, and a near-miss against another
same-net shape is legal only when the facing slot between them is covered by
same-net metal the new shape merges with (`router._rects_cover`). A gLayout
tap ring arrives as a wide band plus the contact pads it contains, so an
escape drawn on the band is within min-spacing of pads the band itself
encloses — no gap exists after the boolean merge, and rejecting it strands
every `body` terminal on the device. A slot nothing fills is still a
violation.

**Widths and pitch are per-layer.** `width_for(net)` is chosen before a path
exists and returns the ACCESS layer's width for the whole net;
`_emit_segment` raises each segment to its own layer's minimum. GF180's top
metal is the one that differs (MT.1 = 0.44um against 0.28um for met2-met4),
so a net routed at the access width and sent over met5 is a guaranteed width
violation. The grid pitch is likewise per-layer, and comes from
`grid_params()` — which `GridRouter` and `power.py` both use, so the rails
and the routes are on one grid.

**Notch fills cover net-owned metal, not just routes.** Power-rail via drops
and device tap metal are net-owned obstacles, never segments.
`_same_net_notch_fills` pairs each segment against its own net's obstacle
metal as well as against other segments, and refuses any fill that would
overlap another net.

Useful complexity metrics, and the ladder that reports them, live in
`tests/test_complexity_ladder.py`. Run it for the structural table before
theorising about why a design is hard.

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
- Applying findings from the DesignContext router (`src/mbg/router.py`) to a
  layout that was actually produced by the legacy shape router
  (`src/mbg/routing.py`'s `auto_router`, reached only via `legacy=True`) —
  the two have unrelated failure models; confirm which one ran
  (`mbg-repo-analysis`).
- Reporting internal connectivity as clean from `opens` and `shorts` alone.
  A terminal with no access point is invisible to both; read
  `missing_access` too.
- Explaining a failure on a larger circuit by device count. Check the
  structural metrics first — the known boundary was triggered by device-size
  heterogeneity, not by size.
