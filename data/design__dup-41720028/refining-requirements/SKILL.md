---
name: refining-requirements
description: Use when PRD is prose-heavy, ambiguous, has scattered file paths, missing API contracts, or says "similar to X" without explanation. Transforms rough requirements into implementation-ready specs. Auto-detects tech stack, validates file paths (EXISTS/CREATE/VERIFY markers), handles greenfield and multi-stack projects. Do NOT use for simple bug fixes, typos, or already-structured Jira tickets with clear file paths and acceptance criteria.
---

# Requirements Refiner

Transform rough requirements into implementation-ready specifications optimized for Claude Code execution.

## When to Use

- Received a PRD/spec that's prose-heavy and ambiguous
- Requirements scatter file paths throughout text
- Specs say "similar to X" without explaining X
- Missing API contracts, data models, or clear scope
- Before starting implementation on complex features
- **Starting a new project from scratch (greenfield)**
- Need to identify missing information before coding
- Architectural refactoring (e.g., session-based to JWT)
- Multi-service features spanning frontend/backend/database

## When NOT to Use

**Skip refinement for:**
- Simple bug fixes with clear location (e.g., "fix typo in file X line Y")
- Well-structured Jira tickets that already have:
  - Explicit file paths to modify
  - Clear acceptance criteria
  - Defined scope and deliverables
- Single-line changes or trivial updates
- Tasks where implementation path is obvious

**Decision rule:** If the task has specific file paths, clear acceptance criteria, and no ambiguity about what to build → execute directly, don't refine.

## Workflow

### Phase 0: Auto-Detect Project Context

**Step 1: Detect tech stack automatically**

```bash
# Run these checks to auto-detect stack
ls package.json 2>/dev/null && echo "DETECTED: Node.js"
ls go.mod 2>/dev/null && echo "DETECTED: Go"
ls requirements.txt pyproject.toml 2>/dev/null && echo "DETECTED: Python"
ls pom.xml build.gradle 2>/dev/null && echo "DETECTED: Java"
ls Gemfile 2>/dev/null && echo "DETECTED: Ruby"
ls composer.json 2>/dev/null && echo "DETECTED: PHP"
ls Cargo.toml 2>/dev/null && echo "DETECTED: Rust"
```

**Step 2: Read project conventions from CLAUDE.md**

```bash
# Check for project conventions
cat CLAUDE.md 2>/dev/null || cat .claude/CLAUDE.md 2>/dev/null || echo "No CLAUDE.md found"
```

Extract and apply:
- Code style preferences
- Naming conventions
- Architecture patterns
- Testing requirements
- Documentation standards

**Step 3: Detect project type**

| Type | Indicators | Template |
|------|------------|----------|
| Greenfield | "new project", "build from scratch", "new microservice", "from scratch", no existing code to reference | Use `references/greenfield-patterns.md` |
| Feature | References existing code, adds to current system | Use standard templates |
| Multi-stack | Monorepo with multiple languages, feature spans services | Create separate sections per stack |

**Greenfield indicators** (any of these = greenfield):
- "Build new service/microservice"
- "From scratch" or "brand new"
- "No existing code"
- "Deploy to Kubernetes" (new service)
- No file paths to validate (all CREATE, no EXISTS)

**Multi-stack indicators** (any of these = multi-stack):
- Monorepo structure mentioned (packages/, services/)
- Multiple languages listed (React + Go + Python)
- Cross-service feature (frontend + backend + database)
- Shared types/contracts between services

### Phase 1: Check for Missing Information

Scan PRD for completeness. See `references/edge-cases.md` for checklist.

If critical info is missing, note the gaps for the interview phase.

### Phase 1.5: Interactive Deep-Dive Interview

**This is the core differentiator.** Don't just identify gaps - actively probe for them.

#### Step 1: Offer Skip Option

If PRD appears comprehensive (all sections present, clear scope, explicit file paths):

```
"Your requirements look comprehensive. Would you like to:
1. Proceed directly to spec generation
2. Quick sanity-check interview (5-10 questions)
3. Deep-dive interview (thorough exploration)"
```

If user chooses to proceed, skip to Phase 2.

#### Step 2: Conduct Interview

Use `AskUserQuestion` tool to probe deeply. Ask 1-4 questions per round.

**Question Selection Priority:**
1. Blocking unknowns (can't proceed without answer)
2. High-impact architectural decisions
3. Failure modes and edge cases
4. UX details and user segments
5. Operational concerns

**Question Categories** (see `references/interview-patterns.md` for full templates):

| Category | Focus Areas |
|----------|-------------|
| Technical Edge Cases | Failure/recovery, concurrency, scaling, data integrity |
| User Experience | Loading states, error presentation, multi-platform, accessibility |
| Data & Security | PII handling, compliance, access control, audit trails |
| Business Logic | Rule conflicts, state transitions, edge cases, dependencies |
| Operations | Deployment strategy, monitoring, support tools |
| Tradeoffs | Scope prioritization, quality attributes, build vs buy |

**Question Quality Rules:**
- Ask about WHAT HAPPENS WHEN, not WHAT IS
- Scenario-based > abstract
- Specific > general
- Probe edge cases, not happy paths
- Never ask obvious questions (database choice, endpoint names)

**Example Good Questions:**
```
"If the user closes the browser mid-transaction, what state should they see when they return?"

"When [Service A] and [Service B] both try to update the same record, which wins?"

"If this feature gets 100x expected traffic tomorrow, what breaks first?"

"What's the experience for a user on 3G mobile with 500ms latency?"
```

**Example Bad Questions (NEVER ask these):**
```
"What database will you use?" (obvious/they'll tell you)
"What should the API return?" (too low-level)
"Is security important?" (obviously yes)
"Should it be fast?" (obviously yes)
```

#### Step 3: Iterate Until Complete

```
WHILE interview_active:
    1. Review current knowledge and gaps
    2. Select 1-4 highest-priority questions
    3. Ask using AskUserQuestion with smart options
    4. Record answers
    5. Update mental model with new information
    6. Check exit conditions
```

**Always include an exit option in each question set:**
- "That's enough, proceed with spec" as an option
- Or ask explicitly: "Continue probing or ready to generate spec?"

#### Step 4: Exit Conditions

Stop interviewing when ANY of these are true:
- User explicitly says "proceed" or "that's enough"
- All critical gaps are filled (no blocking unknowns)
- Questions become repetitive or hypothetical
- Answers converge to "standard approach" or "same as before"

**Anti-rationalization:** If you're unsure whether to continue, ask one more round. Better to over-interview than under-interview.

#### Step 5: Summarize Findings

Before proceeding, briefly summarize key decisions from interview:

```markdown
## Interview Summary

**Key Decisions:**
- Error handling: Show all errors at once, inline validation
- Scaling: Must handle 10k concurrent users by month 3
- Rollback: Feature flag with kill switch required
- Mobile: Responsive, not separate app

**Discovered Requirements:**
- Need audit trail for compliance
- Session timeout: 30 minutes idle
- Rate limit: 100 requests/minute per user
```

### Phase 2: Extract and Classify

Pull out: scope, file mappings, data models, API contracts, business logic, UI copy

**Incorporate interview findings:**
- Add discovered requirements from interview
- Update scope based on tradeoff decisions
- Include edge cases and failure modes discussed
- Add compliance/security requirements surfaced
- Note any constraints or limitations mentioned

### Phase 3: Validate File Paths Against Codebase

**Actually verify paths exist:**

```bash
# For each file path mentioned in PRD, check if it exists
find . -path "*/node_modules" -prune -o -name "filename.js" -type f -print
```

**Read similar files to understand patterns:**

```bash
# If PRD says "similar to existing controller", read it
cat app/controllers/v2/integrations/pos/pin/create.js 2>/dev/null | head -50
```

Mark paths as:
- `✓ EXISTS` — file found, will modify
- `✗ CREATE` — file doesn't exist, will create
- `? VERIFY` — path mentioned but needs confirmation

Include validation summary in output:
```markdown
## File Path Validation
| Path | Status | Action |
|------|--------|--------|
| app/models/egift.js | ✓ EXISTS | Modify — add field |
| app/controllers/v2/msite/verify.js | ✗ CREATE | New endpoint |
```

### Phase 4: Structure

Apply template from `references/templates.md`

Adapt to detected tech stack using `references/stack-patterns.md`:
- File extensions and paths
- Migration format
- Naming conventions
- Test patterns

**For multi-stack projects:**
Create SEPARATE file mapping sections per stack:
```markdown
## File Mappings

### Frontend (React/TypeScript)
| Path | Status | Action |
|------|--------|--------|
| packages/web/src/components/Feature.tsx | ✗ CREATE | New component |

### Backend API (Go)
| Path | Status | Action |
|------|--------|--------|
| services/api/internal/handlers/feature.go | ✗ CREATE | New handler |

### Shared Types (TypeScript)
| Path | Status | Action |
|------|--------|--------|
| packages/shared/types/feature.ts | ✗ CREATE | Shared interfaces |
```

Include cross-service API contracts showing how services communicate.

### Phase 5: Generate Test Scenarios

Derive tests from business logic. See `references/test-patterns.md`

### Phase 6: Security & UI Copy

**Security**: Auto-generate checklist based on detected patterns. See `references/security-checklist.md`

**UI Copy**: Extract all user-facing text into bilingual table (ID/EN). See `references/ui-copy-patterns.md`

### Phase 7: Verify Completeness

**STOP before saving. Verify content and determine output format:**

#### 7a. Determine Output Format (Threshold-Based)

**Estimate your total output line count using this heuristic:**

| Feature Complexity | Typical Output | Format |
|--------------------|----------------|--------|
| Simple (1-2 files, no API, no DB) | 50-100 lines | Single file |
| Medium (3-5 files, some API or DB) | 100-200 lines | Depends on triggers |
| Complex (6+ files, API + DB + external) | 200-400+ lines | Multi-file |

**Threshold:** < 150 lines = single file, ≥ 150 lines = multi-file

**Always use multi-file for (regardless of line count):**
- Greenfield projects (creating a new service/package from scratch)
- Multi-stack features (different language ecosystems, e.g., React + Go)
- Features with 3+ API endpoints
- Features with external API integrations (webhooks, third-party services)
- Features with ANY TWO of: database migrations, API changes, UI copy

**Single file is fine for:**
- Simple bug fixes with clear scope
- Small features affecting 1-2 files
- Quick refinements that fit on one screen
- Client-side only changes (no backend)

**Anti-rationalization rule:** If you're trying to "fit" content into single-file, use multi-file instead. When uncertain, multi-file is always acceptable.

#### 7b. Verify Section Content

| Section | Required? | Check |
|---------|-----------|-------|
| Scope (in/out) | Always | [ ] |
| File Mappings with markers | Always | [ ] |
| Data Model | If DB changes | [ ] |
| API Contracts | If endpoints | [ ] |
| Business Logic | Always | [ ] |
| Test Scenarios | Always | [ ] |
| Security Checklist | Always | [ ] |
| UI Copy | If user-facing | [ ] |
| Execution Checklist | Always | [ ] |

**For greenfield:** Verify ALL file paths are marked CREATE (no EXISTS).

**For multi-stack:** Verify separate sections exist for each stack.

**If any required section is missing:** Complete it before proceeding.

### Phase 8: Save Output

**Use the format determined in Phase 7a (threshold-based).**

---

#### Option A: Single File (< 150 lines or simple features)

```bash
mkdir -p agent-workflow/requirements
```

**Naming:** `agent-workflow/requirements/YYYYMMDD-feature-name.md`

**Examples:**
- `agent-workflow/requirements/20241127-add-email-field.md`
- `agent-workflow/requirements/20241127-fix-validation-bug.md`

**Use the single-file template** from Output Structure section below.

---

#### Option B: Multi-File Directory (≥ 150 lines or complex features)

```bash
mkdir -p agent-workflow/requirements/YYYYMMDD-feature-name
```

**Directory structure:**
```
agent-workflow/requirements/YYYYMMDD-feature-name/
├── README.md              # Overview + navigation (always)
├── scope.md               # In/Out scope (always)
├── file-mappings.md       # Files to create/modify (always)
├── api-contracts.md       # Endpoint definitions (if applicable)
├── data-model.md          # Database changes (if applicable)
├── business-logic.md      # Rules and flows (always)
├── test-scenarios.md      # Test cases (always)
├── security.md            # Security checklist (always)
├── ui-copy.md             # Bilingual UI text (if applicable)
└── execution-checklist.md # Implementation steps (always)
```

**Examples:**
- `agent-workflow/requirements/20241127-whatsapp-verification/`
- `agent-workflow/requirements/20241127-new-verification-service/` (greenfield)

**Conditional file creation (multi-file only):**
- `api-contracts.md` — Only create if feature has API endpoints
- `data-model.md` — Only create if feature has database changes
- `ui-copy.md` — Only create if feature has user-facing text

---

**Frontmatter (both formats):**
```markdown
---
title: [Feature Name]
created: [ISO timestamp]
status: draft | review | approved
stack: [detected stack]
type: feature | greenfield
original_prd: [filename if provided]
---
```

### Phase 9: Offer Scaffolding (Optional)

After saving refined PRD, ask:

> "Would you like me to scaffold the boilerplate files for this feature?"

If yes, create:
- Empty controller/handler files with correct structure
- Model files with field definitions
- Migration files with schema
- Test file skeletons
- Route registrations

**Scaffolding rules:**
- Read existing files to match code style
- Use project's linting/formatting conventions from CLAUDE.md
- Add TODO comments for implementation
- Don't overwrite existing files (create `.new` suffix if conflict)

## Output Structure

**For templates, see `references/templates.md`:**
- Single-File Output Template — for simple features (< 150 lines)
- Multi-File Output Templates — for complex features (≥ 150 lines)

**Multi-file directory structure:**
```
agent-workflow/requirements/YYYYMMDD-feature-name/
├── README.md              # Overview + navigation
├── scope.md               # In/Out scope
├── file-mappings.md       # Files to create/modify
├── api-contracts.md       # (if applicable)
├── data-model.md          # (if applicable)
├── business-logic.md      # Rules and flows
├── test-scenarios.md      # Test cases
├── security.md            # Security checklist
├── ui-copy.md             # (if applicable)
└── execution-checklist.md # Implementation steps
```

## Claude Code Commands

Quick reference for commands used by this skill:

```bash
# Auto-detect stack
ls package.json go.mod requirements.txt pyproject.toml pom.xml 2>/dev/null

# Read project conventions
cat CLAUDE.md 2>/dev/null

# Validate file exists
test -f "path/to/file.js" && echo "EXISTS" || echo "CREATE"

# Read existing pattern
cat path/to/similar/file.js | head -100

# Option A: Single file (< 150 lines)
mkdir -p agent-workflow/requirements
cat > agent-workflow/requirements/YYYYMMDD-feature-name.md << 'EOF'
[all sections in one file]
EOF

# Option B: Multi-file directory (≥ 150 lines or complex)
mkdir -p agent-workflow/requirements/YYYYMMDD-feature-name
cat > agent-workflow/requirements/YYYYMMDD-feature-name/README.md << 'EOF'
[overview content]
EOF
cat > agent-workflow/requirements/YYYYMMDD-feature-name/scope.md << 'EOF'
[scope content]
EOF
# ... repeat for each required file

# Scaffold files (with conflict check)
test -f "path/to/file.js" && cp "path/to/file.js" "path/to/file.js.new" || touch "path/to/file.js"
```

## Examples

See `references/transformation-patterns.md` for detailed before/after examples including:
- API integration features
- Data model changes
- Complex verification flows

## Anti-Patterns

1. **Narrative flow** — Use structured sections, not stories
2. **Embedded paths** — Consolidate all paths in File Mappings
3. **Implicit comparisons** — "Like existing flow" needs explanation
4. **Mixed concerns** — Separate UI copy from business logic
5. **Missing edge cases** — Explicitly list: what if X fails?
6. **Not reading existing code** — Always `cat` similar files first
7. **Not saving output** — Always save to `agent-workflow/requirements/`
8. **Over-refining structured specs** — Don't bloat already-clear Jira tickets
9. **Mixed stack patterns** — Don't use Node.js patterns for Go projects
10. **Missing completeness check** — Always verify all sections before saving
