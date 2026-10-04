---
name: mbg-placement-debug
description: Inspects analog device placement — matching groups, symmetry constraints, device bounding boxes and overlap, pin access points, reserved zones, routing channels, congestion, and the placement-routability feedback loop. Use when a layout's device placement looks wrong, a net cannot find a routable path, or you need to explain why the placer chose a given floorplan. Do not use it to change the router or to generate a new layout end to end.
metadata:
  short-description: Inspects analog device placement — matching groups, symmetry constraints, device bounding boxes and overlap, pin access points, reserved zones, routing…
---
<!-- GENERATED FILE — do not edit by hand. Source: .ai/skills/mbg-placement-debug/SKILL.md. Regenerate with: python3 scripts/sync_agent_tools.py -->

# MBG Placement Debug

## Purpose

Diagnose why an analog placement looks the way it does, or why it is not
routable, using the `DesignContext`-based placement engine in
`src/mbg/placement_engine.py` and the data
model in `core/design_context.py`. Read both files before relying on any
claim in this skill — placement logic changes, and this is a map, not a
copy.

Note: this engine is the newer of two placement implementations in the
repo (see `mbg-repo-analysis`). The legacy `mbg.placement.placement()`
path used by `spice_to_gds`/`spice_to_gds_with_checks` has a different,
simpler model; confirm which path produced the layout you are debugging
before applying findings from this skill.

## When to Use

- A device sits somewhere unexpected, or two devices overlap.
- A net fails to route and you suspect the cause is placement (no
  accessible pin, insufficient channel width) rather than the router
  itself.
- You need to explain a matching-group or symmetry decision (why two
  transistors in a differential pair ended up where they did).
- You need to check whether trial-routing feedback changed the floorplan
  across placement attempts.

## When Not to Use

- Debugging an already-placed, already-attempted route's pathfinding,
  vias, or metal usage — use `mbg-routing-debug`.
- Changing placement weights or algorithm behavior — this skill explains,
  it does not modify `core/placement_engine.py` (owned by Huda; read
  `mbg-extension-authoring`'s ownership rules before proposing an edit).
- Running the full pipeline — use `mbg-spice-to-gds`.

## Required Inputs

- A `DesignContext` (`ctx`) already populated via
  `mbg.spice_parser.build_design_context`, or a netlist to build one from
  (see `mbg-repo-analysis`).
- Optionally, a `PlacementConfig` used for the run in question, if
  non-default weights were passed.

## Preconditions

- Placement must have actually run (`mbg.placement_engine.place` or
  `place_with_routability`) so that `ctx.placements`, `ctx.access_points`,
  and `ctx.obstacles` are populated — inspecting an empty context only
  tells you what the netlist says, not what was placed.

## Workflow

### 1. Matching groups and symmetry constraints

`ctx.matching_groups` (dict of `MatchingGroup`) records which devices must
be laid out identically — `kind` is `"diff_pair"`, `"current_mirror"`,
`"cascode"`, or `"generic"`, with a `devices` list and a `symmetric` flag.
`SymmetryConstraint` records a pair (or self-symmetric singleton) that must
straddle or sit on a symmetry axis. These are inferred structurally by
`build_design_context` from the netlist (shared source/gate, matched
geometry) — nothing is invented from styling or naming conventions.

Placement gives matching/symmetry heavy weight by default:
`PlacementConfig.w_symmetry` (25.0) and `w_matching` (10.0) dominate
`w_wirelength` (1.0) and `w_congestion` (2.0) — if a placement looks
wirelength-suboptimal, check whether a matching or symmetry constraint
explains the choice before calling it a bug.

### 2. Device bounding boxes and overlap

Each placed device has a `Placement` (`instance`, `x`, `y`, `orientation`,
`row`) in `ctx.placements`, and real per-layer geometry is harvested into
`ctx.obstacles` as `Obstacle` records (`layer`, `bbox`, `owner`, `kind`,
`net`) by `harvest_obstacles` in `placement_engine.py`. Use
`BoundingBox.overlaps()` to check two devices' footprints; `harvest_obstacles`
already does per-net attribution via connected-component analysis of
touching polygons, so a "collision" between same-net metal is expected
(merging is legal — see the overlap-or-clear rule in `mbg-routing-debug`)
while a collision between different nets is a real problem.

### 3. Pin access points — read from the TRANSFORMED reference only

`PinAccessPoint` (`instance`, `terminal`, `net`, `layer`, `x`, `y`,
`orientation`, `port`, `direction`, `width`) is the physical routing
handle for one logical terminal. The critical rule, stated directly in
`design_context.py` and enforced by `harvest_access_points` in
`placement_engine.py`: **coordinates must always be read back from the
transformed (moved) device reference, never cached from before a move.**
`harvest_access_points` is called strictly after the reference is placed,
and the placer re-harvests any time it moves something. If you find stale
or inconsistent access-point coordinates, look for a place in the calling
code that read `ref.ports` before a move rather than after — that is
exactly the class of bug this rule exists to prevent.

A `PinAccessPoint.footprint(min_width)` treats the port as the edge it
actually is (it spans `width` along the device face), not a point — a
common placement/routing bug is treating a port as a point and getting a
via pad that silently overlaps the neighboring terminal's metal.

### 4. Reserved zones and routing channels

`Zone` (`kind`: `"device_local"` / `"dnw"` / `"guardring"` / `"power"`,
`bbox`, `layers`, `owner`, `net`) marks protected areas the router must
respect. Channel spacing is controlled by `PlacementConfig`:
`channel_x` (gap between clusters in a row, default 3.0),
`channel_y` (gap between rows, default 6.0), `intra_cluster_gap` (default
1.0), and hard ceilings `max_channel_x` (14.0) / `max_channel_y` (24.0).
If placement looks unnecessarily spread out, check whether
`place_with_routability` already widened channels in response to routing
failures (see step 6) — that is deliberate, not a bug.

### 5. Congestion

`ctx.routing_congestion` is a `CongestionMap` (`add_demand`, `at`, `ratio`,
`hotspots`, `max_ratio`, `avg_ratio`) built from committed segments after
routing. `hotspots(threshold)` returns `BoundingBox` regions where demand
exceeds capacity — cross-reference these against `Zone`/`Obstacle` data to
see whether a hotspot is caused by insufficient channel width or by devices
themselves crowding the region.

### 6. The placement-routability feedback loop

`place_with_routability(ctx, pdk, cfg, router_cfg)` in
`placement_engine.py` is the loop that ties placement to actual routing
outcomes:

1. Call `place(ctx, pdk, cfg)`.
2. If `cfg.trial_route` is true (default), run a trial `GridRouter` pass.
3. Build a `PlacementFeedback` (`unrouted_nets`, `congestion_regions`,
   `inaccessible_pins`, `excessive_detours`, `failures` — a list of
   `RoutingFailure`). `PlacementFeedback.clean` is true only when there are
   no unrouted nets, no inaccessible pins, and no failures.
4. If not clean and attempts remain (`cfg.max_placement_attempts`, default
   3), widen `channel_x` (x1.6) and `channel_y` (x1.5) up to the max
   ceilings, call `ctx.clear_routing()`, and retry from step 1.
5. Return `(component, feedback)` — a non-clean `feedback` after the final
   attempt means the design was placed but is not fully routable; do not
   report it as a routing success.

Each `RoutingFailure` carries a structured `cause` (`NO_PIN_ESCAPE`,
`BLOCKED`, `CONGESTED`, `NO_LEGAL_VIA`, `SEARCH_EXHAUSTED`) and a
`suggested_action` — read these directly instead of re-deriving a
diagnosis from raw geometry.

## Outputs

- Which matching/symmetry constraints governed a given placement decision.
- Whether an apparent overlap is same-net metal merging (legal) or a real
  cross-net collision.
- Confirmation that access points were harvested post-transform, or
  identification of a stale-coordinate bug.
- Which channel/zone reservations exist and whether they were widened by
  the feedback loop.
- Congestion hotspots and their likely cause.
- The `PlacementFeedback` from the most recent `place_with_routability`
  call, with `RoutingFailure.cause` and `suggested_action` reported
  verbatim per failing net.

## Failure Modes

- Reading `ref.ports` before the device reference was moved and reporting
  coordinates as if they were final — this is the exact class of bug
  `harvest_access_points`'s post-transform rule exists to prevent.
- Treating a same-net obstacle overlap as a bug — check net attribution
  first (see `mbg-routing-debug`'s overlap-or-clear rule).
- Calling a design "placed successfully" when `PlacementFeedback.clean` is
  false after the final attempt.
- Confusing the legacy `mbg.placement.placement()` output (a plain
  `port_map`, no `MatchingGroup`/`PinAccessPoint`/`PlacementFeedback`
  structures) with this engine's `DesignContext` output — they are not the
  same data model; check which one actually produced the layout in
  question, per `mbg-repo-analysis`.
