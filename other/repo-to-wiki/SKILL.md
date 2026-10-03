---
name: repo-to-wiki
description: >
  Build a local markdown wiki for a repo, research folder, or cloned source
  collection. Use when the user wants living docs, repo explainers, source
  synthesis, citations, cross-links, or llmwiki-style knowledge accumulation.
---

# Repo To Wiki

Turn source files into stable markdown pages that future Codex sessions can
read instead of rediscovering the project.

## Folder Shape

```text
wiki/
  overview.md
  architecture.md
  setup.md
  concepts/
  decisions/
  sources.md
```

## Build Order

1. Create `wiki/sources.md` with repo URLs, local paths, commit/date if known.
2. Create `wiki/overview.md` from README and manifests.
3. Create `wiki/architecture.md` from entry points and module layout.
4. Create focused concept pages only when they remove repeated context.
5. Cross-link pages with relative markdown links.

## Page Contract

Each page should include:

- purpose
- evidence/source files
- current understanding
- open questions
- last reviewed date

## Rules

- Source files remain the source of truth.
- Keep wiki pages concise and updateable.
- Do not invent details when source evidence is thin.
- Use exact file links or paths for traceability.

Reference pattern source: `sources/llmwiki`.

## Skip When

- The user only needs a short one-time repo summary.
- Source evidence is too thin to maintain living docs.

## Validation

- Wiki pages cite source files or URLs and last-reviewed dates.
- Broad examples stay in concept/reference pages, not the overview.
- Open questions are preserved instead of inventing missing architecture.
