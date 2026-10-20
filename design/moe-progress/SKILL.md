---
name: moe-progress
description: Use when editing the 14th_ua MoE Calculator's two centre-screen TRANSIENT battle bars — the Progress Bar (Moving Average variant) and the Damage Efficiency bar — their radio-alternative gating, MoEProgress.js/.css/.html, MoEProgressVertical.css, MoEEfficiency.js/.css/.html, MoEEfficiencyVertical.css, the shared MoEBarTransient.js fade/hold/peek/size/drag/orientation state machine, bridge/bar_window.py's BarHost/_BarView/_BarWindow, progress_view.py, efficiency_view.py, ProgressVM/EfficiencyVM in view_models.py, the vertical vs horizontal orientation variants, the Default/Large size modes, the Ctrl+drag absolute-placement reposition, and the gen_bar_tuner*.ps1 CSS generators + their check_*.js gates. For the in-battle corner overlay see moe-battle. For the hangar bar see moe-garage. For the MSA controls themselves (Progress Bar / Transitions / Layout groups) see moe-settings. For build/hot-reload of this window (no hot-reload — full relaunch) see moe-build-release.
---

# 14th_ua MoE Calculator — centre-screen transient bars (feature map)

## Boundary (read this first, it is the #1 confusion)

"Progress Bar" in the MSA/UI names the **master checkbox** `progress_bar_enabled` that gates
**both** centre bars. The variant radio `progress_bar_variant` picks which one opens:
**0 = Efficiency (default), 1 = Moving Average**. At most one is ever open —
`battle_bridge._window_gates()` is the single place deciding all
three battle windows. Neither centre bar is the corner in-battle overlay (`MoEBattle.*` /
`battle_view.py`, gated by `BATTLE_KEY`) — that is `moe-battle`. Three coexisting widgets,
not a rename.

## File inventory

| File | Scope | Role |
|---|---|---|
| `MoEProgressView.html`, `MoEProgress.css`, `MoEProgressVertical.css`, `MoEProgress.js` | Progress-only | Moving Average bar front-end |
| `bridge/progress_view.py`, gen_resources view `MoEProgressView` | Progress-only | window instantiation + registration |
| `MoEEfficiencyView.html`, `MoEEfficiency.css`, `MoEEfficiencyVertical.css`, `MoEEfficiency.js` | Efficiency-only | Damage Efficiency bar front-end (mirror) |
| `bridge/efficiency_view.py`, gen_resources view `MoEEfficiencyView` | Efficiency-only | window instantiation + registration |
| `MoEBarTransient.js` | SHARED | fade/hold/peek/size/drag/orientation state machine for BOTH bars |
| `MoEBattle.ttf`, `checker.png` | SHARED | glyph font + halftone backdrop asset, reused from the corner overlay |
| `bridge/bar_window.py` (`BarHost`/`_BarView`/`_BarWindow`) | SHARED | ONE hosting implementation, instantiated once per bar |
| `bridge/battle_bridge.py`, `bridge/view_models.py`, `bridge/mod_settings.py` | SHARED | lifecycle, VM classes, settings getters |
| `adapter/battle_adapter.py`, `adapter/battle_input.py` | SHARED | efficiency read, Ctrl/Alt input sampling |
| `domain/positioning.py`, `domain/battle_builder.py`, `domain/constants.py` | SHARED | placement math, CD/EWMA/axis math, anchor constants |

## Data flow

`battle_bridge._on_efficiency_updated` / `_on_summary_feedback` → `_schedule_refresh()` →
`refresh()` → `battle_adapter.build_battle_snapshot()` →
`build_battle_model(snap)` → `push_progress(bar.viewModel, snap, model)` /
`push_efficiency(eff.viewModel, snap, model)` (all in `battle_bridge.py`). `push_progress`
computes `marks_from_percentile`, `mark_axis`, `ewma_project_raw`, `battles_to_axis_hi`,
`progress_axis_lo`, writing inside `rvm.transaction()`. `push_efficiency` has **no
has-baseline gate**, unlike `push_progress` — its axis is the tank's requirement table alone,
so it doesn't need a career baseline to draw.

## VM slot table — `ProgressVM` (`bridge/view_models.py`), `commands=0` (the `properties=` count is the `__init__` default there — read it, `tests/test_view_models.py` pins it)

| # | field | type | notes |
|---|---|---|---|
| 0 | `visible` | bool | |
| 1 | `marks` | Number | held marks 0..3 |
| 2 | `axisLo` | **Real** | display floor (progress_axis_lo), not the mark's own requirement |
| 3 | `axisHi` | **Real** | requirement chased (the 100 stop at 3 marks) |
| 4 | `preAvg` | Number | career moving-avg combined damage |
| 5 | `projAvg` | **Real** | this battle folded in (EWMA) |
| 6 | `hasData` | bool | mark axis usable |
| 7 | `altHeld` | bool | Alt down → pull bar up (additive trigger) |
| 8 | `barSize` | Number | 0 default / 1 Large |
| 9 | `transEvents` | bool | animate battle-event enter/exit |
| 10 | `transManual` | bool | animate Alt-peek enter/exit |
| 11 | `showEvents` | bool | may a battle event raise the bar at all |
| 12 | `holdMs` | Number | hold duration, default 5000 |
| 13 | `ctrlHeld` | bool | Ctrl down → hold up for reposition |
| 14 | `etaBattles` | Number | battles to `axisHi`, -1 = no data |
| 15 | `vertical` | bool | draw vertical composition |
| 16 | `curPercent` | **Real** | live MoE % shown "(73.84%)" beside the current-damage numeral; **`-1.0` = "setting off / no data"** (0.0 is a real percentile) |

`EfficiencyVM` (`bridge/view_models.py`), `commands=0` (count: read the `__init__` default) — its OWN model,
deliberately NOT sharing ProgressVM's two-end mark axis (it plots ONE battle's combined damage
against ALL FOUR requirement stops):

| # | field | type | notes |
|---|---|---|---|
| 0 | `visible` | bool | |
| 1 | `damage` | Number | this battle's combined damage |
| 2 | `barX` | **Real** | `damage` on the axis, 0..100% (`domain.efficiency_bar_x`) |
| 3 | `band` | Number | 0..4 highest requirement passed (`>=`), selects `.mp-b-{w,g,t,v,au}` |
| 4-7 | `r65`/`r85`/`r95`/`r100` | **Real** ×4 | the four requirement stops |
| 8 | `hasData` | bool | all four requirements present + ascending |
| 9 | `altHeld` | bool | |
| 10 | `battleEpoch` | Number | monotonic per-battle counter, resets the JS damage-delta latch |
| 11 | `barSize` | Number | |
| 12-14 | `transEvents`/`transManual`/`showEvents` | bool ×3 | same wire meaning as ProgressVM's |
| 15 | `holdMs` | Number | |
| 16 | `ctrlHeld` | bool | |
| 17 | `vertical` | bool | |
| 18 | `damagePercent` | **Real** | percentile THIS battle's damage alone is worth, shown "(73.84%)"; **`-1.0` = "setting off / no data"** |

No `damageDelta` slot on Efficiency — the "last increment" caption is derived and latched in
`MoEEfficiency.js` off successive `damage` pushes; adding one would have renumbered every
property after it, which is exactly the hand-maintained-index hazard the module header warns
about (`battleEpoch` was therefore APPENDED, not filed next to `damage`).

Read-polarity rule (both VMs): `vertical`/`ctrlHeld` read `=== true` (fail-soft to horizontal /
not-held — the shipped composition IS horizontal and NOT pinned up); `transEvents`/
`transManual`/`showEvents` read `!== false` (fail-soft to animated / shown). `axisLo`/`axisHi`/
`projAvg` (Progress) and `barX`/`r65..r100` (Efficiency) **must** be `_addRealProperty`/
`_setReal` — `projAvg` moves ~a couple damage points per battle (k≈0.02), and an int truncation
quantises the JS change-detect signal away entirely (this already shipped once as "the bar
never showed").

## DOM + CSS

`MoEProgressView.html`'s static markup is ONLY `<div id="moe-bar-box">` — a sizing shim, sized
to `BOX_W_REM + 2*PAD_REM` × `BOX_H_REM + 2*PAD_REM - CLIP_B_REM` (VIEW_H), mirrored exactly in
`MoEProgress.css`. The box numbers (`BOX_LEFT_REM`/`BOX_TOP_REM`/`BOX_W_REM`/`BOX_H_REM`, `PAD_REM`,
`CLIP_B_REM`) are consts at the top of each bar's JS (`MoEProgress.js`, `MoEEfficiency.js`) with the
derived `VIEW_W_REM`/`VIEW_H_REM` in the header comment above them — read them there, they change
whenever a caption grows (the `%` caption widened Progress's surface), and
`tests/test_progress_surface_mirror.py` / `tests/test_efficiency_surface_mirror.py` pin the CSS
mirror (`.mp-backdrop` and `#moe-bar-box`). `CLIP_B_REM` is a bottom-only trim and never
enters `shiftY`. `#moe-bar-root` is JS-created in `ensureRoot()` (`MoEProgress.js`) and appended
to `document.body` — the box must exist at the FIRST layout
pass or the engine's size calculation has nothing to measure and clobbers the surface (see
Placement below).

Horizontal `MARKUP` (`MoEProgress.js`): per-caption shadow strips, then the track, then the
captions. Progress: `.mp-bd mp-bd-1..3` (-1 behind `capP`, -2 behind `capC` JS-tracked left,
-3 behind `capR` fixed). Efficiency: `.mp-bd-1..5` (-1..-4 at the quarter marks, fixed; -5 behind
`capC`). Then the track (fill + 4 ticks
`mp-end.mp-left`/`mp-right`, `mp-pre`, `mp-proj`), 3 captions `mp-capP` (projected avg) /
`mp-capC` (current combined damage + delta) / `mp-capR` (requirement + eta/battles glyph).
There is NO `.mp-backdrop` DOM node any more; `.mp-backdrop` survives only as an invisible CSS
rule that the mirror tests and `check_eff_css.js` read as the surface bounding-box — keep it.
Order-dependent: `capV()` is a first-match `querySelector` for `.mp-v`, so the mark-pair-first
ordering inside `capR` is load-bearing (`check_progress_js.js`'s `battles-pair-comes-first`
mutation exists exactly to catch a swap here).

Vertical `V_MARKUP` (`MoEProgress.js`): numeral-before-icon, `capR`'s two groups
reordered. Class prefix `.mpv-*`, gated by `body.mpv`. Both stylesheets are `<link>`ed
unconditionally (`MoEProgressView.html`) — orientation is a JS **mount-time branch** on
the `vertical` VM field, not a second registered layout. The two sheets are namespace-DISJOINT (`.mp-*` vs `.mpv-*`); only
`body`, `#moe-bar-box`, `#moe-bar-root` are shared subjects, and `body.mpv` at (1,1,1)
out-ranks the horizontal `.mp-lg #moe-bar-root` at (1,1,0) — the vertical sheet is linked
SECOND so source order also backs it up.

Size: `barSize` → `MoEBarTransient.applySize()` toggles `document.body.classList.toggle
("mp-lg", large)` and rewrites the root font-size, `SIZE_F=1.25`. The `.mp-lg` block
(in `MoEProgress.css`) re-declares ONLY cross-axis (x) lengths at `SIZE_XF=4/3`; y-lengths
ride the root font alone. Double-applying either is the classic bug. `.mp-s1` is a SEPARATE
orthogonal body class for interface-scale legibility (`px > 0 && px < 1.5`); the two combine as
the **compound** selector `.mp-s1.mp-lg` (never descendant).

## Generated-CSS pipeline (exact commands)

```
pwsh tools\dev\gen_bar_tuner.ps1 -EmitCss [-CssOut TASKS/refs/MoEProgress.css]
pwsh tools\dev\gen_bar_tuner_vertical.ps1 -EmitCss [-CssOut TASKS/refs/MoEProgressVertical.css]
```

The emit is written to gitignored `TASKS/refs/`. Shipped `MoEProgress.css` = emit + **2**
hand-additions (marked `ADDITION n OF 2` near the top of `MoEProgress.css` — the `@font-face` and the
`#moe-bar-box` rule). The horizontal emit now carries the per-caption `.mp-bd` strips plus
`.mp-backdrop` as an invisible marker, plus a hand-authored LARGE block (`.mp-lg .mp-bd*`).
Shipped `MoEProgressVertical.css` carries **8** hand-edits (its header says `HAND-EDIT n/8`).
Efficiency's vertical sheet (`MoEEfficiencyVertical.css`) = emit + **5** hand-edits. Never paste a fresh emit over a shipped
sheet — see the memory `emitcss-is-not-the-whole-shipped-stylesheet`.

The Efficiency tuners have **no separate PowerShell generator** — `eff_bar_tuner.html` /
`eff_bar_tuner_vertical.html` are self-contained HTML tuners; the Node checkers evaluate their
`cssOut()` headlessly instead of shelling a `-EmitCss` switch.

Gates, all `node tools\dev\<script>.js`, exit 1 on failure, most support `--probe-all` /
`--list-mutations` / `--mutate=<key>`:
- `check_progress_js.js` — Progress DOM/timing/size/drag-gate assertions against a large,
  named `MUTATIONS` table (each key breaks exactly one real behaviour this bar shipped a bug
  around — read the table itself in the file rather than trust a stale count anywhere else).
- `check_efficiency_js.js` — the Efficiency mirror.
- `check_bar_orientation_js.js` — vertical DOM/surface/run-identity for BOTH bars.
- `check_bar_vertical.js` — pins `cssOut()` byte-for-byte against the checked-in
  `TASKS/refs/MoEProgressVertical.css` (re-run `-EmitCss` after any generator edit or this
  fails on a stale artifact — it is gitignored and absent in a fresh clone).
- `check_vertical_css_handedits.js` — intended: shipped vertical CSS == fresh emit + exactly the
  documented hand-edits, for both bars. **CURRENTLY RED**: out of sync with the vertical CSS's 8
  hand-edits (header says `HAND-EDIT n/8`; the checker encodes 6). Fix in progress.
- `lib/gf_check_shim.js` is the shared harness (assertion helpers `eq`/`ok`, a minimal DOM, a
  virtual clock, the `jsConst`/`jsFactor` scrapers) — not a checker itself.

The hand-edit count lives in each shipped vertical CSS's own header (`HAND-EDIT n/N`); trust that,
not any restated count in a doc.

**Gate honesty:** a green plain `check_*.js` run does NOT prove its probes still catch anything — a
CSS/JS re-anchor can leave a gate vacuously green. After any re-anchor run the checker with
`--probe-all` and confirm every mutation still reports failures.

## Placement / window

`bridge/progress_view.py` builds `BarHost("MoEProgressView", ProgressVM,
PROGRESS_ANCHOR_Y_FRAC, PROGRESS_ANCHOR_X_OFFSET, PROGRESS_ANCHOR_Y_SHIFT,
PROGRESS_ANCHOR_Y_SHIFT_LARGE, PROGRESS_MM_TRACK_X, PROGRESS_MM_TRACK_X_LARGE,
PROGRESS_MM_GAP_BOTTOM, "[moe-bar]")`; `efficiency_view.py` is the byte-identical shape off its
own `EFFICIENCY_*` constants. `BarHost` hosts a `WindowLayer.WINDOW` content-sized window — same
flags/layer reasoning as the corner overlay (`moe-battle`'s hosting-model section): NOT
`WINDOW_FULLSCREEN`, because a full-screen surface steals the whole-screen mouse hit-test
whenever the cursor is raised.

`_resolve()` (`bar_window.py`) has two live top-level branches now, `alignment` reduced
(v23) to `PROGRESS_ALIGN_FIXED` (0, default) / `PROGRESS_ALIGN_FREE` (1) — see `moe-settings`'s
"The Fixed-alignment redesign (v23)" section for the full collapse story and why it shipped.
**Fixed** resolves internally, purely by Orientation: Horizontal → the Damage Log anchor
(`anchor_centred_reduced`, centred horizontally, proportionally down the viewport), Vertical → the
Minimap anchor (`anchor_minimap`, to the left of the minimap, measured to the visible TRACK box for
a vertical bar — no horizontal tuner has a minimap placement at all, since Fixed+Horizontal never
resolves there). `PROGRESS_ALIGN_DAMAGE_LOG` / `PROGRESS_ALIGN_MINIMAP` (both still `0`/`1`) are
INTERNAL anchor selectors now, never a stored `progress_bar_alignment()` value — `_resolve`
branches on `vertical` directly rather than re-testing a locally-assigned "resolved anchor"
variable, because `PROGRESS_ALIGN_MINIMAP` and `PROGRESS_ALIGN_FREE` are BOTH `1` (two different,
never-crossed vocabularies) and re-testing would wrongly match Minimap as Free. The stored X/Y
stepper pair is composed on top of Fixed's anchor via `anchor_offset`; offset (0,0) IS the shipped
placement byte-for-byte, so Fixed needs no sentinel. **Free** is its own third branch, unchanged in
shape from v22 — not composed via `anchor_offset` at all.

**Free's stored pair is an ANCHOR POINT, not a top-left (v22, `TASKS/in-battle-bar-layout-auto-set-redesign.md`
Trap 3 Fix B / DECISION 2 — kept as-is by the v23 redesign).** `domain/positioning.py`'s
`free_top_left(pair, surface, vertical)`
converts it at placement time — bottom-**centre** for horizontal (`pair - (surface_w // 2,
surface_h)`), bottom-**right** for vertical (`pair - (surface_w, surface_h)`) — using THIS
placement's live surface size, so a Default↔Large size flip re-anchors the bar instead of growing
it off to one side (rule 5's size-invariance). `free_anchor_point(top_left, surface, vertical)` is
the exact inverse, used ONLY to write the pair back (`BarHost._materialise`, and `BarHost.drag`'s
gesture-end persist). **The conversion is placement-only, never written back on a size change** —
the engine's compiled clamp (memory `[[engine-clamps-every-wulf-window-to-screen-and-the-mod-depends-on-it]]`)
would bake a crossed-edge clamp in forever if it were. A pre-v22 store's Free pin is still a
literal top-left until the bar's next mount converts it once (`progress_bar_pos_frame() ==
POS_FRAME_LEGACY`, `mod_settings.py`) — no arithmetic migration at bump time, because no
surface exists to convert against outside a live battle (same wall as materialise-on-mount below).

**Free DOES have an auto sentinel (in `BarHost._resolve`, corrected 2026-08-08).** Under
`PROGRESS_ALIGN_FREE` the exact pair `(0, 0)` is rewritten to this ORIENTATION's default alignment
before the branch runs (Horizontal → Damage Log, Vertical → Minimap) — it does NOT mean the screen
corner. That is what lets an explicit Orientation flip zero the stored pair
(`mod_settings._derive_layout` / `_on_changed`) without moving the bar somewhere it was never
tuned for.
The one lost capability is pinning a bar at exactly logical (0, 0) — accepted. This claim has
flipped repeatedly; trust the code, and see
`[[unclamping-drag-is-constrained-by-the-auto-placement-sentinel]]` plus
`TASKS/in-battle-bar-layout-auto-set-redesign.md`, where (0,0) additionally comes to mean
"Free, not yet materialised".

**Materialise-on-mount** (`bar_window.BarHost._materialise`, called from `_place` after every
resolve): the FIRST real-surface placement after Free is picked (or a legacy pre-v22 pin is
upgraded) writes the resolved on-screen point back as the anchor point, so the panel's steppers
stop reading 0/0 the next time the user looks — no numeric change is possible before then, because
no surface exists to compute one from in the garage panel where Free is picked. Three gates, all
load-bearing: `_sized` (the first `_place` at `_onReady` still sees the engine's 256×256
size-timeout fallback surface — materialising against that bakes a wrong anchor point forever),
own-variant only (both bar hosts share ONE stored pair, and a live variant flip mid-battle can
briefly have both open), and the pair/frame re-read fresh rather than reused from `_resolve`'s
locals (which were overwritten in place by the AUTO rewrite).

Ctrl+drag: `adapter/battle_input.py` samples Ctrl+LMB → `battle_bridge._on_drag(phase, cursor)`
→ `progress_view.drag(...)` / `efficiency_view.drag(...)` →
`BarHost.drag()` (`bar_window.py`). **v23: `drag()` refuses the WHOLE gesture outright**
— checked at the very top, before any cursor read or window move, on EVERY phase — while
`progress_bar_alignment() != PROGRESS_ALIGN_FREE`. This is not a spatial gate (see
`[[battle-bar-installdrag-has-no-spatial-gate-by-design]]` for the JS-side one that predates and
is unrelated to this); it is an ALIGNMENT gate, and it exists precisely because MSA cannot make a
peer control's edit flip Alignment to Free for us (see `moe-settings`'s gating vocabulary note) —
so the gesture is blocked instead of letting the bar visibly follow the cursor and then snap back
at gesture end. Absolute placement via `cursor_top_left`
(`positioning.py`), gain exactly 1 (see `_space()`'s derivation), ownership gated by
`cursor_in_rect` against the gesture's own window rect. **`window.move()` still takes the
computed top-left, but what gets persisted (both the live per-move update and the gesture-end
write) is that top-left re-expressed as the Free anchor point via `free_anchor_point`** — the grab
offset stays in top-left space throughout; only the value handed to
`mod_settings.set_bar_position(x, y, persist=True)` is converted, on every move (unpersisted) and
on phase `"end"` (persisted, and only if the gesture actually moved). Both bar VMs are
`commands=0` — no `setPosition` reverse command; the
drag is entirely Python-owned (see `moe-battle`'s Ctrl+drag section for the full mechanics,
shared verbatim by both bars).

Constants (`domain/constants.py`): `PROGRESS_ANCHOR_Y_FRAC=0.865`,
`PROGRESS_ANCHOR_X_OFFSET=0`, `PROGRESS_ANCHOR_Y_SHIFT=-32` / `_LARGE=-48`,
`PROGRESS_MM_GAP_BOTTOM=30`, `PROGRESS_MM_TRACK_X(_LARGE)` (a pure derivation plus a flat measured
-2 hand-placement correction — see the constants' long comment); `EFFICIENCY_ANCHOR_Y_FRAC=0.865`,
`EFFICIENCY_ANCHOR_Y_SHIFT=-45` / `_LARGE=-64`,
`EFFICIENCY_MM_GAP_BOTTOM=28`, `EFFICIENCY_MM_TRACK_X(_LARGE)` (pure derivation, no correction).
**Read the `*_MM_TRACK_X` values in `domain/constants.py` — never restate them**: they are
re-derived whenever a bar surface grows (growth moves the track inside it; the `%` caption growth
re-derived all four), and the Progress flat -2 correction rides on top of the re-derived pure
value. Shared:
`MM_GAP=8`, `MM_TICK_OVERHANG=3`/`_LARGE=5`, `MM_TRACK_Y=290`/`_LARGE=363`,
`VERTICAL_ANCHOR_Y_SHIFT=-90`/`_LARGE=-170` (identical for both bars — both vertical
compositions share the same backdrop geometry).

**Rule: `_LARGE` shifts pin the composition's bottom ink, not `shift*SIZE_F`.** (Current horizontal
values -48/-64; vertical -170 still correct.) The naive algebraic identity pins
neither ink edge — see memory `[[anchor-y-shift-large-pins-neither-ink-edge]]`. These stay live:
rule 5's size-invariance still holds through `anchor_minimap` (Minimap/Fixed+vertical) and
`free_top_left` (Free, either orientation).

**DELETED at v23** (the Fixed-alignment redesign, not merely unreachable): `anchor_centred_
reduced`'s `x_shift` parameter, `BarHost`'s `x_shift_large` constructor argument, and
`PROGRESS_ANCHOR_X_SHIFT_LARGE` / `EFFICIENCY_ANCHOR_X_SHIFT_LARGE`. This machinery existed only
to right-pin a VERTICAL bar resolving to the **Damage Log** anchor under Large (rule 5's X term for
that one combination); it is now structurally unreachable, not just unused — Alignment only ever
stores Fixed or Free (`clamp_variant`'s ceiling is `PROGRESS_ALIGN_FREE == 1`), and Fixed always
resolves to Minimap when vertical (`_resolve`), which was already X-invariant by construction
(`anchor_minimap` subtracts from the full space using per-size TRACK offsets). There is no stored
value or UI path left that can select the old vertical+Damage-Log combination, so the constants,
the parameter and the constructor argument were removed rather than left dead. `VERTICAL_ANCHOR_Y_
SHIFT` / `_LARGE` (the −170 value) are KEPT even though placement no longer reads them for a
centred vertical anchor — the JS files still cite them as a wire-contract record and tests still
pin them against real geometry.

## Settings (keys/getters — see `moe-settings` for the panel itself)

`SETTINGS_VERSION` is in `mod_settings.py` (read it there; 28→29 was a stored-value self-heal;
29→30 and 30→31 were forward structural bumps for the four per-bar caption checkboxes —
`progress_show_percent` / `progress_show_delta` (Moving Average) and `efficiency_show_percent` /
`efficiency_show_delta` (Damage Efficiency), default True; see `moe-settings`). Master `PROGRESS_BAR_KEY="progress_bar_enabled"` (default False), getter
`progress_bar_enabled()`. Variant `PROGRESS_VARIANT_KEY=
"progress_bar_variant"` (0=Efficiency/1=Moving Average). Size `PROGRESS_SIZE_KEY=
"progress_bar_size"` (0=default/1=Large). Orientation `PROGRESS_ORIENTATION_KEY=
"progress_bar_orientation"` (0=Horizontal/1=Vertical). Alignment `PROGRESS_ALIGNMENT_KEY=
"progress_bar_alignment"` (0=Fixed/1=Free as of v23, collapsed from 0=Damage Log/1=Minimap/
2=Free — see `moe-settings`). Visibility children
`PROGRESS_SHOW_EVENTS_KEY`, `PROGRESS_SHOW_ALT_KEY`, `PROGRESS_SHOW_ALWAYS_KEY` (all default
True/True/False), folded by `progress_show_events()` and `progress_alt_held(alt_held)`
("Always" IS a permanently-held Alt, no fourth code path). Transitions
`PROGRESS_TRANSITIONS_KEY` (master) + `PROGRESS_TRANS_EVENTS_KEY` + `PROGRESS_TRANS_MANUAL_KEY`
(all True) folded by `progress_transitions_events()`/`progress_transitions_manual()`. Hold slider `PROGRESS_HOLD_SECONDS_KEY` 1–30s default 5 →
`progress_hold_seconds()` — deliberately NOT master-folded (a duration, not a switch). Position
`BAR_POS_X_KEY="progress_bar_pos_x"` / `BAR_POS_Y_KEY="progress_bar_pos_y"` →
`bar_pos_x()`/`bar_pos_y()`/`set_bar_position()`. Every one of these is shared by both bars.
`battle_bridge._window_gates()` folds `progress_bar_enabled()` × `progress_bar_variant()`
into the two centre-bar entries — keep any new gate in lockstep there.

## Tests

`python -m pytest -q` (repo root, Python 3.13). Progress/Efficiency-relevant:
`tests/test_progress_bar_domain.py`, `tests/test_progress_bridge.py`,
`tests/test_progress_surface_mirror.py`, `tests/test_efficiency_axis.py`,
`tests/test_efficiency_bridge.py`, `tests/test_efficiency_surface_mirror.py`,
`tests/test_bar_window.py` (shared `BarHost`, both bars), `tests/test_battle_input.py`,
`tests/test_battle_bridge_settings.py`, `tests/test_mod_settings.py`,
`tests/test_view_models.py` (derives `properties=` counts from source — the ONE place that
catches a slot append without the matching bump). Plus the Node checkers above.

## Gotchas

### Orientation flip is not live-stylable
The JS branches on `vertical` only at mount, so a live radio change must close+reopen the
window via `battle_bridge.apply_settings()` (which diffs
`_bar_orientation` against the freshly-read setting), not just re-push the VM.

### `_extent()` is a real window MOVE
Far-sentinel `window.move(1<<20, 1<<20, ...)` (`bar_window.py`) — memoize it, invalidate
only in `_place()`. `BarHost.drag()` must read `window.position` BEFORE calling `_extent()`
(`bar_window.py`) or a cold cache teleports the window to the sentinel first.

### `#moe-bar-box` does not defeat the size-calculation timeout
The engine's "Size calculation timeout" fallback (256×256) runs LAST and wins even with the box
present, in-flow, and correctly sized — the JS's post-deadline `SURFACE_REASSERT_MS` re-assert
is the real fix, and the bar must stay hidden (`surfaceSettled`) until the surface lands or it
renders cropped ~142px too high.

### VM `properties=` must be bumped with every appended field
Rule: the LAST append moves — every new slot is appended at the end and bumps that VM's `properties=`
in the same edit (see the slot tables above for what is last now; do not restate the count).
`test_view_models.py` derives the count from source and
does catch a mismatch — the push tests' fake VM ignores the declared count and cannot.

### The two bars share `#moe-bar-root` and the `.mp-*` namespace
They avoid collision only because they are radio alternatives — never assume they compose or
can both be open (each host still keeps its OWN `_active` singleton so a live variant switch can
open one before the other closes).

### Vertical surface must stay concentric with its track
`anchor_centred_reduced` has no x term, so widening one side of a vertical surface alone re-aims
the whole bar — mirrored in three places (both JS files' `V_PAD_X_REM`/shift derivations, one in
document rem, plus the shared `VERTICAL_ANCHOR_Y_SHIFT` constant). Read `V_PAD_X_REM` in each bar's
JS; never restate it here.

### The vertical Efficiency bar has no clip-invariance gate yet
The vertical Moving Average bar shipped a real clip on its bottom row once, caught only by
manually opening the tuner artifact and running its in-browser digit-count invariance check
(`checkCaptionInvariance()` in `gen_bar_tuner_vertical.ps1`, headless-SKIPped by
`check_bar_vertical.js`/`test_progress_surface_mirror.py`). The equivalent check exists inside
the Efficiency tuner's own `selfCheck()`, but nothing yet asserts a live clip bound the way the
Moving Average side does — treat a vertical Efficiency layout change as unverified until you
open the artifact and press Self-check.

## Efficiency delta section

Beyond the VM/DOM/settings tables above (already Efficiency-inclusive), the Damage Efficiency
bar's own quirks: its bottom row has **two icon-Y knobs** in the tuner (`eff_bar_tuner.html`) —
`icoyReq` moves the three requirement-tick icons, `icoyBm` the r4/goalpost glyph, `icoyCur` the
current-damage top-row icon; these are tuner-only constants baked into the emitted CSS, not
exposed at runtime. `band` selects one of five CSS classes `.mp-b-{w,g,t,v,au}` (white/green/
teal/violet/gold — 0..4 requirements passed). `barX` is computed by
`domain.battle_builder.efficiency_bar_x` over the four equal-quarter stops
`EFFICIENCY_BAR_STOPS=(0,25,50,75,100)` (`constants.py`) — do not recompute the axis mapping
in JS. `battleEpoch` (slot 10) is the only field with no Progress equivalent: a monotonic
per-battle counter Python bumps before the first `refresh()` each battle
(`battle_bridge.py`), letting `MoEEfficiency.js` reset its own damage-delta latch on a
battle boundary without a dedicated VM reset command.
