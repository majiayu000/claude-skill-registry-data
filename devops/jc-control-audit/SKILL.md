---
name: jc-control-audit
description: Use when performing a comprehensive quality audit of the JapaConnect Control Panel (apps/control) before merge or release. Verifies security-critical key handling, polling reliability, RBAC CRUD completeness, DataTable spec, and LayerChart compliance.
---

# JapaConnect Control Panel — Audit Skill

Work file-by-file. Conventions: `jc-control-develop`. Security findings carry extra weight here.

## A. RBAC CRUD Completeness Matrix (Run First)
Same matrix method as `jc-admin-audit` §A, over Control entities: API keys, OAuth clients, extensions, tenant sites, system settings, permission nodes, webhook endpoints, backup configs. Verify List/Get/Create/Update/Delete + state routes (revoke, enable/disable, activate/deactivate) exist in backend AND are surfaced in UI. **Any super-admin CRUD gap = Critical** (⛔ block).

## B. Security — Critical
- [ ] Raw API keys cleared from `$state` after one-time reveal · never in URLs/history/console
- [ ] Reveal dialog clears on `onOpenChange`
- [ ] Secret settings values masked in UI
- [ ] `control_panel.access` node verified on mount (not just session) · 403 → error page
- [ ] CSRF on all mutations · JSON settings validated pre-save

## C. Polling Reliability
Every `setInterval`: `$effect` cleanup return present · initial fetch before interval · errors caught inside tick · no stacked intervals (navigate away/back 5×, confirm single interval in DevTools) · live chart series capped (≤60 points).

## D. DataTable Spec Compliance
Full checklist from `jc-admin-audit` §B per entity list. Control-specific verifications: readonly logs (audit, impersonation, webhook deliveries, job history) have per-row Delete/Clear + bulk clear · API keys have Revoke · extensions have Enable/Disable conditional on state · failed jobs have Retry.

## E. LayerChart Compliance
Health/queue/cost dashboards use LayerChart exclusively · `var(--color-*)` only (dark-default verified) · fixed heights · skeletons · poll-driven charts append correctly.

## F. Extension & Settings Integrity
Toggle: in-flight disable, rollback, active-content warning. Settings: deep-equality dirty, `beforeNavigate` guard, snapshot-after-load, batch save all changed keys. **Geo/Japa Academy settings (ADR-063/064):** `geo_personalization.enabled` killswitch present with disable-warning dialog · `university.*` settings (commission tiers, pro stream rate, payout threshold/period, surface_domain) all present and editable · JSON-typed settings validated before save · `university.surface_domain` change shows a warning (affects Learn app host detection).

## G. API Consumption, SPA, Bits UI, Svelte 5, A11y, i18n
Apply `jc-admin-audit` §§C, E, and `jc-main-audit` §§D, B(runes), H, I. Plus: env badge correct · monospace on IDs/keys/args · health cards show last-updated timestamp.

## Report Format
```
## Audit Report — Control Panel (apps/control)
**Files Audited:** [n] · **Status:** PASS / NEEDS FIXES
### Critical (security + RBAC CRUD gaps block deployment) / High / Medium / Low
### RBAC CRUD Matrix
[entity × routes table]
### Compliance Summary
| Security (keys, permissions) | ✅/❌ |
| Polling reliability | ✅/❌ |
| RBAC CRUD completeness | ✅/❌ |
| DataTable spec | ✅/❌ |
| LayerChart | ✅/❌ |
| Settings/toggle integrity | ✅/❌ |
| SPA · Bits UI · Svelte 5 · A11y | ✅/❌ |
```
**V2 control panel:** No new control panel pages for v2 features — v2 features are managed in the Admin panel. Control panel remains super-admin infrastructure (tenants, system settings, feature flags). Update system_settings pages to expose the new v2 keys (settings are already stored; control panel just needs form fields for them).

**V2 system settings (JEOS v1.22.0–v1.23.1, §§79–102):** Verify the system_settings page exposes form fields for:
- **14 tool-domain keys** for §§79–101 functional tools: `{slug}.subdomain` and `{slug}.custom_domain` per tool. Flag missing form fields for any of the 12 functional tool slugs.
- **`mentorship.max_capacity`** — maximum mentee capacity per mentor (§102, ADR-110). Flag if missing.
- Total system settings count is now ~187 (up from 85). Flag if settings page doesn't have a "V2 Tools" category tab for the tool-domain keys.

**V2 feature flags (§§79–102):** ~24 new feature flags for v2 features:
- ~22 flags for §§79–101 community features and functional tools
- 2 flags for mentorship (§102, ADR-110): `mentorship.enabled` and `mentorship.matching.enabled`
- Feature-flag middleware returns **404 (not 403)** when disabled (ADR-042) — flag if the control panel feature-flag toggle UI doesn't communicate this behavior
- Total feature flags count is now ~24

**Geo-aware tool pattern & ADR-088 verification:** When auditing control panel settings for v2 functional tools, verify:
- Tool-domain settings (`subdomain`/`custom_domain`) are string fields with domain validation
- Feature flags for v2 tools are boolean toggles with ADR-042 404 behavior documented in field help text
- ADR-088 AI content generation settings (AI model selection, HITL review workflow toggles) are exposed if applicable

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
