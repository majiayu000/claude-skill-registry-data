---
name: pages
description: "MythiStone page generation: generate*.py, Jinja templates and macros, shared generator modules (pageGeneration, commonUtils, aggregateData, compArchetypes) and page-specific data rules for spec, item, dungeon, comps, analyzer, tierlist, routes, trends. Use when changing what a page renders."
---

# Pages domain

## Gotchas

Before changing a file listed below, read its gotcha: `ref/<id>.md` in this skill (or `kb_gotcha <id>`).

| id | rule | files |
|---|---|---|
| `analyzer-page` | The analyzer's talent tree is assembled from two artifacts built by two different workflows and decoded by two hand-kept copies of the loadout decoder | `assets/js/analyzer.js`, `assets/js/loadout-view.js`, `backend_scripts/generateAnalyzerPage.py`, `assets/css/analyzer.css`, `templates/analyzer.html` |
| `build-new-page` | How to scaffold a NEW static page so its markup, includes, and asset wiring match existing pages | `backend_scripts/pageGeneration.py`, `templates/base_template.html`, `templates/header_imports.html`, `templates/javascript_imports.html` |
| `dungeon-npc-portrait-icons` | Which creature-image sources work for the dungeon page NPC portraits and which were tried and rejected, plus the order and the deploy path the icons depend on | `backend_scripts/fetchNpcIcons.py`, `backend_scripts/generateDungeonPages.py`, `.github/workflows/buildPages.yml` |
| `enchant-link-icon-rune-fallback` | Every enchant link/icon render surface must fall back to spellId/spellIcon because DK weapon runes have no scroll itemId | `templates/spec_page.html`, `templates/item.html` |
| `enchant-lookup-filter` | Which enchants a spec or item page shows is decided by one shared predicate, an offline expansion id and a 14-day denominator, and a missing enchant is usually deliberate | `backend_scripts/generateSpecPages.py`, `backend_scripts/generateItemPages.py`, `backend_scripts/commonUtils.py` |
| `frontend-json-dungeon-keys` | The in-memory frontend_json keys each comp's dungeons map by INT, but on-disk comps_index.json keys them by STR, so per-dungeon lookups must handle both | `backend_scripts/compArchetypes.py`, `backend_scripts/generateCompPage.py` |
| `item-quality-from-bonus` | Item quality/color (rarity) is resolved from the item's bonus ids, not the base item quality, on both the spec page and the items page, through one shared commonUtils helper | `backend_scripts/generateSpecPages.py`, `backend_scripts/generateItemPages.py`, `backend_scripts/commonUtils.py`, `templates/item.html`, `assets/js/items.js` |
| `item-source-filters` | Where an item drops is joined through Blizzard journal ids and travels to the items page as source tokens that Python writes and JS parses | `backend_scripts/generateItemPages.py`, `backend_scripts/generateDungeonPages.py`, `backend_scripts/pageGeneration.py`, `assets/js/items.js`, `backend_scripts/fetchRaidData.py`, `backend_scripts/fetchDungeonData.py` |
| `page-data-and-scripts` | Page JS and CSS live in assets/js/<page>.js and assets/css/<page>.css, never inline in templates, and server data reaches the script either as a fetched JSON file or an inline application/json block depending on how the page consumes it | `assets/js/dashboard.js`, `assets/js/comps.js`, `backend_scripts/generateDashboardPage.py`, `backend_scripts/generateCompPage.py` |
| `route-accordion-macro` | The keystone.guru route accordion item is one shared Jinja macro used by the spec, routes and dungeon pages, and assets/js/routes-finder.js must mirror its full markup | `templates/_route_macros.html`, `templates/spec_page.html`, `templates/find_routes.html`, `templates/dungeon_page.html`, `assets/js/routes-finder.js` |
| `spec-team-comps` | The comps page Details modal shows family totals that compArchetypes emits and comps.js assembles, and the archetype ranking rules live in the compArchetypes docstrings | `backend_scripts/compArchetypes.py`, `backend_scripts/generateSpecPages.py`, `assets/js/comps.js`, `templates/_team_comp_macros.html`, `templates/comps.html` |
| `tierlist-gear-modal` | The sim tierlist's gear sets and its gear modal span two generators, three CI jobs and catalogs baked by other pages | `assets/js/tierlist-modal.js`, `assets/js/loadout-view.js`, `backend_scripts/generateSimcProfiles.py`, `backend_scripts/generateTierlistPage.py`, `templates/simc_tierlist.html`, `.github/workflows/buildPages.yml` |
| `top-trends-bar` | The Top Trends bar depends on a CI step order, on two stored weeks and on a stable archetype key | `backend_scripts/snapshotTrends.py`, `backend_scripts/pageGeneration.py`, `templates/trends_bar.html`, `templates/top_chrome.html`, `assets/js/trends-bar.js` |
