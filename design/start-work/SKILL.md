---
name: start-work
description: "/start-work - Begin Working on a GitHub Issue"
---

# /start-work - Begin Working on a GitHub Issue

Start work on a GitHub issue with proper environment setup, branch creation, and workflow enforcement.

## Usage

```
/start-work <issue-number>
```

## Arguments

- `issue-number` (required): The GitHub issue number to work on (e.g., `198`)

---

## Workflow Steps

Execute these steps in order. **STOP and report if any step fails.**

### Step 1: Pre-flight Checks

```bash
# Check for uncommitted changes
git status --porcelain
```

**If output is not empty:**
> "You have uncommitted changes. Please commit or stash them before starting new work."
> Show the uncommitted files and STOP.

**If clean:** Proceed.

### Step 2: Fetch GitHub Issue

```bash
gh issue view $ISSUE_NUMBER
```

**Extract from issue:**
- Title
- Labels (to determine: feature, bug, docs, etc.)
- Description/body

**Report to user:**
> "Starting work on #[number]: [title]"

### Step 3: Review Available MCP Tools

**BEFORE planning implementation, review available MCP servers and tools that might be useful for this issue.**

Use the `ListMcpResourcesTool` to see all available MCP servers and their capabilities:

```typescript
// Review all MCP servers
ListMcpResourcesTool({})
```

**Consider which tools might be relevant:**
- **Supabase MCP**: Database queries, migrations, logs, advisors
- **GitHub MCP**: Issue management, PR operations, code search
- **Context7 MCP**: Library documentation lookup (Next.js, Supabase, React, etc.)
- **Netlify MCP**: Deployment, forms, serverless functions
- **Fireflies MCP**: Meeting transcripts, user data
- **Claude in Chrome MCP**: Browser automation (if UI testing needed)

**Report to user:**
> "Available MCP tools reviewed. Relevant for this issue: [list applicable tools]"

### Step 4: Consider Subagent Usage

**CRITICAL: Assess whether specialized subagents would be advantageous for this issue.**

**Use subagents (Task tool) when:**
- Issue requires deep codebase exploration (use `explore` agent)
- Issue involves database schema changes (use `database-auditor` agent)
- Issue requires security review (use `review` agent)
- Issue is complex with multiple independent research tasks (use `general-purpose` agent)

**Recommended subagent strategy by issue type:**

| Issue Type | Recommended Subagents | Purpose |
|------------|----------------------|---------|
| Database refactoring | `database-auditor` | Analyze schema change risks |
| Complex features | `explore` + `Plan` | Explore codebase, design approach |
| Security-sensitive | `review` or `multi-tenant-security-auditor` | Audit for vulnerabilities |
| Large refactoring | `explore` + `general-purpose` | Map dependencies, plan phases |

**Report to user:**
> "Subagent assessment: [Will use X agent for Y task] or [No subagents needed - straightforward implementation]"

### Step 5: Parse Issue for Workflow Requirements

**CRITICAL: Scan the issue body for TDD requirements.**

**TDD is REQUIRED if the issue contains ANY of these patterns:**
- "TDD Required" or "TDD required"
- "Test-Driven Development Required"
- "Write tests FIRST"
- "test-driven-development skill"
- "RED" and "GREEN" in the context of testing workflow
- "Write failing test" or "failing test first"
- A "TDD Workflow" section
- References to the `test-driven-development` skill

**Set workflow flags:**
```
TDD_REQUIRED = true/false  (based on pattern detection)
UI_AFFECTED  = true/false  (based on pattern detection below)
```

**UI change detection — scan the issue for ANY of these signals:**
- Labels: `frontend`, `ui`, `ux`, `design`, `css`, `styling`, `component`, `layout`, `responsive`
- Title/body keywords: "button", "modal", "dialog", "form", "page", "layout", "style", "CSS", "Tailwind", "component", "responsive", "mobile", "animation", "theme", "color", "font", "icon", "image", "header", "footer", "sidebar", "navbar", "menu", "tooltip", "dropdown", "table", "card", "dashboard", "UI", "visual", "pixel", "spacing", "margin", "padding", "border", "shadow", "hover", "focus", "dark mode", "light mode"
- File paths referenced: `*.css`, `*.scss`, `*.tsx`, `*.jsx`, `components/`, `pages/`, `app/`, `styles/`, `public/`, `assets/`
- Any mention of visual changes, look-and-feel, or user-facing appearance

**If UI patterns detected:**
> "UI CHANGE DETECTED: This issue affects the user interface. Browser confirmation will be required before completion."

**If TDD patterns detected:**
> "TDD DETECTED: This issue explicitly requires Test-Driven Development."

### Step 6: Sync with Main

```bash
git checkout main
git pull origin main
```

**If conflicts or errors:** Report and STOP.

### Step 7: Create Feature Branch

**Determine branch type from issue labels:**
- `bug` label → `fix/`
- `documentation` label → `docs/`
- `enhancement` or `feature` label → `feature/`
- Default → `feature/`

**Create branch:**
```bash
# Format: <type>/<issue-number>-<short-description>
# Example: feature/198-email-reminders
git checkout -b <type>/<issue-number>-<kebab-case-description>
```

**Branch name rules:**
- Lowercase
- Kebab-case (hyphens)
- Include issue number
- Short but descriptive (3-5 words max)

### Step 8: Establish Baseline - Build

**Detect the project's build command.** Check for:
1. `package.json` in the project root or common subdirectories — use `npm run build`
2. `Makefile` — use `make build`
3. Other build systems as appropriate

```bash
# Run from the project root (or appropriate app directory)
npm run build
```

**If build fails:**
> "Build is failing on main. This is a pre-existing issue."
> Show errors and ask: "Continue anyway or fix first?"

**If build passes:** Record success.

**If no build system found:** Skip and note "No build step detected."

### Step 9: Establish Baseline - Tests

**Detect the project's test command.** Check for:
1. `package.json` with a `test` script — use `npm test`
2. `pytest.ini` or `pyproject.toml` — use `pytest`
3. Other test runners as appropriate

```bash
npm test 2>&1 | tail -20
```

**Record:**
- Number of passing tests
- Number of failing tests (if any)
- Note: Pre-existing failures are acceptable baseline

**If no test system found:** Skip and note "No test runner detected."

### Step 10: Report Ready State and Enforce Workflow

**If TDD_REQUIRED = true:**

```
============================================
TDD ENFORCEMENT ACTIVE
============================================

Issue:    #[number] - [title]
Branch:   [branch-name]
Base:     main @ [commit-hash]

Baseline Status:
  Build:  [PASS/FAIL/SKIPPED]
  Tests:  [X passing, Y failing / SKIPPED]

THIS ISSUE REQUIRES TEST-DRIVEN DEVELOPMENT

The issue explicitly requires TDD. You MUST:

1. Write a failing test FIRST (RED)
2. Watch the test fail
3. Write minimal code to pass (GREEN)
4. Refactor while keeping tests green
5. Repeat for each feature/behavior

DO NOT write implementation code before tests.
DO NOT skip the "watch it fail" step.

Invoking test-driven-development skill now...
============================================
```

**Then IMMEDIATELY invoke the `test-driven-development` skill.**

**After TDD skill completes, show issue details:**
```
Issue Details:
---
[Issue body/description]
---

Ready to begin TDD workflow. Start with your first failing test.
```

---

**If TDD_REQUIRED = false:**

```
============================================
READY TO START WORK
============================================

Issue:    #[number] - [title]
Branch:   [branch-name]
Base:     main @ [commit-hash]

Baseline Status:
  Build:  [PASS/FAIL/SKIPPED]
  Tests:  [X passing, Y failing / SKIPPED]

Next Steps:
1. Review the issue requirements below
2. Plan your implementation approach
3. Consider TDD for new features (recommended)
4. Implement the feature
5. If UI_AFFECTED: Confirm changes visually in the browser (see Step 11)
6. Run /ship-it when complete

Issue Details:
---
[Issue body/description]
---
============================================
```

### Step 11: Browser Confirmation for UI Changes

**This step is MANDATORY when `UI_AFFECTED = true`.** Do not skip it. Do not ship without it.

When implementation is complete and the dev server is running, use the Claude in Chrome browser tools to visually verify the changes:

1. **Get browser context:**
   - Call `tabs_context_mcp` to see current browser state
   - Navigate to the relevant page(s) using `navigate` or create a new tab with `tabs_create_mcp`

2. **Capture the current state:**
   - Use `read_page` to take a screenshot of each affected page/component
   - Show the screenshot to the user

3. **Confirm with the user:**
   > "Here's how the UI looks after the changes. Does this match what you expected?"

4. **If the user requests adjustments:**
   - Make the changes
   - Re-capture and re-confirm (repeat until approved)

5. **If the user approves:**
   > "UI confirmed. Ready to /ship-it."

**Rules:**
- NEVER skip browser confirmation when `UI_AFFECTED = true`, even if the code change seems trivial
- Check all relevant viewport sizes if the issue mentions responsive/mobile
- If the dev server is not running, start it before confirming
- If Chrome browser tools are unavailable, ask the user to manually verify and confirm before proceeding to /ship-it

---

## TDD Detection Patterns

The following patterns in the issue body trigger TDD enforcement:

| Pattern | Example |
|---------|---------|
| Explicit requirement | "TDD Required", "Test-Driven Development Required" |
| Skill reference | "invoke the `test-driven-development` skill" |
| Workflow markers | "RED:", "GREEN:", "REFACTOR:" in testing context |
| Process instructions | "Write tests FIRST", "Write failing test" |
| Section headers | "## TDD Workflow", "### TDD Workflow" |
| Critical markers | "CRITICAL: Test-Driven Development" |

**When in doubt, assume TDD is required for:**
- New features with business logic
- Bug fixes (prove the fix with a test)
- Database operations
- API endpoints

---

## Error Handling

| Error | Action |
|-------|--------|
| Uncommitted changes | STOP - user must commit/stash first |
| Issue not found | STOP - verify issue number |
| Git pull fails | STOP - report conflict |
| Build fails | WARN - note baseline, ask to continue |
| Tests fail | WARN - note baseline failures, continue |
| TDD required but skipped | BLOCK - do not allow implementation without TDD |
| UI affected but not confirmed | BLOCK - do not /ship-it without browser confirmation or explicit user approval |

---

## What This Command Does NOT Do

- Does not write any code
- Does not create worktrees (use `isolation: "worktree"` on the Task tool if workspace isolation is needed for parallel agents)
- Does not skip any verification steps
- Does not auto-commit anything
- Does not bypass TDD requirements when detected in issue
