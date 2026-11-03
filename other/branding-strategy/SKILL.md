---
name: branding-strategy
description: Define a brand platform — purpose, vision, mission, values, positioning, personality and differentiation. Use when the user asks what their brand stands for, what personality it should have, or how it should stand apart from competitors. Not for voice, product messaging or critiquing a strategy; see /branding-verbal, /marketing-product-marketing-context or /coaching-strategy.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: branding
  phase: 2
  artifact: 02-strategy.md
---

# Strategy

Define the brand strategy for "$ARGUMENTS". Synthesize discovery findings into a clear positioning, values, personality, and differentiation framework.

See also `/marketing-product-marketing-context` for the product positioning, messaging framework and go-to-market context built on this brand platform.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"branding-strategy","workflow":"branding","phase":2,"project":"<project>","event":"skipped","artifact":"02-strategy.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 2 (Strategy) of the Brand Identity Process workflow (`branding`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `branding` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"branding-strategy","workflow":"branding","phase":2,"project":"<project>","event":"refused","artifact":"02-strategy.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"branding-strategy","workflow":"branding","phase":2,"project":"<project>","event":"started","artifact":"02-strategy.md","note":""}`.

Read `.singularskills/branding/<project>/01-discover.md`. If this file does not exist, tell the user:

> Phase 1 (Discover) has not been completed for "<project>". Run `/branding-discover <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context files:**
   - Read `.singularskills/branding/<project>/01-discover.md` for research findings
   - Read `references/brand-platform-template.md` for output structure
   - Read `references/brand-prism-guide.md` for the six brand facets

2. **Define brand purpose, vision, and mission:**
   - Purpose: why does this brand exist?
   - Vision: where is the brand going?
   - Mission: what does it do, for whom, and how?

3. **Define brand values:**
   - 3-5 core values that guide all brand decisions
   - For each value: description and how it manifests in behavior

4. **Craft positioning statement:**
   - For [target audience] who [need], [brand] is the [category] that [benefit] because [reason]

5. **Define brand personality:**
   - 3-5 personality traits (e.g., bold, approachable, expert, playful)
   - For each trait: how it influences communication

6. **Map competitive differentiation:**
   - What sets this brand apart from each key competitor?
   - The unique value proposition

7. **Write the artifact** to `.singularskills/branding/<project>/02-strategy.md` following the brand platform template.

## Output

The brand strategy written to `.singularskills/branding/<project>/02-strategy.md`. Present a summary to the user highlighting:
- The positioning statement
- Core values
- Key personality traits
- Primary differentiator

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"branding-strategy","workflow":"branding","phase":2,"project":"<project>","event":"finished","artifact":"02-strategy.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: branding-strategy
workflow: branding
phase: 2
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
