---
name: "che-xray"
description: "X-ray onboarding for NEW repositories. Detects stack, language, monorepo vs single structure, folder conventions, code patterns, tests, CI, DB, and services. Generates a 12-section project_profile.md persisted in the global project registry (Level 1.5) and populates half of architecture.md automatically via graphify. Use the FIRST TIME che touches a repo. Idempotent: rerun for refresh."
---

# Che X-Ray — Repo Onboarding X-Ray

> **SHARED REFERENCES (CANONICAL — DO NOT DUPLICATE body here):**
> - Full engineering contracts (precedence 1-18, DbC, KISS, No Accidental Complexity, Ousterhout): `engineering-contracts` skill
> - Path resolution + project registry Level 1.5 helpers: `che` CLI (`che compute_paths`, `che registry_lookup`)
> - Knowledge graph AST: `/che-graph refresh` (graphify CLI pipx wrapper: `graphifyy`)
> - Human product context complement: `/che-onboarding`

---

## 0. WHEN TO CALL

**EXACTLY ONCE per PROJECT (not per worktree, not per session):**
- The first time che touches this repository (any worktree)
- Or an explicit refresh when architecture changes significantly (e.g. migrated monolith → monorepo, changed framework)

**NON-GOALS (do not use X-Ray for):**
- Task spec → use `/che-spec`
- Human product context → use `/che-onboarding`
- Real-time diff knowledge → use `/che-explain`

---

## 1. PREFLIGHT (Mandatory before any scan)

Execute the X-Ray Python script to resolve safe paths (outside worktree):

```bash
python3 -m che_core.xray "$WORKTREE_ROOT" "$SESSION_ID"
```

Capture the environment variables printed by the script (e.g. `XRAY_PROJECT_PROFILE_PATH`, `XRAY_ARCHITECTURE_PATH`, `GRAPHIFY_OK`).

### 1.1 Writing registry artifacts (3 outputs)

**DO NOT perform manual `cat > file` write inside worktree.** Use the `Write` tool to save files to the exact (absolute) paths returned by preflight.

After generating and saving the files, finalise the audit by running:

```bash
python3 -m che_core.xray "$WORKTREE_ROOT" "$SESSION_ID" --finalize --files-scanned <COUNT>
```

---

## 2. 7-STEP SCAN PIPELINE (Fixed order)

### Step 1 — Graphify (Mandatory, ~15s)
```
/che-graph refresh          # generates Knowledge Graph at project L2 level (project/graphify/)
/che-graph stats            # extracts symbol counts, languages, files
```
Automatically extracts from graph output (L2):
- entry points (Next.js apps, package.json main, server.ts, main.py)
- data layer tables/entities/repositories
- test framework detection (Vitest/Jest/Pytest)
- dependency graph hubs (most imported modules)

### Step 2 — Fallback lightweight AST scan (if GRAPHIFY_OK=0)
Alternative without graphify (grep + Glob heuristics):
- `*Glob **/*.{ts,tsx,py,rs,go,java,rb}` → top 3 extensions by count → primary language
- `Glob package.json pyproject.toml Cargo.toml go.mod pom.xml build.gradle` → build system
- `Glob docker-compose.yml compose.yml .env.example docker/` → container infra
- `Glob .github/workflows/* .gitlab-ci.yml .circleci/* nx.json turbo.json` → CI/orchestrator
- `Glob **/migrations/ **/prisma/schema.prisma supabase/migrations/*` → DB layer

### Step 3 — Structure + monorepo detection
Classifies as:
- `SINGLE-REPO` (1 app): single package.json at root
- `PNPM-MONOREPO-WORKSPACES`: `pnpm-workspace.yaml` at root + `packages/`
- `NPM-MONOREPO-WORKSPACES`: root package.json `"workspaces": []`
- `NX-MONOREPO`: `nx.json` at root
- `TURBOREPO`: `turbo.json` at root
- `POETRY/WORKSPACES` Python: `workspaces = true` in pyproject.toml
- `UNKNOWN-CUSTOM` if multiple apps in `apps/*/src` folders

Extracts:
- Number of apps and packages
- Name of each package (and `@org/pkg` scope if present)
- Detected canonical folder conventions: `src/`, `app/`, `pages/`, `components/`, `services/`, `repositories/`, `lib/`, `db/`, `tests/`

### Step 4 — Tech Stack (auto-detect)
Populates 10-category stack table:
| Category | Auto-detect sources |
|---|---|
| Primary language | % .ts/.py/.rs/.go files + package.json engines |
| Frontend framework | next/react/vue/angular/svelte in dependencies |
| Backend framework | nest/express/fastify/django/fastapi/actix/gin/spring |
| Database driver | pg/postgres prisma typeorm sqlite mysql redis neo4j |
| Auth provider | next-auth supabase-auth auth0 clerk jwt |
| Payment (if any) | stripe braintree paypal mercadopago |
| Testing framework | vitest jest playwright cypress pytest pnpm test: |
| Lint/format | biome eslint prettier ruff black gofmt |
| CI/CD provider | .github → GitHub Actions; .gitlab → GitLab CI; railway.json → Railway; vercel.json → Vercel |
| Deploy target | vercel.json → Vercel; railway.json → Railway; Dockerfile + k8s manifests → K8s; terraform → TF provider |

### Step 5 — Code Conventions + Patterns
Auto-detects (grep + glob heuristics):
- **Import strategy**: `tsconfig.json` has `paths:`? → `@/` alias; `moduleResolution:"bundler"`? → `exports` field
- **3-Layer Architecture?** `*Router.* + *Service.* + *Repository.*` files exist in ≥2 places → Router→Service→Repository pattern
- **Test location**: global `tests/` OR co-located `__tests__/` OR side-by-side `*.test.ts`?
- **Env var parsing**: `zod` + schema exists? → validated safe parsing; `.env.example` exists?
- **Structured Logger?** Search for `pino`, `winston`, `bunyan`, `@flockr/logger` OTel fields pattern
- **Commit convention**: `.husky/commit-msg`? → conventional; `cz`/commitlint config?
- **i18n** (if any): `next-intl`, `i18next` messages dirs detected?

### Step 6 — Obvious Architectural Risks (red flags for Scrum Master)
Mark YES/NO + 1-line evidence:
| Red flag | Where to search |
|---|---|
| ⚠️ Single God package ≥1k files | 1 package contains everything |
| ⚠️ Suspicious circular imports | graphify cycle detection or deep grep `from "../"` |
| ⚠️ Raw SQL without migration | `.execute()` in `.ts` files not in migrations/ |
| ⚠️ No unit tests detected | 0 `*.test.*` files in entire project |
| ⚠️ Hardcoded secrets (HEURISTIC) | grep `sk_`, `-----BEGIN RSA`, `NEXT_PUBLIC_SECRET` — warn only, do not execute action |
| ⚠️ Hardcoded environment URLs | grep `http://prod.` / `app.<tld>` without .env |

### Step 7 — Generate registry Level 1.5 files
Writes 3 artifacts **UNDER `$CHE_PROJECT_DIR/`** (shared across worktrees):

#### 7a. `project_profile.md` — MANDATORY, 12 FIXED SECTIONS
```markdown
---
project_slug: <CHE_PROJECT_SLUG>
generated_at: <ISO8601 UTC>
xray_version: 1
worktree_root_at_scan: <ABS_PATH>
git_origin_url_at_scan: <ORIGIN_URL or "N/A local">
graphify_used: true|false
---

# Project Profile — <slug>

## 1. Repo Classification
- Structure: SINGLE-REPO | PNPM-MONOREPO | NX-MONOREPO | etc
- Number of detected apps: N
- Number of detected shared packages: N

## 2. Tech Stack (auto-detect)
| Category | Detected Tool(s) |
|---|---|
| Language | ... |
| Frontend | ... |
| (continues 10 categories above) |

## 3. Shared Packages (if monorepo — table name→purpose→relative path)
| Package | Public exports entry points | Inferred Purpose | Change Risk (1-5) |
|---|---|---|---|
| `@scope/db` | `., ./qrcode` | Entities + QR | 5 = high cross-app impact |

## 4. Canonical Folder Conventions
```
root/
├── apps/
│   ├── platform/    → Next.js RSC public + admin
│   └── scanner/     → Next.js PWA scanner
└── packages/
    ├── db/          → data layer
    └── ui/          → shared components
```

## 5. Main Entry Points
- App A: `apps/platform/src/server.ts` (port 3000, Next.js standalone)
- App B: `packages/scanner/src/pages/_app.tsx` (default export)

## 6. Detected Data Layer
- ORM/Query builder: TypeORM v0.3.x / Prisma v5 / ...
- Migrations path: `packages/db/src/migrations/*.ts`
- Primary Entities (top-5 by graph references): Order, Ticket, User, Event, Refund
- RLS (Row Level Security): Supabase enabled? YES/NO + tables

## 7. Auth & Security Model
- Strategy: NextAuth (Auth.js) v5 / Supabase Auth / Clerk / ...
- Session store: Cookie JWT | Session DB | Redis
- PII data location: tables with email, phone, address fields listed

## 8. Testing Stack (location, how to run)
- Unit test framework: Vitest (pnpm vitest run)
- E2E framework: Playwright (CI=1 pnpm test:e2e)
- Coverage: `--coverage` → minimum coverage? (if detected)

## 9. Detected CI/CD Pipeline
- Provider: GitHub Actions
- Main files: `.github/workflows/ci.yml` (build+typecheck+test), `.github/workflows/deploy.yml`
- Deploy targets: Vercel (apps: platform + scanner) / Railway / K8s

## 10. Detected Architectural Patterns
- Router → Service → Repository: YES (>=2 locations) | NO
- Composition patterns: React hooks + context providers | Compound components detected?
- Observability: Structured logger (pino + trace_id) | OTel structured logs?

## 11. Architectural Red Flags (Step 6)
| Red flag | Evidence | Suggested first contact action |
|---|---|---|
| (e.g. God package) | `packages/db` 2.3k files, everything there | Split into subpackages when touching |

## 12. Knowledge Graph Index (if graphify)
- graphify-out/GRAPH_REPORT.md exists? YES
- Top-5 Import Hubs:
  1. `@scope/db/src/index.ts` (referenced 142 times)
  2. `@scope/trpc/src/client.ts` (referenced 89 times)
  3. ...
```

#### 7b. `architecture.md` — AUTO-FILL half, leave HUMAN the rest
```markdown
# Architecture — <slug>

## ⚙️ Auto-populated by che-xray (DO NOT edit this section manually)
- Project Profile: [project_profile.md](./project_profile.md)
- Detected structure: ...
- Stack: ...
- Entry points: ...
- Data layer: ...

## 🧭 Manual Part — FILL via /che-onboarding
### General Architecture (mental map: 1 page)
### C4 Context Diagram (Level 1: external systems + this one)
### C4 Container Diagram (Level 2: apps + DB + cache + queues)
### Main Components (Level 3: cross-app modules)
### Registered Architectural Decisions (ADRs — links)
### Architectural Roadmap (planned upcoming changes)
```

#### 7c. Append line to `registry.jsonl` (audit trail)
```json
{"ts":"ISO8601","event":"XRAY_SCAN","project_slug":"...","data":{"graphify_used":true,"files_scanned":4286,"stack_version":"2026-09-01"}}
```

---

## 3. POST-SCAN: 1-PAGE SUMMARY RETURNED TO AGENT

DO NOT fill the chat with lines. Return 10 compact lines at the end:

```
[che-xray] ✅ DONE — project_flockr--Lumos (registry: ~/code/che-sessions/.registry/projects/...)
  ├─ Structure: NX-MONOREPO PNPM workspaces · 2 apps · 8 shared packages
  ├─ Stack: TS v5 + Next.js 16 (RSC) · TypeORM v0.3 · Postgres · Redis · Stripe
  ├─ Architecture: Router→Service→Repository YES (14 routers detected)
  ├─ Tests: Vitest + Playwright · 0 unit files / 14 E2E specs
  ├─ Data layer: @flockr/db packages · 38 migrations · Supabase RLS
  ├─ Auth: Auth.js v5 + cookie JWT session
  ├─ CI/CD: GitHub Actions → Vercel deploy 2 apps
  ├─ ⚠️  2 RED FLAGS: (1) @flockr/db god package 2.3k files (2) no unit tests
  ├─ Knowledge graph: graphify v0.9.53 OK (4286 files indexed)
  └─ ── Next step: now run /che-onboarding to fill in product, roadmap, manual architecture
```

---

## 4. IDEMPOTENCY + REFRESH

When rerunning `/che-xray`:
1. Reads existing `project_profile.md`, merges new findings, DOES NOT destroy human-edited section (marked "Manual Part")
2. The "⚙️ Auto-populated" section always overwrites (they are generated)
3. "🧭 Manual Part" sections are NEVER touched (only created the 1st time)
4. Provides diff of what changed since last scan: `2 new packages added, 1 framework version upgrade: Next 15→16`
5. Always appends 1 new line to `registry.jsonl` with summary diff.
