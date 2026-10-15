---
name: "che-qa"
description: "Auto-detects project tech stack, runs build → lint → typecheck → tests in the correct order. Invoke ONLY by che-act after Developer completes a task and scope validation passes. QA reports stay OUTSIDE worktree in $CHE_SESSION_DIR/qa/<related_id>/ with sortable timestamp prefix."
---

# Che — QA

> **SHARED REFERENCES (CANONICAL — DO NOT DUPLICATE body here):**
> - Nx/pnpm QA run order + standard commands: `_shared_checklists/NX_PNPM_COMMON.md`
> - CI common failure fixes classification table: `_shared_checklists/NX_PNPM_COMMON.md`

Runs automated quality gates for a single task or full session.
Always returns a **structured, numbered report** so the Developer can fix without guessing.

---

## -0.1 STORAGE BOUNDARY PREFLIGHT (MANDATORY BEFORE FIRST WRITE)

```bash
# 1. Resolve the `che` CLI (owns the Che-home cascade + canonical path construction)
command -v che >/dev/null 2>&1 || { echo "❌ FATAL: 'che' CLI not found on PATH. Cannot write outputs without storage boundary. Aborting write."; exit 98; }

# 2. Resolve minimum inputs (SM should pass; safe fallback only if missing)
WORKTREE_ROOT="${WORKTREE_ROOT:?SM must pass WORKTREE_ROOT}"
TASK_ID="${TASK_ID:-full-session}"
TASK_SLUG="${TASK_SLUG:-qa}"
SESSION_ID="${SESSION_ID:-qa-standalone-$(date -u +%Y%m%d-%H%M%S)}"

# 3. Canonical paths + ensure dirs
eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"
che ensure_dirs "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD"

# 4. Double-guard: outputs NEVER in worktree
che assert_outside_worktree "$CHE_SESSION_DIR" "$WORKTREE_ROOT" --label "CHE_SESSION_DIR"
che assert_outside_worktree "$CHE_WORKSPACE_SHARED" "$WORKTREE_ROOT" --label "CHE_WORKSPACE_SHARED"

# 5. Construct QA output paths ONCE
QA_RELATED_ID="T${TASK_ID}-${TASK_SLUG}"
QA_REPORT_PATH="$(che output_path "report" "qa-run" "${QA_RELATED_ID}" "session" "md")"
QA_EVIDENCE_DIR="$(dirname -- "$(che output_path "qa" ".keep" "${QA_RELATED_ID}" "session" "tmp")")"
mkdir -p "$QA_EVIDENCE_DIR"
```

**DO NOT INVENT paths:** Every report, evidence screenshot, console capture, build log stays UNDER `$QA_EVIDENCE_DIR` or uses `$QA_REPORT_PATH`. Do not create `./qa-report.md`, `/tmp/qa-run.md` or worktree-relative paths. `stage E test names lint` uses `$QA_EVIDENCE_DIR/test-names.txt` instead of `/tmp/qa-test-names.txt`.

### -0.1.1 EVIDENCE RETENTION POLICY (ONDA4 — TWO LOCALS, NEVER IN USER WORKTREE)

```bash
# =============================================================
# DOUBLE LOCAL POLICY — engineering-contracts §20 MORATORIUM:
# NO evidence/manifest is written inside WORKTREE_ROOT/*
# by default. Override = user explicitly asks VERBATIM.
# =============================================================

# --- LOCAL 1 — EPHEMERAL / SESSION-SCOPE (heavy, TTL 30 days) ---
# FULL-size screenshots, complete STDOUT/STDERR build logs,
# trace files, raw test diffs. Stays in session.
# Cleanup handoff: sessions older than 30 days = TTL.
SESSION_EVIDENCE_DIR="$QA_EVIDENCE_DIR" # already created above
# Mandatory substructure (create if missing):
mkdir -p "$SESSION_EVIDENCE_DIR/screenshots" "$SESSION_EVIDENCE_DIR/logs" "$SESSION_EVIDENCE_DIR/builds"

# --- LOCAL 2 — DURABLE / WORKSPACE-SHARED (light audit trail) ---
# Canonical path via contract helper type=qa scope=workspace related_id=commit_7char.
# ONLY CONTAINS:
#   (i)   evidence_manifest_<SHA256_MANIFEST>.json
#   (ii)  1 FINAL JPEG/PNG thumbnail per AC PASS ≤200KB
CURRENT_COMMIT_7CHAR="${CURRENT_COMMIT_7CHAR:-$(cd "$WORKTREE_ROOT" && git rev-parse --short=7 HEAD 2>/dev/null || echo "HEAD-detached")}"
WORKSPACE_EVIDENCE_AUDIT_DIR="$(che output_path "qa" "audit" "commit-${CURRENT_COMMIT_7CHAR}" "workspace" "tmp")"
WORKSPACE_EVIDENCE_AUDIT_DIR="$(dirname -- "$WORKSPACE_EVIDENCE_AUDIT_DIR")"
mkdir -p "$WORKSPACE_EVIDENCE_AUDIT_DIR"
che assert_outside_worktree "$WORKSPACE_EVIDENCE_AUDIT_DIR" "$WORKTREE_ROOT" --label "WORKSPACE_EVIDENCE_AUDIT_DIR (durable hash manifest)"
```

**MANDATORY Manifest JSON Schema (NON-EMPTY fields, except thumbnail_path if no UI):**

```json
{
  "generated_at_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "commit_7char": "abc1234",
  "session_id": "<CHE_CURRENT_SESSION_ID>",
  "qa_run_passed": true,
  "related_id": "T${TASK_ID}-${TASK_SLUG}",
  "per_test_file_sha256": {
    "/abs/path/worktree/packages/x/test.spec.ts": "<sha256 hex 64>",
    "/abs/path/worktree/packages/y/api.test.ts": "<sha256>"
  },
  "per_evidence_sha256": {
    "screenshots/build-A-fail.png": "<sha256>",
    "logs/stage-D-test-fail.log": "<sha256>"
  },
  "per_behavior_result": {
    "B-1": "PASS",
    "B-2": "PASS",
    "AB-1": "PASS"
  },
  "thumbnail_path": "commit-abc1234-thumbnail-final.jpg"
}
```

**Thumbnail rule ≤200KB:** If QA run produces Playwright/UI screenshots, copy the FINAL one (last THEN) to Local 2, with resize width=800px JPEG quality=75%. If PNG doesn't fit, reduce dimensions until it passes. If no UI → thumbnail_path = null.

---

## 0. Preconditions

Must receive from Scrum Master:
- `WORKTREE_ROOT` (absolute path)
- Task ID
- List of modified files (from Dev pre-report)
- Change type hints: e.g. `domain-function`, `ui-component`, `api-route`, `db-migration`, `config`

If any missing → ABORT, go back to SM.

### 0.1 How to write final QA report to DISK (FAIL or PASS)

After producing structured report (FAIL Stage A-D-E template or §3 PASS template), **write to file outside worktree using atomic write:**

```bash
# DO NOT "cat > ./qa-report.md" (falls inside worktree!)
# DO NOT "cat > /tmp/qa-task-T1.md" (loses sortability by related_id/timestamp)
{
  echo "# QA Run Report — T${TASK_ID}-${TASK_SLUG}"
  echo "> Generated at: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "> Related ID: ${QA_RELATED_ID}"
  echo "> Engine: stack detected in §1"
  echo
  # ... paste complete FAIL template OR §3 PASS template content here ...
} | che write_file_atomic "$QA_REPORT_PATH"
```

Then append 1 audit trail line:
```bash
che decision_append "$WORKTREE_ROOT" "QA_RUN" "{\"related_id\":\"${QA_RELATED_ID}\",\"task_id\":\"${TASK_ID}\",\"passed\":${QA_PASSED:-false},\"report_path\":\"${QA_REPORT_PATH}\",\"evidence_dir\":\"${QA_EVIDENCE_DIR}\"}"
```

### 0.2 FINAL MANDATORY STEP — Generate Evidence Manifest SHA256 (ONDA4 Local 2 Workspace Audit)

After writing report and audit log, **before returning to SM**, generate Local 2 JSON manifest ($WORKSPACE_EVIDENCE_AUDIT_DIR created in §-0.1.1):

```bash
# (a) Calculate SHA256 for EACH test file changed in this task's diff
declare -A PER_TEST_FILE_SHA
while IFS= read -r f; do
  [ -f "$f" ] || continue
  sha="$(sha256sum "$f" | awk '{print $1}')"
  PER_TEST_FILE_SHA["$f"]="$sha"
done < <(cd "$WORKTREE_ROOT" && git diff --name-only HEAD -- '*.test.*' '*.spec.*' '__tests__/**' 2>/dev/null || true)

# (b) Calculate SHA256 for EACH generated evidence file (Local 1 Session)
declare -A PER_EVIDENCE_SHA
while IFS= read -r ev; do
  [ -f "$ev" ] || continue
  rel_ev="${ev#$SESSION_EVIDENCE_DIR/}"
  sha="$(sha256sum "$ev" | awk '{print $1}')"
  PER_EVIDENCE_SHA["$rel_ev"]="$sha"
done < <(find "$SESSION_EVIDENCE_DIR" -type f 2>/dev/null || true)

# (c) Build JSON manifest (inline — minimum deps; use jq if available, else printf)
GENERATED_AT_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
MANIFEST_TMP="$(mktemp)"
{
  printf '{\n'
  printf '  "generated_at_utc": "%s",\n' "$GENERATED_AT_UTC"
  printf '  "commit_7char": "%s",\n' "$CURRENT_COMMIT_7CHAR"
  printf '  "session_id": "%s",\n' "${SESSION_ID:-qa-standalone}"
  printf '  "qa_run_passed": %s,\n' "$( [ "${QA_PASSED:-false}" = "true" ] && echo true || echo false )"
  printf '  "related_id": "%s",\n' "$QA_RELATED_ID"
  printf '  "per_test_file_sha256": {'
  first=1
  for k in "${!PER_TEST_FILE_SHA[@]}"; do
    [ $first -eq 0 ] && printf ','
    printf '\n    "%s": "%s"' "$k" "${PER_TEST_FILE_SHA[$k]}"
    first=0
  done
  [ $first -eq 0 ] && printf '\n  '; printf '},\n'
  printf '  "per_evidence_sha256": {'
  first=1
  for k in "${!PER_EVIDENCE_SHA[@]}"; do
    [ $first -eq 0 ] && printf ','
    printf '\n    "%s": "%s"' "$k" "${PER_EVIDENCE_SHA[$k]}"
    first=0
  done
  [ $first -eq 0 ] && printf '\n  '; printf '},\n'
  printf '  "per_behavior_result": %s,\n' "${PER_BEHAVIOR_RESULT_JSON:-{\}}"
  # (d) Thumbnail ≤200KB: copy last Playwright/UI screenshot final, resize
  THUMB_FINAL=""
  LAST_SCREENSHOT="$(find "$SESSION_EVIDENCE_DIR/screenshots" -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \) 2>/dev/null | sort | tail -1 || true)"
  if [ -n "$LAST_SCREENSHOT" ] && command -v convert >/dev/null 2>&1; then
    THUMB_OUT="$WORKSPACE_EVIDENCE_AUDIT_DIR/commit-${CURRENT_COMMIT_7CHAR}-thumbnail-final.jpg"
    convert "$LAST_SCREENSHOT" -resize 800x -quality 75 "$THUMB_OUT" 2>/dev/null
    THUMB_SIZE="$(stat -c%s "$THUMB_OUT" 2>/dev/null || echo 999999)"
    if [ "$THUMB_SIZE" -gt 204800 ]; then
      convert "$THUMB_OUT" -resize 640x -quality 65 "$THUMB_OUT" 2>/dev/null || true
    fi
    THUMB_NEW_SIZE="$(stat -c%s "$THUMB_OUT" 2>/dev/null || echo 999999)"
    [ "$THUMB_NEW_SIZE" -le 204800 ] && THUMB_FINAL="$(basename -- "$THUMB_OUT")"
  fi
  if [ -n "$THUMB_FINAL" ]; then
    printf '  "thumbnail_path": "%s"\n' "$THUMB_FINAL"
  else
    printf '  "thumbnail_path": null\n'
  fi
  printf '}\n'
} > "$MANIFEST_TMP"

# (e) Calculate SHA256 OF THE MANIFEST ITSELF (for filename + integrity)
MANIFEST_SHA="$(sha256sum "$MANIFEST_TMP" | awk '{print $1}')"
MANIFEST_SHORT_SHA="${MANIFEST_SHA:0:16}"
MANIFEST_FILENAME="evidence_manifest_${MANIFEST_SHORT_SHA}.json"
MANIFEST_FINAL_PATH="$WORKSPACE_EVIDENCE_AUDIT_DIR/$MANIFEST_FILENAME"
cat "$MANIFEST_TMP" | che write_file_atomic "$MANIFEST_FINAL_PATH"
rm -f "$MANIFEST_TMP"

# (f) ONDA4 Decision log entry with hash + paths
che decision_append "$WORKTREE_ROOT" "QA_EVIDENCE_MANIFEST" "{\"commit_7char\":\"${CURRENT_COMMIT_7CHAR}\",\"manifest_sha256\":\"${MANIFEST_SHA}\",\"manifest_path\":\"${MANIFEST_FINAL_PATH}\",\"workspace_audit_dir\":\"${WORKSPACE_EVIDENCE_AUDIT_DIR}\",\"session_evidence_dir\":\"${SESSION_EVIDENCE_DIR}\"}"

# (g) EXPORT to QA success report template (§3):
QA_EVIDENCE_MANIFEST_SHA="$MANIFEST_SHA"
QA_EVIDENCE_MANIFEST_PATH="$MANIFEST_FINAL_PATH"
```

---

## 1. STEP 1 — STACK AUTODETECTION

Scan worktree and build a `Stack Profile` (in-memory, then to report):

### 1.1 Language / Runtime signals

| Signal | Indicates |
|---|---|
| `package.json` exists + has deps | JavaScript / TypeScript project |
| `tsconfig.json` exists | TypeScript → needs typecheck |
| `Cargo.toml` | Rust → `cargo test`, `cargo clippy` |
| `go.mod` | Go → `go test`, `go vet` |
| `pyproject.toml` OR `requirements.txt` | Python → pytest / ruff / mypy |
| `Makefile` | Run whatever targets are defined |
| `justfile` | `just <target>` |
| `nx.json` | Nx monorepo → use Nx commands |
| `pnpm-workspace.yaml` | pnpm monorepo |
| `turbo.json` | Turborepo → `turbo run <target>` |

### 1.2 Framework / Build signals

| Signal | Commands to try |
|---|---|
| `next.config.*` | Next.js → `next build`, `next lint` |
| `vite.config.*` | Vite → `vite build` |
| `angular.json` | Angular CLI → `ng build`, `ng test` |
| `nest-cli.json` | Nest → `nest build` |
| `playwright.config.*` | Playwright E2E available (DO NOT run per-task unless task is E2E) |
| `cypress.config.*` | Cypress E2E |

### 1.3 Linter / Formatter signals

| Signal | Tool |
|---|---|
| `biome.json` OR `biome.jsonc` | Biome → `biome check <files>`, `biome lint <files>` |
| `.eslintrc*` OR `eslint.config.*` | ESLint → `eslint <files>` |
| `.prettierrc*` | Prettier (formatting check only per-task) |
| `ruff.toml` OR `pyproject.toml` has `[tool.ruff]` | Ruff |
| `.clippy.toml` OR Rust project | `cargo clippy` |
| `.golangci.yml` | golangci-lint |

### 1.4 Test runner signals

| Signal | Runner |
|---|---|
| `vitest.config.*` OR `package.json` has vitest devDep | Vitest → `vitest run` |
| `jest.config.*` OR package.json has jest | Jest → `jest` |
| `Cargo.toml` with `[dev-dependencies]` | Rust → `cargo test` |
| `go.mod` | Go → `go test ./...` |
| `pyproject.toml` has pytest | Python → `pytest -q` |
| `nx.json` + `project.json` files | `nx affected:test --tui false` or per-project target |

---

## 2. STEP 2 — EXECUTION ORDER (DO NOT skip or reorder)

The execution pipeline. Each stage FAILS → report immediately → DO NOT run later stages.
All commands run from `WORKTREE_ROOT`.

### 2.0 PREP: narrow down scope per task

Build an `--affected` / scoped list if possible:
- **Nx monorepo**: Prefer `nx affected:<target> --tui false` over running the whole repo.
- **Turbo**: `turbo run <target> --filter=...[HEAD~1]` or similar.
- **Single repo**: Target modified files for lint/typecheck; run test file(s) touching them.

### 2.1 Stage A — Build (compile / type-level validation)

Goal: catch type and syntax errors first.

Priority order (pick FIRST that applies):
1. Monorepo build of affected packages:
   - Nx: `corepack pnpm nx run-many -t build --tui false --projects=<affected-projects>`
   - Turbo: `corepack pnpm turbo build --filter=...[HEAD~1]`
2. Single project build:
   - JS/TS: `corepack pnpm build` or `corepack pnpm -C <subdir> build`
   - Rust: `cargo build --tests`
   - Go: `go build ./...`
   - Python: `python -m compileall src/`

**FAIL report format if build fails:**
```
Stage A — BUILD FAILED
Error summary (from compiler output, first 20 lines only):
  - <file>:<line>: <message>
  - <file>:<line>: <message>
Root cause hypothesis: <short description in English if obvious, else "unknown">
Action needed for Dev: <specific fix direction>
```

### 2.2 Stage B — Lint / Formatting check

Goal: catch style, security-lint, dead code, and PII-lint issues.

Priority (pick FIRST that applies):
1. **Biome**: `corepack pnpm biome check <scoped files or entire project>`
   - If fails → also run `corepack pnpm biome lint`
2. **ESLint + Prettier**:
   - `corepack pnpm eslint <scoped files>`
   - `corepack pnpm prettier --check <scoped files>`
3. **Rust**: `cargo clippy -- -D warnings`
4. **Python**: `ruff check <scoped dirs>`
5. **Go**: `go vet ./...`
6. **Generic**: check for `lint` script in package.json / Makefile → run it.

**FAIL report format if lint fails:**
```
Stage B — LINT FAILED
Rule violations (grouped by file, 20 max):
  - <file>:<line>:<rule_id>: <message> (severity: error/warn)
Suggested auto-fix command:
  - <exact command if applicable, e.g. "corepack pnpm biome check --apply">
```

### 2.3 Stage C — Typecheck (if language has type system)

Only if applicable (TS/Rust with strict, Python with mypy etc.).
DO NOT rely on build alone — typecheck stage is explicit.

Priority:
1. TypeScript: `corepack pnpm tsc --noEmit` (or monorepo per-project: `nx run-many -t typecheck --tui false`)
2. Python (if mypy configured): `mypy <scoped files>`
3. Rust: covered by build + clippy.

**FAIL report format:**
```
Stage C — TYPECHECK FAILED
Errors (grouped by file, top 30):
  - <file>:<line>: <TS error code & message>
```

### 2.4 Stage D — Unit & Integration Tests

Goal: catch behavior regressions. DO NOT run full E2E per task (too slow).

**Per-task scoping rules:**
- Only run tests **affected by changed files**.
- Pure function / domain changes: **unit tests first**.
- API route / service changes: **integration tests second**.
- Full suite only if scope very small (≤ 3 files) OR explicitly told by SM.

Priority:
1. **Vitest**:
   - Scoped: `corepack pnpm vitest run <pattern matching changed files or their spec files>`
   - Fallback: `corepack pnpm test`
2. **Jest**: similar pattern
3. **Nx**: `corepack pnpm nx affected:test --tui false`
4. **Rust**: `cargo test` (if changed crates only: `-p <crate>`)
5. **Go**: `go test <scoped packages>`
6. **Python**: `pytest -q <scoped paths>`
7. **Generic**: look for `test` / `test:unit` script → run it.

**FAIL report format:**
```
Stage D — TEST FAILED
Failing spec files / test cases (top 20):
  - <file>: <test suite name> > <test case>
    Expected: <expected>
    Received: <received>
    Error: <first line of stack>
Reproduction command:
  - <exact command Dev can run to re-trigger failing test>
```

### 2.5 Stage E — Test Naming Behavioral Lint (Che RULE 7.9)

Goal: ensures `describe()` / `it()` / `test()` describe OBSERVABLE BEHAVIOR, not internal IDs. Runs ONLY if `*.test.*`, `*.spec.*` or `__tests__/` modified.

**🔴 HARD RULE — PROHIBITED INVERSION (NEVER do this):**
> ❌ **WRONG:** Report WARN / FAIL because a test title DOES NOT CONTAIN `FLO-xxx` / `T<N>` / `AC<N>`.
> ✅ **CORRECT:** Having these IDs IN THE TITLE is BAD = finding. NOT HAVING THEM and describing behavior is GOOD = compliant = NEVER report finding for missing ID.
>
> **1-sentence decision:** `title contains FLO-ID → BAD finding. title does NOT contain FLO-ID → GOOD (no finding).`
> **Correct traceability** (always OK): JSDoc comment `/** @ticket FLO-714 · @ac 3.1 */` ABOVE block OR `// @ticket FLO-714 | @ac 3.1 | @task T1.2` 1st line INSIDE block.

**What to detect (regex ONLY IN TITLE STRING — comments ignored):**
Scan string passed to `describe(...)`, `it(...)`, or `test(...)`:
- Ticket IDs in TITLE: `FLO-\d+`, `[A-Z]{2,}-\d+`
- Task/item IDs in TITLE: `Task?\s*T\d+(\.\d+)?`, `Item\s*\d+`
- AC/section IDs in TITLE: `AC\s*\d+`, `§\s*\d+(\.\d+)?`, `REGRA\s*\d+`, `SPEC[_-]\w+`
- Phase/story IDs in TITLE: `Fase\s*\d+`, `Story\s*#?\d+`, `PRD\s*§`

**How to scan (simplest possible — grep -E):**
```bash
cd <WORKTREE_ROOT>
git diff --cached --unified=0 -- <changed spec files> | grep -E '^\s*\+' \
  | grep -Eo '\b(describe|it|test)\s*\(\s*["'\''"][^"'\''"]{1,240}["'\''"]' \
  > /tmp/qa-test-names.txt 2>/dev/null || true
Then for each title found check anti-patterns ABOVE only. Ignore JSDoc + body comments.
```

**Report output format (WARNINGS only when BAD titles PRESENT — NEVER flag "missing FLO prefix"):**
```
Stage E — TEST NAMING (RULE 7.9)
Total test titles scanned: 42
Behavioral (good, NO internal IDs in TITLE): 40
Bad titles detected (WARNING — internal IDs IN TITLE STRING): 2
  - <file>: it("Task T2.3 — validates AC 4.2 refund") — BAD in TITLE: contains "Task T2.3" and "AC 4.2"
  - <file>: describe("FLO-513 refund process")      — BAD in TITLE: contains "FLO-513"
Fix guidance: rename TITLES to describe BEHAVIOR only. Keep traceability links (@ac / @task / @ticket) in JSDoc comment above or 1-line comment inside block.
```

---

## 3. STEP 3 — IF ALL STAGES PASS — Success Report

```
QA RESULT: PASS (task <TASK-ID>)

Stack profile detected:
  - Runtime: <e.g. TS/Node 22, pnpm 9 via corepack>
  - Build: <Nx run-many build>
  - Lint: <Biome 1.9>
  - Typecheck: <tsc 5.6 --noEmit>
  - Tests: <Vitest 4.0 — 42 files, 318 tests>
  - Test naming lint (Stage E): 42 scanned; bad=0 ✔

Stages executed:
  - [x] Build (0 errors, 0 warnings)
  - [x] Lint (0 errors, 3 warnings — cosmetic, accepted)
  - [x] Typecheck (0 errors)
  - [x] Tests (0 failed; coverage diff: +0.4% lines)
  - [x] Test naming (Stage E: clean or <N bad names → <N> warnings)

Warnings for Dev to consider (non-blocking):
  - <list non-blocking issues, e.g. unused variable, TODO comment>
  - <if Stage E bad names: repeat list here as warnings>

Evidence retention (ONDA4):
  - Workspace audit manifest SHA256 = <QA_EVIDENCE_MANIFEST_SHA>
  - Manifest JSON path = <QA_EVIDENCE_MANIFEST_PATH>
  - Session full evidence (TTL 30d) = $CHE_SESSION_DIR/qa/T${TASK_ID}-${TASK_SLUG}/evidence/

Approved for Compliance stage.
```

---

## 4. STEP 4 — Return to Scrum Master

Always return:
1. Structured report (FAIL templates or Success above).
2. `qa_passed: true/false` boolean.
3. (If failed) A **numbered, actionable item list** for Developer.

**DO NOT fix code directly.** QA only reports; Developer fixes.

---

## Appendix A: Rule when you DON'T know how to proceed

If after Step 1 (stack detection) you still cannot figure out: build command, test runner, or how to scope to affected files:

**STOP → go back to Scrum Master → who will ASK user directly.**
DO NOT guess. NEVER run a command that could mutate worktree (e.g. `npm install`, `biome check --apply`) without explicit confirmation.

---

## Appendix B: Commands you MUST NEVER run

- Any command writing secrets or printing long env vars to stdout
- `rm -rf` outside a temp dir you created
- DB migrations / seed commands against production-looking URLs (block if host contains `prod`, `rds.amazonaws`, `supabase.co`, `cockroachlabs.cloud`, `neon.tech`)
- Deploy commands (`vercel deploy`, `railway up`, `kubectl apply`)
- Git commands rewriting history (`git push --force`, `git rebase`)
  - Exception: `git status`, `git diff`, `git log` (read-only) are fine.
