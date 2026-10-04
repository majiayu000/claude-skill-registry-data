---
name: bmc-dashboard-one-click-setup
description: >
  One-click setup and verification of the BMC Dashboard: .env, service account,
  Apps Script (Code.gs, DialogEntregas), sheets, triggers, API server, Panelin
  integration, and ngrok. Use when the user asks for dashboard setup, one-click
  setup, run dashboard, configure BMC dashboard, or verify dashboard readiness.
  Also handles version bump, changelog automation, and update logs.
---

# BMC Dashboard One-Click Setup

Orchestrates full local dashboard setup: env, credentials, sheets, automations, API, Panelin, and health checks. Supports versioning and changelog automation.

## Quick Start

**One command:**

```bash
./run_dashboard_setup.sh
```

Or from repo root:

```bash
bash run_dashboard_setup.sh
```

## Setup Checklist (Automated)

The script performs:

| Step | Action | Validation |
|------|--------|------------|
| 1 | Ensure `.env` exists with `BMC_SHEET_ID`, `GOOGLE_APPLICATION_CREDENTIALS` | `.env` present, vars set |
| 2 | Ensure service account JSON at `docs/bmc-dashboard-modernization/service-account.json` | File exists, valid JSON |
| 3 | Share spreadsheet with service account email as Editor | Manual (script prompts) |
| 4 | `npm install` | `node_modules` populated |
| 5 | Start API (port 3001) + optional ngrok | `GET /health` returns `ok: true` |
| 6 | Run dashboard (port 3849) or use integrated `/finanzas` | Dashboard loads |
| 7 | Run verification checks | All checks pass |

## Manual Prerequisites (Before One-Click)

1. **Google Cloud:** Create service account with Sheets API (read + write). Download JSON key → save as `docs/bmc-dashboard-modernization/service-account.json`.
2. **Spreadsheet:** Share "2.0 - Administrador de Cotizaciones" with service account email as **Editor**.
3. **Apps Script (Phase 1–2):** Paste `Code.gs`, add `DialogEntregas.html`, run `runInitialSetup`, add triggers per `IMPLEMENTATION.md`.

## Verification Commands

```bash
# Health
curl -s http://localhost:3001/health | jq .

# Dashboard API
curl -s http://localhost:3001/api/cotizaciones | jq .ok

# Finanzas tab (integrated)
# Open http://localhost:5173 → Finanzas
```

## Versioning & Changelog

When user asks for version bump or update logs:

```bash
./scripts/bump_version.sh [major|minor|patch] ["Changelog message"]
```

Example:

```bash
./scripts/bump_version.sh patch "Fix dashboard API health check"
./scripts/bump_version.sh minor "Add one-click setup script"
```

**Version criteria:**

- **MAJOR:** Breaking API/sheet structure, removed features.
- **MINOR:** New dashboard features, new sheets, new automations.
- **PATCH:** Fixes, refactors, docs, UI tweaks.

After bumping, update `README.md` if architecture or setup changed.

## File Reference

| File | Purpose |
|------|---------|
| `run_dashboard_setup.sh` | One-click setup script |
| `scripts/bump_version.sh` | Version bump + changelog automation |
| `docs/bmc-dashboard-modernization/IMPLEMENTATION.md` | Phase-by-phase guide |
| `docs/bmc-dashboard-modernization/Code.gs` | Apps Script (Phase 1–2) |
| `docs/bmc-dashboard-modernization/sheets-api-server.js` | API + dashboard server |
| `.env` | `BMC_SHEET_ID`, `GOOGLE_APPLICATION_CREDENTIALS` |

For env template, verification endpoints, and phase checklist, see [reference.md](reference.md).

## Output Format

- **Setup:** Numbered steps with ✓/✗ status.
- **Errors:** Clear message + suggested fix (e.g. "Add BMC_SHEET_ID to .env").
- **Success:** Summary table (API URL, Dashboard URL, health status).
