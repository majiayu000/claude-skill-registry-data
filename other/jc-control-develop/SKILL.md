---
name: jc-control-develop
description: Use when building new pages or components for the JapaConnect Control Panel (apps/control, port 3002, SPA). Covers infrastructure dashboards with LayerChart, the RBAC CRUD Gate, the mandatory DataTable spec, API key/extension/settings/job-queue patterns, and safe polling.
---

# JapaConnect Control Panel — Development Skill

Operator-facing SPA (adapter-static, `super_admin` + `control_panel.access` only). API base `/api/v1/control/*`. Design: dev.to admin + Vercel dashboard; dark mode default; monospace for IDs/keys/JSON.

## ⛔ GATE 1 — API-READINESS
Identical to `jc-admin-develop` Gate 1: list endpoints → verify each → any missing: STOP + ⚠️ MISSING BACKEND API ROUTES alert. Never mock.

## ⛔ GATE 2 — RBAC CRUD (Non-Negotiable)
**Super-admin full CRUD on every Control Panel entity** (API keys, OAuth clients, extensions, tenant sites, system settings, permission nodes, webhook endpoints, backup configs). Before implementing any entity page, verify List/Get/Create/Update/Delete + state routes (activate/deactivate, enable/disable, revoke/restore) all exist and are RBAC-gated. Any missing: STOP + ⛔ MISSING RBAC CRUD ENDPOINTS alert (format in `jc-admin-develop`).

## 📋 DATATABLE SPEC — Same Mandate as Admin
Every entity list (API keys, sites, extensions list-view, failed jobs, audit log, impersonation log) uses the full spec from `jc-admin-develop`: **sortable · searchable · filterable · paginated · action column (View/Edit/Delete + state actions like Revoke, Enable/Disable) · bulk actions · Create button on non-readonly entities**.
Readonly entities here (audit log, impersonation log, webhook delivery log, job history): action column MUST include **Delete/Remove/Clear** per row + a "Clear all / Clear older than…" bulk control.

## LayerChart — Infrastructure & Ops Visualization (Mandatory)
All Control Panel dashboards render metrics with LayerChart:
- **Health dashboard:** per-service time-series sparklines (PG pool usage, Valkey memory, Meilisearch index size) — `<Chart>` + `<Area>`/`<Spline>`
- **Job queue monitor:** queue depth over time per tier (`<Spline>` × 3, legend), failed-vs-processed stacked `<Bars>`
- **AI cost monitoring:** daily spend `<Bars>` + cumulative `<Spline>`
- **Traffic/platform metrics:** request volume, error rate `<Area>`
- Rules: colors `var(--color-success|warning|danger|primary)` only · fixed-height containers · data from `/api/v1/control/*` endpoints · skeletons · live charts append new points on each poll tick

## Key Page Patterns
**API Keys:** DataTable · create in `<Dialog.Root>` with scope multi-select · show key ONCE in reveal dialog (copy button + `<Tooltip.Root>` "Copied!") · never keep raw key in `$state` after close (`onOpenChange` clears) · Revoke = state action with confirmation.
**Extensions:** card grid + `<Toggle.Root>` per extension · toggle disabled while PATCH in-flight · optimistic + rollback · disabling with active content → warning dialog · Configure → manifest-driven settings dialog.
**System Settings (85 keys):** `<Tabs.Root>` per category · type-appropriate inputs · JSON values validated before save · deep-equality dirty tracking (`$derived(JSON.stringify(a)!==JSON.stringify(b))`) · unsaved banner + `beforeNavigate` guard · batch `PATCH` with `[{key,value}]`.

**Geo-aware personalization (ADR-064) settings:**
- `geo_personalization.enabled` (boolean, default `true`) — the killswitch. When false, all surfaces fall back to global ranking. Prominently placed in the settings UI with a warning dialog on disable ("This will disable geo-personalized content for all users").
- Feed geo boost cap, search geo weight multiplier — numeric settings, tuneable without deploy.

**Japa Academy (ADR-063) settings:**
- `university.default_commission_pct`, `university.verified_tier_commission_pct`, `university.partner_tier_commission_pct` — revenue split percentages per tier.
- `academy.pro_stream_rate_kobo` — per-Pro-learner stream rate for creator compensation.
- `university.payout_min_threshold_kobo` — minimum payout amount; below this, payouts roll to next period.
- `university.payout_period_days` — payout cycle length.
- `university.surface_domain` — the Japa Academy branded domain (default `academy.japa.to`). Changing this affects host detection in the Learn app.

**Job Queue:** tabs Critical/Default/Low · stats + failed-jobs DataTable (retry action) · poll 15s.
**Health:** service cards + LayerChart sparklines · poll 30s.
**Safe polling (mandatory pattern):**
```svelte
$effect(() => {
  const tick = async () => { try { const r = await fetch(url); if (r.ok) data = await r.json(); } catch {} };
  tick();
  const id = setInterval(tick, 30_000);
  return () => clearInterval(id);
});
```

## SPA Architecture & Stack
Same as `jc-admin-develop`: `ssr=false`, auth guard verifying BOTH session AND `control_panel.access` node, `$effect` fetching, Svelte 5 Runes, Bits UI dot-notation, Tailwind v4, `$t()` i18n, no AI attribution. Environment badge (PRODUCTION/STAGING) in top bar.

## Deliverables Per Task
1. Gate 1 + Gate 2 output · 2. `+page.svelte` (full-spec DataTable / LayerChart dashboard / settings pattern) · 3. dialogs & components · 4. types · 5. every `/api/v1/control/*` route confirmed
**V2 control panel:** No new control panel pages for v2 features — v2 features are managed in the Admin panel. Control panel remains super-admin infrastructure (tenants, system settings, feature flags). Update system_settings pages to expose the new v2 keys (settings are already stored; control panel just needs form fields for them).

**V2 system settings (JEOS v1.22.0–v1.23.1, §§79–102):** The system_settings page must expose form fields for:
- **14 tool-domain keys** for §§79–101 functional tools: `{slug}.subdomain` and `{slug}.custom_domain` per tool (visa-route, embassy-alerter, arrival-checklist, processing-tracker, credential-checker, cv-formatter, housing-guide, attestation-guide, language-test, tax-calculator, community-locator, plus community feature domains). These feed the Tools app host-detection map.
- **`mentorship.max_capacity`** — maximum mentee capacity per mentor (§102, ADR-110).
- Other feature-specific settings for §§79–102 community features and functional tools.
- Total system settings count is now ~187 (up from 85). Update the settings tab categories to include a "V2 Tools" category for the tool-domain keys.

**V2 feature flags (§§79–102):** ~24 new feature flags for v2 features:
- ~22 flags for §§79–101 community features and functional tools (one per feature, plus sub-feature flags)
- 2 flags for mentorship (§102, ADR-110): `mentorship.enabled` and `mentorship.matching.enabled`
- Feature-flag middleware returns **404 (not 403)** when disabled (ADR-042) — verify the control panel feature-flag toggle UI communicates this behavior
- Total feature flags count is now ~24 (up from previous count)

**Geo-aware tool pattern & ADR-088 verification in control panel:** When adding settings forms for v2 functional tools, verify:
- Tool-domain settings (`subdomain`/`custom_domain`) are string fields with domain validation
- Feature flags for v2 tools are boolean toggles with the ADR-042 404 behavior documented in the field help text
- ADR-088 AI content generation columns (`ai_generated`, `ai_model`, `hitl_reviewed_by`, `ai_generated_at`, `is_japabot_indexed`) are backend concerns but the control panel should expose any related settings (e.g. AI model selection, HITL review workflow toggles)

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
