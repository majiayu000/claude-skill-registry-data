---
name: prod-db-maintenance
description: >
  Skill for invoking import or update of the production database as Stage 6 infrastructure (operating system).
  Treats DB maintenance as a first-class "agent slot" task: spec-driven, heavily cache-backed, followed by .github/skills/eval/maintenance-task/SKILL.md, with observability.
  Maximizes shared context (docs/codebase, TODO, previous evals, architecture, mysql expert) to avoid "ten things" and ensure clean prod state.
  Use for full clean import from latest local backup (for dirty prod reset) or updates (e.g. via daily listings job + verification).
  Always run from host (not ddev exec for doctl/mysql to prod). Sources .env for DO_APP_ID, TARGET_*, etc.
user-invocable: true
disable-model-instruction: false
---

# Prod DB Maintenance (Stage 6: Operating System)

**Primary source**: https://upsun.com/blog/8-stages-ai-engineering-maturity/ (Stage 6: shared context as real infrastructure; agent slots; humans as supervisors verifying via evals; recurring tasks as first-class with central logs).

**Stage 6 context for this skill**:
- DB import/update is no longer ad-hoc "babysitting" (Stage 7) or manual steps.
- It is infrastructure: an agent slot task that can be "scheduled" or invoked, with defined spec (clean state = specific row counts/freshness from cache), TDD-like verification via .github/skills/eval/maintenance-task/SKILL.md, cost/observability (note doctl/mysql calls), and standards living in the system (this skill + evals + .env + scripts).
- Human role: supervisor — review the one-liner, run it, invoke eval, confirm report, escalate if FAIL.
- Parallel to other maintenance (registry via cleanup script + eval).
- Ties to production path: clean DB data state is prerequisite for reliable deploys, daily jobs (live listings), and overall readiness. Amplifies our good practices (DDEV for local prep, env sourcing, safer non-interactive, security/governance).

**Mandatory start (ALWAYS load cache first — maximizes shared context per Stage 4/6)**:
1. Invoke `.github/prompts/load-project-cache-first.prompt.md` (or equivalent: load `docs/codebase/`, TODO carry, `.copilot/memories/INDEX.md`, CONCERNS.md, previous evals like registry-cleanup reports).
2. Cross-reference `.github/skills/ai-engineering-maturity/SKILL.md` for current stage assessment (typically 4-5, advancing to 6 via this).
3. Load relevant docs: ARCHITECTURE.md (DB models), INTEGRATIONS.md (DO DBaaS), mysql-database-expert skill, previous TODOs on DB import/DBaaS, doctl_scripts (connect, import_backup, the wrapper).
4. Current branch context (via branch-context-agent if needed) and "production ease" items from TODO.
5. This ensures the "import or update" is not from vague memory but from full project memory (what "clean" means, last known state, priorities).

**When to invoke**:
- For **full clean import** (reset dirty prod DB to latest backup state — your local `backup/latest-ndestates-io-db.sql.gz`).
- For **update** (e.g., after local DDEV ingest of new open-data, export fresh dump, then import; or incremental via daily listings job + targeted updates).
- Post any prod DB change, before promoting code or daily jobs.
- In daily-standup-with-cache when tracking production path (combine with registry eval).
- As "agent slot" task: specify the task in a prompt, this skill generates the exact one-liner, you run it (or agent in future sandbox), then call `.github/skills/eval/maintenance-task/SKILL.md db-import`.

**Core principles (amplify good practices, Stage 4+ prerequisites)**:
- Shared context over drift: Never ad-hoc; always cache-first. Update shared assets (e.g., TODO with post-import state, this skill with new checks).
- Security & governance before scale (Stage 4): All access via doctl_scripts or .env (TARGET_DB_*, DO_DB_CLUSTER_ID, CA cert). Never hardcode. This skill triggers full security checklist + MCP threat scan if extended (e.g., new agent invocation).
- Spec/context first (Stage 5): The "spec" is the expected clean state from cache (row counts, MAX dates, last_seen_at from TODO/runbooks). Vague "update DB" is invalid input — always reference specific backup or ingest.
- Risk-based review + evals as gates (Stage 5/8): After execution, ALWAYS invoke `.github/skills/eval/maintenance-task/SKILL.md db-import` (or with --apply-run=true). Status must be PASS before considering "done". Reports logged to .tmp/ for audit (central "log" per Stage 8).
- Don't skip stages: This assumes Stage 4+ foundations (env, safer scripts, cache). For Stage 7/8: move from local one-liner to scheduled agent job with this skill + eval as gate.
- AI as amplifier: Our DDEV (for local prep/ingest), test-safety, recovery-first, TODO discipline are amplified. Sloppy (e.g., no CA, wrong TARGET) will fail fast via eval.
- Cost & observability (Stage 6): Note doctl/mysql calls, token/ time if any Grok involvement, and observability (the eval report as "trace").
- Center of gravity: Use this to advance from Stage 5 (one-liners) to 6 (agent slots + shared infra).

**How to invoke (one-liner friendly, cache-maximized)**:
1. Start session with `.github/prompts/load-project-cache-first.prompt.md` + `.github/prompts/daily-standup-with-cache.prompt.md` (include maturity + production path items).
2. Invoke this skill (or directly in prompt): `/prod-db-maintenance --mode=full-import` (or `--mode=update --source=local-ingest`).
3. The skill will:
   - Confirm cache loaded (reference specific docs/TODO/evals for expected state).
   - Output the exact command (one-liner or script).
   - Note: Run from host (for doctl access to prod cluster). Use real creds (export or in .env — never commit).
   - After run: "Next: .github/skills/eval/maintenance-task/SKILL.md db-import [--apply-run=true]".
4. Execute the command.
5. Invoke the eval for verification.
6. Log the eval report. Update TODO with outcome. Consider commit if changes (per guardrails).

**Exact one-liners (from current doctl_scripts/README.txt + wrapper; always cache-verified first)**:

For **full clean import** (reset to your latest local backup for dirty/clean prod state):
```bash
# Ensure .env has DO_APP_ID (or DO_DB_CLUSTER_ID), TARGET_* if overriding, TARGET_SSL_CA, CONFIRM_OVERWRITE=YES
bash bash/import_prod_db_from_local_backup.sh
```
(The wrapper handles discovery via doctl + your APP ID, forces `backup/latest-ndestates-io-db.sql.gz` + reset. Cache context: this achieves "clean state" as defined in TODO-2026-06-14.md and runbooks.)

For **update** (e.g., after local changes):
- Prep in DDEV (per ddev-local-runtime): ingest new data, `ddev export-db --file=backup/latest-ndestates-io-db.sql.gz --gzip`.
- Then same one-liner above.
- Or for incremental (listings-focused): rely on daily job + targeted, then verify with eval.

Post any:
```bash
.github/skills/eval/maintenance-task/SKILL.md db-import
# or with flag for "after apply":
.github/skills/eval/maintenance-task/SKILL.md --task=db-import --apply-run=true
```

**DB-specific checks (via eval skill — run after; use prod connection)**:
- The eval runs the exact queries (loaded from cache: runbooks, prior DB work, mysql-expert):
  ```sql
  SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = DATABASE();
  SELECT MAX(year) FROM house_price_index_annuals;
  SELECT MAX(quarter_start_date) FROM house_price_index_quarters;
  SELECT COUNT(*) FROM house_price_transaction_counts;
  SELECT COUNT(*) FROM live_listings;
  SELECT COUNT(*) FROM agent_live_listings;
  SELECT MAX(last_seen_at) FROM live_listings;
  ```
- Compare to "expected" from cache (backup contents conceptually, or historical baseline in TODO/docs).
- Verify no regression in core (properties, valuations, credits, etc.).
- Status: PASS only if matches clean state spec.

**Security & governance (Stage 4 — non-negotiable)**:
- All via doctl_scripts (connect_do_db.sh for discovery, the wrapper) or .env (never hardcode passwords/CA in prompts/skills).
- This skill + any invocation triggers full security checklist (MCP/agent/prompt threats if Grok generates new logic).
- Prod access: limited to necessary (doadmin for import); prefer least-privilege post-import.
- Reports: no secrets; audit via .tmp/ + TODO references.

**Cost/observability (Stage 6)**:
- Note: doctl calls (for cluster discovery) + mysql (import) — run on host with auth.
- If Grok involved in planning: track tokens (this skill is cache-heavy to minimize).
- Observability: the eval JSON report acts as trace/log. For future: centralize in shared infra (Stage 8).

**Cross-references (load these first — max cache)**:
- `.github/prompts/load-project-cache-first.prompt.md` (docs/codebase for schema, TODO for prod priorities, previous evals like registry).
- `.github/skills/ai-engineering-maturity/SKILL.md` (stage assessment, advancement).
- `.github/prompts/daily-standup-with-cache.prompt.md` (include this as production ease item + maturity indicators).
- `mysql-database-expert` (for query details).
- `doctl_scripts/README.txt` (exact one-liners, the wrapper).
- `bash/import_prod_db_from_local_backup.sh` (the invocation mechanism).
- `copilot-instructions` (DDEV for local prep, data safety — never destructive on live without eval).
- `git-workflow-guardrails` (if commit post-import changes).
- `.github/skills/eval/maintenance-task/SKILL.md` (the verification gate).
- docs/codebase/ARCHITECTURE.md, INTEGRATIONS.md (DO DBaaS), CONCERNS.md (AI + DB items).
- Previous TODOs (e.g., 2026-06-14 for this work).

**Example full flow (one-liner + cache + eval)**:
1. `.github/prompts/load-project-cache-first.prompt.md`
2. `.github/prompts/daily-standup-with-cache.prompt.md` (note: prod DB dirty? → use this skill).
3. `/prod-db-maintenance --mode=full-import`
   (Outputs the one-liner above, with cache-backed rationale: "Per TODO-2026-06-14 and runbooks, this achieves clean state = [list expected counts].")
4. Run the one-liner (with your real .env TARGET_ or cluster).
5. `.github/skills/eval/maintenance-task/SKILL.md --task=db-import --apply-run=true`
   (Outputs JSON report. Status PASS → prod clean. Advancement: "Now promote to agent slot in sprint.")
6. Update TODO with report reference. Commit if needed (guardrails).

**Advancement using this skill (Stage 6/8)**:
- This turns DB maintenance into infrastructure: invocable via Grok (agent slot), cache-backed (no drift), eval-gated (standards in system), observable (reports).
- After success: add as recurring (e.g., "after open-data ingest" or scheduled), with central logs.
- Update this skill with new checks (e.g., from new models in ARCHITECTURE.md).
- Reference reports in branch context/PRs for production pushes.
- Future: full agent invocation (sandboxed doctl/mysql with this skill as spec + eval as gate).

When extending/invoking: Re-run full security checklist. Do not skip governance (Stage 4). Cite https://upsun.com/blog/8-stages-ai-engineering-maturity/

**Grok execution note**: When active, surface current stage (4-5 → advancing via this to 6) + one step (e.g., "Add token budget tracking to the one-liner for observability"). Always maximize cache load in the response.

This skill makes prod DB import/update a native, cache-heavy, Stage 6 task — easy one-liner, verifiable, infrastructure-like. No ten things; all context from system. Use it to keep production clean and progressing.