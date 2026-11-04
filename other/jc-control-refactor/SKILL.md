---
name: jc-control-refactor
description: Use when updating or refactoring existing JapaConnect Control Panel code (apps/control). Fixes polling patterns, upgrades tables to full DataTable spec, migrates ops charts to LayerChart, hardens key handling.
---

# JapaConnect Control Panel — Updating & Refactoring Skill

Conventions and gates: `jc-control-develop`. Behavior-preserving only; one-line comment per change.

## 0. Gates
New endpoint needed by the refactor → verify first (⚠️/⛔ alerts, pause). Refactoring an entity page → run Gate 2 (RBAC CRUD) on that entity and flag gaps.

## 1. Polling → Safe $effect Pattern
```svelte
// BEFORE: onMount/onDestroy interval pair (or worse, no cleanup)
// AFTER:
$effect(() => {
  const tick = async () => { try { const r = await fetch(url); if (r.ok) data = await r.json(); } catch {} };
  tick();
  const id = setInterval(tick, 30_000);
  return () => clearInterval(id);
});
```

## 2. Table → Full DataTable Spec
Apply `jc-admin-refactor` §1 in full. Control-specific: audit log / impersonation log / webhook deliveries / job history are readonly — ensure Delete/Remove/Clear per row + "Clear all / older-than" bulk. API keys get Revoke state action; extensions list-view gets Enable/Disable.

## 3. Chart Migration → LayerChart
All health/queue/cost/traffic visualizations rewritten in LayerChart (patterns in `jc-control-develop`). Live-updating charts: cap series arrays (last 60 points) to prevent unbounded growth. Remove old chart libraries from package.json.

## 4. Key Handling Hardening
One-time reveal dialog clears value on close · remove any `$state` retention, URL exposure, console logging of raw keys.

## 5. Settings Modernization
Deep-equality `$derived` dirty tracking · `beforeNavigate` guard · JSON validation `$effect` · batch save. **Geo/University settings (ADR-063/064):** add `geo_personalization.enabled` killswitch with disable-warning dialog · add `university.*` settings (commission tiers, pro stream rate, payout threshold/period, surface_domain) with range validation and surface_domain change warning.

## 6. Toggle Hardening
Add `toggling` guards, in-flight disable, optimistic + rollback to all extension/feature-flag toggles.

## 7. Standard Migrations
Svelte 4→5, Bits UI adoption, Tailwind v4, i18n, a11y — apply `jc-main-refactor` §§1–2, 5.
**V2 control panel:** No new control panel pages for v2 features — v2 features are managed in the Admin panel. Control panel remains super-admin infrastructure (tenants, system settings, feature flags). Update system_settings pages to expose the new v2 keys (settings are already stored; control panel just needs form fields for them).

**V2 system settings (JEOS v1.22.0–v1.23.1, §§79–102):** The system_settings page must expose form fields for:
- **14 tool-domain keys** for §§79–101 functional tools: `{slug}.subdomain` and `{slug}.custom_domain` per tool. These feed the Tools app host-detection map.
- **`mentorship.max_capacity`** — maximum mentee capacity per mentor (§102, ADR-110).
- Total system settings count is now ~187 (up from 85). A "V2 Tools" category tab should exist for the tool-domain keys.

**V2 feature flags (§§79–102):** ~24 new feature flags for v2 features:
- ~22 flags for §§79–101 community features and functional tools
- 2 flags for mentorship (§102, ADR-110): `mentorship.enabled` and `mentorship.matching.enabled`
- Feature-flag middleware returns **404 (not 403)** when disabled (ADR-042)
- Total feature flags count is now ~24

## V2 Feature Areas (Implement Only After Corresponding Backend Phase Is Complete)

| Feature | Backend phase | Key sections | Gates |
|---|---|---|---|
| JapaBot (RAG-grounded) | Phase 41 | §69 | `/ai/chat` amended |
| AI Content Studio (admin) | Phase 42 | §75 | `studio.*` RBAC |
| Participation queue (admin) | Phase 42 | §76 | `participation.review` RBAC |
| Visa Checklist | Phase 43 | §70 | `checklist.use` RBAC |
| Readiness Assessment | Phase 43 | §71 | `assessment.take` RBAC |
| Cost of Living Calculator | Phase 43 | §72 | `col_calculator.use` RBAC |
| Scholarship Finder | Phase 43 | §73 | `scholarship.browse` RBAC |
| Remittance Rate Tracker | Phase 44 | §74 | `remittance.view` RBAC |
| Referral system | Phase 45 | §60 | `referral.use` RBAC |
| Self-serve ads | Phase 45 | §61 | `ads.self_serve.create` RBAC |
| Newsletter | Phase 45 | §62 | `newsletter.subscribe` RBAC |
| Jobs board | Phase 45 | §63 | `jobs.browse` RBAC |
| Gamification | Phase 45 | §64 | `gamification.view` RBAC |
| Content import | Phase 46 | §65 | `import.use` RBAC |
| Advanced analytics | Phase 46 | §66 | `analytics.advanced` RBAC |
| Travel search | Phase 46 | §67 | `travel.search` RBAC |

**API-Readiness Gate applies to all v2 features.** Verify against `api-routes-catalog.md` — all v2 routes are marked as "V2 planned" in the catalog. Once the corresponding backend phase lands, the planned routes become available.

**Removed surface:** `apps/tools` was consolidated into `apps/main` (`/tools/{tool}`) — ADR-086 superseded. `tools.japa.to` and per-tool subdomains 301 to `japa.to/tools/{tool}`; the `jc-tools-*` skills were deleted.
