---
name: moe-battle
description: Use when editing the 14th_ua MoE Calculator's IN-BATTLE live-MoE overlay — how it is hosted as a registered Gameface window over the HUD, its arena lifecycle, the Alt-key peek mode, the BattleMoEVM channel, the combined-damage/EWMA math, the Counted Assistance third row, the MoEBattle.js/.css/.html DOM, its colours/font/checker backdrop, or the window placement/anchors. Overlay visibility is settings-gated — see moe-settings. For the hangar bar see moe-garage. For the two OTHER centre-screen transient battle windows — the Progress Bar (Moving Average) and the Damage Efficiency bar, and the shared MoEBarTransient.js/BarHost they ride — see moe-progress.
---

# MoE Calculator — in-battle overlay (feature)

A live combined-damage / projected-MoE readout floated over the battle HUD. Reusable
patterns: `wotmod:gameface-widget` (front-end), `wotmod:architecture` (Python +
`references/game-api.md` "Battle HUD / efficiency"), `wotmod:debug-repl` (live probing).
All paths under `src/res/`.

## Hosting model (the hard-won part)

You **cannot** `gf_mod_inject` a garage-style sub-view overlay into the battle HUD: there is
no shared full-screen Gameface document — each WG battle Gameface view is Flash-composited at
its own placeId. Instead the mod **registers its own view** and opens it as a window:

- **Register** — WG-native resources (client 2.4.1+): `src/res/gui/gen_resources/com.14th_ua.moe_calculator.json`
  declares `R.mods.com_14th_ua_moe_calculator.views.MoEBattleView` (`type "Layout"`, `impl "gameface"`, points at
  `MoEBattleView.html`), plus the two bar views. Ships **inside** the `.wotmod`; no restart. (The old
  OpenWG `mods/configs/res_map` + `ModDynAccessor` path is dead on 2.4.1 — always resolves `-1`.)
- **Resolve layoutID** — `bar_window.layout_id("MoEBattleView")` → `R.mods.dyn(...).dyn("views").dyn(name)()`;
  returns `-1` (logged once via `LOG_PROD`, window skipped) if unresolved. **Do not hard-code the numeric id.**
- **Window** — `MoEBattleView(ViewImpl)` (its root VM is `BattleMoEVM`) inside
  `MoEBattleWindow(WindowImpl)` at **`WindowLayer.WINDOW` (7)**, `show(focus=False)`.
  - `WindowLayer.OVERLAY` (11) sits **above** the modal in-battle menu (`INGAME_MENU`, TOP_WINDOW 10) and made our window the keyboard sink → menu starved. WINDOW (7) sits below the menu but above the battle MainView. **This is the WINDOW-vs-OVERLAY input-steal rule.**
  - **Content-sized, NOT `WINDOW_FULLSCREEN`.** `pointer-events:none` only stops our own DOM being an event target — it does **not** make the window rectangle click-through to the engine's cross-surface hit-test. A full-screen surface stole the mouse whenever the cursor was raised (Ctrl). Dropping fullscreen shrinks the surface to the small readout box so the minimap/markers stay live.

## Lifecycle

`mod_moe_calculator.py::_install_battle()` arms `bridge/battle_bridge.py::install_all_listeners()`
off the **global** `g_playerEvents` arena hooks (they persist across battles):
`onAvatarReady` opens the window + arms the efficiency listener, `onAvatarBecomeNonPlayer`
destroys it. `battle_view.open_window()`/`close_window()` keep a `_active` singleton; the view's
`_onLoading` calls `battle_bridge.refresh()` for an immediate first paint.

- **Settings-gated.** Overlay presence is gated by `mod_settings.battle_enabled()` /
  `battle_alt_key_enabled()` (`battle_bridge.battle_bar_visible`); see `moe-settings`.
- **Alt-key peek.** `adapter/battle_input.py` shows the overlay only while Alt is held
  (`battle_widget_alt_key`). Mutually exclusive with always-on — soft-gated, so it's ignored while
  `battle_enabled()` is ON.

## Data flow

- **Read** — `adapter/battle_adapter.py::build_battle_snapshot()` from
  `IBattleSessionProvider.personalEfficiencyCtrl.getTotalEfficiency(PERSONAL_EFFICIENCY_TYPE
  .DAMAGE=1 / .ASSIST_DAMAGE=2 / .STUN=32)` (+ `onTotalEfficiencyUpdated`); intCD via
  `getControllingVehicleID()` → `arena.vehicles[vid]['vehicleType'].type.compactDescr`; gated on
  `ARENA_PERIOD.BATTLE` (3); spectate detected via `getPlayerVehicleID() != getControllingVehicleID()`
  (not `isObserver()`); `read_damage_log_summary_flags()` for the raised anchor.
- **Baseline** — the dossier is unreadable in battle, so the career baseline comes from
  `domain/baseline_cache.py` (snapshotted in the garage, keyed by intCD; garage intCD == battle intCD).
- **Math** — see the section below.
- **Push** — `bridge/battle_bridge.py` → `BattleMoEVM`.

## Math (`domain/battle_builder.py`)

- **Combined damage** — `C = max(0, damage + max(track, spot, stun) − team_damage)`
  (**MAX not sum**, per WG support #15060). `counted_assistance()` also returns which stream won
  (row-3 icon), with the pre-split merged assist as an early-battle fallback.
- **Projection** — `ewma_project`: `proj = round_half_away(pre_avg + EWMA_K·(C − pre_avg))`,
  `EWMA_K = 2/(N+1) = 2/101` (`constants.py`; community-derived, not WG-confirmed). A 0-damage
  battle IS folded, so the overlay opens slightly below career standing.
- **damage → percent: piecewise-LINEAR over WG's anchors plus a `(0, 0)` origin.** This is not an
  approximation of WG's `damageRating` — it **is** `damageRating`, reproduced to max **0.24 pp**
  over 118 real logged battles (`tools/dev/analyze_battle_samples.py --backtest`). Nothing is
  solved: no z-space, no probit, no normal CDF.
  - **`thresholds` is keyed by PERCENTILE** (`20, 40, 55, 65, 75, 85, 95, 100` — the 8 anchors WG
    actually stores; `adapter/moe_wgapi._PCTS`), *not* by mark count. `65/85/95/100` are the
    required legacy four (a WG row is dropped unless all four parse); `20/40/55/75` are optional
    enrichment that only adds resolution low on the axis.
  - `_fit_from_thresholds(thresholds)` → `[(0.0, 0.0), (damage, percentile), …]` ascending — the
    origin stop first, then the surviving anchors. **The fit IS the anchor list.** An anchor whose
    damage is not strictly greater than the last kept one is dropped individually (WG can return
    missing / zero / equal / non-monotone anchors), which guarantees `d_hi > d_lo` on every segment
    so the interpolation never divides by zero. Returns `None` only when **no real anchor
    survived** (falsy / unparseable table, or every anchor `<= 0`) → `has_data=False` → the overlay
    hides the percent (`cur_percent`/`pct_delta` = 0). One surviving anchor is enough.
  - `_smooth_percent(damage, fit)` — plain linear interpolation over `fit`: `0` at no damage (the
    origin stop) and **FLAT** at the top anchor's percentile above it (WG's table ends at the 100th
    percentile; there is nothing to extrapolate into). `_clamp` not `float()` on the input, so a
    NaN maps to the low bound instead of reporting the top percentile.
  - **The origin stop is load-bearing.** The superseded piecewise-normal fit was exact at its four
    stops but had nothing anchoring it *below* `D65`, and read mean **+6.71 pp** high wherever
    `pre_avg < 0.3·D65` (max error 11.9 pp) — nearly all its error, band-localised. Never drop it.
  - Independently corroborated by `tv.lebwa.gunmarks` (`linierInterpretator` over the same 8
    stops), which we already matched on `EWMA_K` and on the combined-damage formula.
- **The readout is ANCHORED on `pre_percentile` (2026-08-15, reversing a 2026-08-13
  un-anchoring — see `TASKS/shipped/` history if it's there, and
  `[[in-battle-percent-anchored-both-terms-same-curve]]`):**
  `move = f(proj_raw) − f(pre_avg_damage)` — **both terms evaluated on the SAME fitted curve
  `f`**, never mixing `f` with WG's stamped `pre_percentile`. Then
  `cur_percent = clamp(pre_percentile + move, 0, 100)` and `pct_delta = move`. `proj_raw` stays
  the unrounded `ewma_project_raw(pre_avg, cd)` (see the Projection bullet above — never the
  rounded `proj_avg_damage`). **Invariant:** `cur_percent − pct_delta == pre_percentile` always.
  The brief 2026-08-13 un-anchored form (`pct_delta = f(proj_raw) − pre_percentile`) mixed our
  curve with WG's stamp: the reconstruction gap `f(pre_avg) − pre_percentile` (mean ~0.05pp, max
  ~0.24pp) leaked straight into the delta, and at low per-battle damage that fixed gap could
  outweigh the real move and flip `pct_delta`'s sign opposite the damage delta. Anchoring both
  terms on one curve cancels that gap and guarantees the percent delta agrees in sign with the
  damage delta — the trade is giving up exact lebwa delta-parity by up to ~0.24pp.
- **Deleted with the old model:** the per-segment `(mu, sigma)` solve, `moe_estimate.norm_cdf`, and
  before it a global OLS fit over the 4 stops. `moe_estimate.inv_norm_cdf` and `fit_mu_sigma` (with
  their `MIN_Z_SPREAD` / `Sxx<=0` guards) **are still live**, but ONLY for
  `thresholds_from_samples` — the WG-API-error fallback (`engine_adapter._estimate_thresholds`,
  which `battle_adapter` now also takes) that derives a whole threshold table from the player's
  single dossier point. `GOALPOST_PERCENTILE` belongs to that estimator alone; the battle mapping
  does not use any of it.
- The `~`/`approx` plumbing was fully removed per user.

## VM slots (`bridge/view_models.py::BattleMoEVM`)

`properties=` is the `BattleMoEVM.__init__` default (10 at the time of writing; read it), indices 0–9: 0 `visible`, 1 `combinedDamage`, 2 `projAvgDamage`,
**3 `curPercent` (Real)**, **4 `pctDelta` (Real)**, 5 `hasData`, **6 `hasBaseline`** (career
baseline present; false on the replay/relogin BUG-B path → JS dashes proj/%/delta),
**7 `countedAssist`** (Number, = `max(track, spot, stun)`), **8 `assistKind`** (String:
`track|spot|stun|assist`, selects the row-3 icon), **9 `assistVisible`** (Bool: the "Enable
Counted Assistance" setting; JS also hides the row while `countedAssist == 0`).
`curPercent`/`pctDelta` must be Real — see the Wulf-decimals rule in `wotmod:architecture`.
The next free index is 10 — any new flag (single/double-row mode, RTL) must bump `properties`
and append; the backlog notes' "spare slot 7/8/9" assumption is obsolete.

## Front-end (`MoEBattle.js` / `.css` / `.html`)

- `MoEBattleView.html` is an empty body loading `MoEBattle.css` + `MoEBattle.js`. The JS uses
  **`ModelObserver()` with NO feature name** — the observed root model **IS** `BattleMoEVM`;
  fields are read directly (`model.combinedDamage`, …), no nested submodel, no unwrap for scalars.
- `#moe-battle-root` = two base `.mb-row`s: row 1 `[dmg icon] <combinedDamage> / <projAvgDamage>`,
  row 2 `[mark icon] <curPercent%> (<signed pctDelta>)`. Icons
  `icon_battle_condition_barrel_mark.png` (row 1) / `icon_battle_condition_improve.png` (row 2),
  from `…/personal_missions_30/quest_type/128x128/`.
- **Row 3 — Counted Assistance (opt-in):** a third `.mb-row`, gated by `assistVisible` **and**
  `countedAssist > 0`. Icon chosen from `assistKind` (`track`|`spot`|`stun`); value =
  `max(track, spot, stun)` — the assist MoE credits (MAX not sum, per WG; see
  `domain/battle_builder.py`). Enabled by the `counted_assistance_enabled` setting (default OFF);
  see `moe-settings`.
- **Render branch:** hidden unless `visible` **and `hasData`** (truthy guard, not `=== false` —
  a VM whose flags are still undefined before the first push must hide, not paint a `0/0` stub).
  When shown but **`hasBaseline` is false** (replay / relogin — no career baseline; BUG B), the
  projected avg, percent and delta are **dashed to `-`**, keeping only the live combined damage
  (a plain hyphen, NOT an em-dash — see Font). `signedPct`/`pctText` truncate via a `trunc2`
  helper so a sub-precision value reads `0`/`0%` in white, never a coloured `+0.00%`.
- **Colour by sign (`colourBySign`)** — sign carried by a **coloured text-shadow glow, not a fill**
  (numerals stay white): `.mb-up` green, `.mb-down` red, neutral = white + dark drop only. Row 1
  live damage vs projected avg; row 2 delta vs pre-battle standing. Only the delta **number**
  (`.mb-delta-num`) is coloured — the parens stay white.
- **Colours (live `MoEBattle.css`, canonical):** green **`#7BEC37`** `rgba(123,236,55,.9)`, red
  **`#D3443F`** `rgba(211,68,63,.9)`, gold bloom `#FFCD5A`, white `#ffffff`. (A stale note says
  `#61bf22`/`#c81400` — ignore it; the CSS above is what ships.)
- **Font:** `@font-face "MoEBattle"` weight 600 from **bare-sibling `url(MoEBattle.ttf)`**
  (+ a `coui://` absolute fallback). A `fonts/…` subdir path silently falls back to Arial Narrow.
  The family is renamed to avoid colliding with the engine's Flash-registered `MoEBattle`.
  **`MoEBattle.ttf` is a 19-glyph SUBSET** — `0-9 % ( ) + - , . /` + space, NO em-dash/letters;
  an unsupported char renders blank in Gameface (this is why the no-baseline placeholder is `-`,
  not `—`). A new overlay glyph needs a wider re-extract via `tools/dev/swf_font_to_ttf.py` (it
  pulls whatever the SWF `DefineFont3` embeds); check coverage with `fontTools …getBestCmap()`.
- **Backdrop (two layers):** `.mb-row::before` tiles `checker.png` (WG halftone dither, 4px tile /
  2px cells, `background-size:auto`, `image-rendering:pixelated`, `opacity:0.2`, radial **`mask`**
  — unprefixed); `.mb-row::after` = dark radial gradient + left-clip `mask:linear-gradient(...)`.
- Fixed box `340rem × 130rem`, `pointer-events:none`; `.mb-ico` uses `background-size:260%` +
  `brightness(3) drop-shadow(...)` (the glyph fills ~¼ its PNG). Numbers use layered `text-shadow`, no stroke.

## Ctrl+drag reposition (the two centre-screen bars, Python-owned end to end)

Holding **Ctrl + left mouse button** over a bar drags it; releasing persists the position. There
is **no JS drag code and no wire protocol** for this — Python samples the gesture and moves the
window directly:

- `adapter/battle_input.py` samples Ctrl/left-button state off `AvatarInputHandler.handleKeyEvent`
  / `handleMouseEvent` (wrapped, observe-only) **plus** a `gui.g_mouseEventHandlers` set member
  (added via `set.add`, no monkey-patch) — three vantage points because the raised-cursor Gameface
  input can swallow either dispatcher alone. Reports `on_drag(phase, cursor)` — `"start"`/`"move"`/
  `"end"` — through the **same single callback slot** the Alt-peek listener uses
  (`install_alt_key_listener(on_change, on_drag)`); a second `install_alt_key_listener` call would
  silently replace it.
- `bridge/bar_window.BarHost.drag()` maps the live cursor into the window's own logical GUI space
  (`domain/positioning.cursor_logical` / `cursor_top_left`) and moves the window there, offset by
  the grab point recorded at gesture start — an **absolute placement every event**, never a delta.
  `mod_settings.set_bar_position(x, y, persist=False)` updates the in-memory value on every move;
  `persist=True` on `"end"` writes it through MSA (see `moe-settings`).
- Both bar VMs are `commands=0` — there is no `setPosition` command anymore. `ctrlHeld` is still
  pushed to JS (`ProgressVM`/`EfficiencyVM`) so `MoEBarTransient` holds the bar visible while
  dragging, but JS does not move anything.
- Superseded design (do not resurrect): a JS `installDrag`-style delta protocol reporting mouse
  deltas for Python to add. It failed structurally — see the memory
  `[[absolute-cursor-placement-replaces-js-delta-drag-protocol]]` for why a delta can't work when
  the dragged thing is the surface the cursor is measured against.

## Placement (`bridge/battle_view.py` + `domain/positioning.py`)

- Anchor constants (`domain/constants.py`, fixed **logical-GUI-space px**, scale-invariant):
  default `BATTLE_ANCHOR_X=264` (from left), `BATTLE_ANCHOR_Y=0` (bottom-flush); RAISED
  `X_RAISED=215` / `Y_RAISED=33` used when **all four** DAMAGE_LOG summary flags are unticked (WG
  collapses the summary block → events shift up). `damage_log_summary_hidden()` decides; a failed read defaults to the un-raised anchor.
- The surface is a fixed **~256×256** (windowSize is read-only). Wulf's BOTTOM `PositionAnchor`
  clamps to TOP for a tall surface, so `_place()` always moves with a **TOP-LEFT anchor** and an
  absolute y (self-calibrated by clamping to `_FAR` to read the movable extent).
- **Move the WINDOW from Python (`window.move`), never the DOM.** `apply_position()` re-places on interface-scale change.
- No hot-reload for this window — every JS/CSS tweak needs a full client relaunch (see `moe-build-release`).
