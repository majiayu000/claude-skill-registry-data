---
name: project-drift-guardian
description: >
  Specialized guardian against project drift for ndestates-io. Uses GitHub branches for work isolation, persistent database (or app DB table) for requirements tracking (e-sign features, signing flows, audit/compliance), and Grok reviews for alignment checks. Enforces pre-deploy drift scans (code, schema, container tags, scope) to avoid drift at all costs. Trigger on planning, feature dev, scope reviews, branch switches, suspected drift, CI/deploy prep, or multi-agent workflows. Integrates with .github/skills/digitalocean-app-platform-docr-deploy/SKILL.md, prod-db-maintenance, git-workflow-guardrails, model-schema-check, schema-audit-agent, eval/maintenance-task.
user-invocable: true
disable-model-invocation: false
---

# Project Drift Guardian (ndestates-io)

## Overview
Prevents scope creep, code drift, DB schema drift, infra/container drift, and deployment drift for the ndestates-io Laravel e-signature platform. Enforces branch discipline, maintains a "single source of truth" for e-sign requirements (canvas capture, multi-signer workflows, PDF embed/audit, token security, Filament admin, DDEV local + DO prod), and uses AI reviews + automated checks. Critical for "avoid drift at all costs" when hosting on DigitalOcean (droplet or App Platform) with CI deploys and DB updates.

Ties directly to ndestates-io domain: requirements around signature integrity (hashes, immutability), public magic links (roundtrips), PDF handling, auth/audit, compliance.

## Core Principles (amplified for ndestates-io + DO)
- Branch-per-feature or scoped change: Never work on main for features/deploys.
- Requirements DB (or ndestates-io DB extension) as truth: Track e-sign features (e.g., "support canvas signature + FPDI embed", "Filament resources for Documents/Signers", "safe token roundtrip", "DO App Platform deploy with DOCR", "schema drift guards on migrations").
- Continuous + pre-deploy alignment: Run on branch switch, before CI, before DB update or DO deploy. Detect code vs requirements, model vs DB schema (via model-schema-check), container image drift (tags vs prod), scope vs TODO.
- AI review: Grok for execution/creative (deploys, flows), critical analysis for drift flags. Dual if needed.
- Drift as first-class failure: Any detected drift blocks deploy/CI until remediated (new branch, scope update in DB, or explicit approval logged).
- Integration with existing: Always load cache first (.github/prompts/load-project-cache-first.prompt.md + .github/skills/cache-efficient/SKILL.md). Pair with .github/skills/git-workflow-guardrails/SKILL.md, /github-expert (for workflows), /prod-db-maintenance or DB update skill, /eval/maintenance-task (post-deploy verification), .github/prompts/model-schema-check.prompt.md + /schema-audit-agent (DB drift), /security-audit-agent (e-sign PII/audit implications).
- Avoid drift at all costs: Enforce in CI (pre-build checks), deploys (pre + post), DB updates (backup + schema check + verify + eval), planning (branch-context + this).
- Observability: Log drifts/decisions to DB or reports/. Central for audits (e-sign signatures are sensitive).

## Database / Storage for Requirements (use project's strengths)
Preferred: Extend ndestates-io's own DB (migrations for a `requirements` or `deploy_specs` table) for tight integration + audit (signatures/audit already in models).
Alternative (lightweight, like lightstone): SQLite `drift_guardian.db` in project root or .grok/ or .github/.

Core tables (adapt for ndestates-io):
- projects (id, name='ndestates-io', description='Laravel e-sign platform...', start_date, status, hosting='droplet|app-platform', do_project_id)
- requirements (id, project_id, title e.g. 'Public canvas signature roundtrip with PDF embed', description (detailed acceptance: token expiry, hash audit, FPDI fallback), priority, status (todo/in_progress/done), branch, linked_to (model/migration/workflow), created_at, updated_at)
- decisions (id, requirement_id, decision, rationale, ai_reviewer='grok' or 'drift-guardian', timestamp, deploy_blocked)
- branches (name, purpose e.g. 'feature/do-app-deploy', status, linked_requirements JSON or FKs, last_drift_check)
- drifts (id, requirement_id or scope, type='code|schema|container|infra|scope', evidence (diff or output), detected_at, resolved_at, remediation)
- deploys (id, type='droplet|app', commit, image_tag, db_migration_applied, drift_check_passed, status, timestamp)

Use the app's MySQL (via ddev-local or prod) when possible for "one DB" feel, or sqlite for the guardian. Scripts handle both.

See references/drift-analysis-prompt.md for AI prompts tailored to ndestates-io (e.g., "Does this PR preserve signature_hash immutability and token roundtrip? Any drift from Filament resources or DO deploy spec?").

## Scripts (in .github/skills.github/skills/project-drift-guardian/SKILL.md/scripts/)
- `drift-check.sh`: Runs git diff vs main, php artisan model:show or schema checks (integrate model-schema-check), docker inspect for image tags vs expected, DB query for pending requirements. Outputs JSON or report. Calls drift-analysis.
- `db_ops.sh`: Init, query requirements, log decision/drift, backup before changes.
- `init_db.sql` or migration: For sqlite or ndestates-io DB extension.
- Integrate with existing: Before any DB update call prod-db-maintenance + this; before DO deploy run this + github-expert checks.

(Adapt/copy from lightstone equivalents; make ndestates-io specific e.g. check for signature tables, FPDI presence, DOCR image labels.)

## Tools & Integration (ndestates-io specific)
- Git + GitHub (via tools or gh): branch/PR, checks in CI.
- `ddev exec` for local schema/model checks (per ddev-local-runtime).
- doctl for DO (droplet create/list, app deploy, registry).
- Load alongside: branch-context-agent, github-expert, prod-db-maintenance (or new db skill), git-workflow-guardrails, eval/maintenance-task, security-audit-agent (for e-sign data).
- CI: GitHub Actions must call this (or equivalent checks) as required step before build/deploy/DB migrate.
- For deploys: This skill generates "pre-deploy drift report" as gate.

## Procedures

### Initialize (for ndestates-io)
```bash
# Prefer extending ndestates-io DB; fallback sqlite
# php artisan migrate --path=database/migrations/xxxx_add_drift_requirements.php (create if needed)
# or
sqlite3 .grok/drift_guardian.db < .github/skills.github/skills/project-drift-guardian/SKILL.md/scripts/init_db.sql

# Seed initial ndestates-io requirements (examples):
# - e-sign core: canvas capture, multi-signer ordered requests, PDF embed (FPDI + dompdf fallback), signature_hash + ip/ua audit, token roundtrips (magic links)
# - Hosting: support DigitalOcean droplet (nginx/php-fpm or Docker) AND App Platform (DOCR container, auto-deploy)
# - CI: GitHub Actions with tests, model-schema-check, drift-guardian, hardened build, DOCR push, App deploy or droplet rollout, safe DB migrate (with prod-db-maintenance)
# - DB: safe updates/migrations with pre-checks, backups, post-verify (row counts, signature integrity samples), no drift in schema vs models
# - Drift: block on scope creep, unapproved DB changes, image tag drift, code vs requirements mismatch
```

### Pre-Work / Branch Check (always)
```bash
git checkout -b feature/do-app-deploy-ndestates-io  # or droplet
# Run drift guardian
./.github/skills.github/skills/project-drift-guardian/SKILL.md/scripts/drift-check.sh --branch $(git branch --show-current) --scope "e-sign roundtrip + DO deploy + DB update"
# Review output + update DB with new requirement/decision
```

### Drift Detection (code, schema, container, deploy, scope)
- Code/scope: git diff main, compare to requirements DB (e.g. "does this change touch signing without updating audit hash?").
- Schema/DB: Run model-schema-check + schema-audit-agent + compare migrations vs current prod (via doctl or dump). Flag if model changes without migration or vice versa.
- Container/infra: In CI, inspect built image tags/labels vs "production-latest" or pinned; check DO App spec or droplet config drift (via doctl apps get or droplet list).
- Deploy/DB: Before any prod change, full report. Post-deploy: re-run + eval-maintenance-task.
- AI prompt (via this skill or drift-analysis): "Given ndestates-io requirements [list from DB: canvas, embed, tokens, DO hosting paths, no-drift policy], analyze this diff/PR/deploy plan. Flag any drift with evidence and severity. Suggest remediation."

If drift: flag, do not proceed to CI/deploy/DB until fixed or explicitly approved + logged.

### CI / Deploy Flow (with this guardian as gate)
1. PR or main push: GitHub Action runs tests + .github/prompts/model-schema-check.prompt.md equivalent + this drift-check (script or simulated via prompt) + security-audit.
2. If pass + approved: build hardened container (per digitalocean skill), push to DOCR (or Docker for droplet).
3. DB update (if migrations): Call prod-db-maintenance (or safe-db skill) with backup first, pre-schema check, post-verify (sample signature data, counts), then .github/skills/eval/maintenance-task/SKILL.md.
4. Deploy:
   - App Platform: doctl apps deploy or GitHub integration with DOCR + floating or pinned tag. Guardian confirms no container drift.
   - Droplet: doctl compute or SSH/Docker compose pull/restart (prefer no-ssh patterns from other projects). Guardian confirms droplet config vs expected.
5. Post: Run full drift report + eval + update requirements DB with "delivered".
6. This skill + guardrails enforce the "no drift" policy.

See the enhanced digitalocean skill (or create .github/workflows/deploy-ndestates-io.yml) for exact yaml that calls these checks.

### Remediation
- Out of scope (e.g., new e-sign feature during deploy work): New branch, log in DB via this skill.
- Schema drift detected: Revert or create dedicated migration + re-check.
- Container tag drift: Pin + rebuild.
- Log decision with AI rationale (this skill can generate the report).

### Reports
- Generate alignment/drift report (use references/alignment-report-template.md adapted for ndestates-io: sections for signing integrity, DO hosting (droplet vs app), DB safety, CI compliance).
- Useful for stakeholders, audits (e-sign data handling), or before major deploys.

## Activation / When to Use
- Project planning or new feature (e-sign or hosting).
- Branch switch or before coding.
- Suspected drift (e.g., after manual DB change or direct droplet edit).
- Pre-CI, pre-deploy, pre-DB update (mandatory gate).
- Post-deploy verification.
- Multi-agent (Grok + others) workflows.
- Scope reviews or release prep.

Always combine with load cache first, branch-context-agent, github-expert (for workflows), git-workflow-guardrails (before any push/deploy), and the digitalocean/deploy skill.

## ndestates-io Specific Extensions
- Requirements must cover: public unauthenticated roundtrips, canvas + embed (FPDI/dompdf), signature immutability/audit (hash + fields), token security, Filament for admin (Documents, Signers, Requests), DDEV local parity, DO hosting (droplet full control vs App managed + DOCR), safe DB (migrations + prod-db-maintenance + no data loss for signatures).
- Drift checks must include: model vs migration (model-schema-check), prod DB schema vs local, container image vs deployed (for both droplet Docker and App), code changes vs "no drift on audit/compliance".
- Tie DB for guardian to ndestates-io's signing tables where possible (reuse audit patterns).
- For DO: this skill reviews droplet provisioning (e.g. doctl compute droplet create with user-data for php/nginx or docker) or App spec (no broad DBaaS tokens), CI steps, and post-deploy state.

## Monitoring / After Load Confirm
After activation or checks: emit something like `DriftGuardian: ndestates-io | Branch: feature/... | Requirements checked: 12/14 | Drifts: 0 (or list) | Pre-deploy gate: PASS | Cache: loaded`.

Update TODO, requirements DB, and run .github/skills/eval/maintenance-task/SKILL.md or equivalent after any remediation/deploy.

## References
- lightstone original for base structure/scripts/prompts (adapted here).
- ndestates-io docs/codebase/ (CONCERNS for drift risks, ARCHITECTURE for flows).
- .github/workflows/ (to be created per digitalocean skill).
- prod-db-maintenance, model-schema-check, git-workflow-guardrails, security-audit-agent.
- DO docs: App Platform, DOCR, doctl for droplets/apps/registry.

This skill makes "avoid drift at all costs" operational for ndestates-io's DO hosting journey. Run it early and often.