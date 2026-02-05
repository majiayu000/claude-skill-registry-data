---
name: page-diff
description: Visual regression testing for web pages. Compares screenshots to detect UI changes, generates overlay images highlighting differences. Use after making frontend changes to verify visual correctness, catch unintended side effects, or validate that changes look as expected.
---

# Page Diff

Compare screenshots to detect visual changes. Outputs similarity percentage and an overlay image with differences highlighted in magenta.

## Usage

```bash
uv run .claude/skills/page-diff/scripts/diff.py <expected> <actual>
```

**Output:**
```
PASS: 99.2% similar (3,247 pixels differ)
/path/to/overlay.png
```

The overlay image shows the actual screenshot with changed regions tinted magenta. Use `Read` to view it.

## Baselines

Store known-good screenshots in `baselines/`:

```
.claude/skills/page-diff/baselines/
├── demo.png
├── settings.png
└── upload-complete.png
```

**Workflow:**
1. Capture baseline: `browser_take_screenshot` → save to `baselines/demo.png`
2. Make changes, reload
3. Capture current: `browser_take_screenshot` → `/tmp/current.png`
4. Compare: `uv run .claude/skills/page-diff/scripts/diff.py baselines/demo.png /tmp/current.png`
5. If diff is expected, update baseline

## Interpreting Results

- **100% identical**: No visual changes
- **>99% similar**: Minor differences (anti-aliasing, subpixel rendering) - usually a PASS
- **<99% similar**: Meaningful changes detected - review the overlay

When similarity is lower than expected, view the overlay image to see exactly what changed. Correlate with your code changes to determine if the diff is intentional.

## Options

```bash
--threshold, -t   Color difference threshold (0-1). Default: 0.1
                  Higher = more tolerant of minor color variations

--alpha, -a       Overlay tint transparency (0-1). Default: 0.5

--output, -o      Custom output path for overlay image
```

## Fixes

