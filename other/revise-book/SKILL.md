---
name: revise-book
description: Revise a completed or partial book at manuscript, arc, chapter, scene, continuity, and prose levels while preserving chapter IDs and updating dependent plans when structure changes.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Revise Book

## Workflow

1. Read core contract, style rules, story craft, book plan, canon, chapter state, and the manuscript range in scope.
2. Diagnose in layers: whole-book causality, character and subplot arcs, chapter necessity and order, scene turns, continuity, then prose.
3. Fix the highest causal layer first. If chapter order or purpose changes, patch `book_plan.md` before line editing downstream chapters.
4. Keep stable `CH-###` IDs when moving chapters. Add new IDs for genuinely new chapters instead of renumbering the book.
5. Rebuild `chapter_state.json` for any affected range.
6. Run continuity and style checks after the structural pass and again after prose edits.

7. Apply the `project-impact` procedure after accepted chapter or structural changes and mark affected downstream artifacts stale.

## Done

Every accepted revision note is resolved, chapter plan and manuscript agree, and chapter state can be regenerated from the revised text without contradiction.
