---
name: filament-panel-review
description: >
  Review one or more of the 7 Filament 5 panels in ndestates-io multi-panel architecture using the local cache first.
  Use for panel audits, resource reviews, widget checks, cross-panel reuse, or before changes to providers/resources.
argument-hint: "Panel name or scope, e.g. 'admin', 'sales', 'lettings', 'all panels', 'user + block-manager'"
user-invocable: true
disable-model-invocation: false
---

# Filament Panel Review (Cache-First)

**Always start by loading the cache** (use `.github/prompts/load-project-cache-first.prompt.md` or explicit reads of STRUCTURE/ARCHITECTURE/CONCERNS).

## Required First Reads from Cache
1. `docs/codebase/STRUCTURE.md` — Panel table and provider locations (Admin, User, BlockManager, Lettings, LettingsManager, Sales, Database).
2. `docs/codebase/ARCHITECTURE.md` — Multi-panel architecture + cross-panel reuse notes.
3. `docs/codebase/CONCERNS.md` — Any open panel-related items.
4. `.copilot/memories/INDEX.md` + relevant repo memories.

## Then Read the Specific Panel Provider(s) (targeted)
- Admin: app/Providers/Filament/AdminPanelProvider.php
- User, BlockManager, Lettings, LettingsManager, Sales, Database panels similarly.
- Common resources (Property, etc.) and policies.

## Review Checklist (cite cache file + line)
- Panel registration and middleware
- Resource discovery / explicit registration
- Widget composition (dashboards)
- Navigation groups/icons
- Cross-panel resource reuse (e.g. Property model across panels)
- Custom theme, render hooks, policies/authorization
- Observers/services backing the panel

After review, return structured summary:
- Panel purpose (1 sentence)
- Resource count and notable resources
- Deviations from CONVENTIONS.md
- Recommendations

Cite specific cache files. Follow DDEV and security rules from copilot-instructions. Use `.github/prompts/load-project-cache-first.prompt.md` first.

Source: `.github/prompts.github/prompts/filament-panel-review.prompt.md.md` (full content embedded here + in prompts dir)
