---
name: task-start
description: Comprehensive work session initialization orchestrator that validates environment, creates properly named branches, loads GitHub Issues, and prepares development environment for new tasks
category: productivity
version: 1.0.0
---

# Task-Start Skill

**Comprehensive work session initialization orchestrator** for consistent and reliable task startup.

## Purpose

Automate session-start workflows by:
- Validating git status and working directory cleanliness
- Checking and auto-fixing development environment (Docker, database, dependencies)
- Loading task information from GitHub Issues (highest priority or user-specified)
- Creating properly named feature branches from develop
- Logging session start timestamps
- Optionally invoking frontend-debug skill for GitHub Issue-based tasks

## When to Use

Trigger this skill when:
- Starting a new development task or feature
- Beginning work on a GitHub Issue
- Setting up environment for development session
- Need to ensure clean git state before starting work
- Keywords: "start task", "begin work", "new task", "start issue"

## Core Workflow

### Phase 1: Configuration Management

**Check for shared configuration file**:
1. Look for `.task_wrapup_skill_data.json` in current working directory
2. This file is shared with task-wrapup skill for consistency
3. If not found, create default configuration by prompting user for:
   - Project name
   - Default base branch (typically "development")
   - Docker configuration (enabled, services, health check URL)
   - GitHub integration settings
   - Environment validation preferences

**Configuration location**: `.task_wrapup_skill_data.json` in project root

**Manage configuration**:
```bash
# Create new config (interactive)
scripts/config_manager.py create

# Create with project name
scripts/config_manager.py create --project-name "MyProject"

# Show current config
scripts/config_manager.py show

# Validate config
scripts/config_manager.py validate

# Get config file path
scripts/config_manager.py path
```

### Phase 2: Preflight Validation

**Execute preflight checks** using `scripts/preflight-checks.sh`:

1. **Verify git repository**: Ensure current directory is a git repository
2. **Check current branch**: Get current branch name for validation
3. **Protected branch check**: Abort if on main/master/production branches
4. **Working directory status**: Check for uncommitted changes
5. **Stash detection**: Warn about stashed work that may need attention
6. **Base branch verification**: Confirm on development or prepare to switch

**Exit codes**:
- `0`: All checks passed
- `1`: On protected branch (cannot start task)
- `2`: Uncommitted changes detected
- `3`: Stashed work detected
- `4`: Not a git repository

**Behavior**:
- Abort if on protected branch
- Warn and prompt user if uncommitted changes or stashes exist
- Prepare to switch to base branch if needed

**Environment variables**:
- `BASE_BRANCH`: Default base branch (default: "development")
- `PROTECTED_BRANCHES`: Space-separated protected branches (default: "main master production")

### Phase 3: Environment Health Checks

**Execute environment validation** using `scripts/environment-health.sh`:

#### Docker Validation
- Check if Docker daemon is running
- Verify container status
- **Auto-fix**: Start Docker services if configured and not running
- Test health endpoint if specified in config
- Wait for services to become ready

#### Database Validation
- Check for pending migrations (Rails-specific)
- **Auto-fix**: Run migrations automatically if configured
- Verify database connectivity

#### Dependencies Validation
- Check npm/yarn packages for outdated versions
- Check Ruby gems (bundler) status
- Alert on missing or outdated dependencies
- **Note**: Does not auto-update, only alerts

#### Environment Variables
- Verify .env files exist (.env, .env.development)
- Check critical environment variables are defined
- Warn about missing required variables

**Auto-fix behavior**:
- Docker services: Auto-start if `DOCKER_AUTO_START=true`
- Database migrations: Auto-run if `AUTO_MIGRATE=true`
- Dependencies: Alert only, no auto-fix
- Environment variables: Alert only, no auto-fix

**Exit codes**:
- `0`: All checks passed or auto-fixed
- `10`: Docker not running (auto-fix failed or disabled)
- `11`: Database not ready
- `12`: Pending migrations (auto-migrate disabled)
- `13`: Dependencies outdated
- `14`: Environment variables missing

**Environment variables**:
- `DOCKER_ENABLED`: Enable Docker checks (default: "true")
- `DOCKER_AUTO_START`: Auto-start Docker if not running (default: "true")
- `DOCKER_HEALTH_URL`: Health endpoint to test (default: "http://localhost:3000/health")
- `CHECK_MIGRATIONS`: Enable migration checks (default: "true")
- `AUTO_MIGRATE`: Auto-run migrations (default: "true")
- `CHECK_DEPS`: Enable dependency checks (default: "true")

### Phase 4: Task Resolution & GitHub Integration

**Determine task to work on**:

**If user provides task in initial prompt**:
- Use the user-provided task description or issue number directly
- Skip to Phase 5: Branch Creation

**If user does NOT provide task in initial prompt**:
- Present menu of options:
  - **a) Specify task description**: User provides custom task description
  - **b) Specify GitHub Issue Number**: User enters specific issue number to work on
  - **c) Proceed with next most-critical outstanding GitHub Issue**: Auto-fetch highest priority open issue
- Wait for user selection before proceeding

**GitHub Issue fetching** using `scripts/github-issue-fetch.py`:

**Fetch specific issue**:
```bash
# By issue number
scripts/github-issue-fetch.py --issue 123

# With custom priority labels
scripts/github-issue-fetch.py --issue 123 --priority-labels critical high medium low

# JSON output
scripts/github-issue-fetch.py --issue 123 --format json
```

**Fetch highest priority issue**:
```bash
# Default priority order: urgent, high, medium, low
scripts/github-issue-fetch.py

# Custom priority order
scripts/github-issue-fetch.py --priority-labels critical blocker high

# JSON output for programmatic use
scripts/github-issue-fetch.py --format json
```

**Requirements**:
- GitHub CLI (`gh`) must be installed: `brew install gh`
- Must be authenticated: `gh auth login`
- Must be in a git repository with GitHub remote

**Issue data returned**:
```json
{
  "number": 123,
  "title": "Fix login button not responding",
  "body": "Description of the issue...",
  "labels": ["bug", "high", "frontend"],
  "state": "OPEN",
  "priority": "high"
}
```

**Display to user**:
- Show issue number and title
- Display priority level
- Show labels
- Display description (truncated if very long)
- Allow user to confirm or specify different task

### Phase 5: Branch Creation

**Create feature branch** using `scripts/branch-create.sh`:

**Branch naming convention**:
- Pattern: `feature/{issue-number}-{sanitized-description}`
- If no issue: `feature/{sanitized-description}`
- Max length: 50 characters
- Sanitization: lowercase, hyphens for spaces/special chars

**Examples**:
- With issue #123 "User Authentication": `feature/123-user-authentication`
- No issue "Password Reset": `feature/password-reset`
- Issue #456 "Fix Dashboard Loading Speed": `feature/456-fix-dashboard-loading-speed`

**Execution**:
```bash
# With task description only
scripts/branch-create.sh "user authentication"

# With GitHub issue number
scripts/branch-create.sh "user authentication" 123

# From GitHub issue object (automated)
scripts/branch-create.sh "$(echo $ISSUE_TITLE | head -c 30)" $ISSUE_NUMBER
```

**Behavior**:
1. Capture current branch as parent branch (for PR automation)
2. Switch to base branch (development) if not already there
3. Create new branch with sanitized name
4. Checkout new branch
5. Create session state file (`.task_session_state.json`) for PR automation
6. Display confirmation with branch name

**Session State File**:
The branch creation process automatically creates `.task_session_state.json` in the project root to enable automated pull request creation via the task-wrapup skill. This file tracks:
- Parent branch (for PR targeting)
- Feature branch name
- GitHub issue number and metadata (if available)
- Session creation timestamp

**Important**: `.task_session_state.json` should be added to `.gitignore` as it contains local session state.

**Environment variables**:
- `BRANCH_PREFIX`: Branch prefix (default: "feature")
- `MAX_LENGTH`: Max branch name length (default: 50)
- `BASE_BRANCH`: Base branch to create from (default: "development")

### Phase 6: Session Initialization

**Log session start**:
1. Record timestamp of session start
2. Record branch name created
3. Record task/issue reference
4. Store in session log (if configured)

**Session log structure** (if enabled):
```
.claude/sessions/2025-01-15-143022.md

# Session Start: 2025-01-15 14:30:22

**Branch**: feature/123-user-authentication
**Issue**: #123 - Fix login button not responding
**Priority**: high
**Started**: 2025-01-15 14:30:22
```

**Purpose**: Future time tracking, session analytics, work pattern analysis

### Phase 7: Frontend-Debug Skill Integration

**Invoke frontend-debug skill** (if applicable):

**Triggers**:
- Task is based on a GitHub Issue
- Issue has labels suggesting frontend work (bug, frontend, UI, etc.)
- Configuration enables auto-invoke (`integrations.frontend_debug_skill: true`)
- Configuration enables GitHub issue integration (`integrations.invoke_on_github_issue: true`)

**Invocation**:
```bash
# Pass issue number to frontend-debug skill
@~/.claude/skills/frontend-debug/SKILL.md --github-issue 123
```

**Behavior**:
- Frontend-debug skill loads issue details
- Begins systematic debugging workflow
- User continues with frontend-debug skill guidance
- Task-start skill completes successfully

**Note**: In the future, this will be replaced with a more general debugging skill that handles all issue types, not just frontend issues.

### Phase 8: Final Summary

**Display session initialization results**:
- ✅ Preflight checks passed
- ✅ Environment health validated (with auto-fixes applied)
- ✅ Task loaded: GitHub Issue #123 or user description
- ✅ Branch created: feature/123-user-authentication
- ✅ Session logged
- ✅ Frontend-debug skill invoked (if applicable)

**Ready to work**: Environment prepared and task context loaded

## Configuration Schema

Configuration shared with task-wrapup skill in `.task_wrapup_skill_data.json`:

```json
{
  "schema_version": "1.0",
  "project_name": "MyProject",
  "created_at": "2025-01-15T10:30:00",
  "last_updated": "2025-01-15T10:30:00",

  "task_start": {
    "default_base_branch": "development",
    "protected_branches": ["main", "master", "production"],

    "branch_naming": {
      "prefix": "feature",
      "include_issue_number": true,
      "max_length": 50
    },

    "github": {
      "enabled": true,
      "default_behavior": "prompt_user",
      "labels_priority_order": ["urgent", "high", "medium", "low"]
    },

    "environment": {
      "docker": {
        "enabled": true,
        "auto_start": true,
        "health_check_url": "http://localhost:3000/health",
        "services": ["backend", "frontend", "db"]
      },
      "database": {
        "check_migrations": true,
        "auto_migrate": true
      },
      "dependencies": {
        "check_updates": true,
        "package_managers": ["npm", "bundler"]
      },
      "env_files": {
        "required": [".env", ".env.development"],
        "critical_vars": ["DATABASE_URL", "SECRET_KEY_BASE"]
      }
    },

    "logging": {
      "session_logs_dir": ".claude/sessions",
      "track_start_time": true,
      "create_session_file": false
    },

    "integrations": {
      "frontend_debug_skill": true,
      "invoke_on_github_issue": true
    }
  },

  "summary_generation": { ... },
  "communication": { ... },
  "worklog": { ... },
  "documentation": { ... }
}
```

## Usage Examples

### Basic Usage - Start New Task
```
User: "Start new task for user authentication"
```

The skill will:
1. Run preflight checks (git status, working directory)
2. Validate environment (Docker, DB, dependencies)
3. Prompt for task description if not provided
4. Create branch: `feature/user-authentication`
5. Display ready-to-work confirmation

### Start Task with GitHub Issue Number
```
User: "Start task for issue #123"
```

The skill will:
1. Run all validation checks
2. Fetch GitHub Issue #123 details
3. Display issue summary for confirmation
4. Create branch: `feature/123-{sanitized-title}`
5. Invoke frontend-debug skill if issue is frontend-related

### Start Task - Highest Priority Issue
```
User: "Start next task"
```

The skill will:
1. Run validation checks
2. Fetch highest priority open GitHub Issue
3. Display issue for user confirmation
4. Create appropriately named branch
5. Proceed with skill integration if applicable

### Manual Task Description
```
User: "Start task"
```

If no GitHub Issue specified:
1. Complete all validation
2. Prompt: "What task are you starting?"
3. User provides description
4. Create branch from description
5. Ready to work

## Error Handling

### Preflight Failures

**Protected Branch Error**:
```
❌ Cannot start new task from protected branch: main
   New tasks must be started from development branch
```
**Action**: Switch to development manually or let skill switch automatically

**Uncommitted Changes**:
```
⚠️  Uncommitted changes detected:
 M backend/app/models/user.rb
 M frontend/src/components/Login.tsx

Please commit or stash changes before starting new task
```
**Action**: Commit changes or stash, then re-run skill

**Stashed Work**:
```
⚠️  3 stashed change(s) detected:
stash@{0}: WIP on feature/old-task: abc123 work in progress
stash@{1}: WIP on feature/another: def456 more work
stash@{2}: WIP on develop: ghi789 old stash

Consider applying or clearing stashes before starting new task
```
**Action**: Review and clear stashes, or continue with warning

### Environment Failures

**Docker Not Running**:
```
⚠️  No Docker containers running
🔄 Attempting to start Docker services...
✅ Docker services started
```
**Auto-fix**: Starts services automatically if enabled

**Pending Migrations**:
```
⚠️  5 pending migration(s) detected
🔄 Running migrations...
✅ Migrations complete
```
**Auto-fix**: Runs migrations automatically if enabled

**Outdated Dependencies**:
```
⚠️  12 outdated npm package(s)
   Run 'npm outdated' to see details
```
**Action**: User decides whether to update before proceeding

### GitHub Integration Failures

**GitHub CLI Not Installed**:
```
❌ GitHub CLI (gh) not installed or not authenticated
   Install: brew install gh
   Authenticate: gh auth login
```
**Fallback**: Prompt user for manual task description

**No Open Issues**:
```
⚠️  No open issues found
```
**Fallback**: Prompt user for manual task description

**Issue Closed**:
```
⚠️  Issue #123 is not open (state: CLOSED)
```
**Action**: User selects different issue or provides description

## Integration with Other Skills

### Task-Wrapup Skill
- **Shared configuration**: Uses same `.task_wrapup_skill_data.json` file
- **Complementary workflow**: task-start begins session, task-wrapup ends it
- **Session continuity**: Session logs can inform wrap-up summaries

### Frontend-Debug Skill
- **Auto-invocation**: Triggered for GitHub Issue-based frontend tasks
- **Issue context**: Passes issue number to debug skill
- **Seamless handoff**: User continues with debug workflow after initialization

### Contacts Skill
- **Future integration**: Potential for notifying team members when starting tasks
- **Not currently implemented**: Placeholder for future enhancement

## Bundled Scripts

### scripts/config_manager.py
**Purpose**: Manage shared configuration file

**Features**:
- Create new configuration (interactive or scripted)
- Load and validate existing configuration
- Compatible with task-wrapup skill configuration
- Schema validation and migration support

**CLI**:
```bash
python3 scripts/config_manager.py create [--project-name NAME] [--directory DIR]
python3 scripts/config_manager.py show [--directory DIR]
python3 scripts/config_manager.py validate [--directory DIR]
python3 scripts/config_manager.py path [--directory DIR]
```

### scripts/preflight-checks.sh
**Purpose**: Git and working directory validation

**Features**:
- Protected branch detection
- Working directory cleanliness check
- Stash detection and warning
- Base branch verification
- Non-destructive (read-only checks)

**Environment**: BASE_BRANCH, PROTECTED_BRANCHES

### scripts/environment-health.sh
**Purpose**: Development environment validation and auto-fixing

**Features**:
- Docker daemon and container checks with auto-start
- Database migration status with auto-migrate
- Dependency version checking (npm, bundler)
- Environment variable validation
- Intelligent auto-fix capabilities

**Environment**: DOCKER_ENABLED, DOCKER_AUTO_START, DOCKER_HEALTH_URL, CHECK_MIGRATIONS, AUTO_MIGRATE, CHECK_DEPS, CRITICAL_VARS

### scripts/github-issue-fetch.py
**Purpose**: GitHub Issue integration and priority detection

**Features**:
- Fetch specific issue by number
- Find highest priority open issue
- Priority detection from labels
- JSON and summary output formats
- GitHub CLI integration

**Requirements**: gh CLI installed and authenticated

### scripts/branch-create.sh
**Purpose**: Consistent branch naming and creation

**Features**:
- Automatic name sanitization
- Issue number integration
- Length constraints (50 chars)
- Lowercase normalization
- Base branch switching

**Environment**: BRANCH_PREFIX, MAX_LENGTH, BASE_BRANCH

## Best Practices

### Configuration Strategy
1. Create configuration once per project
2. Commit `.task_wrapup_skill_data.json` to version control if team-shared
3. Add to `.gitignore` if contains sensitive data
4. Update configuration as project needs evolve

### Workflow Integration
1. Always start tasks with this skill for consistency
2. Let auto-fix handle environment issues when safe
3. Review GitHub Issue before starting work
4. Use descriptive branch names even without issue numbers
5. Leverage frontend-debug skill integration for bug fixes

### Team Coordination
1. Establish team conventions for priority labels
2. Use consistent base branch across team
3. Document protected branches in configuration
4. Share configuration file structure for new projects

## Future Enhancements

### Planned Features
- General debugging skill integration (not just frontend)
- Team notification when starting tasks
- Time estimation integration
- Dependency auto-update option
- Multiple branch naming conventions
- Jira/Linear integration alongside GitHub

### Potential Improvements
- IDE integration for automatic environment setup
- Serena memory integration for context loading
- Task dependency checking
- Automated code review prep
- Integration with /sc:load for project context

---

**Author**: Claude Code SuperClaude Framework
**License**: MIT
**Repository**: ~/.claude/skills/task-start/
**Version**: 1.0.0
