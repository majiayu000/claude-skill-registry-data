---
name: generate-speakmanai-code
description: Phase 3 of the SPEAKMAN.AI pipeline — implement a working, locally-runnable codebase from Phase 2 coding contracts. Routes to a language-specific variant based on TECH_STACK.
---

# generate-speakmanai-code — SPEAKMAN.AI Phase 3 Code Generator (Router)

You are executing Phase 3 of the SPEAKMAN.AI delivery pipeline. Your job is to implement a
complete, working, locally-runnable codebase from the Phase 2 coding contracts. You write,
install, test, and commit — you do not stop at generating files.

Every milestone has a gate: write code → install dependencies → run the validation command →
commit on pass, stop on failure. Do not advance past a failed gate.

The implementation details for each language are in a **variant skill file**. After loading
Phase 2 contracts in Step 1, you identify the language, read its variant file, and use its
`LANG_CONFIG` for all language-specific decisions throughout Steps 2–9. The DDD principles,
gate mechanics, and commit conventions in this file apply to every language.

---

## Step 0 — Collect Inputs

Ask the user:

> "Do you have Phase 2 output files already on disk?
>  - **Yes** → provide the path to the directory that contains a `raw/` folder
>    (e.g. `D:\git\tutorial\outputs\2026-06-15_my-project`)
>  - **No** → provide your Phase 2 SPEAKMAN.AI session ID and I'll fetch the contracts"

> "Where should the new project be created? Provide the parent directory path."

> "What is the project/repo name? This becomes the directory name."

> "What is the tech stack? Provide: language, runtime, framework, database, and any external
>   services. (e.g. `Go 1.22, chi, SQLite, JWT auth` or `JavaScript, Node.js 22, Express + React 18, SQLite`)"

> "Do you have a style guide or brand reference for the UI? (Used in Milestone 5 — skip if
>   no frontend.)
>  - **A file path** — a Markdown, CSS, or PDF design guide
>  - **A URL** — a brand or design page to mimic
>  - **None** — skip Milestone 5"

Store:
- **PHASE2_SOURCE**: local directory path OR session ID
- **PROJECT_ROOT**: parent directory where the repo will be created
- **REPO_NAME**: directory name for the new repo
- **REPO_PATH**: `{PROJECT_ROOT}/{REPO_NAME}`
- **TECH_STACK**: language, runtime, framework(s), database, external services
- **STYLE_SOURCE**: a file path, a URL, or `none`

---

## Step 1 — Load Phase 2 Contracts

### Branch A — Local files on disk

If PHASE2_SOURCE is a directory path, set **PHASE2_DIR** = that path and read:

| File | Variable | Contains |
|---|---|---|
| `{PHASE2_DIR}/raw/domain_model.txt` | DOMAIN_MODEL | Aggregates, value objects, invariants, repository interfaces |
| `{PHASE2_DIR}/raw/naming_dictionary.txt` | NAMING_DICT | Canonical names, banned synonyms, SQL/JSON/UI forms |
| `{PHASE2_DIR}/raw/use_case_catalog.txt` | USE_CASES | UC-XX IDs, Gherkin scenarios, actors, req_refs |
| `{PHASE2_DIR}/raw/api_schema.txt` | API_SCHEMA | OpenAPI 3.0 — endpoints, request/response schemas, field constraints |
| `{PHASE2_DIR}/raw/database_schema.txt` | DB_SCHEMA | Idempotent DDL — tables, columns, constraints |
| `{PHASE2_DIR}/raw/test_strategy.txt` | TEST_STRATEGY | Per-layer test type, tooling, mock boundaries, T-xxx IDs |

If `{PHASE2_DIR}/raw/field_definitions.txt` exists, read it as FIELD_DEFS. If absent, warn
and continue without it.

### Branch B — Fetch from SPEAKMAN.AI (uses credits)

If PHASE2_SOURCE is a session ID, call `get_outputs(PHASE2_SOURCE)` then fetch each contract
in parallel via `get_output(session_id, agent_id)`:

| Agent ID | Variable | Filename |
|---|---|---|
| `RE_DOMAIN_MODEL_SYNTHESIS_V1` | DOMAIN_MODEL | `domain_model.txt` |
| `RE_NAMING_CONVENTION_ARCHITECT_V1` | NAMING_DICT | `naming_dictionary.txt` |
| `RE_USE_CASE_ANALYST_V1` | USE_CASES | `use_case_catalog.txt` |
| `RE_API_SCHEMA_SYNTHESIS_V1` | API_SCHEMA | `api_schema.txt` |
| `RE_DATABASE_SCHEMA_DESIGNER_V1` | DB_SCHEMA | `database_schema.txt` |
| `RE_TEST_STRATEGIST_V1` | TEST_STRATEGY | `test_strategy.txt` |
| `RE_FIELD_DEFINITIONS_CATALOG_V1` | FIELD_DEFS | `field_definitions.txt` (optional) |

`RE_DOMAIN_MODEL_SYNTHESIS_V1` / `RE_API_SCHEMA_SYNTHESIS_V1` are synthesis aggregators that merge two upstream sub-agents server-side — fetch them like any other agent, the combined document shape is unchanged.

Save every fetched file to `{PROJECT_ROOT}/outputs/YYYY-MM-DD_{slug}/raw/` so future runs
use Branch A and incur no further credit cost.

---

### Step 1c — Select Language Variant

Derive **VARIANT** from TECH_STACK:

| If TECH_STACK contains… | VARIANT |
|---|---|
| "JavaScript", "Node.js", "TypeScript" | `js` |
| "Python", "FastAPI", "Flask", "Django" | `python` |
| "Java", "Spring", "Quarkus", "Kotlin" | `java` |
| "Go", "Golang" | `go` |

If no match, ask the user which registered variant to use and list the available ones.

**Read the variant file.** The variant SKILL.md is a sibling directory to this skill:

```
{this skill's parent directory}/generate-speakmanai-code-{VARIANT}/SKILL.md
```

For example, if this skill is at `C:\Users\davidis\.claude\skills\generate-speakmanai-code\SKILL.md`,
the Go variant is at `C:\Users\davidis\.claude\skills\generate-speakmanai-code-go\SKILL.md`.

Read the variant SKILL.md in full and extract **LANG_CONFIG** — the complete set of
language-specific constants and implementation guides defined in that file.

If the file is not found, stop and report:
> "No variant found for '{VARIANT}'. Available variants: js, go, python. To add a new language stack,
> see CONTRIBUTING.md in the generate-speakmanai-code skill directory."

---

### Derive shared variables

After reading LANG_CONFIG:

- **DIR_SKELETON**: apply LANG_CONFIG.DIR_SKELETON_LAYOUT to the aggregate names from
  DOMAIN_MODEL. Substitute `{aggregate}` with the lowercased aggregate name in each pattern.
  Include all entries marked "always present" in LANG_CONFIG.

- **DEPENDENCIES**: apply LANG_CONFIG.DEPENDENCIES_DERIVATION rules against TECH_STACK,
  API_SCHEMA, DOMAIN_MODEL, USE_CASES, and TEST_STRATEGY.

- **CODING_STANDARDS**: LANG_CONFIG.CODING_STANDARDS verbatim. All canonical names from
  NAMING_DICT take precedence over any inferred name.

- **VALIDATION_GATE**: LANG_CONFIG.VALIDATION_GATE verbatim.

---

## Step 2 — Scaffold Project

### 2a — Create directory structure

Create every directory from DIR_SKELETON. No implementation code yet.

Create `.gitignore` at the repo root using LANG_CONFIG.GITIGNORE_ENTRIES.

Create any scaffold files required by LANG_CONFIG.SCAFFOLD_FILES (build-tool entry points,
not application code).

### 2b — Create manifest files

Create one manifest file per service in DIR_SKELETON per LANG_CONFIG.SCAFFOLD_CONFIG.
(The manifest format differs by language: `package.json` for Node.js, `go.mod` + `Makefile`
for Go, `pom.xml` for Java, etc. — follow LANG_CONFIG.SCAFFOLD_CONFIG exactly.)

Wire build commands so every milestone validation target is defined. The root-level top-level
test command (`npm test`, `make test`, `mvn test`, etc.) must invoke all per-service test
suites sequentially.

After creating manifests, install all declared dependencies in each service:
```
LANG_CONFIG.MILESTONE_GATES.install   ← run in each service directory
```
This install step runs once at scaffold time. Re-run it in any service directory whenever
new dependencies are added, before re-running the affected gate.

### 2c — Create environment files

For each service that reads environment variables, create:
- An example env file (`.env.example`, `config.example.yaml`, or equivalent per LANG_CONFIG) —
  variable names with placeholder values and inline comments
- A working dev env file — generated secrets (see LANG_CONFIG.SECRET_GENERATION_CMD),
  non-conflicting port defaults, inter-service URLs, CORS origin

Do NOT commit the working dev env file — it must be in `.gitignore`.

### 2d — Git init and initial commit

```
git init {REPO_PATH}
```

Stage all scaffold files (manifests, example env files, `.gitignore`, directory structure):
```
chore: initialise repository structure
```

Do NOT commit dev env files.

---

## Step 3 — Milestone 1: Domain Layer

### What to write

From DOMAIN_MODEL, implement every aggregate root, child entity, and value object following
LANG_CONFIG.DOMAIN_IMPLEMENTATION_GUIDE for language-specific patterns.

**Domain layer absolute rules — no exceptions, regardless of language:**
- Zero imports of database drivers, HTTP libraries, file I/O, or any side-effecting module
- All functions/methods are pure and synchronous
- Every public export is documented (JSDoc, GoDoc, Javadoc, docstring per LANG_CONFIG)
- Invariant violations surface as a domain error carrying `code: VALIDATION_ERROR` — never
  HTTP status codes
- Repository interfaces (contracts) live in the application interfaces layer, not in domain

Repository interfaces: defined per LANG_CONFIG.REPO_INTERFACE_PATTERN (JSDoc `@typedef`,
Go `interface`, Java `interface`, Python `Protocol`, etc.).

Write domain unit tests covering every invariant and every value object per
LANG_CONFIG.DOMAIN_TEST_GUIDE. Include at least one failing case and one passing case per invariant.

### Gate

If new dependencies were added: `LANG_CONFIG.MILESTONE_GATES.install` (in each affected service).

Run LANG_CONFIG.MILESTONE_GATES.domain.

- **Pass**: commit: `"feat: implement domain layer — entities, value objects, invariants"`
- **Fail**: surface the full test output. Fix, re-run. Do not commit. Do not continue.

---

## Step 4 — Milestone 2: Application Layer

### What to write

From USE_CASES, implement one use case per UC-XX following
LANG_CONFIG.APPLICATION_IMPLEMENTATION_GUIDE.

**Application layer absolute rules:**
- Repositories are injected — never imported directly from infrastructure
- Never import from the interface layer
- Every mutation use case writes an audit log entry — not optional
- Business errors are domain error codes (`NOT_FOUND`, `UNAUTHORIZED`, `CONFLICT`,
  `VALIDATION_ERROR`) — never HTTP status codes

Write application unit tests per LANG_CONFIG.APPLICATION_TEST_GUIDE:
- Inject stubbed / mocked repository interfaces
- Cover every happy path and every unhappy path from USE_CASES
- Verify audit log repository is called on every mutation

### Gate

If new dependencies were added: `LANG_CONFIG.MILESTONE_GATES.install` (in each affected service).

Run LANG_CONFIG.MILESTONE_GATES.application.

- **Pass**: commit: `"feat: implement application layer — use cases {UC-01} to {UC-XX}"`
- **Fail**: fix, re-run. Do not continue.

---

## Step 5 — Milestone 3: Infrastructure Layer

### What to write

From DB_SCHEMA, implement per LANG_CONFIG.INFRASTRUCTURE_IMPLEMENTATION_GUIDE:
- A database connection module — singleton, initialised once at startup
- A migration runner — executes the full DDL idempotently on startup
- One repository implementation per aggregate root, mapping DB columns ↔ domain fields
  per NAMING_DICT (`sql_column` → domain field name)

**Infrastructure rules:**
- NOT_FOUND: when a query returns no row, surface as domain error `code: NOT_FOUND`
- CONFLICT: when a unique constraint is violated, surface as domain error `code: CONFLICT`
- Boolean columns: convert DB representation ↔ language boolean correctly
- Column names in SQL follow NAMING_DICT `sql_column` values
- Field names in the returned domain object follow NAMING_DICT canonical / `json_field` values

Write infrastructure integration tests per LANG_CONFIG.INFRASTRUCTURE_TEST_GUIDE:
- Use a real in-memory database (LANG_CONFIG.LOCAL_DB_TEST) — no mocks
- Run migrations before each test suite
- Test every repository method; test constraint violations produce correct domain error codes

### Gate

If new dependencies were added: `LANG_CONFIG.MILESTONE_GATES.install` (in each affected service).

Run LANG_CONFIG.MILESTONE_GATES.infrastructure.

- **Pass**: commit: `"feat: implement infrastructure layer — repositories and schema migrations"`
- **Fail**: fix, re-run. Do not continue.

---

## Step 6 — Milestone 4: Interface Layer

### What to write

Implement the HTTP interface, optional BFF layer, and optional frontend SPA following
LANG_CONFIG.INTERFACE_IMPLEMENTATION_GUIDE.

**Backend — non-negotiable interface rules (apply regardless of language):**
- Error handler returns a static string for any unhandled error (status 500) — never forward
  the raw error message or stack trace to the client
- Log every unhandled error before responding — silent 500s make production debugging impossible
- `GET /health` with no auth requirement — expected by every load balancer and uptime monitor
- Boolean request fields must be validated as strict boolean type — no coercions that silently
  accept strings or integers
- All inter-service URLs come from environment variables — never hardcoded

**Field Definitions Catalog enforcement (when FIELD_DEFS is present):**
- Enforce `minLength` / `maxLength` on string fields at the API boundary
- Enforce `minimum` / `maximum` on numeric fields
- Enforce `pattern` (regex) on string fields where specified
- Enforce `allowedValues` (enum) on constrained fields — VALIDATION_ERROR for out-of-range
- If a field has no constraint entry in FIELD_DEFS, flag as `[DECISION REQUIRED]`

**Domain error → HTTP status mapping (universal):**

| Domain error code | HTTP status |
|---|---|
| `NOT_FOUND` | 404 |
| `UNAUTHORIZED` | 401 |
| `CONFLICT` | 409 |
| `VALIDATION_ERROR` | 422 |
| unhandled | 500 (static message) |

**Domain event wiring:**
- For every event published by a use case that has a catalog consumer in USE_CASES, wire a
  subscriber in the composition root invoking the consuming use case
- A published event with a catalog consumer but no subscriber is an incomplete implementation
  — the downstream effect silently never happens
- The subscriber must not throw back into the publisher's request path — log and swallow

**BFF layer** (if LANG_CONFIG.BFF_PRESENT is true):
- Stateless, logic-free proxy — no business logic
- Forwards method, path, headers (especially `Authorization`), and body verbatim
- Returns backend response verbatim; returns 502 on network failure
- See LANG_CONFIG.BFF_IMPLEMENTATION for the language-specific proxy pattern

**Frontend SPA** (if a SPA framework is in TECH_STACK):
- All API calls through the BFF — never directly to the backend
- No business logic in components — only presentation and API calls
- All service URLs from environment variables

**UI completeness rule:**
- Every USE_CASES operation must be reachable from the UI
- Create forms include inputs for every field the API accepts (required AND optional)
- List views display all fields meaningful to the user
- Each list item has controls for every single-resource operation defined in API_SCHEMA
- Destructive actions require explicit user confirmation before the API call
- Edit forms pre-populate all current field values

**Styling (Milestone 4 default — Milestone 5 applies the real design system):**
- One stylesheet, no external framework
- Apply at minimum: centered max-width layout, consistent font, distinct button styles,
  form field spacing, basic table/card structure

Write interface integration tests per LANG_CONFIG.INTERFACE_TEST_GUIDE.

### Gate

If new dependencies were added: `LANG_CONFIG.MILESTONE_GATES.install` (in each affected service).

Run LANG_CONFIG.MILESTONE_GATES.interface.

- **Pass**: commit: `"feat: implement interface layer — API, BFF proxy, SPA"`
- **Fail**: fix, re-run. Do not continue.

---

## Step 7 — Milestone 5: UI Styling

**Skip if STYLE_SOURCE is `none`, or if there is no frontend in DIR_SKELETON.**

Extract the design system from STYLE_SOURCE (file or URL) — palette, typography, component
patterns, layout tokens. Rewrite the frontend stylesheet as a full design system with CSS
custom properties. Update all pages to use the design system classes.

**Design system rules:**
- CSS custom properties for every palette value — no hardcoded hex in component rules
- Inline style props only for values derivable only at runtime
- The stylesheet must stand alone: removing all inline styles must leave the UI visually correct

### Gate

Run LANG_CONFIG.MILESTONE_GATES.ui_build.

- **Pass**: commit: `"style: apply {brand/source} design system to all frontend pages"`
- **Fail**: fix, re-run. Do not continue.

---

## Step 8 — Milestone 6: E2E

From TEST_STRATEGY, implement one test file per use case covering every Gherkin scenario
marked as E2E, following LANG_CONFIG.E2E_IMPLEMENTATION_GUIDE.

**Chain dependent use cases through the API — no database seeding at journey seams:**
- Obtain values produced by one use case from the producing endpoint's real API response
- Database seeding only allowed for preconditions no in-scope use case can create

**Primary-journey tests:**
- For every actor flow in USE_CASES (ordered UC sequence), implement at least one journey
  test running the full sequence through the API

### Gate

If new dependencies were added: `LANG_CONFIG.MILESTONE_GATES.install` (in each affected service).

Run LANG_CONFIG.MILESTONE_GATES.e2e, then immediately run VALIDATION_GATE.

- **Pass** (both green): commit: `"feat: E2E acceptance tests — all UC-01 to UC-XX scenarios passing"`
- **Fail**: fix, re-run. Do not commit a broken state.

---

## Step 9 — Report

```
Project       : {REPO_NAME}
Location      : {REPO_PATH}
Language      : {VARIANT} (variant: generate-speakmanai-code-{VARIANT})
Commits       : 7 (initial scaffold + 6 milestones)
Validation    : {VALIDATION_GATE} — PASS

To run locally:
  {LANG_CONFIG.RUN_LOCALLY_INSTRUCTIONS}
```

List any `[DECISION REQUIRED]` items. If there are none, say so.

Then say: "Phase 3 complete. All milestone gates passed and committed. Proceed to Phase 4
(Terraform / cloud deployment) when ready."

---

## Rules

- **Never advance past a failed gate.** Fix the failure, re-run, confirm green before committing.
- **All names come from NAMING_DICT.** Canonical name for identifiers, sql_column for DB
  columns, json_field for API fields. Unknown names → `[DECISION REQUIRED]`.
- **No invented business rules.** Decisions not in Phase 2 contracts → `[DECISION REQUIRED]`.
- **Domain layer stays pure.** No I/O, no side effects. No exceptions.
- **Application layer never imports infrastructure.** Repositories always injected.
- **Tests pass before committing.** The git log must only contain passing states.
- **Dev env file is never committed.** Only the example file goes into git.
- **LANG_CONFIG is authoritative for all language-specific decisions.**
