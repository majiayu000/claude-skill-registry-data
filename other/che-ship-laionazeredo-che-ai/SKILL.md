---
name: "che-ship"
description: "End-of-task ship command. EXECUTES 4 EXECUTABLE GATES in non-negotiable order BEFORE any git ops (fail-fast): §0.9.1 che-scope-checker (delivery+LEAN 6-checks, APPROVED≥7.0) → §0.9.2 che-code-review Mode B (0C + ≤2H auto-fix-and-commit WITHOUT asking user; else block) → §0.9.3 che-compliance HEAVY full scan (0C 0H) → §0.9.4 QA gate optional flag --run-qa. After: atomic conventional commits on worktree, git push, opens DRAFT PR against default branch with structured description, assigns PR to user. Invoke ONLY after all che tasks DONE, or when user explicitly runs /che-ship."
---

# Che — Ship (commit + push + open PR)

> **SHARED REFERENCES (CANONICAL — DO NOT DUPLICATE body here):**
> - Conventional Commits full types + regex + examples: engineering-contracts skill Appendix B
> - GitHub CLI gh auth + push + create PR commands: `_shared_checklists/GITHUB_CLI_COMMON.md`
> - gh-stack hierarchical PR workflow (multi-PR partial deliveries): engineering-contracts Appendix C
> - Light pre-ship security check: `_shared_checklists/SECURITY_PII_COMMON.md` (secrets leak, PII log scan)
> - QA run order local verification: `_shared_checklists/NX_PNPM_COMMON.md`

This skill handles the end-of-development workflow for a worktree.
It runs ONLY after the user says "I believe everything is OK" and is prepared to commit.

---

## 0. Preconditions — Non-negotiable (FAIL if any missing)

1. **Worktree confirmed.** Absolute path provided. If not — block.
2. **`gh` CLI is available and authenticated.** Run `gh auth status` silently. If not authenticated → guide user to `gh auth login` and stop.
3. **Worktree has uncommitted changes OR new commits ready to push.** `git status` is not clean OR branch is behind/ahead.
4. No uncommitted `.env` / secret files being committed.
5. (If the user ran via che) all tasks are marked DONE in `task_graph.md`. Compliance + scope + review gates are EXECUTABLE CODE in §0.9.1→§0.9.4 and will run NOW before any git operation; §0.5 item 5 legacy-text compliance requirement is replaced entirely by gate §0.9.3 execution. If user explicitly passed `--skip-gates` (override flag): log EXPLICIT_OVERRIDE entry to decision.log with user verbatim justification, SKIP all 4 gates, jump directly to §1 Git Housekeeping. No other bypass path exists.

If any precondition fails → report exactly which, stop execution, ask user.

### 0.6 gh-stack mode detection (N4 hierarchical PR stack)

1. Check if file exists: `$CHE_WORKSPACE_SHARED/gh_stack_plan.md` (`$CHE_WORKSPACE_SHARED` is exported by `che compute_paths`; see §0.7.1 preflight).
2. If it exists:
   - Read it. Validate it has a field `Status: APPROVED` at the top.
   - Check `gh` extension installed: run `gh extension list 2>/dev/null | grep -i "stack"` silently.
   - If gh-stack extension NOT installed → offer `gh extension install https://github.com/github/gh-stack` to user; wait for confirmation, install, then continue. If user declines → FALLBACK to single-PR mode (Steps 2–5 normal path).
   - Parse layers table bottom-up (first layer = lowest in the stack, merged first; last layer = top of stack). Extract per layer: `Layer ID`, `Branch Name` (slug like `PROJ-123-l1-refund-pipeline`), `Scope (files)`, `Depends on`.
   - Set boolean: `GH_STACK_MODE=true`. Record `LAYERS[]` array ordered bottom-up.
3. If file NOT exists OR status ≠ APPROVED → `GH_STACK_MODE=false`. Proceed with standard single-PR path (Steps 2–5 current).

### 0.7 WORKTREE SESSION BINDING PREFLIGHT (engineering-contracts §19, NON-NEGOTIABLE)

Run BEFORE any `git status / git add / git commit / git push`. PREVENTS wrong-worktree commits.

1. **Level 1 Global Index (AUTHORITY):** Read `$CHE_REGISTRY_PATH`. Find LAST STATUS=BOUND entry using the effective session id from `${CHE_SESSION_ID:-${HARNESS_SESSION_ID:-$SESSION_ID}}`. Extract WORKTREE_ROOT from that entry.
   - If NO entry: SHIP BLOCKED NOW. Ask "No Level1 binding for this session. Create before ship? (A = Select worktree; B = Cancel ship)." NEVER ship unbound.
   - If found BOUND entry: confirm WORKTREE_ROOT from registry **MUST EQUAL** WORKTREE_ROOT precondition 1.
   - MISMATCH → **BLOCK SHIP NOW.** Ask: "Level 1 GLOBAL registry binding says worktree = X, ship was invoked on Y. Which one actually ships? (A = X per binding; B = Y override binding + rebind; C = Cancel ship)." Never silent-continue.
2. **Level 2 Detail File (optional audit):** Verify `$CHE_SESSION_DIR/binding.md` exists (`$CHE_SESSION_DIR` is exported by `che compute_paths` — see §0.7 preflight). If missing → warn decision.log entry (SM skipped Level 2 write). Do NOT block ship (Level 1 is the authority).
3. **Scissor check staging + file ops:**
   - EVERY file staged/committed → path MUST start with WORKTREE_ROOT from Level1 registry.
   - Generated files under `$CHE_SESSIONS_ROOT/**` are NEVER staged; they live outside user code by design.
   - File path outside WORKTREE_ROOT and not under CHE_SESSIONS_ROOT (symlinks, relative tricks, etc.) → UNSTAGE immediately, report, DO NOT commit.
4. **Cross-worktree safety during ship loop (gh-stack mode):**
   - After finishing layer's commit/push/PR, NEXT layer file ops → RE-RUN scissor check (3) against BOUND WORKTREE_ROOT registry entry.
   - Never silent cd another worktree during multi-layer ship. Layer says "use worktree B" → STOP. Ask user confirm re-binding §19.3 (old entry STATUS=RELEASED append new BOUND registry entry) before switching.

---

### 0.7.1 MANDATORY STORAGE PREFLIGHT (run IMMEDIATELY after §0.7, BEFORE §0.8 or ANY report/decision write)

BEFORE generating ANY report file (gates 0.9.1→0.9.5), decision log, backup artifact: execute EXACTLY this command ONCE per /che-ship execution. **Ensures all paths resolve OUTSIDE the worktree:**

```bash
python3 -m che_core.ship preflight "$WORKTREE_ROOT" "$SESSION_ID"
```

Export the variables printed by the script to use them in the next gates.

---

### 0.8 PLANNING ARTIFACTS BLACKLIST PREFLIGHT (NON-NEGOTIABLE)

**Purpose:** NEVER allow che internal planning/decision files to end up in user-code PRs. If any bug/legacy skill accidentally creates them inside the user worktree, detect, unstage, and DELETE them before any `git add` runs.

Execute the blacklist verification script:

```bash
python3 -m che_core.ship blacklist_check "$WORKTREE_ROOT" "$SESSION_ID"
```

If the script reports tracked files (exit code 2), present options (A or B) to the user as suggested in the output.

---

## 0.9 EXECUTABLE QUALITY GATES (RUN BEFORE ANY GIT OPERATION — FAIL FAST ORDER)

> **CANONICAL 4-PASS ORDER (non-negotiable — fail-fast by blast radius):**
> 1. **§0.9.1 Scope + Lean delivery** (lowest compute cost, highest blast radius if wrong — shipping the wrong thing is the worst scenario)
> 2. **§0.9.2 Code Review bugs** (depends on scope being correct; ≤2 HIGH = auto-remediate WITHOUT asking)
> 3. **§0.9.3 Compliance security/PII** (since review and scope passed, we guarantee 0C 0H)
> 4. **§0.9.4 QA — DEFAULT ON, 3 profiles: minimal / normal / full** (no flag = `minimal` profile; `--qa=<profile>` flag selects; unique bypass = user EXPLICIT_OVERRIDE logged in decision.log)
>
> Any GATE with 🔴 status BLOCKS the ship. Gates 0.9.1 and 0.9.3 NEVER have auto-fix. Only Gate 0.9.2 has an auto-fix branch when threshold ≤ 2 HIGH findings. Gate 0.9.4 DOES NOT have a `--no-run-qa` flag. The only way to bypass is user EXPLICIT_OVERRIDE.

### 0.9.1 GATE 1 — che-scope-checker 6-checks (Mode B: Local Worktree)

**Purpose:** Ensure that what is about to be committed (1) delivers EVERYTHING promised in the scope and (2) has no overengineering / bloat / YAGNI violations. Executes the `che-scope-checker` skill in Mode B.

**Internal precondition of this gate:**
- `$CHE_WORKSPACE_SHARED` is exported by `che compute_paths` (see §0.7.1 preflight).

**Scope source auto-discover order (first match wins — DOES NOT cascade multiple sources):**
1. **Explicit envelope** → does `$CHE_WORKSPACE_SHARED/tasks/*/envelope.md` exist? (last DONE task in task_graph, take its envelope) → SCOPE_SOURCE=ENVELOPE.
2. **Local task graph** → does `<WORKTREE_ROOT>/task_graph.md` exist? → SCOPE_SOURCE=TASK_GRAPH. Reads list of Acceptance Criteria + Tasks marked DONE.
3. **Local/global che spec** → does a SPEC exist in `$CHE_WORKSPACE_SHARED/specs/**/*.md` (canonical), the legacy `$CHE_WORKSPACE_SHARED/spec_*.md`, OR `<WORKTREE_ROOT>/spec_*.md`? → SCOPE_SOURCE=SPEC. Extracts §5 Acceptance Criteria section.
4. **GitHub PR body (if PR URL provided via `--pr-url` flag)** → use `gh pr view <URL> --json body,title` → parse Acceptance Criteria bullet points. SCOPE_SOURCE=PR_BODY.
5. **No source found** → ⚠️ WARN + ASK user: "No scope source located. (A) Inform spec/envelope path manually; (B) Proceed WITHOUT scope validation (risk: shipping out of scope); (C) Cancel ship." If user chooses B → log EXPLICIT_OVERRIDE in decision.log, SKIP this gate, go to 0.9.2.

**Execution:**
1. Invoke `che-scope-checker` skill passing:
   - `--worktree <WORKTREE_ROOT>`
   - `--mode B`
   - `--scope-source <SCOPE_SOURCE>`
   - `--scope-path <file_path>`
   - `--report-out "$SHIP_SCOPE_CHECK_REPORT"` (variable from §0.7.1; UTC timestamp prefix + report/ship-wt-<slug>/ structure outside worktree)
2. Wait for return with `verdict` field + `final_score` field + `findings[]` (CHECK 1-6).

**Verdict handling (EXACT che-scope-checker §8 rule):**
| scope-checker Verdict | Gate 0.9.1 Action | Next step |
|---|---|---|
| 🟢 APPROVED (score ≥7.0 AND 0 🔴 in CHECKS 1–6) | ✅ PASS GATE 1 | Proceed immediately to §0.9.2 |
| 🟡 CONDITIONS (score ≥7.0 but has some non-blocking action item OR score 5.0–6.9) | ⏸️ PAUSE + ASK user | Print findings and action items to user. EXACT options: **(A) = Apply suggested fixes and re-run gate 1; (B) = Conditionally approve (mandatory justification → recorded via decision.log helper); (C) = Cancel ship.** |
| 🔴 REJECTED (score <5.0 OR any 🔴 in CHECK 1 Delivery / CHECK 4 Env / CHECK 3 Mandatory Docs) | 🔴 BLOCK SHIP | Present findings to user. DOES NOT offer direct override option (requires new round). Suggest: fix → run standalone /che-scope-checker → then re-run /che-ship. |

**Output artifacts:**
- `$SHIP_SCOPE_CHECK_REPORT` — full 6-checks report with SCOPE × LEAN final score. Final structure: `$CHE_WORKSPACE_SHARED/report/ship-<wt-slug>/YYYYMMDD-HHMMSS-ship-scope-check.md` (sorted by timestamp prefix, grouped by related worktree).
- Decision log entry via official helper: `che decision_append "$WORKTREE_ROOT" "SHIP_GATE_0_9_1" "verdict=${verdict} score=${final_score} source=${SCOPE_SOURCE} report=${SHIP_SCOPE_CHECK_REPORT}"`.
- NO artifact is created inside `<WORKTREE_ROOT>` (assert outside helper already locks exit 99 if path lands there; §0.8 blacklist ensures redundant cleanup).

---

### 0.9.2 GATE 2 — che-code-review Mode B Local Worktree + **THRESHOLD ≤ 2 HIGH AUTO-FIX RULE (USER VERBATIM CONTRACT)**

> **NON-NEGOTIABLE USER VERBATIM RULE:**
> _"in the case of code review, in the case of <= 2 high findings, already fix and commit and proceed with ship without even asking me. But otherwise, perfect."_
> **This rule has no exceptions.** ASK NOTHING to the user in the ≤ 2 HIGH branch. Auto-remediate, commit, proceed. If CRITICAL ≥1 or HIGH ≥3 → block and present.

**Purpose:** Run `che-code-review` skill in **Mode B — Local Worktree** (diff of current worktree against `<DEFAULT_BRANCH>` already determined in preamble). Post-processing of the result with the ≤ 2 HIGH threshold rule.

**Step-by-Step Execution:**

**Step 2.0 — Base diff preparation:**
1. Reuse `DEFAULT_BRANCH` which will already be determined in §1.2 (if gate 2 runs before §1, just execute `gh repo view --json defaultBranchRef` silently).
2. Base diff = `origin/<DEFAULT_BRANCH>..HEAD` (commits already made in this branch) PLUS current unstaged + uncommitted changes in worktree. **Both are reviewed.** Not just staged.

**Step 2.1 — che-code-review invocation:**
1. Invoke `che-code-review` skill with params:
   - `--worktree <WORKTREE_ROOT>`
   - `--mode B`
   - `--base origin/<DEFAULT_BRANCH>`
   - `--report-out "$SHIP_CODE_REVIEW_REPORT"` (variable from §0.7.1; helper guaranteed outside worktree)
   - `--include-unstaged true`
2. Wait for structured result: `{ critical_count: N, high_count: N, medium_count: N, low_count: N, findings: [...] }`
   - Each finding has: `{ severity: CRITICAL|HIGH|MEDIUM|LOW, file, line, title, suggested_fix_code_block (optional), auto_fixable: boolean }`.

**Step 2.2 — THRESHOLD BRANCHING (core user rule — IMPLEMENT EXACTLY):**

```
IF (critical_count === 0) AND (high_count <= 2):
    → AUTO-REMEDIATE-AND-CONTINUE BRANCH (WITHOUT ASKING ANYTHING TO USER — NEVER ASK HERE)
ELSE:
    → BLOCK-SHIP BRANCH (present findings to user)
```

---

#### BRANCH A: AUTO-REMEDIATE-AND-CONTINUE (0 CRITICAL + ≤ 2 HIGH)

**Goal:** Automatically fix HIGH findings that are `auto_fixable=true`, commit with conventional commit, and proceed to gate 0.9.3 **without any user interaction.**

**2.A.1 — Filter auto-fixable HIGH findings:**
```
<FIXABLE_HIGHS> = findings.filter(f => f.severity === 'HIGH' AND f.auto_fixable === true)
<UNFIXABLE_HIGHS> = findings.filter(f => f.severity === 'HIGH' AND f.auto_fixable === false)
```
- `UNFIXABLE_HIGHS` (if any, ≤ 2 total): **still proceed without asking user.** The rule is ≤2 total HIGH, regardless of being fixable or not. Log WARNING in decision.log with each unfixable finding listed. DO NOT block.

**2.A.2 — Apply fixes programmatically:**
For each `f` in `<FIXABLE_HIGHS>`:
1. Read target file (via Read tool, guaranteed latest content).
2. Apply `Edit` tool exactly using `f.suggested_fix_code_block` as `new_string`, replacing corresponding old_string.
3. DO NOT add comments in edits. Maintain file style.
4. If any Edit fails (old_string mismatch): **abort only this specific finding**, log `AUTO_REMEDIATE_FAILED` in decision.log with file+line, continue with others. Do not abort Branch A.

**2.A.3 — Commit remediation with conventional commit (WITHOUT going through normal §1 — special commit):**
```bash
cd "$WORKTREE_ROOT"
# 1. Re-run §0.8 blacklist stages 1-2 just for safety (ensure no artifact entered diff):
#    (run same §0.8 stage 1 + 2 commands for unstaged)
# 2. Stage only files modified by auto-fixes:
git add -- <files_changed_by_fixes>
# 3. EXACT conventional commit:
N_FIXED=<total_high_fixes_applied>
N_TOTAL_HIGH=<high_count>
git commit -m "fix(review): auto-remediate code review HIGH findings ($N_FIXED/$N_TOTAL_HIGH)

- Applied automated remediation for ≤ 2 HIGH findings per ship gate 0.9.2 rule
- Remediation source: che-code-review Mode B against origin/<DEFAULT_BRANCH>
- Unfixed HIGH (<= count) logged to decision.log as AUTO_REMEDIATE_UNFIXABLE"
```

**2.A.4 — Post-commit:**
- Decision log entry via official helper:
  ```bash
  che decision_append "$WORKTREE_ROOT" "SHIP_GATE_0_9_2" "verdict=AUTO_REMEDIATED_PASSED critical=0 high=${N_TOTAL_HIGH} auto_applied=${N_FIXED} auto_failed=${Y} report=${SHIP_CODE_REVIEW_REPORT}"
  ```
- **PROCEED IMMEDIATELY TO GATE §0.9.3.** DO NOT RETURN to normal §1 Git Housekeeping. Special commit already done. Normal §1 will run and account only for remaining changes (if any).

---

#### BRANCH B: BLOCK SHIP (CRITICAL ≥ 1 OR HIGH ≥ 3)

**Rule:** Present detailed findings to user and ask for input. NO auto-fix in this branch.

EXACT options to user:
```
🔴 SHIP GATE 0.9.2 CODE REVIEW BLOCKED
  Summary: <critical_count> CRITICAL · <high_count> HIGH · <medium_count> MEDIUM · <low_count> LOW

  (Top findings first — print only CRITICAL + HIGH to user; medium/low go to report only)

Options:
  A = I want to apply fixes MANUALLY now. Pause ship, back to interactive shell.
      (After user fixes, they run /che-ship again)
  B = Reject specific findings + override. Need: mandatory justification per
      finding to be overridden (save to decision.log).
  C = Cancel ship.
```

If user chooses B (override):
- Each overridden finding requires free-text justification.
- All saved in decision.log as `REVIEW_OVERRIDE {finding_id, justification}` entries.
- Change gate verdict to PASSED_WITH_OVERRIDES.
- **ONLY ALLOW OVERRIDE UP TO 2 HIGH total.** If HIGH ≥3 → option B is disabled.
- **NEVER PERMIT CRITICAL OVERRIDE — option B disabled if critical_count > 0.**

---

**Output artifacts gate 0.9.2:**
- `$SHIP_CODE_REVIEW_REPORT` — full findings report. Final structure: `$CHE_WORKSPACE_SHARED/report/ship-<wt-slug>/YYYYMMDD-HHMMSS-ship-code-review.md` (sorted, grouped).
- Decision log entries via `che decision_append` helper according to Branch A or B.
- Branch B: If OVERRIDE, each overridden finding uses: `che decision_append "$WORKTREE_ROOT" "REVIEW_OVERRIDE" "finding_id=${id} justification=${text}"`.
- Branch A has 1 new commit in worktree prefixed `fix(review): auto-remediate...`.

---

### 0.9.3 GATE 3 — che-compliance HEAVY FULL SCAN (Heavy Step 2, not just diff)

**Purpose:** Ensure 0 CRITICAL + 0 HIGH findings in the **ENTIRE REPO**, not just the diff. Executes the `che-compliance` skill in its HEAVY Step 2 version (full-session scan, not diff-only). This is the old §0.5 compliance rule, now turned into executable code.

**Execution:**
1. Invoke `che-compliance` skill with params:
   - `--worktree <WORKTREE_ROOT>`
   - `--mode HEAVY_STEP_2_FULL_SCAN`
   - `--report-out "$SHIP_COMPLIANCE_HEAVY_REPORT"` (variable from §0.7.1; helper guaranteed outside worktree)
   - `--required 0_CRITICAL_AND_0_HIGH`
2. Wait for result: `{ critical_count: N, high_count: N, scan_categories_ran: [1..15] }`

**Verdict handling:**
| Scenario | Action |
|---|---|
| `critical_count === 0 AND high_count === 0` | ✅ PASS GATE 3. Proceed to 0.9.4. |
| Any `critical_count > 0` OR `high_count > 0` | 🔴 **BLOCK SHIP — NO DIRECT OVERRIDE OPTION.** Present CRITICAL + HIGH list to user with paths and lines. Options: (A) Fix manually and re-run /che-ship; (B) Run standalone `che-compliance` first for verbose output, then return. |

**Compliance categories guaranteed to run (canonical from che-compliance skill Step 2 Heavy):**
- Category 1: Secrets leak (hardcoded API keys sk-*, AWS, JWT in text)
- Category 2: PII exposure (raw email log/return, SSN, sensitive data)
- Category 3: SQL injection patterns (string concat in SQL, no parameterisation)
- Category 4: Auth / RLS bypass patterns
- Category 5: Dangerous URLs (SSRF, open redirect)
- Categories 6-15: remaining from che-compliance skill.

**Output artifacts:**
- `$SHIP_COMPLIANCE_HEAVY_REPORT` — full scan report. Final structure: `$CHE_WORKSPACE_SHARED/report/ship-<wt-slug>/YYYYMMDD-HHMMSS-ship-compliance-heavy.md` (sorted, grouped).
- Decision log entry via official helper: `che decision_append "$WORKTREE_ROOT" "SHIP_GATE_0_9_3" "verdict=${verdict} critical=${critical_count} high=${high_count} categories=${#scan_categories_ran} report=${SHIP_COMPLIANCE_HEAVY_REPORT}"`.

---

### 0.9.4 GATE 4 — QA Gate (DEFAULT ON — `minimal` profile if no flag passed)

**Purpose:** Last line of defence before real commit. **ON BY DEFAULT — ALWAYS runs, unless user passes justified EXPLICIT_OVERRIDE.** 3 speed/comprehensiveness profiles. NO more `--no-run-qa` flag.

**Profile resolution (non-negotiable precedence):**
1. User passed `--skip-qa` in command → **REQUIRE user verbatim EXPLICIT_OVERRIDE** recorded in decisions.log. Without written override → **BLOCK SHIP NOW, ask user justification.**
2. User passed `--qa=full` → **PROFILE_FULL** (everything, ~5-15min)
3. User passed `--qa=normal` → **PROFILE_NORMAL** (affected typecheck+lint+test, ~1-3min)
4. **DEFAULT** (no QA flag) → **PROFILE_MINIMAL** (only affected unit/integ tests, ~30s-2min)

**When skipped (ONLY path 1):**
- If `--skip-qa` present AND EXPLICIT_OVERRIDE `QA_SKIP` recorded via `che decision_append "$WORKTREE_ROOT" "SHIP_GATE_0_9_4_OVERRIDE" "verbatim=<user justification>"` → SKIP, proceed to §1.
- **ANY OTHER skip path (without logged override) → BLOCKS SHIP.**

**Profile specs (stack-detect execution):**

Automatically detects monorepo stack (attempt order):
1. **Nx workspace (pnpm + nx)** → `nx.json` + `pnpm-workspace.yaml` exist:
   | Profile | Command chain | Target duration |
   |---|---|---|
   | 🟢 **MINIMAL (default)** | `cd "$WORKTREE_ROOT" && corepack pnpm nx affected:test --tui false --exclude=e2e 2>&1` (only unit/integ tests AFFECTED by dirty files — NO typecheck, NO lint, NO playwright/e2e) | ~30s-2min monorepo |
   | 🟡 **NORMAL (--qa=normal)** | `cd "$WORKTREE_ROOT" && { echo "===== QA GATE NORMAL: typecheck $(date -Iseconds) ====="; corepack pnpm nx affected:typecheck --tui false 2>&1; echo "===== QA GATE NORMAL: lint $(date -Iseconds) ====="; corepack pnpm nx affected:lint --tui false 2>&1; echo "===== QA GATE NORMAL: test $(date -Iseconds) ====="; corepack pnpm nx affected:test --tui false --exclude=e2e 2>&1; }` — affected: typecheck + lint + unit/integ tests | ~1-3min monorepo |
   | 🔴 **FULL (--qa=full)** | `cd "$WORKTREE_ROOT" && { echo "===== QA GATE FULL: typecheck $(date -Iseconds) ====="; corepack pnpm nx run-many --target=typecheck --tui false 2>&1; echo "===== QA GATE FULL: lint $(date -Iseconds) ====="; corepack pnpm nx run-many --target=lint --tui false 2>&1; echo "===== QA GATE FULL: unit+integ tests $(date -Iseconds) ====="; corepack pnpm nx run-many --target=test --tui false 2>&1; echo "===== QA GATE FULL: E2E tests $(date -Iseconds) ====="; corepack pnpm nx run-many --target=e2e --tui false 2>&1; }` — all: typecheck+lint+unit+integ+e2e+playwright | ~5-15min monorepo |
   Every output from any profile is recorded via pipe: `| che write_file_atomic "$SHIP_QA_GATE_LOG"`

2. **Generic pnpm/npm/yarn (no Nx)** → `package.json` exists:
   - MINIMAL: heuristic find matching test files: `grep` diff paths → run only `*.test.*` / `*.spec.*` files matching changed file dirs via `corepack pnpm vitest run <matched_paths>` (no typecheck, no lint)
   - NORMAL: `{ echo typecheck; corepack pnpm typecheck 2>&1; echo lint; corepack pnpm lint 2>&1; echo test; corepack pnpm test 2>&1; }`
   - FULL: all NORMAL + `corepack pnpm test:e2e 2>&1` (if script exists; otherwise WARN and skip)

3. **No detection** → WARN "Could not detect QA stack. MINIMAL fallback: attempts to run test command documented in AGENTS.md. If none → WARN + SKIP gate with decision.log entry SKIPPED_STACK_NOT_DETECTED".

**QA Verdict handling:**
- **MINIMAL profile:** only test command — exit code 0 → ✅ PASS. exit code != 0 → 🔴 BLOCK SHIP.
- **NORMAL profile:** exit code 0 in ALL 3 (typecheck + lint + test) → ✅ PASS. Any failure → 🔴 BLOCK.
- **FULL profile:** exit code 0 in ALL → ✅ PASS. Any failure → 🔴 BLOCK.
- **In any BLOCK (0.9.4):** Print tail -80 of error output to user. EXACT options:
  - (A) I want to fix manually now → pause ship, back to interactive shell (then user re-runs /che-ship).
  - (B) Override (REQUIRE user verbatim EXPLICIT_OVERRIDE text justifying WHY failing typecheck/lint/test MUST SHIP now — recorded in decision.log; override only allowed if (i) failure count is ≤2 known FLAKY tests AND (ii) justification cites an issue/ticket).

**Output artifacts:**
- `$SHIP_QA_GATE_LOG` — concatenated stdout of selected profile. Final structure: `$CHE_WORKSPACE_SHARED/report/ship-<wt-slug>/YYYYMMDD-HHMMSS-ship-qa-gate.log` (sortable timestamp, grouped). Atomic write via `che write_file_atomic` stdin pipe.
- Decision log entry via helper: `che decision_append "$WORKTREE_ROOT" "SHIP_GATE_0_9_4" "verdict=${verdict} profile=${MINIMAL|NORMAL|FULL} tc_status=${status} lint_status=${status} test_status=${status} e2e_status=${status|N/A} override_logged=${yes|no} log=${SHIP_QA_GATE_LOG} evidence_manifest_sha256=${QA_EVIDENCE_MANIFEST_SHA:-N/A} evidence_workspace_path=${QA_EVIDENCE_MANIFEST_PATH:-N/A}"`.

---

### 0.9.5 GATE 5 (NEW Three-Layer Domains v2) — Mandatory DOMAIN GATES for Non-Engineering Domains

> **Precedence order resolve effective_domain (STOP at first non-null match):** (1) SPEC frontmatter `domain:` field → (2) Project Level 1.5 registry `domains[0]` array first entry → (3) DEFAULT FALLBACK `engineering`.

Purpose: Same fail-fast engine G1-G4 generalised for ANY domain (ux/product/devops/copywriting/social/seo-analytics) using numerical thresholds, 1 automatic free retry, and HUMAN REQUIRED after 2nd failure. Same as engineering-contracts §6 DbC + §15 incremental BDD pattern. No "taste" or subjective evaluation allowed — all NUMERICAL threshold.

Execution steps (fixed order):

1. **Resolve `effective_domain`:** Read SPEC (same path as gate 0.9.1 scope) YAML `domain:` + fallback project registry `domains[]`. If both null/missing → `effective_domain = engineering`.
2. **IF `effective_domain === 'engineering'` → **SKIP GATE 5 COMPLETELY AND SILENTLY (0 log lines, 0 extra output).** Old sessions/specs WITHOUT `domain:` field have IDENTICAL behaviour to original v2. 100% backward compat guaranteed.
3. **IF `effective_domain !== 'engineering':`**
   a. **Check folder exists:** `${CHE_HOME:-$HOME/.che-ai}/domains/<effective_domain>/gates/` → MUST exist. Does not exist → **WARN "Domain <slug> has no gates implemented yet (phase 2 rollout). Skip §0.9.5."** Log decision entry helper:
      ```bash
      che decision_append "$WORKTREE_ROOT" "DOMAIN-GATES-WARN" "domain=${effective_domain} reason=no-gates-folder phase-2-rollout skip=TRUE"
      ```
      Proceed §0.9.6 ALL GATES PASSED normally.
   b. **Glob + sort alphabetical gate files:** `${CHE_HOME:-$HOME/.che-ai}/domains/<effective_domain>/gates/*.md`. Execution order = filename alphabetical order (same as G1→G2→G3→G4 convention). UX example: `accessibility-gate.md` executes BEFORE `pixel-check-gate.md`.
   c. **For EACH gate file (0.9.5.1, 0.9.5.2, ...):**
      - Parse file YAML frontmatter: `threshold_pass`, `retry_policy`, `log_format_decisions`, `tool_official`, `executable`.
      - If frontmatter missing → FAIL gate immediately: "Gate <filename> has no declared YAML threshold frontmatter. Invalid domain."
      - **Executability check — runs BEFORE anything else:** if the frontmatter declares `executable: false`, this gate has no working mechanism yet. **SKIP it. Do NOT attempt it, do NOT invent a result, do NOT report PASS.** A gate silently recorded as passed is worse than no gate at all, because it converts "never verified" into "verified". Log:
        ```bash
        che decision_append "$WORKTREE_ROOT" "DOMAIN-GATE-SKIPPED-NOT-IMPLEMENTED" "domain=${effective_domain} gate=${GATE_BASENAME} blocked_by=${BLOCKED_BY} skip=TRUE"
        ```
        `executable: false` MUST come with `blocked_by:` naming what is missing. Without it the skip is indistinguishable from a pass → FAIL immediately instead of skipping.
      - **Build report path PER gate using helper (one JSON file per gate, sorted, grouped):**
        ```bash
        GATE_BASENAME="$(basename "$gate_file" .md)"
        DOMAIN_GATE_REPORT="$(che output_path report "domain-gate-${effective_domain}-${GATE_BASENAME}" "${RELATED_ID}" workspace json)"
        ```
      - **Run gate evaluation (automatic):** Follow EXACTLY the steps listed in `domains/<slug>/gates/<name>.md` "Execution" section. Record all gate output in JSON report via `che write_file_atomic "$DOMAIN_GATE_REPORT"` (atomic write, guaranteed outside worktree). If gate uses an official tool via §21 External Connectors (P1 MCP or P2 CLI): ALWAYS use P1→P2 order channels; NEVER raw curl/fetch.
      - `PASS condition`: `threshold_pass` frontmatter satisfied NUMERICALLY (e.g. `score >= 8.0`, `critical_count === 0`). If string → FAIL.
      - Verdict:
        | 1st round gate result | Action |
        |---|---|
        | 🟢 PASS threshold | ✅ Passes this gate. Decision log helper: `che decision_append "$WORKTREE_ROOT" "DOMAIN-GATE-EXECUTED" "domain=${effective_domain} gate=${GATE_BASENAME} status=PASS score=${score} duration_ms=${ms} report=${DOMAIN_GATE_REPORT}"`. Next gate. |
        | 🔴 FAIL threshold (1st time) | **AUTOMATIC FREE Retry = 1 single round:** Apply recommended steps in gate file "Retry Policy" section (e.g. "fix top-3 deviations >4px", "fix missing alt"). Re-run gate 1 NEW time with `--attempt 2`. Decision log helper for retry: `che decision_append "$WORKTREE_ROOT" "DOMAIN-GATE-RETRY" "domain=${effective_domain} gate=${GATE_BASENAME} score_before=${sb} retry=1"`. **This is the whole retry budget** — a third pass is refused by the runner (exit `2`) unless the user's verbatim `--override-reason` is supplied, so the loop cannot run past it. Before re-running, check `design_map_sha256` in the previous report: a changed digest means the check was *moved*, not retried, and the two scores are not comparable. |
        | 🔴 FAIL threshold AFTER automatic retry = 2nd failure | **HARD STOP §0.9.5 DOMAIN GATES.** Does not open PR. Does not commit. Does not proceed to §0.9.6. Decision log HELPER with details: `che decision_append "$WORKTREE_ROOT" "DOMAIN-GATE-HARD-FAIL" "domain=${effective_domain} gate=${GATE_BASENAME} threshold=${orig} score_now=${sn} report=${DOMAIN_GATE_REPORT}"`. Show standardised message to user. |
        | 🟡 INCONCLUSIVE | **HARD STOP. NOT a skip, NOT a retry, NOT a pass.** The gate ran and could not measure — so there is no score to retry against, and reporting it as PASS would convert "never verified" into "verified". Classify the report's `reason` BEFORE acting on it, because only one class is repairable and the other two are not loops at all: **(a) procedural, repairable once** — something you can actually change: wrong `--design-backend`, a stale or mistyped `design_node`, a renamed selector, a viewport mismatch. Fix it and re-run **at most once per gate per ship** (`--attempt 2`). **(b) structural, NOT repairable by re-running** — a category the design source does not expose, or an element the `design-map` omits. Re-running cannot change either, and widening the map until the gate speaks is *moving the goalposts*, not fixing the implementation — it also invalidates comparison with every earlier run. Record it as a disclosed blind spot from the gate's §6.1 list, then either (i) stop and ask the user, or (ii) if the user accepts it, log an EXPLICIT_OVERRIDE citing that blind spot. Never present it as "verified". **(c) `--attempt` already 2** — hard stop; there is no third run. The runner enforces this itself: a third attempt exits `2` and will not execute without a user-verbatim `--override-reason`. **The rule that bounds this loop: an INCONCLUSIVE is never resolved by re-running the same check — it is resolved by changing the *input*, which is a decision, or by disclosing the blind spot.** Log: `che decision_append "$WORKTREE_ROOT" "DOMAIN-GATE-INCONCLUSIVE" "domain=${effective_domain} gate=${GATE_BASENAME} reason=${REASON} report=${DOMAIN_GATE_REPORT}"`. EXPLICIT_OVERRIDE is NOT valid here: the override exists for a *measured* disagreement, never for a missing measurement. |
   d. **After all gates PASS, are SKIPPED, or explicit override logged:** Log FINAL gate 5 entry HELPER: `che decision_append "$WORKTREE_ROOT" "DOMAIN-GATES-ALL-PASSED" "domain=${effective_domain} n_gates=${N} skipped=${S} skipped_gates=[${SKIPPED_LIST}] overrides=${COUNT} duration_total_ms=${ms}"`. Skipped gates MUST be named in the PR description (e.g. "social motion gate: not executed — engine unimplemented"), so the PR never implies a verification that did not happen. Proceed §0.9.6.
4. **EXPLICIT_OVERRIDE rules (same as G2 code-review today):** Threshold is NEVER lowered automatically by agent. ONLY allowed if user LITERALLY typed "EXPLICIT_OVERRIDE domain=<slug> gate=<X> old=<threshold> new=<n> reason=<TEXT>" in chat. In this condition: log HELPER entry `che decision_append "$WORKTREE_ROOT" "EXPLICIT_OVERRIDE" "domain=${effective_domain} gate=${GATE_BASENAME} old=${OLD} new=${NEW} reason=${TEXT} trace_id=${TRACE_ID}"` and mark gate as "PASS (WITH OVERRIDE)". No other bypass form exists. Do not trust "seems OK".

**Output artifacts gate 0.9.5:**
- 1 decision.log entry PER gate (EXECUTED PASS/FAIL/RETRY, SKIPPED-NOT-IMPLEMENTED, or OVERRIDE), **all via official `che decision_append` helper.**
- Report per gate: `$DOMAIN_GATE_REPORT` (1 JSON file per gate, dynamically built via `che output_path` inside loop). Final structure: `$CHE_WORKSPACE_SHARED/reports/<related_id>/YYYYMMDD-HHMMSS-domain-gate-<dom>-<name>.json` (timestamp prefix = sorted within the same `<related_id>` subfolder → easy to search glob `**/reports/<related_id>/*`). A gate whose own recipe resolves a typed path (e.g. `che pixel paths` → `$CHE_PIXEL_REPORT`) writes there instead; `$DOMAIN_GATE_REPORT` is the generic slot for gates that have none.

**Blacklist check:** Reports are 100% in `$CHE_WORKSPACE_SHARED/reports/<related_id>/` (helper guaranteed outside assert). §0.8 + §2.2 continue to ensure no report/diff artifact/decisions log enters user commit diff.

---

### 0.9.6 ALL GATES PASSED — Transition guard

**Appears only if 0.9.1 ✅ + 0.9.2 ✅ (any branch that passed) + 0.9.3 ✅ + 0.9.4 ✅ OR SKIPPED + 0.9.5 DOMAIN ✅ OR SKIPPED (engineering default).**

Print one-liner BEFORE starting §1 Git Housekeeping:
```
🟢 ALL 5 EXECUTABLE SHIP GATES PASSED (scope-checker 6-checks · code-review · compliance-heavy · qa[minimal|normal|full] · domain-gates[<slug or skipped>])
Proceeding to Git Housekeeping §1 → atomic conventional commit → push → open DRAFT PR.
```

Append FINAL entry via official decision log helper:
```bash
che decision_append "$WORKTREE_ROOT" "ALL_SHIP_GATES_PASSED" "gates=[0.9.1,0.9.2,0.9.3,0.9.4,0.9.5] scores_scope=${score} effective_domain=${effective_domain} related_id=${RELATED_ID}"
```

**Post-gates blacklist reminder:** All reports above were written EXCLUSIVELY in `$CHE_WORKSPACE_SHARED/report/${RELATED_ID}/YYYYMMDD-HHMMSS-*.{md,log,json}` (centralised helper built all paths). §0.8 blacklist stage 1-2 already ran and will continue to run in §2.2 before each commit to ensure NONE of these reports or decision artifacts accidentally enter user diff.

---

## 1. STEP 1 — Git Housekeeping (inside WORKTREE_ROOT)

### 1.1 Git sanitisation check (secret scan pre-commit, extra)

Run a quick grep BEFORE staging anything (use che-compliance skill Category 1 + 2 patterns on the DIFF against default branch).
If any matches → block, report, offer to unstage / remove the problematic file, do NOT proceed.

### 1.2 Determine the following

Run these one by one and record results:
- **Current branch**: `git branch --show-current` → `<BRANCH_NAME>`
- **Default remote branch**: `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name` → usually `main` or `master`. Call it `<DEFAULT_BRANCH>`.
- **Remote tracking branch exists?**: `git ls-remote --heads origin <BRANCH_NAME>` → empty = does not exist yet; we'll create on push.
- **Staged vs unstaged files**: list both

### 1.3 Worktree path absolute guard

If any git command runs and it turns out the current directory is NOT the provided worktree root → fail immediately, do not run any commit/push against wrong directory.

---

## 2. STEP 2 — Build atomic conventional commits

This is the user's requested default: conventional commits + atomic.

### 2.1 Generate proposed commit plan

Look at the diff. `git diff --name-only <DEFAULT_BRANCH>...HEAD` (or vs staged).

**BLACKLIST FILTER — ALWAYS run BEFORE grouping:**
From the diff-name-only output, REMOVE all files matching the patterns in §0.8 BLACKLIST (`.trae/**`, `decisions.log*`, `decision.log*`, `task_graph.md`, `manual_test_plan.md`, `final_summary.md`, `execution_batches.md`, `batch_execution_report.md`, `merge_audit.*`, `scope-report.*`, `scope_check_report.*`, `spec_*.md`, `gh_stack_plan.md`, `session.md`, `envelope.md`, `task_envelope.md`, `graphify-out/**`, `*review-report.md`).
- If any of those files appear in the diff → §0.8 preflight SHOULD have cleaned them already. If still present → **DO NOT ADD TO ANY COMMIT.** Skip silently and add 1 note at the bottom of the commit plan: "Note: N planning-artifact files auto-skipped (never committed)."

Group the remaining (filtered) changes into atomic, logical commits:

- **feat(scope):** new functionality, new endpoints, new UI components
- **fix(scope):** bug fixes — include "Fixes #TICKET" if applicable
- **refactor(scope):** code move, rename, no behavior change
- **test(scope):** spec files, e2e, fixtures only
- **docs(scope):** markdown, README, docstrings, no runtime
- **chore(scope):** deps bump, config, CI file changes, migrations
- **perf(scope):** perf improvements with measurable impact
- **build(scope):** build scripts, nx config, package.json
- **style(scope):** Biome/format, indentation, CSS-only cosmetic
- **ci(scope):** GitHub Actions, workflows
- **revert(scope):** reverts prior commit

Rule for grouping:
- If a change can stand alone (migration separate from runtime code that uses it) → separate commits.
- Tests for a feature go WITH the feature commit, not in separate, unless the feature is already merged.
- Migrations: usually `chore(db): add migration for X` separate commit.
- Max 15 commits per ship. If > 15 → offer user option to squash into fewer + plan, or proceed with 15+.

Present commit plan to the user as a **numbered list**, in order of application. Add the "N planning artifacts skipped" note at the bottom if applicable.
Wait for explicit user APPROVAL before running any `git commit`.

### 2.2 Execution — apply the commits (AFTER USER APPROVES plan)

Run each commit:
```
# BEFORE every commit: unstage ANY blacklisted files that somehow re-entered the index.
git reset HEAD -- \
  .trae  .che-ai  decisions.log.jsonl  decisions.log.md  decisions.log \
        decision.log.jsonl   decision.log.md   decision.log \
  task_graph.md manual_test_plan.md final_summary.md \
  execution_batches.md batch_execution_report.md \
  merge_audit.md merge_audit.jsonl \
  scope-report.md scope-report.json scope_check_report.md scope_check_report.json \
  spec_*.md gh_stack_plan.md session.md envelope.md task_envelope.md \
  graphify-out che-review-report.md che-compliance-report.md flockr-review-report.md \
  2>/dev/null || true

git add <files for this commit>
git commit -m "type(scope): imperative description in English, lowercase, max 72 chars"
```
Rules:
- NEVER run `git add .` — always add per-file or per-directory explicitly.
- Before EVERY `git add`, run the `git reset HEAD -- <blacklist patterns>` line above. (Fail-closed — cost 1 ms per commit, prevents a whole class of PR-pollution bugs.)
- Every commit message in **ENGLISH** (Header and Body), following the **Storytelling Conventional Commit** rule.
- After last commit → run `git log --oneline -20` to present final chain to user.
- **POST-COMMIT ASSERT (after all commits applied):** `git show --name-only --pretty=format: HEAD~10..HEAD` → scan file names for §0.8 blacklist patterns. If any commit contains a blacklisted file → **STOP, DO NOT PUSH.** Report to user, offer `git reset HEAD~N` + re-apply cleanly, then continue.

### 2.3 GH_STACK_MODE=true — Group commits PER LAYER (bottom-up)

**ONLY run when `GH_STACK_MODE=true`. Overrides 2.1/2.2 default flat plan; standard flat commits become per-layer grouped commits.**

For each layer `L[i]` in `LAYERS[]` (bottom-up order, starting with the lowest stack layer):

1. **Checkout / create layer branch**:
   ```bash
   git checkout -b <L[i].BranchName>   # if branch doesn't exist locally yet
   # or: git checkout <L[i].BranchName>  # if already exists
   ```
2. **Cherry-pick OR stage only files in layer scope**:
   - Strategy A (preferred when commit plan already aligns): cherry-pick only the commits relevant to this layer onto this branch from the consolidated work branch.
   - Strategy B (simpler fallback — use when scope-per-layer is clearly file-based): from worktree state, **FIRST run `git reset HEAD -- <blacklist patterns>` (same as §2.2)** then `git add <only files matching L[i].Scope (files)>`, then create 1 or more conventional commits scoped EXCLUSIVELY to this layer (no cross-layer files in same commit).
3. Present plan of "branch → commits → scope" to user as numbered list. **Wait for explicit user APPROVAL before applying any layer commit.**
4. After user approves: apply commits per layer. Record per-layer: final commit SHAs.
5. After all layers done: present to user summary "Layers bottom-up (N layers): L1 → 2 commits; L2 → 3 commits; L3 → 1 commit" etc.

Rule invariant for GH_STACK_MODE commits:
- **Every file in a given layer's commit MUST be listed in L[i].Scope (files).** If a file belongs to layer L[i+1] it MUST NOT appear in commits of L[i]. Any cross-layer file → block, ask user which layer gets it.
- **Additional GH-stack invariant:** Zero files from §0.8 BLACKLIST allowed in ANY layer's commit. If after building layer the index contains a blacklist file → `git reset HEAD -- <file>` and warn.

---

## 3. STEP 3 — Push with `--no-verify`

User's rule: default to `--no-verify` for push.

### Path A: GH_STACK_MODE=false (single branch, standard)

```bash
# Case 1: remote branch does NOT exist yet
git push --no-verify --set-upstream origin <BRANCH_NAME>

# Case 2: remote branch already exists (ahead/behind)
git push --no-verify
```

Wait for success. If push fails:
- Non-fast-forward → ask user: rebase or force push? NEVER force push without explicit confirmation.
- Auth failure → stop.

### Path B: GH_STACK_MODE=true (push each layer bottom-up)

Loop layers in bottom-up order:

For each layer `L[i]` in `LAYERS[]`:
```bash
git checkout <L[i].BranchName>
# Case 1: remote branch doesn't exist
git push --no-verify --set-upstream origin <L[i].BranchName>
# Case 2: remote branch exists
git push --no-verify
```

Push failure rule same as Path A (per layer; block on first failure, don't continue to upper layers).

---

## 4. STEP 4 — Open DRAFT PR(s) against default branch

### Common Step: 4.0 Detect Linear/Jira ticket reference (both paths)

Look in:
- `$CHE_SESSION_DIR/session.md` for field "Ticket URL/ID" (resolved via `che compute_paths`; never inside the worktree)
- Branch name pattern: `feat/PROJ-123-login`, `fix/PROJ-456`, `ticket PROJ-123` anywhere in session/task_graph/envelope files
- User command args: `/che-ship ticket:PROJ-123`

If found ticket: extract `<TICKET-ID>` (full URL or just ID). Append `Refs: <TICKET-ID>` footer to EVERY PR body (single OR all layers in stack).

---

### Path A: GH_STACK_MODE=false (single PR, standard)

#### A-4.2 Build PR Description — READABLE 5 BLOCKS (ENGLISH by default, ≤50 lines TOTAL target)

> **Canonical body + FILLED real EXAMPLE (refund feature from screenshot, low-context readable version):** `references/PR_DESCRIPTION_TEMPLATE.md` (Layer 3 SOLE owner of structure/content + readability rules). Below only process budgets.
> **Copy the STYLE of the filled example in PR_DESCRIPTION_TEMPLATE.md, not only the section names.** The filled example shows exactly how to phrase bullets, acronym expansion, user impact, and risk consequence.

**LANGUAGE GATE (non-negotiable — #1 rule, before any writing):**
- **DEFAULT = ENGLISH (EN-US / EN-GB).** Write the ENTIRE PR body, headings, bullets, ticket refs, commands — EVERYTHING — in English.
- **Other language ONLY IF:** the user explicitly requests another language.
- **Never guess / NEVER assume.** Absent an explicit mention → PR body is ALWAYS English.

**PROCESS GATES (non-negotiable — readable for low-context reviewers, trim only the useless, never the clear context):**

1. **Block 1 — What was implemented:** bullets only, 3–8 items. No paragraphs. **MANDATORY pattern per bullet:** `feat|fix|chore(scope): <WHAT changed in plain English>. <1 short sentence WHY / end-user impact>.` **READABILITY sub-rules (from template §RULES 1-3):**
   - **Acronyms expanded on FIRST use** inside the bullet (example: "RLS (Row-Level Security — Postgres access control)"). After first use → acronym alone is OK.
   - **Avoid concatenating 5–10 micro-changes into 1 monster bullet.** Each `feat(scope)` line = ONE self-contained area (DB schema / entity / service / Stripe / API / UI / tests — 1 bullet each, not 8 changes jammed).
   - **Internal jargon gets ½-line context** (example: "reverse_transfer (Stripe Connect — money moves from the connected org account back to the platform, then to the buyer)" not just "reverse_transfer=true").
   - If >8 bullets → PR is too large (split into gh-stack, §Path B).
2. **Block 2 — 🔍 Attention points:** bullets only, 3 IDEAL, 5 MAX. **MANDATORY pattern per bullet:** `**Risk label:** \`path/or filename\` — <what is risky, plain English>. **If review misses this:** <plain-English consequence — what actually breaks for users/devs>.` Risk labels (rename jargon to the readable versions below):
   - ✅ Use: `Security-sensitive` · `Performance-sensitive` · `Schema change (DDL migration)` · `Cross-module change` · `Concurrency / race condition` · `Product decision`
   - ❌ Stop using: `Blast-radius` (too vague — say what it actually hits)
   - If >5 bullets → split gh-stack.
3. **Block 3 — 💥 Breaking changes:** **INCLUDE ONLY IF they EXIST.** If NONE → DELETE the ENTIRE "Breaking changes" section (do NOT write "NONE", do NOT leave an empty section). When including: 1 heading per breaking change + Before / After / Migration bullets.
4. **Block 4 — 🧪 How to verify:** bullets only, 1–3 items, IN THIS ORDER:
   - (a) **Automated tests:** CONCRETE COMMAND pointing to a SPECIFIC test + 1 sentence what is covered + 1 expected-result sentence ("Expected: 1/1 passing green").
   - (b) **Quick manual check:** 2–3 CONCRETE steps with numbered parens, NO assumed folder-structure knowledge, always state the EXPECTED VISIBLE outcome (not "test it works").
   - (c) **Full plan (optional):** link to `$CHE_WORKSPACE_SHARED/manual_test_plan.md`
5. **Block 5 — 🔗 Refs:** Linear/Jira ticket (ID + URL). Optionally 1 extra link (Figma, PRD .md path, related PR number).
6. **FORBIDDEN sections (always delete if they creep in):** Scope In/Out, Assumptions adopted, long What/Why intro paragraphs, Che gates checklist, giant tables, 2-paragraph context intro. (The "why" lives INSIDE each Block 1 bullet, NOT as a preamble.)
7. **Body budget:** ≤50 lines TOTAL (all 5 blocks + headings summed). No breaking → target ~30 lines. With breaking → target ~45 lines. If over → move long migration/design details into a separate linked doc + keep 1 summary line in Block 2 or 3. **Do NOT butcher acronyms/user-impact sentences to save 2 lines — save by cutting forbidden prose instead.**

**Linear ticket auto-include (A-4.0 common step):** When a ticket is detected (A-4.0), ALWAYS include it in Block 5 "Refs". Do NOT duplicate the ref in a separate footer/comment.

#### A-4.3 Create PR (Draft, not ready for review)

```bash
gh pr create \
  --draft \
  --base <DEFAULT_BRANCH> \
  --head <BRANCH_NAME> \
  --title "<conventional commit style title, more descriptive: feat(auth): implement Stripe Connect onboarding>" \
  --body-file <tmpfile_with_pr_description.md>
```

Capture the created PR URL: `<PR_URL>`.

#### A-4.4 Assign to user + labels

```bash
gh pr edit <PR_URL> --add-assignee @me
# Optional: add existing labels (type: bug/feature, needs review, security, breaking-change)
# Only add labels that EXIST in repo.
```

---

### Path B: GH_STACK_MODE=true (hierarchical PR stack via gh-stack)

#### B-4.2 Per-layer PR body + Depends-on chain (bottom-up)

For each layer `L[i]` in `LAYERS[]` (bottom-up order):
1. Build a PR description SCOPED EXCLUSIVELY to `L[i]` — same **READABLE 5-block structure + readability rules from Path A §A-4.2** (acronym expansion, user-impact per bullet, risk-consequence explanation, non-jargon labels, plain-language How-to-verify). Body is SCOPED TO ONLY the layer's changes (no cross-layer leaks).
   - **Depends on header (CANONICAL gh-stack)**:
     - If `L[i].Depends on` is non-empty → PREPEND block to the **TOP of PR body** (before the 5 blocks):
       ```
       Depends on: #<PR-ID-of-L[i-1]>
       ---
       ```
       (Use the numeric PR ID, not the full URL.)
     - If first layer (base, no Depends on) → skip this header.
   - Append: related ticket footer `Refs: <TICKET-ID>` inside Block 5 (🔗 Refs).
   - NO assumptions paragraphs / NO che checklists. **Body total ≤35 lines per layer** (relaxed vs single PR because stack layers are smaller). Still enforce the readable style from PR_DESCRIPTION_TEMPLATE.md filled example.
2. Write each layer body to `<tmp>_layer_<L[i].ID>_body.md`.

#### B-4.3 Create each layer PR individually + gh-stack link

Loop layers **bottom-up**:
For each layer `L[i]`:
```bash
# Ensure on correct layer branch:
git checkout <L[i].BranchName>

# Create DRAFT PR for THIS layer:
gh pr create \
  --draft \
  --base <if first layer: DEFAULT_BRANCH; else: L[i].Depends on layer's branch> \
  --head <L[i].BranchName> \
  --title "<L[i].ID>: <layer scope descriptive conventional title>" \
  --body-file <tmp>_layer_<L[i].ID>_body.md
```
- Capture each layer's PR URL: `L[i].PR_URL` AND numeric PR ID: `L[i].PR_NUMBER`.
- After PR created: self-assign: `gh pr edit <L[i].PR_URL> --add-assignee @me`.

After **all individual layer PRs are created + assigned**:
```bash
# Run gh-stack to formalize the Depends-on hierarchy:
gh-stack create --draft
```
This validates the chain; if errors → fix base/head references manually per layer.

#### B-4.4 Stack invariant check

After gh-stack create: verify the chain:
- Layer 1 (base) PR `base: DEFAULT_BRANCH` → correct.
- Layer N PR `base: L[N-1] branch` AND body has `Depends on: #<L[N-1].PR_NUMBER>` → correct.
If mismatch → report to user; offer to fix via `gh pr edit --base` or body edit; wait approval.

---

## 5. STEP 5 — Report to user (in English)

### Path A: GH_STACK_MODE=false (single PR report)

Final output to user chat in English:

```
✅ /che-ship successfully completed.

Summary:
  • Worktree: <worktree path>
  • Remote branch: <branch> (created if missing)
  • Applied commits: N (summary list)
    - <short sha1> type(scope): message
    - ...
  • Created PR (DRAFT): <PR_URL>  [assigned to you]
  • Assumptions, review points, breaking changes: see PR body

Ship gates reports (all in che-sessions, sorted by UTC timestamp):
  • Scope check (§0.9.1): $SHIP_SCOPE_CHECK_REPORT
  • Code review (§0.9.2): $SHIP_CODE_REVIEW_REPORT
  • Compliance heavy (§0.9.3): $SHIP_COMPLIANCE_HEAVY_REPORT
  • QA gate log (§0.9.4): $SHIP_QA_GATE_LOG

Related artifacts (same workspace):
  • Manual test plan: referenced in body and available at:
    $MANUAL_TEST_PLAN_PATH
  • Decision log (all decisions append-safe JSONL, via che decision_append):
    $CHE_DECISIONS_PATH

Next steps:
  1. Run a manual smoke test using the plan above.
  2. Review the PR diff to ensure no unintended files entered.
  3. When all ok: open PR <PR_URL>, click "Ready for review" and assign reviewers.
```

### Path B: GH_STACK_MODE=true (hierarchical PR stack report)

Final output to user chat:

```
✅ /che-ship successfully completed — HIERARCHICAL gh-stack MODE.

General Summary:
  • Worktree: <worktree path>
  • Number of PRs in stack (bottom-up): <N layers>
  • gh-stack chain created. All PRs DRAFT + assigned to you.

Ship gates reports (all in che-sessions, sorted by UTC timestamp):
  • Scope check (§0.9.1): $SHIP_SCOPE_CHECK_REPORT
  • Code review (§0.9.2): $SHIP_CODE_REVIEW_REPORT
  • Compliance heavy (§0.9.3): $SHIP_COMPLIANCE_HEAVY_REPORT
  • QA gate log (§0.9.4): $SHIP_QA_GATE_LOG

Related artifacts (same workspace):
  • Original gh-stack plan: $GH_STACK_PLAN_PATH
  • Global manual test plan: $MANUAL_TEST_PLAN_PATH
  • Decision log (all decisions append-safe JSONL, via che decision_append):
    $CHE_DECISIONS_PATH

PR Stack (merge order = base first to top):
───────────────────────────────────────────────
L1 (base, merged first) →
   branch: <L1.BranchName>
   commits: K1
      - <sha> type(scope): message
      - ...
   PR DRAFT: <L1.PR_URL>   [base: DEFAULT_BRANCH]
───────────────────────────────────────────────
L2 → depends on #<L1.PR_NUMBER>
   branch: <L2.BranchName>
   commits: K2
      - ...
   PR DRAFT: <L2.PR_URL>   [base: L1.BranchName]
───────────────────────────────────────────────
...
───────────────────────────────────────────────
LN (top, merged last) → depends on #<L[N-1].PR_NUMBER>
   branch: <LN.BranchName>
   commits: KN
   PR DRAFT: <LN.PR_URL>   [base: L[N-1].BranchName]
───────────────────────────────────────────────

(Validate each layer's behaviour individually before marking the stack as ready.)

Next steps (review order = same bottom-up merge order):
  1. Run individual smoke tests in each layer starting from L1 (base).
  2. Review diffs one PR at a time — always L[i] PR review BEFORE L[i+1].
  3. When L[i] approved + merged: gh-stack automatically updates L[i+1] base → repeat until LN.
  4. Only after LN merged: click "Ready for review" on the top-level, or follow normal flow per layer.
```

---

## Appendix A: Hard stops / What we will NEVER do

- Commit files with `.env` in name OR any file matching secrets regex patterns.
- Push against a branch you are NOT currently on.
- Commit directly to `main` / `master` / default branch. Block. Always: feature branch → PR.
- Force push without explicit user confirmation.
- Merge the PR. Ship stops at DRAFT PR creation + assign.
