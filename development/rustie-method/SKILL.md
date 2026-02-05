---
name: rustie-method
description: AI-assisted development workflow system for feature planning, session management, and quality assurance (v2.3). WORKTREE-CENTRIC - automatically scopes to current worktree's feature (worktree name = feature name). In feature worktrees, shows only relevant feature context. In main branch, shows dashboard of all worktrees. AUTO-ACTIVATES for session start (show priorities/NBA with Explore agent), feature work (load plan context with LSP symbol grounding), new features (spike mode with parallel sub-agents), context >70% (create handoff), UI changes (run Playwright tests), completed features (suggest archive), errors or failures (trigger RCA-PCA). Works with agent-docs/ folder structure. Modes are nba, work, spike, test, validate, sync, status, handoff, archive, rca-pca, tidyup. Use when working in codebases with agent-docs/ directory.
---

# Rustie Method Skill

AI-assisted development workflow for structured feature development, session management, and quality assurance.

## Quick Reference - All Modes

**CORE PRINCIPLE**: Worktree name = Feature name = Context scope

| Mode | Auto-Trigger | Manual Trigger | Feature Worktree | Main Branch |
|------|--------------|----------------|------------------|-------------|
| **nba** | Session start, "priorities" | "run nba mode" | THIS feature only | Dashboard: all worktrees |
| **work** | Git branch `feature/*` | "load feature X" | Auto-load (no prompt) | List & ask |
| **test** | UI files modified | "run tests" | THIS feature | Prompt for feature |
| **validate** | Before work mode | "validate feature" | THIS feature | Prompt for feature |
| **spike** | After validate (new features) | "test assumptions" | THIS feature | Prompt for feature |
| **sync** | Called by nba/work | "sync plans" | THIS worktree | "sync all" for all |
| **status** | "status", "where am I" | "show status" | THIS feature only | Overview all worktrees |
| **handoff** | Context >70%, "wrap up" | "create handoff" | Auto-detect feature | Read from context |
| **archive** | Feature 100% complete | "archive feature" | THIS feature | List completable |
| **rca-pca** | Errors, failures | "run rca" | Lesson in feature | Global lesson |
| **tidyup** | "organize", "cleanup" | "tidyup" | - | - |

---

## Worktree-Centric Workflow - CORE CONCEPT

Rustie operates on a fundamental principle: **worktree name = feature name = context scope**.

### The 1:1 Mapping

```
Worktree Folder    ←→    Feature Folder              ←→    Active Context File
─────────────────────────────────────────────────────────────────────────────────
./project-auth     ←→    agent-docs/features/auth/   ←→    features/auth/active-context.md
./project-payments ←→    agent-docs/features/payments/ ←→  features/payments/active-context.md
./project (main)   ←→    agent-docs/features/*/      ←→    (reads ALL feature contexts)
```

### Feature-Scoped Active Context (v2.1)

Each feature maintains its own `active-context.md` file inside its folder:

```
agent-docs/features/
├── auth/
│   ├── PRD.md
│   ├── plan.md
│   ├── active-context.md    ← Auth's session state
│   └── sessions/
└── payments/
    ├── PRD.md
    ├── plan.md
    ├── active-context.md    ← Payments' session state
    └── sessions/
```

**Why feature-scoped context?**
- Prevents sync conflicts between worktrees
- Each worktree reads its own feature's context
- Main branch can aggregate all contexts for dashboard view
- Context and sessions stay co-located

### Worktree Configuration (worktrees.md)

Each project should have an `agent-docs/worktrees.md` file to track port assignments and worktree-specific configuration. This enables running multiple dev servers simultaneously.

**Location**: `agent-docs/worktrees.md`

**Template**:
```markdown
# Worktree Configuration

## Port Assignments

| Worktree | Feature | Dev Port | Other Services |
|----------|---------|----------|----------------|
| project (main) | - | 3000 | - |
| project-auth | auth | 3001 | - |
| project-payments | payments | 3002 | Stripe mock: 4242 |
| project-design | design-system | 3003 | Storybook: 6006 |

## Port Convention

- **Main branch**: Default port (3000)
- **Feature worktrees**: 3001+ in creation order
- **Additional services**: Document in "Other Services" column

## Adding a New Worktree

1. Create worktree: `git worktree add ../project-feature feature-branch`
2. Assign next available port in this table
3. Configure the worktree:
   ```bash
   cd ../project-feature
   echo "PORT=30XX" >> .env.local
   ```
4. Commit the updated worktrees.md

## Environment Setup

Each worktree should have a `.env.local` (gitignored) with:
```
PORT=30XX
# Other worktree-specific env vars
```
```

**Benefits**:
- Run multiple dev servers simultaneously
- Quick reference for which port to use
- Avoid port conflicts between features
- Document additional services (Storybook, mock APIs, databases)

### Detection Logic

At session start and for every mode, Rustie determines context:

```bash
# 1. Get current worktree folder name
worktree_name=$(basename "$(git rev-parse --show-toplevel)")

# 2. Get current branch
branch=$(git branch --show-current)

# 3. Determine scope
if [[ "$branch" =~ ^(main|master)$ ]]; then
  SCOPE="DASHBOARD"  # Show all worktrees/features
else
  # Extract feature name from worktree
  # Convention: {project}-{feature} where feature may contain hyphens
  # e.g., "trustie-auth" → "auth"
  # e.g., "trustie-design-system" → "design-system"

  # Method: Remove first segment (project name) only
  feature_name="${worktree_name#*-}"  # Remove up to FIRST hyphen only

  # Validate feature exists in agent-docs
  if [[ -d "agent-docs/features/$feature_name" ]]; then
    SCOPE="$feature_name"
  else
    # Fallback: try matching against existing feature folders
    for dir in agent-docs/features/*/; do
      dir_name=$(basename "$dir")
      if [[ "$worktree_name" == *"$dir_name"* ]]; then
        SCOPE="$dir_name"
        break
      fi
    done
    [[ -z "$SCOPE" ]] && SCOPE="UNKNOWN"  # Prompt user to clarify
  fi
fi
```

**Important**: The convention is `{project}-{feature}` where:
- Project name is a single segment (no hyphens): `trustie`, `myapp`, `acme`
- Feature name can contain hyphens: `auth`, `design-system`, `user-profile`

Examples:
| Worktree Name | Extracted Feature |
|---------------|-------------------|
| `trustie-auth` | `auth` |
| `trustie-design-system` | `design-system` |
| `trustie-user-profile` | `user-profile` |
| `myapp-payments` | `payments` |

### Scoping Rules by Mode

| Mode | Feature Worktree Behavior | Main/Master Behavior |
|------|---------------------------|----------------------|
| **NBA** | Next task for THIS feature only | Dashboard: all features across all worktrees |
| **Work** | Auto-load feature (no prompt) | List features, ask which one |
| **Status** | THIS feature's progress only | Overview of all worktrees |
| **Handoff** | Auto-detect feature from worktree | N/A (prompt for feature) |
| **Sync** | Sync THIS worktree | Sync all or prompt for specific |
| **Test** | Test THIS feature | Prompt for feature |
| **Archive** | Archive THIS feature | List completable features |

### Scope Indicator in Output

Every Rustie output MUST include scope context:

```
RUSTIE [auth] - Scoped to current worktree
# or
RUSTIE [DASHBOARD] - All worktrees
```

### Worktree Overview Table (Main Branch Only)

When in main/master, NBA and Status modes show:

```
WORKTREE OVERVIEW
─────────────────────────────────────────────────────────────────
Worktree              Feature             Status        Progress
─────────────────────────────────────────────────────────────────
./trustie-auth        auth                In Progress   60% (6/10)
./trustie-payments    payments            Not Started   0% (0/8)
./trustie-ui          design-system       On Hold       30% (3/10)
./trustie (main)      [DASHBOARD]         -             -
─────────────────────────────────────────────────────────────────
Active: 1 in progress, 1 not started, 1 on hold
```

### Worktree Discovery

To build the overview table:

```bash
# List all worktrees for this repo
git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2

# For each worktree, extract feature name and find matching plan
for wt in $(git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2); do
  wt_name=$(basename "$wt")
  feature="${wt_name#*-}"  # Remove project prefix (up to first hyphen)
  plan="$wt/agent-docs/features/$feature/plan.md"
  if [[ -f "$plan" ]]; then
    # Extract progress from plan
  fi
done
```

### Why This Matters

1. **Reduced cognitive load**: Only see what's relevant to current work
2. **Faster startup**: No scanning unrelated plans
3. **Natural isolation**: Git worktrees provide code isolation; Rustie mirrors this for docs
4. **Dashboard when needed**: Main branch = planning/coordination view

---

## Commit Discipline - CRITICAL

**Rule**: Every commit must be EITHER agent-docs OR code, NEVER both.

**Enforcement**: Install the pre-commit hook to block mixed commits automatically:
```bash
rustie-install-hooks.sh
```

### Why
- Enables cherry-picking agent-docs commits to other worktrees
- Keeps git history clean and sync-able
- Makes `git log -- agent-docs/` useful for finding updates

### Workflow
1. **Before committing**: Check `git status` (or let pre-commit hook catch it)
2. **If both agent-docs/ AND code changed**:
   - Stage and commit agent-docs first: `git add agent-docs/ && git commit -m "docs: ..."`
   - Then stage and commit code: `git add . && git commit -m "feat/fix: ..."`
3. **If only one type changed**: Commit normally

### Commit Message Examples
```
docs: update plan progress for topic-research
docs: session handoff - design-system
docs: add lesson on playwright conflicts
feat: implement forum adapter component
fix: resolve null reference in survey form
```

### Cherry-Pick Workflow
To sync agent-docs to another worktree:
```bash
# In target worktree
git fetch origin
git cherry-pick <commit-hash>  # Pick specific docs: commits
# Or cherry-pick a range
git log --oneline origin/main -- agent-docs/  # Find commits
```

---

## Mode: NBA (Next Best Action)

**Triggers**: Session start with agent-docs/ present, "priorities", "what should I work on", "what's next"

Recommend what to work on next. **Behavior depends on worktree context.**

### Worktree-Aware Behavior

| Context | Behavior |
|---------|----------|
| **Feature worktree** | Show next task for THIS feature only |
| **Main/master** | Dashboard view of ALL worktrees/features |

### Steps

0. **Script alternative**: Run `rustie-session-start.sh` for automated pre-flight checks.
   The script handles steps 1-3 and outputs a summary. Use when starting a session.

1. **Detect scope** (see Worktree-Centric Workflow section):
   ```bash
   branch=$(git branch --show-current)
   if [[ "$branch" =~ ^(main|master)$ ]]; then
     SCOPE="DASHBOARD"
   else
     worktree_name=$(basename "$(git rev-parse --show-toplevel)")
     SCOPE="${worktree_name#*-}"  # Remove project prefix (up to first hyphen)
   fi
   ```

2. **Pre-flight**: Check `agent-docs/features/` exists.

3. **Auto-sync** (silent): Fetch latest plan updates from origin.
   ```bash
   git fetch origin --quiet
   ```

4. **If SCOPE = feature name** (Feature Worktree):
   - Read ONLY `agent-docs/features/$SCOPE/plan.md`
   - Extract status, progress, next unchecked task
   - Display scoped output (see below)

5. **If SCOPE = DASHBOARD** (Main Branch):
   - Discover all worktrees: `git worktree list`
   - For each worktree, find matching feature plan
   - Also scan local `agent-docs/features/*/plan.md` for features without worktrees
   - Build worktree overview table
   - Categorize and prioritize

6. **For each plan**, extract:
   - Feature name (from directory)
   - Status (`**Status**:` line)
   - Progress (count `[x]` vs total `[ ]`)
   - Next unchecked task (first `- [ ]`)
   - Worktree path (if exists)

7. **Categorize**:
   - **In Progress**: Has unchecked tasks, not "Complete" or "On Hold"
   - **Not Started**: 0% progress
   - **On Hold**: Status contains "Hold" or "Blocked"
   - **Complete**: 100% or Status = "Complete"

8. **Display (Feature Worktree)**:
   ```
   RUSTIE [feature-name] NBA
   ─────────────────────────────────────────

   Feature: [feature-name]
   Progress: X/Y tasks (Z%)
   Status: In Progress

   NEXT TASK:
   → [first unchecked task]

   Following tasks:
   2. [task]
   3. [task]

   START: [next task or blocker to resolve]
   ```

9. **Display (Dashboard - Main Branch)**:
   ```
   RUSTIE [DASHBOARD] NBA - ALL WORKTREES
   ─────────────────────────────────────────────────────────────────────────

   WORKTREE OVERVIEW
   Worktree              Feature             Port   Status        Progress
   ─────────────────────────────────────────────────────────────────────────
   ./project-auth        auth                3001   In Progress   60% (6/10)
   ./project-payments    payments            3002   Not Started   0% (0/8)
   (no worktree)         design-system       -      On Hold       30% (3/10)
   ─────────────────────────────────────────────────────────────────────────

   RECOMMENDATION:
   Continue "auth" in ./project-auth (localhost:3001)
   Next: [task description]

   To work: cd ../project-auth && claude
   To create worktree: git worktree add ../project-payments payments
   ```

   Port information is read from `agent-docs/worktrees.md`.

10. **Optionally** ask user which feature to work on (main branch only).

---

## Mode: Work

**Triggers**: Git branch pattern `feature/*` or `claude/*`, "load feature X", "start work on X", "work on X"

Load a feature's plan and PRD, update active-context, show next tasks. **Auto-detects feature from worktree.**

### Worktree-Aware Behavior

| Context | Behavior |
|---------|----------|
| **Feature worktree** | Auto-detect feature from worktree name - NO prompt needed |
| **Main/master** | List features and ask user which one to load |

### Steps

1. **Detect scope and auto-select feature**:
   ```bash
   branch=$(git branch --show-current)
   if [[ "$branch" =~ ^(main|master)$ ]]; then
     # Main branch: list features and ask
     feature=""  # Will prompt user
   else
     # Feature worktree: auto-detect
     worktree_name=$(basename "$(git rev-parse --show-toplevel)")
     feature="${worktree_name#*-}"  # Remove project prefix (up to first hyphen)

     # Validate feature exists
     if [[ ! -d "agent-docs/features/$feature" ]]; then
       echo "Warning: No matching feature for worktree '$worktree_name'"
       feature=""  # Fall back to prompt
     fi
   fi
   ```

2. **If feature not auto-detected**: Match argument against `agent-docs/features/*/`. If no argument, list features and ask user.

3. **Auto-sync** (silent): Fetch latest from origin.

4. **Check assumptions** (v2.2 - MANDATORY for new features):
   ```bash
   assumptions_file="agent-docs/features/$feature/assumptions.md"
   if [[ ! -f "$assumptions_file" ]]; then
     echo "No assumptions.md found. Running spike mode first..."
     # Trigger spike mode
   elif grep -q "❌ FAILED" "$assumptions_file"; then
     echo "Warning: Feature has unresolved failed assumptions"
     # Show failed assumptions and ask to confirm
   fi
   ```
   - If no assumptions.md → automatically run spike mode first
   - If assumptions.md has unresolved failures → warn and confirm before proceeding

5. **Read plan**: `agent-docs/features/[feature]/plan.md`
   - Extract status, progress, next 5 unchecked tasks
   - Extract current phase

6. **Read PRD** (if exists): `agent-docs/features/[feature]/PRD.md`
   - Extract overview and user stories for context

7. **LSP Symbol Grounding** (v2.3 - prevents hallucination):
   Before implementation, verify key symbols exist using LSP:

   ```
   # Identify key files from plan.md
   key_files = ["src/adapters/forum.ts", "src/types/post.ts"]

   # For each file, get real symbols via LSP
   for file in key_files:
     LSP: documentSymbol(file)
     → ForumAdapter (class), fetchPosts (method), Post (interface)

   # Include verified symbols in session context
   ```

   **Why this matters:**
   - AI may "remember" function names that don't exist
   - LSP provides ground truth from the actual codebase
   - Prevents errors like calling `getPosts()` when it's actually `fetchPosts()`

   **Integration:**
   - Run LSP documentSymbol on 2-5 key files identified in plan
   - Include real symbol names in session briefing
   - Reference verified names during implementation

8. **Update feature's active-context.md** (v2.1 - feature-scoped):

   **Script alternative**: Run `rustie-context-update.sh start` to create/update context reliably.

   Manual approach:
   ```bash
   # Path: agent-docs/features/[feature]/active-context.md
   context_file="agent-docs/features/$feature/active-context.md"
   ```
   ```markdown
   **Last Updated**: [now]
   **Feature**: [feature]
   **Worktree**: [worktree path]
   **Status**: In Progress

   ## Current Session
   Started: [timestamp]

   ## Next Steps
   1. [ ] [task from plan]
   2. [ ] [task from plan]

   ## Recent Changes
   - [will be updated as work progresses]
   ```

9. **Commit agent-docs separately**:
   ```bash
   git add agent-docs/
   git commit -m "docs: start work on [feature]"
   ```
   Note: If you also have code changes, commit them separately AFTER this.

10. **Show session briefing**:
   ```
   RUSTIE [feature-name] WORK SESSION
   ─────────────────────────────────────────

   Feature: [name]
   Worktree: [./project-feature]
   Dev Server: localhost:[port]  ← from worktrees.md
   Progress: X/Y tasks (Z%)
   Current Phase: [phase]

   ASSUMPTIONS: ✅ All verified (or ⚠️ X unresolved)

   NEXT 5 TASKS:
   - [ ] Task 1
   - [ ] Task 2
   ...

   FILES TO READ:
   - [path] - [why]

   START HERE: [first task or file to read]
   ```

   Read port from `agent-docs/worktrees.md` for this feature.

### Auto-Detection Examples

```
# In worktree ./trustie-auth (branch: auth or feature/auth)
$ claude "work mode"
→ Auto-detects feature "auth", loads plan immediately

# In main worktree (branch: main)
$ claude "work mode"
→ Lists all features, asks user which to load

# In worktree with explicit argument
$ claude "work on payments"
→ Uses explicit argument, ignores worktree detection
```

---

## Mode: Test

**Triggers**: Files in `app/`, `components/`, `pages/` modified, "test feature", "run playwright", "run tests"

Test features with Playwright, capture screenshots, optionally verify against design system.

### ⚠️ CRITICAL: Use Direct Playwright, NOT MCP

**For any project with UI, ALWAYS use project-installed Playwright via Bash**, not Playwright MCP tools.

**Why**: Playwright MCP uses a shared browser profile that causes "Browser is already in use"
errors in multi-worktree environments. Direct Playwright launches isolated browser instances.

**Setup** (one-time per project):
```bash
npm install -D @playwright/test playwright
npx playwright install chromium
```

**Create test script** at `tests/capture-screenshots.ts`:
```typescript
import { chromium } from 'playwright';

// Use PORT from .env.local or default based on worktree
// See agent-docs/worktrees.md for port assignments
const PORT = process.env.PORT || '3000';
const BASE_URL = process.env.TEST_URL || `http://localhost:${PORT}`;

async function captureScreenshots() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 }
  });
  const page = await context.newPage();

  // Navigate and capture
  await page.goto(`${BASE_URL}/your-page`);
  await page.screenshot({ path: 'tests/screenshots/page.png' });

  await browser.close();
}

captureScreenshots().catch(console.error);
```

### Usage Variants
- Basic test: "test [feature]"
- Full journey: "test [feature] user-journey"
- With design review: "test [feature] verify"

### Steps

1. **Ensure Playwright is installed**:
   ```bash
   grep "@playwright" package.json || npm install -D @playwright/test playwright
   ```

2. **Find feature plan**: `agent-docs/features/[feature]/plan.md`

3. **Read PRD** for user stories and expected behavior.

4. **Start dev server** if not running:
   ```bash
   npm run dev &
   # Wait for localhost:3000 (verify with: curl -s localhost:3000)
   ```

5. **If user-journey**:
   - Design journey from PRD user stories (CRUD flow)
   - Generate test data with LLM
   - **Run tests via Bash** (NOT MCP):
     ```bash
     npx tsx tests/capture-screenshots.ts
     # OR for full test suite:
     npx playwright test
     ```
   - Take screenshot after each step

6. **If verify**:
   - Send each screenshot to LLM for design review
   - Compare against design system (if exists)
   - Flag issues

7. **Create test report**:
   ```bash
   mkdir -p agent-docs/features/[feature]/tests/screenshots
   # Save report: test-report-[timestamp].md
   ```

8. **Summary**:
   ```
   RUSTIE TEST COMPLETE

   Steps: X/Y passed
   Screenshots: Z captured
   Design Issues: N found

   Report: agent-docs/features/[feature]/tests/test-report-*.md
   ```

### When to Use MCP vs Direct Playwright

| Scenario | Use MCP | Use Direct Playwright |
|----------|---------|----------------------|
| Single worktree only | ✅ OK | ✅ OK |
| Multi-worktree environment | ❌ Conflicts | ✅ Required |
| Interactive exploration | ✅ Good | ⚠️ Requires script |
| Screenshot capture | ⚠️ Lock issues | ✅ Required |
| Visual regression testing | ❌ Unreliable | ✅ Required |
| CI/CD pipelines | ❌ N/A | ✅ Required |

**Reference**: See `agent-docs/lessons/playwright-mcp-worktree-conflicts.md` for full RCA-PCA.

---

## Mode: Validate

**Triggers**: Before work mode, "validate feature", "check structure"

Check that a feature directory has all required files and valid structure.

### Steps

1. **Find feature** (or validate current if no argument)

2. **Check required files**:
   - PRD.md - REQUIRED
   - plan.md - REQUIRED
   - sessions/ - OPTIONAL
   - tests/ - OPTIONAL

3. **Validate plan structure**:
   - Has `**Status**:` field
   - Has checkboxes (`- [ ]` or `- [x]`)
   - Has phases (## Phase headers)

4. **Validate PRD structure**:
   - Has Problem Statement
   - Has User Stories
   - Has Success Criteria

5. **Report results**:
   ```
   VALIDATION: [feature-name]

   Required Files:
   PRD.md: FOUND / MISSING
   plan.md: FOUND / MISSING

   Plan Structure:
   Status field: FOUND / MISSING
   Checkboxes: X found
   Phases: Y found

   Result: VALID / NEEDS FIXES
   ```

6. **If invalid**, suggest fixes.

7. **If valid AND new feature** (no assumptions.md exists):
   - Automatically trigger Spike mode
   - "Structure valid. Running assumption validation..."

---

## Mode: Spike (v2.4)

**Triggers**:
- Automatically after validate passes for new features (no assumptions.md)
- "test assumptions", "spike", "validate assumptions"
- "check assumptions for [feature]"

**Purpose**: Identify and test key technical assumptions BEFORE implementation starts. This prevents wasted effort when plans are based on false assumptions.

**v2.4 Enhancements**:
- **LSP Grounding**: Verify code reality before planning
- **ADR Integration**: Record significant decisions during spike
- **Pattern Compliance**: Surface lessons and codebase patterns
- **PRD Hash Tracking**: Detect assumption drift

### Why Spike Mode Exists

**Problem**: Plans often contain implicit technical assumptions that aren't validated until implementation fails.

**Example**: A web scraping project assumed server-side rendering, but the site was client-side rendered. The entire approach was invalidated after work started.

**Solution**: Test assumptions with minimal "spike" code before committing to implementation.

### Assumption Categories (Explicit)

| Category | Examples | Test Methods |
|----------|----------|--------------|
| **Rendering** | SSR vs CSR, static vs dynamic | `curl` + check content, view page source |
| **API** | REST vs GraphQL, auth method, rate limits | API probe requests |
| **Data Format** | JSON structure, encoding, pagination | Sample request + parse |
| **Dependencies** | Package availability, version compatibility | Package lookup, install test |
| **Performance** | Response times, throughput limits | Timed requests |
| **Access** | Authentication requirements, CORS, robots.txt | Direct access tests |

### Implicit Assumption Discovery (v2.2)

The categories above catch "known unknowns" - assumptions we know to look for. But plans often contain "unknown unknowns" - assumptions so implicit they're invisible until they fail.

**Two-Phase Approach**:
- **Phase 1**: Check explicit categories (table above)
- **Phase 2**: Discover implicit assumptions through structured prompting

**Discovery Prompts** (run after Phase 1):

1. **Senior Engineer Review**:
   ```
   As a senior engineer with 20 years of experience, ultrathink about this plan and PRD.
   What implicit assumptions are being made that aren't explicitly stated? Consider:
   - Environmental (OS, memory, network reliability, disk space)
   - Timing/ordering (events arrive in order, responses before timeout)
   - State/consistency (database state, cache validity)
   - Scale (concurrent users, data volume growth)
   - Integration (third-party API stability, backward compatibility)
   - Security (input sanitized upstream, auth handled elsewhere)
   - User behavior (users won't do X, all users have Y)
   - Cultural/locale (language, timezone, currency, date format)
   ```

2. **Failure Mode Analysis**:
   ```
   What could go wrong that we haven't explicitly considered?
   What edge cases would break this design?
   What happens if [network fails / API is slow / data is malformed / load spikes]?
   ```

3. **Pessimist Review**:
   ```
   As a pessimistic code reviewer who has seen many projects fail:
   What holes would you poke in this plan?
   What would you insist we verify before proceeding?
   What's the most likely way this project fails?
   ```

**Domain-Specific Discovery Questions**:

| Domain | Questions to Ask |
|--------|------------------|
| **Web Scraping** | What if site structure changes? Rate limiting? Geo-blocking? |
| **API Integration** | What about retries? Idempotency? Version changes? |
| **Data Processing** | Character encoding? Malformed input? Memory limits? |
| **Mobile/Cross-platform** | Device fragmentation? Offline mode? Battery impact? |
| **Auth/Security** | Token expiry? Session handling? Permission edge cases? |

**Discovered Assumption Handling**:
- **Testable**: Add to test queue with appropriate priority
- **Non-testable but critical**: Document as "⚠️ NOTED - manual consideration required"
- **Architectural**: May require plan revision before testing

### Pre-Spike LSP Grounding (v2.4)

Before testing assumptions, ground the plan in code reality using LSP tools. This prevents plans that reference non-existent code or ignore established patterns.

**LSP Grounding Steps**:

1. **Identify key files from PRD.md**:
   - Dependencies mentioned (APIs, libraries, components)
   - Integration points (files that will be modified)
   - Related existing features

2. **Run LSP documentSymbol** on key files:
   ```
   For each key file:
   → LSP documentSymbol to get functions, classes, interfaces
   → Build verified symbol table
   ```

3. **Run LSP findReferences** for key functions:
   ```
   For heavily-used patterns:
   → LSP findReferences to see how they're used
   → Extract existing conventions
   ```

4. **Build Code Reality Summary**:
   ```markdown
   ## Code Reality Check (LSP-Grounded)

   ### Verified Symbols (can be called/used)
   | File | Symbol | Type | References |
   |------|--------|------|------------|
   | src/auth/jwt.ts | verifyToken | function | 12 |
   | src/api/client.ts | fetchWithRetry | function | 8 |

   ### Existing Patterns Detected
   - Error handling: ErrorBoundary component (23 usages)
   - API calls: All use fetchWithRetry wrapper
   - State management: React Context (no Redux)

   ### Grounding Violations
   ⚠️ Plan references `AuthService.validate()` - symbol not found
   ⚠️ Plan assumes REST, but `graphql/` directory detected
   ```

**Benefits**:
- Plans cannot reference non-existent functions
- Existing patterns are surfaced before decisions
- Architectural assumptions caught before implementation

### ADR Integration (v2.4)

When significant design decisions are made during spike, record them as Architecture Decision Records (ADRs) in the existing `decisions/adrs/` structure.

**When to Create ADR**:
- Choosing between alternative approaches (e.g., REST vs GraphQL)
- Selecting technology/library for a capability
- Deciding on architectural patterns
- Resolving contradictions between requirements

**ADR Creation During Spike**:

1. **Detect decision point**: When spike reveals a choice must be made
2. **Prompt for ADR**:
   ```
   Significant decision detected: [choice description]

   Create ADR? This will document:
   - The decision and rationale
   - Alternatives considered
   - Lessons that informed this choice

   [Create ADR] [Skip - not significant]
   ```

3. **Create ADR file** in appropriate location:
   - Feature-specific: `agent-docs/features/{feature}/decisions/ADR-{n}-{slug}.md`
   - Global/cross-cutting: `agent-docs/decisions/adrs/ADR-{n}-{slug}.md`

4. **ADR Template**:
   ```markdown
   # ADR-{number}: {title}

   **Status**: Proposed | Accepted | Deprecated | Superseded
   **Date**: {date}
   **Feature**: {feature-name} or "Global"

   ## Context
   What is the issue that motivated this decision?

   ## Decision
   What is the change or approach we're adopting?

   ## Rationale
   Why this approach over alternatives?

   ## Alternatives Considered
   | Alternative | Pros | Cons |
   |-------------|------|------|
   | {alt 1} | {pros} | {cons} |
   | {alt 2} | {pros} | {cons} |

   ## Consequences
   What becomes easier or harder because of this?

   ## Related
   - PRD: {link if applicable}
   - Lessons: {relevant lesson refs}
   - Prior ADRs: {supersedes/relates-to}
   ```

5. **Link from assumptions.md**: Add ADR reference to Related ADRs section

### Pattern Surfacing (v2.4)

At spike start, systematically gather patterns from three sources:

**Tier 1: Lesson Patterns** (from RCA-PCA system)
- Query lessons catalog for `trigger_technologies` matching PRD tech stack
- Query for `trigger_contexts` matching feature type
- Extract PCAs as patterns to follow/consider

**Tier 2: Code Patterns** (from codebase via Explore agent + LSP)
- **Use Explore agent** for broad pattern detection (v2.4):
  ```
  Task(subagent_type="Explore", prompt="""
  Find existing implementations related to [feature domain]:
  1. Similar features (authentication, API endpoints, etc.)
  2. Established patterns (error handling, state management, etc.)
  3. Utility functions that should be reused
  4. Architectural patterns (folder structure, naming conventions)

  Return: file paths, pattern descriptions, usage counts
  """)
  ```
- Use LSP findReferences on common utilities for precise counts
- Identify established conventions (error handling, API calls, etc.)
- Surface as "existing patterns"

**Tier 3: ADR Patterns** (from prior decisions)
- **Use rustie-prior-decisions.sh** for automated ADR cross-referencing (v2.4):
  ```bash
  # Query prior ADRs for relevant precedents
  ./scripts/rustie-prior-decisions.sh --keywords "auth,jwt,session" --feature "user-login"

  # Output: matching ADRs with status, decisions, and conflict flags
  ```
- Search `decisions/adrs/` for related prior decisions
- Flag potential conflicts with new decisions
- Surface as "precedent decisions"

**Pattern Compliance Table** (added to assumptions.md):
```markdown
## Pattern Compliance

| Pattern | Source | Status | Notes |
|---------|--------|--------|-------|
| "Always use fetchWithRetry" | codebase:src/api/client.ts | Will Follow | |
| "JWT via interceptor" | ADR-042 | Will Follow | |
| "Validate inputs at boundary" | lesson:api-security | Will Follow | |
| "Use GraphQL for complex queries" | ADR-015 | Conflict | PRD suggests REST |
```

**Status Values**:
- `Will Follow`: Will implement this pattern
- `Conflict`: Pattern conflicts with current approach - needs ADR
- `Not Applicable`: Pattern doesn't apply to this feature
- `Override`: Consciously choosing different approach (document why)

### Steps

1. **Read PRD.md and plan.md** for the feature

2. **Compute PRD Hash** (for drift detection):
   ```bash
   # Store hash to detect future PRD changes
   PRD_HASH=$(sha256sum agent-docs/features/{feature}/PRD.md | cut -d' ' -f1)
   ```

3. **Run Pre-Spike LSP Grounding** (v2.4):
   - Identify key files mentioned in PRD
   - Run LSP documentSymbol on each
   - Build Code Reality Summary
   - Flag any grounding violations

4. **Surface Patterns** (v2.4):
   - Query lessons catalog for matching patterns
   - Use LSP to detect codebase patterns
   - Check prior ADRs for precedent decisions
   - Build Pattern Compliance table

5. **Phase 1 - Extract explicit assumptions** (predefined categories):
   - Scan for technology choices mentioned or implied
   - Identify external dependencies
   - Note data format expectations
   - Flag performance requirements
   - List access/auth assumptions

6. **Phase 2 - Discover implicit assumptions** (structured prompting):
   - Run Senior Engineer Review prompt
   - Run Failure Mode Analysis
   - Run Pessimist Review
   - Apply domain-specific questions if applicable
   - Merge discovered assumptions with explicit list

7. **Categorize ALL assumptions by risk**:
   - **Critical**: If wrong, invalidates entire approach
   - **High**: Requires significant plan changes
   - **Medium**: Requires task-level adjustments
   - **Low**: Minor impact

8. **Create verification tests** for Critical/High assumptions:
   ```bash
   # Example: Test if site is SSR
   curl -s "https://example.com" | grep -q "expected-content"

   # Example: Test API endpoint exists
   curl -s -o /dev/null -w "%{http_code}" "https://api.example.com/endpoint"

   # Example: Check rate limiting
   for i in {1..10}; do curl -s -o /dev/null -w "%{http_code}\n" "https://api.example.com"; done
   ```

9. **Run tests** and collect results

10. **Create/update assumptions.md** (v2.4 enhanced template):
   ```markdown
   # Technical Assumptions: [feature]

   ## Context (v2.4)
   **Last Validated**: [timestamp]
   **Feature**: [feature-name]
   **PRD Hash**: sha256:[hash] (for drift detection)
   **Related ADRs**: [links to ADRs created during this spike]

   ## Code Reality Check (LSP-Grounded)

   ### Verified Symbols
   | File | Symbol | Type | References |
   |------|--------|------|------------|
   | src/auth/jwt.ts | verifyToken | function | 12 |
   | src/api/client.ts | fetchWithRetry | function | 8 |

   ### Grounding Violations
   ⚠️ None detected (or list violations)

   ## Pattern Compliance

   | Pattern | Source | Status | Notes |
   |---------|--------|--------|-------|
   | "Use fetchWithRetry" | codebase:src/api/client.ts | Will Follow | |
   | "JWT via interceptor" | ADR-042 | Will Follow | |
   | "Validate inputs" | lesson:api-security | Will Follow | |

   ## Critical Assumptions (Explicit)

   | Assumption | Test | Result | Impact |
   |------------|------|--------|--------|
   | Site is SSR | curl + grep content | ❌ FAILED | Need browser automation |
   | API is REST | GET /api endpoint | ✅ PASSED | - |

   ## High-Risk Assumptions (Explicit)

   | Assumption | Test | Result | Impact |
   |------------|------|--------|--------|
   | No auth required | curl without headers | ✅ PASSED | - |

   ## Discovered Assumptions (Implicit)

   These were surfaced through structured review, not predefined categories.

   | Source | Assumption | Risk | Test | Result |
   |--------|------------|------|------|--------|
   | Senior Review | Network is reliable | Medium | N/A | ⚠️ NOTED |
   | Failure Analysis | API may change structure | High | Check API versioning | ✅ PASSED |
   | Pessimist Review | Rate limits under burst | High | Burst test (10 req/s) | ✅ PASSED |
   | Domain-Specific | Site structure may change | Medium | N/A | ⚠️ NOTED |

   ## Pending (not yet tested)

   - [ ] Rate limit > 60/min
   - [ ] Pagination supported

   ## Plan Impact

   ### Failed Assumptions
   - **Site is SSR**: Original plan used simple HTTP requests
     - **Revised**: Use Playwright for browser automation
     - **Tasks affected**: All scraping tasks

   ### Noted Assumptions (require manual consideration)
   - **Network reliability**: Add retry logic with exponential backoff
   - **Site structure changes**: Design for graceful degradation, add monitoring

   ### Recommendations
   1. Update plan.md with Playwright approach
   2. Add browser setup task
   3. Add retry logic for network resilience
   4. Increase time estimates by 50%
   ```

11. **If critical assumptions fail**:
   - Display clear warning
   - Show impact on plan
   - Offer options:
     1. Update plan automatically
     2. Discuss alternatives with user
     3. Proceed anyway (not recommended)

12. **Output summary**:
   ```
   RUSTIE [feature] SPIKE COMPLETE
   ─────────────────────────────────────────

   EXPLICIT ASSUMPTIONS (predefined categories):
   ✅ Passed: 3  ❌ Failed: 1 (CRITICAL)  ⏳ Pending: 1

   DISCOVERED ASSUMPTIONS (implicit):
   ✅ Tested: 2  ⚠️ Noted: 2 (require consideration)

   CRITICAL FAILURE:
   → "Site is SSR" - Content loaded via JavaScript

   NOTED (manual consideration required):
   → Network reliability - Add retry logic
   → Site structure changes - Add monitoring

   IMPACT: Plan requires browser automation (Playwright)

   Options:
   1. Update plan with Playwright approach
   2. Discuss alternatives
   3. Proceed with original plan (not recommended)

   assumptions.md saved to: agent-docs/features/[feature]/
   ```

### Integration with Work Mode

Work mode checks for assumptions.md:
- If exists with no critical failures → proceed
- If exists with unresolved failures → warn and ask to confirm
- If missing for feature with plan.md → trigger spike first

**PRD Drift Detection (v2.4)**:
Work mode also checks PRD hash when assumptions.md exists:
```bash
# Compare current PRD hash against stored hash
CURRENT_HASH=$(sha256sum agent-docs/features/{feature}/PRD.md | cut -d' ' -f1)
STORED_HASH=$(grep "PRD Hash" assumptions.md | cut -d':' -f2 | tr -d ' ')

if [ "$CURRENT_HASH" != "$STORED_HASH" ]; then
    echo "⚠️ PRD has changed since last spike!"
    echo "Assumptions may no longer be valid."
    echo "Options: [Re-spike] [Proceed anyway] [View diff]"
fi
```

**Continuous LSP Grounding (v2.4)**:
During work mode, run a background agent to verify code references in real-time:

```
Task(subagent_type="Explore", run_in_background=true, prompt="""
CONTINUOUS GROUNDING VERIFICATION

Monitor the current implementation for hallucination detection:

1. **File Path Verification**:
   - Extract file paths from plan.md and current task
   - Verify each path exists using Glob
   - Alert if referencing non-existent files

2. **Symbol Reference Verification**:
   - For each function/class mentioned in plan
   - Use LSP documentSymbol to verify it exists
   - Check signature matches expected usage

3. **Pattern Drift Detection**:
   - Compare implementation against Pattern Compliance table
   - Flag if deviating from stated patterns without ADR

Report Format:
```json
{
  "status": "grounded|drift_detected|hallucination",
  "verified_paths": [...],
  "missing_paths": [...],
  "verified_symbols": [...],
  "missing_symbols": [...],
  "pattern_violations": [...]
}
```

Alert immediately if:
- File path in plan doesn't exist
- Symbol referenced but not found via LSP
- Implementation contradicts Pattern Compliance table
""")
```

**When to Trigger Background Verification**:
- At work mode start (initial grounding check)
- After completing each plan step (incremental verification)
- Before major implementation decisions (pre-decision check)
- When context usage exceeds 50% (drift prevention)

**Handling Verification Alerts**:
```markdown
## Grounding Alert Response

| Alert Type | Severity | Action |
|------------|----------|--------|
| Missing file path | ERROR | Stop, correct plan or create file |
| Missing symbol | ERROR | Stop, verify with LSP, update approach |
| Pattern violation | WARN | Document deviation, create ADR if needed |
| Signature mismatch | WARN | Verify correct usage, update if wrong |
```

### Spike Best Practices

1. **Keep tests minimal** - Just enough to validate, not full implementation
2. **Test critical first** - Don't waste time on low-risk assumptions if critical fails
3. **Document everything** - Future sessions need to know what was validated
4. **Update on re-spike** - If context changes, re-run relevant tests
5. **Time-box testing** - Max 5 minutes per assumption test
6. **Run discovery prompts thoroughly** - The implicit assumptions often cause the biggest failures
7. **Don't dismiss "NOTED" assumptions** - They can't be tested but still need mitigation
8. **Think like a pessimist** - The failure modes you don't consider are the ones that bite you

### Parallel Testing with Sub-Agents (v2.3)

When multiple Critical/High assumptions are independent, test them in parallel using the Task tool:

**When to Parallelize:**
- 3+ assumptions to test
- Assumptions are independent (don't depend on each other's results)
- Testing would take >2 minutes sequentially

**How to Parallelize:**

1. **Launch up to 3 agents simultaneously** (single message, multiple Task tool calls):
   ```
   Agent 1: "Test rendering assumption - use curl to fetch {url} and check if content
            contains expected elements. Return: PASSED/FAILED with evidence."

   Agent 2: "Test API authentication - probe {endpoint} with/without auth headers.
            Return: PASSED/FAILED with response codes."

   Agent 3: "Test rate limiting - send 10 rapid requests to {endpoint}.
            Return: PASSED/FAILED with any 429 responses noted."
   ```

2. **Aggregate results** from all agents into assumptions.md

3. **Handle mixed results**: If any Critical assumption fails, stop and reassess before continuing

**Example Parallel Spike:**
```markdown
Launching 3 parallel assumption tests:
├─ Agent 1: Rendering type (SSR vs CSR)
├─ Agent 2: API authentication method
└─ Agent 3: Rate limit detection

Results:
├─ Agent 1: ✅ PASSED - SSR confirmed (content in initial HTML)
├─ Agent 2: ❌ FAILED - Requires OAuth (got 401 without token)
└─ Agent 3: ✅ PASSED - No rate limit detected in 10 requests
```

**Benefits:**
- Reduces spike time from 5-10 min to 2-3 min
- Each agent focuses on one category (better accuracy)
- Parallel discovery of issues

---

## Mode: Sync

**Triggers**: Called by nba/work modes, "sync plans", "sync worktrees", "sync all"

Commit plan updates, fetch from origin, merge changes. **Scope depends on worktree context.**

### Worktree-Aware Behavior

| Context | Behavior |
|---------|----------|
| **Feature worktree** | Sync THIS worktree only |
| **Main/master** | "sync" = this worktree, "sync all" = all worktrees |

### Steps (Single Worktree - Default)

1. **Detect current worktree**:
   ```bash
   worktree_path=$(git rev-parse --show-toplevel)
   worktree_name=$(basename "$worktree_path")
   feature="${worktree_name#*-}"  # Remove project prefix
   ```

2. **Check git status**:
   ```bash
   git status --porcelain agent-docs/
   ```

3. **If changes**, commit them:
   ```bash
   git add agent-docs/
   git commit -m "docs: sync progress from $feature"
   ```

4. **Fetch from origin**:
   ```bash
   git fetch origin --all --prune
   ```

5. **Merge agent-docs/** from origin:
   ```bash
   git merge origin/$(git branch --show-current) --no-commit -- agent-docs/
   ```

6. **If conflicts**:
   - For checkbox-only changes: Auto-merge (prefer `[x]`)
   - For text changes: Abort, ask user to resolve manually

7. **Complete merge**:
   ```bash
   git commit -m "docs: merge updates from origin"
   ```

8. **Summary (Feature Worktree)**:
   ```
   RUSTIE [feature-name] SYNC COMPLETE
   ─────────────────────────────────────────

   Worktree: [./project-feature]
   Committed: X files
   Fetched: Y branches updated
   Merged: Z changes
   ```

### Steps (All Worktrees - Main Branch "sync all")

1. **Discover all worktrees**:
   ```bash
   git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2
   ```

2. **For each worktree**:
   ```bash
   for wt in $(git worktree list --porcelain | grep "^worktree" | cut -d' ' -f2); do
     echo "Syncing $wt..."
     (cd "$wt" && git fetch origin && git status --porcelain agent-docs/)
   done
   ```

3. **Report cross-worktree status**:
   ```
   RUSTIE [DASHBOARD] SYNC ALL
   ─────────────────────────────────────────────────────────────────

   WORKTREE SYNC STATUS
   Worktree              Branch        Local Changes   Remote Ahead
   ─────────────────────────────────────────────────────────────────
   ./project-auth        auth          2 files         0 commits
   ./project-payments    payments      0 files         3 commits
   ./project (main)      main          0 files         0 commits
   ─────────────────────────────────────────────────────────────────

   CHERRY-PICK NEEDED
   From auth → main: 2 docs commits
   Command: git cherry-pick abc123 def456

   To sync specific: cd ../project-payments && git pull origin payments
   ```

### Helper Scripts

**Check sync status across all worktrees**:
```bash
./agent-docs/scripts/compare-worktrees.sh
```

**Get cherry-pick commands for manual sync**:
```bash
./agent-docs/scripts/sync-helper.sh           # All worktrees
./agent-docs/scripts/sync-helper.sh design    # Specific worktree
```

---

## Mode: Status

**Triggers**: "status", "where am I", "what's the current state"

Show quick status without full NBA analysis. **Scoped to worktree context.**

### Worktree-Aware Behavior

| Context | Behavior |
|---------|----------|
| **Feature worktree** | Show THIS feature's status only |
| **Main/master** | Show overview of ALL worktrees/features |

### Steps

0. **Script alternative**: Run `rustie-plan-status.sh` for quick progress check.
   Use `rustie-plan-status.sh --all` for dashboard view.

1. **Detect scope**:
   ```bash
   branch=$(git branch --show-current)
   if [[ "$branch" =~ ^(main|master)$ ]]; then
     SCOPE="DASHBOARD"
   else
     worktree_name=$(basename "$(git rev-parse --show-toplevel)")
     SCOPE="${worktree_name#*-}"  # Remove project prefix
   fi
   ```

2. **If SCOPE = feature name** (Feature Worktree):
   - Read feature's context: `agent-docs/features/$SCOPE/active-context.md`
   - Get progress from `agent-docs/features/$SCOPE/plan.md`
   - Check for blockers
   - Display feature-scoped status

3. **If SCOPE = DASHBOARD** (Main Branch):
   - Discover all worktrees: `git worktree list`
   - For each worktree, read `features/{feature}/active-context.md`
   - Build overview table from all feature contexts
   - Show cross-worktree sync status

4. **Show summary (Feature Worktree)**:
   ```
   RUSTIE [feature-name] STATUS
   ─────────────────────────────────────────

   Feature: [name]
   Worktree: [./project-feature]
   Dev Server: localhost:[port]
   Progress: X/Y tasks (Z%)
   Status: [In Progress / Blocked / etc.]

   Next tasks:
   - [ ] Task 1
   - [ ] Task 2

   Blockers: None / [blocker description]

   Context: ~X% (estimate)

   Commands:
   - "work on [feature]" - Load full context
   - "create handoff" - Create handoff (if context > 70%)
   ```

5. **Show summary (Dashboard - Main Branch)**:
   ```
   RUSTIE [DASHBOARD] STATUS - ALL WORKTREES
   ─────────────────────────────────────────────────────────────────────────

   WORKTREE OVERVIEW
   Worktree              Feature             Port   Status        Progress
   ─────────────────────────────────────────────────────────────────────────
   ./project-auth        auth                3001   In Progress   60% (6/10)
   ./project-payments    payments            3002   Not Started   0% (0/8)
   (no worktree)         design-system       -      On Hold       30% (3/10)
   ─────────────────────────────────────────────────────────────────────────

   SYNC STATUS
   Last sync: 2h ago
   Pending cherry-picks: 2 commits from auth → main

   Commands:
   - cd ../project-auth && claude  - Work on auth (localhost:3001)
   - "sync all" - Sync all worktrees
   - "show priorities" - Detailed NBA analysis
   ```

---

## Mode: Handoff

**Triggers**: Context >70%, "handoff", "wrap up", "create handoff", "ending session"

Create a handoff document for the next AI agent session. **Auto-detects feature from worktree.**

### Worktree-Aware Behavior

| Context | Behavior |
|---------|----------|
| **Feature worktree** | Auto-detect feature - handoff goes to THIS feature's sessions/ |
| **Main/master** | Must specify feature explicitly |

### Steps

0. **Pre-step**: Run `rustie-context-update.sh end` to record session summary.
   This updates the context file with what was accomplished before creating the handoff.

1. **Detect scope and auto-select feature**:
   ```bash
   branch=$(git branch --show-current)
   if [[ "$branch" =~ ^(main|master)$ ]]; then
     # Main branch: must specify feature or prompt
     feature=""  # Prompt user for feature
   else
     # Feature worktree: auto-detect
     worktree_name=$(basename "$(git rev-parse --show-toplevel)")
     feature="${worktree_name#*-}"  # Remove project prefix
   fi
   ```

2. **Read feature's active context** (v2.1 - feature-scoped):
   ```bash
   context_file="agent-docs/features/$feature/active-context.md"
   cat "$context_file"
   ```
   Extract: Feature, Worktree, Status, Recent Changes

3. **Get git context**:
   ```bash
   git log --oneline -10
   git status
   git diff --stat
   ```

4. **Ask user** (use AskUserQuestion):
   - Context percentage: "70-75%", "76-85%", "86-95%", ">95%"
   - Reason: "Context limit", "Natural breakpoint", "End of session"
   - Any blockers?
   - What should next agent do first?

5. **Create session folder** in feature directory:
   ```bash
   feature_dir="agent-docs/features/$feature"
   timestamp=$(date -u +"%Y%m%d-%H%M%S")
   session_dir="${feature_dir}/sessions/session-${timestamp}"
   mkdir -p "$session_dir"
   ```

6. **Create handoff** using template at `agent-docs/templates/handoff-template.md`. Fill in ALL [TODO:] markers.

7. **Write handoff** to `$session_dir/handoff.md`

8. **Update feature's active-context.md** with handoff reference:
   ```bash
   context_file="agent-docs/features/$feature/active-context.md"
   # Update with: Handoff created, session path, next agent instructions
   ```

9. **Commit agent-docs separately**:
   ```bash
   # First, commit any uncommitted code changes
   git status
   # If code changes exist:
   git add -u  # Stage modified code files only (excludes agent-docs)
   git reset agent-docs/  # Ensure agent-docs not staged
   git commit -m "feat/fix: [describe code changes]"

   # Then commit agent-docs
   git add agent-docs/
   git commit -m "docs: session handoff - [feature name]"
   ```

10. **Confirm**:
    ```
    RUSTIE [feature-name] HANDOFF CREATED
    ─────────────────────────────────────────

    Handoff: [session_dir]/handoff.md
    Worktree: [./project-feature]
    Commits this session: [X]
    Files changed: [Y]

    Next agent should: [user's answer]

    To resume: cd [worktree-path] && claude "load feature [name]"
    ```

### Key Rules
- **v2.0 paths**: Sessions go in `agent-docs/features/[feature]/sessions/`, NOT `agent-docs/sessions/`
- **No placeholders**: Replace ALL [TODO:] markers
- **Always commit**: Handoff must be in git
- **Include worktree path**: Next agent needs to know which worktree to cd into

---

## Mode: Archive

**Triggers**: Feature plan 100% complete, "archive feature", "feature complete"

Move a completed feature from features/ to archives/.

### Steps

1. **Find feature** (or list available if no argument)

2. **Verify completion** - Check plan.md is 100% complete:
   ```bash
   feature_dir="agent-docs/features/$1"
   total=$(grep -c "^\- \[" "$feature_dir/plan.md")
   done=$(grep -c "^\- \[x\]" "$feature_dir/plan.md")
   ```

3. **If not 100%**, ask user to confirm archiving incomplete feature.

4. **Update plan status**:
   - Set `**Status**: Complete`
   - Add `**Archived**: YYYY-MM-DD`

5. **Move to archives**:
   ```bash
   mv agent-docs/features/$1 agent-docs/archives/features-completed/$1
   ```

6. **Note**: The feature's `active-context.md` moves with the feature to archives (no separate update needed).

7. **Commit**:
   ```bash
   git add agent-docs/
   git commit -m "docs: archive completed feature - $1"
   ```

8. **Confirm**: "Feature archived. Run NBA to see next priorities."

---

## Mode: RCA-PCA (Root Cause Analysis)

**Triggers**: Errors, failures, "why did this fail", "run rca", "what went wrong"

Perform systematic 5 Whys analysis on issues.

### When to Use
- After debugging a tricky issue
- When something broke unexpectedly
- After deployment failures
- When doing the same workaround twice

### Steps

1. **Gather context** - Ask user (use AskUserQuestion):
   - What went wrong?
   - When did it happen?
   - How was it discovered?
   - What was the immediate fix?

2. **Perform 5 Whys analysis**:
   ```
   Problem: [what went wrong]
   Why 1: [immediate cause]
   Why 2: [why did that happen]
   Why 3: [deeper cause]
   Why 4: [system/process cause]
   Why 5: [root cause]
   ```

3. **Identify root cause category**:
   - Configuration drift
   - Missing validation
   - Unclear documentation
   - Implicit assumption
   - Missing test coverage
   - Process gap

4. **Define Permanent Corrective Actions** (PCAs):
   - What check would have caught this?
   - What documentation should be added?
   - What automation could prevent recurrence?

5. **Create lesson document**:
   ```bash
   timestamp=$(date -u +"%Y-%m-%d")
   filename="agent-docs/lessons/${timestamp}-[short-name].md"
   ```

6. **Use lesson template**:
   ```markdown
   # Lesson: [Title]

   **Date**: YYYY-MM-DD
   **Severity**: High/Medium/Low
   **Category**: [category]
   **Triggers**: [keywords for retrieval]

   ## What Happened
   [Brief description]

   ## 5 Whys Analysis
   1. Why: [answer]
   2. Why: [answer]
   3. Why: [answer]
   4. Why: [answer]
   5. Why (Root Cause): [answer]

   ## Permanent Corrective Actions
   - [ ] PCA 1: [action]
   - [ ] PCA 2: [action]

   ## Prevention
   Next time, do this BEFORE:
   1. [check]
   2. [check]
   ```

7. **Update lessons catalog** if exists

8. **Commit** and show summary

---

## Mode: Tidyup

**Triggers**: "organize", "cleanup docs", "tidyup", scattered .md files detected

Auto-categorize scattered .md files into proper agent-docs/ structure.

### Steps

1. **Scan for scattered files**:
   ```bash
   find . -maxdepth 2 -name "*.md" -not -path "./agent-docs/*" -not -path "./node_modules/*"
   ```

2. **For each file**, determine category:
   - Contains "PRD", "requirement" → PRD for feature
   - Contains "plan", "implementation" → Plan for feature
   - Contains "lesson", "RCA" → lessons/
   - Contains "ADR", "decision" → decisions/adrs/
   - Contains "checklist" → instructions/checklists/
   - Other → reference/

3. **Preview moves**: Show user what will be moved and where.

4. **Ask confirmation**: Use AskUserQuestion.

5. **Move files** (use git mv to preserve history):
   ```bash
   git mv ./OLD-PLAN.md agent-docs/features/[name]/plan.md
   ```

6. **Commit**:
   ```bash
   git commit -m "docs: tidyup - organize scattered documentation"
   ```

7. **Summary**:
   ```
   RUSTIE TIDYUP COMPLETE

   Moved: X files
   - Y to features/
   - Z to lessons/
   - N to reference/

   Project root is now clean!
   ```

---

## Agent-Docs Structure Reference

```
agent-docs/
├── worktrees.md                    # Port assignments & worktree config (v2.1)
├── features/
│   └── [feature-name]/
│       ├── PRD.md                  # Requirements
│       ├── plan.md                 # Implementation tasks
│       ├── active-context.md       # Feature's current state (v2.1)
│       ├── sessions/               # Handoffs
│       ├── tests/                  # Test reports
│       └── verify-reports/         # Stop hook verification reports (v2.1)
├── archives/
│   └── features-completed/         # Archived features
├── lessons/
│   ├── high-priority/              # Critical lessons
│   └── catalog.yaml                # Lesson index
├── decisions/adrs/                 # Architecture decisions
├── instructions/checklists/        # Validation checklists
├── reference/                      # Reference docs
├── templates/                      # Templates
└── rustie-method.md               # Full methodology
```

### DEPRECATED: current/ folder (v2.0 → v2.1 migration)

The `agent-docs/current/` folder is **deprecated** as of v2.1.

**Why**: In multi-worktree setups, a single `current/active-context.md` causes conflicts when syncing between worktrees. Each worktree overwrites the others' context.

**New approach**: Active context lives inside each feature folder:
- `agent-docs/features/auth/active-context.md`
- `agent-docs/features/payments/active-context.md`

**Migration**: If `current/active-context.md` exists:
1. Read it to determine which feature it references
2. Move content to `features/{feature}/active-context.md`
3. Delete `current/` folder (or leave empty)

### Migration Script

```bash
#!/bin/bash
# migrate-context.sh - Run once per project to migrate from v2.0 to v2.1

OLD_CONTEXT="agent-docs/current/active-context.md"

if [[ -f "$OLD_CONTEXT" ]]; then
  echo "Found old context file: $OLD_CONTEXT"

  # Extract feature name from old context
  feature=$(grep -E "^\*\*Current Feature\*\*:|^\*\*Feature\*\*:" "$OLD_CONTEXT" | head -1 | cut -d: -f2 | tr -d ' ')

  if [[ -n "$feature" && -d "agent-docs/features/$feature" ]]; then
    NEW_CONTEXT="agent-docs/features/$feature/active-context.md"
    echo "Migrating to: $NEW_CONTEXT"

    # Move the file
    mv "$OLD_CONTEXT" "$NEW_CONTEXT"

    # Clean up old directory if empty
    rmdir agent-docs/current 2>/dev/null

    echo "Migration complete!"
    git add agent-docs/
    git commit -m "docs: migrate active-context to feature folder (v2.1)"
  else
    echo "Could not determine feature from old context. Manual migration needed."
    echo "1. Check which feature the context belongs to"
    echo "2. Move to: agent-docs/features/{feature}/active-context.md"
  fi
else
  echo "No old context file found. Already on v2.1 or fresh install."
fi
```

### Auto-Migration in Work Mode

When Work mode runs, it should check for and handle migration:

```bash
# In Work mode, before reading context:
feature="$SCOPE"  # Already detected from worktree
new_context="agent-docs/features/$feature/active-context.md"
old_context="agent-docs/current/active-context.md"

# Check if old context exists and references this feature
if [[ -f "$old_context" && ! -f "$new_context" ]]; then
  old_feature=$(grep "Feature" "$old_context" | head -1 | cut -d: -f2 | tr -d ' ')
  if [[ "$old_feature" == "$feature" ]]; then
    echo "Migrating context from v2.0 to v2.1..."
    mv "$old_context" "$new_context"
  fi
fi

# Now read the context
cat "$new_context"
```

---

## Session Lifecycle

```
1. SESSION START
   ↓
   [Script] rustie-session-start.sh → Fetch, show progress, warn issues
   [Script] rustie-context-update.sh start → Initialize active-context.md
   [Agent] Explore agent (v2.3) → Scan for changes since last session
   [Auto] NBA mode → Show priorities (enriched with change summary)
   ↓
2. SELECT WORK
   ↓
   [Auto] Validate mode → Check structure
   ↓
3. SPIKE (for new features - MANDATORY)
   ↓
   [Auto] If no assumptions.md exists:
   ├─ Extract technical assumptions from PRD/plan
   ├─ Run quick verification tests
   ├─ Create assumptions.md with results
   └─ If critical assumptions fail → revise plan before continuing
   ↓
4. WORK MODE
   ↓
   [Auto] Load feature context (checks assumptions.md first)
   ↓
5. IMPLEMENT (loop)
   ↓
   [Hook] Pre-commit hook → Block mixed commits (docs + code)
   [Manual] Mark checkboxes, commit after each task
   [Script] rustie-plan-status.sh → Check progress anytime
   ↓
   [EVERY RESPONSE] Stop hook checks context %
   ├─ < 70%  → Continue to step 6
   ├─ 70-84% → Warning displayed, continue or handoff
   └─ ≥ 85%  → Critical warning, should handoff → Go to step 8
   ↓
6. TEST (if UI changes)
   ↓
   [Auto-suggest] Test mode → Run Playwright
   ↓
7. LOOP BACK or HANDOFF
   ↓
   [Stop hook] Context still < 70%? → Loop back to step 5
   [Stop hook] Context ≥ 70%? → Proceed to step 8
   ↓
8. HANDOFF (when context ≥70% or natural breakpoint)
   ↓
   [Script] rustie-context-update.sh end → Record session summary
   [Auto] Handoff mode → Create handoff doc
   ↓
9. ARCHIVE (when feature 100%)
   ↓
   [Auto-suggest] Archive mode → Move to archives
   ↓
10. NEW SESSION
   ↓
   Next agent starts at step 1, reads handoff
```

**Key changes in v2.2**:
- Spike mode is MANDATORY for new features before implementation
- Context is checked after EVERY response via the stop hook

**Key changes in v2.3**:
- Explore agent at session start scans for changes since last session
- Parallel sub-agent spike testing for faster assumption validation
- LSP symbol grounding prevents hallucinated function/class names

---

## Explore Agent at Session Start (v2.3)

At the beginning of each session, launch an Explore agent to detect changes since the last session. This provides situational awareness and catches potential conflicts with existing assumptions.

### When to Run

- Every session start (after rustie-session-start.sh, before NBA mode)
- When resuming work after >24 hours
- When switching between features

### Explore Agent Prompt

```
Explore this codebase to identify changes since the last session:

1. Check git log for commits since {last_session_timestamp}
2. Look for new/modified dependencies in package.json
3. Identify API changes that might affect {feature} assumptions
4. Note any structural changes to key directories

Return a 3-5 bullet summary of relevant changes.
Focus only on changes that could affect current feature work.
```

### Integration with NBA Mode

The Explore agent's findings are incorporated into the NBA briefing:

```
RUSTIE [feature] NBA
─────────────────────────────────────────

CHANGES SINCE LAST SESSION:
• 3 commits to main (auth module refactored)
• New dependency: @auth/core@2.0.0
• API endpoint /users moved to /api/v2/users

Feature: [name]
Progress: X/Y tasks (Z%)
...
```

### Benefits

- **Early warning**: Catch breaking changes before they cause errors
- **Assumption refresh**: Identify when spike assumptions need re-validation
- **Context efficiency**: Only load relevant change information

---

## Stop Hook - Context Monitoring & Verification (v2.2)

The stop hook runs **after every Claude response** (not just at session end). It:
1. Checks context window usage (from status line data)
2. Signals when handoff is needed (>70% context used)
3. Runs Rustie Method verification (if agent-docs/ exists)

### How Context Monitoring Works

```
┌─────────────────┐     writes      ┌──────────────────────────┐
│  Status Line    │ ──────────────→ │ /tmp/claude-context-*.json │
│ (every update)  │                 │ {percent_used, remaining} │
└─────────────────┘                 └──────────────────────────┘
                                              │
                                              │ reads
                                              ▼
                                    ┌─────────────────┐
                                    │   Stop Hook     │
                                    │ (every response)│
                                    └─────────────────┘
                                              │
                              ┌───────────────┴───────────────┐
                              ▼                               ▼
                    context < 70%                    context >= 70%
                    Continue work                    Signal handoff needed
```

### Context Thresholds

| Threshold | Action |
|-----------|--------|
| **< 70%** | Continue normally |
| **70-84%** | Warning: "Consider creating handoff soon" |
| **≥ 85%** | Critical: "Create handoff NOW" |

### What It Checks (Verification)

| Category | Checks | Severity |
|----------|--------|----------|
| **Context Usage** | Percentage from status line | INFO/WARN |
| **Commit Discipline** | Mixed commits (docs + code), message prefixes | ERROR |
| **Context Management** | active-context.md exists, not stale, correct location | ERROR/WARN |
| **Plan Progress** | Status field, checkbox format | WARN |
| **Worktree Config** | worktrees.md exists, port assigned | WARN |
| **Structure Compliance** | Required files (PRD.md, plan.md) exist | ERROR |
| **Uncommitted Changes** | Uncommitted agent-docs or code | ERROR/WARN |

### Blocking Behavior

```
if not agent-docs/ exists → ALLOW (not a Rustie project)
if on main/master branch → ALLOW (dashboard mode)
if context >= 70% → ALLOW + signal handoff (never block when context high)
if errors > 0 → BLOCK
else → ALLOW
```

### Output Examples

**Normal operation (context low):**
```
{"decision": "allow", "context_percent": 45}
```

**Context getting high:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  CONTEXT HIGH (72%, 56k remaining) - Consider creating handoff soon
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{"decision": "allow", "context_percent": 72, "handoff_recommended": true, ...}
```

**Context critical:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  CONTEXT CRITICAL (88%, 24k remaining) - Create handoff NOW before context exhausted
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{"decision": "allow", "context_percent": 88, "handoff_recommended": true, ...}
```

**With verification errors:**
```
════════════════════════════════════════════════════════════
RUSTIE VERIFICATION REPORT
════════════════════════════════════════════════════════════
Feature: auth
Worktree: ./trustie-auth
Context High (>70%): No
────────────────────────────────────────────────────────────
Errors: 2  |  Warnings: 1

[ERROR] Commit Discipline: Mixed commit detected: abc123
[ERROR] Uncommitted Changes: 3 uncommitted agent-docs files
[WARN]  Context Management: Stale active-context.md (3h old)
════════════════════════════════════════════════════════════

{"decision": "block", "reason": "..."}
```

### Report Files

Verification reports are saved to:
```
agent-docs/features/{feature}/verify-reports/verify-{timestamp}.md
```

### Configuration

The stop hook is configured in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/scripts/claude-stop-with-verify 'Response complete'"
      }]
    }]
  }
}
```

Scripts location: `~/.claude/scripts/`
- `rustie-verify.py` - Main verification logic
- `claude-stop-with-verify` - Wrapper integrating with notification

---

## CLI Scripts (v2.2)

Standalone scripts provide reliable execution of Rustie Method tasks that previously relied on AI memory. These scripts can be run manually or integrated into hooks.

### Available Scripts

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `rustie-session-start.sh` | Session startup checks | Beginning of every Claude session |
| `rustie-plan-status.sh` | Show plan progress | Anytime during work |
| `rustie-context-update.sh` | Manage active-context.md | Session start/end |
| `rustie-pre-commit-hook.sh` | Block mixed commits | Automatic via git hook |
| `rustie-verify.py` | Session end verification | Automatic via stop hook |
| `rustie-install-hooks.sh` | Install hooks in a project | One-time setup |

### Script Details

#### rustie-session-start.sh

Run at the start of every Claude session. Provides:
- Worktree/feature detection
- `git fetch origin` to check for remote changes
- Plan progress summary (X/Y tasks, Z%)
- Next tasks from plan.md
- Warnings for stale context or pending changes

```bash
rustie-session-start.sh          # Human-readable output
rustie-session-start.sh --json   # JSON output for parsing
rustie-session-start.sh --quiet  # Silent (exit code only)
```

#### rustie-plan-status.sh

Display plan progress with visual feedback:

```bash
rustie-plan-status.sh              # Current feature (auto-detected)
rustie-plan-status.sh auth         # Specific feature
rustie-plan-status.sh --all        # Dashboard of all features
rustie-plan-status.sh --next 5     # Show next 5 tasks
rustie-plan-status.sh --json       # JSON output
```

Output includes:
- Progress bar
- Current phase
- Next N unchecked tasks
- Recently completed tasks

#### rustie-context-update.sh

Manage active-context.md reliably:

```bash
rustie-context-update.sh start   # Begin work session
rustie-context-update.sh end     # End session (prompts for summary)
rustie-context-update.sh touch   # Update timestamp only
rustie-context-update.sh show    # Display current context
rustie-context-update.sh check   # Verify context exists and is fresh
```

The `end` command:
- Calculates session duration
- Prompts for session summary
- Suggests handoff if session was long (>2h)
- Updates Recent Changes section

#### rustie-pre-commit-hook.sh

Git pre-commit hook that enforces commit discipline:
- Blocks commits that mix agent-docs/ with code files
- Provides clear instructions for splitting commits
- Only active in Rustie projects (with agent-docs/)

Install via:
```bash
rustie-install-hooks.sh          # Current repo
rustie-install-hooks.sh --global # Also copy scripts to ~/.local/bin
```

### Integration with Claude Code

For automatic script execution, configure Claude Code hooks:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Task|Bash|Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "rustie-context-update.sh touch 2>/dev/null || true"
      }]
    }]
  }
}
```

### Script vs AI Responsibility

| Task | Script (Reliable) | AI (Flexible) |
|------|-------------------|---------------|
| Detect context | `rustie-session-start.sh` | Work mode detection |
| Fetch origin | `rustie-session-start.sh` | Sync mode |
| Show progress | `rustie-plan-status.sh` | NBA/Status modes |
| Update context file | `rustie-context-update.sh` | Work/Handoff modes |
| Block mixed commits | Pre-commit hook | (was caught at end) |
| Session verification | `rustie-verify.py` | (stop hook) |
| Mark tasks done | (not scripted) | Manual during work |
| Create handoff doc | (not scripted) | Handoff mode |
| Decide next action | (not scripted) | NBA mode |

**Philosophy**: Scripts handle mechanical, easily-forgotten tasks. AI handles judgment calls and content creation.

---

## Manual Invocation

To manually invoke this skill:
- Say: "use rustie-method skill" or "run [mode] mode"
- Or: `/skill rustie-method` then specify mode
- Or: Natural language like "show my priorities", "create a handoff"
