---
name: skill-finder
description: Use when someone asks whether a skill already exists for a task, what skill they should use, whether an existing skill can handle a proposed task, or whether they should build a new skill.
argument-hint: [task description]
allowed-tools: Read, Glob, Grep
---

## What This Skill Does

Given a proposed task, compares it against the current skill catalog in `.claude/skills/`
and recommends exactly one disposition: USE EXISTING, USE WITH PARAMETERS, EXTEND
EXISTING, COMBINE EXISTING SKILLS, CREATE NEW, or ESCALATE.

This skill is **read-only and chat-only**. It never creates, edits, renames, moves, or
deletes anything, and never acts on its own recommendation — building, extending, or
combining skills always requires a separate, explicit follow-up request.

## Input

`$ARGUMENTS` is the proposed task description.

If `$ARGUMENTS` is missing or too vague to compare against the catalog, ask exactly one
focused clarifying question before proceeding (e.g. "What should this task do, and what
would trigger it?"). Ask this directly as free text — a proposed task description has no
finite menu of good answers, so it's exempt from the clickable-question convention in
`skill-builder/reference.md`.

## Step-by-Step Workflow

1. **Validate the input.** If `$ARGUMENTS` is missing or too vague, ask exactly one
   focused clarifying question, then proceed using the answer.

2. **Discover and shortlist.** Glob `.claude/skills/*/SKILL.md`. Read only the
   frontmatter (`name`, `description`, `argument-hint`) of each discovered skill.
   Shortlist any skill whose frontmatter plausibly overlaps the proposed task — by
   function, synonym, or expected input/output, not just exact wording.

3. **Sanity-check against CLAUDE.md.** If CLAUDE.md exists and contains a skill
   inventory table, cross-reference it against what Step 2 actually found on disk. If
   CLAUDE.md and `.claude/skills/` disagree (a skill documented but missing, or present
   but undocumented), report the drift and trust the actual `SKILL.md` files as source
   of truth — do not silently pick one.

4. **Deep-read the shortlist.** Read the full `SKILL.md` content only for the
   shortlisted plausible matches — not every skill in the catalog.

5. **Compare.** For each shortlisted skill, compare its actual scope, inputs, workflow,
   outputs, parameters, and guardrails against the proposed task. Note the matched
   capability and the important gap, if any.

6. **Assign exactly one disposition**, using this priority order (highest first — stop
   at the first one that applies):
   1. **USE EXISTING** — a shortlisted skill is a complete match; no changes needed.
   2. **USE WITH PARAMETERS** — a shortlisted skill fully covers the task once given
      different arguments/input; no content change needed.
   3. **COMBINE EXISTING SKILLS** — two or more shortlisted skills, used together
      unmodified, collectively cover the complete workflow.
   4. **EXTEND EXISTING** — a shortlisted skill must be changed (new steps, fields, or
      capability) to cover the task.
   5. **CREATE NEW** — no existing skill, combination, or reasonable extension
      adequately covers the task.
   6. **ESCALATE** — evidence is insufficient or contradictory, or the decision
      requires a human call on permissions, ownership, risk, or scope.

7. **Report.** Present the findings and disposition in chat only. Never write a file.

## Output Format

```
# Skill Fit Report: [task description]

## Understood Task
[one-line restatement of the proposed task]

## Shortlisted Candidates
| Skill | SKILL.md path | Why shortlisted |
|---|---|---|
| ... | ... | ... |

## Comparison
| Candidate skill | Relevant SKILL.md path | Matched capability | Important gap |
|---|---|---|---|
| ... | ... | ... | ... |

## Catalog Drift
[mismatch between CLAUDE.md's skill inventory and .claude/skills/, or "None found"]

## Disposition: [USE EXISTING / USE WITH PARAMETERS / COMBINE EXISTING SKILLS / EXTEND EXISTING / CREATE NEW / ESCALATE]
[evidence-based justification, 2-4 sentences, citing the specific skill(s) and the
match/gap that drove the decision]
```

## Notes

- Read-only and chat-only: never creates, edits, renames, moves, or deletes anything
  under `.claude/skills/`; never modifies CLAUDE.md; never saves the report to a file.
- Does not scan `output/` folders — those hold results, not reusable skill definitions.
- Never acts on its own recommendation. Building, extending, or combining skills always
  requires a separate, explicit follow-up request (e.g. via `skill-builder`).
- Shortlist by frontmatter first; only read full `SKILL.md` content for plausible
  matches — don't read the entire catalog in full on every run.
- Apply the disposition priority order strictly, top to bottom, to keep
  recommendations consistent across runs.
- Runs directly in the main conversation (no subagent fork) since Step 1 may need to
  pause and ask the user a clarifying question before continuing.
- Clickable-question convention: this skill has exactly one user-facing question (the
  Step 1 clarifying question), and it's genuine free text with no finite set of good
  answers, so no `AskUserQuestion` conversion applies here.
