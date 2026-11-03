---
name: marketing-page-cro
description: Optimize a landing or product page for conversion — headline, value proposition, CTA, social proof, objections and layout — with prioritized fixes and A/B test ideas. Use when a specific marketing page gets traffic but too few visitors click, sign up or buy. Not for a form, popup or signup flow; see /marketing-form-cro, /marketing-popup-cro or /marketing-signup-flow-cro.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: marketing
  phase: 2
  artifact: 02-act.md
---

# Page CRO

Optimize landing pages and product pages for "$ARGUMENTS". Analyze current conversion performance and recommend improvements to increase conversion rate.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"marketing-page-cro","workflow":"marketing","phase":2,"project":"<project>","event":"skipped","artifact":"02-act.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 2 (Act) of the RACE Framework workflow (`marketing`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `marketing` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"marketing-page-cro","workflow":"marketing","phase":2,"project":"<project>","event":"refused","artifact":"02-act.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"marketing-page-cro","workflow":"marketing","phase":2,"project":"<project>","event":"started","artifact":"02-act.md","note":""}`.

Read `.singularskills/marketing/<project>/00-strategy.md`. If this file does not exist, tell the user:

> Phase 0 (Strategy) has not been completed for "<project>". Run `/marketing-customer-research <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context:**
   - Read `.singularskills/marketing/<project>/00-strategy.md` for audience and positioning
   - Read `.singularskills/marketing/<project>/02-act.md` if it exists

2. **Page audit (if URL provided):**
   - Use WebFetch to analyze the page
   - Evaluate: headline clarity, value proposition visibility, CTA prominence, social proof, objection handling
   - Check page speed and mobile experience
   - Identify friction points in the conversion path

3. **Analyze page structure:**
   - Above-the-fold content: does it answer "what, who, why"?
   - Information hierarchy: is the most important content most prominent?
   - Visual flow: does the eye naturally reach the CTA?
   - Content length: appropriate for the decision complexity?

4. **CRO recommendations:**
   - Headline and subheadline improvements
   - CTA placement, copy, and design recommendations
   - Social proof placement and type
   - Objection handling and FAQ placement
   - Trust signals (security badges, guarantees, testimonials)
   - Page speed and technical improvements

5. **A/B test suggestions:**
   - Identify the highest-impact elements to test
   - For each: hypothesis, variant description, expected impact
   - Prioritize by potential uplift and ease of implementation

6. **Write the artifact** — append to `.singularskills/marketing/<project>/02-act.md` under a `## Page CRO` section. Create the file with a `# Act — <project>` heading if it does not exist; if a `## Page CRO` section already exists, replace only that section. The section contains:
   - **Current State Assessment** — strengths and weaknesses
   - **Recommendations** — prioritized by impact
   - **A/B Test Suggestions** — with hypotheses
   - **Wireframe Notes** — suggested layout changes
   - **Expected Impact** — estimated conversion lift per change

## Output

Page CRO analysis appended to `.singularskills/marketing/<project>/02-act.md`. Present a summary highlighting:
- Top 3 conversion blockers identified
- Highest-impact recommendation
- Suggested first A/B test

**Record the run.** After you have written your section, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"marketing-page-cro","workflow":"marketing","phase":2,"project":"<project>","event":"finished","artifact":"02-act.md","note":""}`.

This artifact is shared by every skill of phase 2 (Act). The frontmatter is written once, by whoever creates the file: if you create it, open it with the block below (`skill` is the phase title, `started` the time of that first write; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`); if it already exists, leave the block alone except to update `finished` and to set `gate` to the worst value among the sections (`skipped` over `passed`).

```yaml
---
skill: Act
workflow: marketing
phase: 2
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: <passed|skipped>
---
```

Open your `## Page CRO` section with one italic line, `*<skill name> · <ISO timestamp> · gate: <passed|skipped>*` (your skill name is `marketing-page-cro`).

End your section with `### Decisions` and `### Open questions` (one level under your `## Page CRO` heading, so the section stays one block), in this shape:

```markdown
### Decisions
- <what was chosen> — <why> — <what was rejected>

### Open questions
- <what the next phase or a reviewer must settle>
```
