---
name: moe-build-release
description: Use when packaging, deploying, testing, hot-reloading, versioning, or releasing the 14th_ua MoE Calculator — which files carry the version, what each build/ script and installer file does, the garage-vs-battle hot-reload split, the debug REPL wiring, and the dev-tools inventory. For feature internals see moe-garage / moe-battle.
---

# MoE Calculator — build, deploy, version & dev loop

Reusable mechanics live in `wotmod:build-deploy`, `wotmod:release`, and `wotmod:debug-repl`;
this skill is the concrete file list and command set. **Two Pythons:** package with
`C:\Python27\python.exe` (bytecode is version-locked), test/dev-tool with Python 3.13.

## Version files (bump together; `src/meta.xml` is canonical)

`build/check_version.py` enforces consistency (`<py> build/check_version.py`, exit 1 on drift):

| File | Reference |
|---|---|
| `src/meta.xml` | `<version>X.Y.Z</version>` — **source of truth** |
| `src/res/scripts/client/gui/mods/mod_moe_calculator.py` | `MOD_VERSION = "X.Y.Z"` |
| `installer/moe_calculator-setup.iss` | `#define ModVersion "X.Y.Z"` + `#define ModWotmod "…_X.Y.Z.wotmod"` |
| `installer/build_installer.ps1` | `$ModWotmod = …com.14th_ua.moe_calculator_X.Y.Z.wotmod` |
| `INSTALL.md` | `MoECalculator-Setup-X.Y.Z.exe`, `…_X.Y.Z.wotmod` |
| `dist/INSTALL.txt` | prose `version X.Y.Z` (gitignored build output; checked when present) |

_`X.Y.Z` is illustrative — the live canonical value is in `src/meta.xml` (currently 8.0.0,
client target EU 2.4.1.0)._

- `README.md` uses `<version>` placeholders (no hard-coded number). `adapter/moe_wgapi.py`'s
  `_AGENT` string carries the project URL (no version number — nothing cosmetic to bump there).
- The 4-part **client** version is deliberately excluded from the check (a `(?!\.\d)` lookahead skips the 4-part client version).

## Release must stay silent (no unconditional logging)

A shipped build must write **nothing** to WoT's `python.log` in normal operation — those logs
are world-readable on every player's machine. Never call `debug_utils.LOG_NOTE` (or `LOG_NOTE`
re-exported from `_compat`) directly for informational output. Route every chatty/internal note
(lifecycle, placement, data payloads, fetch lists) through **`_compat.LOG_DEBUG`**, which is
gated on **`_compat.DEBUG`** (ships **`False`**; flip `True` only for local dev, never commit it
`True`). Genuine failures go through the always-on, path-safe `LOG_CURRENT_EXCEPTION`.

`tests/test_logging_gate.py` enforces this: it fails the build if `DEBUG` is committed `True` or
if any module outside `_compat.py` grows a raw `LOG_NOTE(` call site. **Run the full pytest suite
before every release** (it is part of the gate, alongside `check_version.py`), and eyeball
`python.log` after an in-game smoke test — it should stay clean.

## build/ scripts

- **`build_wotmod.py`** — **Python 2.7 only** (asserts). Reads `meta.xml`, compiles `.py`→`.pyc`
  (drops `.py`, skips `__pycache__`), zips `meta.xml` + `res/` as **`ZIP_STORED`** →
  `dist/com.14th_ua.moe_calculator_<version>.wotmod`. Non-`.py` files (fonts/PNG/JSON) are copied verbatim.
  **Self-enforces `-OO`** (`_ensure_optimized`, since 1cd8c27): if `sys.flags.optimize < 2` it
  re-execs *this script* (not `sys.argv`, so `deploy_wotmod.py`'s in-process `main()` isn't
  restarted) in an `-OO` subprocess, so a plain `python build/build_wotmod.py` ships
  docstring-stripped `.pyc` **by default** — the harness "Ship docstring-stripped bytecode"
  standard. (`-OO` also drops `assert`, so keep asserts to tests/dev tools, never load-bearing
  in shipped src.)
  **Single build, no arguments** — MoE thresholds come from the official WG API at runtime
  (`adapter/moe_wgapi.py`), so GitHub and WGMods ship the identical `.wotmod`.
- **`deploy_wotmod.py`** — Python 2.7. Cleans old `…_[0-9]*.wotmod` from `mods/<ver>/` + loose
  `res_mods` leftovers, calls `build_wotmod.main()`, copies in. Reads `deploy.local.json` if no args.
  `--clean-overlay` removes the hot-reload overlay. **Needs `WorldOfTanks.exe` closed** (`wgc` ok).
- **`build_moe_zip.py`** — any Python. Builds `dist/MoECalculator_<version>.zip` = bilingual
  `readme.txt` (from `installer/readme.moe.txt`, `{VERSION}` substituted, CRLF) + the mod `.wotmod`
  + all `installer/vendor/*.wotmod` under `mods/<CLIENT_VERSION>/`. Manual upload to wgmods.net. Holds `CLIENT_VERSION` (bump it each client upgrade).
  Packages whatever `.wotmod` is in `dist/` — the same single build the GitHub installer uses.
- **`check_version.py`** — the version gate above. **`clean_dist.py`** — prunes non-current release artifacts from `dist/` (`--dry-run`).

## installer/

- **`moe_calculator-setup.iss`** — Inno Setup 6. Detects WoT root, resolves client version, installs
  to `mods\<version>\`, bundles the vendor deps from `installer/vendor/` **unless a same-or-newer
  copy is present** (`NeedVendor` Check + `PurgeOlderVendor` AfterInstall deletes older copies of
  that id; `uninsneveruninstall`), cleans old builds, WoT-running guard, GitHub
  Atom-feed self-update. Repo `drizzer14/moe-calculator`, base name `MoECalculator-Setup`.
- **`build_installer.ps1`** — preflights the built `.wotmod` + vendor dep, finds `ISCC.exe`, compiles → `dist/MoECalculator-Setup-<version>.exe`, writes the `<exe>.sha256` sidecar (.NET hash; a missing sidecar fails the build).
- **`readme.moe.txt`** — bilingual EN/UA readme for the wgmods zip (the only readme template; the old `readme.wgmods.txt` stub was deleted). **`installer/vendor/`** — `net.openwg.gameface_1.2.2.wotmod` + `aslain.modmenu_2.1.04.wotmod` + `me.poliroid.modslistapi_1.8.0.wotmod` (sha256-pinned in `MANIFEST.json`, guarded by `tests/test_vendor_manifest.py`). Client 2.4.1 needs these builds — the older gameface 1.1.6 / modmenu 2.0.16 / modslist 1.7.9 are dead there.

## Hot-reload (the split that bites)

- **Garage widget hot-reloads:** `<py3> tools\dev\sync_gameface.py "D:/Games/World_of_Tanks_EU" <client ver>`
  copies only the Gameface JS/CSS/assets into `res_mods`, then toggle Tech-Tree↔Garage to re-inject. No relaunch.
- **The in-battle registered WINDOW does NOT hot-reload** — its resources pin at client launch;
  reopen and `Window.reload()` both serve the launch-time cached document. **Every CSS/JS tweak to
  `MoEBattle.*` needs a full client relaunch.** Gate the commit on the in-game sign-off (deploy → verify live → commit).
- Clean the `res_mods` overlay before any ship-verification — a stale overlay shadows a fresh packaged build.

## Dev loop / REPL

- Live introspection: the per-mod debug REPL package has been retired in favour of the
  harness-owned debug REPL — `wotmod-harness/plugins/wotmod/tools/debug-repl/`
  (package `com.wotmod_harness.debug_repl`, TCP **:2223**, client `repl_client.py` there).
  See `wotmod:debug-repl`.
- Decompiled client source for symbol hunting:
  `C:\Users\Dmytro Vasylkivskyi\wot-src-eu\sources\res\scripts\client\`.
- **`tools/dev/` inventory:** `sync_gameface.py` (hot-reload), `gen_checker.py` (battle dither PNG),
  `swf_font_to_ttf.py` / `swf_probe.py` (extract `MoEBattle.ttf` from `fontlib.swf`),
  `gen_overlay_tuner.ps1` / `gen_icon_picker.ps1` (browser calibration artifacts → `TASKS/refs/`),
  and the `probe_*` live-discovery scripts.

## Release state

**v8.0.0 is STAGED, not published** (`src/meta.xml` is 8.0.0, committed on `main`, artifacts in
`dist/`). It retargets the mod to WoT client **EU 2.4.1.0** (up from 2.4.0.2; major bump per
convention). WG 2.4.1 dropped `gen_utils`/`DynAccessor` and stopped processing
`mods/configs/res_map`, so the three battle windows moved to WG-native resources:
`src/res/gui/gen_resources/com.14th_ua.moe_calculator.json` declares
`R.mods.com_14th_ua_moe_calculator.views.{MoEBattleView,MoEProgressView,MoEEfficiencyView}`, resolved by
`bridge/bar_window.layout_id()` (fail-soft `-1`, logged once). The res_map JSONs are deleted and
the "one-time client restart" no longer exists. Vendor builds bumped to gameface 1.2.2 / modmenu
2.1.04 / modslist 1.8.0. `SETTINGS_VERSION` unchanged at **31**. Live in-battle confirm owed.
When it is published, promote it to "current Latest" below and fold v7.0.0 into history.

**v0.1.0 through v7.0.0 are published** on `github.com/drizzer14/moe-calculator` (`origin/main`);
**v7.0.0 (2026-10-07) is the current Latest**. It retargets the mod to
WoT client **EU 2.4.0.2** (up from 2.4.0.1; major bump per convention) and ships the MoE `%`
caption work: a parenthesised MoE % beside both centre bars' current-damage numeral (new
`ProgressVM.curPercent` / `EfficiencyVM.damagePercent` slots), **four per-bar MSA checkboxes**
(Moving Average / Damage Efficiency × show % / show change; keys in `mod_settings.py`), the
%-caption font matched to the damage numeral, grown bar surfaces with re-derived
`*_MM_TRACK_X(_LARGE)`, and a fix for the pre-v23 alignment migration that re-ran on every
version bump (Free alignment is no longer collapsed to Fixed; now gated on `pre_v23`).
`SETTINGS_VERSION` went **29 → 31** (structural forward bumps, no `_migrate_pre_v30_*` /
`_migrate_pre_v31_*`; every saved value is kept, pinned by a v30→v31 test). The maintainer
live-tested the build on 2.4.0.2 on 2026-10-07.

**v6.0.1 (2026-09-20) was the prior Latest** — a patch release cut on top of v6.0.0. The garage
weekly MoE trend chart's 100% mark icon is now centered on its top gridline (it was clamped
~5.5rem too low) and two dead JS constants left over from that clamp were removed. The two
horizontal centre-screen transient bars (Progress Bar "Moving Average" variant and Damage
Efficiency) had their single whole-bar backdrop dither replaced with **per-caption** shadow
strips — each caption now gets its own dither+radial box, matching the vertical bars'
treatment — and the surface box was shrunk (a new `CLIP_B_REM` bottom trim was added) so both
bars can drag closer to the bottom screen edge; the current-damage caption's shadow was
re-sized/re-centered, and the now-dead `.mp-backdrop` DOM node was removed. Touched
`MoEProgress.js`/`.css`, `MoEEfficiency.js`/`.css`, the `tools/dev` CSS generators/checkers, and
`domain/constants.py`. `SETTINGS_VERSION` is unchanged at **29** (no MSA control changed);
client target **unchanged at EU 2.4.0.1**. The settings-panel widget preview PNGs were
regenerated for the two changed bars. No player-facing settings/controls were added; player
docs needed no change.

**v6.0.0 (2026-09-18) was the prior Latest** — a game-upgrade release retargeting the mod to
WoT client **EU 2.4.0.1** (up from 2.4.0.0), major bump per convention, cut on top of v5.1.0
(same pattern as v3.0.0/v4.0.0/v5.0.0). `SETTINGS_VERSION` unchanged at **29**.

**v5.1.0 (2026-09-16) was the Latest two releases before that** — a minor feature release cut on top of v5.0.0. It
adds a **garage weekly moving-average MoE trend chart** inside the MoE-award tooltip: per-battle
dots on a fixed percentile axis, horizontal mark lines at the 65/85/95/100 percentile thresholds
drawn from a tiled PNG, Y-axis mark icons in a right gutter including the `barrel_mark` 100%
glyph, and full-height day dividers with per-day end-of-day moving-average labels. Touched
`MoECalculator.js` + `.css`, plus new `domain/trend.py` and `adapter/trend_log.py` (with
`tests/test_trend.py` / `tests/test_trend_log.py`). A pre-build cleanup collapsed the chart's
duplicate `axisPos` helper into the existing `barX` (−16 lines), and a JS clamp fix stopped the
100% `barrel_mark` icon cropping at the top. It also fixed a `check_version.py` stale-doc-scan
false positive (the settingsVersion DOC regex now ignores historical arrow prose).
`SETTINGS_VERSION` is unchanged at **29** (no MSA settings control changed); client target
**unchanged at EU 2.4.0.0**. Player docs (`README.md`, `INSTALL.md`, `installer/readme.moe.txt`)
were reconciled for the new trend chart in both EN and UA halves.

**v5.0.0 (commit `600ae49`) was the Latest three releases before that** — a game-upgrade release
retargeting the mod to WoT client **EU 2.4.0.0** (up from 2.3.1.3), major bump per convention,
cut directly on top of v4.0.1 with **zero functional/code changes** (same pattern as
v3.0.0/v4.0.0). `SETTINGS_VERSION` unchanged at **29**; deploy target confirmed via
`deploy.local.json`.

**v4.0.1 (2026-08-27) was the Latest two releases before that** — a patch release carrying two bar-render
bugfix commits on top of v4.0.0: `0f79e28` opens the Moving Average bar fill at the axis
floor instead of the `pre_avg` stop; `24010ab` stops the vertical wide-glow backdrop
clipping on the left. Touched `MoEProgress.js`, `MoEProgressVertical.css`,
`MoEEfficiencyVertical.css`, plus `tools/dev/` tuner tooling. **No user-facing surface
change** (no new/renamed settings controls, no changed defaults, no new widgets); player
docs needed no reconciliation. `SETTINGS_VERSION` unchanged; client target **unchanged at
EU 2.3.1.3**.

**v4.0.0 (2026-08-12-era) was the Latest two releases before that** — a game-upgrade release retargeting the
mod to WoT client **EU 2.3.1.3** (up from 2.3.1.2), major bump per convention.

**v3.1.4 and v3.1.3 were patch bar-fix releases published between v3.1.2 and v4.0.0.**

**v3.1.2 (2026-08-17) was the Latest before that chain** — a patch release carrying three bugfix/tooling
commits: `904d49e` re-mounts a natively-destroyed `WindowFlags.TOOLTIP` bar window (`BarHost`'s
`_is_dead` detection + a per-tick re-drive of `open_window` in `battle_bridge`) and restores the
bar's **last-good placement** instead of stranding it at the `_FAR`/minimap corner on a failed
`_place()` (`has_placed()` now gates `visible`); `c17f339` gates the vertical Progress bar's
ETA-row backdrop strip (`.mpv-bd-1`/`showEta`, plus the missing `.mpv-bd.none` rule) so it no
longer renders when the ETA row is hidden, and corrects vertical caption/minimap-gap tuning
(widened mark-requirement/preAvg backdrop strips, fixed the Large-mode caption translateX
direction); `e5b5ffa` adds `tools/dev/watch_repl.py` and refreshes the vertical CSS
tuner/hand-edit-check tooling for the above. **No user-facing surface change** (no new/renamed
settings controls, no changed defaults, no new widgets); player docs needed no reconciliation
(`git log v3.1.1..HEAD` touched none of `README.md` / `INSTALL.md` / `installer/readme.moe.txt`).
`SETTINGS_VERSION` unchanged; client target **unchanged at EU 2.3.1.2**.

**v3.1.1 (2026-08-16) was the prior Latest** — a patch release carrying a single in-battle
MoE-projection accuracy fix (commit `20cc5a9`): `cur_percent`/`pct_delta` are now re-anchored on
ONE curve so the displayed percent agrees with the damage (previously mixing a curve value
against a server stamp let a fixed gap flip the delta's sign). **No user-facing surface change**
(no new/changed settings controls, defaults, or widgets); player docs needed no reconciliation.
`SETTINGS_VERSION` unchanged; client target **unchanged at EU 2.3.1.2**.

**v3.1.0 (2026-08-14) was the Latest two releases before that** — an ordinary feature/minor release cut on top of
v3.0.0 (merged the `v3.0.0` tag into `main` so it inherited the client-retarget pointers, then
bumped `3.0.0 → 3.1.0`; client target **unchanged at EU 2.3.1.2**). `SETTINGS_VERSION` went
**23 → 28** across the feature's five bumps (24 = the Progress-Bar-to-column-2 swap, 25 = two
live MSA panel widget-preview `Image` controls, 26 = the per-vehicle Mode-override `HotKey`
control (a new MSA `HotKey` component type, default **K**), 27 = moving the bar preview Image
next to the calculator preview in column 1, 28 = the "Automatic Mode Toggle" threshold `Slider`).
User-facing surface added since v3.0.0/v2.0.0: **vertical orientation** for both centre-screen
in-battle bars (Moving Average + Damage Efficiency), each with its own per-mark caption geometry,
per-number backdrop, and a closed-form minimap-facing edge; **Alignment collapsed to Fixed/Free**
(replacing the old three-way Damage-Log/Minimap/Free model), with Orientation/Alignment/Position
no longer mutually auto-set (all cross-derivation was deleted, not just inert); a **per-vehicle
Mode override HotKey** (default K) plus an **Automatic Mode Toggle** percentile threshold that
flips a vehicle's bar mode automatically; **in-panel widget previews** — the MSA panel now shows
live `Image` previews of both in-battle widgets, updating as driving settings change; the
**Progress Bar feature moved to settings column 2** (the v23→24 column swap, with column 1 now
holding Battle Calculator + every garage-related group); an **ETA-in-battles rework** on the
vertical bars with caption/backdrop geometry tuning; and a batch of in-battle MoE-projection
accuracy fixes (interpolating the raw projection for `cur_percent`, measuring the delta from WG's
stamped career percent, priming baseline/thresholds independently of the garage widget, serving a
stale threshold table during a refetch, and no longer seeding the baseline from a pre-sync garage
read).

**v3.0.0 (2026-08-12) was the Latest before that** — a game-upgrade release retargeting the mod to
WoT client **EU 2.3.1.2** (up from 2.3.1.1), major bump per convention, with **zero functional/code
changes**.

**v2.0.0 (2026-08-06) was the Latest two releases before that** — a game-upgrade release retargeting the mod to
WoT client **EU 2.3.1.1** (#910, up from 2.3.1.0 #903), major bump per convention, with **zero
divergences found and no functional/code changes**. The `upgrade-analyzer` pass resolved all
198 gathered seams (monkey-patch targets, subscribed Events, Wulf ViewModel API, `img://` art
paths) present and unchanged in the new client's packed `.pyc` — **this was a static resolve, not
a live one; no WoT client was launched during this upgrade.** Vendor deps (OpenWG GameFace 1.1.6,
Aslain ModsSettingsAPI 1.6.4, Mods List API 1.7.8) were kept unchanged but were **not** live-verified
on 2.3.1.1.

**v1.8.0 (2026-08-03) was the Latest before that** (v1.7.0 was the Latest before that, 2026-08-01),
carrying the in-battle progress bar's Ctrl+drag reposition + Bar Position X/Y fields, a
configurable Hold Duration, the Moving Average bar's ETA-in-battles readout, the relabelled
Transitions master, and the shrunk Large mode. The **1.0.0** release retargeted the mod to WoT
client **2.3.1.0** (major bump) and added the Alt-key peek mode + Counted Assistance row; **1.1.0**
is a patch-level polish of the in-battle overlay row/backdrop alignment (shipped as a minor bump by
choice); **1.2.0** is a minor bump carrying the in-battle MoE-projection accuracy work (smooth
probit curve + self-calibrating EWMA `k`) plus the R3 row-backdrop fix — all committed after the
v1.1.0 tag but unreleased until then; **1.3.0** is a minor bump carrying the settings-surface
overhaul — migrated to Aslain **ModsSettingsAPI** + bundled **Mods List API** (settings now surface
in WoT's in-game "Modification list" window), a redesigned **two-column MSA settings panel**, and
resolution-correct **high-DPI/4K garage widget** size + position (plus an enlarged MoE award tooltip);
**1.3.1 (2026-07-19)** is a patch; **1.4.0 (2026-07-20)** is a minor bump carrying **garage widget
drag-to-reposition** (Ctrl+drag + numeric X/Y position steppers + a "Follow Carousel" toggle + a
reset command — moves only, no resizing) and **MSA settings-value migration** so a `SETTINGS_VERSION` bump (now **v5**) no longer
wipes users' saved settings (migrates the persisted Aslain ModsSettingsAPI values across the bump,
fail-soft to a fresh install); **1.5.0 (2026-07-25)** is a minor bump carrying in-battle
MoE-projection accuracy work — the damage→percent mapping moved from a single global
least-squares normal `(mu, sigma)` over the four threshold stops to an **exact-at-stops piecewise**
normal fit. Least squares passed through *none* of the stops (live-EU residuals sign-identical on
every tank: D1 −3.1, D2 +1.6, D3 +0.9, D100 −0.25 percentile points), so the 1-mark stop read
~61.9% instead of 65% and the slope just above a mark ran ~50% too steep — a **slope** bias the
`pre_percentile` anchor cannot cancel (it cancels only a level bias), so the readout started right
and drifted as damage accrued. `_fit_from_thresholds` now returns the usable stops as ascending
`[(damage, z), …]` and `_smooth_percent` solves the bracketing segment's `(mu, sigma)` exactly
through both stops, so `f(D_i) == 100*p_i` at every stop while the curve still rides WG's normal
shape between them; the end segments extend for both tails (no truncation above D100). Unusable WG
stops are dropped **individually** (`d <= 0`, or `d <=` the last kept `d`), so a bad interior stop
costs resolution, not `has_data`; **1.6.0 (2026-07-29)** is a minor bump carrying **two new
mutually exclusive centre-screen in-battle progress bars**, both **off by default** behind a new
independent `progress_bar_enabled` MSA master ("Progress Bar", its own column-1 group, never a
child of the In-Battle Widget) with an int-valued `progress_bar_variant` RadioButtonGroup child
(`0 = Moving Average`, the default, so an existing user lands on the original bar; `1 = Damage
Efficiency`). **Moving Average** (`MoEProgress.js/.css` + `MoEProgressView.html`,
`bridge/progress_view.py`, `res_map/MoEProgressView.json`) plots the career projected average
between the held mark and the next mark's requirement, plus this battle's signed delta; it is gated
on `model.has_baseline`, so it stays hidden in replays and after a relogin until a Garage visit
populates the baseline. **Damage Efficiency** (`MoEEfficiency.js/.css` + `MoEEfficiencyView.html`,
`bridge/efficiency_view.py`, `res_map/MoEEfficiencyView.json`) plots this battle's damage against
all four mark requirements on four equal quarters (`EFFICIENCY_BAR_STOPS = (0, 25, 50, 75, 100)`)
and auto-shows only on a new high-water damage mark; it has **no** baseline gate, only `hasData`.
`battle_bridge._window_gates()` is the single place that decides who may be up and opens **at most
one** centre bar — the only reason both stylesheets can own `#moe-bar-root` / `.mp-*` without
colliding. Shared transient behaviour (the fade/hold/fade life cycle, `HOLD_MS = 5000`) lives in
`MoEBarTransient.js`, instantiated once per document; **Alt is an ADDITIVE show trigger** for both
bars and is deliberately NOT gated by the overlay's "Show on Alt Key", and the bars' centre-screen
position is fixed, not configurable. `SETTINGS_VERSION` went **5 → 10** across the feature's
iterations (6 = the checkbox, 7 = a column-3 relayout, 8 = its revert plus the "Next Mark Progress
Bar" label rename, 9 = the re-parent into its own group + the variant radio, 10 = dropping the
radio's own "Bar Type" label row) — 6–9 shipped to nobody but the maintainer's install. Saved
values migrate across every step and no `varName` was renamed. Cosmetics: the Damage Efficiency
delta renders **without parentheses** (Moving Average and the corner overlay keep theirs) and
caption centring was fixed to sit on the numeral, not the row. Player docs were **resynced** this
release (`README.md` / `INSTALL.md` / `installer/readme.moe.txt`, both language halves), and
`installer/readme.wgmods.txt` was **DELETED** as a superseded stub — `readme.moe.txt` is now the
single portal-readme template, and `build/build_moe_zip.py` was already its only consumer.
**1.7.0 (2026-08-01)** is a minor bump carrying in-battle MoE-projection accuracy work plus a
full MSA panel restructure. The damage→percent mapping moved **off** 1.5.0's exact-at-stops
piecewise normal fit onto **WG's own LINEAR interpolation over the 8 published anchors plus a
(0,0) origin** — no z-space, no probit; the old normal fit's 11.9pp error was localised below the
lowest stop. Both centre bars gained a **Large** size mode (the `progressSize` radio, labelled
"Scale", options Default/Large). The progress bar's enter/exit fade+slide can now be switched off
per trigger area (`progress_transitions_enabled`/`_events`/`_manual`). The interface-scale-1
caption-drift fix landed on the efficiency bar then was mirrored onto the moving-average bar. A
died/survived flag was added to the battle-sample log to split the credit shortfall
(dev/sample-corpus only, not user-facing). The MSA panel itself was restructured into three
column-1 categories (Battle Calculator / Battle Progress / Transitions) with bold `<b>` headers and
`Empty` spacers; column 2 split into Garage Widget + Layout; every master now reads "Enabled"; new
progress-visibility flags `progress_show_events` / `_alt_key` / `_always` were added, with "Always"
greying the other two via an MSA multi-condition AND gate; both radios went standalone and inline;
the Mode radio was reordered so Damage Efficiency is index 0 and the new default; and
`counted_assistance_enabled` now defaults **True**. `SETTINGS_VERSION` went **12 → 14** (v1.6.0
shipped 10). A follow-up fix (`_migrate_pre_v13_variant` in `bridge/mod_settings.py`) flips a
pre-v13 store's `progress_bar_variant` raw int 0↔1 during `register()`'s migration branch, keyed
on the absence of the v13-introduced `progress_show_events` key (no stored version int to compare
against directly), so an upgrading v1.6.0 user keeps the bar they actually chose across the
reorder — no `SETTINGS_VERSION` bump of its own. Player docs (`README.md`, `INSTALL.md`,
`installer/readme.moe.txt`) were reconciled against the v14 panel in both EN and UA halves.
Both channels now ship the **same single build** (WG-API threshold source): the GitHub release
carries `MoECalculator-Setup-<ver>.exe` + the bare `.wotmod`, and `MoECalculator_<ver>.zip`
(same `.wotmod` + vendor deps) is uploaded manually to
[wgmods.net/7745](https://wgmods.net/7745/). Since **v0.3.0** the installer and the zip also
bundle **Aslain ModsSettingsAPI 1.6.4** (migrated from izeberg 1.7.0 in v1.3.0) alongside
OpenWG GameFace, plus **Mods List API**
(`installer/vendor/me.poliroid.modslistapi_1.7.8.wotmod`, added in v1.3.0) which surfaces the
settings in the in-game "Modification list" window. The installer self-update reads the GitHub Atom
feed, so keep the `vX.Y.Z` tag + `MoECalculator-Setup-<ver>.exe` asset-name convention. Follow
`wotmod:release` for the bump→tag→build→publish flow.
**1.8.0 (2026-08-03)** is a minor bump carrying three feature commits (`d80a739`, `ec614e3`,
`0d5496d`). It adds **Ctrl+drag reposition for the two centre-screen in-battle progress bars** —
a new column-1 **"Bar Position"** MSA category with two `NumericStepper`s `progress_bar_pos_x` /
`progress_bar_pos_y` (default **0** = auto), **one** shared position for both bar variants —
contrast the Garage widget's own drag, which has a Shift axis-lock; the battle bars have **no**
Shift lock. **`Large` scale mode was shrunk**: `SIZE_F` **1.5 → 1.25**, so the total x factor is
now **5/3** (was 2×1.5). A new **"Hold Duration (s)" slider** `progress_hold_seconds` (range
1–30, default **5**) was added under the Transitions category — a configurable hold has to
correct the baked fade/hold/fade keyframe's deadline (a no-op at the shipped 5s default). On the
**Moving Average bar**, the axis floor moved **off** the held mark's requirement onto a
`preAvg`-extrapolated floor, and the next-mark caption now also renders an **ETA in battles** (a
`quest_type` battles glyph + count); new constants `PROGRESS_AXIS_MIN_WINDOW` /
`PROGRESS_ETA_MARGIN` / `PROGRESS_ETA_CAP`, the ProgressVM went **14 → 15** properties for
`etaBattles`, and `.mp-capL` was removed entirely. The **MSA panel** gained five new `Empty`
spacer rows, real tooltips (11 languages) for **Mode**, **Scale**, and the Garage **Position**
sub-label, and the Transitions master's row label was renamed to **"Enabled"** (varName
unchanged, deliberately). `SETTINGS_VERSION` went **14 → 19** (15/16 = the Empty spacers in
`d80a739`; 17 = the Transitions category promotion + the hold slider; 18 = the Bar Position
category + its two steppers; 19 = one more Empty spacer) — every layout-affecting change got its
required forward bump; `0d5496d` touched no MSA structure so it correctly owes none. Saved values
migrate across each bump; no `varName` was renamed. Player docs were reconciled this release
(`README.md`, `INSTALL.md`, `installer/readme.moe.txt`, both EN and UA halves) — struck the now-
false "the bar's position is not configurable / is fixed" claims, corrected the stale Large-mode
ratio prose, and documented the Bar Position / Hold Duration controls and the ETA readout.
`INSTALL.md` is English-only (it has no genuine UA half), unlike `README.md` and
`readme.moe.txt`.

**Every release cut MUST reconcile the player docs** — `README.md`, `INSTALL.md` and
`installer/readme.moe.txt` — against the user-facing surface shipped since the last tag: new or
renamed settings controls, changed defaults, new widgets. Walk `git log <lasttag>..HEAD` for those
three, and apply **every** edit to **BOTH language halves** of the bilingual files (EN + UA). This
is required, same as bumping the version files: player docs have silently missed two feature
releases (1.4.0's garage drag-to-reposition, 1.6.0's two centre-screen bars) precisely because no
step checked them.

**Every release cut MUST refresh this "Release state" prose** to the newly published version —
promote it to "current Latest", add the prior version to the history line, and correct the
canonical `src/meta.xml` value noted above. Treat this edit as a required, non-optional step of
the release, same as bumping the version files. **Do NOT** end the post-release summary with a
reminder to manually upload the zip to wgmods — the maintainer already knows the zip is a manual
upload and has asked not to be reminded.

**GitHub release title = `vX.Y.Z` (v-prefixed), strictly.** Both the tag AND the release title
are `vX.Y.Z` (e.g. `v1.3.0`) — never the bare `X.Y.Z`. Every prior release (v0.1.0 … v1.3.0)
follows this. Create with `gh release create vX.Y.Z --title "vX.Y.Z" …`, then verify
`gh release view vX.Y.Z --json name --jq '.name'` prints `vX.Y.Z`; fix drift with
`gh release edit vX.Y.Z --title "vX.Y.Z"`.

**Upload the pinned `.sha256` next to the Setup `.exe`.** The installer's self-updater
(`installer/moe_calculator-setup.iss`) downloads `<SetupBaseName>-<ver>.exe.sha256`
alongside the `.exe` and refuses to run the downloaded installer on a missing or
mismatched hash. `build_installer.ps1` writes `MoECalculator-Setup-X.Y.Z.exe.sha256`
next to the built `.exe` automatically -- upload BOTH files as release assets every
release, or every existing install's self-update silently refuses to run the new one.
