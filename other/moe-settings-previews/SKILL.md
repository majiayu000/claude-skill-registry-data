---
name: moe-settings-previews
description: Invoke when the MoE Calculator settings-panel widget preview PNGs must be regenerated — after ANY change to the shipped in-battle widget CSS/JS that alters a widget's look (MoEBattle*, MoEEfficiency*, MoEProgress*, MoEBarTransient), or when adding/altering a preview.
---

# Regenerating the settings-panel preview PNGs

Six transparent PNGs at `src/res/gui/maps/icons/moe_calculator/previews/`, shown live in the
MSA settings panel via two `Image` controls (`mod_settings.py` `CALC_PREVIEW_KEY` /
`BAR_PREVIEW_KEY`), so the user can see a widget's look without starting a battle:

- `calc_assist_on.png` / `calc_assist_off.png` — in-battle calculator, `countedAssist` 3-row / 2-row.
- `bar_eff_horizontal.png` / `bar_eff_vertical.png` — Damage Efficiency bar, both orientations.
- `bar_ma_horizontal.png` / `bar_ma_vertical.png` — Moving Average (Progress) bar, both orientations.

Full background/rationale: `TASKS/settings-preview-images.md`.

## Run the generator

```
py tools/dev/gen_settings_previews.py
```

Dev-only deps: `py -m pip install pillow playwright` (no `playwright install` / browser
download needed). It drives the system WebView2-runtime Chromium
(`C:\Program Files (x86)\Microsoft\EdgeCore\<ver>\msedge.exe`, globbed — highest version wins)
via Playwright, `omit_background=True`, `device_scale_factor=4` (SUPERSAMPLE — real Chromium
supersampling, not a post-hoc PIL upscale), waits for the hold-fade-in, floors output alpha,
then Pillow alpha-bbox-crops. Ships the FULL 4x crop — MSA's own `width`/`height` do the
downscale at render time.

Source tuners (`tools/dev/gen_settings_previews.py`'s `_JOBS`):
- `TASKS/refs/in-battle-overlay-tuner.html` — calculator (both assist states via
  `setAssist(false)`).
- `tools/dev/eff_bar_tuner.html` / `eff_bar_tuner_vertical.html` — Damage Efficiency H/V.
- `TASKS/refs/in-battle-bar-tuner.html` / `in-battle-bar-tuner-vertical.html` — Moving Average
  H/V.

Each bar job uses the tuner's OWN default on-load state (the same state its `check_*.js` gate
already verifies) — do not drive it. `_STRIP_SCENE_CSS` hides the tuner's own scene dressing
(`.panel`, `#ribbons`, `#mmMock`, `#loupe`) before the shot; none of that is shipped widget CSS.

## Accuracy gate — MANDATORY before trusting any render

1. **The tuners derive from the shipped CSS, not the reverse.** If shipped widget CSS changed,
   regenerate the tuners FIRST: `pwsh tools/dev/gen_bar_tuner_vertical.ps1 -EmitCss`,
   `node tools/dev/make_eff_vertical_artifact.js`, `pwsh tools/dev/gen_overlay_tuner.ps1`, and
   refresh any gate reference the documented way (see moe-progress / moe-battle skills).
2. Run ALL four drift gates and require GREEN before rendering:
   `node tools/dev/check_eff_css.js`, `check_eff_vertical.js`, `check_bar_vertical.js`,
   `check_overlay_css.js`.
3. **These gates are BYTE-level, not geometry-level.** They diff CSS text/tokens — they do NOT
   catch rendered icon/backdrop MISPOSITIONING. When geometry changed, also measure elements via
   Playwright `getBoundingClientRect()` against the shipped CSS's intended positions before
   trusting a render. A gate-green tuner can still paint icons in the wrong place — this bit the
   `bar_ma_horizontal` and `bar_eff_horizontal` renders (see Gotchas below).

## Wiring the output (mod_settings.py)

- MSA `Image` `source` is a **bare Scaleform resource path**,
  `gui/maps/icons/moe_calculator/previews/<name>.png` — **never** the Gameface `img://` scheme.
  MSA's Image control is Scaleform/AS3 feeding a WG `UILoaderAlt`/`Loader`; an `img://` URL
  fails silently there, leaving the reserved box blank (`mod_settings.py:501-506`).
- The PNGs are 4x-supersampled; MSA must DOWNSCALE. `_PREVIEW_DISPLAY` (`mod_settings.py:514`)
  maps each name → display `(w, h)` px, passed as `width`/`height` on both the `_image`
  descriptor and every `updateImage` swap. NOT yet live-confirmed that MSA's AS3 loader honors
  `width`/`height` as a scale rather than a crop — revisit if the live panel shows cropped/
  unscaled previews.
- `_CALC_PREVIEW_W/H` and `_BAR_PREVIEW_W/H` (the reserved container size) = the MAX display
  dims across each swappable set, so the panel doesn't jump when the image swaps.
- Both preview varNames are addressing handles for `updateImage`, deliberately absent from
  `DEFAULTS` — never treat them as a stored setting or give them a template row (that whole
  class of bug is documented in memory `msa-drops-any-varname-without-a-template-row` and its
  family — these two are the deliberate exception since they're never persisted).
- **After regen:** if any render's display size changed, update `_PREVIEW_DISPLAY` (and the two
  container maxes) and the three pin tests in `tests/test_mod_settings.py`.

## Gotchas (all live-confirmed during the build/tuning pass)

- **Alpha haze.** `omit_background` capture over stacked masked/gradient layers leaves a
  low-alpha (~0-40) veil across nearly the whole stage — independent of GPU vs software render
  (`--disable-gpu`, `--disable-gpu-compositing`, `--use-gl=swiftshader` all tried, none changed
  it). Fix is an OUTPUT alpha floor (T=45 for bars, T=10 for the calculator — its page has no
  haze), not a launch arg. The flat T=45 floor applies to all bars (the protected-floor
  machinery was removed); the backdrop is hidden via `_STRIP_SCENE_CSS`.
- **Wait ≥2s before capture.** The bars hold-fade in on load; a short wait under-renders every
  alpha value (calculator has no such fade — 200ms suffices there).
- **The bare Edge CLI is broken for this.** `msedge.exe --screenshot
  --default-background-color=00000000` caps captured alpha at ~41/255 on this build — must go
  through Playwright's `omit_background`, not the CLI flag.
- **Raster `.pkg` icons cap at source resolution** — quest glyphs 128x128, marksOnGun pips have
  no larger variant. Supersampling the PAGE doesn't fix an icon asset that was already small; a
  hard crispness ceiling for those specific glyphs, not a bug in this pipeline.
- **`calc_assist_off` must TOP-align, not center-pad, into `calc_assist_on`'s taller canvas.**
  The two share a container so the panel doesn't jump when `countedAssist` toggles between the
  2-row and 3-row calculator, but `calc_assist_on` (3 rows) is strictly taller. Center-padding
  the shorter `off` crop into that canvas shifts rows 1/2 vertically relative to `on` — the
  "toggling the 3rd row moves the whole preview" regression, since rows 1/2 are the SAME content
  in both states and must stay registered at the same y. Top-align (`y = 0`) instead: rows 1/2
  land identically in both crops, and the missing 3rd row becomes transparent padding at the
  BOTTOM only. This is a deliberate product decision (no shift on toggle beats a standalone
  centered look) — see `gen_settings_previews.py` around the `calc_assist_off` padding step for
  the exact code and comment.

## Verify

- Composite each PNG onto the MSA dark panel colour (`#2b2d30`) and eyeball; an HTML gallery
  artifact (4x source next to its display-size render) is a useful throwaway for this.
- Live-only, needs a deployed client: MSA actually downscales via `width`/`height` (LIVE-ONLY,
  unconfirmed, see wiring note above), the previews render at all, and geometry reads aligned
  in-client — none of this is checkable from the dev box alone.
