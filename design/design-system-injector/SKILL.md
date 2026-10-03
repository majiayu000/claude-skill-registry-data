---
name: design-system-injector
description: Phase 5 part of disease-market-sizing-orchestration. Injects consulting palette (navy/gold/blue) + base CSS + floating TOC + section dividers into raw report HTML. Validates token coverage ≥60% (warn) and floating TOC li ≥5 (block). Use AFTER content-verification passes, BEFORE report-bundle-builder build_all_deliverables.
license: Cite-or-Block strict (P0 iron law, see ../../CLAUDE.md)
---

# Design System Injector (Phase 5 part)

## Functions

- `inject(html, tokens) -> str` — insert :root tokens + base CSS + floating TOC button + overlay
- `validate_design(html) -> DesignReport` — compute coverage + TOC li count

## Validation Thresholds

- `token_coverage ≥ 0.60` → ok; otherwise warn (not block)
- `toc_li_count ≥ 5` → ok; otherwise BLOCK (B3 守门)

## P0 Watchdog

Skill scripts contain 0 hardcoded disease/drug names — CI block on hit.
