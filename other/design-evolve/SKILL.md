---
name: design-evolve
description: Use when integrating supplied discussions or decisions into a self-contained next version of existing design documents.
---

# Design Evolve

Integrate authorized decisions into a complete next version of design documents,
preserving source precision and invariants. Integration does not authorize redesign.

1. Resolve source version, target identifier/path and included discussion files
   from the request. Use supplied paths without reconfirmation; ask only about
   missing material scope or whether existing target content may be overwritten.
2. Inventory source core and discussions. Group changes by concept and identify
   authoritative decisions versus proposals, scratchpads and unresolved conflicts.
   Read incrementally; delegate bounded independent reads only when beneficial.
3. For each concept, read the actual discussion and affected core sections before
   editing. A summary guides navigation but is not sufficient evidence for a
   consequential change. Record source → target section → intended change.
4. Start each target document from its complete source. Integrate only supported
   decisions; preserve exact identifiers, numbers, error behavior and invariants
   unless explicitly superseded. Keep ambiguous choices unresolved and continue
   independent integrations while asking about material conflicts.
5. Update version headers, filenames and internal references. Copy untouched core
   files too. The target must stand alone; prior-version references belong only
   in history/provenance, not as a substitute for current design content.
6. Check cross-document consistency, section links, invariant coverage and stale
   version references. Consolidate routine duplication while preserving distinct
   context; ask only when consolidation would change meaning or authority.

Use `references/integration.md` for large-set mechanics and an optional handoff
shape. No file-size threshold or per-file agent quota applies. Report integrated
concepts, files, decisions and deferred items with source pointers. Do not label
unresolved scratchpad proposals as approved design.
