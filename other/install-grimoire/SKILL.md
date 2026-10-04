---
name: install-grimoire
description: Use when the user wants to install or uninstall grimoire skills by domain or individual skill, upgrade grimoire to the latest version, clean up broken symlinks, list what skills are available, or run a health check on the grimoire installation.
source: Package manager UX patterns (Homebrew, npm, apt); grimoire scripts/grimoire
tags: [uninstall, upgrade, clean, doctor, health, diagnostics, skills, setup]
---

# Install Grimoire

Install, uninstall, or upgrade grimoire skills — a guided interface over the `grimoire` CLI.

## Why This Is Best Practice

**Adopted by:** Every major package manager (Homebrew, npm, apt, pip) provides a guided CLI with confirmation prompts before destructive operations and clear output of what was changed. The pattern of "show command → confirm → execute → report" is universal because it prevents silent failures and makes installs auditable.
**Impact:** Silent install failures (wrong path, broken symlink, permission error) are the primary cause of "the skill isn't working" confusion. Explicit confirmation before uninstall and clear post-install reporting (what was installed, where, how many) eliminates the ambiguity. Homebrew's `brew install` output format — listing each installed path — is the gold standard for install UX.
**Why best:** Running `grimoire` directly requires knowing the exact flags. A guided skill extracts intent from natural language ("install the engineering skills for Claude"), constructs the correct command, confirms before running, and surfaces the result in plain language.

Sources: Homebrew documentation; npm CLI documentation; grimoire CLI

## Steps

**Platform-aware prompts:** Claude Code → `AskUserQuestion`; OpenCode → `question` (same schema); Gemini CLI → `ask_user`; all other platforms → the inline `[y/n]` block shown at each step.

### Step 1: Detect operation

| User signal | Operation |
|-------------|-----------|
| "install", "add", "set up" | `install` |
| "uninstall", "remove", "delete" | `uninstall` |
| "upgrade", "update", "get latest skills" | `upgrade` |
| "clean", "fix broken links" | `clean` |
| "list", "what's available", "show domains" | `list` |
| "doctor", "health check", "status", "is everything working" | `doctor` |
| "init", "initialize project", "create settings" | `init` |
| "update grimoire binary", "upgrade grimoire CLI", "self-update" | `self-update` |
| "add package", "remove package", "list packages", "manage skill sources" | `package` |
| "wizard", "setup wizard", "interactive setup", "guided setup" | `wizard` |
| "set up MCP", "configure Claude Code", "connect to AI assistant", "MCP" | `mcp-setup` |
| "watch", "watch compliance", "watch for changes", "continuous check" | `watch` |
| "compliance status", "project status", "what's my status", "health" | `status` |
| "publish package", "share package", "submit package" | `package-publish` |

### Step 2: Gather parameters

For `install` and `uninstall`, determine scope:

```
# Install all skills
grimoire install                                                        # installs everything

# Install one domain
grimoire install --domain engineering                                   # only engineering skills

# Install one subdomain
grimoire install --domain engineering --subdomain development           # one subdomain

# Install one skill
grimoire install --skill engineering/development/apply-kiss-principle   # one skill
```

For `install`, also determine target agent:

```
grimoire install --domain engineering --target all      # all detected agents (default)
grimoire install --domain engineering --target claude   # Claude Code only
grimoire install --domain engineering --target codex    # Codex only
grimoire install --domain engineering --target gemini   # Gemini CLI only
```

**Install mode** — symlink (default) vs copy:

```
grimoire install --domain engineering                   # symlink (default) — updates automatically on grimoire update
grimoire install --domain engineering --copy            # copy files — use when symlinks are unsupported (e.g. some CI, Windows without admin)
```

Copy-mode installs write a `.grimoire-managed` marker inside each skill directory. Grimoire uses this marker to safely identify and remove its own copies during uninstall and clean — it will never delete a directory it didn't create.

If scope or target is ambiguous, ask one question before proceeding.

### Step 3: Show command and confirm

Construct the `grimoire` command and show it before running (platform-aware confirm, options "Continue (Recommended)"/"Cancel" — see Steps intro). Other platforms: show the block below and wait for `[y/n]`.

Install example (other platforms):
```
Will run:
  grimoire install --domain engineering --target claude

This will install all engineering skills (~101 skills) to Claude Code.
Continue? [y/n]
```

For `uninstall`, flag it explicitly (same platform-aware confirm — Claude Code/OpenCode/Gemini CLI use their native tool):
```
Will run:
  grimoire uninstall --domain business --target all

This will REMOVE all business skills from all agents. Cannot be undone without re-installing.
Continue? [y/n]
```

For `upgrade` (same pattern):
```
Will run:
  grimoire update

This will pull the latest grimoire from GitHub and refresh all symlinks.
Continue? [y/n]
```

For `init` (no confirmation needed — non-destructive):
```bash
grimoire init                                     # current directory
grimoire --project-dir /path/to/project init      # specific directory
```

For `self-update` (check-only by default, confirm before applying):
```
Will run:
  grimoire self-update --yes

This will replace the grimoire binary with v1.2.3.
Continue? [y/n]
```

For `package` operations:
```bash
grimoire package list                                      # no confirmation needed
grimoire package add <name> <url>                          # confirm before cloning (owner/repo, git URL, or local path)
grimoire package remove <name>                             # confirm — deletes local clone
grimoire package update                                    # confirm if changes expected
grimoire package update <name>                             # update one package
grimoire package set <ref>                                 # set official package to a fork/mirror; run grimoire update after
grimoire package reset                                     # revert official package to default (grimoire-core)
grimoire package validate [path]                           # validate package structure before publishing
grimoire package publish                                    # step-by-step publishing checklist; opens github.com/new
```

For `wizard`:
```bash
grimoire wizard                                             # interactive setup — guides through package, profile, and settings
```

For `watch`:
```bash
grimoire watch              # re-run compliance check on every file save
grimoire watch --via claude # force a specific AI agent
```

For `status`:
```bash
grimoire status             # show active profile, skill count, last check result + age
```

### Step 4: Execute

Run the confirmed command via Bash. Stream or capture output.

### Step 5: Report result

**Partial-failure handling:** After running the install command, verify each requested component installed successfully. If some domains installed and others failed:
1. List what succeeded and what failed with error reason
2. Do not report 'installation complete' if any component failed
3. Offer retry for failed components: 'Retry failed installs? [y/n]'
4. If a domain fails due to network/permission error vs. not-found error, distinguish them — not-found means the domain name is wrong; network/permission means retry may work.

**Terminal conditions:**
- Max retries: 2 per failed component
- After 2 failures: mark component as FAILED, continue with remaining components
- Error type routing:
  - `404 / not found / unknown domain`: wrong name — do NOT retry; ask user to verify the domain name
  - `network timeout / 503`: transient — retry up to 2×
  - `403 / permission denied`: stop retrying; output manual install command: `grimoire install --skill [failed-component]`
  - Any other error: retry once; if still failing, mark FAILED and continue

```
✅ Installed 101 skills from engineering domain to Claude Code.

Installed at: ~/.claude/skills/

Domains installed:
  engineering/development        (18 skills)
  engineering/architecture       (12 skills)
  engineering/testing            (9 skills)
  ... (and 8 more sub-domains)
```

For `upgrade`:

```
✅ Grimoire upgraded to latest.

  Previous: commit abc1234 (2026-05-01)
  Current:  commit def5678 (2026-06-09)

  New skills: 14
  Updated skills: 7
  Symlinks refreshed: 202
```

For `list`:

Show available domains and skill counts. For subdomain or skill scope, show names.

For `doctor`:

Run `grimoire doctor` directly (read-only, no confirmation needed). Output shows 3 sections:

```
Grimoire health check

  Source
    ✅  git repo:    /path/to/grimoire (commit abc1234, 2026-06-09)
    ✅  grimoire:  executable

  Installed skills
    ✅  claude:   312 skills, 0 broken symlinks
    ⚠️   codex:    88 skills, 3 broken symlinks  → run: grimoire clean --target codex
    ⬜  gemini:  (not detected — skipped)

  Config
    ✅  project (grimoire.toml) — present, valid TOML
    ⬜  global (~/.config/grimoire/grimoire.toml) — not found

  Summary: 1 warning.
```

For full ground truth beyond health check, run `grimoire context` — it shows resolved settings, active profiles with expanded skills, compliance status, and all structural findings in one output.

For `init`:

```
✅ Grimoire initialized.

  Created: /path/to/project/grimoire.toml
  Profile: engineering (auto-detected)

  Next steps:
    1. Ask your AI to run /check-best-practice-compliance   (generates report in .grimoire/reports/)
    2. Run grimoire check --from-report --ci                (enforce thresholds, annotate CI)
    3. Or: grimoire check                                   (independent mode — runs AI itself)
    4. Run grimoire watch                                   (continuous monitoring on file save)
```

For `self-update`: output shows current/latest version and upgrade status. For `package`: output shows each package name, URL, skill count, and operation result.

### Step 6 (mcp-setup): Configure MCP server

After successful install, offer MCP setup:

```
Connect grimoire to your AI assistant natively via MCP? This lets the AI call grimoire
tools automatically at session start without manual commands. [y/n]
```

If yes, determine the target assistant (ask if ambiguous), then run:

```
grimoire mcp config --target <assistant>
# Supported: claude, cursor, windsurf, cline
```

Show the printed config snippet and guide the user to add it to their assistant's MCP config file.

If the AI assistant runs outside the project root (common with desktop apps like Claude Code Desktop), pin the project directory so grimoire reads the right settings and compliance reports:

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

Alternatively via environment variable: `GRIMOIRE_PROJECT_DIR=/absolute/path/to/project`.

Confirm that a restart is needed. Once connected, all 32 grimoire MCP tools are available (see `configure-grimoire` for the full list).

**For uninstall:** also offer to remove the MCP server config block if the user is fully removing grimoire.

## When NOT to Use

- **Changing preferences or settings**: use `configure-grimoire` or `pin-best-practice-preference`.
- **Resolving skill conflicts**: use `resolve-best-practice-conflict`.
- **Writing a new skill**: use `write-best-practice-skill`.

## Common Mistakes

**Uninstalling instead of upgrading**: if the user says "update my skills," that almost always means `--upgrade` (refresh to latest), not `--uninstall`. Confirm the intended operation before running.

**Wrong target agent**: defaulting to `--target all` is usually correct, but if the user only uses one agent, installing to all wastes disk space with unused symlinks. Ask if ambiguous.

**Skipping confirmation on uninstall**: always show the uninstall command and warn it's destructive before running. Never auto-run uninstall without explicit user confirmation.
