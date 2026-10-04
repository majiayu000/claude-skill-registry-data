---
name: project-contractor
description: Comprehensive codebase survey and understanding system that forces Claude to fully understand a project before making any changes. Use this skill BEFORE starting work on any new or existing project. Triggers on phrases like "start working on", "help me build", "continue the project", "fix my code", "add a feature", or when encountering an unfamiliar codebase. Employs parallel subagent analysis to survey all aspects of a project - architecture, connections, integrations, operations - and creates a living SOURCE-OF-TRUTH.md that becomes the canonical reference. PREVENTS assumptions and guessing. Claude must KNOW before it can DO.
---

# Project Contractor Skill

A contractor doesn't show up and start swinging a hammer. They survey the job site, understand the existing structure, trace the wiring, follow the plumbing, and ONLY THEN make a plan.

**This skill enforces that discipline for Claude Code.**

## The Core Rule

```
KNOW BEFORE YOU DO

Claude must demonstrate understanding before making changes.
If Claude doesn't know → Claude asks or surveys.
If Claude assumes → Claude is wrong.
```

## When This Skill Triggers

- Starting work on any project for the first time
- Returning to a project after context loss
- User says "help me with my project" without clear scope
- User requests changes to unfamiliar code
- Before any refactoring or restructuring
- Before adding features that touch multiple systems

## Phase 0: Pre-Flight Check

Before doing ANYTHING else:

```bash
# Check if we've already surveyed this project
if [ -f "SOURCE-OF-TRUTH.md" ]; then
    echo "SOURCE-OF-TRUTH.md exists - reading current state"
    # Read and validate the existing source of truth
else
    echo "No SOURCE-OF-TRUTH.md found - FULL SURVEY REQUIRED"
    # Trigger Phase 1
fi

# Check for existing CLAUDE.md
if [ -f "CLAUDE.md" ]; then
    echo "CLAUDE.md exists - reading project context"
fi
```

**Critical**: If SOURCE-OF-TRUTH.md exists but is outdated (user says things have changed), re-run the survey.

## Phase 1: The Complete Survey

### Orchestrator Responsibilities

The orchestrator (main Claude instance) MUST:
1. Create the survey workspace
2. Dispatch subagents for parallel analysis
3. Collect and synthesize subagent reports
4. Generate SOURCE-OF-TRUTH.md
5. Get user validation before proceeding

```bash
# Create survey workspace
mkdir -p .contractor-survey/{reports,evidence}
echo "Survey started: $(date)" > .contractor-survey/survey.log
```

### Subagent Deployment

Deploy these subagents in parallel. Each produces a structured report.

**SUBAGENT 1: Structure Mapper**
```
ROLE: Map the complete project structure
OUTPUT: .contractor-survey/reports/structure.md

TASKS:
1. Create complete directory tree (excluding node_modules, .git, dist)
2. Identify entry points (index.*, main.*, app.*, server.*)
3. Document the naming conventions used
4. Identify frameworks and major dependencies
5. Note any unusual or non-standard organization
6. Find all configuration files and their purposes

DELIVERABLE FORMAT:
# Structure Report

## Directory Tree
[tree output]

## Entry Points
- Frontend: [path]
- Backend: [path]
- Other: [list]

## Frameworks Detected
- [name]: [version] - [purpose]

## Configuration Files
| File | Purpose | Critical Settings |
|------|---------|-------------------|

## Non-Standard Patterns
- [description]
```

**SUBAGENT 2: Connection Tracer**
```
ROLE: Trace all connections and integrations
OUTPUT: .contractor-survey/reports/connections.md

TASKS:
1. Find all API endpoints (internal and external)
2. Identify database connections and schemas
3. Map WebSocket/real-time connections
4. Trace authentication flows
5. Document third-party service integrations
6. Find all environment variables and their purposes
7. Map inter-service communication patterns

DELIVERABLE FORMAT:
# Connection Report

## Internal APIs
| Endpoint | Method | Handler | Purpose |
|----------|--------|---------|---------|

## External APIs
| Service | Auth Method | Env Vars | Purpose |
|---------|-------------|----------|---------|

## Database Connections
- Type: [PostgreSQL/MongoDB/etc]
- Connection string var: [name]
- Schema location: [path]

## Real-Time Connections
- Protocol: [WebSocket/SSE/MQTT]
- Handler: [file:line]
- Events: [list]

## Environment Variables
| Variable | Purpose | Example | Required |
|----------|---------|---------|----------|
```

**SUBAGENT 3: Operations Validator**
```
ROLE: Validate and document all operational commands
OUTPUT: .contractor-survey/reports/operations.md

TASKS:
1. Find ALL ways to start development servers
2. Find ALL database migration methods
3. Find ALL deployment methods
4. Find ALL test commands
5. Find ALL build commands
6. TEST each command (dry-run if destructive)
7. Document which commands are CANONICAL (actually work)

DELIVERABLE FORMAT:
# Operations Report

## Development Server
CANONICAL COMMAND: [the one that actually works]
TESTED: [yes/no]
RESULT: [output summary]

Alternative methods found (may be outdated):
- [command] - Status: [works/broken/deprecated]

## Database Operations
CANONICAL MIGRATION: [command]
CANONICAL SEED: [command]
Schema location: [path]

## Deployment
CANONICAL DEPLOY: [command or process]
CI/CD: [yes/no - describe]
Manual steps required: [list]

## Testing
CANONICAL TEST: [command]
Coverage: [percentage if available]

## Build
CANONICAL BUILD: [command]
Output location: [path]
```

**SUBAGENT 4: State Analyzer**
```
ROLE: Understand current project state and history
OUTPUT: .contractor-survey/reports/state.md

TASKS:
1. Check git status and recent commits
2. Identify active branches and their purposes
3. Find open issues/todos in code
4. Check for existing documentation and its accuracy
5. Identify any broken or deprecated code
6. Find all TODO/FIXME/HACK comments
7. Assess test coverage and health

DELIVERABLE FORMAT:
# State Report

## Git Status
Current branch: [name]
Uncommitted changes: [yes/no - summary]
Recent commits (last 5):
- [hash] [message] [date]

## Active Branches
| Branch | Purpose | Last Commit |
|--------|---------|-------------|

## Code Health
TODOs found: [count]
FIXMEs found: [count]
HACKs found: [count]
Critical issues: [list]

## Documentation Accuracy
| Doc File | Accurate | Issues |
|----------|----------|--------|

## Test Health
Test coverage: [percentage]
Failing tests: [count]
Skipped tests: [count]
```

**SUBAGENT 5: Dependency Auditor**
```
ROLE: Audit all dependencies and their relationships
OUTPUT: .contractor-survey/reports/dependencies.md

TASKS:
1. List all production dependencies
2. List all dev dependencies
3. Check for unused dependencies
4. Check for outdated dependencies
5. Check for security vulnerabilities
6. Identify circular dependencies
7. Document critical dependencies that everything depends on

DELIVERABLE FORMAT:
# Dependencies Report

## Critical Dependencies
[These are core to the application - breaking changes here break everything]
- [package]: [purpose]

## Production Dependencies
| Package | Version | Purpose | Outdated |
|---------|---------|---------|----------|

## Dev Dependencies
| Package | Version | Purpose |
|---------|---------|---------|

## Issues Found
- Unused: [list]
- Vulnerable: [list]
- Circular: [list]
```

## Phase 2: Synthesis

After all subagents complete, the orchestrator synthesizes their reports into **SOURCE-OF-TRUTH.md**:

```markdown
# SOURCE OF TRUTH

Generated: [timestamp]
Project: [name]
Last validated: [timestamp]

## Quick Reference

### Start Development
```bash
[CANONICAL COMMAND FROM OPERATIONS REPORT]
```

### Database Migration
```bash
[CANONICAL COMMAND]
```

### Deploy to Production
```bash
[CANONICAL COMMAND or PROCESS]
```

### Run Tests
```bash
[CANONICAL COMMAND]
```

## Architecture Overview

[Synthesized from Structure + Connections reports]

### Frontend
- Framework: [name]
- Entry: [path]
- Key directories: [list]

### Backend
- Framework: [name]  
- Entry: [path]
- Key directories: [list]

### Database
- Type: [name]
- Connection: [env var]
- Schema: [path]

## External Integrations

[From Connections report]

| Service | Purpose | Auth | Env Vars |
|---------|---------|------|----------|

## Environment Variables Required

[Consolidated from all reports]

| Variable | Purpose | Example | Where Used |
|----------|---------|---------|------------|

## Known Issues

[From State report]

## Files Claude Must Not Touch Without Asking

[Critical files that could break everything]
- [path]: [reason]

## Assumptions Log

[Start empty - Claude adds here when it makes ANY assumption]

---
VALIDATION STATUS: [PENDING USER VALIDATION]
User validated: [no]
```

## Phase 3: User Validation

**CRITICAL**: Before proceeding with ANY work, Claude must:

1. Present the SOURCE-OF-TRUTH.md to the user
2. Ask: "Does this accurately reflect your project? Any corrections?"
3. Update based on user feedback
4. Get explicit "yes, proceed" before continuing

```markdown
I've completed the project survey. Here's what I understand:

[Summary of key findings]

**Before I do anything else, I need you to validate this:**

1. Are the canonical commands correct?
2. Are there any integrations I missed?
3. Are there any files I should never touch?
4. Anything else I got wrong?

Once you confirm, I'll update SOURCE-OF-TRUTH.md and we can proceed.
```

## The Assumptions Log

Every time Claude makes an assumption (no matter how small), it MUST be logged:

```markdown
## Assumptions Log

| Date | Assumption | Basis | Verified |
|------|------------|-------|----------|
| 2024-01-15 | Component uses React hooks | Saw useState import | Yes |
| 2024-01-15 | API uses REST not GraphQL | Found express routes | No - ASK USER |
```

If an assumption cannot be verified from code:
1. Log it as unverified
2. ASK THE USER before proceeding
3. Update log with answer

## Rules of Engagement

### Claude MUST:

1. **Read before writing** - Never modify a file without reading it first
2. **Survey before changing** - Run Phase 1 before any significant work
3. **Ask before assuming** - If it's not in SOURCE-OF-TRUTH.md, ask
4. **Verify before claiming** - Test commands actually work
5. **Update the truth** - Keep SOURCE-OF-TRUTH.md current

### Claude MUST NOT:

1. **Restructure without asking** - User's structure is intentional
2. **Add unrequested features** - No bathrooms they didn't ask for
3. **Assume conventions** - This project may not follow standards
4. **Skip the survey** - Even for "simple" changes
5. **Trust outdated docs** - Verify everything

### When Claude Doesn't Know:

```markdown
STOP. I don't have enough information to proceed safely.

I need to know:
- [specific question 1]
- [specific question 2]

Without this, I would be guessing, and guessing breaks things.
```

## Maintaining the Source of Truth

After every significant change:

```bash
# Update SOURCE-OF-TRUTH.md
echo "Last updated: $(date)" >> SOURCE-OF-TRUTH.md

# Log what changed
echo "- [description of change]" >> SOURCE-OF-TRUTH.md
```

## Emergency Stop

If Claude realizes it's been making assumptions:

```markdown
STOP. I need to pause.

I just realized I've been assuming [X] without verification.
Before I continue, I need to:
1. Check if my assumption was correct
2. Update SOURCE-OF-TRUTH.md
3. Verify no damage was done

Let me survey the affected areas first.
```

## Quick Commands Reference

These can be used as slash commands or explicit requests:

- `/survey` - Run full Phase 1 survey
- `/verify [topic]` - Verify specific information
- `/truth` - Display current SOURCE-OF-TRUTH.md
- `/assume` - Show all logged assumptions
- `/stop` - Emergency halt - something seems wrong

## References

See reference files for specific patterns:
- references/survey-prompts.md - Detailed prompts for each subagent
- references/synthesis-template.md - Complete SOURCE-OF-TRUTH template
- references/red-flags.md - Signs Claude is about to make a mistake
