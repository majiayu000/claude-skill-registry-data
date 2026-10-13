---
name: building-flashfusion-live-artifacts
metadata:
  version: "1.3.2"
description: >
  Builds, patches, and registers the FlashFusion Agent Control Center as a Cowork live
  artifact — void-dark dashboard with semi-transparent blur panels, live Supabase data, and
  per-panel Demo fallback. Activates on build the FlashFusion artifact, rebuild the control
  center, add a panel to the dashboard, the artifact is broken, update FlashFusion dashboard,
  patch the agent dashboard, fix the live connection, update brand tokens, ff artifact, ff
  dashboard, agent control panel, agent control center, demo mode artifact, approval queue
  panel, HITL queue dashboard, live agent view, ChaosClubCo dashboard. Fires on dashboard or
  control-center requests in the FlashFusion context even when FlashFusion or artifact is not
  named. PERSONAL lane only — never run on LOXIHART tasks.
---

# Building FlashFusion Live Artifacts

Navigation layer for the full FlashFusion Agent Control Center workflow. Canonical specs live in `sot/FF-PLAT-CORE-SOT.md`. Phase detail, patch playbook, and gotchas live in `references/`.

## TL;DR

Sandbox enforces strict CDN whitelist (Chart.js 4.5.0, Grid.js, Mermaid), blocks `fetch()`, requires `color-scheme: light` on `:root`. Demo mode is the primary UX — OAuth TTL expires within one turn. Every panel needs independent Demo fallback. LOXIHART project ID `oorstbwcydxwiojrsoim` is a hard stop.

---

## Source of Truth — READ THESE BEFORE WRITING ANY CODE

All canonical FlashFusion specs live in `sot/FF-PLAT-CORE-SOT.md`. **Query by section anchor — never load the entire SOT.**

Required SOT reads, by task type:

| Task | Read these SOT sections | Read these references |
|---|---|---|
| Build from scratch | §1, §2, §3, §6, §7, §8, §9, §10 | `references/phases.md` |
| Patch 1–3 panels | §3 (panels), §4 (schema) | `references/patch-playbook.md` |
| Add new panel | §3 (canonical list), §4 (schema), §5 (state) | `references/patch-playbook.md` |
| Fix live connection | §7 (sandbox), §10 (MCP tools), §8 (LOXIHART check) | `references/gotchas.md` #3, #7 |
| Update brand tokens | §1 (tokens), §2 (recipe) | — |
| Debug rendering | §7 (sandbox), §6 (CDN) | `references/gotchas.md` |

`sot/INFOGRAPHIC-CORRECTED.md` explains the tier model. Read once for context; not needed per-task.

---

## Decision Tree

```
What triggered this workflow?
  ├─ Build from scratch
  │    └─ Run all 7 phases — references/phases.md
  │       Read SOT §1, §2, §3, §6, §7, §8, §9, §10 first
  ├─ Schema change (column renamed, table added/dropped)
  │    └─ references/patch-playbook.md — 5 steps
  │       Read SOT §3, §4
  │       Do NOT full rebuild
  ├─ Add a new panel
  │    └─ references/patch-playbook.md — "Adding a Panel" template
  │       Read SOT §3, §5
  │       Do NOT rewrite existing panels
  ├─ Fix broken live connection (OAuth error / MCP failure)
  │    └─ references/gotchas.md #3, #7 — diagnose first, don't rebuild
  │       Read SOT §7, §10
  └─ Update brand tokens only
       └─ Update SOT §1 — then patch artifact CSS
          Re-run smoke test items 1, 3, 4 only
```

---

## Usage Examples

**Example 1 — Build from scratch.**
User: "Build the FlashFusion Agent Control Center artifact."
→ Lane check (PERSONAL confirmed). Read SOT §8 (LOXIHART quarantine) first. Read SOT §1, §2, §3, §6, §7, §9, §10. Read `references/phases.md`. Build 10 required panels with Demo data. ToolSearch for `create_artifact`. Register with `artifact_id` from SOT §9. Smoke test all 10 items.

**Example 2 — Schema change patch.**
User: "The approvals table got a new 'priority' column — update the dashboard."
→ Read SOT §3, §4. Read `references/patch-playbook.md`. Affected panels: approval queue only (§3 row 5). Update SOT §4 schema first, then apply Patch Playbook 5 steps. Re-register with `update_artifact`.

**Example 3 — Fix broken live connection.**
User: "The live data isn't loading, just showing Demo."
→ Do NOT rebuild. Read `references/gotchas.md` #3 (network blocked) and #7 (OAuth TTL). Check localStorage for `ff_pid`. Check OAuth status. Verify MCP tool names via ToolSearch (per SOT §10).

---

## Phase Navigator

| Phase | Name | Primary detail location |
|---|---|---|
| 1 | Pre-Build Lane Gate | `references/phases.md` Phase 1 + SOT §8 |
| 2 | Brand Token Load | SOT §1 + §2 |
| 3 | HTML Build (10 panels) | `references/phases.md` Phase 3 + SOT §3 |
| 4 | Data Fetch Architecture | `references/phases.md` Phase 4 |
| 5 | CDN Requirements | SOT §6 |
| 6 | Register Artifact | `references/phases.md` Phase 6 + SOT §9 + §10 |
| 7 | Smoke Test | Inline below |

---

## Gotchas — Top 10 (Full Diagnosis in references/gotchas.md)

1. `create_artifact` and `update_artifact` are ALWAYS deferred — ToolSearch every time
2. `color-scheme: light` on `:root` is non-negotiable, even on dark themes
3. No `fetch()`, `XMLHttpRequest`, or third-party SDKs — only `window.cowork.callMcpTool`
4. LOXIHART project ID `oorstbwcydxwiojrsoim` — hard stop if found anywhere
5. Chart.js exact version `4.5.0` with integrity hash from SOT §6 — silent failure otherwise
6. Per-panel Demo fallback — never a global catch-all
7. OAuth TTL expires within one turn — Demo mode is primary UX, Live is opt-in
8. Artifact ID `flashfusion-control-center` is FIXED — never change (SOT §9)
9. `unpkg.com` and `cdnjs.cloudflare.com` are blocked — only `cdn.jsdelivr.net` (SOT §6)
10. Patching beats rebuilding for <6 affected panels

Full diagnosis + fix for each: `references/gotchas.md`.

---

## Smoke Test Checklist

Run after every build or patch. All 10 must pass before the artifact is production-ready.

- [ ] 1. Renders without JS errors in browser console
- [ ] 2. Demo mode displays all 10 panels with plausible data (no empty panels)
- [ ] 3. Config modal opens with `?` key and C button; closes with Escape
- [ ] 4. Entering a project ID sets `ff_pid` in localStorage and switches badge to "LIVE"
- [ ] 5. Clearing project ID reverts to Demo mode
- [ ] 6. Budget gauge reflects `ff_budget` from localStorage (default 50)
- [ ] 7. Chart.js line chart renders 7-day trend (Demo data acceptable)
- [ ] 8. Approval queue table shows rows (Demo data acceptable)
- [ ] 9. V3 style: void bg (#000), semi-transparent blur panels, violet accents, Geist/Geist Mono fonts
- [ ] 10. Artifact ID is exactly `flashfusion-control-center` (not a new ID — SOT §9)

---

## Self-Verification Checklist (Before Registering)

- [ ] PERSONAL lane confirmed — no LOXIHART references present
- [ ] `oorstbwcydxwiojrsoim` does NOT appear anywhere in artifact HTML (per SOT §8)
- [ ] `color-scheme: light` is the first property in `:root` (per SOT §1)
- [ ] Chart.js uses exact version `4.5.0` with correct integrity hash (per SOT §6)
- [ ] No `fetch()`, `XMLHttpRequest`, or `supabase-js` in artifact HTML (per SOT §7)
- [ ] All data access uses `window.cowork.callMcpTool()`
- [ ] Every panel has its own Demo fallback (not a global catch-all)
- [ ] `ff_pid`, `ff_budget`, `ff_mode` read/written from localStorage per SOT §5
- [ ] Artifact ID is `flashfusion-control-center` (per SOT §9)
- [ ] ToolSearch called before `create_artifact` / `update_artifact` (per SOT §10)
- [ ] All 10 smoke test items checked

---

## CLAIMS / COUNTEREXAMPLES / CONTRADICTIONS

- [SOURCED] Cowork artifact sandbox CDN whitelist includes Chart.js, Grid.js, Mermaid only (observed)
- [SOURCED] `color-scheme: light` required on `:root` (observed behavior)
- [SOURCED] `mcp__cowork__create_artifact` is deferred every session (observed across sessions)
- [SOURCED] Supabase OAuth TTL expires before callback in one turn (observed twice)
- [SOURCED] `window.cowork.callMcpTool()` is the only permitted data access pattern (observed: direct fetch produces empty panels, no console error)
- [SOURCED] SKILL.md body ≤ 500 lines per Anthropic — this file is now ~200 lines, well under
- [GENERATED] Per-panel Demo fallback safer than top-level catch-all — reasoned from partial-failure scenario
- [GENERATED] Demo mode as primary UX correct given OAuth TTL constraints

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS

- CDN whitelist policy not publicly documented — derived from empirical observation, may change
- Chart.js integrity hash for versions other than 4.5.0 not verified
- `window.cowork.askClaude()` behavior with large payloads untested
- Write-back to Supabase via `callMcpTool` architecturally possible but untested
- Artifact HTML size limits (if any) undocumented — very large artifacts may fail silently at registration

---

## Version History

- **1.1.0** (2026-05-16) — Refactored to navigation layer. Canonical specs moved to `sot/FF-PLAT-CORE-SOT.md`. Body reduced from ~365 to ~200 lines per Anthropic progressive disclosure pattern.
- **1.0.0** (2026-05-15) — Initial release. All content inline.

## FAIL Conditions

Named failure modes for this skill. Each is a hard stop, not a warning.

- **The LOXIHART project ID oorstbwcydxwiojrsoim appears anywhere in the artifact HTML** → cross-lane data leak — this is PERSONAL-lane only; scan for it and abort the build if found (SOT §8).
- **Using fetch(), XMLHttpRequest, or supabase-js directly for data access** → the artifact silently fails in the Cowork sandbox — all data goes through window.cowork.callMcpTool only (SOT §7).
- **Calling create_artifact or update_artifact without ToolSearch first** → tool-not-found failure — these tools are always deferred, ToolSearch every time (SOT §10).
- **Changing the fixed artifact ID flashfusion-control-center** → registration breaks or duplicates — the ID is immutable (SOT §9).
- **A global Demo catch-all instead of a per-panel fallback** → one dead panel blanks the whole dashboard — every panel gets its own Demo fallback (SOT §3).
- **Treating Live data as the primary path** → blank UX when the OAuth TTL expires mid-turn — Demo is primary, Live is opt-in (gotcha #7).

## Evals

- ✅ **SHOULD TRIGGER** — "rebuild the FlashFusion control center" or "add a panel to the dashboard."
- ✅ **SHOULD TRIGGER** — "the live data isn't loading, just showing Demo" — diagnose per gotchas, do not rebuild.
- ❌ **SHOULD NOT TRIGGER** — any LOXIHART dashboard or tool request — hard stop, this skill is PERSONAL lane only.
