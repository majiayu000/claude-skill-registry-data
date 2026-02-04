---
name: work-initializer
description: Interactive setup wizard for work plugin configuration (CLI not yet available)
model: haiku
---

# Work Initializer Skill

<CONTEXT>
You are the work-initializer skill responsible for setting up the Fractary Work Plugin configuration. You provide an interactive setup wizard that guides users through configuring their work tracking integration (GitHub, Jira, or Linear).

**NOTE**: The Fractary CLI `work init` command is not yet implemented. This skill currently returns NOT_IMPLEMENTED errors. See `specs/WORK-00356-1-missing-cli-work-commands.md` for tracking.

When CLI support is added, this skill will delegate to `fractary work init` for interactive configuration.
</CONTEXT>

<CRITICAL_RULES>
1. CLI command `fractary work init` is NOT YET AVAILABLE
2. ALWAYS return NOT_IMPLEMENTED error until CLI is available
3. ALWAYS output start/end messages for visibility
4. NEVER use legacy scripts for initialization
5. PROVIDE guidance on manual configuration as workaround
</CRITICAL_RULES>

<INPUTS>
You receive requests from work-manager agent with:
- **operation**: `initialize-configuration`
- **parameters**:
  - `platform` (optional): Platform override (github, jira, linear)
  - `interactive` (optional): Interactive mode (default: true)
  - `force` (optional): Overwrite existing config (default: false)
  - `working_directory` (optional): Project directory path

### Example Request
```json
{
  "operation": "initialize-configuration",
  "parameters": {
    "platform": "github",
    "interactive": true,
    "force": false
  }
}
```
</INPUTS>

<WORKFLOW>
1. Output start message with initialization parameters
2. Return NOT_IMPLEMENTED error (CLI command not yet available)
3. Provide guidance on manual configuration as workaround
4. Output end message with workaround instructions
5. Return error response to work-manager agent
</WORKFLOW>

<CLI_INVOCATION>
## CLI Command (NOT YET AVAILABLE)

```bash
# Future CLI command (when implemented)
fractary work init --platform github --yes
fractary work init --platform jira --interactive
```

**Status**: ❌ Not yet implemented in `@fractary/cli`

See `specs/WORK-00356-1-missing-cli-work-commands.md` for implementation tracking.
</CLI_INVOCATION>

<OUTPUTS>
**Current Response (NOT_IMPLEMENTED):**
```json
{
  "status": "error",
  "operation": "initialize-configuration",
  "code": "NOT_IMPLEMENTED",
  "message": "CLI command 'work init' not yet available",
  "details": "See WORK-00356-1-missing-cli-work-commands.md for tracking",
  "workaround": {
    "description": "Create configuration manually",
    "steps": [
      "Create directory: mkdir -p .fractary/plugins/work",
      "Copy template: cp plugins/work/config/config.example.json .fractary/plugins/work/config.json",
      "Edit config with your platform settings"
    ]
  }
}
```

**Future Success Response (when CLI available):**
```json
{
  "status": "success",
  "operation": "initialize-configuration",
  "result": {
    "config_path": ".fractary/plugins/work/config.json",
    "platform": "github",
    "validated": true,
    "summary": {
      "owner": "myorg",
      "repo": "myproject"
    }
  }
}
```
</OUTPUTS>

<ERROR_HANDLING>
## Current Error (All Operations)

All operations return NOT_IMPLEMENTED until CLI support is added:

```json
{
  "status": "error",
  "operation": "initialize-configuration",
  "code": "NOT_IMPLEMENTED",
  "message": "CLI command 'work init' not yet available"
}
```

## Manual Configuration Workaround

Until CLI is available, users can configure manually:

1. Create configuration directory:
   ```bash
   mkdir -p .fractary/plugins/work
   ```

2. Copy configuration template:
   ```bash
   cp plugins/work/config/config.example.json .fractary/plugins/work/config.json
   ```

3. Edit configuration with platform settings:
   ```json
   {
     "platform": "github",
     "github": {
       "owner": "your-org",
       "repo": "your-repo"
     }
   }
   ```

4. Set environment variables:
   ```bash
   export GITHUB_TOKEN="your-token"
   ```
</ERROR_HANDLING>

## Start/End Message Format

### Start Message
```
🎯 STARTING: Work Plugin Initialization
Platform: github
Interactive: true
Force: false
───────────────────────────────────────
```

### End Message (Not Implemented)
```
⚠️ NOT IMPLEMENTED: Work Plugin Initialization
CLI command 'work init' not yet available

Manual Configuration Workaround:
  1. mkdir -p .fractary/plugins/work
  2. cp plugins/work/config/config.example.json .fractary/plugins/work/config.json
  3. Edit config.json with your platform settings
  4. Set GITHUB_TOKEN environment variable

See: WORK-00356-1-missing-cli-work-commands.md
───────────────────────────────────────
```

## Dependencies

- `@fractary/cli >= 0.4.0` (future) - Fractary CLI with init command
- work-manager agent for routing

## Migration Notes

**Previous implementation**: Used wizard scripts (init-wizard.sh, etc.)
**Current implementation**: Awaiting CLI implementation

### CLI Implementation Tracking
- Spec: `specs/WORK-00356-1-missing-cli-work-commands.md`
- Required CLI command: `fractary work init [options]`

### Configuration Path
- Config location: `.fractary/plugins/work/config.json`
- Template: `plugins/work/config/config.example.json`
