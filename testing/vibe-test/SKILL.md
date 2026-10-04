---
name: vibe-test
description: >
  Blast-radius-aware test generation for vibe-* projects.
  Traces every file a change touches, maps the full dependency graph,
  and writes complete test coverage across the entire blast radius —
  component tests, integration tests, and E2E tests.
  Extends existing tests in-place. Writes from scratch where none exist.
  Triggers on "test:" prefix, "write tests for", "test this feature",
  "add test coverage", "what needs testing", "test the blast radius",
  "coverage is missing", "write regression tests".
  Runs automatically at the end of vibe-add-feature and vibe-fix-bug sessions.
  Always use when any code has changed and test coverage must be verified or created.
  Never skips files. Never assumes untouched means unaffected.
---

# Vibe Test Skill

Blast-radius-aware test generation.
Traces the full dependency graph of any change, maps every affected file,
and writes complete coverage — component, integration, and E2E.
No gaps. No assumptions. Everything the change could have touched gets tested.

> **Autonomous / headless mode.** At startup resolve the settings with
> `python3 ~/.claude/skills/vibe-mode/scripts/vibe_state.py mode`. If `vibe_mode` is
> `autonomous`, every "wait", "ask", "confirm" and approval step in this skill follows
> vibe-mode's `references/HEADLESS.md` §2 instead: take the recommended option, accept your
> own draft after one self-check, log each choice to `vibe/DECISIONS.md`, never ask the
> user, and stop — writing `vibe/.run_state.json` — only when a person is genuinely required.

**Runs in agent mode (Claude Code / Cursor). Requires filesystem access.**

---

## The principle this enforces

A change is only complete when everything it could affect is verified.
Direct changes are obvious. Indirect consumers are where regressions hide.

This skill does not ask "what should I test?"
It asks "what could this break?" — then tests all of it.

**Assertions come from the intended behaviour, not from the code.** Derive what a
unit *should* do from the spec / acceptance criteria / bug report — ideally before
reading the implementation — and assert that. A test written by mirroring what the
code currently does is a tautology: it passes by construction and can never catch
the code being wrong. When there is a spec or a `done_when`, the test encodes it;
where behaviour is genuinely unspecified, name the assumption in the test's name.

**Testing is a loop, not a batch.** The value is not in generating test files — it
is in generate → run → observe the failure → repair → run again, until the suite is
green *for the right reason*. A green suite bought by weakening or deleting
assertions is worse than a red one, because it lies. (See Step 8.)

---

## Entry points

### Entry point A — On demand
Triggered by: `test:`, "write tests for X", "test this feature", "coverage is missing"

The user specifies what changed or what to test.
Go to **Step 1 — Identify the change set**.

### Entry point B — After vibe-add-feature
Triggered automatically at the end of a `feature:` session.

The change set is already known: every file listed in `FEATURE_TASKS.md` under **Touches**.
Skip Step 1. Read those files directly as the seed set.
Go to **Step 2 — Blast radius trace**.

### Entry point C — After vibe-fix-bug
Triggered automatically at the end of a `bug:` session.

The change set is already known: every file listed in `BUG_TASKS.md` under **Touches**.
The regression test written during `fix-bug` already exists — do not duplicate it.
Note it, include it in the coverage map, skip re-writing it.
Go to **Step 2 — Blast radius trace**.

---

## Step 0 — Read project context

**Large codebase check — run first, before reading anything:**

```bash
find . -type f \
  ! -path '*/node_modules/*' ! -path '*/.git/*' \
  ! -path '*/dist/*' ! -path '*/build/*' \
  | wc -l
```

**Set blast radius budget by project size:**

| Size | Files | Max blast radius files | Grep depth | Source file reads |
|------|-------|----------------------|------------|------------------|
| Small | < 50 | Unlimited | 2 levels | All affected |
| Medium | 50–200 | 30 files | 2 levels | All affected |
| Large | 200–500 | 20 files | 1 level | Direct consumers only |
| XL | 500+ | 15 files | 1 level | Seeds + direct only |

**For Large / XL projects:**
- Cap total blast radius at the budget above
- Prioritise: seeds → direct importers → contract consumers
- Skip indirect (Pass 2) if budget is reached after Pass 1
- Flag skipped files explicitly in the blast radius map:
  `⚠️ Budget reached — [N] indirect files not traced. Run test: on those modules separately.`
- Tell the user the cap was applied before presenting the blast radius map

Store the size classification. Apply the budget throughout Steps 2–3.

Read in this order before anything else:

1. `vibe/ARCHITECTURE.md` — testing philosophy, framework, conventions, test location rules
2. `vibe/CODEBASE.md` — section 1 (stack), section 2 (commands), section 4 (key files),
   section 5 (routes), section 7 (components), section 10 (patterns)
3. `vibe/SPEC.md` — acceptance criteria (drives what behaviour must be verified)
4. If Entry B: `vibe/features/[date-slug]/FEATURE_SPEC.md` + `FEATURE_TASKS.md`
5. If Entry C: `vibe/bugs/[date-slug]/BUG_SPEC.md` + `BUG_TASKS.md`

**Detect test runner from ARCHITECTURE.md and CODEBASE.md:**

| Stack | Default runner | Test command |
|-------|---------------|-------------|
| Node / Next.js / React | Jest or Vitest | `npm test` / `npx vitest` |
| Python / FastAPI / Django | pytest | `pytest` |
| Flutter / Dart | flutter test | `flutter test` |
| Go | go test | `go test ./...` |

**If no test runner detected:**
Read `references/RUNNER_SETUP.md`.
Ask the user which runner to install — present only options appropriate for their stack.
Generate setup instructions + install commands.
Wait for confirmation before proceeding.

**Detect E2E runner:**
- `playwright.config.*` present → Playwright installed
- `cypress.config.*` present → Cypress installed
- Neither present → E2E runner missing

> **Coordinate with `vibe-e2e`:** if the `vibe-e2e` skill is available, it owns the
> full isolated E2E suite (its own `e2e/` folder, live-URL runs, cleanup). Prefer
> delegating end-to-end coverage to it rather than writing a second, parallel
> Playwright suite here — two E2E suites (`vibe-test`'s vs `vibe-e2e`'s `e2e/`) will
> drift. Use this skill's E2E layer only for lightweight in-suite flows, or when
> vibe-e2e isn't present.

**If E2E runner missing (and not delegating to vibe-e2e):**
> "No E2E runner detected. Which would you like to set up?
> 1. Playwright — recommended for most projects
> 2. Cypress — if your team already uses it
> 3. Skip E2E for now — flag as coverage gap"

Wait for answer. If 1 or 2: read `references/RUNNER_SETUP.md` for setup instructions.
Generate the config file + install command. Present to user. Confirm before proceeding.

---

## Step 1 — Identify the change set (Entry A only)

Ask the user exactly what changed:
> "What changed? Give me file paths, a feature name, or describe what was modified."

From their answer, build the initial seed set — the specific files that were directly modified.

If vague ("I changed the auth system"):
- Read `vibe/CODEBASE.md` to locate relevant files
- List candidates: "These look like the auth-related files: [list]. Which ones changed?"
- Confirm the seed set before tracing

---

## Step 2 — Blast radius trace

**Check for dependency graph first:**
```bash
ls vibe/graph/DEPENDENCY_GRAPH.json 2>/dev/null && echo "GRAPH EXISTS" || echo "NO GRAPH"
```

**If graph exists — use it for blast radius (fast path):**

For each file in the seed set:
```
vibe-graph: query [file]
```

The graph returns the pre-computed blast radius — imports, imported_by,
test file, verifier, API routes, concept — in one read (~300 tokens).

Union the blast radii of all seed files. That is the full test scope.
No grep required. No file-by-file tracing.

**Validate graph result:**
For each file in the returned blast radius — confirm it exists:
```bash
ls [file_path] 2>/dev/null || echo "FILE NOT FOUND — graph may be stale for this node"
```

If any blast radius file doesn't exist → fall back to manual tracing for that node only.

**If no graph exists — manual trace (original approach):**

Starting from the seed set, trace all dependencies in three passes.

### Pass 1 — Direct importers (who imports the changed files?)

For each file in the seed set, run:

```bash
# TypeScript / JavaScript
grep -rn "from.*[filename-without-ext]" \
  --include="*.ts" --include="*.tsx" \
  --include="*.js" --include="*.jsx" \
  . | grep -v node_modules | grep -v ".test." | grep -v ".spec."

# Python
grep -rn "from [module] import\|import [module]" \
  --include="*.py" . | grep -v "__pycache__" | grep -v "test_"

# Go
grep -rn '"[module-path]"' --include="*.go" . | grep -v "_test.go"
```

For each importer found — does it use the specific thing that changed?
(function signature, exported type, API response shape, schema field)
If yes → add to blast radius. If it imports but doesn't use what changed → exclude.

### Pass 2 — Indirect importers (who imports the importers?)

Repeat Pass 1 for every file added in Pass 1.
Go **two levels deep maximum** — beyond that, the signal-to-noise ratio drops.
Flag if indirect chain is longer than 2 levels: note it but don't trace further.

### Pass 3 — Contract consumers (API / schema / type changes)

If the change touched an **API endpoint:**
```bash
# Find all consumers of this route
grep -rn "[route-path]" --include="*.ts" --include="*.tsx" \
  --include="*.js" --include="*.jsx" . | grep -v node_modules
```

If the change touched a **database schema / model:**
```bash
# Find all files referencing this model
grep -rn "[ModelName]\|[table_name]" \
  --include="*.ts" --include="*.py" --include="*.go" \
  . | grep -v node_modules | grep -v "migrations"
```

If the change touched a **shared type or interface:**
```bash
grep -rn "[TypeName]\|[InterfaceName]" \
  --include="*.ts" --include="*.tsx" \
  . | grep -v node_modules | grep -v ".test."
```

---

## Step 3 — Build the blast radius map

Consolidate all three passes into a structured map.
Classify every affected file by layer:

```
BLAST RADIUS — [change description]
Seeds (directly changed):
  [file path] — [what changed]

Layer 1 — Direct consumers:
  [file path] — [what it uses from the seed] — [has tests: yes/partial/no]

Layer 2 — Indirect consumers:
  [file path] — [chain: seed → L1 → this file] — [has tests: yes/partial/no]

Contract consumers:
  [file path] — [uses: route / model / type] — [has tests: yes/partial/no]

Existing regression tests:
  [test file] — [what it covers] (Entry C only — from vibe-fix-bug)
```

Check test coverage for each file:
```bash
find . -name "*.test.*" -o -name "*.spec.*" | grep -v node_modules
```

For each affected file, check if a corresponding test file exists.
Read existing test files for affected files — note what's covered and what's missing.

**Classify each affected file:**
- `COVERED` — tests exist and cover the affected behaviour
- `PARTIAL` — tests exist but don't cover what changed
- `NONE` — no test file exists at all

Present the blast radius map to the user.
Ask: "Does this look right? Any files to add or remove from scope?"
Wait for confirmation before proceeding.

---

## Step 4 — Generate the test spec

Read `references/TEST_SPEC_TEMPLATE.md` for the full format.

For each affected file in the blast radius, draft what tests are needed:

**For COVERED files:**
Note existing coverage. Identify the specific gap introduced by the change.
Document: "extend [test file] — add [N] tests covering [what changed]."

**For PARTIAL files:**
List what's already tested. List what's missing.
Document: "extend [test file] — missing: [list of uncovered behaviours]."

**For NONE files:**
Write a full test plan from scratch.
Derive expected behaviours from `SPEC.md` acceptance criteria where possible.
Where SPEC.md doesn't cover it, derive from reading the actual source file.

**Layer ordering in the spec:**
1. Integration tests (API endpoints, DB queries) — test the data contracts first
2. Component tests (UI interactions, rendering, state) — test against verified data
3. E2E tests (full user flows) — test the assembled system last

**For each test, specify:**
- Test file path (where it will be written)
- Describe block and test name
- Setup (mocks, fixtures, test data)
- Action (what to call or render)
- Assertion (what to verify)
- Why this test — what failure it would catch

Present the full test spec.

> "Here's the complete test plan across [N] files — [N] integration,
> [N] component, [N] E2E tests. Approve to write all files."

**Wait for explicit approval before writing a single file.**

---

## Step 5 — Write tests: Layer 1 — Integration tests

Write all integration tests first.
API endpoints and DB queries are the foundation — UI tests depend on them being correct.

**For each integration test file:**

Read the source file in full before writing tests.
Read any existing test file to understand the established pattern.

Test every affected endpoint:
- Happy path — correct input, expected output
- Auth boundary — authenticated vs unauthenticated where applicable
- Validation — invalid input handled correctly
- Edge cases — empty, null, boundary values
- Error states — what happens when downstream fails

For DB-touching code: use test transactions that roll back, or a test database.
Never write tests that mutate production data.

**Write pattern — always follow ARCHITECTURE.md testing conventions:**
```
[Actual test code following the project's exact patterns from CODEBASE.md section 10]
```

After writing each file: run the tests immediately.
```bash
[test command from CODEBASE.md section 2] [test file path]
```

If tests fail: fix before moving to next file.
If tests pass: mark file complete, continue.

---

## Step 6 — Write tests: Layer 2 — Component tests

Write all component tests after integration tests pass.

**For each component test file:**

Read the component source in full.
Read `vibe/ARCHITECTURE.md` for the component testing approach.
Check `vibe/DESIGN_SYSTEM.md` if it exists — visual states may need testing.

Test every affected component:
- Renders correctly with standard props
- Renders correctly in empty/loading/error states
- User interactions fire correct handlers
- State changes produce correct UI updates
- Conditional rendering shows/hides correctly

For components that call APIs: mock the API layer using the project's established mock pattern.
Never make real API calls in component tests.

Write using the established component test pattern from `CODEBASE.md section 10`.

Run after each file. Fix failures before continuing.

---

## Step 7 — Write tests: Layer 3 — E2E tests

Write E2E tests last — they verify the assembled system, not individual units.
E2E tests are scoped to full user flows that the change affects.

**For each E2E test:**

Derive flows from `SPEC.md` acceptance criteria.
Only test flows that the blast radius change could have affected.
Do not duplicate flows already covered by existing E2E tests.

Map each flow:
1. Starting state — what the user sees before
2. Actions — exact user interactions (click, type, navigate)
3. Assertions — what the user sees after
4. Edge case flows — error states, empty states, auth boundaries

**Playwright pattern:**
```typescript
test('[flow name]', async ({ page }) => {
  // arrange
  // act
  // assert
})
```

**Cypress pattern:**
```javascript
it('[flow name]', () => {
  // arrange
  // act
  // assert
})
```

Follow the exact E2E pattern from `CODEBASE.md section 10` if one exists.
If no pattern exists (first E2E tests): establish one and document it in `CODEBASE.md`.

Run E2E suite after all tests are written:
```bash
npx playwright test   # or
npx cypress run
```

---

## Step 8 — Run full suite and verify

After all layers are written, run the complete test suite:

```bash
[full test command from CODEBASE.md section 2]
```

Required outcome: **all tests green, zero failures** — green for the right reason.

Run the loop until it settles, one failure at a time:
1. Run the suite; read the failure output carefully (message, stack, actual vs expected).
2. **Classify the failure before touching anything:**
   - the assertion was wrong / tested the wrong thing → fix the **test**;
   - the test is right and the code misbehaves → fix the **source** (this is the
     test doing its job — a real bug caught);
   - the test is flaky (passes/fails without a code change) → stabilise it, don't
     paper over it.
3. Apply the smallest fix for that one failure, then re-run.
- Never make a test pass by weakening or deleting the assertion it was written to
  make — if it revealed a real bug, the bug gets fixed, not the test.
- Do not suppress, `.skip`, or comment out failures to reach green.
- Do not move to Step 9 until the suite is fully green with its assertions intact.

---

## Step 9 — Update vibe docs

**vibe/CODEBASE.md:**
Add every new test file to section 4 (key files) or section 10 (patterns).
If a new E2E pattern was established, document it in section 10.

**vibe/TASKS.md:**
Update "What just happened":
```
## What just happened
✅ Tests written — [N] files across blast radius
   Integration: [N] tests · Component: [N] tests · E2E: [N] tests
   All passing. Full suite green.
```

**vibe/reviews/backlog.md:**
If any file was excluded from coverage (user removed from scope in Step 3):
Log as P2: "Coverage gap — [file] excluded from blast radius testing on [date]."

**FEATURE_TASKS.md / BUG_TASKS.md (if Entry B or C):**
Mark test tasks as complete. Tick conformance checklist items:
- [x] All new tests pass
- [x] All existing tests still pass
- [x] No regressions in related features

---

## Step 10 — Report

```
✅ vibe-test complete

BLAST RADIUS
  Seeds:              [N] files changed
  Direct consumers:   [N] files
  Indirect consumers: [N] files
  Contract consumers: [N] files
  Total in scope:     [N] files

COVERAGE WRITTEN
  Integration tests:  [N] new · [N] extended · [files]
  Component tests:    [N] new · [N] extended · [files]
  E2E tests:          [N] new · [N] extended · [files]
  Regression tests:   [N] carried from fix-bug (Entry C only)

SUITE RESULT
  [N] tests passing · 0 failing · 0 skipped

GAPS FLAGGED
  [Any P2 backlog entries added — or "None"]

WHAT'S NEXT
  review:   ← gate now has real coverage to verify against
```

---

## Absolute rules

**Never skip a file.** If it's in the blast radius, it gets tested.
"It probably still works" is not a reason to skip.

**Never mock what you're testing.** Mock the layer below.
Testing a service? Mock the DB. Testing a component? Mock the API. Never mock the subject.

**Never write tests that can't fail.** Every assertion must be able to catch a real regression.
A test that always passes regardless of implementation is noise, not coverage.

**Never move to the next layer if the current layer is red.**
Integration tests must be green before component tests.
Component tests must be green before E2E tests.

**Never write E2E tests for flows the change didn't affect.**
E2E tests are expensive. Scope them tightly to the blast radius.

**Always run after writing.** Never deliver unrun tests.
