---
name: running-drive-automation
version: "3.0.1"
description: >
  Operates the Drive Automation Chain 1+2 system — a multi-agent Google Drive
  classification and routing pipeline backed by a Supabase audit trail. Activates
  when the user wants to classify, route, or organize Google Drive files; invoke
  the agent council; run the drive router; check for file drift; trigger smoke
  tests; view the Supabase audit log; or work with any component of the personal
  drive automation system. Also triggers on: organize my drive, run the council,
  classify these files, drive drift, agent council, chain 1, chain 2, drive router,
  run smoke test, check drive audit, council memo, n8n drive workflow, supabase
  drive, CrewAI council, fire up the council, batch classify, council throughput,
  asyncio parallel, drive pipeline, file routing, drive inbox. Always use this
  skill before touching any part of the drive automation system — even if the
  request seems simple (e.g., "check the audit log", "did the router run?").
  NOTE: n8n MCP CONNECTION_ISSUE. Chain 1 manual-only at krosebrook.app.n8n.cloud.
allowed-tools: Read Write Bash
disable-model-invocation: false
compatibility:
  tools: [bash, google_drive_search, google_drive_fetch]
  dependencies:
    - name: n8n
      status: CONNECTION_ISSUE
      affected_components: [Chain 1 — Drive Router trigger, Chain 1 execution monitoring]
      fallback: https://krosebrook.app.n8n.cloud
    - name: CrewAI
      status: OPERATIONAL
    - name: Supabase
      status: OPERATIONAL
    - name: Python 3.11+
      status: OPERATIONAL
  mcp_servers:
    - name: n8n
      status: CONNECTION_ISSUE
      note: Chain 1 MCP trigger unavailable; manual trigger available in n8n Cloud UI
    - name: Google Drive
      status: OPERATIONAL
---

# Running Drive Automation

**TL;DR:** Chain 1 (n8n) classifies + routes incoming Drive files automatically.
Chain 2 (10 CrewAI crews in `agent_council.py`) performs deep per-file evaluation
and writes structured memos. Supabase logs every action. Smoke tests gate
production runs.

> ⚠ **DEGRADED STATE ACTIVE** — n8n MCP is CONNECTION_ISSUE. Chain 1 automatic
> trigger is unavailable via MCP. See DEGRADED MODE section before proceeding.
> Chain 2, Supabase, and Google Drive components are fully operational.

---

## FAIL_IF — n8n MCP Unavailable (Chain 1)

**This block fires before any Chain 1 operation is attempted.**

```
IF n8n MCP status = CONNECTION_ISSUE:
  STOP. Do NOT attempt MCP tool calls to trigger or monitor Chain 1.
  Do NOT simulate Chain 1 execution or fabricate routing results.

  Chain 1 manual trigger path:
    1. Navigate to https://krosebrook.app.n8n.cloud
    2. Workflows → "Drive Router Chain 1"
    3. Click "Execute workflow" (top-right button, lightning bolt icon)
    4. Monitor execution in the Executions tab on the left sidebar
    5. Verify results in Supabase: SELECT * FROM file_audit ORDER BY
       created_at DESC LIMIT 20;

  Chain 2, Supabase queries, Google Drive reads, and drift checks are
  UNAFFECTED by this failure. Proceed with those operations normally.

  "Just do it" override: If user explicitly says "try the n8n MCP anyway,"
  attempt the call once and report the exact error. Do not retry silently.
```

---

## DEGRADED MODE — n8n MCP: CONNECTION_ISSUE

| Component | Status | Notes |
|---|---|---|
| Chain 1 — Drive Router (auto trigger via MCP) | ❌ UNAVAILABLE | n8n MCP CONNECTION_ISSUE; use manual trigger at krosebrook.app.n8n.cloud |
| Chain 1 — Execution log monitoring via MCP | ❌ UNAVAILABLE | Check manually: n8n.cloud → Executions |
| Chain 1 — Webhook trigger (direct curl) | ✅ OPERATIONAL | curl to CHAIN1_WEBHOOK_URL still works; see Chain 1 section |
| Chain 2 — Agent Council (agent_council.py) | ✅ OPERATIONAL | Runs locally via Python; no n8n dependency |
| Chain 2 — Drift Check (--drift-check) | ✅ OPERATIONAL | Runs locally; reads Drive via API, writes to Supabase |
| Supabase audit log (file_audit, council_memos) | ✅ OPERATIONAL | Supabase MCP and direct SQL both available |
| Google Drive reads (classify, list, fetch) | ✅ OPERATIONAL | Google Drive MCP unaffected |
| Smoke Tests (partial) | ⚠ PARTIAL | `[PASS] Chain 1 webhook reachable` will FAIL if n8n is down; all other checks pass |

**In DEGRADED MODE, the recommended workflow is:**

1. Trigger Chain 1 manually (see manual path in FAIL_IF above), OR trigger
   via direct webhook curl (see Chain 1 section)
2. Run Chain 2 Council as normal (fully operational)
3. Check audit results directly in Supabase
4. Run smoke tests and expect exactly 1 FAIL (`Chain 1 webhook reachable`);
   treat this as expected, not a blocker for Chain 2 operations

---

## Decision Tree

```
What do you need?
  ├─ Route a batch of new files
  │    ├─ n8n MCP operational ──────────────► Chain 1 — see §Golden Path: Chain 1
  │    └─ n8n MCP CONNECTION_ISSUE ──────────► Chain 1 MANUAL — see §Manual Trigger
  │
  ├─ Deep evaluation on files ────────────────► Chain 2 Council — FULLY OPERATIONAL
  │                                             see §Golden Path: Council
  │
  ├─ Check for file drift ────────────────────► Drift Watcher — FULLY OPERATIONAL
  │                                             see §Golden Path: Drift
  │
  ├─ Verify pipeline health ──────────────────► Smoke Tests — PARTIAL (1 expected FAIL)
  │                                             see §Smoke Test Protocol
  │
  ├─ View what happened to a file ────────────► Supabase audit — FULLY OPERATIONAL
  │                                             see references/supabase-schema.md
  │
  ├─ Understand crew roles/behavior ──────────► FULLY OPERATIONAL
  │                                             see references/crews.md
  │
  ├─ Configure n8n Chain 1 ───────────────────► Manual only while MCP down
  │                                             see references/n8n-config.md
  │                                             and §Manual Trigger below
  │
  └─ Apply asyncio throughput fix ────────────► FULLY OPERATIONAL
                                               see references/asyncio-fix.md
```

---

## System Map

| Component | Location | Purpose | MCP Status |
|---|---|---|---|
| Chain 1 — Drive Router | `krosebrook.app.n8n.cloud` → `chain1_drive_router.n8n.json` | Watches Drive, classifies files, routes to destination folders | ❌ MCP UNAVAILABLE — manual trigger available |
| Chain 2 — Agent Council | `personal/drive-automation/agent_council.py` | 10 CrewAI crews evaluate each file; produces structured memo | ✅ OPERATIONAL |
| Supabase Audit | `personal/drive-automation/supabase_migration.sql` | Schema: `file_audit` + `council_memos` tables | ✅ OPERATIONAL |
| Smoke Tests | `personal/drive-automation/smoke_test.py` | End-to-end validation; 1 FAIL expected in degraded mode | ⚠ PARTIAL |
| Drift Watcher | Embedded in `agent_council.py` | Detects files that moved or changed classification since last run | ✅ OPERATIONAL |

**⚠ Lane rule:** Personal drive automation uses a **dedicated** Supabase project. Never route through `oorstbwcydxwiojrsoim` (Loxihart). Verify `.env` `SUPABASE_URL` before any Supabase op.

**⚠ Large-file rule:** Files >3KB (`agent_council.py` 22K, `chain1_drive_router.n8n.json` 32K, `supabase_migration.sql` 7.6K, `smoke_test.py` 7.9K) must be pushed via `git push` locally — Zapier's `github_create_or_update_file` times out above 3KB.

---

## Golden Path: Chain 1 (Route New Files)

> **CONNECTION CHECK — n8n MCP: CONNECTION_ISSUE**
> Claude cannot trigger or monitor Chain 1 via MCP.
> Use direct webhook curl (path A, below) OR the manual UI trigger (path B).
> Both paths work regardless of MCP status.

### Path A: Direct Webhook (n8n MCP not required)

```bash
# 1. Confirm Chain 1 is active in n8n dashboard
#    https://krosebrook.app.n8n.cloud → Workflows → "Drive Router Chain 1"
#    Status toggle must be: Active

# 2. Trigger via webhook (see references/n8n-config.md for full URL + auth headers)
curl -X POST <CHAIN1_WEBHOOK_URL> \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <N8N_WEBHOOK_TOKEN>" \
  -d '{"trigger": "manual", "folder": "<DRIVE_INBOX_FOLDER_ID>"}'

# 3. Monitor execution in n8n Executions tab (manual, since MCP unavailable)
#    https://krosebrook.app.n8n.cloud → Executions → filter by "Drive Router Chain 1"

# 4. Verify results in Supabase file_audit table (Supabase MCP: OPERATIONAL)
#    SELECT * FROM file_audit ORDER BY created_at DESC LIMIT 20;
```

→ Full webhook config, auth, node map: **references/n8n-config.md**

### Path B: Manual UI Trigger (n8n MCP not required)

```
1. Navigate to https://krosebrook.app.n8n.cloud
2. Workflows → "Drive Router Chain 1"
3. Click "Execute workflow" button (lightning bolt, top-right of editor)
4. Executions tab → watch the live run populate
5. When complete: verify in Supabase (see Path A, step 4)
```

---

## Golden Path: Chain 2 (Agent Council) — FULLY OPERATIONAL

```bash
# Pre-flight: run smoke tests first — NEVER skip
python personal/drive-automation/smoke_test.py
# Expected in DEGRADED MODE:
#   [FAIL] Chain 1 webhook reachable  ← expected, non-blocking in degraded mode
#   [PASS] all other checks
# If any check other than Chain 1 webhook FAILs: stop and debug before proceeding.

# Build manifest
MANIFEST='{
  "run_id": "'$(date +%Y-%m-%d-%H%M)'",
  "items": [
    {"file_id": "...", "name": "...", "mime_type": "...", "path": "..."}
  ]
}'

# POST to council endpoint
curl -X POST https://<COUNCIL_HOST>/council \
  -H "Content-Type: application/json" \
  -d "{\"manifest\": $MANIFEST}"

# Poll Supabase for memo results (Supabase MCP: OPERATIONAL)
# SELECT * FROM council_memos WHERE run_id = '<run_id>';
```

**If batch > 5 files:** Apply the asyncio parallel fix first → **references/asyncio-fix.md**
**Council crew behavior:** → **references/crews.md**
**Or use the script wrapper:** `bash scripts/run_council.sh --manifest <path_to_manifest.json>`

---

## Golden Path: Drift Check — FULLY OPERATIONAL

```bash
# Drift watcher runs inside agent_council.py when invoked with --drift flag
python personal/drive-automation/agent_council.py --drift-check

# Output: files flagged with [DRIFT] have changed classification or path since last run
# Review each DRIFT entry before re-routing — don't auto-re-route drift without review
# Results written to Supabase file_audit (Supabase MCP: OPERATIONAL for review)
```

---

## Smoke Test Protocol

Run before **every** production council batch. In DEGRADED MODE, 1 FAIL is expected.

```bash
cd personal/drive-automation/
python smoke_test.py

# Expected output — DEGRADED MODE (n8n MCP CONNECTION_ISSUE):
# [FAIL] Chain 1 webhook reachable  ← EXPECTED in degraded mode; non-blocking for Chain 2
# [PASS] Supabase connection (personal project)
# [PASS] file_audit table exists
# [PASS] council_memos table exists
# [PASS] agent_council.py imports cleanly
# [PASS] Sample crew instantiation
# [PASS] Drift watcher init

# Expected output — FULLY OPERATIONAL (n8n MCP connected):
# [PASS] Chain 1 webhook reachable
# [PASS] Supabase connection (personal project)
# [PASS] file_audit table exists
# [PASS] council_memos table exists
# [PASS] agent_council.py imports cleanly
# [PASS] Sample crew instantiation
# [PASS] Drift watcher init

# STOP conditions:
#   Any FAIL other than "Chain 1 webhook reachable" → debug before proceeding
#   "Chain 1 webhook reachable" FAIL in FULLY OPERATIONAL mode → n8n is actually down
```

---

## Self-Verification Checklist

Before invoking the council on a real batch:

- [ ] **n8n MCP status checked. If CONNECTION_ISSUE, FAIL_IF block acknowledged.**
  FAIL: Chain 1 triggered via MCP while n8n MCP is CONNECTION_ISSUE — use
  direct webhook curl or manual UI trigger per §Golden Path: Chain 1.

- [ ] **`personal/drive-automation/` files are current in GitHub.**
  FAIL: Any of the 4 large files (`agent_council.py`, `chain1_drive_router.n8n.json`,
  `supabase_migration.sql`, `smoke_test.py`) not pushed locally via `git push` —
  do NOT use Zapier for files >3KB.

- [ ] **Supabase migration has run on personal project.**
  FAIL: `file_audit` or `council_memos` tables missing in personal Supabase project
  → run `supabase_migration.sql` against the personal project before proceeding.

- [ ] **`.env` `SUPABASE_URL` points to personal project (NOT `oorstbwcydxwiojrsoim`).**
  FAIL: `SUPABASE_URL` contains `oorstbwcydxwiojrsoim` → lane isolation violation;
  stop immediately and correct the env var before any Supabase write.

- [ ] **`smoke_test.py` passes with 0 unexpected failures.**
  FAIL: Any PASS→FAIL other than "Chain 1 webhook reachable" in degraded mode
  → debug the specific failing component before running production batch.

- [ ] **Chain 1 n8n workflow is Active (manual UI check).**
  FAIL: Chain 1 status is Inactive in n8n Cloud UI → activate before triggering
  or the webhook will be ignored regardless of trigger method.

- [ ] **If batch > 5 files: asyncio parallel fix applied.**
  FAIL: Batch >5 files submitted to Council without asyncio fix → ThreadPoolExecutor
  default will exceed RPM cap; apply fix per `references/asyncio-fix.md`.

- [ ] **`COUNCIL_HOST` env var is set and `/council` endpoint is reachable.**
  FAIL: `curl -I https://<COUNCIL_HOST>/council` returns non-200 → Chain 2 cannot
  receive the manifest; debug Council host before proceeding.

---

## Reference Layer

| File | Load when... |
|---|---|
| `references/crews.md` | Running council; need to understand crew roles, tweak behavior, or debug a specific crew output |
| `references/n8n-config.md` | Configuring Chain 1, debugging webhook, updating trigger conditions or node logic; required for CHAIN1_WEBHOOK_URL and auth headers |
| `references/supabase-schema.md` | Querying audit log, running migrations, understanding table structure or RLS |
| `references/asyncio-fix.md` | Batch > 5 files; applying or reverting parallel throughput improvement |

---

## Key Constraints Summary

1. **n8n MCP CONNECTION_ISSUE** — Chain 1 auto-trigger via MCP is unavailable.
   Use direct webhook curl or manual UI trigger at krosebrook.app.n8n.cloud.
   Chain 2, Supabase, Drive, and drift checks are unaffected.
2. **Supabase lane isolation** — personal ≠ Loxihart (`oorstbwcydxwiojrsoim`).
   Cross-contamination breaks audit trails.
3. **RPM cap** — 10 crews × LLM calls. Default model: Haiku. Cap
   `ThreadPoolExecutor` at 5 workers.
4. **Smoke-gate** — `smoke_test.py` must fully PASS before any production run
   (in degraded mode: all checks except "Chain 1 webhook reachable"). One
   unexpected FAIL = debug first.
5. **Git-push for large files** — 4 files exceed Zapier's 3KB limit. Always
   push locally.
6. **Drift review before re-route** — DRIFT flags require manual review, not
   automatic re-routing.

---

## CLAIMS / COUNTEREXAMPLES / CONTRADICTIONS

- [GENERATED] Chain 1 n8n workflows continue running on their own schedules
  when MCP is CONNECTION_ISSUE — the MCP connection is a Claude-to-n8n channel,
  not the workflow execution engine. Scheduled triggers are unaffected.
- [GENERATED] Direct webhook curl bypasses n8n MCP entirely and remains
  operational regardless of MCP status, provided the n8n Cloud instance
  itself is healthy.
- [GENERATED] Supabase MCP operates independently of n8n MCP — Supabase
  audit queries remain available while n8n is unavailable.
- ! CONTRADICTION: `smoke_test.py` uses `[FAIL] Chain 1 webhook reachable` as
  a hard-stop signal, but in degraded mode this FAIL is expected and non-blocking
  for Chain 2. The smoke test protocol in this skill annotates this explicitly,
  but the `smoke_test.py` script itself does not distinguish between
  CONNECTION_ISSUE (n8n MCP down) and n8n Cloud itself being down. A test FAIL
  on this line requires manual confirmation of n8n Cloud health before proceeding.

---

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS

- **`references/n8n-config.md` contains the load-bearing CHAIN1_WEBHOOK_URL
  and auth headers.** If that reference file is absent, the direct webhook
  curl in §Golden Path: Chain 1 cannot be completed without locating those
  values in the n8n Cloud UI manually. Consider embedding the webhook URL
  pattern (without the token) in this SKILL.md directly.
- **Root cause of n8n MCP CONNECTION_ISSUE not captured here.** May be token
  expiry, MCP server config change, or n8n Cloud outage. Check
  https://status.n8n.io and re-authenticate in Claude.ai Settings →
  Integrations as first recovery step.
- **No automated alert when n8n MCP reconnects.** The degraded mode annotation
  in this skill must be manually updated (compatibility block + description +
  DEGRADED MODE table) when MCP is restored. No hook or self-detection exists.
- **Smoke test `[PASS] Chain 1 webhook reachable` tests the webhook URL, not
  the n8n MCP connection.** If n8n Cloud itself goes down (not just MCP), this
  test FAIL is no longer "expected and non-blocking" — it indicates Chain 1
  cannot run at all, even via manual trigger. Manual confirmation of n8n Cloud
  health status required when this check fails.
