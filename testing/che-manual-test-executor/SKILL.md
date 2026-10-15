---
name: "che-manual-test-executor"
description: "Executes the manual_test_plan.md step-by-step using Playwright MCP (browser interactions + screenshots) or HTTP/curl requests for API-only scenarios, generates evidence files (PNG screenshots, JSON logs), and delivers a structured pass/fail report per AC. Call this AFTER manual_test_plan.md is written by che-act and BEFORE che-ship, or standalone when user passes a worktree + task-id or a manual test plan path explicitly."
---

# Che — Manual Test Executor (step-by-step Playwright + HTTP)

> **SHARED REFERENCES (CANONICAL — DO NOT DUPLICATE body here):**
> - Manual Test Plan canonical format (AC structure with GWT / Manual Steps / Severity): che-act `references/MANUAL_TEST_PLAN_TEMPLATE.md`
> - Nx/pnpm build/dev service startup commands: `_shared_checklists/NX_PNPM_COMMON.md`
> - Worktree Session Binding (one session = one worktree, doubt = ask): engineering-contracts §19
> - Output shape rules (concise 4 sections, diagonal readability, deep-dive gate): engineering-contracts §18

## What this skill does (vs QA automated)

| Concern | `che-qa` | This skill `che-manual-test-executor` |
|---|---|---|
| Scope | lint / typecheck / build / unit / E2E commands (CI-style) | **Manual Test Plan steps** written in `$CHE_WORKSPACE_SHARED/manual_test_plan.md` (`$CHE_WORKSPACE_SHARED` is exported by `che compute_paths`; see §0 preflight) — DURABLE, shared between sessions in this worktree. |
| Driver | Shell commands (pnpm/vitest/playwright CLI) | **Playwright MCP** (open tab, navigate, click, fill, screenshot) + **HTTP driver** (curl-style via playwright_get/post/put/patch/delete). |
| Evidence | Command exit codes + stdout/stderr | **PNG screenshots per step**, visible text assertions, HTTP response bodies, browser console logs. |
| Output | Per-pass/fail command line summary | **Per-AC pass/fail report** with evidence links + environment checks pass/fail + smoke check summary. |

> **Rule:** If user says "run unit/E2E tests" → use `che-qa`. If user says "execute manual test plan / open browser and test / check visual behavior" → use THIS skill. Never mix.

---

## 0. Preconditions (non-negotiable)

1. **WORKTREE_ROOT absolute path** provided (by SM or user via command).
2. **Task ID or explicit path to `manual_test_plan.md`** — one of two:
   - Option A (from che session): `$CHE_WORKSPACE_SHARED/manual_test_plan.md` (via contract) exists (DURABLE workspace-shared).
   - Option B (standalone): user passes explicit path to a Markdown file containing AC sections below.
3. If neither exists → STOP. Ask user for task-id or manual_test_plan.md path.
4. **Worktree Session Binding preflight + 🔴 STORAGE BOUNDARY (engineering-contracts §19 + §20 MORATORIUM — NON-NEGOTIABLE):**
   ```bash
   # (a) Resolve the `che` CLI (owns the Che-home cascade + canonical path construction)
   command -v che >/dev/null 2>&1 || { echo "❌ FATAL: 'che' CLI not found on PATH. Zero writes allowed without storage boundary. exit 98"; exit 98; }
   SESSION_ID="${CHE_CURRENT_SESSION_ID:-${CHE_SESSION_ID:-fallback-manual-test-session}}"
   eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"
   che ensure_dirs "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD"

   # (b) Double-guard: assert NO output directory falls WITHIN worktree
   che assert_outside_worktree "$CHE_SESSION_DIR" "$WORKTREE_ROOT" --label "CHE_SESSION_DIR (ephemeral QA evidence)"
   che assert_outside_worktree "$CHE_WORKSPACE_SHARED" "$WORKTREE_ROOT" --label "CHE_WORKSPACE_SHARED (durable plans)"

   # (c) CANONICAL PATHS FOR ALL SKILL OUTPUTS — construct ONCE, reuse everywhere
   # Final report (session-scope — ephemeral, this execution only):
   MANUAL_TEST_REPORT_PATH="$(che output_path "qa" "manual-test-execution-report" "${TASK_ID:-standalone}" "session" "md")"
   # Evidence directory helper: every screenshot/log must use che output_path type=qa scope=session related_id=TASK_ID suffix="AC-<id>"
   # AC-2 screenshot example:  "SCREENSHOT_AC2_PATH=$(che output_path "qa" "screenshot" "${TASK_ID:-standalone}" "session" "png" "AC-002")"
   # env setup log example:    "ENV_SETUP_LOG_PATH=$(che output_path "qa" "env-setup" "${TASK_ID:-standalone}" "session" "log")"
   ```
   - Check `$CHE_SESSION_DIR/binding.md` Level 2 entry if present (EPHEMERAL per-session).
   - Mismatch with provided WORKTREE_ROOT → BLOCK. Ask override/switch/cancel.
   - Missing binding → follow §19 canonical binding flow (global registry Level 1 + Level 2), ask user for confirmation.
   - **HARD RULE FROM NOW ON:** NEVER construct path manually. Every screenshot, log, report = mandatorily via `che output_path "qa" ...`. No PNG/LOG/MD file lands inside worktree. MORATORIUM.

### 0.1 EVIDENCE RETENTION POLICY (ONDA4 — TWO LOCALS, NEVER IN USER WORKTREE)

```bash
# =============================================================
# DOUBLE LOCAL POLICY — engineering-contracts §20 MORATORIUM:
# NO evidence/manifest is written inside WORKTREE_ROOT/*
# by default. Override = user explicitly asks VERBATIM.
# =============================================================

# --- LOCAL 1 — EPHEMERAL / SESSION-SCOPE (heavy, TTL 30 days) ---
# FULL-size screenshots EVERY step, raw browser console logs,
# HTTP response bodies, get_visible_text capture. Stays in session.
# Cleanup handoff: sessions older than 30 days = TTL.
MANUAL_SESSION_EVIDENCE_DIR="$CHE_SESSION_DIR/qa"
mkdir -p "$MANUAL_SESSION_EVIDENCE_DIR/screenshots" "$MANUAL_SESSION_EVIDENCE_DIR/logs" "$MANUAL_SESSION_EVIDENCE_DIR/api"

# --- LOCAL 2 — DURABLE / WORKSPACE-SHARED (light audit trail) ---
# Canonical path via contract helper type=qa scope=workspace related_id=commit_7char.
# ONLY CONTAINS:
#   (i)   evidence_manifest_<SHA16_MANIFEST>.json
#   (ii)  1 FINAL JPEG/PNG thumbnail per AC PASS ≤200KB
CURRENT_COMMIT_7CHAR="${CURRENT_COMMIT_7CHAR:-$(cd "$WORKTREE_ROOT" && git rev-parse --short=7 HEAD 2>/dev/null || echo "HEAD-detached")}"
MANUAL_WORKSPACE_AUDIT_DIR="$(che output_path "qa" "audit" "commit-${CURRENT_COMMIT_7CHAR}" "workspace" "tmp")"
MANUAL_WORKSPACE_AUDIT_DIR="$(dirname -- "$MANUAL_WORKSPACE_AUDIT_DIR")"
mkdir -p "$MANUAL_WORKSPACE_AUDIT_DIR"
che assert_outside_worktree "$MANUAL_WORKSPACE_AUDIT_DIR" "$WORKTREE_ROOT" --label "MANUAL_WORKSPACE_AUDIT_DIR (durable hash manifest)"
```

**MANDATORY Manifest JSON Schema (same as che-qa schema):** same `generated_at_utc / commit_7char / session_id / qa_run_passed / per_test_file_sha256 / per_evidence_sha256 / per_behavior_result / thumbnail_path` keys (see che-qa §-0.1.1 for canonical format). For this skill, `per_behavior_result` maps manual AC-IDs (e.g. `AC-001 → PASS`).

**Per-AC Screenshot Rules (HARD):**
1. **Every FULL screenshot via playwright_screenshot** → always saved in `LOCAL 1 Session` (Session TTL 30). Calculate file SHA256 → insert in `per_evidence_sha256`.
2. **After THEN verified (last AC step):** generate thumbnail width=800px JPEG quality=75%. **SAVE ONLY THUMBNAIL in LOCAL 2 Workspace.** If PNG → reduce dimensions until ≤200KB. If it doesn't fit → thumbnail=null.
3. **DO NOT save FULL screenshot in LOCAL 2 (size moratorium).** Only its SHA256 in manifest.

---

## 1. STEP 0 — Parse Manual Test Plan into executable steps

Open and parse `$CHE_WORKSPACE_SHARED/manual_test_plan.md` (DURABLE workspace-shared, via contract) or user-provided custom path.
Extract into in-memory `PLAN_DATA` object with these sections:

### 1.1 Environment Setup (§0 of plan)
- Commands from ```bash``` block under `## 0. Environment Setup — Preconditions`
- Test accounts / data list (names only — never values)
- App URLs / base URLs present (extract ALL URL strings like `http://localhost:3000`)

### 1.2 Acceptance Criteria list (§1 Scenario Test Cases)
For every `### AC-<N>:` block:
- Extract AC-ID, Title, GIVEN, WHEN, THEN
- Extract numbered list under `#### Manual Steps` (step numbers + action text)
- Extract Severity if FAILS field (BLOCKER / HIGH / MEDIUM / LOW)
- If Automated equivalent command present → note it (but skill still executes MANUAL steps; automated is extra run if user asks).

### 1.3 Smoke Test Checklist (§2)
Extract table rows S1..S5. Mark which ones skill CAN execute (S3/S4 via browser; S1/S2 via shell; S5 via server log grep). §3 Security/Compliance is **human-only per plan**, skill skips it (explicitly note "HUMAN_REVIEW_NEEDED" for §3). §4 Rollback Plan = informational only.

### 1.4 Error if no ACs found
If zero `### AC-` headers → STOP. Report: "manual_test_plan.md missing AC sections. Need at least 1 AC-<N> block with numbered Manual Steps."

---

## 2. STEP 1 — Evidence directory pre-creation

Create directory structure immediately after successful parsing (before browser/curl). Use `eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"` + `che ensure_dirs "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD"` first (see §0 item 4 preflight).

```
$CHE_SESSION_DIR/qa/              ← EPHEMERAL per-session (generated evidence, never in user code)
├── ENVIRONMENT_SETUP.log             # stdout/stderr of executed setup commands
├── screenshots/
│   ├── AC-<N>_<slug>/
│   │   ├── step_<K>_screenshot.png   # one PNG per visual verification step
│   │   ├── step_<K>_visible_text.txt # get_visible_text() content after step K
│   │   ├── step_<K>_api_response.json# HTTP response if step did get/post/etc
│   │   ├── step_<K>_console.log      # playwright_console_logs() if errors/warnings
│   │   └── FINAL_ASSERT_<X>.png      # final screenshot of verified THEN expected
│   └── SMOKE_<Sx>_<slug>.*           # smoke test evidence S1..S5 (png/log)
├── logs/
│   └── execution.log                 # global timeline: step timestamp + action + result
```

---

## 3. STEP 2 — Environment Setup Execution (§0 of plan)

Goal: make target app reachable for browser steps.

1. **User approval gate BEFORE running setup commands.** Present plan:
   > `I will execute these setup steps in <WORKTREE_ROOT>. Confirm? (A = Yes, execute all) (B = Skip setup, app already running at <URL>) (C = Cancel)`
   - If B → ask user for base URL (e.g., `http://localhost:3000`) + skip setup block.
   - If C → stop.
2. **Run commands from §0 bash block sequentially** inside `WORKTREE_ROOT`.
3. Record stdout+stderr to `ENVIRONMENT_SETUP.log`.
4. **Hard-fail rule:** If any setup command returns non-zero exit (pnpm install fail / build error / port in use):
   - STOP before AC steps. Report failed command + last 20 log lines.
   - Ask: "Setup command <N> failed: (A = Try alternative command <suggestion>) (B = Skip setup, app accessible at <URL>) (C = Cancel)".
5. After setup OK: confirm base URL(s) reachable (HTTP GET to root should return 200 or 302 via playwright_get). If not → warn but proceed; user may have custom URL.

---

## 4. STEP 3 — AC Execution Loop (per AC-N in order)

For each AC block in extracted PLAN_DATA.AC_LIST:

### 4.1 AC Header
Append to `execution.log`:
```
[<ISO ts>] === START AC-<N>: <TITLE> ===
```

### 4.2 Per-Step Driver Dispatch (natural language to Playwright MCP)

Each numbered step under Manual Steps is classified into ONE driver type. **Execute ONE step at a time. Never batch.** Write evidence to disk after each. Append result to timeline.

#### Driver classification rules (match in order):
| Step pattern says | Driver used | MCP tool / action |
|---|---|---|
| "Navigate to `URL`" / "Open `URL`" / "Acessar URL" | Playwright (browser) | `playwright_navigate` with URL + default viewport |
| "Click `<button name or CSS selector>`" | Playwright | `playwright_click` using `selector` (prefer CSS `button:has-text("...")` for names; fallback ask user if ambiguous) |
| "Fill form with Field A: `value` Field B: `value`" / "Type X" | Playwright | `playwright_fill` — one call per field. Selector = `input[name="<field>"]` or `label:has-text("Field A") + input` etc. Ask user if ambiguous (§19 doubt). |
| "Select `<option>` from `<dropdown>`" | Playwright | `playwright_select` |
| "Submit" / "Click Submit" | Playwright | `playwright_click` on `button[type=submit]` + wait 2s after |
| "Upload file `<path>`" | Playwright | `playwright_upload_file` |
| `curl` mention or "call API <METHOD> <URL>" / "request GET" | HTTP Driver | `playwright_get / playwright_post / playwright_put / playwright_patch / playwright_delete` with URL + headers. |
| "Check page: expected visible text `XYZ`" / "URL changed to `/path`" | Assertion Playwright | Run: (a) `playwright_get_visible_text()` and grep for `XYZ`; (b) check current URL. Record as assertion. |
| "Check server logs / email sandbox / external system" | **Cannot execute → SKIP with HUMAN_REVIEW_NEEDED** | Do not fake. Write "Step K: requires human verification (external system)". |
| Step is ambiguous / no driver pattern matches | **STOP → ASK user.** | Do not guess. Example: "proceed with checkout" without UI flow described → ask clarification. |

### 4.3 Mandatory evidence capture rules (per step)
After EACH step (pass/fail):
1. **Browser step:**
   - `playwright_screenshot` with `name="AC-<N>_step_<K>"` + `savePng=true` to evidence dir.
   - `playwright_get_visible_text()` → `step_<K>_visible_text.txt`.
   - `playwright_console_logs()` → `step_<K>_console.log` if ERROR/WARN present.
2. **HTTP step:**
   - Save full response body as `step_<K>_api_response.json`.
   - If `assert_response` used → save result in filename.
3. **Assertion check step:**
   - FINAL_ASSERT screenshot named `FINAL_ASSERT_<short_desc>.png`.
   - Record pass/fail based on THEN expected text / URL match.

### 4.4 Then-Block Final Verification
When AC steps finished:
- Run explicit verification against extracted `THEN` text.
- Classification:
  - ✅ **PASS**: All THEN conditions found in visible_text / HTTP response / URL. At least one screenshot per visual THEN.
  - ⚠️ **PARTIAL**: Some THENs pass, others SKIPPED (external system / human-only).
  - ❌ **FAIL**: At least one THEN not matched; step K exception/timeout; or console shows CRITICAL error + THEN mismatch.
  - ⏭️ **SKIP**: ALL steps are HUMAN_REVIEW_NEEDED.
- Append final verdict to `execution.log` + report data.
- `playwright_close` explicitly for next AC isolation.

---

## 5. STEP 4 — Smoke Test Checks (§2 of plan, light)

After all ACs pass/partial/fail:

| Smoke ID | How skill executes |
|---|---|
| S1 Build | Shell command equivalent (from QA stack detection): run build → capture exit code + last 10 lines. |
| S2 Lint | Same: lint command. ≤5 warnings is PASS. |
| S3 Login | If plan has login AC or test account steps → execute login-only scenario via Playwright + screenshot landing. Else: HUMAN_REVIEW_NEEDED. |
| S4 Nav top-level pages | Collect nav links from footer/header (after login if S3 pass) → playwright_navigate 3 top pages. 500 / WSOD = FAIL. Screenshot each. |
| S5 Server logs | Best-effort: grep CRITICAL/ERROR from last 50 lines of dev output (if started in session). Not accessible → HUMAN_REVIEW_NEEDED. |

Save evidence: `SMOKE_<Sx>_<name>.log` or `.png`.

---

## 6. STEP 5 — Build Final Structured Report

Canonical sections (match `references/MANUAL_TEST_EXECUTION_REPORT.md`). Use **English for file content and chat summary**.

Report saved to: **`$MANUAL_TEST_REPORT_PATH`** variable (constructed during §0 item 4c preflight via `che output_path`). Example:
```
$CHE_SESSION_DIR/qa/evidence/T123-refund/20260902-130000-manual-test-execution-report.md
```
⚠️ NO hardcoded `reports/MANUAL_TEST_EXECUTION_REPORT.md`. Re-run §0 item 4 preflight BEFORE saving if variable is empty.

Report sections:
1. Header (task-id, worktree, timestamps, base URLs)
2. Environment Setup result (PASS / FAIL + note + link to ENVIRONMENT_SETUP.log)
3. Per AC summary table: AC-ID, Title, Verdict (✅/⚠️/❌/⏭️), Severity, Evidence link, Notes.
4. Detailed per AC: GIVEN/WHEN/THEN, step actions + verdicts + evidence links, assertion notes.
5. Smoke Tests §2 result table (S1..S5)
6. Human-only items remaining (§3 Security, etc.)
7. Rollback Plan reference (link to original plan §4)
8. Overall Verdict (✅ All BLOCKER/HIGH PASS | ❌ ≥1 BLOCKER or ≥2 HIGH FAIL | ⚠️ low-severity failures)
9. **Evidence retention (ONDA4 — MANIFEST + THUMBNAIL):**
   - Workspace audit manifest SHA256 = <MANUAL_EVIDENCE_MANIFEST_SHA>
   - Manifest JSON path = <MANUAL_EVIDENCE_MANIFEST_PATH>
   - Session full evidence (TTL 30d) = $CHE_SESSION_DIR/qa/

### 6.1 FINAL MANDATORY STEP — Generate Evidence Manifest SHA256 (Local 2 Workspace Audit)

After saving final report (§6), **before returning**, generate Local 2 manifest using SAME che-qa §0.2 algorithm:
- SHA256 of EVERY Local 1 (Session) evidence → `per_evidence_sha256` entry.
- SHA256 of EVERY FINAL_ASSERT screenshot for AC PASS → ≤200KB Local 2 (Workspace) thumbnail.
- `per_behavior_result` maps AC-ID → PASS/FAIL/PARTIAL/SKIP.
- `per_test_file_sha256` = empty `{}` for this skill.
- Calculate manifest SHA256 → name `evidence_manifest_<SHA16>.json`; save via `che write_file_atomic`.
- Decision log entry: `MANUAL_TEST_EVIDENCE_MANIFEST` with manifest details.

### Chat delivery rule (§18 contracts)
Chat message uses condensed §18 shape. Chat summary contains in English:
- 📍 Status: overall verdict + AC pass/fail counts
- 🧩 Key failures: max 3 bullets (AC-ID + failed condition)
- 🔗 Refs: report, evidence dir, original plan links
- ❓ 1 deep-dive offer: failure evidence screenshot or setup retry.

---

## 7. General execution rules / safety

1. **NEVER interact with production URLs**: If URL contains `.prod.` / `.production.` / known production TLD+domain without explicit `test`/`staging`/`dev` subdomain, or user says "this is prod" → BLOCK. Ask for confirmation TWICE. Use `NODE_ENV=test` guard. Heuristic: `/(^|\.)prod(uction)?\./` or project registry `$CHE_PROJECT_DIR/product_context.md`.
2. **Never log secrets**: If login needed → user provides via chat (or env vars in Playwright header). **Never echo credentials in execution.log / screenshots (do not screenshot password fields).**
3. **AC Isolation**: After last AC step → `playwright_close` + new navigate for next AC. Do not share browser session unless steps explicitly say so.
4. **Ambiguity rule (§19 doubt = ask)**: If step text / selector ambiguous → ASK user. Never guess.
5. **One SKIP per AC OK; ≥5 SKIP total → warn user**: "Many HUMAN_REVIEW_NEEDED. Continue?"
6. **Per operation scissor check (§19)**: All written PNG/LOG must be under `$CHE_SESSION_DIR/qa/`. Block if escape. NO evidence in user worktree (engineering-contracts §19.1 MORATORIUM).
7. **Response budget (§18):** Chat summary ≤500 words. Full report/evidence on disk only.
