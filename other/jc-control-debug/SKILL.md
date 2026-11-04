---
name: jc-control-debug
description: Use when reviewing or debugging JapaConnect Control Panel code (apps/control, SPA). Diagnoses polling memory leaks, sensitive key handling, extension toggle races, DataTable spec gaps, LayerChart issues, and RBAC gaps.
---

# JapaConnect Control Panel — Review & Debugging Skill

Conventions and gates: `jc-control-develop`. Run in order.

## 0. Gates First
Data not loading → verify route exists before debugging (⚠️ alert if missing). Entity page missing a CRUD/state action → check backend route (⛔ alert if missing; hiding the action in the UI is not a fix).

## 1. Polling Memory Leaks (#1 Control Panel Bug)
Every `setInterval` inside `$effect` MUST return `() => clearInterval(id)`. Stacked intervals from navigation = exponential API load. Also check: initial fetch before interval starts · fetch errors caught silently inside the tick (a thrown error kills the loop) · optional `visibilitychange` pause.

## 2. Sensitive Data
Raw API key never in `$state` after one-time reveal (dialog `onOpenChange` clears it, with close-animation delay) · never in URL params/history/`console.log` · secret settings masked · JSON textareas validated before PATCH.

## 3. Extension Toggle Races
Toggle `disabled` during in-flight PATCH · `toggling` guard flag · optimistic + rollback on failure · disable-with-active-content confirmation dialog.

## 4. Settings Dirty State
Deep equality (`JSON.stringify`) not reference compare · `original` snapshot captured AFTER data load · `beforeNavigate` guard fires when dirty · batch save includes ALL changed keys. **Geo/University settings:** `geo_personalization.enabled` toggle should show a warning dialog before disabling (affects all users). `university.surface_domain` change should warn (affects Learn app host detection). Commission/payout settings are numeric — validate range (0-100 for percentages, positive for kobo amounts).

## 5. DataTable Spec
Apply the full checklist from `jc-admin-debug` §1 — including readonly-entity Delete/Clear actions on audit/impersonation/job logs, and Revoke/Enable/Disable state actions conditional on row state.

## 6. LayerChart
Fixed-height containers · `var(--color-*)` colors (dark-default theme — verify contrast) · live charts appending points correctly on poll ticks without unbounded array growth (cap series length, e.g. last 60 points) · `d3-scale` imports · skeletons · LayerChart vs Bits UI `Tooltip` import alias.

## 7. Permission Gate
Root layout verifies `control_panel.access` node (not just session) · 403 → error page not blank screen · super_admin-only actions doubly gated.

## 8. SPA / Svelte 5 / Bits UI / A11y
Apply `jc-admin-debug` §§2–3, 6–7.

## Output Protocol
1. Root cause (one sentence) · 2. Broken code · 3. Fixed code · 4. Secondary findings
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
