---
name: omc-setup
description: Install or refresh oh-my-copilot for plugin, npm, and local-dev setups from the canonical setup flow
level: 2
---

# OMC Setup

This is the **only command you need to learn**. After running this, everything else is automatic.

**When this skill is invoked, immediately execute the workflow below. Do not only restate or summarize these instructions back to the user.**

Note: All `~/.claude/...` paths in this guide respect `COPILOT_HOME` when that environment variable is set.

## Best-Fit Use

Choose this setup flow when the user wants to **install, refresh, or repair OMC itself**.

- Marketplace/plugin install users should land here after `/plugin install oh-my-copilot`
- npm users should land here after `npm i -g oh-my-copilot@latest`
- local-dev and worktree users should land here after updating the checked-out repo and rerunning setup

## Flag Parsing

Check for flags in the user's invocation:
- `--help` → Show Help Text (below) and stop
- `--local` → Phase 1 only (target=local), then stop
- `--global` → Phase 1 only (target=global), then stop
- `--force` → Skip Pre-Setup Check, run full setup (Phase 1 → 2 → 3 → 4)
- No flags → Run Pre-Setup Check, then full setup if needed

## Help Text

When user runs with `--help`, display this and stop:

```
OMC Setup - Configure oh-my-copilot

USAGE:
  /oh-my-copilot:omc-setup           Run initial setup wizard (or update if already configured)
  /oh-my-copilot:omc-setup --local   Configure local project (.claude/CLAUDE.md)
  /oh-my-copilot:omc-setup --global  Configure global settings (~/.claude/CLAUDE.md)
  /oh-my-copilot:omc-setup --force   Force full setup wizard even if already configured
  /oh-my-copilot:omc-setup --help    Show this help

MODES:
  Initial Setup (no flags)
    - Interactive wizard for first-time setup
    - Configures CLAUDE.md (local or global)
    - Sets up HUD statusline
    - Checks for updates
    - Clears retired setup values (5.0.0 removed defaultExecutionMode) and points MCP registration at Claude Code's native config
    - Configures team mode defaults (agent count, type, model)
    - If already configured, offers quick update option

  Local Configuration (--local)
    - Invokes the plugin-local coordinator through `scripts/setup-claude-md.mjs`; the script validates the coordinator response and its exit status before any post-install work
    - Reports coordinator-created byte-identical backups only for files that required mutation
    - Project-specific settings
    - Use this to update project config after OMC upgrades

  Global Configuration (--global)
    - Invokes the plugin-local coordinator through `scripts/setup-claude-md.mjs`; the script validates the coordinator response and its exit status before any post-install work
    - Reports coordinator-created byte-identical backups only for changed global files
    - Default: explicitly overwrites ~/.claude/CLAUDE.md so plain `claude` also uses OMC
    - Optional preserve mode keeps the user's base `CLAUDE.md` and installs OMC into `CLAUDE-omc.md` for `omc` launches
    - Applies to all Claude Code sessions
    - Preserves same-named legacy hook files unless their exact historical contents are independently verified
    - Use this to update global config after OMC upgrades

  Force Full Setup (--force)
    - Bypasses the "already configured" check
    - Runs the complete setup wizard from scratch
    - Use when you want to reconfigure preferences

EXAMPLES:
  /oh-my-copilot:omc-setup           # First time setup (or update CLAUDE.md if configured)
  /oh-my-copilot:omc-setup --local   # Update this project
  /oh-my-copilot:omc-setup --global  # Update all projects
  /oh-my-copilot:omc-setup --force   # Re-run full setup wizard

For more info: https://github.com/Yeachan-Heo/oh-my-copilot
```


## Setup Invocation

Do not independently scan plugin cache directories or select a plugin root in this skill. Invoke the setup script from the plugin root supplied by the running plugin environment:

```bash
node "${OMC_SETUP_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/scripts/setup-claude-md.mjs" <local|global> [overwrite|preserve]
```

This runs unchanged on Windows, macOS, and Linux: it needs only Node, never bash or jq. (`scripts/setup-claude-md.sh` remains for back-compat with older invocations; the Node entry point above is the supported path.)

The script is the sole cache resolver. It accepts only complete plugin roots (canonical `docs/CLAUDE.md`, coordinator artifact, and `wiki` skill), chooses a strict full-SemVer cache version, verifies the compiled-source handshake, and fails closed on coordinator protocol or status disagreement. Do not download configuration or mutate `CLAUDE.md` outside that coordinator.

## Pre-Setup Check: Already Configured?

**CRITICAL**: Before doing anything else, check if setup has already been completed. This prevents users from having to re-run the full setup wizard after every update.

```bash
node -e "const p=require('path'),f=require('fs'),d=process.env.COPILOT_HOME||p.join(require('os').homedir(),'.copilot'),t=p.join(d,'.omc-config.json');if(f.existsSync(t)===false){console.log('ALREADY_CONFIGURED=false');process.exit(0)}let c;try{c=JSON.parse(f.readFileSync(t,'utf8'))}catch{console.error('ERROR: Existing OMC config is invalid JSON. Existing config was not modified.');process.exit(1)}if(c&&c.setupCompleted){console.log('OMC setup was already completed on: '+c.setupCompleted);if(c.setupVersion)console.log('Setup version: '+c.setupVersion);console.log('ALREADY_CONFIGURED=true')}else{console.log('ALREADY_CONFIGURED=false')}"
```

Treat `ALREADY_CONFIGURED=true` in the output as the configured case. A non-zero exit
means the existing config could not be parsed; stop and report that rather than
overwriting it.

### If Already Configured (and no --force flag)

If `ALREADY_CONFIGURED` is true AND the user did NOT pass `--force`, `--local`, or `--global` flags:

Use AskUserQuestion to prompt:

**Question:** "OMC is already configured. What would you like to do?"

**Options:**
1. **Update CLAUDE.md and clear retired setup values** - Install the active plugin's canonical CLAUDE.md and run Phase 2 Step 2.4 without re-running the full setup
2. **Run full setup again** - Go through the complete setup wizard
3. **Cancel** - Exit without changes

**If user chooses "Update CLAUDE.md and clear retired setup values":**
- Detect if local (.claude/CLAUDE.md) or global (~/.claude/CLAUDE.md) config exists
- If local exists, run: `node "${OMC_SETUP_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/scripts/setup-claude-md.mjs" local`
- If only global exists, run: `node "${OMC_SETUP_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/scripts/setup-claude-md.mjs" global`
- Run Phase 2 Step 2.4 to clear the retired `defaultExecutionMode` key
- Skip all other steps after the cleanup
- Report success and exit

**If user chooses "Run full setup again":**
- Continue with Resume Detection below

**If user chooses "Cancel":**
- Exit without any changes

### Force Flag Override

If user passes `--force` flag, skip this check and proceed directly to setup.

## Resume Detection

Before starting any phase, check for existing state:

```bash
node "${OMC_SETUP_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/scripts/setup-progress.mjs" resume
```

If state exists (output is not "fresh"), use AskUserQuestion to prompt:

**Question:** "Found a previous setup session. Would you like to resume or start fresh?"

**Options:**
1. **Resume from step $LAST_STEP** - Continue where you left off
2. **Start fresh** - Begin from the beginning (clears saved state)

If user chooses "Start fresh":
```bash
node "${OMC_SETUP_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/scripts/setup-progress.mjs" clear
```

## Phase Execution

### For `--local` or `--global` flags:
Read the file at `${OMC_SETUP_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/omc-setup/phases/01-install-claude-md.md` and follow its instructions.
(The phase file handles early exit for flag mode.)

### For full setup (default or --force):
Execute phases sequentially. For each phase, read the corresponding file and follow its instructions:

1. **Phase 1 - Install CLAUDE.md**: Read `${OMC_SETUP_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/omc-setup/phases/01-install-claude-md.md` and follow its instructions.

2. **Phase 2 - Environment Configuration**: Read `${OMC_SETUP_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/omc-setup/phases/02-configure.md` and follow its instructions. Phase 2 must delegate HUD/statusLine setup to the `hud` skill; do not generate or patch `statusLine` paths inline here.

3. **Phase 3 - Integration Setup**: Read `${OMC_SETUP_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/omc-setup/phases/03-integrations.md` and follow its instructions.

4. **Phase 4 - Completion**: Read `${OMC_SETUP_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/skills/omc-setup/phases/04-welcome.md` and follow its instructions.

## Graceful Interrupt Handling

**IMPORTANT**: This setup process saves progress after each phase via `${OMC_SETUP_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/scripts/setup-progress.mjs`. If interrupted (Ctrl+C or connection loss), the setup can resume from where it left off.

## Keeping Up to Date

After installing oh-my-copilot updates (via npm or plugin update):

**Automatic**: Just run `/oh-my-copilot:omc-setup` - it will detect you've already configured and offer a quick "Update CLAUDE.md and clear retired setup values" option that skips the rest of the wizard.

The quick update path must still perform Phase 2 Step 2.4 so upgrades remove the retired `defaultExecutionMode` value; it must not write any replacement execution-mode setting.

**Manual options**:
- `/oh-my-copilot:omc-setup --local` to update project config only
- `/oh-my-copilot:omc-setup --global` to update global config only
- `/oh-my-copilot:omc-setup --force` to re-run the full wizard (reconfigure preferences)

This ensures you have the newest features and agent configurations without the token cost of repeating the full setup.
