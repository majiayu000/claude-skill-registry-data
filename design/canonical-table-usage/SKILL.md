---
name: canonical-table-usage
type: Skill
title: Canonical table usage
description: "Approved table usage rules. Use when configuring, migrating, or reviewing MatrxDataTable columns, toolbars, or pagination."
tags: [tables, ui]
timestamp: 2026-09-17
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/canonical-table-usage/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# Canonical table usage

1. Dense tables keep independently meaningful values in separate columns; do not stack unrelated fields to save width.
2. Every value users need to sort or filter must have its own column and accessor, even if initially hidden.
3. Deliberately combined cells must keep each intended line unwrapped, truncate overflow, and expose full values through canonical tooltips or detail controls.
4. Use the canonical title, toolbar and footer. Do not add duplicate title/count rows or pagination footers.
5. New and converted tables use the shared `MatrxDataTable` with adjustable desktop columns enabled by default. Do not disable `resizableColumns` or a column's `resizable` flag without recording the specific purpose and decision-maker. A legacy grid does not inherit this default; migrate it or explicitly track that capability gap.
6. Before converting a hand-built table, screenshot it in place and apply [canonicalize without destroying](../../policies/no-dead-ends.md): if the converted table is visibly worse in its spot (a box inside a box, lost counts or columns, added chrome), the hand-built design is adopted into the table package as an option or new primitive, never replaced by the default. A table inside a card, section or panel never adds its own frame inside the host's frame.
