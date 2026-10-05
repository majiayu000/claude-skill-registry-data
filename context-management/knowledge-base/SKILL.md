---
name: knowledge-base
description: "Create, organize, audit, or maintain a durable Markdown knowledge base with an index, atomic notes, stable identifiers, links, tags, and maintenance checks. Use for a personal or team knowledge base, research vault, documentation library, MOC, note organization, broken links, or knowledge-base cleanup; do not confuse it with short-term agent memory. Turkish triggers: bilgi tabanı kur, belgeleri düzenle, indeks ve bağlantılar, tekrar kullanılabilir bilgi."
---

# Knowledge Base

Build a user-owned, navigable knowledge system. `k-mem` handles recurring working context; this skill handles durable documents and notes the user can inspect and own.

## Start safely

Ask for the intended root folder and allowed sources. Do not scan the whole disk, unrelated projects, mail, or cloud services. Preserve existing structure unless a migration is explicitly requested.

## Structure

1. Create or repair a concise `INDEX.md` with entry points, scope, and maintenance date.
2. Keep notes atomic: one durable concept, decision, procedure, or source synthesis per note.
3. Use stable, human-readable IDs or slugs. Avoid timestamp-only names when notes will be referenced later.
4. Record source/provenance, confidence, and update date for claims that can become stale.
5. Link notes with a brief relationship reason; use a controlled tag vocabulary rather than uncontrolled tag sprawl.
6. Use topic maps/MOCs only where navigation improves retrieval.

## Maintenance pass

Check for broken links, duplicate notes, orphan notes, stale indexes, empty tags, and claims that need source review. Propose changes before mass moves, renames, or deletions.

## Guardrails

- Do not persist hidden user profiles or personal data without clear consent.
- Never claim that note links prove truth; preserve uncertainty and source context.
- Keep imports reversible and provide a migration map for any structural change.
