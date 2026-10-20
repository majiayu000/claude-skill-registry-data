---
name: moe-garage
description: Use when editing the 14th_ua MoE Calculator's HANGAR percentile-bar widget — its garage mount/hook, the MoEVM/MarkTickVM data channel, the engine read, or the MoECalculator.js/.css DOM, render branches, bar axis, carousel positioning, assets, or the hover tooltip. For the in-battle overlay see moe-battle.
---

# MoE Calculator — garage widget (feature)

The hangar percentile bar. Reusable patterns are in `wotmod:gameface-widget` (front-end)
and `wotmod:architecture` (Python layering + `references/game-api.md`); this skill is the
concrete wiring. All paths under `src/res/`.

## Data flow (game → widget)

1. **Mount** — `gui/mods/mod_moe_calculator.py::_install()` patches
   `HangarVehicleParamsPresenter._onLoading` (a hangar sub-view). Every mount it re-arms
   listeners then `bridge.attach()` + `bridge.push()` — re-arming is required because the
   post-battle hangar teardown drops our `onChanged` delegate. Idempotent (`_moe_calculator_patched`).
2. **Inject** — `bridge/gameface_bridge.py::attach()` calls `openwg_gameface.gf_mod_inject`
   with `WIDGET_NAME="MoECalculator"`, styles `MoECalculator.css`, module `MoECalculator.js`,
   and adds the `DATA_PROP="moeData"` property. Five re-armed listeners: vehicle, loadout,
   lobby-state, stats, settings.
3. **Read** — `adapter/engine_adapter.py::build_snapshot()` reads `g_currentVehicle` +
   dossier `MARK_ON_GUN_RECORD` (`.getValue()`=marks 0–3, `.getDamageRating()`=percentile
   float, nation) and `movingAvgDamage`; caches the career baseline into `baseline_cache`.
4. **Build** — `domain/builder.py::build_model()` — three ticks at `MARK_PERCENTS=(65,85,95)`,
   fill = clamped percentile, `end_damage_required` from threshold key `100`. `bar_visible()` gates.
   Widget presence is also gated by `mod_settings.garage_enabled()` (default ON); see `moe-settings`.
5. **Push** — `bridge/view_models.py::MoEVM` (see slots below).

**Lifecycle guard:** `attach()` caches `_active=(host_vm, rvm)` and nothing clears it (no
view-destroy hook is wired). Session-persistent listeners — the `moe_wgapi` ready hook and
`IItemsCache.onSyncCompleted` — can fire AFTER battle entry tears the hangar down, so `refresh()`
early-returns via `_host_alive()` (lobby state machine present) instead of pushing into the dead
VM. `_arm` uses `getattr(holder, attr, None)` so a renamed WG event degrades quietly. A full
`_active` teardown + the re-injection observer-stacking question stay open (`TASKS/garage-bridge-lifecycle.md`).

## VM slots (`bridge/view_models.py`) — HAND-NUMBERED, JS reads by name

- **`MoEVM`** — read `properties=`/`commands=` off its `__init__` in `view_models.py` (the 12 read
  slots below are only the v1 set; later slots are APPENDED after `labels` — the drag/position
  channel, the `rev` push counter, the `trend` JSON — plus a `setPosition` command). Indices: 0 `visible`, 1 `nation`, 2 `marks`,
  **3 `curPercent` (Real)**, 4 `curAvgDamage`, **5 `fill` (Real)**, 6 `hasData`,
  7 `carouselRows`, 8 `carouselSmall`, 9 `ticks` (Array of `MarkTickVM`),
  **10 `endDamageRequired`**, 11 `labels` (JSON string for the tooltip).
- **`MarkTickVM`** — `properties=4`: 0 `percent`, 1 `markCount`, 2 `damageRequired`, 3 `reached`. (No `icon` slot — the widget draws a flat glyph; the old nation-art URL was removed.)
- `curPercent`/`fill` must be Real — see the Wulf-decimals rule in `wotmod:architecture`.

## Front-end (`MoECalculator.js` / `.css`)

- `ModelObserver("MoECalculator")` reads `model.moeData`. `#moe-root` built once by `ensureRoot()`:
  `.moe-head>.moe-cur(.moe-cur-dmg + .moe-cur-icon)` and `.moe-body>.moe-track` holding
  `.moe-fill .moe-split .moe-split-label(50%) .moe-end .moe-end-label .moe-cur-marker .moe-cur-pct .moe-ticks`.
- **Bar axis** (`barX`): piecewise `PCT_STOPS=[0,65,85,95,100]` → `BAR_STOPS=[0,25,50,75,100]`
  (equal quarters — same convention as the Damage Efficiency bar's `EFFICIENCY_BAR_STOPS`, see
  `moe-progress`). The tooltip's weekly-MoE trend chart's Y axis reuses `barX` directly (the old
  `axisPos` was collapsed into it in v5.1.0) — there is no separate copy of the constants to keep in lockstep.
- **Render branches (`render`):** no `moeData` → hidden; `visible===false` → hidden;
  otherwise shown. **New tank genuinely reads `0` / `0%`** (synchronous dossier read, not the
  async table) — explicit zeros, not a "—" placeholder. Percent via `pctText` is **floored to
  2 decimals** (never rounds up past a threshold). Carousel classes `moe-rows2` / `moe-small`
  toggled from `data.carouselRows`/`carouselSmall`.
- **Ticks** use the flat glyph `img://…/library/marksOnGun/mark_%d.png` (ignores `tk.icon` — nation decals mush at tick size); damage requirement printed below each (blank when unknown).
- **Localization:** `labels` arrives as a JSON bundle; `L(key)` is missing-key-safe; JS hardcodes no English (mirrored contract with `adapter/i18n.py`).
- **`applyWidgetScale()`** (on `whenReady` + `resize`) sets `#moe-root`'s `transform: scale(k)` so the widget height matches WG's viewport-driven bottom-bar slot boxes; `k = 1 + GROWTH·(vp/scale − SIZE_REF)/SIZE_REF` (`SIZE_REF=1080`, `GROWTH=0.625`). See the CSS-notes anchor/height bullets for the full rem-vs-vh reasoning.
- **`posW`/`posH` are NOT the widget's width/height** — they are the *viewport* size (`window.innerWidth`/`innerHeight`) captured at pin time, stored only to rescale the widget's *position* proportionally when the resolution/UI-scale changes. They are internal (written only via `setPosition`), never user-facing controls — the v1.4.0 drag-to-reposition feature moves the widget only (Ctrl+drag + X/Y position steppers), it does NOT resize it.

## CSS notes (`MoECalculator.css`)

- No `var(--color-*)` (Gameface drops the whole declaration on an unresolved var); most sizing in **`rem`** (1rem == interfaceScale px); font `PFDINMax`; white fill `#ede6d9` (band/zone colours were removed — plain white bar).
- **Anchor (bottom-right).** X pure rem (`right:46rem`); width `315rem`. **Y is a `calc(B rem + V vh)` BLEND** (`V=18.33vh`; B per carousel state — `.moe-rows2`=104, single-row=77.5, `.moe-small`=61rem), NOT pure rem and NOT a fixed-px term. Why: WG's Auto interfaceScale is **power-of-two gated** (x2 only when width≥2560 AND height≥1536; `gui/shared/utils/graphics.py`), so 1080p & 1440p are both x1 while 4K is x2 — and 4K is exactly 2× 1080p, making those two points **degenerate** (pure rem, pure vh, and every blend agree there). The carousel top the bar clears is neither pure-scale nor pure-viewport: pure rem sits too LOW at 1440p, pure vh too HIGH. The blend reproduces 1080p/4K exactly and was pinned live at 1440p (the only non-degenerate point) on the 2-row carousel (302/368/604px). **Do NOT collapse Y to a single unit or re-add a fixed `+140px` term** — that `+140px` hybrid was the resolution-scaling bug. Retune: change V, re-solve `B = px_1080 − V·10.8`.
- **Widget height** tracks WG's bottom-bar slot boxes (crew/equip/directive/ammo/consumables — **Flash**, viewport-driven, so the rem widget is too short at non-4K). Fixed in **`MoECalculator.js`** via `transform: scale(k)` on `#moe-root`, origin bottom-right (preserves the anchor): `k = 1 + GROWTH·(vp/scale − SIZE_REF)/SIZE_REF` with `SIZE_REF=1080`, `GROWTH=0.625` → 1.0× at 1080p/4K, ~1.208× at 1440p; recomputed from live `innerHeight` + root font-size on `resize`.
- **Calibration tooling:** `tools/dev/probe_resolutions.py` (video-mode + `interfaceScale.getScaleOptions()` table) and a **temporary on-screen JS diagnostic div** (logs `computed bottom` + rendered rect + `1rem`px). **GOTCHA:** a 2-row carousel makes `#moe-root.moe-rows2` win, so base-`#moe-root` `bottom` probes are silently OVERRIDDEN — always confirm which carousel-state rule is live before probing.
- Track uses WG `img://` progressbar textures; **`card_border.png` is a `border-image`** and MUST be a bare-sibling `url(card_border.png)` (`img://`/`data:` silently fail for `border-image`).

## Hover tooltip — SHIPPED (native award-tooltip clone)

`TOOLTIP_ENABLED = true`. On hover (400ms intent delay) a body-level `position:fixed`
`#moe-tooltip` reproduces the client's **Marks-of-Excellence award tooltip** (Vehicle stats →
Awards), keyed by mark count 0..3: nation mark art (marksOnGun 180×180) top-right + title +
current-ratio line (percentile in white) + description + divider + 5-bullet condition. Text is
the client's own strings via the `labels` bundle (`adapter/i18n.py`).

Built in the **shared `.wg-tooltip` / `.wg-tip-*` vocabulary** — the SAME classes as the sibling
`wgmod-research-progress` tooltip (both render identically), but a STANDALONE copy scoped to
`#moe-tooltip` (no shared file). Recipe: the `wotmod:gameface-widget` skill's "Native tooltip
recipe". MoE-local classes: `.wg-tip-icon-mark`/`.wg-tip-main-mark`, `.wg-tip-icon-unearned`,
`.moe-tip-ratio`/`.moe-tip-descr`, `.moe-tip-hi`, `.moe-tip-empty`.

Engine gotchas baked into the CSS/JS (see the file comments):
- **No inline formatting** in this Gameface build (any element child drops to its own line,
  `display` has no effect) → the white-% ratio line is a `flex-wrap` row of one span PER WORD
  (`ratioHtml`), the `%` word = `.moe-tip-hi`; word spacing via `margin-right`, not `gap`.
- **Mark icon** box uses the glyph's real aspect (64×46, `background-size:100% auto` + center)
  to crop the 180×180 source's ~25/27px transparent bands, so it aligns with the title.
- **Description** is a full-width paragraph OUTSIDE `.wg-tip-main` (the icon's reserved column
  would otherwise narrow it).
- **Frame** = 9-slice via `border-image-source: url('img://…background_with_border.png')` — the
  LONGHAND resolves `img://` where the `border-image` shorthand fails; `tooltip_bg.png` bundled
  as fallback.

## Assets (bare siblings of the JS/CSS)

`card_border.png` (border-image), `tooltip_bg.png` / `tooltip_divider.png` (tooltip skin). Fonts for this feature: engine `PFDINMax` (no bundled TTF; the bundled `MoEBattle.ttf` is the battle overlay's).
