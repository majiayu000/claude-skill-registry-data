---
name: app-production-readiness
description: Build portable apps (any stack - TypeScript, Python, Go, Rust) for localhost, Docker, Vercel, Netlify, Railway, Render, Fly.io, Cloudflare Free plan, then run an adaptive 21-gate production-readiness review - cross-browser visual QA, bundle budgets, performance, a measured design-polish rubric, desktop Lighthouse, security + dependency-CVE scan, WCAG 2.1 AA audit, live SEO/header/health checks, tests, reliability, production-grade README with real screenshots, observability, free-tier cost check, business rules (executable contract + domain sign-off), load/soak, migrations, privacy/GDPR (policy + legal sign-off), i18n/RTL, screen-reader contract, payment/email flows, code quality, and an adversarial re-verification of every claimed PASS. A scoping step decides which gates actually apply to the app in front of you (no migration gate for a static site, no payment gate for an API service). One command runs the whole review - `python scripts/review.py --root <app> --serve` starts the app, measures it, judges every gate adversarially and writes qa/report.md; `--fix` writes the safe mechanical fixes first, and a framework-profile layer knows what Next.js/Remix/Astro/Nuxt/SvelteKit inject by default, so a framework default is never reported as an app defect. Absorbs the frontend-design, mobile-design, i18n-localization, api-patterns, database-design, seo/geo-fundamentals, lint-and-validate, nextjs-react-expert, review-team and security-audit skills so you do not need them separately. Works on any single app or across every app in a workspace. Use when asked to make an app portable, deploy free anywhere, check design match, optimize speed, polish UI, run Lighthouse audit, review for production readiness, write a professional README, capture app screenshots, prep a release, or audit all apps in a repo.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
category: devops-docker-cicd
---

# Portable Deploy + QA (Production Readiness)

> Build once, run anywhere free. Then prove it: looks right everywhere, loads fast, feels polished, audits green — and every claimed PASS is re-derived from evidence.

## 0. Quick Start & Bootstrap

Verify environment tooling before running audits:
```bash
python scripts/bootstrap_env.py              # Health-check Node, Python, Playwright, Lighthouse
python scripts/bootstrap_env.py --install    # Auto-install missing browsers / dependencies
```

Run one-command review (starts app, auto-fixes mechanical issues, evaluates scoped gates, writes `qa/report.md`):
```bash
python scripts/review.py --root <app_root> --serve --fix
```

## 1. App Inputs & Agnostic Guarantees

Resolve dynamic inputs from arguments, environment, or codebase (never assume port 3000):

| Input | How to detect | Default |
|-------|---------------|---------|
| `APP_URL` | `$ARGUMENTS` → `APP_URL` env → `package.json` → framework configs → ask user | `http://localhost:3000` |
| `PORT` | Parse from `APP_URL`, `PORT` env, `Dockerfile EXPOSE`, or `fly.toml` | `3000` |
| `PKG` | `pnpm-lock.yaml`→pnpm, `bun.lockb`→bun, `yarn.lock`→yarn, else npm | `npm` |
| `ROUTES` | Crawl `/` links + framework routes dir (`app/`, `pages/`, `src/routes/`) | `/` + 2 key routes |
| `HEALTHZ` | `src/**/health*`, `/api/health`, else `/` status 200 | `/healthz` or `/` |

Auto-detect via stdlib script:
```bash
python scripts/detect_env.py <root>
```

App-agnostic rules: Accept any project root (JS/TS, Python, Go, Rust, static), detect without guessing, support CLI overrides, and never alter apps outside declared scope.

## 2. Portable Build & Deploy Platform Matrix

See [deploy-matrix.md](references/deploy-matrix.md) and [free-tier-limits.md](references/free-tier-limits.md).
- **Targets**: localhost, Docker, Vercel/Netlify, Railway/Render/Fly, Cloudflare Pages/Workers.
- **Rules**: Env-driven (`process.env.*`, `os.environ`), `.env.example` verified, Cloudflare behind flags, no paid-only SDKs.
- **README Standards**: See [readme-standard.md](references/readme-standard.md) and template [assets/README.template.md](assets/README.template.md). Verify with `python scripts/check_readme.py <root>`.

## 3. The 21 Quality Gates

Not all apps have every surface. Gate scoping classifies gates into `applies`, `conditional`, or `not_applicable` from codebase evidence:
```bash
python scripts/gate_scope.py --root <app_root>
```
See checklists: visual + performance in [qa-checklists.md](references/qa-checklists.md), hardening in [hardening-checklists.md](references/hardening-checklists.md), and depth in [depth-gates.md](references/depth-gates.md).

### Gate A — Cross-browser visual QA
Check Chrome, Edge, Firefox, Safari (WebKit) at 1280/1440/1920 + 360/390 across default, hover, active, focus, disabled, loading, empty, and error states.
**Proof**: `python scripts/capture_screenshots.py --root <root> --url <APP_URL> --routes /,/a --out docs/screenshots --browsers chromium,firefox,webkit` → PNGs + `docs/screenshots/manifest.json`.

### Gate B — Performance / low resource
Code-split routes, tree-shake, WebP/AVIF, minify, cache headers. JS budget <= 200 kB gzipped per route, dep <= 50 kB. CWV: LCP <= 2.5s, CLS <= 0.1, INP <= 200ms.
**Proof**: `python scripts/bundle_report.py <root>` → per-route gzip budgets, asset sizes, source map checks.

### Gate C — Design polish (measured rubric + human sign-off)
Consistent hierarchy, spacing rhythm, 44px touch targets, 150-250ms transitions, 45-75 char lines, reduced-motion. Rubric score >= 0.85.
**Proof**: `python scripts/design_polish.py --root <root>` and stored sign-off `python scripts/design_polish.py --root <root> --record-signoff --reviewer "<name>" --verdict approved` → writes `qa/signoff/design.json`.

### Gate D — Desktop Lighthouse audit
Incognito desktop preset on key routes. Targets: Perf >= 90, A11y >= 95, BP >= 95, SEO >= 90. Fallback uses absorbed `lighthouse_audit.py`. CI config: [lighthouse-ci.md](references/lighthouse-ci.md).
**Proof**: `python scripts/lighthouse_run.py --url <APP_URL> --routes /,/a --out qa/lighthouse` → `qa/lighthouse/lighthouse-summary.json`.

### Gate E — Security
Zero HIGH vulnerabilities. Independent scanners run own rules + absorbed `vulnerability_security_scan.py`. Dependency audit via `dep_audit.py`. Deep mode playbooks in [security/](references/security/README.md).
**Proof**: `python scripts/security_scan.py <root>` and `python scripts/dep_audit.py <root>` (deep mode: `python scripts/security_audit.py --root <root>`).

### Gate F — Accessibility (WCAG 2.1 AA)
axe-core zero critical/serious issues + keyboard-only traversal, focus visibility, logical tab order, contrast >= 4.5:1.
**Proof**: `python scripts/a11y_audit.py --url <APP_URL> --routes /,/a --browsers chromium,firefox,webkit` → `qa/a11y/a11y-report.json`.

### Gate G — SEO & metadata
Unique title + meta description per page, Open Graph/Twitter tags, canonical URL, robots.txt, sitemap.xml, semantic HTML, lang attribute, 404 handling.
**Proof**: `python scripts/runtime_check.py --url <APP_URL> --routes /,/a --healthz <HEALTHZ>` and `python scripts/seo_static.py --root <root>`.

### Gate H — Tests & correctness
Unit tests for business logic, integration for APIs. Project test script passes, no `.only` or skipped tests.
**Proof**: `python scripts/preflight.py <root>` checks for skipped tests, and `scripts/absorbed/test_runner.py` detects and runs test runner.

### Gate I — Reliability & error handling
Route-level error boundaries, try/catch with timeouts, no unhandled rejections, loading/empty/error UI. Deep mode boots app with platform runner.
**Proof**: `python scripts/runtime_check.py` validates healthz and 404s; deep mode `python scripts/deploy_smoke.py --root <root>` confirms platform boot → `qa/deploy-smoke.json`.

### Gate J — Docs & DX
README matches standard ([readme-standard.md](references/readme-standard.md)), `.env.example` synced, CONTRIBUTING and LICENSE present.
**Proof**: `python scripts/check_readme.py <root>` and `python scripts/preflight.py <root>`.

### Gate K — Observability
Structured JSON logging in production, request/correlation IDs, error tracking hook, health check endpoint.
**Proof**: `python scripts/verify_claims.py` validates >= 3 independent source signals for observability.

### Gate L — Free-tier cost check
Verify every service used has a free plan; document fallback behaviors when limits are reached.
**Proof**: README contains free-tier limits table verified against [free-tier-limits.md](references/free-tier-limits.md).

### Gate M — README & screenshots (delivery gate)
Production README with >= 3 real screenshots, generated contact sheet, resolved image paths, and manifest.
**Proof**: `python scripts/check_readme.py <root>` and `docs/screenshots/manifest.json`.

### Gate N — Business rules (executable contract + domain sign-off)
Execute business rule scenarios (`qa/scenarios.json`) against live app, paired with fingerprint-bound domain sign-off (`qa/signoff/business-rules.json`).
**Proof**: `python scripts/business_logic_check.py --root <root> --url <APP_URL>` and `python scripts/signoff.py`.

### Gate O — Load & soak
p95 <= 1000ms, error rate <= 1%, soak time-series drift <= 50% between first and last third of run.
**Proof**: `python scripts/load_check.py --url <APP_URL> --routes /,/a --duration 10 --soak 60 --soak-interval 10` → `qa/load.json`.

### Gate P — Migrations & schema
Rollback paths defined, destructive DDL guarded, idempotency verified.
**Proof**: `python scripts/migration_check.py --root <root>` (deep mode: `python scripts/migration_apply.py --root <root>` applies and rolls back chain) → `qa/migrations.json`.

### Gate Q — Privacy & GDPR (policy + legal sign-off)
Privacy policy reachable and linked, consent before tracking, no PII in logs/storage/analytics, fingerprinted legal sign-off.
**Proof**: `python scripts/privacy_check.py --root <root> --url <APP_URL>` → `qa/signoff/privacy.json`.

### Gate R — i18n & RTL
Catalogs with matching translation keys, declared doc language, RTL dir switching and logical CSS properties.
**Proof**: `python scripts/i18n_check.py --root <root>`.

### Gate S — Assistive technology contract
Screen-reader contract: programmatic labels, aria-live regions for async updates, landmark roles, skip links.
**Proof**: `python scripts/at_check.py --root <root>`.

### Gate T — Payment & email flows
No raw card data in code, webhook signatures verified, integer minor currency units, email providers without header injection.
**Proof**: `python scripts/payment_email_check.py --root <root>` (deep mode: `python scripts/payment_email_live.py --root <root>`).

### Gate U — Code quality & AI-risk debt
Complexity thresholds, no duplicate blocks, no dead markers (TODO/FIXME/mock), clean type coverage, React performance patterns.
**Proof**: `python scripts/code_quality.py --root <root>`.

---

### Panel review
Run reviewer prompts in [panel-review/](references/panel-review/README.md) across correctness, security, architecture, UX, and reliability.

## 4. Tooling & Automation

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/review.py` | Complete orchestrator: scope → fix → measure → judge → `qa/report.md` | `python scripts/review.py --root <root> --serve [--fix] [--json]` |
| `scripts/bootstrap_env.py` | Environment dependency checker and installer (Playwright, browsers, Lighthouse) | `python scripts/bootstrap_env.py [--install] [--json]` |
| `scripts/serve.py` | Starts app for review using production or dev runner | `python scripts/serve.py --root <root> [--dev] [--wait]` |
| `scripts/fixes.py` | Safe auto-fixes: `.env.example`, `.dockerignore`, `robots.txt`, LICENSE, Next headers | `python scripts/fixes.py --root <root> [--only env-example,dockerignore]` |
| `scripts/framework_profiles.py` | Profile layer preventing framework defaults from being marked as defects | `python scripts/framework_profiles.py <root>` |
| `scripts/gate_scope.py` | Scopes the 21 gates to the codebase in front of you | `python scripts/gate_scope.py --root <root>` |
| `scripts/detect_env.py` | Detects port, URL, package manager, framework, routes, healthz | `python scripts/detect_env.py <root>` |
| `scripts/preflight.py` | Production-readiness checks (**30 checks** with framework scoping) | `python scripts/preflight.py <root>` |
| `scripts/security_scan.py` | Secrets and insecure patterns scanner | `python scripts/security_scan.py <root>` |
| `scripts/security_audit.py` | Deep security audit ledger and finding validator | `python scripts/security_audit.py --root <root>` |
| `scripts/dep_audit.py` | Dependency vulnerability audit for npm, pip, cargo, go | `python scripts/dep_audit.py <root>` |
| `scripts/bundle_report.py` | Bundle budgets, asset sizes, source map checks | `python scripts/bundle_report.py <root>` |
| `scripts/deploy_verify.py` | Target verification for Docker, Vercel, Netlify, Fly, Render, Cloudflare | `python scripts/deploy_verify.py <root>` |
| `scripts/deploy_smoke.py` | Boots app with platform runner and probes healthz | `python scripts/deploy_smoke.py --root <root>` |
| `scripts/runtime_check.py` | Live HTTP probe for headers, health, SEO metadata, 404 behavior | `python scripts/runtime_check.py --url <APP_URL> --routes /,/a` |
| `scripts/seo_static.py` | Static SEO checks + Generative Engine Optimization (GEO) scoring | `python scripts/seo_static.py --root <root>` |
| `scripts/a11y_audit.py` | Multi-engine axe-core (WCAG 2.1 AA) + keyboard navigation audit | `python scripts/a11y_audit.py --url <APP_URL> --routes /,/a` |
| `scripts/lighthouse_run.py` | Desktop Lighthouse runner with threshold enforcement | `python scripts/lighthouse_run.py --url <APP_URL> --routes /,/a` |
| `scripts/capture_screenshots.py`| Multi-engine Playwright screenshot capture + contact sheet | `python scripts/capture_screenshots.py --root <root> --url <APP_URL> --routes /,/a` |
| `scripts/check_readme.py` | Validates README structure, env table, and screenshot assets | `python scripts/check_readme.py <root>` |
| `scripts/design_polish.py` | Rubric evaluation for typography, color, spacing rhythm, layout | `python scripts/design_polish.py --root <root>` |
| `scripts/business_logic_check.py`| Executes scenario tests and verifies API contracts | `python scripts/business_logic_check.py --root <root> --url <APP_URL>` |
| `scripts/load_check.py` | Concurrency load and soak drift time-series measurement | `python scripts/load_check.py --url <APP_URL> --soak 60` |
| `scripts/migration_check.py` | Rollback, idempotency, and destructive DDL analyzer | `python scripts/migration_check.py --root <root>` |
| `scripts/migration_apply.py` | Deep migration tester: applies, rolls back, and reapplies on scratch DB | `python scripts/migration_apply.py --root <root>` |
| `scripts/privacy_check.py` | Analyzes privacy policy, consent gates, and PII storage | `python scripts/privacy_check.py --root <root> --url <APP_URL>` |
| `scripts/i18n_check.py` | Locale key matching and RTL styling verification | `python scripts/i18n_check.py --root <root>` |
| `scripts/at_check.py` | Screen-reader accessible name, live region, and landmark checks | `python scripts/at_check.py --root <root>` |
| `scripts/payment_email_check.py` | Card security, webhook validation, and mail safety analyzer | `python scripts/payment_email_check.py --root <root>` |
| `scripts/payment_email_live.py` | Test-mode payment intent and transactional email round-trip | `python scripts/payment_email_live.py --root <root>` |
| `scripts/code_quality.py` | Code complexity, duplication, and AI debt detector | `python scripts/code_quality.py --root <root>` |
| `scripts/mobile_check.py` | Viewport, 44px touch targets, and hover traps audit | `python scripts/mobile_check.py --root <root>` |
| `scripts/flow_test.py` | Playwright E2E journey flow runner (`qa/flows.json`) | `python scripts/flow_test.py --root <root> --url <APP_URL>` |
| `scripts/verify_claims.py` | Adversarially re-derives claimed PASSes from disk evidence | `python scripts/verify_claims.py --root <root> --claims qa/claims.json` |
| `scripts/scan_workspace.py` | Workspace discovery scanning for multi-app repositories | `python scripts/scan_workspace.py <workspace>` |
| `scripts/qa_common.py` | Core CLI parsing, file scoping, subprocess, and format helpers | imported |
| `scripts/qa_ext.py` | Extensions for HTTP clients and gate runners | imported |
| `scripts/schema_validate.py` | Schema validators for findings and coverage ledgers | imported |
| `scripts/signoff.py` | Fingerprint-bound human sign-off manager (Gates C, N, Q) | imported / CLI |
| `scripts/skill_check.py` | Health-check for skill packaging, scripts, and links | `python scripts/skill_check.py --root .` |
| `scripts/remediate.py` | Autonomous remediation engine: codemods + atomic rollback + recipes | `python scripts/remediate.py --root <root> [--dry-run]` |
| `scripts/remediation_handlers.py` | Codemods for XSS innerHTML, CORS, touch targets, focus visible, empty catch | imported by remediate.py |
| `scripts/web_guidelines.py` | Web Interface Guidelines machine checker | `python scripts/web_guidelines.py --root <root>` |
| `scripts/absorbed_rules.py` | Rules from absorbed doc skills | imported |
| `scripts/fixtures/make_sample_app.py` | Fixture generator for good/broken apps | `python scripts/fixtures/make_sample_app.py` |
| `scripts/absorbed/verify_manifest.py` | Hash integrity verifier for absorbed sibling tools | `python scripts/absorbed/verify_manifest.py` |

### Exit-code contract
- `0`: Checked and passed.
- `1`: Checked and failed.
- `2`: **SKIPPED** — required tool or evidence was unavailable. A skipped gate is **never a pass**.

Tool failures (unreachable server, failed test runner) report `UNSUPPORTED` (Exit 2, SKIPPED), not app defects.
Evidence artifacts must reside in the target project (`<app>/qa/...`). To point to an external directory, use `--artifact-dir <dir>`.
Unverified sign-offs are marked `UNVERIFIABLE`.

### Self-Tests

Execute test suites:
```bash
python -m pytest scripts/test_advanced.py -q       # 76 tests
python -m pytest scripts/test_gates_extended.py -q # 45 tests
python -m pytest scripts/test_qa_scripts.py -q     # 49 tests
python -m pytest scripts/test_absorbed.py -q       # 23 tests
python -m pytest scripts/test_scope.py -q          # 22 tests
python -m pytest scripts/test_phase6.py -q        # 35 tests
python -m pytest scripts/test_signoff.py -q        # 27 tests
python -m pytest scripts/test_frameworks.py -q     # 33 tests
python -m pytest scripts/test_measurement_failures.py -q # 11 tests
python -m pytest scripts/test_absorption.py -q      # 16 tests
python -m pytest scripts/test_docs.py -q           # doc-consistency
python scripts/test_preflight.py                   # secret-heuristic self-test
```
Total: **346 tests**.

## 5. End-to-End Workflow

```
1. BOOTSTRAP -> scripts/bootstrap_env.py => verify local Playwright/Lighthouse
2. SCOPE     -> scripts/gate_scope.py   => identify applicable gates
3. AUTO-FIX  -> scripts/fixes.py        => apply safe mechanical fixes
4. SERVE     -> scripts/serve.py        => boot app
5. MEASURE   -> capture screenshots, bundle budgets, a11y, lighthouse, security
6. SIGN-OFF  -> store human sign-offs for visual polish, business rules, privacy
7. JUDGE     -> verify_claims.py        => re-derive all claims adversarially
8. REPORT    -> emit qa/report.md
```
Details: [deep-modes.md](references/deep-modes.md) and [verification.md](references/verification.md).
For workspace reviews: [workspace-review.md](references/workspace-review.md).

## 6. Multi-App / Workspace Mode

Discover apps and review each independently without cross-app assumption leaks:
```bash
python scripts/scan_workspace.py <workspace>
```

## 7. Final Report Format

```
APP        : <name> @ <APP_URL> (<framework>, <PKG>)
DETECTED   : port=<PORT> healthz=<HEALTHZ> routes=<ROUTES>
SCOPE      : applies=<list of gates> | conditional=<list> | skipped=<list>
GATES      : A visual PASS | B perf PASS | C polish PASS (human) | D lighthouse PASS (Perf 96)
             E security PASS | F a11y PASS | G seo PASS | H tests PASS
             I reliability PASS | J docs PASS | K observability PASS | L cost PASS
             M readme+shots PASS (3 shots, contact sheet)
             N logic PASS | O load PASS | P migrations PASS | Q privacy PASS
             R i18n PASS | S screen-reader PASS | T payments PASS | U quality PASS
EVIDENCE   : qa/lighthouse/lighthouse-summary.json, qa/a11y/a11y-report.json,
             docs/screenshots/manifest.json, qa/security/findings.json
SKIPPED    : <gate + reason, or none>
BLOCKERS   : <list or none>
FIXED      : <list>
ARTIFACTS  : docs/screenshots/, qa/lighthouse/*.html, qa/a11y/a11y-report.json, qa/report.md
```

## Related Skills & Absorbed Tools

Absorbs tools and playbooks from: `frontend-design`, `mobile-design`, `i18n-localization`, `api-patterns`, `database-design`, `seo-fundamentals`, `geo-fundamentals`, `lint-and-validate`, `nextjs-react-expert`, `performance-profiling`, `testing-patterns`, `vulnerability-scanner`, `security-audit` (in `scripts/security_audit_pack/`), `review-team`, `web-design-guidelines` (in [web-interface-guidelines.md](references/web-interface-guidelines.md)), `api-contract-testing`, `security-hardened-api`, `observability-and-instrumentation`, `microservices-resilience`, `ai-debt-detector`, `property-based-testing`, and `mutation-testing` (in `references/knowledge/`).
