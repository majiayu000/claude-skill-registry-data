---
name: ia-nav-adr
description: Use when changing information architecture, section placement, navigation YAML, slugs, URLs, page identity, /ops rules, ADRs, or contribution rules.
---

# IA, Nav, And ADR

## Read First

- `/ops/ia.md`
- `/ops/requirements.md`
- Relevant existing ADRs under `/ops/adr/`
- `src/_data/nav.ja.yml` and matching locale nav files when localization is in scope.

## Rules

- `/ops` is the source of truth.
- Slugs, `navId`, and public URLs are stable IDs.
- Renames need owner approval, nav updates, redirect consideration, and ADR coverage.
- Do not add EN/ZH nav entries unless matching localized pages are part of the requested task.
- Parent grouping changes and sidebar order changes are IA changes.

## Workflow

1. Update `/ops` or add an ADR before implementation.
2. Update nav YAML only for the requested locales.
3. Add or move content files only after IA is documented.
4. Validate nav and content integrity.

## Checks

- `npm run check:content`
- `npm run build`
- `npm run test:playwright` for sidebar, search, language switch, previous/next, or notes changes.

## Naming

An **asset prefix** is always singular, because it modifies the rest of the name and English uses the singular in attributive position — `loop_simple.png`, never `loops_simple.png`.

A **slug or navId** follows the subject instead: singular for a page about one mechanism (`queue`, `list`, `batch-video`, `loop`), plural for a page enumerating many items (`data-types`, `text-ops`, `wildcards`). Check the siblings before choosing.

A **display title or nav label** is not attributive either, and may be plural where that is the natural English even when the slug is singular — `loop` and `Loops`.

An ADR records the decision as it shipped. If the scope changes while the work is in progress — localization was requested halfway, placement moved — update the ADR before the PR, or it documents a plan nobody followed.

## Pipeline

Part of the article pipeline in [article-authoring](../article-authoring/SKILL.md), alongside [workflow-json](../workflow-json/SKILL.md).

Nav and slug changes do not reach a running dev server — restart it, see [preview-site](../preview-site/SKILL.md).
