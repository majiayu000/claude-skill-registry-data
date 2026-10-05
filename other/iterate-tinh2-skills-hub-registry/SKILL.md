---
name: iterate
description: Autonomous build loop — implements, tests, reviews, analyzes, and refines. Default 6 iterations (thorough) or --fast for 4 iterations (ship it quick).
version: 11
category: build
instructions: |
  You are in FULLY AUTONOMOUS MODE. Zero questions. Just build.

  TASK:
  $ARGUMENTS

  MODE DETECTION:
  - If $ARGUMENTS starts with "--fast" (e.g., "/iterate --fast add search bar"):
    MAX_ITERATIONS = 4 (fast mode -- build it, harden it, analyze it, ship it)
    Remove "--fast" from the task description before proceeding.
  - Otherwise: MAX_ITERATIONS = 6 (thorough mode -- full iterative refinement)

  RULES:
  - Do NOT ask the user anything. Decide and move.
  - If you're unsure between two approaches, pick the simpler one.
  - If a dependency is missing, install it.
  - If tests don't exist, write them.
  - If something breaks, fix it -- don't report it, fix it.

  === PRE-BUILD: BRANCH STRATEGY ===

  CHECK the project's CLAUDE.md and global CLAUDE.md for branch conventions.

  DEFAULT for solo/personal projects: commit directly to main. Do NOT create
  feature branches unless the project's CLAUDE.md explicitly requires them or
  the user asks for a branch. Solo projects use CI on main as the quality gate.

  For TEAM projects (multiple contributors): use feature branches.
  - Branch naming: `feat/{short-description}` for features, `fix/{short-description}` for fixes.
  - Push the branch early: `git push -u origin {branch}` after the first commit.
  - Merge via PR after validation.

  IMPORTANT: Before committing and pushing, run the project's full validation
  suite (format, lint, test) locally. Only push code that passes CI. This saves
  compute time on self-hosted runners.

  === PRE-BUILD: MIGRATION/FORK DETECTION ===

  If the project was scaffolded from, forked from, or migrated from another
  project (check git log for "migrate", "rename", "fork", or if early commits
  reference a different app name):
  1. Verify all references to the old project name are replaced (package names,
     bundle IDs, import paths, string constants, test fixtures, CI config).
  2. Verify models/services match the NEW domain, not the old one.
  3. Run the full test suite — failures from stale references are cheaper to
     fix now than after building features on a broken foundation.
  4. Commit any fixes: "chore: clean up migration from [old project]"
  Skipping this step causes downstream fix commits that tank First-Time-Right
  rate (observed: 45.5% FTR when migration validation was skipped).

  === PRE-BUILD: VALIDATION GATE ===

  Before writing any feature code, validate the project foundation.
  This prevents wasting iterations on lint, platform, and config issues.

  1. DETECT PROJECT TYPE:
     Identify the tech stack from project files (package.json, pubspec.yaml,
     Cargo.toml, go.mod, requirements.txt, pom.xml, Gemfile, etc.).
     Adapt all subsequent checks to the detected stack.

  2. STATIC ANALYSIS:
     - Run the project's type checker (tsc --noEmit, flutter analyze, mypy, cargo check, etc.).
     - Run the project's linter if configured (eslint, dart fix --apply, ruff, clippy, etc.).
     - Fix all errors and warnings.

  3. DEPENDENCY CHECK:
     - Run the project's dependency installer (npm install, flutter pub get, pip install, cargo build, etc.).
     - Fix version conflicts or missing packages.

  4. PLATFORM/CONFIG CHECK:
     - If the project has platform-specific code, verify guards are in place (e.g., web vs native,
       OS-specific imports, conditional compilation).
     - If the project has database rules/migrations, cross-check them against code usage.
     - If the project has config files (env templates, schema files), verify they match code expectations.

  5. DOCKER/INFRASTRUCTURE CHECK (if docker-compose.yml or Dockerfile exists):
     - Verify image references use full registry paths where needed.
     - Verify volume mounts: target paths exist in container, writable dirs have correct permissions.
     - Verify config files are mounted where the application actually reads them.
     - Run `bash -n` on all .sh scripts to catch syntax errors.
     - Check for cross-platform portability issues (sed, readlink, date flags, etc.).

  Fix everything found. Commit: "chore: pre-build validation fixes"
  If clean, skip the commit and proceed.

  === PER-COMPONENT QUALITY CHECKLIST ===

  Every component (screen, page, module, endpoint) you create or modify MUST
  satisfy these before committing. Applying these at creation time prevents
  dozens of retrofit commits later.

  a) ACCESSIBILITY:
     - Web: ARIA labels on interactive elements, focus management, keyboard navigation.
     - Mobile (Flutter): semanticLabel on icons/images, Semantics wrappers, 48dp touch targets.
     - Mobile (native): accessibilityLabel, accessibilityHint on interactive elements.
     - All: meaningful alt text, sufficient color contrast, screen-reader-friendly structure.

  b) DESIGN TOKENS:
     - Web: CSS custom properties or theme variables -- zero hardcoded hex colors or magic numbers.
     - Flutter: Colors from ColorScheme, TextStyles from TextTheme, spacing from constants.
     - Native: Style resources, design system tokens -- not inline literal values.
     - All: configurable values (rates, limits, feature flags) from config, not hardcoded.

  c) ASYNC SAFETY:
     - React: cleanup in useEffect return, abort controllers for fetch, check component mounted state.
     - Flutter: `if (!mounted) return;` before setState after every await.
     - General: cancellation tokens for long-running operations, cleanup on component unmount/dispose.
     - All: proper error handling on every async call, timeout on network requests.

  d) SCALABILITY:
     - Database queries have limits and pagination (no unbounded fetches).
     - Batch operations for multi-record writes.
     - Idempotent background jobs and event handlers.
     - Index coverage for compound/filtered queries.

  e) STRUCTURAL HEALTH: If any file exceeds 500 lines, decompose it into
     domain-specific modules. Do not let monolithic files grow across iterations.

  f) SHARED WIDGET / COMPONENT EXTRACTION:
     When 3+ screens/pages share visual patterns (cards, list items, dialogs,
     form sections, stat displays), extract a shared widget/component BEFORE
     building more screens. Cross-cutting changes (theme, a11y, responsive)
     applied to shared widgets fix all consumers at once instead of requiring
     per-screen modification waves.
     - Before creating a new screen, scan existing screens for reusable patterns.
     - If a pattern appears in 3+ places, extract it into a shared component first.
     - Track shared components in commit messages: "refactor: extract [widget] shared by [screens]"
     This prevents hotspot accumulation where the same screens are modified 5-9x
     each due to cross-cutting concerns applied in separate passes.

  MONOLITH DECOMPOSITION GATE:

  Before adding ANY feature code to a file that exceeds 500 lines:
  1. STOP. Do not add the feature to the monolithic file.
  2. Extract the relevant section into its own file first (component, service, module, utility).
  3. Verify the extraction works (tests pass, build succeeds).
  4. Commit the extraction: "refactor: extract [component] from [monolith]"
  5. THEN implement the feature in the newly extracted file.

  This is NOT optional. Flagging a file for future decomposition does not work --
  monoliths that get flagged but not split accumulate modifications and high fix-commit
  rates. Decompose BEFORE building, not after.

  HOTSPOT-AWARE DECOMPOSITION:

  At the START of each /iterate session (before Iteration 1), run a hotspot scan:

  ```
  git log --format='' --name-only -- '*.dart' '*.ts' '*.tsx' '*.js' '*.py' '*.go' '*.rs' \
    | sort | uniq -c | sort -rn | head -10
  ```

  Any file with 15+ modifications in the git history is a rework magnet. If you are
  about to modify a file with 15+ historical touches:
  1. DECOMPOSE IT FIRST — even if it is under 500 lines.
  2. Extract the section you need to modify into its own file.
  3. Then make your changes in the extracted file.

  Why: Hotspot scores are climbing every /metrics run across all projects. ProjectA
  profile_screen.dart has 68 touches, Skills Hub skill.service.ts had 43 touches
  before split, ProjectB analyze_screen.dart has 44 touches and is STILL 804 lines
  after 7 extraction attempts. The 500-line threshold is necessary but not sufficient
  — files that attract frequent changes need splitting at a LOWER threshold (300
  lines) or by domain concern, regardless of line count.

  MINIMUM TEST REQUIREMENT:

  Every iteration that adds new functionality must include:
  - Backend: At least 2 tests per new endpoint/function (happy path + error case).
  - Frontend: At least 1 component/integration test per new screen or major component.
  - If ZERO tests exist: set up test framework + 3-5 smoke tests first.
  A feature is not complete until its tests exist and pass.

  TEST CO-COMMIT ENFORCEMENT:

  Tests MUST be committed IN THE SAME COMMIT as the feature they test. Do NOT:
  - Write all features first, then batch-write tests in a separate commit/session.
  - Create a "test: add tests" commit that covers 5+ features at once.
  - Defer tests to "the next iteration" or "after the feature is stable."

  The commit pattern must be: `feat: add X [includes tests]` — not `feat: add X`
  followed later by `test: add tests for X, Y, Z, W`.

  Why this is non-negotiable: Test co-commit ratio (M8) is 0.00-0.32 across ALL 6
  projects. Batch-written tests discover stale interfaces (ProjectB TS2345 errors),
  miss wiring bugs, and inflate rework. ProjectA M8=0.28, ProjectB M8=0.04,
  DealWorthy M8=58% batch-written, Confidence Coach tests written 12 days after
  features. Tests written alongside features catch issues at creation time when the
  cost to fix is near zero.

  INTEGRATION TEST REQUIREMENT (for multi-layer projects):

  If the project has a cross-layer pipeline (e.g., client → API → service → response,
  or record → transcribe → analyze → enhance), at least ONE integration test must
  cover the end-to-end flow through 2+ layers:
  - Flutter: integration_test/ directory with a flow that exercises the real pipeline.
  - Node.js: supertest or similar hitting actual endpoints with real middleware.
  - General: a test that wires real components together (not mocked) to verify data
    flows correctly across boundaries.

  When to add: after Iteration 2 (MAKE IT SOLID), before domain analysis.
  Why: Confidence Coach had 27 unit/widget test files but ZERO integration tests.
  Unit tests verify individual components work; integration tests verify they work
  TOGETHER. Wiring bugs between layers are invisible to unit tests and are the most
  expensive to fix post-ship.

  === CO-COMMIT RULES ===

  These rules apply to EVERY iteration. Violating them is the #1 source of rework:

  a) SCHEMA/RULES: When adding or modifying a data model, update corresponding
     database rules, migrations, or schemas in the SAME commit. Never commit
     feature code without its schema changes.
  b) SERVER-SIDE VALIDATION: When adding client-side business logic (permission
     checks, eligibility, rate limits), wire up server-side enforcement in the
     SAME iteration. Client-only validation is not validation.
  c) SERIALIZATION: When backend code writes new fields, update the client model
     (fields, serialization, deserialization) in the SAME commit.
  d) EVENT HANDLERS: When changing data structures, verify triggers, webhooks,
     and event handlers still match in the same commit.
  e) SHARED CONFIGURATION: When 2+ files reference the same configurable value
     (model name, base URL, API key, timeout, port), extract to a shared config
     module. Never hardcode the same default in multiple files. Duplicated config
     is the #1 source of co-change rework in backend projects.

  ============================================================
  PROCESS: ITERATION LOOP (max MAX_ITERATIONS iterations)
  ============================================================

  Run this loop up to MAX_ITERATIONS iterations. Stop early ONLY when ALL exit
  criteria are met.

  === PRE-IMPLEMENTATION: EXTERNAL SERVICE CONTRACT VERIFICATION ===

  Before writing ANY code that integrates with an external service, STOP and verify:

  1. API/TEMPLATE CONTRACTS: If integrating with any external API (payment, email,
     auth, etc.) -- read the actual API field names, webhook payload shapes, and
     response formats FIRST. List them explicitly. Do NOT guess from memory.
  2. PLATFORM REQUIREMENTS: If adding CI/CD workflows, deploy pipelines, or
     platform-specific config -- verify platform constraints before committing
     (plan tier requirements, signing identities, required environment variables).
  3. TIMEOUT/LIMITS: When adding test steps or CI jobs, set timeouts to 2-3x the
     expected duration from the start. Never use the default.

  If you cannot verify locally, document the assumptions explicitly in a code
  comment and flag them for manual verification.

  === PRE-ITERATION: SECURITY-BY-DEFAULT CHECKLIST ===

  Before writing the FIRST line of feature code in Iteration 1, apply these
  defensive defaults to every new service, endpoint, or screen. Do NOT defer
  these to a later "security hardening" pass — that pattern caused 5-38 reactive
  security fix commits across every project.

  For EVERY new API endpoint/Cloud Function/route:
  - [ ] Rate limiting applied (or confirm existing global rate limiter covers it)
  - [ ] Input validation via schema (Zod, Joi, class-validator, etc.) — not manual checks
  - [ ] Error responses sanitized — no stack traces, internal paths, or DB errors leaked to client
  - [ ] Auth/ownership check — user can only access/modify their own resources (prevent IDOR)
  - [ ] Timeouts on all external calls (HTTP, DB, third-party APIs) — 30s default

  For EVERY new database query/Firestore operation:
  - [ ] Uses select/projection (not include/fetch-all) — only retrieve needed fields
  - [ ] Has pagination/limit — no unbounded result sets
  - [ ] Has appropriate index coverage for compound queries

  For EVERY new screen/component that handles user data:
  - [ ] Error states show user-friendly messages (no raw error objects)
  - [ ] Loading states prevent double-submission
  - [ ] Sensitive data (tokens, keys) not logged or exposed in error handlers

  Why: Security was discovered reactively across 3-5 separate passes in every
  project. Skills Hub had 38 security fix commits, DealWorthy had 5 IDOR/scoping
  fixes across 4 phases, ProjectB had 3 separate security hardening passes,
  Confidence Coach had error leaking fixed twice. A single upfront checklist
  prevents all of these.

  === ITERATION 1: MAKE IT EXIST ===

  - Build the simplest version that works. No polish, just function.
  - Apply the SECURITY-BY-DEFAULT CHECKLIST to every new endpoint/service/screen.
  - Co-commit schema changes, server validation, and model fields with features.
  - Co-commit tests with each feature (see TEST CO-COMMIT ENFORCEMENT above).
  - Run tests/build to verify.
  - Fix anything broken.
  - Keep commits incremental -- if touching 15+ files, split into logical commits.
  - Commit: "feat: initial implementation"

  === ITERATION 2: MAKE IT SOLID ===

  - Add error handling for real failure modes (not hypotheticals).
  - Add or fix tests for core behavior.
  - Verify all server-side validation is wired (not just client-side checks).
  - Run full validation -- fix until green.
  - Run domain analysis (see DOMAIN ANALYSIS section below).
  - Commit: "fix: harden implementation"

  === ITERATION 3: DOMAIN ANALYSIS GATE ===

  Run the `/analyze` skill scoped to everything you built or changed.
  Include all analysis phases: consistency audit, validation wiring,
  schema completeness, and platform compatibility.

  Scope: All features/files touched across iterations 1-2.
  Depth: Full analysis (all phases of /analyze).
  Action: FIX everything rated Critical or Warning. Re-run affected checks to confirm.
  Commit: "fix: resolve domain analysis issues"

  === ITERATION 4: CLEANUP / FINAL PASS (fast mode stops here) ===

  - Re-validate everything -- tests, build, re-check analysis.
  - Clean up code quality, naming, structure. Address remaining warnings.
  - If fast mode (4 iterations): this is the final pass. Ship it.
  - Commit: "refactor: cleanup"

  === ITERATION 5 (thorough mode only): HARDENING ===

  - Only run if analysis still finds issues or self-review scores < 4.
  - Re-run domain analysis to confirm previous fixes.
  - Address any remaining warnings.
  - Commit: "fix: hardening pass"

  === ITERATION 6 (thorough mode only): FINAL PASS ===

  - Only run if something still isn't right.
  - Final validation and polish.
  - Commit: "refactor: final pass"

  === SELF-REVIEW (run at end of each iteration) ===

  Score the current state on these dimensions (1-5):
  - Works: Does it run without errors? Do tests pass?
  - Correct: Does it actually do what was asked?
  - Clean: Is the code readable and maintainable?
  - Robust: Are edge cases handled? Is error handling adequate?
  - Wired: Are all layers connected? (schemas, server validation, serialization)

  Output the scores and a brief assessment of what to improve next iteration:

    ## Iteration N Self-Review
    - Works: X/5
    - Correct: X/5
    - Clean: X/5
    - Robust: X/5
    - Wired: X/5
    - Next focus: [what to improve]

  === DOMAIN ANALYSIS (runs on iteration 2 and on the final iteration) ===

  Run the `/analyze` skill scoped to the features you built or changed.
  Include all analysis phases: consistency audit, validation wiring,
  schema completeness, and platform compatibility.

  Scope: Only the features/files touched -- not the full project.
  Depth: Full analysis (all phases of /analyze).
  Action: If analysis finds Critical or Warning issues, feed them into the NEXT
  iteration's improvements as top-priority targets.

  === INTERMEDIATE QUALITY GATE ===

  When implementing MULTIPLE features (e.g., a list from a spec or backlog):
  - After every 3-4 features, run a mini domain analysis even if it's
    not iteration 2 yet. This catches cross-feature issues early.
  - Do NOT batch 8+ features into one iteration without a quality check.
  - If implementing 5+ features, split into batches of 3-4 and run validation
    between batches. This prevents mega-fix-commits later.

  === EXIT CRITERIA (ALL must be true to stop early) ===

  - All tests pass
  - Build succeeds (if applicable)
  - No lint errors (if linter exists)
  - Self-review scores are all 4+
  - Domain analysis shows zero Critical issues and zero Warning issues
  - Server-side validation is wired for all security-critical client logic
  - Schema/rules exist for all data the app reads/writes
  - The feature does what was requested

  === SCREEN/COMPONENT SIGN-OFF TABLE ===

  Before committing ANY screen or major component (new or modified), fill out
  this sign-off table:

  | Component | A11y | Tokens | Async | Scale | Structure | PASS? |
  |-----------|------|--------|-------|-------|-----------|-------|
  | {name}    | Y/N  | Y/N    | Y/N   | Y/N   | Y/N       | ALL Y |

  Rules:
  - Every column must be Y before committing. Any N = fix first, then re-check.
  - Include the checklist in commit messages: "feat: add profile page [A11y:Y Tokens:Y Async:Y Scale:Y Structure:Y]"
  - If implementing multiple components in one iteration, each gets its own row.
  - Do NOT batch components and "come back to fix a11y/tokens later" -- this is
    the #1 source of rework. Fix at creation time, not as a retrofit pass.

  Column definitions (quick reference):
  - A11y: ARIA/semantic labels, touch/click targets, keyboard navigation
  - Tokens: zero hardcoded colors or styles -- all from theme/design system
  - Async: cleanup on unmount, error handling on all async calls, timeouts
  - Scale: query limits, pagination, batch operations
  - Structure: file under 500 LOC, domain-split modules

  === PRE-COMMIT LOCAL VALIDATION ===

  Before EVERY commit (not just the pre-build gate), run the project's local
  validation suite. This catches format/lint/test failures BEFORE they hit CI,
  preventing fix chains like "fix: dart format" or "fix: eslint" that inflate
  the fix:feat ratio.

  1. DETECT & RUN the project's format/lint/test commands:
     - Flutter: `dart format --set-exit-if-changed . && flutter analyze && flutter test`
     - Node.js: `npm run lint && npm run format:check && npm test` (or equivalent)
     - Python: `ruff check . && ruff format --check . && pytest`
     - Go: `gofmt -l . && go vet ./... && go test ./...`
     - Rust: `cargo fmt --check && cargo clippy && cargo test`
     - Adapt to whatever stack is detected. Use the project's existing scripts.

  2. If ANY check fails: fix the issue BEFORE committing. Do NOT commit with
     the intent to "fix formatting in the next commit."

  3. This is NON-NEGOTIABLE. CI failure rates of 43-57% across projects are
     caused by skipping this step. Every format/lint fix commit pushed to CI
     is a wasted commit that degrades metrics.

  === COMMIT DISCIPLINE ===

  - Commit after each iteration with descriptive messages.
  - Keep commits focused. If an iteration touches 20+ files, split into logical commits.
  - NEVER batch all fixes into a single mega-commit like "lots of bug fixes".
    Each fix should be independently reviewable and revertable.
  - NEVER commit feature code without its corresponding schema/rules update.
  - Use conventional commits: feat:, fix:, chore:, test:, docs:
  - TAG EVERY FIX COMMIT WITH A SCOPE. Use `fix(category):` not bare `fix:`.
    Required categories: a11y, ux, scale, security, ci, test, perf, data, auth.
    Example: `fix(a11y): add semantic labels to profile screen`
    Unscoped fix commits (bare `fix:`) make root cause analysis impossible —
    53-86% of fix commits across projects are currently uncategorized, blocking
    data-driven rework reduction. If unsure of category, use the closest match.

  === POST-LOOP: RELEASE TAGGING ===

  After all iterations complete and validation passes, create a release tag.

  1. Check existing tags: `git tag --sort=-v:refname | head -5`
  2. Determine next version:
     - If no tags exist: use `v0.1.0`
     - If tags exist: bump the patch version (e.g., v0.2.1 → v0.2.2)
     - If a new feature was added: bump the minor version (e.g., v0.2.2 → v0.3.0)
  3. Create the tag: `git tag -a v{X.Y.Z} -m "feat: {short description of what was built}"`
  4. Push the tag: `git push origin v{X.Y.Z}`

  Why: D1 (Deployment Frequency) is 0/week across ALL projects — zero release tags
  in 500+ commits across 6 apps. Without tags, DORA metrics are unmeasurable, rollback
  is impossible, and there's no changelog anchor. /preflight checks for tags but no build
  skill was creating them.

  === POST-LOOP: DEAD CODE CLEANUP ===

  Before documenting, scan for dead code introduced or exposed during this build:

  1. If you REPLACED a file (new implementation supersedes old): delete the old file in
     the same commit or immediately after. Do not leave it "for reference."
  2. If you RENAMED a file: verify no imports reference the old name. Delete the old file.
  3. If you EXTRACTED code from a monolith: verify the extracted functions/classes are
     removed from the original file after extraction.
  4. Run: `git diff --name-status HEAD~{N}..HEAD` (where N = commits in this session)
     to review all Added/Deleted/Modified files. Flag any file that was Added then later
     superseded but not Deleted.

  Why: A bootstrap script survived 13 commits after being replaced. ProjectA
  accumulated dead screens and superseded services. Dead files create confusion about
  what is canonical and pollute grep/search results.

  === POST-LOOP: DOCUMENTATION ===

  After all iterations complete and validation passes:
  - Run `/readme` to generate or update the project's README.md.

  === OUTPUT ===

  One short summary:

    ## Build Summary
    - Mode: [thorough (6 iter) / fast (4 iter)]
    - What was built: [description]
    - Pre-validation: [issues found/fixed, or "clean"]
    - Iterations completed: N/MAX_ITERATIONS
    - Final validation: [tests/build/lint status]
    - Final scores: Works X/5, Correct X/5, Clean X/5, Robust X/5, Wired X/5
    - Domain analysis: [issues found / issues fixed / any remaining]
    - Server-side validation: [all wired / gaps found and fixed]
    - Schema/rules: [all data paths covered / gaps found and fixed]
    - Documentation: [README.md generated/updated]
    - Known limitations: [any trade-offs or deferred items]

  NEXT STEPS:

  Recommended pipeline after `/iterate`:
  - "Run `/qa` to verify everything works end-to-end."
  - "Run `/e2e` to generate automated end-to-end test coverage."
  - "Run `/iterate-review` to harden with a focused review pass."
  - "Run `/ux` to audit accessibility, design standards, and usability."
  - "Run `/polish` for the full quality pipeline: `/ux` → `/qa` → `/audit`."
---
