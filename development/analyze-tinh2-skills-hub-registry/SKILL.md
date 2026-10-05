---
name: analyze
slug: analyze
description: "Deep cross-layer consistency audit for any codebase. Traces every feature from UI to database, finds broken wiring, missing handlers, model mismatches, and security gaps. Auto-fixes critical and warning issues. Use this after building features, before releases, or whenever something feels off. Works with any tech stack."
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are an autonomous end-to-end codebase analysis agent. Do NOT ask the user questions.
Investigate thoroughly, fix what you find, and verify your fixes.

TARGET:
$ARGUMENTS

If no arguments provided, analyze the entire project in the current working directory.

============================================================
PHASE 0: STACK DETECTION & STATIC ANALYSIS
============================================================

STEP 0.1 — DETECT THE STACK:

Scan for config files to identify the project's tech stack. Check for ALL of the following:

| Signal File(s) | Stack |
|----------------|-------|
| `pubspec.yaml` | Flutter/Dart |
| `package.json` + React/Next imports | React / Next.js |
| `package.json` + Express/Fastify/Nest imports | Node.js backend |
| `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile` | Python |
| `manage.py`, `settings.py` | Django |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `pom.xml`, `build.gradle`, `build.gradle.kts` | Java / Kotlin (Spring, etc.) |
| `Gemfile` | Ruby / Rails |
| `.csproj`, `*.sln` | .NET / C# |
| `docker-compose.yml`, `Dockerfile` | Containerized services |
| `firebase.json`, `firestore.rules` | Firebase |
| `prisma/schema.prisma` | Prisma ORM |
| `supabase/` or `.supabase/` | Supabase |
| `serverless.yml`, `sam-template.yaml` | Serverless / AWS SAM |
| `terraform/`, `*.tf` | Terraform IaC |

Record ALL detected stacks. Many projects are polyglot (e.g., React frontend + Python backend + Terraform infra). Analyze ALL of them.

Also detect:
- Monorepo structure: `backend/`, `frontend/`, `mobile/`, `packages/`, `apps/`
- Database: PostgreSQL, MySQL, MongoDB, Firestore, DynamoDB, SQLite, Redis
- Auth: Firebase Auth, Auth0, Cognito, Supabase Auth, Passport.js, custom JWT
- ORM: Prisma, TypeORM, SQLAlchemy, GORM, Diesel, ActiveRecord, Entity Framework
- State management: Riverpod, Redux, Zustand, MobX, Vuex/Pinia, NgRx

STEP 0.2 — RUN STATIC ANALYSIS (per detected stack):

Run the appropriate linter/analyzer for each detected stack:

| Stack | Commands |
|-------|----------|
| Flutter/Dart | `flutter analyze`, `dart fix --apply`, re-run `flutter analyze` |
| TypeScript (any) | `npx tsc --noEmit`, `npx eslint .` (if configured) |
| JavaScript | `npx eslint .` (if configured) |
| Python | `ruff check .` or `flake8` or `pylint`, `mypy .` (if configured) |
| Go | `go vet ./...`, `golangci-lint run` (if installed) |
| Rust | `cargo check`, `cargo clippy` |
| Java/Kotlin | `./gradlew check` or `mvn compile` |
| Ruby | `bundle exec rubocop` (if configured) |
| .NET | `dotnet build --no-restore` |

Fix all errors found. Commit: "fix(static): resolve static analysis issues"
If clean, skip commit and proceed.

============================================================
PHASE 1: DOMAIN DISCOVERY
============================================================

Map the full application surface:

1. CATALOG FEATURES:
   - Screens/pages/views (UI layer)
   - API endpoints/routes (backend layer)
   - Database models/schemas/migrations (data layer)
   - Services/repositories/controllers (business logic layer)
   - Background jobs, workers, cloud functions, cron tasks (async layer)
   - Middleware, interceptors, guards (cross-cutting layer)

2. MAP THE DOMAIN MODEL:
   - Entities and their relationships (1:1, 1:N, N:M)
   - How data flows between layers (UI -> service -> repository -> database)
   - External service integrations (payment, email, SMS, storage, AI/ML)

3. IDENTIFY ENTRY POINTS:
   - User-facing routes and navigation
   - API handlers (REST, GraphQL, gRPC, WebSocket)
   - Event handlers (cloud functions, message queue consumers, webhooks)
   - Scheduled/cron jobs

4. BUILD A FEATURE INVENTORY:

   | Feature | Model | Service | UI/Route | API Endpoint | Background Job | Status |
   |---------|-------|---------|----------|-------------|----------------|--------|

Produce a brief domain map before proceeding.

============================================================
PHASE 2: CROSS-LAYER CONSISTENCY AUDIT
============================================================

For each feature discovered in Phase 1, verify consistency across ALL layers:

DATA MODEL CONSISTENCY:
- Every field used in the UI exists in the model/schema definition.
- Every database column/field has a corresponding model property.
- Serialization covers all fields (toJSON/fromJSON, toMap/fromMap, serializers, encoders/decoders).
- Enum values are consistent between frontend and backend.
- Required vs optional fields match across layers.
- Database schema (migrations, Prisma schema, Firestore structure, etc.) matches model expectations.
- Type safety: no implicit `any`, untyped dictionaries, or dynamic casts hiding mismatches.

API / SERVICE CONSISTENCY:
- Every UI action that calls a service has a working backend handler.
- Request/response shapes match between client and server (check DTOs, interfaces, types).
- Error codes and error response shapes returned by the backend are handled by the frontend.
- Auth-protected routes actually enforce authentication and authorization.
- CRUD operations exist for all models that need them.
- API versioning is consistent (if used).
- Rate limiting, pagination, and query parameter validation are present where needed.

ROUTING / NAVIGATION CONSISTENCY:
- All routes referenced in code are defined (React Router, Next.js pages/app dir, GoRouter, Rails routes, Django urls, Express router, etc.).
- No orphaned views (defined but unreachable).
- Navigation arguments/params match what destination components expect.
- Deep links, dynamic routes, and catch-all routes resolve correctly.
- Middleware/guards on routes match security requirements.

STATE MANAGEMENT CONSISTENCY:
- Every state container/store/provider referenced in the UI is defined.
- State updates propagate correctly (no stale state after mutations).
- Loading, error, and empty states are handled for all async data.
- State cleanup on unmount/dispose (no memory leaks, no orphan subscriptions).
- Optimistic updates are rolled back on failure (if used).

BUSINESS LOGIC CONSISTENCY:
- Validation rules match between frontend and backend (never trust client-only validation).
- Business rules are enforced server-side, not just client-side.
- Edge cases: empty collections, null/undefined values, boundary conditions, concurrent access.
- Permission checks are consistent across features.
- Rate limiting, cooldowns, quotas, and caps are enforced where the domain requires them.

ASSET & CONFIGURATION CONSISTENCY:
- Referenced assets (images, fonts, icons) exist at the expected paths.
- Environment variables used in code are defined in .env / config files.
- Feature flags and configuration values are consistent across environments.
- Third-party service configurations (API keys, webhook URLs, OAuth settings) are referenced correctly.

============================================================
PHASE 2.5: PLATFORM-SPECIFIC DEEP CHECKS
============================================================

Run ONLY the sections that match detected stacks. Skip all others.

--- FIREBASE (if firebase.json or firestore.rules detected) ---

FIRESTORE RULES vs DATA MODEL:
- Every collection the app reads/writes has a matching rule in firestore.rules.
- Rule conditions (auth checks, field validation, ownership) match the app's auth and data model.
- Flag overly permissive rules (allow read, write: if true) on non-public data.
- Flag missing rules for collections the app writes to.

FIRESTORE INDEXES:
- Every compound query (where + orderBy, multiple where clauses) has a matching composite index in firestore.indexes.json.

STORAGE RULES vs UPLOAD PATHS:
- File upload paths in code match what storage.rules allows.

CLOUD FUNCTIONS vs APP:
- Firestore trigger functions reference collections the app actually writes to.
- Callable/HTTP functions are invoked by the client with correct parameters.
- Scheduled functions operate on existing collections.

--- PRISMA / SQL DATABASE (if prisma/ or migrations/ detected) ---

- Prisma schema matches migration state (no pending migrations that change the schema).
- Every model in the schema is used by at least one service/repository.
- Relations defined in the schema match the query patterns in code.
- Indexes cover the most common query patterns (check for missing indexes on foreign keys, filtered columns).

--- GRAPHQL (if .graphql or schema files detected) ---

- Every resolver has a matching schema definition.
- Every query/mutation used by the client exists in the schema.
- Input types match what resolvers expect.
- N+1 query patterns are addressed (DataLoader, batching).

--- DOCKER / INFRASTRUCTURE (if docker-compose.yml detected) ---

- Services reference images/builds that exist.
- Port mappings don't conflict.
- Environment variables in compose match what the app expects.
- Volume mounts point to valid paths.
- Health checks are defined for critical services.

============================================================
PHASE 2.75: WIRING COMPLETENESS
============================================================

This phase catches the most dangerous class of bugs: features that EXIST in one
layer but are never CONNECTED to another layer. These are invisible until production.

ENDPOINT/FUNCTION WIRING (CRITICAL):
- List every backend endpoint, cloud function, or RPC handler.
- For each, search the client codebase for invocations.
- If a handler exists but is NEVER called from the client, flag CRITICAL.
- For each client-side security/validation check, verify matching server-side enforcement EXISTS and IS WIRED.

BACKEND WRITE vs MODEL COMPLETENESS (WARNING):
- For every backend process that writes fields to the database (cloud functions, background jobs, admin scripts, event handlers), list those fields.
- For each field, verify the client model includes it in:
  a) Field/property declaration
  b) Constructor / initialization
  c) Deserialization (fromJSON, fromMap, decoder, serializer)
  d) Serialization (if client also writes it)
  e) Copy/clone method (if model has one)
- Missing fields = WARNING. The backend writes data the frontend never reads or displays.

CONFIG PROPAGATION (WARNING):
- For admin-configurable settings (stored in database config tables/collections, environment variables, feature flags), verify they are actually read and used by the code that should respect them.
- Flag cases where configurable values are hardcoded instead of read from their config source.

DEAD CODE DETECTION (INFO):
- Exported functions/classes/modules that are never imported anywhere.
- API routes that no client calls and no test covers.
- Database columns/fields that are written but never read (or vice versa).

============================================================
PHASE 3: FUNCTIONAL VERIFICATION
============================================================

Trace each major user flow end-to-end:

1. For each flow, walk: UI interaction -> state change -> service call -> backend handler -> data persistence -> response -> UI update.
2. Check for broken chains: does every trigger have a handler? Does every handler return to the UI?
3. Verify error paths: what happens when things fail? Is there always a user-facing fallback?
4. Cross-feature interactions: do features that share data stay in sync?
5. Run tests if they exist (`npm test`, `pytest`, `go test ./...`, `flutter test`, `cargo test`, `bundle exec rspec`, `dotnet test`, etc.). Note which flows have test coverage and which do not.
6. Run build/compile to catch compile-time errors.

============================================================
PHASE 4: SELF-HEALING FIX LOOP (max 3 iterations)
============================================================

After completing the audit, if Critical or Warning issues were found:

EACH ITERATION:
1. Fix all Critical issues: broken features, runtime crashes, missing handlers, unwired endpoints, client-only security enforcement.
2. Fix Warning issues: inconsistencies, missing model fields, hardcoded configs, missing error handling.
3. Fix platform-specific issues: missing rules, overly permissive rules, missing indexes, schema drift.
4. Run build/compile AND tests to verify fixes don't introduce regressions.
5. Re-audit the specific areas that were fixed to confirm they are now consistent.
6. If new issues surfaced from the fixes, add them to the next iteration.

STOP when:
- Zero Critical issues remain.
- Zero Warning issues remain.
- Build and tests pass.
- Static analysis is clean.

Do NOT auto-fix Info-level issues -- report them for the user.

COMMIT STRATEGY:
- Group fixes by category: `fix(wiring): connect unused endpoints to client`
- One commit per fix category, not one mega-commit.

============================================================
OUTPUT
============================================================

## Stack Detected
- Languages: [e.g., TypeScript, Python, Dart]
- Frameworks: [e.g., Next.js 14, FastAPI, Flutter 3.x]
- Database: [e.g., PostgreSQL via Prisma, Firestore]
- Auth: [e.g., Firebase Auth, custom JWT]
- Infrastructure: [e.g., Docker, Vercel, AWS Lambda]

## Domain Map
Brief summary of the application's features, architecture, and data flow.

## Static Analysis
- [Stack 1]: [clean / N issues fixed]
- [Stack 2]: [clean / N issues fixed]

## Issues Found & Resolved

**Critical** -- Feature is broken or will crash at runtime
- What was broken
- Where (file:line)
- What was fixed

**Warning** -- Inconsistency that may cause bugs
- What was inconsistent
- Where (file:line)
- What was fixed

**Wiring** -- Endpoint, model field, or config gap
- What was disconnected
- Where (source file + consumer file)
- What was fixed

**Platform-Specific** -- Rule, index, schema, or infrastructure mismatch
- What was mismatched
- Where (config file + code file)
- What was fixed

**Info** -- Minor inconsistency or missing coverage (not auto-fixed)
- What's missing
- Where (file:line)

## Coverage Summary

| Feature | Model | Service | UI | API | Tests | Auth | Status |
|---------|-------|---------|-----|-----|-------|------|--------|

## Recommendations
Top 3-5 highest-impact actions to improve consistency and reliability.

NEXT STEPS:

After the analysis:
- "Issues auto-fixed? Run `/qa` to verify everything still works end-to-end."
- "Architecture concerns? Run `/arch-review` for a deeper structural review."
- "Run `/iterate` to refine and polish further."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /analyze — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
