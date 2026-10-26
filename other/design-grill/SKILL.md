---
name: design-grill
description: "Interviews the user to settle every design system decision, asking in dependency order and writing an HTML preview for each round so the user chooses by looking instead of reading numbers. Produces .design/decisions.json. Use as phase 2 of design-system, after design-extract."
---

# Design Grill

Settle every design decision with the user, one round of questions at a time. Some decisions depend on others (you can't choose spacing sizes before the spacing grid), so ask them in order.

Each round is an HTML file the user opens in a browser. Nobody can judge a type scale, spacing or color from numbers in a terminal.

## Before you start

```bash
test -f .design/drift.json || echo "MISSING"
```

If it's missing, stop and run `design-extract` first. Its counts are what let the user check each recommendation.

## How each round works

Read `references/design-tree.md`. It lists every decision, what each one depends on, and its default.

Each round follows the same loop:

```
find ready questions -> answer what the data already answers -> render the preview -> ask -> wait -> record -> repeat
```

### 1. Find the questions that are ready

A question is ready when every decision it depends on is already made. Ask all the ready questions in one round. Round 1 is always just product character, because everything else depends on it.

### 2. Answer what the data already answers

For each ready question, check `drift.json`. If one value already covers 90% or more of usage in that category, don't ask. Show it in the round as already settled, with the percentage, and move on.

Look up anything you can measure. Only ask the user about things the code can't answer.

### 3. Render the preview

Write `.design/grill/round-N.html`: a single file with no build step that opens directly in a browser. Start from `assets/round-shell.html`.

The preview must:

- Use the project's own fonts and colors, read from the codebase.
- Show the options side by side, labelled A, B, C.
- Use real text from the app. No lorem ipsum, because placeholder text hides problems like lines that run too long.
- Mark the recommended option and show how many current values it fits.
- Show light and dark versions if the project has both.
- Fit a 375px-wide screen without scrolling sideways.

### 4. Ask in the terminal

Print the file path first, then the questions:

```
Round 2 preview: .design/grill/round-2.html

SETTLED **Radius**: rounded-lg on 94% of surfaces. Using it as the base.

---

**Q1. Spacing grid**: 4px or 8px. Options A and B in the preview show the same card on each grid.

> **A, 4px.** Fits 24 of your 31 current spacing values. 8px fits 13 and would mean rewriting 11.

---

**Q2. Type scale**: each font size 1.200× or 1.250× the one below it, shown in Inter with your text.

> **B, 1.250.** Fits 11 of your 14 current sizes. Your largest heading is already about 1.24× body text.
```

Number every question. Back every recommendation with a number from `drift.json`. Separate questions with `---`.

### 5. Wait for answers

Wait for the user to answer before starting the next round. Don't move on if they go quiet, and don't ask the next round's questions early.

If the user picks something other than your recommendation, accept it. Then work out which later questions it affects and tell the user what changed. For example: "With an 8px grid, 6px and 10px are no longer options, so round 3 will offer 4 spacing sizes instead of 6."

## Record each answer

After each round, add the answers to `.design/decisions.json`:

```json
{
  "character": { "value": "dense-productive", "source": "user", "round": 1 },
  "radius.base": { "value": "0.5rem", "source": "pre-settled", "evidence": "94% of surfaces" },
  "spacing.base": { "value": 4, "source": "user", "recommended": 4, "round": 2 }
}
```

`source` says where each answer came from: `user` if the user chose it, `pre-settled` if the data answered it, `default` if the default was used. `design-ratify` reads this field to decide which decisions get a written note.

## Finish

The phase is done when no questions are left, not when you feel you know enough.

Print every decision and wait for the user to confirm before handing off to `design-ratify`.
