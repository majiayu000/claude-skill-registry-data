---
name: configure-grimoire
description: Use when the user wants to view, edit, remove, or validate their grimoire settings — including reading current preferences, changing or deleting a setting, switching a named profile, or checking grimoire.toml for contradictions and expired entries.
source: Settings management patterns (VS Code settings UI, Git config get/set/unset); XDG Base Directory Specification (freedesktop.org)
tags: [settings, configuration, preferences, profile, toml, view, edit, validate]
---

# Configure Grimoire

Read, update, or validate `grimoire.toml` — the single source of truth for all grimoire preferences and configuration.

## Why This Is Best Practice

**Adopted by:** Every major developer tool provides a guided settings interface alongside raw file editing — VS Code `settings.json` + Settings UI, Git `git config get/set/unset`, npm `.npmrc` + `npm config`. Guided operations prevent syntax errors and silent overwrites that raw editing can introduce.
**Impact:** Configuration drift — where users forget what they set, or stale settings silently govern behavior — is one of the primary causes of "why is it doing that?" confusion. VS Code's settings validation (invalid key detection) reduced user-reported configuration bugs by catching errors at write time rather than at apply time. Explicit confirmation before destructive operations (delete, overwrite) is standard across all major CLI tools (`git config --unset`, `npm config delete`).
**Why best:** Manual TOML editing is error-prone (syntax, wrong key names, stale dates). A guided interface validates before writing, confirms before deleting, and surfaces the full settings cascade so the user knows which file actually governs a domain.

Sources: XDG Base Directory Specification (freedesktop.org); VS Code settings documentation; Git config documentation (`git help config`)

## Steps

**Platform-aware prompts:** Claude Code → `AskUserQuestion`; OpenCode → `question` (same schema); Gemini CLI → `ask_user`; all other platforms → the inline `[y/n]`/numbered-list block shown at each step. Steps below say "platform-aware confirm/select" and give only the "other platforms" content, since that's what differs per step.

### Step 1: Detect operation

| User signal | Operation |
|-------------|-----------|
| "show", "view", "what are my settings for X", "list my preferences" | `show` |
| "edit", "update", "change", "set X to Y" | `edit` |
| "remove", "delete", "unset", "clear" | `remove` |
| "add to", "append to", "add a profile", "add X to profiles/practices/disabled" | `config-add` |
| "remove from", "drop from", "remove from profiles/practices/disabled" | `config-remove` |
| "switch to X profile", "use X profile", "activate profile" | `switch-profile` |
| "show context", "full state", "what's my setup", "grimoire context" | `context` |
| "set up MCP", "configure Claude Code", "add grimoire to AI assistant", "MCP config" | `mcp-setup` |
| "validate", "check settings", "any issues" | `validate` |
| "configure check provider", "set AI for check", "check via X", "grimoire check provider" | `check-provider` |
| "show status", "project health", "compliance health" | run `grimoire status` directly |
| "add package", "remove package", "list packages", "manage skill sources" | route to `install-grimoire` |

---

### Step 2: Load settings

**Grimoire-first (preferred):** If grimoire CLI is available, run `grimoire context` (human) or `grimoire settings` for the merged view with per-field source attribution. `grimoire settings` shows section headers (`[standards]`, `[standards.X]`) with active profiles automatically expanded to their resolved skill lists — no manual layer merging or profile resolution needed.

**Fallback (grimoire not installed):** Resolve the active settings by merging in order (highest wins):

```
<project>/grimoire.toml   (local — committed, --local)
  > ~/.config/grimoire/grimoire.toml (global — XDG primary, --global)
    > /etc/grimoire/grimoire.toml    (system — machine-wide, --system)
```

Within any file, cascade by specificity: `[standards.domain.subdomain] > [standards.domain]` — a subdomain section overrides its parent domain section for the same key; unset keys inherit from the domain level.

---

### Step 3a: Show

Display the merged effective settings for the requested domain (or all domains):

```
Effective settings for engineering/architecture:
  Source: grimoire.toml (project)

  practices: ["SOLID principles: production code", "KISS: scripts, prototypes"]
  fallback:  "ask"
  author:    "@backend-team"
  note:      "agreed in ADR-014"
  expires:   "2026-09-01"

  Active profile: (none — using default)
  Overrides from: (no global entry for this domain)
```

Show which file each key came from if multiple files contribute.

---

### Step 3b: Edit

**TOML parse guard:** If the target settings file exists but cannot be parsed as valid TOML (syntax error), stop immediately. Output: 'Settings file at [path] has a syntax error — cannot edit safely. Fix the TOML syntax first (e.g., unclosed quote, missing `=`, invalid array). Inspect with: `cat [path]`.' Do not overwrite a malformed file.

Parse the requested change from user input. Show what will change, then ask which file to write to (platform-aware select — see Steps intro). Options: "This project (local) → grimoire.toml (Recommended)", "All projects (global) → ~/.config/grimoire/grimoire.toml", "System (all users) → /etc/grimoire/grimoire.toml". Other platforms, numbered list:
  ```
  Change:

    [standards.engineering.architecture]
    - fallback = "ask"
    + fallback = "both"

  Write to:
    [1] This project (local)  → grimoire.toml            (committed to repo)
    [2] All projects (global) → ~/.config/grimoire/grimoire.toml
    [3] System (all users)    → /etc/grimoire/grimoire.toml
  ```

Note: Prefer `grimoire config set <key> <value>` for single-key changes. For list-type keys (profiles, practices, disabled), use `grimoire config add/remove` — these are idempotent and won't create duplicates:

```bash
grimoire config add standards.profiles engineering           # add a profile
grimoire config remove standards.profiles engineering        # remove a profile
grimoire config add standards.engineering.practices "Google Engineering Practices"
grimoire config remove standards.engineering.practices "Google Engineering Practices"
# With -g / --global to write to global settings
```

**Higher-precedence warning:** Before writing to a settings file, check if a higher-precedence layer already sets this key. Precedence order (highest to lowest): session pins → grimoire.toml (local) → ~/.config/grimoire/grimoire.toml (global) → /etc/grimoire/grimoire.toml (system). If a higher-precedence layer already defines this key, the edit to the lower layer will have no effect. Warn: 'Note: [higher-layer] already sets [key]=[value]. Your change to [lower-layer] will be overridden until you remove or update the higher-precedence setting.'

After file selection, confirm and write. Never write invalid TOML.

**Post-edit validate:** After writing the settings change, offer: 'Validate settings now? This will show the resolved effective spec and confirm your change took effect. [y/n]'. If yes, invoke `check-best-practice-compliance` with scope=[current project] to show the resolved spec.

---

### Step 3c: Remove

Ask which file to remove from (platform-aware select — see Steps intro). Options: "This project (local) → grimoire.toml (Recommended)", "All projects (global) → ~/.config/grimoire/grimoire.toml", "System (all users) → /etc/grimoire/grimoire.toml". Other platforms:
  ```
  Remove from:
    [1] This project (local)  → grimoire.toml            (committed to repo)
    [2] All projects (global) → ~/.config/grimoire/grimoire.toml
    [3] System (all users)    → /etc/grimoire/grimoire.toml
  ```

After file selection, show what will be removed and ask key vs section (platform-aware select — see Steps intro). Options: "Remove this key only (Recommended)", "Remove the entire section", "Cancel". Other platforms:
  ```
  Remove from grimoire.toml:

    [standards.engineering.architecture]
    expires = "2026-09-01"   ← remove this key

  Or remove the entire [standards.engineering.architecture] section? [key / section / cancel]
  ```

If removing from the project file would expose a global default the user didn't intend, show the effective value after removal before confirming.

After confirmation, remove the key or section. If the domain section becomes empty, use a platform-aware confirm (see Steps intro) to ask whether to remove the section header too.

---

### Step 3d: Config add / remove

For list-type keys, use add/remove instead of set — they are idempotent and preserve other list values:

```bash
grimoire config add <key> <value> [--global]
grimoire config remove <key> <value> [--global]
```

Supported list keys: `standards.profiles`, `standards.<domain>.practices`, `standards.<domain>.disabled`.

Show the effective list after the operation using `grimoire config get <key>`.

---

### Step 3e: Switch profile

Store the active profile for a domain in `grimoire.toml` (project) or global settings — use grimoire config set:

```bash
grimoire config set standards.engineering.architecture.active-profile prototype
# or for all projects:
grimoire config set standards.engineering.architecture.active-profile prototype --global
```

Confirm the switch:

```
Switched engineering/architecture to profile: prototype
Stored in: grimoire.toml (local, committed) or ~/.config/grimoire/grimoire.toml (global)

Active practices:
  1. KISS
  2. YAGNI
```

To reset to default: grimoire config unset standards.engineering.architecture.active-profile

---

### Step 3f: Validate

Check the merged settings for issues:

| Check | Issue |
|-------|-------|
| `require` + `disabled` overlap | Contradiction — skill can't be both required and disabled |
| `expires` date < today | Preference has expired — flag for review or removal |
| `remind` date ≤ today | Reminder due — surface to user |
| Unknown key names | Typo in key name — flag |
| `[standards.domain.subdomain.profiles.X]` referenced but no matching profile | Profile defined but never activated |

Output:

```
Validating settings files...

  grimoire.toml (local)
    ⚠️  engineering/architecture: expires "2026-09-01" is past — still apply? (platform-aware confirm, options "Keep"/"Remove" — see Steps intro)
    ❌  engineering/testing: "apply-tdd" is in both require and disabled — contradiction
    ✅  engineering/development: OK

  ~/.config/grimoire/grimoire.toml (global)
    ✅  global: OK

1 error, 1 warning across 3 files. Fix errors before conflicts can be resolved correctly.
```

### Step 3g: Context

Run `grimoire context` to show the full ground truth in one shot — installed agents, resolved settings with source attribution, active profiles with expanded skill lists, compliance status, and structural rule findings.

```
grimoire context            # human-readable
grimoire context --json     # machine-readable JSON
```

Output includes a `project:` line showing the resolved project directory (useful when `--project-dir` or `GRIMOIRE_PROJECT_DIR` is set).

Via MCP: call `grimoire_context` tool — available to any AI assistant configured with `grimoire mcp serve`.

For a focused compliance health snapshot:
```bash
grimoire status             # active profile, skill count, last check age + pass/fail + staleness
```

### Step 3h: MCP setup

Configure the AI assistant to connect to grimoire natively via MCP:

1. Run: `grimoire mcp config --target <assistant>`
   Supported targets: `claude`, `cursor`, `windsurf`, `cline`

2. Add the printed config snippet to the assistant's MCP config file. Example for Claude Code (`~/.claude/mcp.json` or `.claude/mcp.json`):

```json
{
  "mcpServers": {
    "grimoire": {
      "command": "grimoire",
      "args": ["mcp", "serve"]
    }
  }
}
```

If the AI assistant runs outside the project root (common with desktop apps), pin the project directory so grimoire reads the right settings and compliance reports:

```json
{
  "mcpServers": {
    "grimoire": {
      "command": "grimoire",
      "args": ["--project-dir", "/absolute/path/to/project", "mcp", "serve"]
    }
  }
}
```

Alternatively, set `GRIMOIRE_PROJECT_DIR=/absolute/path/to/project` in the assistant's environment config.

3. Restart the assistant. All 34 grimoire MCP tools are now available (see `install-grimoire` for the full tool list).

### Step 3i: Check provider config

Configure which AI provider `grimoire check` uses in independent mode. Add to `grimoire.toml`:

```toml
[core.check-provider]
provider = "anthropic"            # anthropic | openai | openrouter | grok | ollama | groq
model = "claude-opus-4-8"
api-key-env = "ANTHROPIC_API_KEY" # default for anthropic; omit to use the provider default
```

Or force per-run with `--via`:
```bash
grimoire check --via claude       # use local claude CLI
grimoire check --via gemini       # use local gemini CLI
```

Resolution order: `--via` flag → local CLIs (claude/gemini/codex/copilot) → `[core.check-provider]` → auto-detect env vars.

## When NOT to Use

- **Adding a new preference from scratch**: use `pin-best-practice-preference` — it guides the full pin flow with scope selection.
- **Resolving conflicts between skills**: use `resolve-best-practice-conflict` — it loads both SKILL.md files, identifies the specific contradiction, and updates priorities.
- **Installing or upgrading grimoire**: use `install-grimoire`.

## Common Mistakes

**Editing the wrong file**: always confirm which file (local, global, system) before writing. A setting in `grimoire.toml` commits to repo (--local). Personal settings belong in --global.

**Removing without checking cascade**: deleting a key from the project file may expose a global default the user didn't intend. Show the effective value after removal before confirming.

**Profile confusion**: `active-profile` is personal — use --global flag to keep it out of the committed project file.
