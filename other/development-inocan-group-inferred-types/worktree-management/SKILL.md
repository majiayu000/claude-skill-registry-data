---
name: worktree-management
description: Automate Git worktree creation with isolated Docker services and browser automation for parallel Claude Code development sessions. This skill should be used when creating, managing, or removing Git worktrees for isolated development environments with automatic port allocation, environment file copying, and browser MCP isolation.
---

# Worktree Management Skill

## Purpose

This skill automates Git worktree creation and management for parallel development workflows. It provides isolated development environments with:

- Automatic Git worktree and branch creation
- Auto-incrementing port allocation for Docker services
- Isolated browser MCP servers (Playwright, Chrome DevTools, Puppeteer)
- Automatic `.env` file copying from main project
- Docker Compose configuration extension
- Worktree state tracking and lifecycle management
- Port conflict detection and resolution

## When to Use This Skill

Use this skill when:

- Creating isolated development environments for feature branches
- Running parallel development sessions without port conflicts
- Testing features independently with isolated Docker services
- Managing multiple worktrees across a project
- Cleaning up and removing worktrees safely

## Core Commands

### Create Worktree

```bash
@worktree create <name> [--branch=<branch-name>] [--start-services]
```

Creates a new Git worktree with isolated services. The process:

1. Validates worktree name and checks for conflicts
2. Allocates unique ports (auto-incremented from existing worktrees)
3. Creates Git worktree and branch
4. Copies `.env` files from main project (backend/.env, frontend/.env, .env)
5. **Configures CORS for worktree frontend port** - Updates both `backend/.env` ALLOWED_ORIGINS and `backend/config/initializers/cors.rb` to include the worktree's frontend port
6. Creates isolated browser data directory (`.browser-data/`)
7. Generates `.mcp.json` with browser isolation configuration
8. Generates `docker-compose.worktree.yml` extending main config
9. Creates `start-worktree.sh` startup script
10. **Updates `.gitignore` to exclude `.gitignore` and `.mcp.json` files** (prevents committing worktree-specific configs)
11. Updates worktree tracking registry
12. Optionally starts Docker services
13. Provides next-step instructions for Claude Code launch

**Examples:**
```bash
@worktree create feature-user-export
@worktree create bugfix-email --branch=bugfix/email-preview-fix
@worktree create docs-api --branch=docs/api-documentation --start-services
```

### List Worktrees

```bash
@worktree list [--status]
```

Shows all active worktrees with name, path, branch, allocated ports, Docker service status, and created timestamp.

### Switch to Worktree

```bash
@worktree switch <name>
```

Provides instructions to change directory, check service status, and launch Claude Code instance.

### Start/Stop Services

```bash
@worktree start <name>
@worktree stop <name>
```

Starts or stops Docker services for specified worktree.

### Remove Worktree

```bash
@worktree remove <name> [--delete-branch] [--force]
```

Safely removes worktree with cleanup:
1. Stops Docker services if running
2. Removes worktree directory
3. Optionally deletes Git branch
4. Frees allocated ports
5. Updates tracking registry

**Flags:**
- `--delete-branch`: Delete the Git branch after removal
- `--force`: Skip confirmation prompts

### Check Status

```bash
@worktree status <name>
```

Shows detailed status including Git branch/commit info, Docker service status, port allocations, and uncommitted changes warnings.

### Show Port Allocations

```bash
@worktree ports [<name>]
```

Shows port allocations for specific worktree or all worktrees.

### Sync from Main Branch

```bash
@worktree sync <name>
```

Updates worktree branch from development/main by fetching latest and rebasing.

## Implementation Details

### Port Allocation Strategy

**Auto-increment approach:**
- Scans existing worktrees for highest port numbers
- Increments by 1 for each new worktree
- Maintains port registry to prevent conflicts
- Intelligently scans up to 50 sequential ports to find available ones

**Port ranges:**
- Backend: 3000 (main), 3001+ (worktrees)
- Frontend: 4000 (main), 4001+ (worktrees)
- Database: 5433 (main), 5434+ (worktrees)
- Playwright: 9223 (main), 9224+ (worktrees)
- Chrome DevTools: 9222 (main), 9223+ (worktrees)
- Puppeteer: 9224 (main), 9225+ (worktrees)

**Port conflict prevention:**
- Pre-flight validation checks all ports before Docker startup
- Detects conflicts from main project, other worktrees, or system processes
- Provides detailed conflict report with resolution options
- Graceful degradation: worktree creation succeeds even with port conflicts (services startup deferred)

For detailed port allocation documentation, see `references/port-allocation.md`.

### Browser Isolation

Each worktree gets its own Docker-based browser automation services with complete isolation:

**Docker Services Created:**
- `chrome-devtools-mcp-{worktree-name}`: Headless Chrome for DevTools Protocol automation
- Each service uses a named Docker volume for persistent browser data
- Unique container names prevent conflicts between worktrees

**Chrome DevTools MCP Configuration:**
```yaml
chrome-devtools-mcp:
  container_name: chrome-devtools-mcp-{worktree-name}
  ports:
    - "{allocated-port}:9222"
  volumes:
    - chrome_devtools_data_{worktree-name}:/data
```

**MCP Server Configuration:**
Each worktree's `.mcp.json` is automatically configured to use its own Chrome DevTools container:
```json
{
  "chrome-devtools": {
    "command": "docker",
    "args": ["exec", "-i", "chrome-devtools-mcp-{worktree-name}", ...],
    "env": {
      "CHROME_USER_DATA_DIR": "/data",
      "CHROME_REMOTE_DEBUGGING_PORT": "9222"
    }
  }
}
```

**Benefits:**
- Run browser automation in multiple worktrees simultaneously
- Complete isolation of browser state, cookies, and sessions
- No container name conflicts - each worktree has unique container
- Independent debugging ports for each worktree
- Persistent browser data across container restarts

**Technical Details:**
- Internal port is always 9222 (Chrome debugging protocol standard)
- External port is auto-allocated (9222 for main, 9223+ for worktrees)
- Docker port mapping handles external isolation: `{external}:9222`
- Each worktree's Claude Code instance connects to its own container

For detailed browser isolation information, see `references/browser-isolation.md`.

### Docker Compose Strategy

Each worktree generates a standalone `docker-compose.worktree.yml` file (does NOT extend main docker-compose.yml).

**Services included:**
- `backend-{worktree-name}`: Rails API server with unique port
- `frontend-{worktree-name}`: React dev server with unique port
- `db-{worktree-name}`: PostgreSQL database with unique port
- `chrome-devtools-mcp-{worktree-name}`: Headless Chrome for browser automation
- `redis-{worktree-name}`: Redis (disabled by default for development)

**Key Features:**
- Each service has worktree-specific container name
- Unique port mappings prevent conflicts
- Named Docker volumes for data persistence
- Environment variables configured per worktree

**Usage:**
```bash
cd /path/to/worktree
docker-compose -f docker-compose.worktree.yml up
# Or use the convenience script:
./start-worktree.sh
```

For detailed Docker strategy documentation, see `references/docker-strategy.md`.

### Environment File Management

Automatically copies and configures environment files from main project to each worktree:
- `backend/.env` → Copied to worktree's backend directory (CORS configured)
- `frontend/.env` → Copied and **updated with worktree backend port**
- `frontend/.env.development` → Copied and **updated with worktree backend port**
- `.env` (root) → Copied to worktree root (ports updated)

**Critical Frontend Configuration:**
The skill automatically updates `VITE_API_BASE_URL` in both `frontend/.env` and `frontend/.env.development` to point to the worktree's backend port. This ensures proper frontend-backend isolation between worktrees.

Example:
- Main project: `VITE_API_BASE_URL=http://localhost:3000/api/v1`
- Worktree 1: `VITE_API_BASE_URL=http://localhost:3001/api/v1`
- Worktree 2: `VITE_API_BASE_URL=http://localhost:3002/api/v1`

This prevents Docker service startup failures due to missing gitignored files and ensures each worktree's frontend communicates with its own backend instance.

### CORS Configuration

**Automatic CORS setup for worktree frontend port:**

When creating a worktree, the skill automatically configures CORS to allow the worktree's frontend port:

1. **Updates `backend/.env`**: Adds the worktree frontend port (e.g., `http://localhost:4004`) to the `ALLOWED_ORIGINS` environment variable
2. **Updates `cors.rb`**: Adds the worktree frontend port to the development defaults array in `backend/config/initializers/cors.rb`

**Why this matters:**
- Prevents CORS errors when the frontend tries to communicate with the backend API
- Ensures login, API calls, and authentication work immediately without manual configuration
- Each worktree gets its frontend port automatically whitelisted

**Example:**
For a worktree with frontend port 4004, both files will include `http://localhost:4004`:
- `.env`: `ALLOWED_ORIGINS=http://localhost:4000,...,http://localhost:4004`
- `cors.rb`: `allowed_origins = ["http://localhost:4000", ..., "http://localhost:4004"]`

For detailed CORS configuration documentation, see `references/cors-configuration.md`.

### Worktree-Specific Git Configuration

Each worktree automatically configures its `.gitignore` to exclude worktree-specific files:
- `.gitignore` itself - Prevents worktree's customized gitignore from being committed
- `.mcp.json` - Prevents worktree's browser isolation config from being committed

**Purpose:**
- Keeps worktree-specific configurations isolated
- Prevents accidental merge of worktree configs back to main branch
- Maintains clean separation between worktree and main project settings

**Implementation:**
The skill appends these entries to the worktree's `.gitignore` during creation:
```
# Worktree-specific files (do not commit)
.gitignore
.mcp.json
```

### State Tracking

**Worktree Registry** (`worktrees.json`):
Tracks all worktrees with name, path, branch, creation timestamp, port allocations, status, and Docker service state.

**Port Registry** (`port-registry.json`):
Maintains allocated ports to prevent conflicts.

## Using the Skill

### Typical Development Workflow

```bash
# 1. Create worktree with services
@worktree create feature-auth --start-services

# 2. Switch to worktree (in new terminal)
cd /path/to/worktree
claude

# 3. Develop in isolated environment
# - Separate conversation history
# - Independent browser automation
# - No port conflicts

# 4. When done, merge back
cd /path/to/main/project
git checkout development
git merge feature/auth

# 5. Keep worktree for reuse or remove
@worktree remove feature-auth
```

### Accessing Bundled Resources

**Scripts** (`scripts/`):
- `worktree-manager.sh` - Main worktree management script with all commands

**Templates** (`assets/`):
- `docker-compose.worktree.template.yml` - Docker Compose extension template
- `mcp.template.json` - MCP configuration template with browser isolation
- `start-worktree.template.sh` - Service startup script template

**References** (`references/`):
- `port-allocation.md` - Detailed port allocation documentation
- `browser-isolation.md` - Browser MCP isolation details
- `docker-strategy.md` - Docker Compose extension pattern
- `cors-configuration.md` - CORS auto-configuration details
- `troubleshooting.md` - Common issues and solutions

**State Files** (skill root):
- `worktrees.json` - Worktree registry (auto-managed)
- `port-registry.json` - Port allocations (auto-managed)

To execute worktree commands, invoke the main script:
```bash
~/.claude/skills/worktree-management/scripts/worktree-manager.sh <command> [args]
```

## Best Practices

1. **Name worktrees descriptively**: Use clear names like `feature-auth`, `bugfix-email`, `docs-api`
2. **Use branch naming conventions**: Auto-converts `feature-auth` → `feature/auth`
3. **Verify `.env` files exist**: Ensure main project has `.env` files before creating worktrees
4. **Start services explicitly**: Use `--start-services` flag or run manually after resolving conflicts
5. **Stop services when done**: Free resources with `@worktree stop <name>`
6. **Sync regularly**: Stay updated with `@worktree sync <name>`
7. **Keep worktrees for reuse**: Don't remove unless completely done with feature
8. **Check status before merge**: View uncommitted changes with `@worktree status <name>`
9. **Browser isolation works automatically**: No manual configuration needed for parallel testing
10. **Worktree configs stay isolated**: `.gitignore` and `.mcp.json` automatically excluded from commits

## Safety Features

- Pre-creation validation (name conflicts, port availability)
- Pre-removal validation (uncommitted changes, running services)
- Rollback on failed operations
- Port registry prevents conflicts
- State tracking enables recovery
- Confirmation prompts for destructive operations
- Automatic `.env` file copying prevents Docker failures
- **Automatic CORS configuration prevents authentication and API errors**
- Browser isolation prevents session conflicts
- **Automatic `.gitignore` configuration prevents accidental commit of worktree-specific files**

## Limitations

- **Claude Code launch**: Instruction-based only (can't auto-launch new instance)
- **Manual cleanup**: Worktrees kept indefinitely (manual removal required)
- **No automatic sync**: Must manually sync from development branch
- **Port exhaustion**: No automatic cleanup of unused port allocations
- **`.env` file changes**: Updates to main project `.env` not auto-synced to worktrees

## Troubleshooting

For detailed troubleshooting guidance, see `references/troubleshooting.md`.

### Quick Solutions

**Port conflicts:**
```bash
@worktree ports                    # Check allocations
@worktree stop <name>             # Free ports
```

**Docker services won't start:**
```bash
# Stop main project services
cd /path/to/main/project
docker-compose down
```

**Missing `.env` files:**
```bash
# Copy manually if automatic copying failed
cp /path/to/main/backend/.env ./backend/.env
cp /path/to/main/frontend/.env ./frontend/.env
```

## Recent Bug Fixes

### Critical: Worktree Removal Bug (FIXED - 2025-10-22)

**Issue**: Removing a worktree accidentally removed ALL Docker containers, including main project containers.

**Root Cause**: Removal script used `docker-compose down` with both main and worktree compose files.

**Fix**: Removed `docker-compose down` command. Now uses only targeted container removal by name, which is safe and isolated.

**Impact**: No longer affects main project containers when removing worktrees.
