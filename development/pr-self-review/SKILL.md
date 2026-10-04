---
name: pr-self-review
description: Guide authors through a structured self-review before requesting peer review.
license: MIT
compatibility: claude cursor opencode
metadata:
  version: "1.0.0"
  languages: all
  audience: developers
  workflow: analysis
  since: "2026-02-24"
---

## What I do

I help you review your own pull request through a structured five-category checklist before you request external review:

1. **Description Accuracy** — Does the PR description match what you actually changed?
2. **Scope** — Are all files in the diff intentionally included? Any surprises?
3. **Artifact Cleanup** — Any leftover debug code, console logs, TODOs, or commented-out lines?
4. **Test Coverage** — Does every changed function/method have at least one test?
5. **Single Concern** — Could this PR be split into two separate PRs?

By catching issues before external review, you save reviewers' time and reduce review cycles.

Supporting files in this skill:
- `assets/self-review-checklist.template` — The five-category checklist as a markdown file you can copy into a PR comment

## When to use me

Use when you want to:
- Review your own PR before requesting external review
- Catch obvious mistakes and missed artifacts before reviewers see them
- Ensure your PR is focused on a single concern
- Verify test coverage for all your changes
- Reduce back-and-forth on revision cycles

## PR lifecycle focus

Stage: **Author pre-review checklist** (after implementation, before external review).

## Use Instead [if available]

- Use `pr-create` when you need to draft the PR title/body before opening it.
- Use `pr-review` when reviewing someone else's PR as a reviewer.
- Use `pr-split` when the core question is whether to split a large PR.

## Example usage

"Review my own PR before I request review"
"Walk me through a self-review checklist"
"Help me check my PR for debug code and missing tests"

---

## Workflow

Here's how I guide you through self-review:

### Step 1: Get the Diff
I'll ask for your PR diff or a link to the open PR if not provided in context.

### Step 2: Description Check
I'll ask: **Does the PR description accurately describe every file in the diff?**
- Read the description you wrote
- Review the actual diff
- Flag any mismatches (e.g., "description says 'add auth', but diff also changes payment logic")

### Step 3: Scope Check
I'll ask: **Are all files in the diff intentionally included?**
- Look for files that seem unrelated to the stated purpose
- Flag any surprises (e.g., "why is the config file changed when this is a feature PR?")
- Ask you to confirm each unexpected file is intentional

### Step 4: Artifact Cleanup Check
I'll ask: **Are there any obvious leftover debug artifacts?**
I'll flag obvious issues like:
- `console.log`, `print`, `println`, `println!` (debug output)
- `debugger`, `pdb`, `debug!` (breakpoints)
- `.only`, `.skip` on test cases (ensures tests run)
- Large commented-out code blocks

For TODO/FIXME comments, I'll ask: did you intend to resolve these before requesting review?

**Note**: Thorough artifact detection is your reviewers' job—this catches the obvious ones you might have missed.

### Step 5: Test Coverage Check
I'll ask: **Does every changed function/method have test coverage?**
- For each changed function or method, confirm at least one test covers it
- Check that test files were also changed to add new tests
- Flag any logic changes with no corresponding tests

### Step 6: Concern Focus Check
I'll ask: **Is this PR focused on a single concern, or does it mix unrelated changes?**
- Look for multiple distinct concerns (e.g., "auth changes + refactoring + documentation")
- Ask: "Could this be two PRs?"
- If yes, recommend splitting the PR using the `/pr-split` skill

### Step 7: Summary
I'll summarize the findings:
- ✅ Ready to request review
- ⚠️ Minor issues to resolve before review
- ⛔ Major issues blocking external review

---

## Tips for Success

- **Review as a stranger would** — Imagine someone unfamiliar with your code reading your diff
- **Be honest about artifacts** — Debug code hidden from reviewers wastes their time
- **Verify test coverage manually** — Don't assume tests exist; confirm they do
- **Check the PR description against reality** — Description drift is the most common pre-review failure
- **Consider scope early** — If you spot multiple concerns now, split the PR before requesting review
- **Copy the checklist into your PR** — Leave a visible record that you self-reviewed
