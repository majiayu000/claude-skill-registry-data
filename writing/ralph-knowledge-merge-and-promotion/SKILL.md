---
name: ralph-knowledge-merge-and-promotion
description: Ralph-v2 knowledge extraction, staging, merge, and promotion reference. Use when running Librarian EXTRACT, STAGE, or PROMOTE modes, applying merge rules, writing extracted frontmatter, or promoting staged knowledge into `.docs`.
---

# Ralph Knowledge Merge And Promotion

This skill contains the deterministic parts of Ralph-v2's knowledge pipeline.

## Pipeline Tiers

- Iteration scope: `iterations/<N>/knowledge/`
- Session scope: `knowledge/`
- Workspace scope: `.docs/`

## Preflight Gates

| Gate | Mode | Creates If Missing |
|------|------|--------------------|
| 0 | EXTRACT | `iterations/<N>/knowledge/` + Diátaxis subdirs |
| 1 | STAGE | `knowledge/` + Diátaxis subdirs |
| 2 | PROMOTE | `.docs/` + Diátaxis subdirs |

If auto-creation or validation fails, return `blocked`.

## Extracted File Frontmatter

```yaml
---
category: tutorials | how-to | reference | explanation
source_session: <SESSION_ID>
source_iteration: <N>
source_artifacts:
  - iterations/<N>/tasks/task-3.md
extracted_at: <ISO8601>
staged: false
staged_at: null
promoted: false
promoted_at: null
---
```

## Merge Algorithm

| Case | Condition | Action |
|------|-----------|--------|
| New file | No matching filename in target | Copy directly |
| Source newer | Source timestamp greater than target | Overwrite target |
| Target newer | Target timestamp greater than source | Skip |
| Content overlap | Same category and >50% H2/H3 heading overlap | Append unique sections |
| Contradictory content | Same heading, different body | Newer content wins |

## EXTRACT Checklist

1. Poll signals.
2. Initialize `## Knowledge Progress` if missing.
3. Run Gate 0.
4. Collect evidence from tasks, reports, plan, and review artifacts.
5. Re-poll signals.
6. Filter to reusable knowledge only.
7. Classify into exactly one Diátaxis category.
8. Write iteration knowledge files with traceability frontmatter.
9. Update `iterations/<N>/knowledge/index.md`.
10. Update knowledge progress.

## STAGE Checklist

1. Poll signals.
2. Run Gate 1.
3. Resolve source iterations.
4. Inventory current session knowledge.
5. Merge selected iteration knowledge into session knowledge.
6. Mark source entries as staged.
7. Update `knowledge/index.md`.
8. Update `plan-knowledge-staging`.

## PROMOTE Checklist

1. Poll signals.
2. Initialize knowledge progress section if needed.
3. Respect `INFO + target: Librarian + SKIP_PROMOTION:`.
4. Run Gate 2.
5. Read staged, unpromoted knowledge files.
6. Re-poll signals.
7. Merge into `.docs/`.
8. Strip staging-only frontmatter and normalize content.
9. Apply `diataxis-categorizer` for sub-category resolution.
10. Mark entries promoted.
11. Update `knowledge/index.md` and `.docs/index.md`.