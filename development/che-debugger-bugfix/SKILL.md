---
name: "che-debugger-bugfix"
description: "Scientific debugging che for bug fixes: user provides expected behaviour + reproduction steps; the Debugger expert loops through hypothesize→instrument→reproduce→analyse→fix→verify until expected behaviour is met. Demonstrates the fix or provides clear manual reproduction guide. Invoke when user describes a bug/incorrect runtime behaviour and wants it fixed, or when /che-fix is called."
---

# Che — Debugger / Bugfix Expert (Scientific Debug Loop)

This is the **specialised che for bug fixes**, NOT for features.
The developer mindset here is **hypothesis-driven + evidence-collecting**, not feature-building.

> **Why a different loop for bugs?** Feature che is plan-first, deterministic. Bug che is observation-first: you must REPRODUCE before you understand, then iterate hypotheses until the root cause is found. Evidence beats plan.

---

## 0. Pre-flight — Worktree + inputs

### 0.1 Worktree-first enforcement

Same as the global rules: if worktree path is NOT provided by the user → **ASK immediately** before proceeding to any other step. No code runs, no files opened.

### 0.2 Required inputs from user (block until provided)

User MUST provide:
1. **Expected behaviour**: What SHOULD happen?
2. **Actual behaviour / Bug description**: What IS happening? Include stack traces, error messages, screenshots if available.
3. **Reproduction steps**: Minimum, clear numbered steps (1, 2, 3, ...) to trigger the bug reliably. Include:
   - Which route / endpoint / URL?
   - Credentials / role required (admin? regular user? logged out?)
   - Environment (staging? local dev? which branch? which worktree?)
   - Sample payload / form input / seed data if any
4. **Ticket reference** (if any): Linear/Jira URL/ID — optional

If user fails to provide ANY of 1, 2, or 3 → **ASK with specific questions** before starting debug loop. DO NOT guess reproduction steps.

### 0.3 Session artifacts dir + 🔴 STORAGE PREFLIGHT (MORATORIUM §20)

Run **exactly this block BEFORE** writing any file (logs, traces, screenshots, session md, decisions append):

```bash
# Resolve the `che` CLI (owns the Che-home cascade + canonical path construction)
command -v che >/dev/null 2>&1 || { echo "❌ FATAL: 'che' CLI not found on PATH. HARD STOP — zero files written without storage boundary. exit 98"; exit 98; }

SESSION_ID="${CHE_CURRENT_SESSION_ID:-${CHE_SESSION_ID:-fallback-debugger-session}}"
eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"
che ensure_dirs "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD"

# Double-guard: asserts fail-fast if any output directory lands INSIDE worktree (exit 99)
che assert_outside_worktree "$CHE_SESSION_DIR" "$WORKTREE_ROOT" --label "CHE_SESSION_DIR (ephemeral debug)"
che assert_outside_worktree "$CHE_WORKSPACE_SHARED" "$WORKTREE_ROOT" --label "CHE_WORKSPACE_SHARED (durable decisions)"

# Construct ALL paths ONCE here via the unique CLI. Then reuse only these variables:
BUGFIX_SESSION_MD="$(che output_path "debugger" "bugfix-session" "${BUG_SLUG:-generic-bug}" "session" "md")"
# Hypothesis log (jsonl append via atomic helper):
HYPOTHESIS_LOG="$(che output_path "debugger" "hypotheses" "${BUG_SLUG:-generic-bug}" "session" "jsonl")"
# Evidence dir = CHE_SESSION_DIR/qa/evidence/<related_id>/ (already created by helper when needed)
```

**Storage architecture (ALL strictly OUTSIDE user worktree):**
```
$CHE_SESSION_DIR/                       ← ephemeral per-session
  └── debugger/<BUG_SLUG>/                  ← related_id groups everything for this bug
        ├── 20260902-133000-bugfix-session.md   (append per loop iteration)
        └── 20260902-133000-hypotheses.jsonl    (each hypothesis one line)
$CHE_WORKSPACE_SHARED/                  ← durable: decisions.log.jsonl (single per worktree)
```

**NEVER write to `<WORKTREE_ROOT>/.trae/` or `<WORKTREE_ROOT>/reports/` or any relative path inside worktree.** §20 MORATORIUM. If for any reason you need to save something inside the worktree (rare exception), stop and ask for EXPLICIT VERBATIM user confirmation in text.

Append to `$BUGFIX_SESSION_MD` on every loop iteration using `che write_file_atomic` (pipe append) or `>>` redirection (safe as the path has already passed outside assert).

---

## 1. Phase 0 — Baseline (once per bug)

### Step 1.1 Reproduce the bug FRESH (evidence #1)

1. Start the relevant services using the repo's documented way (follow repo AGENTS/docs/patterns).
2. Execute reproduction steps EXACTLY as user wrote.
3. **Capture evidence:**
   - Stack traces (copy first 40 lines)
   - HTTP request/response (status, body preview — never secrets)
   - Server logs excerpt (first ERROR and ~20 lines around it)
   - Screenshots if UI/visual bug
   - DB state (relevant rows / queries if DB-backed bug)
4. Record to session file: `✅ REPRODUCED` or `❌ FAILED TO REPRODUCE`.

**If FAILED TO REPRODUCE (blocker):**
- DO NOT start fixing.
- Go back to user: "I could not reproduce. Checklist of what diverges: (1) version X vs Y? (2) user/role? (3) seed data? (4) wrong branch?". Ask user clarifying questions + suggest pair steps until we get a clean repro.

### Step 1.2 Minimise the reproduction

Once reproduced: try to make reproduction steps even shorter.
- Remove unnecessary steps.
- Create a minimal test case (unit test snippet) that triggers the error path if possible.
- This minimal case becomes the **regression test at the end.**

### Step 1.2.5 🔴 REPRO AUTOMATION LOCK — FAIL-FAST HARD STOP (Red-Green Before Any Hypothesis or Code Edit)

> **NON-NEGOTIABLE HARD GATE — engineering-contracts §10 TDD + Rule 7.9. You CANNOT advance to Step 1.3 (hypothesise) or touch ANY source code until this step is PASSED or EXPLICIT_OVERRIDE is logged.**

**What this gate enforces (the "Fix Every Bug Twice" Stripe playbook):**
1. Bug is first reproduced AUTOMATICALLY inside a test runner (Vitest unit / integration / Playwright / pytest / etc — whatever matches the repo's stack).
2. We confirm the test FAILS with exit_code != 0 (red phase). This becomes the deterministic regression lock — when we fix the code, the SAME test must PASS without changing the test body.
3. Evidence (test path + sha256 of the failing run output) is saved to `bugfix_session.md` so the next session can resume the lock deterministically.

**Mandatory execution order:**

**Step 1.2.5.1 — Write the repro automation test file**
- Pick the test layer matching the bug:
  - Pure algorithm bug / service-level deterministic → **unit test** (`*.test.ts`, `*.spec.ts`, co-located near source OR `__tests__/unit/...`)
  - Bug crosses 2+ modules (service→DB→stripe) → **integration test** (`__tests__/integration/...` or `__tests__/e2e/*.api.test.ts` for route-level)
  - UI-only visual / event-handler bug → **Playwright E2E** or **React Testing Library** component spec (NEVER manual-only repro for UI bugs unless literally impossible)
- If repo has NO test framework installed → install the minimum matching the AGENTS/docs (e.g. Vitest for TS Node.js + React). If repo cannot have tests → EXPLICIT_OVERRIDE path below.
- The test body MUST contain this EXACT structure as the FIRST lines INSIDE `it(...)` / `test(...)`:
  ```typescript
  it("describes the bug symptom behaviourally — NO ticket id in title", async () => {
    // @ticket FLO-123 | @bug reproduces: <1-line symptom plain English> | @ac B-7
    // arrange: ...
    // act: ...
    // assert: expect(...).rejects.toThrow(...) or similar
  })
  ```
  Exception for Playwright / non-JS runners: place `@ticket | @bug | @ac` as a comment line on the FIRST executable line after the `test(...)` declaration, or as the `test.describe` JSDoc. Never put FLO-id in the display title string.

**Step 1.2.5.2 — Run the test, confirm FAIL (red)**
- Execute ONLY the single test file with the repo's documented runner (e.g. `corepack pnpm vitest run packages/platform/server/__tests__/unit/refund-repro.test.ts`).
- CAPTURE the exit code AND tail-40 lines of output.
- **Confirm assertion: exit_code !== 0 AND failure message matches the user-reported bug symptom.**
  - If exit_code === 0 (passes): the test does NOT reproduce the bug. Rewrite the test — wrong input data, wrong assertion, or fixture setup diverges from user repro steps. Do NOT advance.
  - If test FAILS but with a DIFFERENT error than the bug symptom (wrong assertion): fix the assertion to match the ACTUAL bug symptom confirmed in Step 1.1. Do NOT advance.

**Step 1.2.5.3 — Persist the repro lock evidence**
Append to `$BUGFIX_SESSION_MD`:
```markdown
## 🔴 REPRO AUTOMATION LOCK — EVIDENCE (Step 1.2.5)

- **repro_test_abs_path:** `/absolute/path/to/repro.test.ts`
- **repro_test_run_command:** `corepack pnpm vitest run ...`
- **repro_fail_exit_code:** `1`
- **repro_fail_sha256_output:** `<sha256sum of combined stdout+stderr of the failing run>`
- **repro_fail_message_excerpt:** `<3 lines from test runner output showing exact failure — enough to match symptom>`
- **repro_bug_ticket_ref:** `<FLO-123 or N/A>`
- **repro_ac_trace:** `<B-7 or N/A — SbE behavior-id this test locks>`

> Assertion verified: test FAILS deterministically. Fix must make SAME test PASS without changing its body (only @ticket/@bug/@ac comment line can be adjusted).
```

**Step 1.2.5.4 — Decision path to Phase 1 hypotheses**
| Outcome of 1.2.5.1 → 1.2.5.3 | What happens next |
|---|---|
| ✅ Test written, FAIL confirmed, evidence saved | **ADVANCE to Step 1.3 → build hypotheses.** Gate unlocked. |
| ⚠️ Cannot write automated repro (e.g. visual-only bug that requires GPU rendering / prod-specific race / third-party-UI-outside-our-code) | **HARD STOP — DO NOT ADVANCE.** Ask user verbatim: *"I could not write an automated test that reproduces the bug. Reason: <1-line technical explanation>. To proceed, I need an EXPLICIT_OVERRIDE from you confirming this exception is acceptable. Please confirm by typing EXPLICIT_OVERRIDE_DEBUGGER_REPRO=YES + 1-line justification why it cannot be automated."* Log override VERBATIM into decisions.log.jsonl via `che decision_append "$WORKTREE_ROOT"` BEFORE advancing. |

**POST-FIX MIRROR CHECK — performed at Phase 2 Step 3.3 (verify lock flipped):**
After root cause fix applied, run EXACT SAME `repro_test_run_command`. Assert:
1. exit_code === 0 (green now — lock flipped)
2. Any NEW tests added for expected-behaviour (happy paths / edge cases) also PASS
3. NO previously-passing test in same module NOW FAILS (regression)
Append "✅ REPRO LOCK FLIPPED — same test now PASSES + exit_code=0 + sha256=<new>" line to Phase 2 verification section of bugfix_session.md.

**[G5 NOTE — REGRESSION LOCK LOCATION POLICY (MANDATORY AT THE END OF STEP 3.3):**
- **DEFAULT 95% OF CASES (Fix Every Bug Twice — Stripe Playbook):** regression test (repro lock + behaviour tests) MUST be **IN THE FEATURE/DOMAIN FOLDER WHERE THE BUG OCCURRED** along with other tests for that area. **DO NOT put ticket ID in filename.**
- **Example:** Bug FLO-513 Refund: `packages/platform/server/__tests__/e2e/refundFlow.api.test.ts` (standard refund / server tests folder) with **FIRST LINE INSIDE `it()` BLOCK** (NOT in title):
  ```typescript
  it('confirms a full refund succeeds with reason and shows correct status row', async () => {
    // @ticket FLO-513 @bug reproduces refund amount not reversed on row status @ac B-3
    // ... rest of test
  });
  ```
- **SPECIAL EXCEPTION CASE (< 5% CROSS-CUTTING ≥4 DOMAINS):** Regression test crosses **≥4 independent domains** (e.g. auth + billing + notification + db migration) **OR** is pure infrastructure without specific domain (e.g. worker queue, CI deploy script) → **PERMITTED** to create `tests/regression/<TICKET_ID>--<slug>.test.ts` with ID in filename. **BUT MANDATORY:**
  1. Have `EXPLICIT_OVERRIDE_G5_REGRESSION_FOLDER` logged VERBATIM in `decisions.log.jsonl` with 1-line justification.
  2. Include entry in Notes column of SbE spec Verification Matrix with absolute path.
  3. If no logged override, G7.3 code-review automatically rises to **HIGH severity** (blocking if ≤2 HIGH auto-fix).

### Step 1.3 Build the initial hypothesis list

From evidence:
- State **symptoms clearly** (what breaks, line, data shape).
- Write **3 candidate root causes** as numbered hypotheses, ranked by likelihood:
  ```
  Hypothesis H1 (Likelihood: HIGH): <explanation>
  Hypothesis H2 (Likelihood: MEDIUM): <explanation>
  Hypothesis H3 (Likelihood: LOW): <explanation>
  ```
- NEVER start editing code before hypotheses are written.

---

## 2. Phase 1 — Debug Loop (repeat per hypothesis, max 5 iterations per bug)

```
    ┌─────────────────────────────────────┐
    │  HYPOTHESISE (pick next ranked Hn) │
    └────────────────────┬────────────────┘
                         │
                         ▼
    ┌─────────────────────────────────────┐
    │  INSTRUMENT — add targeted logs /   │
    │  breakpoints / assertions           │
    └────────────────────┬────────────────┘
                         │
                         ▼
    ┌─────────────────────────────────────┐
    │  REPRODUCE — run the minimal case   │
    │  + capture new evidence             │
    └────────────────────┬────────────────┘
                         │
                         ▼
    ┌─────────────────────────────────────┐
    │  ANALYSE evidence                   │
    │  Hypothesis CONFIRMED / REFUTED?    │
    └──────┬───────────────────┬──────────┘
           ▼                   ▼
      REFUTED              CONFIRMED
           │                   │
           │ rank next Hn      ▼
           │               FIX — minimal code change
           │                   │
           │                   ▼
           │             VERIFY fix:
           │             repro steps now show EXPECTED behaviour
           │                   │
           │                   ▼
           ▼             FIX DONE
  > 5 total iterations? ──▶ YES
           │
           ▼ NO
  Loop user: "we are at N iterations. Root cause seems to be X. Next steps? (Y/N)"
```

### Mandatory per-iteration evidence in bugfix_session.md

Every loop iteration appends a section:
```
## Iteration N — Hypothesis H<X>

### Instrumentation
- Added: <file:line> debug_log
- Changed: <none — observability only iteration>

### Reproduction output (captured)
<stack trace / assertion / log lines>

### Analysis — CONFIRMED or REFUTED?
- Decision: CONFIRMED / REFUTED
- Why: <evidence-based rationale>

### If CONFIRMED:
- Root cause (1 sentence): ...
- Proposed minimal fix (what EXACTLY will change, why this fix, not alternatives):
  - Option 1: <what files change>
  - Option 2: <alternative>
  - DECISION: Option X — <rationale>
```

### Forbidden patterns during debugging

- **No shotgun edits:** Changing 5 files "hoping it helps" is FORBIDDEN. One hypothesis → targeted instrumentation or single minimal fix.
- **No `console.log` left in production code at end.** Remove ALL debug logging after verification. Clean up.
- **No refactoring alongside bugfix.** Bugfix = minimal code change. If refactor needed → separate commit, separate PR, after fix verified and merged.

---

## 3. Phase 2 — Fix Engineering (after root cause CONFIRMED)

### Step 3.1 TDD for bug

Write a test (unit preferred, integration if needed) that:
1. Fails before fix (confirms bug reproduction via test)
2. Passes after fix (confirms fix)

The test SHOULD test behaviour (input/output, state transition), not implementation details.

### Step 3.2 Apply MINIMAL fix

- Apply only lines that actually fix root cause.
- If adjacent code "also looks wrong" → note in decision.log for follow-up PR, do NOT fold into this bugfix.

### Step 3.3 Run: fix + regression test

1. Confirm new test now PASSES.
2. Run **related tests** (same module files, affected) to confirm no regressions.
3. Optional: full test suite if task size small or repo supports it quickly.

### Step 3.4 Manual verification

Demonstrate via REPRODUCTION steps that:
- Before fix: actual behaviour (BAD) — confirm you can trigger it
- After fix: expected behaviour (GOOD) — confirm you now see it

Record before/after evidence to session file.

---

## 4. Phase 3 — User Handoff

Two possible outcomes:

### Outcome A — ✅ FIX CONFIRMED

Report to user in English:
```
✅ Bug identified and fixed.

📋 Technical Summary:
  • Symptom: <1 sentence description>
  • Root Cause: <1 sentence description>
  • Modified Files:
      - <path> (EDIT — lines XX-YY)
  • Regression test added: <path/to/spec>

🔬 Proof of Work:
  1. Before fix: <steps> → <error message / bad behavior>
  2. After fix: <same steps> → <expected behavior>
  3. Unit test `describe(...)` fails without fix, passes with.

🧪 How YOU can verify:
  <step-by-step in English, matching initial reproduction session>
  1. git checkout <branch>
  2. corepack pnpm install
  3. ...
  4. Expected: ...

📎 Artifacts (all OUTSIDE worktree, resolved via `che compute_paths`):
  - bugfix_session.md: `$CHE_SESSION_DIR/bugfix_session.md`
  - Decisions: `$CHE_WORKSPACE_SHARED/decisions.log.jsonl`
  - Ticket link recommended if applicable.
```

### Outcome B — ⚠️ NOT FIXED YET (after 5 iterations or blocked)

Report:
```
⚠️ Could not reach a fix in this session.

Progress made:
  • 5 iterations executed. Hypotheses H1-H5 REFUTED.
  • Discarded root causes:
      - H1: ... (evidence: ...)
      - H2: ...
      ...
  • Strongest current hypothesis for next session:
      - H6: ...

Recommended next steps:
  Option 1) Continue investigation for 3 more iterations.
  Option 2) Provide more context: (1) bug history (2) extra screenshots (3) exact data seed.
  Option 3) Guided pair programming session.
```

---

## Appendix A: Observability toolbox (prefer these — order matters; repo-contextual)

| Tool | Use when | Command hints (if repo-agnostic) |
|---|---|---|
| Repo logger (preferred) | Add debug-level line during instrument phase | Use project logger; remove after |
| Structured logs (OTel, pino, winston) | Trace request path | Look for traceId in headers |
| HTTP curl/HTTPie | API bug repro | Reproduce request offline in .http scratch file |
| Node inspect | Node.js runtime bug | `NODE_OPTIONS="--inspect" ...` then chrome://inspect |
| Python pdb | Python bug | `breakpoint()` at suspected line |
| Pry / byebug | Ruby bug | `binding.pry` |
| Delve | Go bug | `dlv debug` |
| Rust dbg! macro + lldb/gdb | Rust bug | Wrap suspected: `dbg!(&var);` |
| Browser devtools | UI bug | Network tab + break on XHR; Console log filter for errors |
| Postgres `EXPLAIN ANALYZE` | DB perf bug | Run query with analyse |
| tRPC query trace | tRPC specific | enable `tRPC logger link` with level=debug for this request |

Always prefer repo-native tooling first. Never add a new observability package just to debug — use what's installed.
