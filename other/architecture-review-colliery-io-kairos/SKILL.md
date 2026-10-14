---
name: architecture-review
description: Review the codebase's architecture — scan, classify by altitude, present deepening candidates as an HTML report, then grill through the one you pick.
disable-model-invocation: true
---

# Architecture Review

[The architecture-review reference](../../../references/architecture-review.md) is the single source of truth for this review — vocabulary, heuristics, checklists, finding format, strength calibration, and reviewer anti-patterns live there and nowhere else. Read it end to end before touching the codebase and apply it verbatim; this file only sequences the work and its presentation.

## 1. Load the contracts

- The reference, in full.
- The ADRs: `search` filtered to ADRs (scoped to the area under review), then `get_item` on each hit for full content. The reference's system-level ADR checks (A2-6..A2-8) and its re-litigation rules cannot be applied without them.

## 2. Scan

Run the reference's Section 1 scan pass over both altitudes. Use the Agent tool with `subagent_type=Explore` to walk the codebase and inventory the Section 2 modules and the Section 3 containers, C4 views included. Complete when every module and container is inventoried with a path.

## 3. Classify

Work the inventory through the reference's Section 1 classify pass and the Section 2.3 / 3.3 checklists. Complete when each checklist has been answered for everything inventoried at its altitude.

## 4. Report

Draft every finding in the reference's Section 4 format, then self-check the whole set against Section 5 before the user sees anything.

Present the findings as a self-contained HTML report — [HTML-REPORT.md](HTML-REPORT.md) has the scaffold, card layout, diagram patterns, and styling. Write it to the OS temp directory (resolve `$TMPDIR`, fall back to `/tmp`; `%TEMP%` on Windows) as `architecture-review-<timestamp>.html` so nothing lands in the repo, open it for the user (`open` on macOS, `xdg-open` on Linux, `start` on Windows), and tell them the absolute path.

Do not propose interfaces yet. Ask: "Which of these would you like to explore?"

## 5. Grilling loop

When the user picks a candidate, invoke the `grilling` skill and walk its design tree — constraints, dependencies, the shape of the deepened module, what sits behind the seam, which tests survive. The reference's design-it-twice rule binds any interface that crystallizes here.

If the user rejects a candidate for a load-bearing reason, offer to record it — `create_item` with `item_type: adr` — framed as: "Want me to record this as an ADR so future architecture reviews don't re-suggest it?" Skip ephemeral reasons ("not worth it right now") and self-evident ones.
