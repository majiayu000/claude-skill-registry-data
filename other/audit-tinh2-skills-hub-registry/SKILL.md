---
name: audit
description: Fast quality gate — detects stack, runs static analysis, checks cross-layer consistency, fixes issues. Run between every pipeline phase, before every commit push, after every feature batch. Lighter than /analyze but catches the same critical issues.
version: "2.0.0"
category: qa
platforms:
  - CLAUDE_CODE
---

You are a fast domain consistency auditor. Do NOT ask the user questions.
Detect the project stack, validate, fix, and report. This skill is designed to
run quickly between pipeline phases as a quality gate — it is lighter than
`/analyze` but catches the same critical issues. Run this aggressively: between
phases, before deploys, after refactors, before PRs.

TARGET:
$ARGUMENTS

If no arguments provided, audit the entire project in the current working directory.

============================================================
PHASE 0: STACK DETECTION
============================================================

Detect the project stack by checking for marker files. A project may use
multiple stacks (e.g., Python backend + React frontend). Detect ALL that apply:

| Stack | Marker Files |
|-------|-------------|
| Flutter/Dart | `pubspec.yaml` |
| React / Next.js | `package.json` with react/next deps |
| Node.js / Express | `package.json` with express/fastify/nest deps |
| Python | `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile` |
| Go | `go.mod` |
| Rust | `Cargo.toml` |
| Java / Spring | `pom.xml`, `build.gradle` |
| Ruby on Rails | `Gemfile` with rails dep |

Also detect infrastructure:
| Infra | Marker Files |
|-------|-------------|
| Firebase | `firebase.json`, `firestore.rules` |
| Docker | `Dockerfile`, `docker-compose.yml` |
| Terraform | `*.tf` files |
| Serverless | `serverless.yml`, `sam-template.yaml` |
| GraphQL | `*.graphql`, `schema.graphql`, `*.gql` |
| gRPC / Protobuf | `*.proto` files |

Record detected stacks — all subsequent phases adapt to what was found.

============================================================
PHASE 1: STATIC VALIDATION (fast, automated)
============================================================

Run every automated check available FOR THE DETECTED STACKS:

FLUTTER (if detected):
- `flutter analyze` — record errors and warnings.
- `dart fix --apply` to auto-fix.
- Re-run `flutter analyze` to confirm.
- Check for unguarded `dart:io` imports in web-reachable code.
- Check platform-specific code is guarded with platform checks or conditional imports.

REACT / NEXT.JS (if detected):
- Run `npx tsc --noEmit` if TypeScript.
- Run the configured linter (`npm run lint` or `npx eslint .`).
- Check for `next build` errors if Next.js.

NODE.JS / EXPRESS (if detected):
- `npx tsc --noEmit` or the project's type-check command.
- Run the project's linter if configured.

PYTHON (if detected):
- Run `ruff check .` or `flake8` or `pylint` (whichever is configured).
- Run `mypy .` or `pyright` if type checking is configured.
- Check for `ruff format --check .` or `black --check .` if formatter is configured.

GO (if detected):
- `go vet ./...`
- `go build ./...` (compile check).
- Run `golangci-lint run` if available.

RUST (if detected):
- `cargo check`
- `cargo clippy -- -D warnings` if clippy is available.

JAVA / SPRING (if detected):
- `./mvnw compile` or `./gradlew compileJava` (compile check).
- Run checkstyle/spotbugs if configured.

RUBY ON RAILS (if detected):
- `bundle exec rubocop` if configured.
- `bin/rails db:migrate:status` to check pending migrations.

TESTS (all stacks):
- Run the test suite using the project's test command. Record pass/fail counts.
- Do NOT fix failing tests yet — just record.

Fix all static analysis errors. Commit: "fix(audit): static analysis cleanup"
If clean, skip commit.

============================================================
PHASE 2: CROSS-LAYER CONSISTENCY (targeted, fast)
============================================================

Run a TARGETED subset of the `/analyze` skill's checks yourself — do NOT invoke
`/analyze` directly. Unlike full `/analyze`, this phase checks only the CRITICAL
consistency paths — what actually breaks at runtime.

Adapt checks to the detected stack. Focus areas:

UNIVERSAL (all stacks):
- Data model / schema fields match what service/controller layers read and write.
- API contracts (REST routes, GraphQL resolvers, gRPC service methods) match
  what clients actually call — method names, parameter types, response shapes.
- Environment variables referenced in code exist in `.env.example` or config docs.
- Database migrations / schema are in sync with model definitions.

FRONTEND ↔ BACKEND (if both detected):
- API call URLs/endpoints in frontend match backend route definitions.
- Request/response types match across the boundary (field names, types, nullability).
- Auth tokens / headers sent by frontend match what backend middleware expects.
- Error response shapes frontend parses match what backend actually returns.

SERVERLESS / CLOUD FUNCTIONS (if detected):
- Function triggers (HTTP, event, schedule) are correctly wired.
- IAM / security rules match code access patterns (e.g., Firestore rules vs. code paths).
- Function ↔ model field completeness (backend writes visible to frontend).

NAVIGATION / ROUTING (if frontend detected):
- All referenced routes/screens are defined.
- Route parameters match what receiving screens/pages expect.

CONFIG PROPAGATION:
- Admin-configurable or environment-driven values are not hardcoded.
- Feature flags referenced in code are defined in config.

Scope: Full project, but only CRITICAL paths.
Depth: Quick checks — flag issues but don't deep-dive every layer.

Flag issues as:
- **Critical**: Will crash or fail at runtime. Must fix.
- **Warning**: Inconsistency that may cause bugs under certain conditions.
- **Info**: Minor issue, not auto-fixed.

============================================================
PHASE 3: FIX (single pass)
============================================================

Fix all Critical and Warning issues found in Phase 2.
For each fix:
1. Apply the fix.
2. Re-run the specific check to confirm.
3. Re-run static analysis for the affected stack to verify no regressions.

Commit all fixes: "fix(audit): cross-layer consistency fixes"

If fixes introduce new issues, fix those too (max 2 rounds).


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing fixes, re-validate your work:

1. Re-run the specific checks that originally found issues.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes

============================================================
OUTPUT
============================================================

Keep the output concise. This is a gate check, not a deep analysis.

## Audit Results

**Stack detected:** [list detected stacks and infra]

### Static Analysis
- [Stack]: [clean / N errors fixed]
- Tests: [X/Y passing]

### Consistency Check

| Layer Pair | Checked | Critical | Warning | Info | Fixed |
|-----------|---------|----------|---------|------|-------|
| Model ↔ Service/Controller | N | N | N | N | N |
| API Contract ↔ Client Calls | N | N | N | N | N |
| Frontend ↔ Backend Types | N | N | N | N | N |
| Auth / Security Rules ↔ Code | N | N | N | N | N |
| Routes / Navigation | N | N | N | N | N |
| Config / Env Propagation | N | N | N | N | N |
| Schema / Migration Sync | N | N | N | N | N |

(Omit rows that don't apply to the detected stack.)

### Issues Fixed
[Brief list of what was fixed, with file references]

### Remaining Issues
[Info-level items not auto-fixed]

### Verdict

**PASS**: Zero critical and zero warning issues. Safe to proceed.
**FAIL**: N critical / N warning issues remain. List them.

NEXT STEPS:

After PASS:
- "Continue with the next pipeline phase."
- "Run `/iterate` to build the next feature."

After FAIL:
- "Fix the remaining issues, then run `/audit` again."
- "Run `/analyze` for a deeper investigation of the failing areas."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /audit — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
