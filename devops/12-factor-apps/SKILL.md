---
name: 12-factor-apps
description: Perform 12-Factor App compliance analysis on any codebase. Use when evaluating app architecture or cloud-native readiness against the original Twelve-Factor methodology.
---

# 12-Factor App Compliance (Concise Checklist)
Reference: https://12factor.net

## How to Use
1) Identify app root. 2) For each factor, scan quickly (grep/find) and decide Strong/Partial/Weak. 3) Write 2–3 concrete remediation steps for any Weak items.

## Factors & Fast Checks

**I. Codebase** – One repo, many deploys
- Check: single VCS root; no env-specific branches.
- Anti: multiple repos per app, duplicated code, prod/dev forks.

**II. Dependencies** – Explicit, isolated
- Check: lockfiles (`package-lock.json`, `poetry.lock`, `requirements.txt`), no implicit globals.
- Anti: system packages assumed, `pip install .` without lock, vendored libs committed.

**III. Config** – In env vars
- Check: secrets/URLs in env, not in code; `.env.example` or README.
- Anti: committed secrets, per-env config files baked into image, branching on NODE_ENV in code for secrets.

**IV. Backing Services** – Treat as attached resources
- Check: URLs/DSNs injected; easy to swap (e.g., Postgres -> RDS) without code change.
- Anti: hardcoded hostnames, local-only assumptions, service-specific branches.

**V. Build/Release/Run** – Strict separation
- Check: CI/CD produces immutable artifacts; config injected at release; run is stateless.
- Anti: editing images on servers, mutable releases, config baked into build.

**VI. Processes** – Stateless, share-nothing
- Check: no writing to local disk for shared state; uses backing services for session/cache.
- Anti: session on local FS, sticky sessions required, stateful workers.

**VII. Port Binding** – Self-contained service
- Check: service exposes HTTP/ports directly; no reliance on injected runtime container.
- Anti: requires being run under specific app server without config, no explicit port binding.

**VIII. Concurrency** – Scale via process model
- Check: process types defined (web/worker); horizontal scaling documented.
- Anti: single long-running process doing everything; no clear worker types.

**IX. Disposability** – Fast start/stop, graceful shutdown
- Check: start <~60s; handles SIGTERM/SIGINT; idempotent jobs.
- Anti: slow boot, ignores signals, long-running jobs without checkpoints.

**X. Dev/Prod Parity** – Keep gaps small
- Check: similar backing services (DB type/versions); infra as code; same build tooling.
- Anti: SQLite locally vs Postgres prod, manual prod setup, long-lived feature branches.

**XI. Logs** – Treat as event streams
- Check: stdout/stderr logging; structured when possible; external aggregation.
- Anti: writes to local files, log rotation on host, missing log levels.

**XII. Admin Processes** – Run as one-off tasks
- Check: migrations/maintenance run in same env/image via one-off process.
- Anti: manual shell on servers, divergent tooling for admin tasks.

## Scoring Template
- Strong: clear evidence of practice; no high-risk anti-patterns.
- Partial: practice present with gaps; list 2 fixes.
- Weak: practice absent or violated; list top 3 fixes + owners.

## Report Skeleton
- Summary: overall parity, top 3 risks, recommended next actions.
- Per factor: Strong/Partial/Weak, evidence, specific remediations, owners/dates.

## Quick Commands (examples)
- Find secrets in repo: `rg "(AKIA|secret|password|connectionString)"`
- Find env usage: `rg 'process.env|os.environ'`
- Check lockfiles: `find . -maxdepth 2 -name "*lock*" -o -name "poetry.lock" -o -name "requirements.txt"`
- Check signal handling (Go/Node/Python): look for `signal.Notify`, `process.on('SIGTERM')`, `signal.signal`.
