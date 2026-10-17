---
name: visual-diff
description: Visually compare two states of a web page with iris — before/after a change on the same URL, or two different URLs (A/B, staging vs production) — by capturing both and producing a structured report of what added, removed, moved or restyled. Use when the user asks to compare two pages, check what changed visually, review a before/after diff, or verify a redesign matches a reference.
license: MIT
compatibility: Requires iris + a Chrome-family browser (Chrome, Chromium, Edge, Brave). Both auto-installed by scripts/install.sh (network needed; Linux may need sudo for system libs).
allowed-tools:
  - Bash(bash scripts/doctor.sh)
  - Bash(bash scripts/install.sh)
  - Bash(iris:*)
  - Read
---

# Visual diff — two captures, one honest report

Capture both states with the SAME settings, inspect them side by side, and
report the differences. iris has no pixel-diff engine: you are the diff
engine. Consistency of capture settings is what makes the comparison valid.

## Preflight (once per session)

Paths like `scripts/` and `references/` below are relative to THIS skill's
directory — run them from there, or prefix them with the skill's absolute path.

```bash
bash scripts/doctor.sh
```

If it fails, run `bash scripts/install.sh` and re-run.
If `$CHROME` is not set, add `--chrome <path printed by doctor>` to every iris
call (or export CHROME). If `iris` is not on PATH, use the absolute path
doctor printed.

## Capture (identical settings, always)

Pick ONE mode and apply it to both sides:

**A/B — two URLs**

```bash
iris --full -s desktop <url-a> -o shots/diff/a.png --json
iris --full -s desktop <url-b> -o shots/diff/b.png --json
```

**Before/after — same URL, two moments** (e.g. across a deploy or a local
change): capture the first state, make/apply the change, capture again with
the exact same flags.

Useful variants: `--selector '#component' --padding 16` to focus the diff on
one region; `-s iphone` for mobile; `--dark` on both sides.

## Cheap pre-check (before looking)

Compare the `--json` lines first:

- identical `bytes` + `css_width`/`css_height` + `scale` → almost certainly no
  visual change; say so and stop (unless the user insists).
- large `bytes` delta or different dimensions → real change; continue.

## Visual comparison (you are the diff engine)

Open both PNGs (Read tool) and scan region by region, top to bottom:

1. **Added** — elements, sections, copy present in one and not the other.
2. **Removed** — the inverse.
3. **Moved** — same content, different position/size/order.
4. **Restyled** — same content, different colors, fonts, spacing, imagery.
5. **Reflow consequences** — cascading shifts, misalignments, overflow
   introduced by the change (even if unintended).

Long pages: if the full captures are too tall to compare reliably, re-capture
both sides scoped with `--selector` on the changed region.

## Report format

```
VISUAL DIFF — <a> vs <b>   (mode: A/B | before/after, viewport, scale)
Δ metadata: bytes a→b, css size a→b, scale

Added     : - …
Removed   : - …
Moved     : - …
Restyled  : - …
Reflow    : - unintended layout fallout, if any

Verdict: no visible change | expected change (matches intent: …)
         | unexpected change — highlight the riskiest item
```

State the verdict explicitly. When the user gave an intent (“I changed the
pricing card”), check it first and say whether the change landed as intended;
then list anything the intent did not mention.
