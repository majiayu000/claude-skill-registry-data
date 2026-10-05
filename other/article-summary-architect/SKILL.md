---
name: article-summary-architect
description: >-
  Create high-quality bilingual `detailed_summary` for StaticFlow articles.
  Focus on evidence, reader value, and clear structure while leaving room
  for flexible writing style and reasoning.
---

# Article Summary Architect

Produce concise, trustworthy, reader-friendly `detailed_summary` (`zh` / `en`).

## When To Use
Use this skill when the user asks to:
1. Add or rewrite `detailed_summary`.
2. Improve summary clarity, structure, or relevance.
3. Fix low-quality/generic/misaligned bilingual summaries.
4. Keep style consistent without forcing one rigid template.

## Design Philosophy
- Principle-first, not template-first.
- Evidence-first: every important claim should be grounded in the article.
- Reader-first: a reader should quickly know what the article delivers.
- Flexible expression: structure is required, wording and section naming are free.

## Load Context
- Required: `references/quality-checklist.md`
- Recommended: `references/summary-templates.md`, `references/type-taxonomy.md`
- If publishing immediately after summary: `../staticflow-cli-publisher/SKILL.md`

## Core Workflow (Flexible, Mandatory)

### Step 1: Understand the article before writing
Quickly extract:
1. What problem/question is being addressed?
2. What conclusion or takeaway matters most?
3. Why should readers trust this conclusion?
4. What boundaries, risks, or assumptions matter?

Type/lens selection is optional and internal. Use it only to organize thinking, not to constrain expression.

### Step 2: Decide what must survive compression
Keep only high-value information:
- Problem and context
- Core mechanism/argument path
- Actionable conclusion or decision guidance
- Validation/boundary notes (when present)

Remove low-value repetition and decorative language.

### Step 3: Draft bilingual summary with natural structure
- Start with one natural opening sentence (reader-facing, not schema labels).
- Prefer sectioned structure with concise bullets for scanability.
- Section count and bullet count are flexible; choose what best fits article complexity.
- Keep `zh` and `en` semantically aligned, but allow natural language differences.

### Step 4: Quality pass before finalize
Validate against `references/quality-checklist.md`.
If evidence is insufficient for a claim, reduce confidence or state uncertainty explicitly.

## Output Contract
Return frontmatter-ready content:

```yaml
detailed_summary:
  zh: |
    这是一篇……
    ### ...
    - ...
  en: |
    This is a ...
    ### ...
    - ...
```

Output expectations:
1. Keep markdown render-safe.
2. Keep summary specific to this article (avoid generic filler).
3. Keep bilingual meaning aligned.
4. Prefer structured sections over a long undivided block.

## Freedom and Boundaries
- Freedom:
  - You may choose your own section names, ordering, and emphasis.
  - You may adapt style for technical and non-technical content.
- Boundaries:
  - No fabricated facts/metrics.
  - No forcing technical framing onto non-technical posts.
  - No noisy schema exposition (for example rigid type labels) unless user asks.

## Integration with Publisher
When used before publication:
1. Generate or refresh `detailed_summary.zh/en` first.
2. Hand off to `staticflow-cli-publisher` for write/sync.
3. Report whether summary was regenerated and whether quality checks passed.
