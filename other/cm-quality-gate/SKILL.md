---
name: cm-quality-gate
description: "Use before any deployment or completion claim. Enforces test gates, evidence-based verification, and frontend safety checks. No deploy without passing. No claims without evidence."
token_budget: 1800
compressed: true
deprecated: false
---

# Quality Gate — Test + Verify + Ship Safe

## TL;DR
- **Use before** any deployment or completion claim
- **Gates**: tests pass, no secrets, frontend safety, evidence logged
- **Reads**: handoff/exec.json — **Writes**: handoff/quality.json
- **Modes**: OFF | WARNING (default) | SOFT | FULL
- **Vibecoding score**: 0..100 (Phase 2)

> **Three checkpoints, one skill:** Pre-deploy testing, evidence verification, frontend safety.

## The Iron Laws
1. **NO DEPLOY** without passing `test:gate`.
2. **NO CLAIMS** without fresh verification output.
3. **NO FRAGILE FRONTEND** — safety tests are mandatory.

---

## Phase 0: Infrastructure Setup
> **Goal:** Identify the framework and install the correct testing dependencies.

1.  **Detect Stack:** Check `package.json` for framework (React, Vue, Astro, etc.) and `wrangler.json(c)`.
2.  **Install Deps:** `npm install -D vitest jsdom acorn`
3.  **Configure:** Create `vitest.config.ts` or `vite.config.ts` with `environment: 'jsdom'`.
4.  **Wire Scripts:**
    ```json
    {
      "scripts": {
        "test:gate": "vitest run --reporter=verbose"
      }
    }
    ```

---

## Phase 1: The 4 Core Test Layers
Do not combine these files. They form the "Quality Gate."

### Layer 1: Frontend Safety (`test/frontend-safety.test.ts`)
Prevents white screens, template corruption, and syntax errors.
```javascript
test('app.js does not contain catastrophic corruption', () => {
    const code = fs.readFileSync('public/static/app.js', 'utf-8');
    expect(code).not.toMatch(/=\s*'[^']*\$\{t\(/); // Bug #1
    expect(code).not.toMatch(/<\s+[a-zA-Z]/); // Bug #2
});
```

### Layer 2: API Routes (`test/api-routes.test.ts`)
Ensures backend endpoints respond correctly.

### Layer 3: Business Logic (`test/business-logic.test.ts`)
Tests pure functions, validations, and transformations.

### Layer 4: i18n Synchronization (`test/i18n-sync.test.ts`)
Guarantees all language files have identical key counts.

---

## Phase 2: Execution (The Gates)

### Gate 1: Pre-Deploy Testing
**ALWAYS** run `npm run test:gate` before deploying. 0 failures required.

### Protocol

1.  **Check for skip override** (explicit user words only):
    -   ✅ "skip tests", "skip testing", "deploy without testing"
    -   ❌ "deploy", "quick deploy", "just push it" (= tests required)

2.  **Run test gate:**
    ```bash
    npm run test:gate
    ```

3.  **Parse results:** total files, total tests, failures, duration

4.  **Gate decision:**
    -   0 failures → proceed to deploy
    -   Any failures → **STOP. Fix first. Do NOT deploy.**

### Anti-Patterns

| DON'T | DO |
|-------|-----|
| Deploy then test | Test then deploy |
| "Tests passed earlier" | Run fresh test:gate NOW |
| Skip for "small changes" | Every change gets tested |
| Run test + deploy parallel | Sequential: test → gate → deploy |

### Gate 2: Evidence Before Claims
**ALWAYS** run the proving command before saying "fixed" or "done."

### The Gate Function

```
1. IDENTIFY → What command proves this claim?
2. RUN → Execute the FULL command (fresh)
3. READ → Full output, check exit code
4. VERIFY → Does output confirm the claim?
5. ONLY THEN → Make the claim
```

### Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test output: 0 failures | "Should pass", previous run |
| Build succeeds | Build: exit 0 | Linter passing |
| Bug fixed | Test symptom: passes | Code changed, assumed fixed |
| Requirements met | Line-by-line checklist | Tests passing |

### Red Flags — STOP
- Using "should", "probably", "seems to"
- Expressing satisfaction before verification
- Trusting agent success reports
- ANY wording implying success without running verification

### Gate 3: Frontend Integrity
Automated via Layer 1 above.

### When
Setting up or enhancing test suites for projects with frontend JavaScript/TypeScript.

### The 7 Layers

| Layer | What it checks | Priority |
|-------|---------------|----------|
| 1. Syntax Validation | JS parses without errors (via acorn) | **CRITICAL** |
| 2. Function Integrity | Named functions exist and are callable | Required |
| 3. Template Safety | HTML templates have matching tags | Required |
| 4. Asset References | Referenced files actually exist | Required |
| 5. Corruption Patterns | Known bad patterns (empty functions, truncation) | Required |
| 6. Import/Export | Module references resolve | Recommended |
| 7. CSS Validation | CSS files parse correctly | Recommended |

### Setup

```bash
npm install -D vitest acorn
```

### Layer 1: Syntax Check (Most Critical)

```javascript
import { parse } from 'acorn';
import { readFileSync } from 'fs';

test('app.js has valid syntax', () => {
  const code = readFileSync('public/static/app.js', 'utf-8');
  expect(() => parse(code, { ecmaVersion: 2022, sourceType: 'script' })).not.toThrow();
});
```

> This single test would have prevented the March 2026 white-screen incident.

---

### Gate 4: Update Working Memory

After ALL gates pass, update `.cm/CONTINUITY.md`:
- **Current Phase:** Set to `verified` or `ready-to-deploy`
- **Just Completed:** Add `✅ Quality gate passed: [test count] tests, 0 failures`

After ANY gate fails, **FIRST run Memory Integrity Check:**
1. List active learnings/decisions for the failing module
2. Ask: "Did AI follow a learning/decision that caused this failure?"
3. If YES → HEAL memory (invalidate/correct/scope-reduce) BEFORE recording new learning
4. Record meta-learning in `.cm/meta-learnings.json` if memory was the cause

**Then** update `.cm/CONTINUITY.md`:
- **Active Blockers:** Add the failing gate details
- **Mistakes & Learnings:** Record what failed with scope tag:
  - What Failed: [test/gate that failed]
  - How to Prevent: [fix pattern]
  - Scope: `module:{failing-module}` or `global` if systemic
  - Memory-caused: [yes/no — was existing memory the root cause?]

> **Token savings:** Next session instantly knows if last run passed or failed
> without re-running the test suite just to check status.

---

## Integration
| Skill | Relationship |
|-------|-------------|
| `cm-safe-deploy` | Quality gate is the primary blocker for the deploy pipeline |
| `cm-identity-guard` | Verify identity before using quality gate to ship |
| `cm-tdd` | TDD creates the logic for Layer 3 |
| `cm-safe-i18n` | Leverages Layer 4 for parity checks |
| `cm-safe-deploy` | **PRE-REQUISITE for production:** Security scan (Snyk + Aikido) PASS must be in deployment evidence. No production deploy without security clearance. |

## Evidence Requirements for Production Deploy

| Evidence | Command | Required |
|----------|---------|----------|
| Test suite passes | `npm run test:gate` | ✅ Always |
| Build succeeds | `npm run build` | ✅ Always |
| Security scan passes | `snyk test && aikido-api-client scan-release ...` | ✅ For production / public releases |
| i18n parity | Included in test:gate | ✅ If multilingual |

## Vibecoding Index (Phase 2)

After all gates pass, compute a 0–100 score for the change:

```bash
cm quality score --mode WARNING
```

Components (each weighted): **intent 30%, ownership 25%, context 20%, tests 15%, review 10%**.
Inputs are derived automatically from `.cm/handoff/{plan,exec,review,quality}.json` when present, or can be overridden with `--intent <0..1>`, `--ownership <0..1>`, etc.

Modes:
- `OFF` — silent (LITE projects)
- `WARNING` — print + advise (default; STANDARD projects)
- `SOFT` — warn loudly under 60 (PROFESSIONAL projects)
- `FULL` — exit 1 under 70 (ENTERPRISE projects, blocks deploy)

The default mode follows the project tier from `cm tier classify`.

## Karpathy Discipline — Loop Until Verified

The gate is where "goal-driven execution" actually closes the loop:
- **No claim without evidence.** "Tests pass" → paste the run. "Build green" → paste the hash. "Feature works" → paste the screenshot or HTTP response.
- **Loop independently while verifiable.** If the success criterion is concrete (test green, status 200, screenshot diff < threshold), keep iterating without asking. If criterion is vague, stop and ask — don't burn cycles on guesses.
- **Verify don't trust.** A subagent's summary says what it intended, not what it did. Re-run the gate yourself.

**Gate principle:** weak criteria fail here, not in production. Reject "make it work" handoffs back to planning.

## The Bottom Line

**Test before deploy. Scan before release. Evidence before claims. Safety before shipping. Non-negotiable.**
