---
name: audit-skill
description: >
  Score a single skill against the gardener rubric. Reads the skill's SKILL.md,
  references/, and templates/, then writes a 7-dimension scorecard with per-criterion
  rationales and a recommended-actions list. Isolated counterpart to /gardener:
  same rubric, one item at a time. Use when the user asks to audit a skill, score
  a skill, check if a skill is healthy, or wants to re-score after making changes.
arguments:
  - name: skill
    description: Path to the skill directory (e.g., skills/research) or skill name.
    required: true
context: fork
user_facing: true
---

## Contents

| Reference                            | When to load                |
| ------------------------------------ | --------------------------- |
| `../../references/rubric.md`         | The scoring rubric (shared) |
| `../../references/write-protocol.md` | Write discipline            |
| `templates/scorecard-skeleton.md`    | Output file shape           |

# Audit a skill

Score one skill against the 7-dimension rubric. The skill is the input; a scorecard Markdown file is the output.

## How it works

1. Resolve `{{ skill }}` to an absolute path. Accept either a directory path (`skills/research`) or a bare skill name (`research`) — glob for the matching `SKILL.md`.
2. Read the rubric at `${CLAUDE_PLUGIN_ROOT}/references/rubric.md`.
3. **Read the skill in full**: SKILL.md, every file under `references/`, every file under `templates/`. The scorecard is grounded in what's in the files, not in the description alone. Reading is the primary work.
4. If a prior `/gardener` audit exists at `plugin-gardener/audit/`, read its latest `collisions.csv` and `clusters.csv` for cross-reference context. Collisions involving this skill inform Dimension 1 (description quality) and Dimension 5 (proactive-label discipline) — check whether the description carries the right negative-keyword discriminators. For every collision row, open the sibling SKILL.md and verify by reading, not from the cosine alone.
5. Write a scorecard to `plugin-gardener/audit/ad-hoc/<skill-name>-<YYYY-MM-DD>.md` using `templates/scorecard-skeleton.md`.
6. Present the total, dimension scores, and top-3 recommended actions inline.

Apply the rubric dimension by dimension. Record a short rationale (1–2 sentences with a file:line citation from the files you read) for every criterion scoring under 3 points. The rationale is the value; the number is the aggregate.

**On the role of embedding data**: collisions and clusters from a prior `/gardener` run are binoculars, not the photograph. They point you at the right cross-references to open. Verify every flagged collision by reading both SKILL.md files — a high cosine is an invitation to investigate, not a verdict.

## When to invoke

- After authoring a new skill — baseline the score before committing.
- After a monthly `/gardener` run flags a skill — re-score to confirm the issue.
- After applying fixes — did the score improve?

## What this does not do

- Edit the skill.
- Open a PR.
- Change frontmatter.

The scorecard is the deliverable. Changes are the user's to apply.
