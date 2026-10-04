---
name: bug-hunter-agent
description: >
  Specialist bug and weakness hunter for any codebase: logic errors, edge cases, error handling,
  races, data integrity, config bugs, performance, integration gaps, and security surface triage.
  Fixes isolated issues or suggests patches with tests. Use on /bug-hunter-agent, "find bugs",
  "hunt bugs", "what could break", or in chains bug-hunt / bug-hunt-deep / bug-hunt-pre-deploy.
argument-hint: "Scope + mode: e.g. 'auth module deep', 'payments fix', 'pre-deploy scan'"
user-invocable: true
disable-model-invocation: false
---

# Bug Hunter Agent

**Purpose:** Find **any** bug, potential bug, or weakness in the project codebase — then **fix** (when safe) or **suggest** fixes with evidence and tests.

**Cache is king:** load manifest + CONCERNS + CONVENTIONS + TESTING before deep source reads.

**Complements (do not duplicate):**

| Skill | Role in bug hunting |
|-------|---------------------|
| security-audit-agent | Deep auth/secrets/OWASP after your surface triage |
| cyber-security-essentials | UK NCSC Cyber Essentials five-control mapping before hunt |
| schema-audit-agent / model-schema-check | Schema and migration drift |
| project-drift-guardian | Scope, CI, deploy, requirements drift |
| test-safety-agent | Gate before any test run |
| test-specialist-agent | Tests for findings and regressions |
| laravel-expert-agent | Framework-specific fixes (Laravel/Filament) |

## Phase 0 — Load context (required)

1. `.github/project-manifest.yaml` or `.claude/project-manifest.yaml` — stack, paths, test command
2. `docs/codebase/CONCERNS.md` — known risks
3. `docs/codebase/CONVENTIONS.md` + `docs/codebase/TESTING.md`
4. Latest `TODO/*.md` — in-scope work
5. User scope from `$ARGUMENTS` (module, path, PR, or `whole codebase`)

## Phase 1 — Mode

Parse argument for mode (default `scan`):

| Mode | Keywords | Output |
|------|----------|--------|
| **scan** | scan, review, audit bugs | Report only |
| **deep** | deep, thorough, comprehensive | Full taxonomy pass |
| **fix** | fix, repair, patch | Report + safe fixes + tests |
| **pre-deploy** | pre-deploy, release, ship | Regressions, config, idempotency |

Emit: `Bug hunter: mode=<mode> scope=<scope>`

## Phase 2 — Static scan (fast signals)

Run via script (never inline heredoc — `/script-not-shell`):

```bash
mkdir -p reports/bugs
bash .grok/skills/bug-hunter-agent/scripts/bug-hunter-scan.sh . reports/bugs/scan-$(date +%Y%m%d).txt
```

Triage scan hits; confirm in source before reporting.

## Phase 3 — Deep hunt (taxonomy)

Read and apply every applicable category in [`references/bug-taxonomy.md`](references/bug-taxonomy.md).

**Hunt method (token-efficient):**

1. Grep for risk patterns in scope (errors, null, raw SQL, TODO, catch blocks)
2. Read hot paths: controllers/services, jobs, webhooks, payment/auth flows
3. Trace happy path + one failure path per critical feature
4. Check tests exist for critical paths; note gaps as weaknesses
5. Cross-check cache ARCHITECTURE vs actual entrypoints

Embody full agent contract: [`.grok/agents/bug-hunter-agent.md`](../../agents/bug-hunter-agent.md)

## Phase 4 — Report

Write `reports/bugs/YYYY-MM-DD-bug-hunt[-scope].md` using [`references/report-template.md`](references/report-template.md).

**Severity:** critical | high | medium | low | info  
**Status:** open | fixed | suggested | delegated

Include code citations for every finding.

## Phase 5 — Fix (mode=fix or user approves)

**Rollback is mandatory.** No patch without a backup session. See [`references/rollback.md`](references/rollback.md).

1. **Init backup** (before any file write):

   ```bash
   BACKUP_ID=$(python3 .grok/skills/bug-hunter-agent/scripts/bug-hunt-backup.py init --scope "<scope>" --mode fix)
   ```

2. Confirm branch scope (`/branch-context-agent` if large change)
3. For each file about to change: `bug-hunt-backup.py backup --backup-id "$BACKUP_ID" <rel/path>`
4. Apply **low/medium** isolated fixes only
5. **Critical security fixes** (critical + security category): if applied, `mark-exempt` — these **survive rollback**
6. **critical/high** (non-security) — suggest only unless user explicitly approves
7. Run `/test-safety-agent` before tests
8. Run project test command (DDEV if manifest says so)
9. Update report with fix log, `backup_id`, and `rollback_cmd`
10. `bug-hunt-backup.py finalize --backup-id "$BACKUP_ID" --report <report-path>`

## Phase 6 — Handoffs (chain or follow-up)

Emit ≤80 token handoff for chains:

```markdown
bug_hunt: N findings (C/H/M/L); fixed=X; tests=pass|fail|skipped
security_pending: [IDs or none]
test_gaps: [cases or none]
drift_flags: [yes/no]
```

## Fix policy (chains and direct invoke)

| Severity / area | Action |
|-----------------|--------|
| **low / medium** (isolated) | Auto-fix in `fix` mode; run tests after |
| **critical / high** | Suggest patch only — unless user explicitly approves in args |
| **auth, payment, crypto, permissions** | Never auto-fix without explicit approval (`fix_policy.require_approval_for`) |
| **Report** | Always write report; append fix log when patches applied |
| **Rollback** | Required backup before fixes; `rollback` restores all except critical security exempt |

Set handoff `fixes_applied: true` and `backup_id: <id>` when any file changed.

**Rollback after fix:**

```bash
python3 .grok/skills/bug-hunter-agent/scripts/bug-hunt-backup.py rollback --backup-id <id>
```

Critical security patches listed in report as `rollback_exempt: true` are **not** reverted.

## Chain invocation

| Chain | Mode | Use when |
|-------|------|----------|
| `/chain bug-hunt` | scan | Report only — quick hunt |
| `/chain bug-hunt-fix` | fix | Hunt + safe fixes + test safety + tests |
| `/chain bug-hunt-deep` | deep | Full report + security + schema + test gaps |
| `/chain bug-hunt-fix-deep` | deep fix | Hunt/fix + security + mandatory test verification |
| `/chain bug-hunt-pre-deploy` | pre-deploy | Report before release |
| `/chain bug-hunt-pre-deploy-fix` | pre-deploy fix | Drift gate + fixes before ship |

Append scope to any chain: `/chain bug-hunt-fix auth module`

Direct: `/bug-hunter-agent payments module fix`

## Anti-patterns

- "LGTM" without source evidence
- Style-only nitpicks as high severity
- Full security audit instead of handoff
- Tests on live database
- Auto-fixing auth/payment/crypto without approval
- Skipping report artifact
- Applying fixes without `bug-hunt-backup.py` session
- Rolling back critical security exempt fixes

## Related

- Taxonomy: `references/bug-taxonomy.md`
- Report template: `references/report-template.md`
- Scan script: `scripts/bug-hunter-scan.sh`
- Registry chains: `chains/registry.yaml` → `bug-hunt*`