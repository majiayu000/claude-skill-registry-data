---
name: macos-launchd-service
description: Set up macOS launchd service for auto-starting Python applications
allowed-tools: Read, Write, Bash, Glob
---

# macOS launchd Service Setup

Generate complete launchd service infrastructure for Python applications on macOS.

## What This Skill Creates

```
launchd/
├── install.sh                          # Automated service installer
├── uninstall.sh                        # Service uninstaller
├── {project}.plist.template           # Service configuration
dev.sh                                  # Development mode script
view-logs.sh                           # Log viewing helper
```

## When to Use This Skill

- **Web services**: FastAPI, Flask apps that should auto-start
- **Background services**: Daemons, periodic tasks
- **Development servers**: Local services you want always running

## Before Running

**Requirements**:

- macOS 10.10+ with launchd
- Python project with uv and .venv
- `pyproject.toml` with `[project.scripts]` defining a CLI command

**Check pyproject.toml**:

```toml
[project.scripts]
yourapp = "yourapp.cli:main"
```

**IMPORTANT - Replacing Existing Setup**:

If the project already has launchd/ directory or existing scripts:
- **ALWAYS use the parameters provided by the user**
- **DO NOT read values from existing files**
- The user wants to replace with NEW values, not keep old ones
- Overwrite existing files with the new parameter values

## Step-by-Step Process

### 1. Gather Information from User

**Ask the user for these parameters** (use AskUserQuestion if needed):

- **Domain** (e.g., "dev.pborenstein", "com.pborenstein") - Reverse domain notation for service label
  - Default suggestion: `dev.{username}` (e.g., "dev.philip")
  - Best practice: Use owned domain (e.g., "dev.pborenstein" if you own pborenstein.dev)
- **Project name** (e.g., "temoa", "apantli") - lowercase, no spaces
- **Module name** (e.g., "temoa", "apantli") - Python import name
- **Port number** (e.g., 4001, 4000) - unique port for this service
- **CLI command** (e.g., "temoa server", "python3 -m apantli.server")
- **Dev command** (e.g., "temoa server --reload", "python3 -m apantli.server --reload")
- **Process name** (e.g., "temoa server", "apantli.server") - for detecting running processes

**Use these exact values provided by the user** - do not infer from existing files.

### 2. Suggest Defaults from pyproject.toml (Optional)

Only if the user hasn't provided values, you may suggest defaults from `pyproject.toml`:

```bash
# Suggest project name
grep "^name" pyproject.toml

# Suggest CLI command from [project.scripts]
grep -A 5 "\[project.scripts\]" pyproject.toml
```

**But always use what the user explicitly provides.**

### 3. Generate launchd Directory

Create `launchd/` directory:

```bash
mkdir -p launchd
```

### 4. Generate Files from Templates

For each template in `skills/macos-launchd-service/templates/`, perform substitutions:

**Substitution variables**:

User-provided parameters (use values from step 1):
- `{{DOMAIN}}` - Reverse domain notation (e.g., "dev.pborenstein", "com.pborenstein")
- `{{PROJECT_NAME}}` - Project name (e.g., "temoa")
- `{{MODULE_NAME}}` - Python module name for import check
- `{{PORT}}` - Port number
- `{{CLI_COMMAND}}` - Full CLI command as plist array elements
- `{{DEV_COMMAND}}` - Development mode command
- `{{PROCESS_NAME}}` - Process name for pkill/pgrep

Auto-detected variables (these are filled in by install.sh at runtime):
- `{{HOME}}` - User's home directory
- `{{PROJECT_DIR}}` - Absolute path to project directory
- `{{VENV_PYTHON}}` - Path to venv Python interpreter
- `{{VENV_BIN}}` - Path to venv bin directory

**CLI_COMMAND special handling**:

Must be converted to plist array format:

```
Input: "temoa server --host 0.0.0.0 --port 4001"

Output:
        <string>{{VENV_BIN}}/temoa</string>
        <string>server</string>
        <string>--host</string>
        <string>0.0.0.0</string>
        <string>--port</string>
        <string>4001</string>
```

### 5. Generated Files

**install.sh** (from `install.sh.template`):

- Auto-detects environment (username, paths, venv)
- Validates venv and module are installed
- Generates service plist from template
- Installs and loads service
- Shows access information and management commands

**uninstall.sh** (from `uninstall.sh.template`):

- Checks if service exists
- Shows what will be removed
- Asks for confirmation
- Stops running service
- Removes plist file
- Confirms uninstall complete

**{project}.plist.template** (from `service.plist.template`):

- Service configuration with substitution placeholders
- Used by install.sh to generate final plist
- Configured with RunAtLoad, KeepAlive for production

**dev.sh** (from `dev.sh.template`):

- Stops launchd service if running
- Runs app with auto-reload for development
- Uses caffeinate to prevent sleep
- Offers to restore service on exit

**view-logs.sh** (from `view-logs.sh.template`):

- Modes: app logs, errors, or all
- Uses tail -f for live viewing
- Logs location: `~/Library/Logs/{project}.log`

### 6. Make Scripts Executable

```bash
chmod +x launchd/install.sh
chmod +x launchd/uninstall.sh
chmod +x dev.sh
chmod +x view-logs.sh
```

### 7. Provide Next Steps

After generation, tell the user:

```
✓ Generated launchd service structure

Next steps:
1. Review generated files in launchd/
2. Run: ./launchd/install.sh
3. Access your service at: http://localhost:{PORT}
4. View logs: ./view-logs.sh
5. Development mode: ./dev.sh

Service will auto-start on login and auto-restart on crash.

Manage service:
  Stop:    launchctl unload ~/Library/LaunchAgents/{DOMAIN}.{project}.plist
  Start:   launchctl load ~/Library/LaunchAgents/{DOMAIN}.{project}.plist
  Status:  launchctl list | grep {project}
```

## Example: temoa

**Input parameters**:

- Domain: dev.pborenstein
- Project name: temoa
- Module name: temoa
- Port: 4001
- CLI command: temoa server --host 0.0.0.0 --port 4001 --log-level info
- Dev command: temoa server --reload
- Process name: temoa server

**Generated CLI_COMMAND for plist**:

```xml
    <array>
        <string>{{VENV_BIN}}/temoa</string>
        <string>server</string>
        <string>--host</string>
        <string>0.0.0.0</string>
        <string>--port</string>
        <string>4001</string>
        <string>--log-level</string>
        <string>info</string>
    </array>
```

## Implementation Notes

**Reading templates**:

Templates are in `skills/macos-launchd-service/templates/`:

- `install.sh.template`
- `uninstall.sh.template`
- `service.plist.template`
- `dev.sh.template`
- `view-logs.sh.template`

**Writing generated files**:

- `launchd/install.sh`
- `launchd/uninstall.sh`
- `launchd/{PROJECT_NAME}.plist.template`
- `dev.sh`
- `view-logs.sh`

**String substitution**:

Simple replace all instances of each `{{VARIABLE}}` with its value.

**CLI_COMMAND conversion**:

Split on spaces, wrap each token in `        <string>TOKEN</string>` with proper indentation.

## Validation

After generation, verify:

- All 5 files created (install.sh, uninstall.sh, plist.template, dev.sh, view-logs.sh)
- Scripts are executable
- No leftover `{{VARIABLES}}` in files
- CLI_COMMAND properly formatted as plist array

## Common Issues

**Port conflicts**: Use `lsof -i :{PORT}` to check if port is available

**Module not found**: User needs to run `uv sync` first

**Permission errors**: Ensure `~/Library/LaunchAgents` exists

## See Also

- [README.md](README.md) - Detailed usage guide
- Example implementations: temoa, apantli in nahuatl-projects
