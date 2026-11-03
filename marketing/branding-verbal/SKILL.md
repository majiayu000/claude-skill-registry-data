---
name: branding-verbal
description: Develop a brand's verbal identity — voice, tone per context, messaging pillars, taglines and style rules. Use when the user wants to define how their brand sounds, settle on a tagline, or align tone across channels. Not for positioning and personality, or product messaging per audience; see /branding-strategy or /marketing-product-marketing-context.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: branding
  phase: 3
  artifact: 03-verbal.md
---

# Verbal Identity

Develop the verbal identity for "$ARGUMENTS". Create the voice, tone, messaging framework, and language guidelines that bring the brand personality to life in words.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"branding-verbal","workflow":"branding","phase":3,"project":"<project>","event":"skipped","artifact":"03-verbal.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 3 (Verbal) of the Brand Identity Process workflow (`branding`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `branding` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"branding-verbal","workflow":"branding","phase":3,"project":"<project>","event":"refused","artifact":"03-verbal.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"branding-verbal","workflow":"branding","phase":3,"project":"<project>","event":"started","artifact":"03-verbal.md","note":""}`.

Read `.singularskills/branding/<project>/01-discover.md` and `.singularskills/branding/<project>/02-strategy.md`. If `02-strategy.md` does not exist, tell the user:

> Phase 2 (Strategy) has not been completed for "<project>". Run `/branding-strategy <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read context files:**
   - Read `.singularskills/branding/<project>/01-discover.md` for audience insights
   - Read `.singularskills/branding/<project>/02-strategy.md` for personality, values, and positioning

2. **Define brand voice:**
   - Voice is consistent — it's WHO the brand is
   - Describe the voice using the personality traits from Strategy
   - Provide "We are / We are not" examples
   - Example: "We are confident but not arrogant. We are friendly but not casual."

3. **Define tone variations:**
   - Tone adapts to context — it's HOW the brand speaks in different situations
   - Define tone for: marketing, support, social media, formal communications, error messages
   - For each context: tone description + example copy

4. **Create messaging pillars:**
   - 3-5 key messages the brand consistently communicates
   - For each pillar: headline, supporting statement, proof point

5. **Develop tagline/endline options:**
   - Generate 3-5 tagline candidates
   - Evaluate each against the positioning and personality
   - Recommend the strongest option

6. **Language guidelines:**
   - Preferred vocabulary and phrases
   - Words and phrases to avoid
   - Grammar and style preferences (e.g., Oxford comma, contractions, capitalization)

7. **Write the artifact** to `.singularskills/branding/<project>/03-verbal.md`

## Output

The verbal identity written to `.singularskills/branding/<project>/03-verbal.md`. Present a summary to the user highlighting:
- Voice description in one sentence
- Top tagline recommendation
- Messaging pillars overview

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"branding-verbal","workflow":"branding","phase":3,"project":"<project>","event":"finished","artifact":"03-verbal.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: branding-verbal
workflow: branding
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
