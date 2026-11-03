---
name: branding-visual
description: Define a brand's visual identity — logo usage rules and variations, a color palette with contrast ratios, typography and type scale, and photography, illustration and icon style. Use when the user needs to settle their brand colors, fonts, logo rules or imagery style, or formalize the visual assets they already have.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: branding
  phase: 4
  artifact: 04-visual.md
---

# Visual Identity

Define the visual identity system for "$ARGUMENTS". Create specifications for logo usage, color palette, typography, and imagery that express the brand visually.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"branding-visual","workflow":"branding","phase":4,"project":"<project>","event":"skipped","artifact":"04-visual.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 4 (Visual) of the Brand Identity Process workflow (`branding`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `branding` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"branding-visual","workflow":"branding","phase":4,"project":"<project>","event":"refused","artifact":"04-visual.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"branding-visual","workflow":"branding","phase":4,"project":"<project>","event":"started","artifact":"04-visual.md","note":""}`.

Read `.singularskills/branding/<project>/02-strategy.md` and `.singularskills/branding/<project>/03-verbal.md`. If `03-verbal.md` does not exist, tell the user:

> Phase 3 (Verbal) has not been completed for "<project>". Run `/branding-verbal <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context files:**
   - Read `.singularskills/branding/<project>/02-strategy.md` for personality and positioning
   - Read `.singularskills/branding/<project>/03-verbal.md` for voice and tone

2. **If the user has existing assets:**
   - Review logo files in `.singularskills/branding/<project>/assets/logo/`
   - Review fonts in `.singularskills/branding/<project>/assets/fonts/`
   - Review imagery in `.singularskills/branding/<project>/assets/imagery/`
   - Document and formalize what exists

3. **If creating from scratch, define:**

   **Logo usage rules:**
   - Minimum size, clear space requirements
   - Approved variations (primary, icon, monochrome, reversed)
   - Prohibited uses
   - Ask the user to provide/create logo files and place in `.singularskills/branding/<project>/assets/logo/`

   **Color palette:**
   - Primary colors (2-3) with hex, RGB values
   - Secondary colors (2-4) with hex, RGB values
   - Neutral colors for backgrounds and text
   - Accessibility: contrast ratios for text on each background

   **Typography:**
   - Primary typeface: name, weights, usage (headings vs. body)
   - Secondary typeface (if needed)
   - Type scale: sizes, weights, line heights for each level
   - Ask the user to provide font files and place in `.singularskills/branding/<project>/assets/fonts/`

   **Imagery style:**
   - Photography style (mood, composition, subjects)
   - Illustration style (if applicable)
   - Icon style
   - Do's and don'ts

4. **Write the artifact** to `.singularskills/branding/<project>/04-visual.md`

## Output

The visual identity written to `.singularskills/branding/<project>/04-visual.md`. Present a summary to the user highlighting:
- Primary color palette
- Typography choices
- Logo variations defined
- Imagery direction

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"branding-visual","workflow":"branding","phase":4,"project":"<project>","event":"finished","artifact":"04-visual.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: branding-visual
workflow: branding
phase: 4
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: <passed|skipped>
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```
