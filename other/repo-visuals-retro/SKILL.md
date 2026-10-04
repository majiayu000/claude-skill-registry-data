---
name: repo-visuals-retro
description: Retrospective meta-skill for the `repo-visuals` skill. Reads accumulated evaluation logs from past runs, spots patterns (recurring low-score criteria, repeated iteration failures, unsatisfied requests), consults other expert skills (skill-creator, frontend-design, etc.) where relevant, and proposes concrete edits to `repo-visuals/SKILL.md` as a reviewable diff. Runs on-demand, not per run.
---

# repo-visuals-retro

The `repo-visuals` skill scores every run on five criteria (see `repo-visuals/SKILL.md` §6). This meta-skill turns that accumulated evidence into skill improvements.

## When to invoke

- You have ≥ 5 runs logged in `./evaluations/runs/` in the user's working directory (before that, the sample is noise).
- Something feels off across multiple runs and you want a structured look.
- A major change to `repo-visuals` is planned and you want the evidence base first.

Do **not** run this every session. Retros are more valuable with accumulated samples.

## Inputs

- The `repo-visuals` skill's `SKILL.md` — the current skill definition (sibling skill in the same plugin)
- `./evaluations/index.md` in the user's working directory — curated aggregate from previous retros
- `./evaluations/runs/*.md` in the user's working directory — all per-run raw evaluations since the last retro
- Available expert skills in the environment (detected, not assumed)

## Workflow

### 1. Read & tabulate

Read all inputs. Build a small table:

- Average score per criterion, overall and by repo-type bucket (CLI, library, web-app, etc. — infer from scan metadata in each run)
- Variance per criterion (high variance = the skill is inconsistent on that axis)
- Free-text feedback clustered by theme

### 2. Identify patterns

Name each pattern concretely:

- "Hero moment delivery averaged 2.6 / 5 across the 4 CLI-tool runs but 4.2 / 5 across library runs"
- "Technical polish dropped whenever the stage was < 400 px tall — type legibility likely"
- "3 runs had identical user feedback: 'loop seam is jarring'"

### 3. Consult expert skills

For each pattern, consult the relevant expert skill(s) if available in the environment. Examples:

- **Visual / design critique** → `frontend-design` skill. Feed it the final HTML + screenshots from low-scoring runs; ask for specific design-rule violations.
- **Skill structure / prompt design** → `skill-creator` skill. Ask whether the skill's Phase N language is ambiguous or missing a step.
- **Evaluation methodology** → any `evaluate-plugins` style skill. Ask whether the 5-criterion scorecard is well-calibrated.
- **Domain-specific knowledge** → e.g. an ast-graph / codebase-compare skill if patterns suggest weaknesses in the scan phase.

Detect which skills are actually available — don't reference non-existent ones.

### 4. Propose edits

Write a diff-style proposal: for each pattern, which section of the `repo-visuals` skill's `SKILL.md` changes and why. Example:

```
Pattern: Hero moment delivery weak on CLI tools (2.6/5 avg over 4 runs).
Hypothesis: §1.4a probes don't surface CLI-specific hero moments
            (install speed, clear command output, shell ergonomics).
Proposed edit to §1.4a: add a CLI-tool branch to the probing list with
            3 tool-specific prompts.
```

Show the proposed diff. Wait for user approval before applying.

### 5. Apply & update aggregate

On user approval:

- Edit the `repo-visuals` skill's `SKILL.md` with the approved changes
- Append a retro summary to `./evaluations/index.md` (date, patterns identified, edits applied)
- Move the raw run files that informed this retro into `./evaluations/runs/processed/` so the next retro only sees new samples

## Outputs

- Updated `repo-visuals` skill `SKILL.md`
- Updated `./evaluations/index.md` with retro summary
- Moved processed run files

## What this skill does NOT do

- Does not run `repo-visuals` itself
- Does not auto-apply edits without user approval
- Does not invent criteria — it only improves the skill against its existing scorecard
