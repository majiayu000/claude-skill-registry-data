---
name: test-suite-ensure
version: "1.1.0"
user-invocable: true
description: "Ensure the current project has a proper test suite — detect tech stack & framework, scaffold if needed, generate unit tests (required, logic code only), and optionally generate/run E2E tests. Triggers when user says \"test-suite-ensure\", 「补全测试」「生成测试」「确保测试」「补充单元测试」「添加单元测试」「检查测试覆盖」 (complete tests / generate tests / ensure tests / add unit tests / check test coverage). Also callable by solve-workflow and opsx-solve-workflow in their execution-stage test steps."
---

# Test Suite Ensure

Ensure the current project's test suite is in place: detect tech stack and framework, scaffold if necessary, generate unit tests (required, logic code only), and optionally generate/run E2E tests.

## Invocation Conventions

- **Standalone trigger**: When the user says a trigger word, run the full flow on the current project
- **Called by workflow**: Scope test generation to the workflow's changed logic files
- **Read SKILL.md before calling**: Workflows must read this file before each invocation — never call from memory

### Workflow modes

Workflow callers MUST declare one mode:

- **`mode=advisory`**: If required test scaffolding is absent and the user declines it, continue with a report reminder that logic changes lack generated tests. This is non-blocking.
- **`mode=mandatory`**: Refused required scaffolding or a failing unit-test run blocks exit from the execution stage. Resolve the issue or wait for the user before continuing.

Standalone invocation uses the full flow. The unit-test failure handling in Phase 5 still applies in both modes.

### Boundary vs `test-first-discipline`

This skill is **post-hoc**: detect stack, scaffold, generate/run tests for **existing** logic, advisory vs mandatory gating. It does **not** own failing-test-first order. Completing test-suite-ensure **MUST NOT** be described as satisfying `test-first-discipline`. When both are in scope, hosts run test-first during behavior implementation and test-suite-ensure afterward for coverage/scaffold gaps.

---

## Phase 1: Tech Stack Detection

Scan the project root to determine the primary language and framework:

| File | Detection |
|------|-----------|
| `package.json` | JavaScript / TypeScript |
| `go.mod` | Go |
| `requirements.txt` / `pyproject.toml` / `setup.py` | Python |
| `pom.xml` / `build.gradle` | Java |
| `Cargo.toml` | Rust |
| `*.csproj` / `*.sln` | C# / .NET |

If `package.json` is detected, further identify the frontend framework:

- Contains `"vite"` → prefer Vitest
- Contains `"react"` / `"vue"` / `"angular"` → frontend framework (but tests still cover logic layer only)
- Contains `"next"` / `"nuxt"` → server-side rendering framework
- Contains only `"express"` / `"fastify"` / `"koa"` etc. → pure Node.js backend

---

## Phase 2: Test Framework Detection

Detect existing test framework based on tech stack:

**JavaScript / TypeScript:**

- `jest.config.js` / `jest.config.ts` exists, or `package.json` `devDependencies` contains `jest` → Jest ✅
- `vitest.config.js` / `vitest.config.ts` exists, or `devDependencies` contains `vitest` → Vitest ✅
- `package.json` `scripts.test` is configured → corresponding framework ✅
- None found → needs scaffolding (see Phase 3)

**Python:**

- `pytest.ini` / `setup.cfg [tool:pytest]` / `pyproject.toml [tool.pytest.ini_options]` exists → Pytest ✅
- `devDependencies` or `requirements*.txt` contains `pytest` → Pytest ✅
- None found → needs scaffolding (see Phase 3)

**Go:**

- Built-in `go test`; detecting `go.mod` is sufficient ✅, no extra framework needed

**Java:**

- `pom.xml` contains `junit` dependency, or `build.gradle` contains `testImplementation 'junit'` → JUnit ✅

**Rust:**

- Built-in `cargo test`, no extra detection needed ✅

---

## Phase 3: Framework Scaffolding (only when Phase 2 determines "needs scaffolding")

Select and install based on tech stack:

| Tech Stack | Preferred Choice | Install Command |
|-----------|-----------------|-----------------|
| TypeScript + Vite project | Vitest | `npm install -D vitest @vitest/ui` |
| TypeScript / JavaScript general | Jest + ts-jest | `npm install -D jest ts-jest @types/jest` |
| Python | Pytest | `pip install pytest pytest-cov` |

Scaffolding steps:

1. Run the install command
2. Create minimal config file (`vitest.config.ts` / `jest.config.ts` / `pytest.ini`)
3. Add `"test"` entry to `package.json` `scripts` (if not present):
   - Vitest: `"test": "vitest run"`
   - Jest: `"test": "jest"`

**Tool constraints**: ✅ Bash allowed for install commands; ✅ Write allowed for config files

---

## Phase 4: Unit Test Scope Determination

### In Scope (Logic Code)

The following directories and file types are **in scope**:

- `services/`, `utils/`, `helpers/`, `lib/`, `core/`, `models/`, `store/`, `api/`
- Pure logic hooks (no JSX/template rendering in `hooks/`, `composables/`)
- Utility function files (`*.util.ts`, `*.helper.ts`, `*.service.ts`)
- State management logic (Vuex / Redux / Zustand / Pinia store logic layer)
- Data processing, formatting, validation, transformation functions

### Out of Scope (UI Layer — No Unit Tests)

The following directories and file types are **out of scope**:

- `components/`, `views/`, `pages/`, `layouts/`, `screens/`
- Files with JSX / template rendering: `.tsx`, `.vue`, `.svelte`, `.jsx`
- `*.stories.tsx`, `*.stories.ts` (Storybook)
- `__mocks__/`, `fixtures/` (test helper files)
- Style files (`*.css`, `*.scss`, `*.less`)

### Scope Priority

1. **When called by workflow**: Prioritize covering logic files from the workflow's changed files; if none provided, scan globally
2. **When standalone**: Scan globally, prioritize logic files without corresponding test files

---

## Phase 5: Unit Test Generation & Execution 【Required, Blocking】

### Generation Principles

- Each logic file maps to one test file; if one exists, **append** missing cases, don't overwrite
- Each function/method must cover at least three case types:
  - Happy path (normal input)
  - Boundary values (empty, zero, extreme input)
  - Error path (exception thrown, invalid input)
- Use the framework's native assertions; don't introduce extra assertion libraries

### Test File Naming Conventions

| Framework | Naming Convention | Recommended Location |
|-----------|-------------------|---------------------|
| Jest / Vitest | `<name>.spec.ts` or `<name>.test.ts` | Same dir as source, or `__tests__/` |
| Pytest | `test_<name>.py` or `<name>_test.py` | `tests/` dir or same dir as source |
| Go | `<name>_test.go` | Same dir as source (same package) |
| JUnit | `<Name>Test.java` | `src/test/java/` matching package path |

### Running

> For Node / JavaScript / TypeScript projects, align the Node version to the project-declared version before running — invoke the `node-version-discipline` skill (it probes the full chain `.nvmrc` / `.node-version` / `.tool-versions` / `volta` / `engines.node` / CI config, and asks the user if none declared). Tests on the wrong Node version produce false passes / false fails. Other stacks (Python / Go / Rust / Java) are unaffected.

```bash
# JavaScript / TypeScript (Jest)
npm test -- --passWithNoTests

# JavaScript / TypeScript (Vitest)
npx vitest run

# Python
pytest --tb=short

# Go
go test ./...

# Rust
cargo test

# Java (Maven)
mvn test

# Java (Gradle)
./gradlew test
```

### Blocking Conditions

When unit tests fail (non-zero exit code):

1. Output failed test list (filename + test name + error message)
2. Attempt auto-fix (max **2 rounds**: analyze error → modify test code or implementation)
3. After 2 rounds still failing: **stop, wait for user intervention**, output:
   - Failure cause analysis
   - Suggested fix direction (modify implementation / adjust test expectations / manually add mocks)

---

## Phase 6: E2E Test Detection & Execution 【Optional】

### Detect E2E Support

| Config File | Framework |
|-------------|-----------|
| `playwright.config.ts` / `playwright.config.js` | Playwright |
| `cypress.config.ts` / `cypress.config.js` | Cypress |
| `nightwatch.conf.js` / `nightwatch.conf.ts` | Nightwatch |
| `wdio.conf.js` / `wdio.conf.ts` | WebdriverIO |

- **Detected** → proceed with E2E test generation and execution
- **Not detected** → silently skip, note in output: "No E2E framework detected, skipping"

### E2E Test Generation Principles (only when framework is detected)

- Prioritize core user flows (login/registration, main business operations, key page navigation)
- When called by workflow, focus on pages/flows affected by this change
- If E2E cases exist, **append**, don't overwrite

### Running

```bash
# Playwright
npx playwright test

# Cypress (headless mode)
npx cypress run
```

On E2E failure: output failure screenshot path (if any) and failure reason; **do not block** the main flow (E2E is optional).

---

## Output Format

```text
【test-suite-ensure Results】
- Tech Stack: ... (e.g. TypeScript + Vite)
- Test Framework: Existing <name> / Newly installed <name> (with config file path)
- Unit Tests:
  - In-scope logic files: X
  - New test files: X, Appended cases: X
  - Run result: ✅ X passed, 0 failed / ❌ X failed (list failed tests)
- E2E Tests:
  - Detection: Detected <framework name> / Not detected, skipped
  - Run result: ✅ X passed / ❌ X failed (with screenshot path) / Skipped
```

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Including UI component files in unit test scope | Generates meaningless render tests, high maintenance cost | Strictly follow exclusion rules, cover logic layer only |
| Reinstalling when framework already exists | Dependency version conflicts | Skip Phase 3 when Phase 2 detects a framework |
| Overwriting existing test files | Loses existing test logic | Always use append mode, never overwrite |
| Continuing after 2+ rounds of unit test failures | Delivering with failing tests | Must stop after 2 rounds, wait for user intervention |
| Blocking main flow on E2E failure | E2E is optional, shouldn't be a hard gate | E2E failure only outputs a warning, doesn't block |
| Ignoring changed file list when called by workflow | Test coverage too broad or missing key changes | Prioritize changed files as scope, then expand globally |
