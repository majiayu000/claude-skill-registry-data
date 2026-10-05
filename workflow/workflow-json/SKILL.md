---
name: workflow-json
description: Use when adding, replacing, validating, or linking ComfyUI workflow JSON files under src/workflows, including article workflow references and reproducibility checks.
---

# Workflow JSON

## Rules

- Workflow JSON files live under `src/workflows/<section-or-type>/<slug>/`.
- Keep workflow files reproducible enough for a third party to load and understand the documented result.
- Do not edit unrelated workflow JSONs.
- Remove Windows `Zone.Identifier` sidecar files if they appear in the worktree.
- Keep article links and workflow file paths in sync.

## Workflow

1. Identify the owning article slug and section.
2. Place JSON files in the matching workflow folder.
3. Validate changed JSON files before build.
4. Check all article links to the workflow files.
5. If workflow behavior changes the article claim, update the article text too.

## Checks

- `npm run check:workflows`
- `npm run check:content`
- `npm run build`

For a single file during iteration:

```bash
node -e "JSON.parse(require('node:fs').readFileSync(process.argv[1], 'utf8'))" path/to/workflow.json
```

## Pipeline

Part of the article pipeline in [article-authoring](../article-authoring/SKILL.md), alongside [ia-nav-adr](../ia-nav-adr/SKILL.md) when placement or slug changes.

File naming follows `/ops/style-writing.md` section 08 — the same rule as media originals. Check sibling folders before inventing a spelling.

Check the result on localhost with [preview-site](../preview-site/SKILL.md) before [release-check](../release-check/SKILL.md).
