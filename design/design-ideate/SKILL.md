---
name: design-ideate
description: Explore at least three visual and layout approaches for a specified component, compare their trade-offs against its contract and recommend one. Use when the component's spec exists and the user wants options to choose from before building it in Figma. Not for solution concepts to a broader problem; see /research-design.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: design
  phase: 3
  artifact: 03-ideate.md
  figma-aware: true
---

# Ideate

Generate multiple design options for "$ARGUMENTS" before committing to a single approach. Encourage creative exploration by producing at least 3 distinct options.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"design-ideate","workflow":"design","phase":3,"project":"<project>","event":"skipped","artifact":"03-ideate.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 3 (Ideate) of the Design Thinking workflow (`design`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `design` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

**Figma.** Steps marked *Figma* use a Figma MCP server you connect to this agent yourself; this pack ships none and makes no network calls. Before you ask the user anything or run the first such step, list the tools available to you and bind each capability the step names to one tool, as `references/figma-capabilities.md`, bundled with this skill, describes: the official Figma server's tool named there, else any tool whose description plainly does the same thing. With a capability bound, take the file key and node id from a Figma link in the request or the conversation, else from the `file:` line of the `## Tools` section of the latest earlier artifact of this project that has one; when a bound capability needs one and there is none, ask for the link once, with any other question you ask. With nothing bound, never ask for a link. Record the result in a `## Tools` section after any `## Recalled` section: a `- file:` line (the Design file; a board or a deck goes on a `- board:` or `- deck:` line), one line per bound capability (`- read-tokens: get_variable_defs (figma)`), and a `- created:` line for node ids you created; or the single line `No Figma server: steps marked Figma ran without one.`; a skill with no artifact says the same in its summary. For an unbound capability do what the step's *Without Figma* line says, using first any values the user gave in the request or in files it names: never ask the user to connect a server, never invent values a tool would have returned, and never report a step as run when it was not.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"design-ideate","workflow":"design","phase":3,"project":"<project>","event":"refused","artifact":"03-ideate.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"design-ideate","workflow":"design","phase":3,"project":"<project>","event":"started","artifact":"03-ideate.md","note":""}`.

Read `.singularskills/design/<project>/02-define.md`. If this file does not exist, tell the user:

> Phase 2 (Define) has not been completed for "<project>". Run `/design-define-component <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context files:**
   - Read `.singularskills/design/<project>/01-empathize.md` for research findings (if exists)
   - Read `.singularskills/design/<project>/02-define.md` for the component contract
   - Read `references/wcag-criteria.md` for accessibility constraints

2. **Read the design system.** *Figma (read-tokens):* read the file's variables and styles for the token values each option maps to. *Without Figma:* read the values the user gave (in the request or in files it names), then the project's own token sources (a `tokens` package, CSS custom properties, a Tailwind config), else map options to token roles and mark the values `not checked`.

3. **Generate 3+ design options.** For each option:
   - Describe the visual approach and layout strategy
   - Map which tokens from the design system would be used
   - Evaluate against the component contract's constraints
   - Assess accessibility compliance
   - Note trade-offs (complexity, flexibility, consistency)

4. **Board the options** (only when the request or the conversation gives a `figma.com/board/` link). *Figma (write-figjam):* add one sticky per option and a table with the comparison matrix to that board, and record the board link on a `- board:` line of the `## Tools` section (never on the `- file:` line). *Without Figma:* skip this step; the comparison matrix in the artifact is the board.

5. **Recommend one approach** with clear rationale explaining why it best satisfies the component contract.

6. **Write the artifact** to `.singularskills/design/<project>/03-ideate.md`

## Output

The ideation document written to `.singularskills/design/<project>/03-ideate.md`. Present a summary to the user highlighting:
- Number of options explored
- Recommended approach and rationale
- Key trade-offs between options
- Any contract constraints that were difficult to satisfy

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"design-ideate","workflow":"design","phase":3,"project":"<project>","event":"finished","artifact":"03-ideate.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: design-ideate
workflow: design
phase: 3
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
