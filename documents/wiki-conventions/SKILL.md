---
name: doc-guide
description: Use before editing, adding, or reconciling any wiki page under docs/wiki/. Trigger when the agent mentions "editing a wiki page", "adding a wiki entry", "wiki conventions", "docs/wiki", "wiki frontmatter", "wiki link rule", "reconciling wiki", "wiki status conflict", or is about to Write/Edit a file under docs/wiki/.
version: 0.1.0
---

# Wiki Conventions

Authoritative rules every wiki edit MUST satisfy. Full schema lives in `docs/wiki/schema.md` — consult it for field semantics, allowed enums, and page taxonomy.

## 1. Required YAML Frontmatter

Every page under `docs/wiki/` starts with:

```yaml
---
type: concept            # one of: concept | entity | flow | decision | glossary
raw_sources:             # files this page was distilled from (relative paths)
  - src/app/(dashboard)/orders/page.tsx
  - prisma/schema.prisma
related:                 # other wiki pages, relative markdown links
  - ../entities/order.md
  - ../flows/checkout.md
last_reconciled: 2026-04-17   # ISO date of the last time sources were re-checked
status: stable           # one of: draft | stable | stale | conflict
---
```

Missing or malformed frontmatter = reject the edit. See `docs/wiki/schema.md` for the full field spec.

## 2. Link Rule

- Links between wiki pages MUST be **relative markdown** (`../flows/checkout.md`), never absolute, never bare slugs.
- Links are **bidirectional**: if page A lists B in `related`, page B MUST list A in its `related`. Before saving, open the other side and add the back-link.

## 3. New Page vs Update

Update an existing page when:
- The topic already has a page (search `docs/wiki/` by title and by `raw_sources` overlap).
- Your change is a refinement, correction, or added nuance to the same concept.

Create a new page when:
- No existing page covers the concept, entity, flow, decision, or term.
- The scope is cleanly separable (would need its own `related` fan-out).

When in doubt: update. Small pages sprawl.

## 4. Contradiction Handling

NEVER silently overwrite existing content. If new information contradicts what is on the page:

1. Keep the existing claim intact.
2. Append a section:

```markdown
## ⚠ Conflict

- **Existing claim**: <quote from page>, sourced from <file>.
- **New claim**: <your finding>, sourced from <file>.
- **Observed**: <ISO date>
- **Needs human review.**
```

3. Set frontmatter `status: conflict` and update `last_reconciled`.

## 5. Forbidden Writes

Wiki agents edit ONLY files under `docs/wiki/`. Do NOT modify:

- `src/**` — application code
- `prisma/**` — schema and migrations
- `docs/eis/**` — executable implementation specs
- `docs/reference/**` — reference material
- Top-level `docs/*.md` — curated root docs

These are **raw sources**. The wiki distills them; it does not mutate them.

## 6. Full Spec

For full spec, read `docs/wiki/schema.md`.
