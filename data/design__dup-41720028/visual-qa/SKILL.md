---
name: visual-qa
description: Use when making UI/styling changes and need to verify no visual regressions - provides screenshot capture, comparison, vision model scoring, and video recording for animations
---

# Visual QA

## Overview

Capture screenshots before/after changes, compare pixel diffs, score with vision models. Use video capture for animations.

## Quick Reference

| Task | Command |
|------|---------|
| **Capture baseline** | `bun visual_qa/capture_anchors.mjs --base-url http://localhost:4321 --start-dev --label baseline "#about" "/cv"` |
| **Capture candidate** | Same command with `--label candidate` (auto-compares to baseline) |
| **Add CSS labels** | Add `--annotate` flag to overlay selector labels |
| **Score screenshot** | `llm -m openrouter/qwen/qwen2.5-vl-32b-instruct -a image.png "$(cat visual_qa/standard_rubric.md) Score this."` |
| **Compare two images** | `llm -m ... -a baseline.png -a candidate.png "Compare. Flag regressions."` |
| **Record video** | See Animation Workflow below |

## Core Workflow

1. **Before changes**: Capture baseline screenshots
2. **Make changes**: Edit CSS/components
3. **After changes**: Capture candidate (auto-compares)
4. **Review diffs**: Only images marked as changed need review
5. **Score if needed**: Use vision model to score or compare

## Animation Workflow

**Use video capture when:** Testing animations, transitions, or interactive UI state changes.

**Do NOT use for routine testing** - video burns tokens. Screenshots suffice for static content.

```javascript
// In Playwright test or script:
const context = await browser.newContext({
  recordVideo: { dir: 'visual_qa/videos/' }
});
const page = await context.newPage();
await page.goto('http://localhost:4321/#about');
await page.waitForTimeout(5000); // Capture full animation cycle
await context.close(); // Video saved on close
```

**Analyze with vision model (use Gemini for video):**
```bash
llm -m gemini/gemini-flash-latest \
    -a visual_qa/videos/recording.webm \
    "This is a 5-second recording of a fade animation. Is the timing smooth? Any visual glitches?"
```

## Extending the Rubric

Add custom metrics (max score increases by 2 per metric):

```bash
llm -m openrouter/qwen/qwen2.5-vl-32b-instruct \
    -a image.png \
    "$(cat visual_qa/standard_rubric.md)

6. Animation smoothness
   - 0: Janky, stuttering, or inconsistent timing
   - 1: Generally smooth with minor hesitations
   - 2: Buttery smooth, professional feel

Score all 6 metrics (0-12 max)."
```

## Interpreting Scores

- **Score drop with intentional content change**: Not a regression if layout remains clean
- **Score drop without content change**: Investigate specific metrics that dropped
- **Use comparison prompt** to identify specific regressions rather than just scores

## Files

- `visual_qa/capture_anchors.mjs` - Screenshot capture at all breakpoints
- `visual_qa/compare_images.mjs` - Pixel diff comparison
- `visual_qa/standard_rubric.md` - 5-metric scoring rubric (0-10)
