---
name: task-startup
description: Comprehensive work session initialization orchestrator that validates environment, creates properly named branches, and prepares development environment for new tasks
category: productivity
version: 2.0.0
---

# Task-Startup Skill

**Comprehensive work session initialization orchestrator** for consistent and reliable task startup.

## Purpose

Automate session-start workflows by:
- Validating git status and working directory cleanliness
- Checking and auto-fixing development environment (Docker, database, dependencies)
- Creating properly named feature branches from develop
- Logging session start timestamps

## When to Use

Trigger this skill when:
- Starting a new development task or feature
- Beginning work on a new task
- Setting up environment for development session
- Need to ensure clean git state before starting work
- Keywords: "start task", "begin work", "new task", "startup task"

## Core Workflow

### Phase 1: Configuration Management

**Check for shared configuration file**:
1. Look for `.task_wrapup_skill_data.json` in current working directory
2. This file is shared with task-wrapup skill for consistency
3. If not found, create default configuration by prompting user for:
   - Project name
   - Default base branch (typically "development")
   - Docker configuration (enabled, services, health check URL)
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

### Phase 4: Task Name Resolution

**Determine task name to work on**:

**If user provides task name in initial prompt**:
- Use the user-provided task name directly
- Skip to Phase 5: Branch Creation

**If user does NOT provide task name in initial prompt**:
- Present menu of options:
  - **a) Specify task name**: User provides task name for branch creation
  - **b) Use default task name**: Use a generic timestamp-based name
  - **c) Skip task name**: Create branch without specific task name (uses "new-task")
- Wait for user selection before proceeding

**Task name formatting**:
- Should be concise and descriptive (e.g., "user-auth", "payment-api", "fix-login")
- Will be automatically sanitized (lowercase, hyphens for spaces)
- Max length: 30 characters (to keep branch names reasonable)

### Phase 5: Branch Creation

**Create feature branch** using `scripts/branch-create.sh`:

**Branch naming convention**:
- Pattern: `feature/{sanitized-task-name}`
- Max length: 50 characters
- Sanitization: lowercase, hyphens for spaces/special chars

**Examples**:
- Task name "user-auth": `feature/user-auth`
- Task name "Payment API": `feature/payment-api`
- Task name "Fix Dashboard Loading": `feature/fix-dashboard-loading`

**Execution**:
```bash
# With task name
scripts/branch-create.sh "user-auth"

# Without task name (uses default)
scripts/branch-create.sh
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
- Task name
- Session creation timestamp

**Important**: `.task_session_state.json` should be added to `.gitignore` as it contains local session state.

**Environment variables**:
- `BRANCH_PREFIX`: Branch prefix (default: "feature")
- `MAX_LENGTH`: Max branch name length (default: 50)
- `BASE_BRANCH`: Base branch to create from (default: "development")

### Phase 6: Session Initialization & OmniFocus Integration

**Automatic OmniFocus Task Creation** (if configured):

When OmniFocus integration is enabled, the skill automatically creates a task in OmniFocus to track your work session:

1. **Check Configuration**: Verifies `omnifocus.auto_log_tasks` is enabled and `omnifocus.project_name` is set
2. **Load Session State**: Reads `.task_session_state.json` for task context
3. **Create OmniFocus Task**: Executes `scripts/session-init.py` to create task via OmniFocus skill
4. **Store Task ID**: Saves OmniFocus task ID back to session state for later completion

**OmniFocus Task Details**:
- **Task Name**: `Work on: {task-name}` (e.g., "Work on: user-auth")
- **Project**: Configured OmniFocus project name
- **Notes**: Includes branch name, parent branch, timestamp, and session context
- **Purpose**: Tracks work sessions in OmniFocus for time management and task completion

**Execution** (automatic via skill):
```bash
python3 scripts/session-init.py --directory .
```

**Configuration Commands**:
```bash
# Set OmniFocus project for this directory
python3 scripts/config_manager.py set-omnifocus --omnifocus-project "Development"

# Get current OmniFocus project
python3 scripts/config_manager.py get-omnifocus

# Example output: Development
```

**Session State Integration**:
The OmniFocus task ID is stored in `.task_session_state.json`:
```json
{
  "task_name": "user-auth",
  "branch_name": "feature/user-auth",
  "parent_branch": "development",
  "created_at": "2025-01-15T14:30:22",
  "omnifocus_task_id": "abc123xyz",
  "omnifocus_created_at": "2025-01-15T14:30:25"
}
```

**Task Completion**: When you complete your work session using the task-wrapup skill, the OmniFocus task is automatically marked as complete using the stored task ID.

**Log session start** (traditional logging):
1. Record timestamp of session start
2. Record branch name created
3. Record task name
4. Store in session log (if configured)

**Session log structure** (if enabled):
```
.claude/sessions/2025-01-15-143022.md

# Session Start: 2025-01-15 14:30:22

**Branch**: feature/user-auth
**Task**: user-auth
**Started**: 2025-01-15 14:30:22
**OmniFocus Task**: abc123xyz
```

**Purpose**: Future time tracking, session analytics, work pattern analysis, OmniFocus task management integration

### Phase 7: Final Summary

**Display session initialization results**:
- ✅ Preflight checks passed
- ✅ Environment health validated (with auto-fixes applied)
- ✅ Task name: user-auth
- ✅ Branch created: feature/user-auth
- ✅ Session logged

**Ready to work**: Environment prepared and ready for task implementation

**Note**: The user is responsible for describing and coordinating the task implementation themselves.

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
      "max_length": 50
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
    }
  },

  "omnifocus": {
    "project_name": "Development",
    "auto_log_tasks": true,
    "prompt_if_missing": true
  },

  "summary_generation": { ... },
  "communication": { ... },
  "worklog": { ... },
  "documentation": { ... }
}
```

## Usage Examples

### Basic Usage - Start New Task with Name
```
User: "Start new task for user-auth"
```

The skill will:
1. Run preflight checks (git status, working directory)
2. Validate environment (Docker, DB, dependencies)
3. Extract task name "user-auth" from prompt
4. Create branch: `feature/user-auth`
5. Display ready-to-work confirmation

### Start Task - Prompt for Name
```
User: "Start task"
```

The skill will:
1. Run all validation checks
2. Prompt: "What is the task name?" with options:
   - a) Specify task name
   - b) Use default (timestamp-based)
   - c) Skip (uses "new-task")
3. Create branch from task name
4. Ready to work

### Start Task with Inline Name
```
User: "Startup task payment-api"
```

The skill will:
1. Complete all validation
2. Use "payment-api" as task name
3. Create branch: `feature/payment-api`
4. Display confirmation

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

## Integration with Other Skills

### Task-Wrapup Skill
- **Shared configuration**: Uses same `.task_wrapup_skill_data.json` file
- **Complementary workflow**: task-startup begins session, task-wrapup ends it
- **Session continuity**: Session logs can inform wrap-up summaries

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

# OmniFocus Integration
python3 scripts/config_manager.py set-omnifocus --omnifocus-project "Development" [--directory DIR]
python3 scripts/config_manager.py get-omnifocus [--directory DIR]
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

### scripts/branch-create.sh
**Purpose**: Consistent branch naming and creation

**Features**:
- Automatic name sanitization
- Length constraints (50 chars)
- Lowercase normalization
- Base branch switching

**Environment**: BRANCH_PREFIX, MAX_LENGTH, BASE_BRANCH

### scripts/session-init.py
**Purpose**: OmniFocus task creation during session initialization

**Features**:
- Automatic OmniFocus task creation for work sessions
- Integration with OmniFocus skill via omnifocus_manager.rb
- Reads configuration from .task_wrapup_skill_data.json
- Loads session state from .task_session_state.json
- Stores OmniFocus task ID back to session state
- Dry-run mode for testing without creating tasks

**CLI**:
```bash
# Create OmniFocus task automatically
python3 scripts/session-init.py --directory .

# Dry-run mode (test without creating)
python3 scripts/session-init.py --directory . --dry-run
```

**Requirements**:
- OmniFocus skill installed at ~/.claude/skills/omnifocus/
- OmniFocus project configured via config_manager.py
- Session state file exists (.task_session_state.json)

**Output** (JSON):
```json
{
  "status": "success",
  "message": "OmniFocus task created successfully",
  "task_id": "abc123xyz",
  "task_name": "Work on: user-auth",
  "project": "Development"
}
```

**Error Handling**:
- Skips if OmniFocus auto-logging disabled
- Prompts if project name not configured
- Reports errors if OmniFocus script fails
- Non-blocking: skill continues even if OmniFocus creation fails

## Best Practices

### Configuration Strategy
1. Create configuration once per project
2. Commit `.task_wrapup_skill_data.json` to version control if team-shared
3. Add to `.gitignore` if contains sensitive data
4. Update configuration as project needs evolve

### Workflow Integration
1. Always start tasks with this skill for consistency
2. Let auto-fix handle environment issues when safe
3. Use descriptive task names for clarity
4. User is responsible for task description and coordination

### Team Coordination
1. Establish team conventions for task naming
2. Use consistent base branch across team
3. Document protected branches in configuration
4. Share configuration file structure for new projects

## Future Enhancements

### Planned Features
- Team notification when starting tasks
- Time estimation integration
- Dependency auto-update option
- Multiple branch naming conventions
- Task tracking integration (Jira/Linear)

### Potential Improvements
- IDE integration for automatic environment setup
- Serena memory integration for context loading
- Task dependency checking
- Automated code review prep
- Integration with /sc:load for project context

---

**Author**: Claude Code SuperClaude Framework
**License**: MIT
**Repository**: ~/.claude/skills/task-startup/
**Version**: 2.0.0
