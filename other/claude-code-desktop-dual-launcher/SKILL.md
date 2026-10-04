---
name: claude-desktop-dual-launcher
description: Set up a second (or third, fourth...) Claude Desktop instance on Windows so two accounts can be logged in side-by-side. Use whenever the user mentions running multiple Claude Desktop accounts, dual-launching Claude, "--user-data-dir", switching Claude accounts without logging out, hitting a usage limit and wanting to use another account in parallel, or anything about multi-account Claude Desktop on Windows. Also triggers on questions like "can I open two Claude windows", "two Pro accounts", or "Claude Desktop second instance".
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - PowerShell
  - Glob
---

# Claude Desktop Dual Launcher (Windows)

Sets up a second isolated Claude Desktop instance on Windows by leveraging Electron's
`--user-data-dir` flag. Each instance has its own OAuth login, chat history, and
local state — they can run **at the same time**, side by side.

> **Scope:** Windows only (v1). The Windows Claude Desktop is a Microsoft Store MSIX
> package that internally still respects standard Electron command-line flags. macOS
> and Linux support is not implemented yet.

Arguments passed: `$ARGUMENTS`

---

## When to use this skill

Trigger on any of:
- "double-open / dual-launch Claude Desktop"
- "run two Claude accounts at the same time"
- "switch Claude accounts without logging out every time"
- "I've hit the usage limit, can I use my other Pro account in parallel"
- "Claude Desktop multi-instance / second window"
- "--user-data-dir"
- "set up a [name] instance" where the user has previously set up dual-launcher

## Dispatch on arguments

### No args — explain + offer to set up

Briefly explain to the user what this skill does (two parallel Claude Desktop
windows, each with its own account), confirm they're on Windows, then offer to
run setup with a default instance name (`secondary`) or ask for a custom name.

Ask for the **instance name** the user wants (alphanumeric, hyphen, or underscore
only). Suggest something memorable tied to the account's purpose ("work",
"personal", an account nickname). Avoid offering the user's email or any
identifying info — the name will appear on the desktop as `Claude (<name>).lnk`.

Then proceed to the "Run setup" step below with that name.

### `<instance-name>` — run setup directly

Treat the first whitespace-separated token of `$ARGUMENTS` as the instance name.
Validate it matches `^[A-Za-z0-9_-]+$`. If not, ask the user to choose a simpler
name.

Then proceed to "Run setup".

### `uninstall <instance-name>` — remove an instance

Run `scripts/uninstall.ps1 -InstanceName <name>`. This deletes the desktop
shortcut, the launcher script, and (after confirmation) the `user-data-dir`.

---

## Run setup

Locate `scripts/setup.ps1` relative to this `SKILL.md` and invoke it through
PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "<path-to>/scripts/setup.ps1" -InstanceName "<name>"
```

The script will:

1. Scan `C:\Program Files\WindowsApps\Claude_*\` for the latest Claude.exe
2. Create an isolated user-data-dir at `%APPDATA%\Claude-<name>\`
3. Deploy a self-healing launcher at `%USERPROFILE%\.claude-dual-launcher\launch-<name>.ps1`
4. Create a desktop shortcut `Claude (<name>).lnk`
5. Launch the new instance so the user can log in with the second account

Stream the script output to the user. When done, summarize what was created and
remind the user that:

- **Two instances can run at the same time.** The original Claude Desktop launches
  from the taskbar/start menu like before; the new instance is opened via the
  desktop shortcut.
- **Don't log in to the same account in both instances.** Anthropic's sessions
  list will show two clients online for the same account, which may trigger
  security review.
- **Each instance is independent.** Logging out of one and signing in as a
  different account does not affect the other.
- **If a Claude update breaks the desktop shortcut**, the self-healing launcher
  script (`%USERPROFILE%\.claude-dual-launcher\launch-<name>.ps1`) auto-detects
  the new version's path. Either run it directly, or re-run this skill (`setup`)
  to refresh the shortcut.

## Common follow-ups

- **"How do I add a third instance?"** — Re-invoke the skill with a different
  instance name (e.g. `personal`). Each name creates an independent instance.
- **"How do I remove one?"** — `uninstall <name>`.
- **"Can I pin the new shortcut to taskbar?"** — Yes, but Windows may visually
  merge it with the original Claude taskbar icon. Pinning is best after
  confirming the new shortcut works reliably.
- **"What about Mac / Linux?"** — Not supported yet in v1. The underlying
  `--user-data-dir` mechanism works on those platforms too, but the setup paths
  differ. PRs welcome.

## How it actually works (background, for the curious)

Claude Desktop on Windows is shipped as a Microsoft Store MSIX package, but
inside the package is a standard Electron application. Electron honors the
`--user-data-dir=<path>` command-line flag, which redirects all of:
- OAuth tokens (stored in `Local Storage\leveldb\`)
- Chat history
- Window state
- Plugin enable/disable state

…to the specified directory instead of the default `%APPDATA%\Claude\`. This is
the same dual-instance technique used by Discord, Slack, VS Code, and other
Electron apps.

Note: Files under `%USERPROFILE%\.claude\` (CLAUDE.md, MEMORY.md, plugin code,
project settings) are **not** part of user-data-dir, so they are shared across
all instances. This is usually what users want — global config and memory
travel with the user, while sessions/auth are isolated.
