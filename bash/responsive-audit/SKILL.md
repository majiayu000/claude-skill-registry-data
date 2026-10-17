---
name: responsive-audit
description: Run a visual responsive and dark-mode audit of a website or local page with iris — captures desktop, iPhone and iPad side by side (light, and dark on request), then reports layout, overflow, overlap and contrast issues with concrete fixes. Use when the user asks to check a page on multiple devices, do a responsive check, a cross-browser-viewport audit, or compare light vs dark rendering.
license: MIT
compatibility: Requires iris + a Chrome-family browser (Chrome, Chromium, Edge, Brave). Both auto-installed by scripts/install.sh (network needed; Linux may need sudo for system libs).
allowed-tools:
  - Bash(bash scripts/doctor.sh)
  - Bash(bash scripts/install.sh)
  - Bash(iris:*)
  - Read
---

# Responsive audit — same page, three viewports, one report

Capture the SAME url in every relevant viewport, then visually inspect each
capture and report defects. Use iris (real Chrome, smart waits) — never a
static proxy screenshot.

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

## Capture matrix

Save under `shots/audit/` (create the dir). Full page for the audit, viewport
shots when the user points at a specific section.

```bash
# light
iris --full -s desktop <url> -o shots/audit/desktop-light.png
iris --full -s iphone  <url> -o shots/audit/iphone-light.png
iris -s ipad           <url> -o shots/audit/ipad-light.png

# dark (only when the user asks, or the page advertises a dark theme)
iris --full -s desktop --dark <url> -o shots/audit/desktop-dark.png
iris --full -s iphone  --dark <url> -o shots/audit/iphone-dark.png
```

Heavy pages: add `--timeout 60`. If a capture reports `scale: 1.0` in `--json`
output, the page exceeded the ~16k px limit and fell back from @2x — note it
in the report and consider auditing sections instead.

## Inspection checklist (per viewport)

Open each PNG (Read tool) and check, in order:

1. **Overflow / clipping** — text cut off, elements running past the viewport,
   horizontal scroll, truncated labels.
2. **Overlap** — elements stacking on each other (hero over navbar, fixed
   footers covering content, modals under headers).
3. **Layout integrity** — broken grids, collapsed sections, missing images
   (broken icons), misaligned columns, stretched logos.
4. **Typography** — illegible sizes, awkward line breaks, font fallbacks.
5. **Dark mode** (when captured) — white-on-white, unstyled surfaces, images
   without dark variants, low-contrast text.
6. **Mobile specifics** (iPhone) — tap targets < 44 px, horizontal carousels
   not scrolling affordances, hamburger menu present.

## Report format

```
RESPONSIVE AUDIT — <url>  (<captured at, browser scale>)
Desktop 1440×900 : ✅ / ⚠️ / 
iPhone 390×844   : ✅ / ⚠️ / ❌
iPad 1024×1366   : ✅ / ⚠️ / ❌
Dark mode        : ✅ / ⚠️ / ❌ / (not captured)

Findings
- ❌ [viewport] what is broken — where — suggested fix
- ⚠️ [viewport] minor issue — where — optional fix

Clean areas: one line per viewport.
```

Severity: ❌ = user-facing breakage (overflow, overlap, missing content);
⚠️ = polish (contrast, spacing, minor misalignment). Be concrete: name the
element, its position, and the likely CSS cause. If everything is clean, say
so explicitly — an empty audit is a useful result.
