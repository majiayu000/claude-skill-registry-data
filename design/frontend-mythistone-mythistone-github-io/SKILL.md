---
name: frontend
description: "MythiStone client-side conventions: design tokens, library choices, Chart.js theming, asset minify, deep links, Klaro consent for embeds, infinite scroll, DataTables, card/sidenav layout utilities. Use when editing assets/css, assets/js, or page markup and styling."
---

# Frontend domain

## Gotchas

Before changing a file listed below, read its gotcha: `ref/<id>.md` in this skill (or `kb_gotcha <id>`).

| id | rule | files |
|---|---|---|
| `bootstrap-capture-phase` | Bootstrap 5 data-api handlers run at document capture phase, so stopPropagation on a link inside an accordion button is useless; use a window-capture shield | `assets/js/spec-page.js` |
| `chart-theming` | Use window.MythiChart (assets/js/chart-theme.js) for Chart.js chrome colors, icon preloading, patch annotations, and live re-theming; do not re-copy chart boilerplate | `assets/js/chart-theme.js`, `assets/js/dashboard.js`, `assets/js/dungeon-page.js`, `assets/js/spec-page.js` |
| `datatables-empty-state` | A DataTables-initialized table whose empty state is a colspan placeholder <tr> inside the same table throws "Requested unknown parameter '1' for row 0, column 1"; wrap the whole <table> in {% if rows %} and put the empty state in a plain <p> | `assets/js/dungeon-page.js`, `assets/js/item.js`, `templates/dungeon_page.html`, `templates/item.html` |
| `deep-links` | Covers site-wide \#fragment deep links, copy-link buttons, and the instant-scroll workaround in assets/js/deep-link.js | `assets/js/deep-link.js`, `assets/js/share.js` |
| `floating-header-card-rows` | Rows of cards with the Material Dashboard floating header (the gold ribbon, mt-n4) need their own mb-4 or top clearance, or the ribbon collides with the card above on wide screens | `templates/dungeon_page.html`, `templates/spec_page.html` |
| `frontend-design-tokens` | Never hardcode domain hex (class, item-rarity, stat, scrollbar colors) in page CSS/templates; use the CSS custom properties and utility classes | `assets/css/*.css`, `assets/scss/*` |
| `frontend-framework-choices` | Which frontend library to reach for per concern (modals, tables, selects, charts, search, consent) and the no-build-step conventions | `templates/header_imports.html`, `templates/javascript_imports.html`, `assets/js/plugins/*` |
| `in-card-scroll-regions` | The shared .card-scroll-body / .card-scroll utility for a list or table that scrolls inside a card while filling the card's real height | `assets/css/custom-scrollbars.css` |
| `infinite-scroll-pages` | How paginated listing pages (blog, items, routes) load more entries via the shared window.MythiInfinite sentinel helper, and the server-render-page-1 + JSON-manifest + shared-card pattern | `assets/js/consumables.js`, `assets/js/infinite-scroll.js`, `assets/js/blog-infinite.js`, `assets/js/items.js`, `assets/js/finder.js`, `backend_scripts/generateBlogPage.py` |
| `klaro-consent-embeds` | Klaro only manages embeds present at its init, so client-rendered keystone.guru iframes must gate consent themselves via MythiConsent.loadEmbed | `assets/js/consent.js`, `assets/js/finder.js`, `assets/js/routes-finder.js` |
| `minify-assets` | How first-party CSS/JS assets are served and minified | `backend_scripts/minifyAssets.py`, `templates/header_imports.html`, `templates/javascript_imports.html` |
| `notification-dismiss-persistence` | Dismissible site notifications are injected client-side from assets/json/notifications.json and persist per-browser in localStorage keyed by a stable key, and first-party functional storage is NOT gated behind Klaro consent | `backend_scripts/pageGeneration.py`, `assets/css/responsive.css`, `assets/js/notifications.js`, `templates/notifications.html` |
| `sidenav-footer-flow` | The left sidenav uses a flex-column flow layout so its scrollable nav list is contained above the support-buttons footer; do not restore absolute positioning or a fixed 72vh list height | `templates/sidenav.html`, `assets/css/responsive.css`, `assets/css/material-dashboard.css` |
