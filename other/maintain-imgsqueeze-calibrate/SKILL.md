---
name: maintain-imgsqueeze-calibrate
description: "Recalibrate the quality presets of imgsqueeze by eye: build the side-by-side calibration page with mise run calibrate, let the user judge it, then change imgsqueeze/presets.py and every place that repeats the values. Use when the user says images look too compressed or not compressed enough, wants to tune a preset, or after an engine change that may shift quality."
---

Set the preset values from the user's own judgment of real images. Never pick values from a metric alone.

Read ../maintain-imgsqueeze-base/SKILL.md, then:
- ../maintain-imgsqueeze-base/references/02-compression-engines.md
- ../maintain-imgsqueeze-base/references/04-presets-and-calibration.md
- ../maintain-imgsqueeze-base/references/05-already-done.md

## Step 1: Build the page

- Ask for a folder of representative images if the user has one: 10 to 20 covering photos, text or diagrams, and smooth gradients. The four samples in `tests/img-raw` are a fallback, not a basis for a decision.
- Run `mise run calibrate -- --input <folder>` (default `tests/img-raw`). The input is never modified.
- Give the user the page, `tmp/calibration/index.html`, and the per-preset gains printed by the script. Point at what to compare: fine text and edges, gradients (pngquant banding or dithering), and preset pairs that barely differ in size.

**Stop for the user's verdict.** The values change only on the user's word, one preset and format at a time as they state it.

## Step 2: Try the change

- Edit `PRESETS` in `imgsqueeze/presets.py`. A pngquant range moves its floor (when pngquant gives up) and its ceiling (how many colors it uses) separately; a JPEG or WebP value is one quality number.
- Rerun `mise run calibrate` with the same input and show the user the new page. Repeat until the user approves.
- If the user wants a different keep threshold instead, that is `DEFAULT_MIN_GAIN`, with the reasoning in `05-already-done.md` (WebP must stay above its measured second-pass gain).

## Step 3: Update every copy of the values

- `docs/source/03-How-It-Works/index.rst` (the presets table).
- `.claude/skills/pypi-imgsqueeze/ref/public-api.md` (the presets table).
- `.claude/skills/maintain-imgsqueeze-base/references/04-presets-and-calibration.md`: the table, and the calibration date and outcome.

If `DEFAULT_MIN_GAIN` changed, also: `docs/source/02-Command-Line/index.rst` (the `--min-gain` row), `.claude/skills/pypi-imgsqueeze/SKILL.md` and `ref/cli.md`, and `05-already-done.md` section 3. The `--min-gain` help text is built from `DEFAULT_MIN_GAIN` and needs no change. Find any other copy with `grep -rn "0\.10" docs README.rst .claude/skills/pypi-imgsqueeze .claude/skills/maintain-imgsqueeze-base`.

Already compressed images are not affected: their sidecars make them done whatever the preset. Say so to the user; to apply new values to an image, they restore its original first.

## Step 4: Verify and report

- `mise run cov` passes (`tests/test_presets.py` asserts the values), and `mise run lint` is clean.
- Report the old and new values, the images they were judged on, and the files changed. Suggest a changelog entry with `pywf-oss-changelog`.
