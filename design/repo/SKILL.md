---
name: cs-repo
description: Analyze a codebase from a product perspective, focusing on specific user role portals (e.g., owner, banker, charter). Per role, enumerate every page/screen and assess whether it's a functional feature or just a visual mockup with hardcoded data. Use when asked to assess project status, audit feature completeness, find hardcoded/dummy data, or produce a product readiness overview. Triggers on phrases like "repo analysis", "project status", "what's done", "hardcode audit", "feature completeness", "what works vs what's fake".
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Write, AskUserQuestion
---

# Repo Analysis Skill

Assess product completeness per user role/portal. The goal is to answer: "For each role, what pages exist, and which ones actually work vs. which are just visual shells?"

## Inputs

`$ARGUMENTS` — optional role portal name(s) to scope analysis (e.g., `owner banker`). If not provided, detect role portals automatically by scanning the routing config and directory structure (`app/`, `pages/`, `routes/`, role-named subdirectories). Report which portals were detected at the start of the output.

If automatic detection finds **zero portals**, use `AskUserQuestion` before proceeding:

- **question**: "Could not auto-detect role portals. How should the analysis be scoped?"
- **options**:

| Option | Description |
|---|---|
| **Analyze as one portal** | Treat the entire codebase as a single portal |
| **Specify portals** | Type portal names in the Other field (e.g., `owner banker`) |
| **Stop** | Cancel — nothing to analyze |

## Process

### 1. Enumerate Pages Per Role

Find the routing config or page directory for each role portal. List every page/screen with its file path.

### 2. Per-Page Assessment

For each page, read the source and determine its product status. **Classification must reflect what data the user actually receives, not how the frontend code is structured.** A page where the frontend correctly calls an API hook but the backend returns hardcoded data is NOT "Functional MVP" — it's "Partially Wired" or "Visual Only" depending on how much is fake.

**Classify each page into one of these levels:**

| Level | Label | What it means |
|-------|-------|---------------|
| 0 | **Empty/Placeholder** | Route exists but page is blank, "coming soon", or just a layout shell |
| 1 | **Visual Only** | UI is built and looks real, but ALL data is hardcoded — whether in the frontend OR in the backend endpoint it calls. Nothing comes from a real database. |
| 2 | **Partially Wired** | Some data comes from a real database, but key parts are hardcoded or mocked — **including backend services that mix real DB queries with hardcoded data files**. A page that calls a real API but the API returns hardcoded data belongs here. |
| 3 | **Functional MVP** | Core workflow works end-to-end with **real database data at every layer**. The frontend fetches from an API, and the API queries a real database — no hardcoded data files, demo entity IDs, or fallback static values in the chain. May lack edge cases, validation, or secondary features. |
| 4 | **Production Ready** | Fully functional with error handling, loading states, validation, and real database data throughout the entire stack. |

### 3. End-to-End Data Flow Tracing (CRITICAL)

**"Calls an API" ≠ real data.** Trace the full stack for every page:

```
UI component → API hook → backend controller → service → data source (DB or hardcode file)
```

Classify based on what the user actually receives, not on whether the frontend code looks properly wired.

### 4. Hardcode Detection

Identify hardcode at all three layers:

**Frontend** — API hooks that exist but are commented out or unused; state initialized with realistic-looking fake data and never updated.

**Backend** — the non-obvious patterns to catch:
- Dedicated mock/hardcode data files imported by services (search for files named `hardcode`, `mock`, `demo`, `fake`, `fixture`, `stub` in `data/`, `fixtures/`, `mocks/` directories)
- Hardcoded entity IDs that silently filter what data is returned (demo org IDs, test user IDs)
- Fallback values embedded in service logic (e.g., `if (year === 2024) return 248414`)
- Services that query a real DB but merge/overlay hardcoded fields on top — this is the most common and hardest to catch

**Hybrid** — backend returns real entity names/IDs but hardcoded numeric values; endpoint works for a hardcoded set of entities but would break for any other input.

### 5. Output Format

Save to `docs/project-status.md` (or user-specified path):

```markdown
# Product Status Report
Generated: [date]
Modules analyzed: [list of role portals]

## Summary
[3-5 sentences: how many pages per role, overall functional vs visual ratio, biggest gaps]

## Overview Matrix

| Role | Page | Status | Hardcoded Items | Notes |
|------|------|--------|-----------------|-------|

Status legend: ○ Empty · ⬤ Visual Only · ◐ Partially Wired · ● Functional MVP · ✅ Production Ready

## [Role Name] Portal

### Summary
- Total pages: X
- Functional: X | Partially wired: X | Visual only: X | Empty: X
- Estimated overall completion: X%

### [Page Name] — [Status Label]
**What the user sees:** [1-2 sentences]
**Data flow:** [frontend hook] → [backend endpoint] → [service] → [data source: DB / hardcode file / hybrid]
**What actually works:** [which fields are real vs hardcoded]
**Hardcoded items:** [description — `file:line` — what it should be]
**What's needed:** [concrete missing pieces]

[repeat per page, per role]

## Backend Hardcode Inventory
All dedicated hardcode/mock data files — so data serving multiple pages is documented once.

- `[file path]` — [what it contains, how many records, which endpoints consume it]

## Cross-Role Observations
[Patterns across roles: shared hardcoded components, backend files serving multiple portals, universal gaps]
```

### 6. Completion % Calculation

Per role, calculate completion as a weighted ratio:
- Empty = 0%, Visual Only = 20%, Partially Wired = 50%, Functional MVP = 80%, Production Ready = 100%
- Role completion = average across its pages
- Overall = average across roles

These numbers are rough estimates for communication purposes. Always present them alongside the detailed breakdown so they can't be misread.
