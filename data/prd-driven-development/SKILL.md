---
name: prd-driven-development
description: "Systematic PRD-driven software development workflow for Claude Code. Use when the user wants to (1) Import/parse feature bundles into draft PRDs with dependency analysis, (2) Create comprehensive Product Requirements Documents from feature descriptions, (2b) Extend existing PRDs with new requirements (version increment), (3) Break down PRDs into structured task lists with dependencies and test plans, (4) Systematically execute task lists with quality gates and verification protocols, (5) Audit test coverage and correctness against specifications, (6) Generate comprehensive PRD status reports showing completion states and progress tracking, or build complete applications from requirements through to tested implementation following enterprise-grade practices."
---

# PRD-Driven Development Workflow

This skill provides a complete workflow for building software applications from Product Requirements Documents (PRDs) through structured task execution and test auditing, following enterprise-grade development practices with built-in quality gates, dependency management, and traceability.

## How to Use This Skill

### Invocation Method

This skill contains a **complete 6-phase workflow** for PRD-driven development. The workflow phases are **built into the skill itself** and don't require separate slash command files.

**To use this skill:**

1. **Invoke the skill once:**
   ```
   skill: prd-driven-development
   ```

2. **Then use natural language** to trigger workflow phases:
   - "Import PRDs from specs/features.md"
   - "Create a PRD for user authentication feature"
   - "Extend PRD-0001 with OAuth authentication"
   - "Generate tasks from prds/0001-prd-auth.md"
   - "Process task list tasks/tasks-0001-prd-auth.md"
   - "Audit tests for completed features"
   - "Generate status report"

### Command Notation in This Documentation

Throughout this skill documentation, you'll see commands referenced like:

```
@import-prds <PATH_TO_FEATURES_FILE>
@create-prd <FEATURE_DESCRIPTION|PATH>
@generate-tasks <PATH_TO_PRD_FILE>
```

**Important:** These are **workflow phase triggers**, NOT separate slash command files. The `@` notation is just a **documentation convention** to clearly mark workflow phases.

**You invoke them by:**
- ✅ Natural language after invoking the skill: "Import PRDs from specs/features.md"
- ✅ Explicit phrasing: "Using Phase 1, import PRDs from specs/features.md"
- ❌ NOT as slash commands: `/import-prds` (these files don't exist)

### Integration with Slash Commands

This skill works **alongside** existing slash commands:

- **Skill Workflow** → Creates PRDs, generates task lists, manages dependencies
- **Slash Commands** (@code, @test, @debug, @ask) → Recognize and update skill outputs (PRD files, task files)

**Example Integration:**
```
skill: prd-driven-development
# Creates PRD and task files

@code implement feature X
# Recognizes task file and updates it automatically

@test add coverage for authentication
# Adds tests and updates task completion status
```

## Prerequisites

### CLAUDE.md Architecture Baseline (REQUIRED)

All commands require a `CLAUDE.md` file at the repository root containing or linking to:
- System architecture and service boundaries
- Tech stack (languages, frameworks, versions)
- Data stores, migrations, and messaging
- Testing strategy and quality gates
- CI/CD and environments
- Feature flags and rollout practices

**Bootstrap Process (First-Time Setup):**

If `CLAUDE.md` is missing, the skill will automatically:
1. Check if `CLAUDE.md.template` exists at root
2. Copy it to `CLAUDE.md`
3. Guide you through filling required sections interactively:
   - Tech stack (languages/frameworks - detect from package.json, requirements.txt, go.mod, etc.)
   - Testing strategy (frameworks - suggest based on detected stack)
   - Data stores (databases - detect from dependencies)
   - Architecture type (monolith/microservices/serverless)
4. Mark template sections that need your input with `[TODO: Fill this]`
5. Save the populated `CLAUDE.md`

You can also manually run: "Create CLAUDE.md from template and help me fill required sections"

**If neither file exists:** The skill will generate a basic `CLAUDE.md` with detected stack information and placeholders.

### Testing Requirements Hierarchy (CRITICAL)

**CLAUDE.md is the authoritative source for testing requirements:**

1. **Read CLAUDE.md Testing Strategy section FIRST**
2. **Respect explicit exclusions:**
   - If CLAUDE.md says "No unit tests" → Do NOT generate unit tests
   - If CLAUDE.md says "No integration tests" → Do NOT generate integration tests
   - If CLAUDE.md says "No E2E tests" → Do NOT generate E2E tests
3. **If CLAUDE.md is silent, has template text, or Testing Strategy section is incomplete:**

   **⚠️ Default Assumption: Testing is REQUIRED**

   Apply test requirements based on PRD complexity:

   **`simple` complexity:**
   - Unit tests: For core business logic only
   - Integration tests: Optional (only if API or database involved)
   - E2E tests: Optional (only if frontend-backend interaction exists)

   **`standard` complexity (DEFAULT):**
   - Unit tests: **REQUIRED** for all FRs involving business logic, validation, utilities
   - Integration tests: **REQUIRED** for all FRs involving APIs, database operations, service integration
   - E2E tests: **AUTOMATIC** for frontend-backend features (login, registration, CRUD, forms, real-time, chatbots)

   **`complex` complexity:**
   - Unit tests: **REQUIRED** for all FRs
   - Integration tests: **REQUIRED** for all FRs
   - E2E tests: **REQUIRED** when applicable (all user-facing frontend-backend flows)

   **Important:** When CLAUDE.md Testing Strategy is incomplete, the workflow will:
   - Prompt: "CLAUDE.md Testing Strategy has template text. Applying defaults: unit + integration + E2E (auto-detect for UI features). Continue? (yes/customize)"
   - Allow customization before proceeding
   - Update CLAUDE.md with chosen strategy

   **Never skip tests due to difficulty** - invest significant effort in making tests work (see Escalation Paths section below)

**Lightweight Mode Triggers (automatically use `simple` complexity):**
- Bug fixes that don't add new functionality
- Configuration changes (env vars, feature flags, settings)
- Documentation updates
- Infrastructure scripts
- Database schema changes ONLY (no business logic)

**Examples:**

✅ CLAUDE.md says: "Unit: Jest (required), Integration: Supertest (required), E2E: None (infrastructure not available)"
→ Skill generates unit + integration only, NO E2E tests

✅ CLAUDE.md says: "Unit: pytest, Integration: TestContainers, E2E: Playwright for critical flows"
→ Skill generates all three test types with diligence

✅ CLAUDE.md says: "Testing: TBD" or has generic template text
→ Skill applies default requirements (unit + integration mandatory, E2E for UI-backend)

**Never override CLAUDE.md explicit requirements.**

### Global Standards

Define in `CLAUDE.md` or linked docs:
- Performance SLO/SLIs, availability targets
- Accessibility level requirements
- Security/privacy/tenancy model
- Test environment standards (Testcontainers, docker-compose)
- ADR (Architecture Decision Records) workflow

## Quick Start Example

Here's a minimal example showing the complete workflow with a trivial feature: "Add /health endpoint"

### 1. Setup (One-Time)

```
skill: prd-driven-development
"Create CLAUDE.md from template"
```

**Output:** `CLAUDE.md` created with detected stack (Node.js from package.json)

**Fill minimum sections:**
- Tech Stack: Node.js 18, Express 4
- Testing: Jest (unit), Supertest (integration)
- Database: None (simple API)

### 2. Create PRD

```
"Create a PRD for: Add a /health endpoint that returns {status: 'ok', uptime: <seconds>}"
```

**Claude asks clarifying questions:**
- Q: "Should this be authenticated?" → A: "No, public endpoint"
- Q: "Any specific uptime format?" → A: "Seconds as integer"

**Output:** `prds/0001-prd-health-endpoint.md` with:
- PRD-0001-FR-1: Endpoint returns 200 with JSON payload
- PRD-0001-FR-2: Payload includes status and uptime fields
- PRD-0001-NFR-1: Response time < 50ms

### 3. Generate Tasks

```
"Generate tasks from prds/0001-prd-health-endpoint.md"
```

**Output (Phase 1 - Parent Tasks):**
```markdown
## Tasks

### 1.0 [  ] Create /health endpoint handler (PRD-0001-FR-1, PRD-0001-FR-2)

### 2.0 [  ] Verify performance requirements (PRD-0001-NFR-1)
```

**Claude stops and waits:**
"I've generated parent tasks. Review them above. Reply 'Go' to proceed with detailed sub-tasks."

**You reply:** "Go"

**Output (Phase 2 - Sub-Tasks):**
```markdown
### 1.0 [  ] Create /health endpoint handler

  - [ ] 1.1 Write unit tests for health check logic (PRD-0001-FR-2)
  - [ ] 1.2 Write integration test for GET /health endpoint (PRD-0001-FR-1)
  - [ ] 1.3 Implement /health route handler
  - [ ] 1.4 Run tests and fix failures

### 2.0 [  ] Verify performance requirements

  - [ ] 2.1 Add performance test harness (PRD-0001-NFR-1)
  - [ ] 2.2 Run performance tests and verify < 50ms
```

**Also created:** `tasks/_index.md` (global dependency tracker)

### 4. Execute Tasks

```
"Process task list tasks/tasks-0001-prd-health-endpoint.md"
```

**Claude works through sub-tasks one at a time:**

**Sub-task 1.1 (Unit Tests):**
```javascript
// tests/health.test.js
describe('PRD-0001-FR-2 health check data', () => {
  test('returns status ok', () => {
    const data = getHealthData();
    expect(data.status).toBe('ok');
  });

  test('returns uptime as integer', () => {
    const data = getHealthData();
    expect(Number.isInteger(data.uptime)).toBe(true);
  });
});
```

**Sub-task 1.2 (Integration Tests):**
```javascript
// tests/health.integration.test.js
describe('PRD-0001-FR-1 GET /health endpoint', () => {
  test('returns 200 with JSON', async () => {
    const res = await request(app).get('/health');
    expect(res.status).toBe(200);
    expect(res.body).toMatchObject({
      status: 'ok',
      uptime: expect.any(Number)
    });
  });
});
```

**Sub-task 1.3 (Implementation):**
```javascript
// routes/health.js
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    uptime: Math.floor(process.uptime())
  });
});
```

**Sub-task 1.4 (Run Tests):**
```bash
npm test
✓ All tests passing (2 unit, 1 integration)
```

**Parent 1.0 Complete - Quality Gates:**
- ✅ Lint: `npm run lint` passes
- ✅ Type-check: `tsc --noEmit` passes
- ✅ Security: `npm audit` clean
- ✅ Coverage: 100% (meets threshold)

**Commit:**
```
feat: add /health endpoint (PRD-0001-FR-1, PRD-0001-FR-2)

- Returns {status, uptime} as JSON
- Adds unit and integration tests
- Response time verified < 50ms

Related to PRD-0001
```

### 5. Audit Tests (Optional)

```
"Audit tests for completed features"
```

**Output:** `TEST_AUDIT.md` with:
- ✅ Coverage: 100% (2 FRs fully tested)
- ✅ Correctness: Tests validate right behavior
- ✅ Traceability: All tests map to PRD-0001-FR-n
- ✅ Quality Gates: All passing

### Final Directory Structure

```
.
├── CLAUDE.md
├── prds/
│   └── 0001-prd-health-endpoint.md
├── tasks/
│   ├── _index.md
│   └── tasks-0001-prd-health-endpoint.md
├── routes/
│   └── health.js
├── tests/
│   ├── health.test.js
│   └── health.integration.test.js
└── TEST_AUDIT.md
```

**For detailed walkthrough with more complex features, see:** `references/quick-start-tutorial.md`

## Core Workflow

### Phase 1: Import Feature Bundle (Optional)

**Workflow Phase:** Import PRDs from feature bundle

**How to invoke:** "Import PRDs from `<PATH_TO_FEATURES_FILE>`" or "Use Phase 1 to import PRDs from `<PATH_TO_FEATURES_FILE>`"

**Use when:** You have a single spec file containing multiple features.

**Process:**
1. Validate `CLAUDE.md` exists with architecture baseline
2. Parse bundle to identify distinct features
3. Extract draft PRD skeletons with preliminary dependencies and sizing
4. Build `/prd-bundle/index.md` with dependency graph and critical path
5. Detect cross-feature conflicts

**Deliverables:**
- `/prd-bundle/index.md` - Global summary and dependency graph
- `/prd-bundle/[nn]-draft-prd-[feature-name].md` - Draft PRD skeletons

**Next Steps:** Use Phase 2 on each draft to finalize into `/prds/`

### Phase 2: Create Comprehensive PRD

**Workflow Phase:** Create Product Requirements Document

**How to invoke:** "Create a PRD for `<FEATURE_DESCRIPTION>`" or "Create a PRD from `<PATH_TO_DRAFT>`" (optional: "with complexity level: simple/standard/complex")

**Complexity Profiles:**
- `simple` - Lightweight mode for UI-only features, bug fixes, scripts, config changes (minimal testing requirements)
- `standard` - Standard mode for typical features (default - unit + integration required)
- `complex` - Comprehensive mode for multi-service, data-heavy features (all test types when applicable)

**Process:**
1. Validate `CLAUDE.md` architecture baseline
2. Analyze feature description
3. Ask tiered clarifying questions (Critical → Important → Nice-to-have)
4. Generate PRD with PRD-scoped IDs (`PRD-####-FR-n`, `PRD-####-NFR-n`)
5. Save to `/prds/[nnnn]-prd-[feature-name].md`

**Key PRD Sections:**
- Introduction, Goals, User Stories
- Functional Requirements (with PRD-scoped IDs)
- Acceptance Criteria (testable, linked to FR IDs)
- Non-Functional Requirements (measurable targets)
- API Contract, Dependencies & Predecessors
- Test Strategy, Feature Flags & Rollout
- Database Change Verification Checklist
- Operational Readiness, Definition of Done
- Traceability Matrix

**Next Step:** Use Phase 3 on the finalized PRD

### Phase 2b: Extend Existing PRD

**Workflow Phase:** Extend an existing PRD with new requirements

**How to invoke:** "Extend PRD-0001 with OAuth authentication" or "Add social login to PRD-0001"

**Use when:**
- Adding new capabilities to a completed PRD
- Enhancing existing features without breaking changes
- Versioning up an existing feature (v1.0 → v2.0)

**Smart Detection:**

The workflow automatically determines if your request is:
- ✅ **Extension** (backward compatible) → Updates existing PRD, appends tasks
- ❌ **Breaking change** (incompatible) → Suggests creating new PRD instead

**Extension Criteria (automatic approval):**
- Adds new FRs/NFRs with incremented IDs (FR-6, FR-7, etc.)
- Doesn't modify existing FR acceptance criteria
- Backward compatible architecture changes
- Can be implemented without rewriting existing code

**Breaking Change Criteria (suggests new PRD):**
- Modifies existing FR definitions
- Requires existing code rewrites
- Incompatible architecture changes
- Changes existing API contracts

**Process:**

1. **Read existing PRD file**
   - Load `prds/0001-prd-feature.md`
   - Parse current version, FRs, NFRs
   - Check completion status in `prds/_index.md`

2. **Analyze extension requirements**
   - Ask clarifying questions about new capabilities
   - Detect if extension or breaking change
   - If breaking change → prompt: "This looks like a breaking change. Create new PRD instead? (yes/no)"

3. **Update PRD file** (if extension approved)
   - Increment version (1.0 → 2.0)
   - Add new FRs/NFRs with next sequential IDs
   - Update architecture/design sections
   - Add to "Version History" section
   - Update "Last Updated" timestamp

4. **Generate incremental tasks**
   - Append new parent tasks to existing task file
   - Generate sub-tasks for new FRs/NFRs
   - Preserve all existing tasks (don't modify completed ones)
   - Update task numbering (if task 3.0 was last, new tasks start at 4.0)

5. **Update status tracking**
   - Update `prds/_index.md`:
     - Change status from "✅ Complete" → "🔄 In Progress"
     - Increment version number
     - Add version history entry
     - Recalculate completion % based on new tasks
   - Update `tasks/_index.md` if cross-PRD dependencies changed

**Example:**

**Before (PRD-0001 v1.0 - Complete):**
```markdown
## Metadata
- **PRD ID:** PRD-0001
- **Version:** 1.0
- **Status:** ✅ Complete
- **Last Updated:** 2025-01-10

## Functional Requirements
### PRD-0001-FR-1: Accept registration request
### PRD-0001-FR-2: Validate email/password
### PRD-0001-FR-3: Check duplicate email
### PRD-0001-FR-4: Create user record
### PRD-0001-FR-5: Return success response
```

**After Extension (PRD-0001 v2.0 - In Progress):**
```markdown
## Metadata
- **PRD ID:** PRD-0001
- **Version:** 2.0
- **Status:** 🔄 In Progress (60% - 3/5 new tasks complete)
- **Last Updated:** 2025-01-15

## Version History
### v2.0 (2025-01-15) - OAuth Authentication Extension
- Added FR-6: OAuth login flow
- Added FR-7: Social provider integration (Google, GitHub)
- Status: 🔄 In Progress (60%)

### v1.0 (2025-01-10) - Email/Password Registration
- Initial implementation
- Status: ✅ Complete (deployed to production)

## Functional Requirements
### PRD-0001-FR-1: Accept registration request ✅
### PRD-0001-FR-2: Validate email/password ✅
### PRD-0001-FR-3: Check duplicate email ✅
### PRD-0001-FR-4: Create user record ✅
### PRD-0001-FR-5: Return success response ✅
### PRD-0001-FR-6: OAuth login flow (NEW v2.0)
### PRD-0001-FR-7: Social provider integration (NEW v2.0)
```

**Task File Update:**
```markdown
### 1.0 [✅] Input Validation (v1.0)
### 2.0 [✅] Database Operations (v1.0)
### 3.0 [✅] API Endpoints (v1.0)

### 4.0 [ ] OAuth Integration (v2.0 - NEW)
  - [ ] 4.1 Write unit tests for OAuth flow (PRD-0001-FR-6)
  - [ ] 4.2 Write integration tests for OAuth providers (PRD-0001-FR-6)
  - [ ] 4.3 Implement OAuth callback handler
  - [ ] 4.4 Run tests and verify

### 5.0 [ ] Social Provider Setup (v2.0 - NEW)
  - [ ] 5.1 Configure Google OAuth (PRD-0001-FR-7)
  - [ ] 5.2 Configure GitHub OAuth (PRD-0001-FR-7)
  - [ ] 5.3 Add provider selection UI
```

**Status Index Update:**
```markdown
| PRD ID | Title | Version | Status | Completion | Tasks | Last Updated | Notes |
|--------|-------|---------|--------|------------|-------|--------------|-------|
| PRD-0001 | User Registration | 2.0 | 🔄 In Progress | 60% (3/5) | 5 | 2025-01-15 | v1.0 complete ✅, v2.0 OAuth in progress |
```

**Deliverable:**
- Updated PRD file with version 2.0
- Appended tasks in existing task file
- Updated `prds/_index.md` with new version and status
- Ready to execute new tasks with Phase 4

**Next Step:** Use Phase 4 to process the extended task list

### Phase 3: Generate Task List

**Workflow Phase:** Generate structured task list from PRD

**How to invoke:** "Generate tasks from `<PATH_TO_PRD_FILE>`" or "Use Phase 3 on prds/0001-prd-feature.md"

**Two-Phase Process:**

**Phase 3.1 - Parent Tasks:**
1. Analyze PRD and existing codebase
2. Extract FR/NFR IDs for traceability
3. Derive dependencies and generate topologically ordered parent tasks (typically 4-6 tasks)
4. Create `tasks/tasks-[prd-name].md` with parent tasks only
5. Present parent tasks to user with clear message:

   **"I've generated {N} parent tasks for this PRD. Please review them above to ensure they match your expectations."**

   **"These parent tasks will be broken down into detailed sub-tasks (including test sub-tasks based on CLAUDE.md requirements)."**

   **"Reply 'Go' when ready to proceed with sub-task generation, or ask for changes if needed."**

6. **STOP and WAIT** for user response (required: "Go", "go", or explicit approval)

**Why the wait?**
- Gives you a chance to review high-level task breakdown
- Allows corrections before detailed sub-tasks are generated
- Prevents rework if parent structure is misaligned with expectations

**Phase 3.2 - Sub-Tasks (Test-First with CLAUDE.md Authority):**
After user confirms "Go":

**STEP 1: Parse CLAUDE.md Testing Strategy**
- Identify which test types are explicitly REQUIRED
- Identify which test types are explicitly EXCLUDED
- For silent/unclear requirements, default to: unit + integration required

**STEP 2: Generate Test Sub-Tasks Based on CLAUDE.md**

For EACH parent task, break down into sub-tasks following pattern:

**If CLAUDE.md requires unit tests (or is silent):**
- [ ] Write unit tests for FR-n (business logic, validation, utilities)
- [ ] Run unit tests and fix ALL failures (invest effort, do not skip easily)

**If CLAUDE.md requires integration tests (or is silent):**
- [ ] Write integration tests for FR-n (API contracts, DB operations, service integration)
- [ ] Run integration tests and fix ALL failures (invest effort, do not skip easily)

**If CLAUDE.md requires E2E tests AND FR involves frontend-backend (or is silent + frontend-backend):**
Auto-detect: login, registration, CRUD operations, chatbots, SSE, forms, etc.
- [ ] Write AUTOMATED E2E tests for FR-n (user flows, UI-to-API integration)
- [ ] Use stack-appropriate E2E framework (Playwright for JS/TS, Playwright/Selenium for Python, etc.)
- [ ] Minimize manual testing - automate browser interactions, form fills, assertions
- [ ] Run E2E tests and fix ALL failures (invest effort, do not skip easily)

**E2E Framework Suggestions by Stack:**
- React/Vue/Angular/Svelte/Next.js → **Playwright** (recommended) or Cypress
- Django/Flask → **Playwright for Python** or Selenium
- Rails → **Capybara** or Playwright
- Go web apps → **chromedp** or playwright-go
- Backend API only → E2E not applicable

**If CLAUDE.md explicitly excludes a test type:**
- [ ] DO NOT generate test sub-tasks for excluded type
- [ ] Add note: "X tests excluded per CLAUDE.md Testing Strategy"

**Implementation sub-task (always included):**
- [ ] Implement functionality for FR-n

**For database changes, add verification sub-tasks:**
- [ ] Generate migration files
- [ ] VERIFY: Execute migrations against database
- [ ] VERIFY: Inspect schema
- [ ] VERIFY: Test seed/population script
- [ ] VERIFY: Test rollback and re-apply
- [ ] Run integration tests against real database

**Only skip tests when:**
- CLAUDE.md explicitly excludes that test type
- Dependencies truly not available (mark with **Structured BLOCKED_BY_TASK notation** - see below)
- Infrastructure not ready (document in Deferred/Skipped Tests section with mitigation)
- NEVER skip due to difficulty - invest significant effort to make tests work

**Structured BLOCKED_BY_TASK Notation (REQUIRED):**

When blocking a test or sub-task, use this format:
```
BLOCKED_BY_TASK <task-id>: <root-cause> | Mitigation: <workaround> | ETA: <date> | Owner: <person> | Safe: <yes|no|partial>
```

**Examples:**

✅ Good (structured):
```javascript
test.skip('PRD-0007-FR-5 payment processing', () => {
  // BLOCKED_BY_TASK 4.2: Payment gateway API not deployed to staging
  // Mitigation: Using mock payment responses in local tests
  // ETA: 2025-01-20 | Owner: @jane | Safe: Yes with feature flag
});
```

✅ Good (structured, Python):
```python
@pytest.mark.skip(reason="BLOCKED_BY_TASK 3.1: User model migration pending | Mitigation: Using in-memory stub | ETA: Tomorrow | Owner: @bob | Safe: No - integration tests blocked")
def test_user_creation_prd_0012_fr_2():
    pass
```

❌ Bad (unstructured):
```javascript
test.skip('payment test', () => {
  // BLOCKED_BY_TASK 4.2
});
```

**Required Fields:**
- **task-id:** Blocking task ID (e.g., `4.2`, `0001-2.0`)
- **root-cause:** Why is this blocked? (dependency not ready, API unavailable, migration pending)
- **Mitigation:** What workaround exists? (mocks, feature flags, contract stubs)
- **ETA:** When will blocker be resolved? (date or "Unknown")
- **Owner:** Who owns unblocking this? (@username or team)
- **Safe:** Can downstream work proceed? (`Yes` with mitigation, `No` must wait, `Partial` limited functionality)

3. Include PRD FR/NFR tokens in test names
4. Update or create `tasks/_index.md` for global dependency tracking

**Contract-First Workflow for Blocked Dependencies:**

When a sub-task depends on an incomplete upstream task, use **contract-first development** to avoid rewrites:

**Step 1: Identify the Dependency Interface**
- API endpoint → OpenAPI/GraphQL schema
- Database → Schema definition (Prisma, SQL DDL, migrations)
- Service → Shared types/interfaces (TypeScript, protobuf, JSON schema)
- Message queue → Event schema (Avro, JSON schema)

**Step 2: Define or Import the Contract**
```bash
# Example: API dependency
mkdir -p contracts/
# Get contract from upstream team OR define expected interface
curl https://api-staging.example.com/openapi.yaml > contracts/auth-api-v1.yaml

# Example: Database dependency
# Reference existing schema or create expected schema
cp prisma/schema.prisma contracts/expected-user-model.prisma
```

**Step 3: Generate Code from Contract**
- **TypeScript:** Use OpenAPI Generator, Prisma client, GraphQL Codegen
- **Python:** Use datamodel-code-generator, OpenAPI Generator, Pydantic
- **Go:** Use oapi-codegen, protoc, sqlc

**Step 4: Implement Against Contract with Feature Flags**
```javascript
// Example: Feature flag for unstable dependency
import { authClient } from './generated/auth-api-client'; // from contract
import { mockAuthClient } from './mocks/auth-client'; // mock for testing

const useRealAuth = process.env.ENABLE_REAL_AUTH === 'true'; // feature flag

export const auth = useRealAuth ? authClient : mockAuthClient;

test('PRD-0007-FR-3 user login', async () => {
  // Test works with both real and mock auth
  const result = await auth.login({ email, password });
  expect(result.token).toBeDefined();
});
```

**Step 5: Add Contract Sync Check**
```bash
# scripts/check_contract_sync.sh
#!/bin/bash
# Compares local contract with upstream to detect breaking changes

LOCAL_CONTRACT="contracts/auth-api-v1.yaml"
REMOTE_CONTRACT="https://api-staging.example.com/openapi.yaml"

diff <(curl -s $REMOTE_CONTRACT) $LOCAL_CONTRACT
if [ $? -ne 0 ]; then
  echo "⚠️ Contract mismatch detected! Upstream API changed."
  echo "Update $LOCAL_CONTRACT and regenerate client code."
  exit 1
fi
```

**Step 6: Switch to Real Implementation**
Once upstream task completes with Readiness Proof:
```javascript
// 1. Update contract file if needed
// 2. Regenerate client code: npm run generate:api-client
// 3. Enable feature flag: ENABLE_REAL_AUTH=true
// 4. Run integration tests: npm test -- --integration
// 5. Remove mock once tests pass
```

**Contract-First Checklist:**
- [ ] Dependency interface documented (API contract, schema, types)
- [ ] Contract file stored in `contracts/` or linked from upstream
- [ ] Generated client/types from contract (not hand-written stubs)
- [ ] Feature flag controls which implementation is used
- [ ] Tests work with both mock and real implementation
- [ ] Contract sync check runs in CI
- [ ] Plan to remove mock once dependency is stable

**Benefits:**
- ✅ Parallel development - no waiting for upstream
- ✅ No rewrites - contract defines expectations upfront
- ✅ Safe rollout - feature flag enables gradual migration
- ✅ Early detection - contract sync checks catch breaking changes

5. Update or create `tasks/_index.md` for global dependency tracking

**Deliverables:**
- Relevant Files section with FR/NFR mappings
- Test Plan Summary
- Deferred/Skipped Tests section
- Blocked/Prerequisites Table
- Task Dependencies section
- Tasks with parent and sub-task hierarchy

**Next Step:** Use Phase 4 to execute tasks

### Phase 4: Execute Task List

**Workflow Phase:** Process task list systematically

**How to invoke:** "Process task list `<PATH_TO_TASK_LIST_FILE>`" or "Use Phase 4 on tasks/tasks-0001.md"

**Sub-Task Level Protocol:**
1. **Check prerequisites - verify parent not blocked:**
   - If sub-task depends on another task, verify it has **Readiness Proof**
   - Check `tasks/_index.md` for dependency status (must be `ready`, not `blocking` or `at-risk`)
   - **Validate readiness artifacts exist:**
     - API contract files exist and are up-to-date
     - Tests pass for the dependency
     - Service/endpoint is deployed and reachable
   - **If readiness proof missing:** Mark current task as `BLOCKED_BY_TASK x.y` with details
   - **If readiness proof stale/incomplete:** Ask for clarification before proceeding
2. **Verify CLAUDE.md test requirements** - confirm which test types apply
3. Work on ONE sub-task at a time
4. **Test-first approach (for REQUIRED test types per CLAUDE.md):**
   - Write unit tests first (if required)
   - Write integration tests second (if required)
   - For frontend-backend features: write E2E tests third (if required)
   - Then implement functionality
5. Run targeted tests for current FR(s)
6. **"Make Effort" enforcement - fix ALL failures with diligence:**
   - Spend significant time solving test setup issues
   - Research test infrastructure requirements
   - Ask for clarification if requirements are ambiguous or issues arise
   - If failures depend on future tasks: Add BLOCKED_BY_TASK x.y notation
   - If infrastructure missing: Document in Deferred/Skipped Tests with resolution plan
   - **NEVER skip because "tests are hard to write" - this is anti-pattern**
7. **Before marking sub-task complete [x]:**
   - ALL required tests written for this FR (per CLAUDE.md requirements)
   - Tests either PASSING or explicitly marked BLOCKED_BY_TASK with valid reason
   - No unexplained skips or commented-out tests
   - Test setup challenges resolved (not bypassed)
8. Mark sub-task complete [x] only after validation
9. Include PRD FR/NFR tokens in code and commits
10. **Proceed automatically to next sub-task** unless:
    - Clarification needed on requirements
    - Blocker encountered that requires user decision
    - Quality gates failed and manual intervention needed

**ANTI-PATTERNS TO AVOID:**
❌ "CLAUDE.md says E2E required but tests are too hard, skipping"
❌ Commenting out failing tests without BLOCKED_BY_TASK
❌ Only writing unit tests when CLAUDE.md requires integration tests
❌ Giving up on test setup after first attempt
❌ Marking sub-task complete with failing tests
❌ Ignoring CLAUDE.md explicit exclusions and generating tests anyway

**CORRECT PATTERNS:**
✅ Reading CLAUDE.md Testing Strategy before generating tests
✅ Respecting explicit exclusions ("No E2E" → don't generate E2E)
✅ Investing significant effort to solve test infrastructure issues
✅ Writing all required test types per CLAUDE.md
✅ Properly documenting blocked tests with task references
✅ Researching and implementing test setup (containers, mocks, fixtures)

**Parent Task Completion Protocol:**
When all sub-tasks under a parent are `[x]`:
1. Run full test suite
2. Apply Quality Gates (lint, type-check, security, coverage)
3. **Database Migration Verification (IF applicable - see detection guide below):**
   - Execute migrations against real database
   - Verify schema matches expectations
   - Test data population/seed script
   - Test rollback and re-apply
   - Run integration tests against real DB (not mocked)
4. **Generate Readiness Proof (IF this task is a dependency for others):**
   - **API Contracts:** Link to OpenAPI/GraphQL schema, protobuf definitions, shared types
   - **Test Evidence:** Link to passing test suite results, test report URL, coverage report
   - **Schema/Model Artifacts:** Link to schema.sql, Prisma schema, DB migration version
   - **Deployment Status:** Service deployed to test/staging environment with health check URL
   - **Example:** `## Readiness Proof: API v1.2.0 contract (openapi.yaml#L45), Tests passing (CI run #123), Deployed to staging (https://api-staging.example.com/health)`
5. ONLY if all gates pass: Stage changes
6. Clean up temporary files/code
7. Commit with conventional format including PRD tokens
8. Mark parent task complete `[x]`
9. **Update `tasks/_index.md` with:**
   - Task status: `ready` (with readiness proof link)
   - Unblock downstream tasks that were waiting on this
   - Update dependency health indicators

**Database Change Detection Guide:**

**When Database Verification Applies:**
✅ PRD includes FRs that modify database schema:
- "Add new table/collection for X"
- "Add column/field to existing entity"
- "Change data type or constraints"
- "Add/modify indexes"
- "Create relationships/foreign keys"

**When Database Verification Does NOT Apply:**
❌ Pure CRUD operations using existing schema
❌ Business logic changes with no schema impact
❌ Frontend-only changes
❌ Configuration or documentation updates

**Database Environment Setup:**

**If migration system exists in CLAUDE.md:**
- Use documented migration tool (Alembic, Flyway, Prisma, Rails migrations, etc.)
- Follow existing migration patterns in codebase

**If NO migration system exists:**
- **Detect database type from CLAUDE.md or dependencies:**
  - PostgreSQL/MySQL → Use Alembic (Python), Flyway (Java), Prisma (Node), Sequelize (Node)
  - MongoDB → Use migrate-mongo, migrations package, or manual scripts
  - SQLite → Raw SQL scripts or framework ORM
- **Create migration infrastructure:**
  - Set up migration tool for the stack
  - Create migration directory structure (migrations/, db/migrate/, prisma/migrations/)
  - Add migration commands to CLAUDE.md
- **Track current database state (CRITICAL for dev/test):**

  **Option 1: Schema Definition File (Recommended)**
  - SQL databases: Maintain `schema.sql` or `schema.prisma` with current state
  - NoSQL: Maintain model definitions or JSON schema
  - Update file with each new migration
  - Use for initializing fresh test databases

  **Option 2: Migration Tracking Table/Collection**
  - Create `schema_migrations` table/collection
  - Record: migration name, applied timestamp, current version
  - Auto-update on each migration run
  - Query to determine current state

  **Option 3: Declarative Models (ORM-based)**
  - Define models in code (SQLAlchemy, Prisma, Mongoose, etc.)
  - Use ORM auto-sync for development
  - Generate migrations from model changes
  - Models serve as source of truth

  **Database State Management Workflow:**
  ```
  1. Developer adds new feature requiring schema change
  2. Update model/schema definition
  3. Generate migration: `npm run migration:generate` or `alembic revision --autogenerate`
  4. Review generated migration
  5. Apply to dev database: `npm run migrate` or `alembic upgrade head`
  6. Commit migration file + updated schema
  7. CI/Test runs migrations against clean test DB
  8. Current state = all migrations applied + schema file matches
  ```

  **For Test/Development Databases:**
  - **Fresh setup:** Apply all migrations in order OR load schema.sql
  - **Incremental:** Apply only new migrations since last run
  - **Seed data:** Maintain seed script for test fixtures (users, products, etc.)
  - **Tear down:** Drop database or use Testcontainers (auto-cleanup)

**Test Database Setup Options (choose based on stack):**
1. **Testcontainers** (recommended - Docker-based isolation)
   - Spins up real database in container for tests
   - Automatically tears down after tests
   - Works for: PostgreSQL, MySQL, MongoDB, Redis, etc.

2. **docker-compose** (manual but flexible)
   - Define test database service
   - Start before tests: `docker-compose up -d test-db`
   - Run migrations: `npm run migrate` or equivalent
   - Stop after tests: `docker-compose down`

3. **In-memory database** (fast but limited)
   - SQLite for SQL databases
   - MongoDB Memory Server for MongoDB
   - Good for unit tests, limited for integration tests

**Add to CLAUDE.md when setting up:**
```markdown
## Data Stores
- Database: [PostgreSQL 15 | MongoDB 6 | etc.]
- Migration tool: [Alembic | Prisma | Flyway | Rails | Sequelize | etc.]
- Test environment: [Testcontainers | docker-compose test-db service]
- Quick start: `docker-compose up -d test-db && npm run migrate`
- Schema location: [migrations/ | prisma/schema.prisma | db/schema.rb]
```

**Critical Database Verification Mindset:**
```
OLD: Files exist = Work complete
NEW: Files exist + Executed + Verified = Work complete
```

### Phase 5: Audit Test Coverage & Correctness (Optional)

**Workflow Phase:** Audit test quality and completeness

**How to invoke:**
- "Audit tests for completed features" - Report only (default)
- "Audit tests and update task files" - Report + auto-append missing tests
- "Audit unit tests in src/auth" - Scoped audit
- "Audit all tests with test execution" - Comprehensive with test runs

**Purpose:** Dual-purpose audit that verifies BOTH test coverage AND test correctness against specifications.

**Two-Phase Workflow:**

**Phase 5.1 - Generate Audit Report (Always - Read-Only)**
1. Analyze codebase for test coverage against PRD requirements
2. Identify missing tests (coverage gaps)
3. Identify incorrect tests (wrong assertions, missing FR/NFR IDs)
4. Generate `TEST_AUDIT.md` report with findings
5. Present report to user for review

**Phase 5.2 - Auto-Append Missing Tests (Optional - Write)**
After report is generated, prompt user:

```
Found 3 missing tests for PRD-0001:
- Unit test for special char validation (PRD-0001-FR-3)
- Integration test for POST /signup (PRD-0001-FR-3)
- Performance test for /signup (PRD-0001-NFR-1)

Should I add these as sub-tasks to your task file?
A) Yes - Add all missing tests to tasks/tasks-0001-prd-auth.md
B) Custom - Let me choose which tests to add
C) No - Just show me the report (I'll add manually)
```

**If approved (Option A or B):**
1. Determine which parent task should contain each missing test
2. Append new sub-tasks to relevant parent tasks
3. Mark additions with `**Added by Test Audit (YYYY-MM-DD):**` annotation
4. Update task file checkboxes (unchecked for new tests)
5. Preserve all existing task structure and numbering

**Example Auto-Append Output:**

```markdown
### 1.0 [✅] User Registration Implementation
  - [✅] 1.1 Write unit tests for email validation
  - [✅] 1.2 Write integration tests for POST /signup
  - [✅] 1.3 Implement signup logic
  - [✅] 1.4 Run tests and verify passing

  **Added by Test Audit (2025-01-15):**
  - [ ] 1.5 Add missing unit test for special char validation (PRD-0001-FR-3)
  - [ ] 1.6 Fix incorrect email assertion in validation.test.js:42 (PRD-0001-FR-2)

### 2.0 [✅] Performance Optimization
  - [✅] 2.1 Database query optimization

  **Added by Test Audit (2025-01-15):**
  - [ ] 2.2 Add performance test for /signup endpoint (PRD-0001-NFR-1)
```

**Invocation Examples:**
- `@test-audit` - Report only, prompts for test type and scope
- `@test-audit unit` - Audits all unit tests, report only
- `@test-audit unit src/features/auth` - Scoped to auth folder
- `@test-audit all completed-only with-run` - Audit + execute tests for completed FRs
- `@test-audit with-update` - Report + auto-append prompt

**Key Features:**
1. **Coverage Analysis:** Identifies missing tests for specifications
2. **Correctness Analysis:** Verifies test assertions match spec requirements
3. **Traceability Verification:** Maps tests to PRD FR/NFR IDs
4. **Skip Hygiene Check:** Validates `BLOCKED_BY_TASK` notation
5. **Quality Gates Review:** Checks lint, type, format, security, coverage
6. **Test Execution:** Optional targeted or full test runs
7. **Auto-Append Missing Tests:** Optional task file updates with user approval

**Scope Options:**
- `completed-only` (default) - Audit only FRs/NFRs linked to completed tasks `[x]`
- `all-tasks` - Audit all FRs/NFRs in PRD (completed + pending)

**Run Modes:**
- Default: No execution, audit only
- `with-run` - Execute targeted tests for implemented FRs/NFRs
- `full-run` - Execute full test suite

**Update Modes:**
- Default: Report only, no task file changes
- `with-update` - Prompt to auto-append missing tests to task files

**Deliverable:** `TEST_AUDIT.md` report with:
- Coverage gaps (missing tests) with suggested locations
- Correctness issues (wrong assertions) with fix recommendations
- FR/NFR traceability matrix
- Deferred/skipped tests review
- Quality gates summary
- Recommendations (immediate, short-term, long-term)
- **Optional:** Updated task files with missing test sub-tasks appended

**When to Use:**
- After completing parent tasks (check for gaps in current work)
- Before marking PRD implementation complete (comprehensive validation)
- When verifying test suite quality (correctness audit)
- During code review process (traceability verification)
- To validate traceability compliance (FR/NFR mapping)

**Next Steps:**
- **Report-only mode:** Review `TEST_AUDIT.md`, manually add missing tests to task files
- **Auto-append mode:** Review appended sub-tasks, execute them using Phase 4 protocol

### Phase 6: Generate Status Report

**Workflow Phase:** Generate comprehensive PRD status report

**How to invoke:**
- "Generate status report" - Full report (all PRDs)
- "Show PRD status" - Full report
- "Status report for in-progress PRDs" - Filtered view
- "Status report for PRD-0001" - Single PRD detail

**Purpose:** Provides at-a-glance visibility into all PRD completion states, progress tracking, and project health.

**Process:**

1. **Read `prds/_index.md`**
   - Parse all PRD entries
   - Extract status, completion %, version history
   - Calculate summary statistics

2. **Generate report sections:**
   - Executive summary (total PRDs, completion stats, velocity)
   - In-progress PRDs (sorted by % completion, with ETA)
   - Recently completed PRDs (last 30 days)
   - Draft PRDs (not started)
   - Blocked PRDs (with blocker details)
   - Superseded PRDs (archived)
   - Dependency chain visualization
   - Quality metrics (test coverage, quality gates)
   - Recommendations (immediate, short-term, long-term)

3. **Apply filters (if specified):**
   - `in-progress` - Show only 🔄 In Progress PRDs
   - `blocked` - Show only 🚫 Blocked PRDs
   - `PRD-0001` - Show detailed status for single PRD
   - `summary` - Executive summary only

4. **Write `STATUS_REPORT.md`**

**Report Sections:**

**1. Executive Summary**
```markdown
## Executive Summary

**Project Health:** On Track | At Risk | Blocked

### Overall Progress
- **Total PRDs:** 5
- **✅ Complete:** 3 (60%)
- **🔄 In Progress:** 1 (20%)
- **📋 Draft:** 1 (20%)
- **🚫 Blocked:** 0 (0%)

### Velocity
- **Completed this week:** 2 PRDs
- **Average time to complete:** 5 days
```

**2. In Progress PRDs** (Most important section)
```markdown
## 🔄 In Progress PRDs

### PRD-0001: User Registration (v2.0)
- **Status:** 🔄 In Progress
- **Completion:** 60% (3/5 tasks complete)
- **Started:** 2025-01-15
- **Est. Completion:** 2025-01-18 (based on current velocity)

**Current Work:**
- [✅] 1.0 Input Validation
- [✅] 2.0 Database Operations
- [✅] 3.0 API Endpoints
- [ ] 4.0 OAuth Integration (IN PROGRESS)
- [ ] 5.0 Security Hardening

**Version History:**
- v2.0 (current): OAuth authentication extension
- v1.0 (complete): Email/password registration

**Next Steps:**
1. Complete OAuth integration (task 4.0)
2. Run security hardening (task 5.0)
3. Run test audit to validate coverage
4. Deploy to staging
```

**3. Recently Completed PRDs**
```markdown
## ✅ Recently Completed (Last 30 Days)

### PRD-0002: Payment Processing (v1.0)
- **Completed:** 2025-01-10
- **Duration:** 7 days
- **Test Coverage:** 95%
```

**4. Dependency Chain**
```markdown
## Dependency Chain

PRD-0001 (In Progress) 🔄
  └─> PRD-0005 (Blocked - waiting on 0001)

PRD-0002 (Complete) ✅
PRD-0003 (Complete) ✅
PRD-0004 (Draft) 📋
```

**Command Variations:**

**Full Report:**
```
"Generate status report"
```
Generates complete STATUS_REPORT.md with all sections.

**In-Progress Only:**
```
"Status report for in-progress PRDs"
```
Shows only 🔄 In Progress section (useful for daily standup).

**Single PRD Detail:**
```
"Status report for PRD-0001"
```
Detailed breakdown of single PRD with all tasks, version history, metrics.

**Summary Only:**
```
"Status report summary"
```
Executive summary section only (quick health check).

**Deliverable:** `STATUS_REPORT.md` with requested scope

**When to Use:**
- Daily standups (in-progress view)
- Weekly planning (full report)
- Stakeholder updates (summary + in-progress)
- Before sprint planning (identify blocked PRDs)
- After completing PRDs (velocity tracking)

**Integration with Status Index:**

Status report reads from `prds/_index.md` (auto-maintained by workflow):
- Phase 2 (@create-prd) → Adds entry
- Phase 2b (@extend-prd) → Updates version
- Phase 3 (@generate-tasks) → Sets in-progress
- Phase 4 (@process-task-list) → Updates completion %
- Phase 5 (@test-audit) → Validates completion
- Phase 6 (@status-report) → Reads and formats

**Next Step:** Use insights from report to prioritize work, unblock dependencies, or generate new PRDs

## Traceability Requirements

Throughout workflow, use PRD-scoped IDs:
- Functional Requirements: `PRD-####-FR-n`
- Non-Functional Requirements: `PRD-####-NFR-n`
- Include in test names, commit messages, and traceability matrix
- Enforce in CI: fail/warn when missing tokens

## Global Dependency Management

**File:** `tasks/_index.md`

Consolidates cross-PRD dependencies and task readiness with **automated health tracking**.

**Structure:**

```markdown
# Global Task Dependency Index

Last Updated: [Timestamp]
Auto-generated by: @generate-tasks, @process-task-list

## Dependency Health Summary
- ✅ Ready: X tasks (0 blockers)
- ⚠️ At-Risk: Y tasks (dependency health degraded)
- 🚫 Blocked: Z tasks (waiting on prerequisites)

## Cross-PRD Dependencies

| Task ID | PRD | Description | Status | Depends On | Readiness Proof | Health | Updated |
|---------|-----|-------------|--------|------------|----------------|--------|---------|
| 0001-1.0 | 0001 | User Auth API | ✅ ready | - | [API contract](./contracts/auth-v1.yaml), [Tests](CI#123) | 🟢 healthy | 2025-01-15 |
| 0002-2.0 | 0002 | Profile Service | 🚫 blocked | 0001-1.0 | - | 🔴 waiting | 2025-01-14 |
| 0003-1.0 | 0003 | Notification API | ⚠️ at-risk | 0001-1.0 | - | 🟡 contract changed | 2025-01-15 |

## Recommended Execution Order (Topological Sort)

**How to determine which task to work on first:**

1. **No dependencies** → Start immediately (these are "entry points")
2. **Has dependencies** → Wait until all prerequisite tasks are `ready` with readiness proof
3. **Critical path** → Longest chain of dependent tasks (prioritize to avoid delays)

**Example from table above:**

**Execution Order:**
1. ✅ **Start: 0001-1.0** (no dependencies)
2. ⏸️ **Wait: 0002-2.0** (blocked by 0001-1.0)
3. ⏸️ **Wait: 0003-1.0** (blocked by 0001-1.0)

**After 0001-1.0 completes:**
4. ✅ **Start: 0002-2.0** (dependency now ready)
5. ✅ **Start: 0003-1.0** (dependency now ready) — can work in parallel with 0002-2.0

**Critical Path:** 0001-1.0 → 0002-2.0 (longest chain = 2 tasks)

**Decision Guide:**
- If multiple tasks are ready (no blockers), prioritize:
  1. Tasks on the critical path (longest dependency chain)
  2. Tasks that unblock the most downstream work
  3. Tasks with earliest deadlines or highest business value

## Status Definitions
- **✅ ready:** All gates passed, readiness proof provided, consumers can proceed
- **⚠️ at-risk:** Completed but readiness proof stale/incomplete, or dependency changed
- **🚫 blocked:** Depends on tasks that are not ready

## Health Indicators
- **🟢 healthy:** Readiness proof valid, no changes since last check
- **🟡 contract changed:** API/schema/interface modified, consumers may need updates
- **🟠 tests failing:** Dependency tests currently failing, instability risk
- **🔴 waiting:** Prerequisite not ready, cannot proceed

## Blockers Detail

### Task 0002-2.0: Profile Service
- **Blocked by:** 0001-1.0 (User Auth API)
- **Root cause:** Auth API not deployed to staging
- **Mitigation:** Using mock auth in local tests
- **ETA:** 2025-01-16 (in 1 day)
- **Owner:** @jane
- **Safe to proceed:** ⚠️ Yes with feature flag `enable_real_auth=false`

### Task 0003-1.0: Notification API
- **Blocked by:** 0001-1.0 (User Auth API)
- **Root cause:** Auth contract changed (userId field renamed to userUuid)
- **Mitigation:** Update contract import to auth-v1.1.yaml
- **ETA:** Today
- **Owner:** @bob
- **Safe to proceed:** ✅ Yes, contract synced
```

**Update Triggers:**
- `@generate-tasks` creates/updates this file with initial dependencies
- `@process-task-list` updates status when tasks complete
- Manual: Run `npm run deps:check` or `python scripts/check_deps.py` for health validation

**Automation Scripts (recommended):**

Create `scripts/check_task_deps.sh` or `scripts/check_deps.py`:
```bash
#!/bin/bash
# Validates readiness proofs and updates health indicators
# - Checks if API contract files exist
# - Pings health check URLs
# - Verifies test reports are recent
# - Updates health column in tasks/_index.md
```

**CI Integration:**
```yaml
# .github/workflows/dep-check.yml
name: Dependency Health Check
on: [push, pull_request]
jobs:
  check-deps:
    runs-on: ubuntu-latest
    steps:
      - run: npm run deps:check || python scripts/check_deps.py
      - name: Comment PR if blockers found
        if: failure()
        run: gh pr comment --body "⚠️ Blocked tasks detected. See tasks/_index.md"
```

## Escalation Paths & Troubleshooting

### When You're Blocked: What to Do

The workflow enforces "make effort" principles, but sometimes you genuinely get stuck. Here's the escalation protocol:

#### **Scenario 1: Tests Keep Failing Despite Significant Effort**

**Escalation Protocol:**

1. **First 30 Minutes: Research & Debug**
   - Read test framework documentation
   - Search for similar issues (Stack Overflow, GitHub issues)
   - Try different approaches (mocks, fixtures, container config)
   - Document what you tried and the results

2. **After 30 Minutes: Ask for Clarification**
   - Stop and describe the issue:
     - "I'm implementing PRD-0007-FR-3 (payment validation)"
     - "Integration tests fail with: `Error: Database connection refused`"
     - "I've tried: docker-compose up, Testcontainers, in-memory SQLite"
     - "CLAUDE.md says integration tests required with Testcontainers"
   - Ask specific questions:
     - "Should I use a different database for tests?"
     - "Is there existing test infrastructure I'm missing?"
     - "Can I temporarily mock the database until infrastructure is ready?"

3. **Decision Point: Continue, Defer, or Adapt**
   - **Option A - Infrastructure Fix:** User provides setup instructions
   - **Option B - Temporary Workaround:** Use mock/stub with `BLOCKED_BY_TASK` notation
   - **Option C - Update CLAUDE.md:** Revise testing strategy if infrastructure genuinely unavailable

4. **Document Resolution**
   - Update task file with resolution
   - Add to "Deferred/Skipped Tests" if blocked
   - Update CLAUDE.md if strategy changed

**✅ Acceptable:**
```markdown
## Deferred/Skipped Tests
- `tests/integration/payment.int.test.ts` - BLOCKED_BY_TASK 4.2: Payment gateway API not deployed to test environment | Mitigation: Using mock payment service | ETA: 2025-01-20 | Owner: @infra-team | Safe: Yes with feature flag `use_real_payments=false`
```

**❌ Unacceptable:**
```markdown
# Skipped integration tests because Testcontainers is hard to set up
```

---

#### **Scenario 2: CLAUDE.md Testing Strategy is Unclear/Missing**

**Escalation Protocol:**

1. **Check for Template Text**
   - If CLAUDE.md has `[Tool name]` or `[Framework(s)]` placeholders → needs filling

2. **Prompt for Clarification**
   - "CLAUDE.md Testing Strategy section has template text. I can:"
     - "A) Apply defaults (unit + integration + E2E auto-detect)"
     - "B) Ask you to fill it out now"
     - "C) Customize testing strategy for this PRD"
   - "What would you prefer?"

3. **Update CLAUDE.md**
   - Once decided, update Testing Strategy section with explicit requirements
   - Mark as user-confirmed

---

#### **Scenario 3: Database Migration Tools Missing**

**Escalation Protocol:**

1. **Detect Missing Infrastructure**
   - PRD requires DB changes (new table, column, index)
   - CLAUDE.md doesn't specify migration tool
   - No existing migrations directory

2. **Propose Solution**
   - "This PRD requires database schema changes, but CLAUDE.md doesn't specify a migration tool."
   - "I've detected [PostgreSQL from dependencies]. Recommended tools:"
     - "Node.js: Prisma, Sequelize, Knex"
     - "Python: Alembic, Django migrations"
     - "Ruby: ActiveRecord migrations"
   - "Should I:"
     - "A) Set up [recommended tool] and add to CLAUDE.md"
     - "B) Create a separate parent task for migration infrastructure setup"
     - "C) Use raw SQL scripts for now"

3. **Create Infrastructure Task (if Option B)**
   - Add parent task 0.0: "Set up database migration infrastructure"
   - Block current tasks with `BLOCKED_BY_TASK 0.0`
   - Execute infrastructure task first

---

#### **Scenario 4: Requirements Are Ambiguous**

**Escalation Protocol:**

1. **Identify Ambiguity**
   - PRD-0007-FR-3 says: "Validate payment information"
   - Unclear: Which payment types? Card only? PayPal? Crypto?

2. **Ask Clarifying Questions**
   - "PRD-0007-FR-3 requires payment validation, but specifics are unclear:"
     - "Which payment methods should be supported?"
     - "What validation rules apply (Luhn algorithm, expiry date, CVV)?"
     - "Should validation be client-side, server-side, or both?"

3. **Update PRD with Answers**
   - Add specific validation rules to FR-3 Acceptance Criteria
   - Mark PRD as updated (increment version or add to Change Control)

---

#### **Scenario 5: Dependency Readiness Proof Missing**

**Escalation Protocol:**

1. **Check `tasks/_index.md`**
   - Task 2.0 depends on Task 1.0
   - Task 1.0 marked `ready` but no readiness proof link

2. **Prompt for Verification**
   - "Task 2.0 depends on Task 1.0 (Auth API), but readiness proof is missing."
   - "I need one of:"
     - "API contract file (e.g., `contracts/auth-v1.yaml`)"
     - "Test report URL showing passing tests"
     - "Deployment health check URL (e.g., `https://auth-staging.example.com/health`)"
   - "Can you provide proof, or should I mark Task 2.0 as `BLOCKED_BY_TASK 1.0` until available?"

3. **Decision**
   - **If proof provided:** Link in tasks/_index.md, proceed with Task 2.0
   - **If proof unavailable:** Use contract-first workflow (define expected interface, implement with mocks, add feature flag)

---

### Common Issues Quick Reference

| Issue | Likely Cause | Solution | See Section |
|-------|--------------|----------|-------------|
| Tests failing | Infrastructure/setup | Research → Ask → Document | Scenario 1 |
| CLAUDE.md unclear | Template not filled | Prompt for clarification → Update | Scenario 2 |
| No migration tool | First DB change | Propose tool → Add infrastructure task | Scenario 3 |
| Ambiguous PRD | Incomplete requirements | Ask questions → Update PRD | Scenario 4 |
| Blocked by dependency | Missing readiness proof | Request proof → Use contracts | Scenario 5 |
| Can't find files | Wrong directory/path | Check codebase structure → Ask | Troubleshooting Guide |

**For detailed troubleshooting, see:** `references/troubleshooting.md`

## Best Practices

### Definition of Ready (DoR) - Before Finalizing PRD
- Architecture and data ownership confirmed
- UX states available or explicitly deferred
- Security/tenancy strategy clarified
- Success metrics aligned to global SLOs
- ADRs drafted and linked (status: Proposed)

### Definition of Done (DoD) - Before Marking Parent Complete
- All sub-tasks completed `[x]`
- **Tests written and passing for ALL FRs (per CLAUDE.md Testing Strategy):**
  - Unit tests (if required by CLAUDE.md or silent)
  - Integration tests (if required by CLAUDE.md or silent)
  - E2E tests (if required by CLAUDE.md or auto-detected for frontend-backend features)
  - **Explicit exclusions in CLAUDE.md respected** (e.g., no E2E if CLAUDE.md says "None")
- Test setup challenges resolved (infrastructure, containers, mocks configured)
- Database verification complete (if applicable)
- Quality gates passed (lint, type-check, security, coverage per CLAUDE.md thresholds)
- No unexplained skipped tests (only BLOCKED_BY_TASK with valid reasons)
- Documentation updated
- Feature flags configured
- Operational readiness verified
- Test audit findings addressed (if audit run)

**DoD Validation Checklist:**
- [ ] Read CLAUDE.md Testing Strategy section
- [ ] Confirm all required test types have passing tests
- [ ] Verify excluded test types were not generated
- [ ] Validate test infrastructure is properly configured
- [ ] Check no tests skipped due to "too hard" reasoning

## Quick Reference

### Minimal Getting Started

**First, invoke the skill:**
```
skill: prd-driven-development
```

**Then use natural language for each phase:**

1. **Setup (one-time):** "Create CLAUDE.md from template" → Fill minimum sections
2. **Phase 1 (optional):** "Import PRDs from specs/all_features.md" → Creates draft PRDs
3. **Phase 2:** "Create a PRD from prd-bundle/0001-draft.md with standard complexity" → Finalizes PRD
4. **Phase 2b (optional):** "Extend PRD-0001 with OAuth authentication" → Updates existing PRD with new version
5. **Phase 3:** "Generate tasks from prds/0001-prd-feature.md" → Creates task list (wait for "Go" prompt)
6. **Phase 4:** "Process task list tasks/tasks-0001-prd-feature.md" → Executes implementation
7. **Phase 5 (optional):** "Audit tests for completed features" → Verifies quality
8. **Phase 6 (optional):** "Generate status report" → Shows all PRD completion states

### Targeted Test Runs
- Pytest: `pytest path/to/test.py -k PRD_0007_FR_3`
- Jest: `npx jest path/to/test.ts -t "PRD-0007-FR-3"`
- Go: `go test ./... -run PRD_0007_FR_3`

See `references/commands-guide.md` for complete command documentation, all test frameworks, quality gates, and batch execution modes.
