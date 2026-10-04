---
name: copilot-cli
description: "Delegate coding to GitHub Copilot CLI (features, PRs, code review). Copilot CLI runs as an ACP-compatible agent via `copilot --acp --stdio` or in print mode via `copilot -p`."
version: 1.0.0
author: Yuno
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Copilot, GitHub, Code-Review, Refactoring, ACP]
    related_skills: [claude-code, codex, opencode, hermes-agent]
---
# GitHub Copilot CLI — Hermes Orchestration Guide

Delegate coding tasks to [GitHub Copilot CLI](https://docs.github.com/copilot/how-tos/copilot-cli). Copilot CLI can read files, write code, run shell commands, and manage git workflows autonomously.

## Prerequisites

- **Install:** Comes pre-installed on this system (`copilot --version` → v1.0.61+)
- **Auth:** Run `copilot` interactively and use `/login` for GitHub OAuth, **OR** set `COPILOT_GITHUB_TOKEN` in `~/.hermes/.env`
- **Check status:** `copilot -p "hello" --allow-all` — if it responds without auth error, you're good
- **Health check:** `copilot --version`

## Two Orchestration Modes

### Mode 1: Print Mode (`-p`) — Non-Interactive (PREFERRED for most tasks)

Print mode runs a one-shot task, returns the result, and exits. No PTY needed.

```
terminal(command="copilot -p 'Add error handling to all API calls in src/' --allow-all", workdir="/path/to/project", timeout=120)
```

**When to use print mode:**
- One-shot coding tasks (fix a bug, add a feature, refactor)
- CI/CD automation and scripting
- Any task where you don't need multi-turn conversation

**Print mode skips ALL interactive dialogs** — no workspace trust prompt, no permission confirmations.

### Mode 2: ACP Mode (`--acp --stdio`) — Agent Protocol

Copilot CLI can act as an ACP server for integration with Hermes `delegate_task`:

```
delegate_task(
    goal="Refactor the auth module to use JWT tokens",
    acp_command="copilot",
    acp_args=["--acp", "--stdio"],
    workdir="/path/to/project"
)
```

**When to use ACP mode:**
- Multi-turn iterative work
- Tasks requiring human-in-the-loop decisions
- When you want Copilot to have full tool access (file read/write, terminal, etc.)

**Note:** ACP mode requires Copilot to be authenticated first.

### Mode 3: VS Code ACP Integration

Copilot CLI can be used as an ACP agent in VS Code:

1. **Install ACP Client extension:** `code --install-extension formulahendry.acp-client`
2. **Configure agent** in `~/.config/Code/User/settings.json`:
   ```json
   {
     "acp.agents": {
       "GitHub Copilot": {
         "command": "copilot",
         "args": ["--acp", "--stdio"]
       }
     }
   }
   ```
3. **Open ACP panel** from Activity Bar → select "GitHub Copilot" → connect

**Status (Stand 13.06.2026):** ✅ ACP Client Extension v0.2.0 installiert, settings.json konfiguriert.

## Auth Setup

Copilot CLI requires GitHub authentication. Two methods:

### Method 1: Interactive Login (Recommended)
```
copilot
/login
```
Follow the browser OAuth flow.

### Method 2: Token
Add to `~/.hermes/.env`:
```
COPILOT_GITHUB_TOKEN=***
```

### Verify Auth
```
copilot -p "hello" --allow-all
```
Should respond with a greeting. If you see "No authentication information found", run the login flow.

## Tested & Verified (13.06.2026)

- ✅ `copilot -p "..." --allow-all` — funktioniert
- ✅ `delegate_task(acp_command="copilot")` — funktioniert, Copilot kann Files erstellen und ausführen
- ✅ VS Code ACP Extension installiert und konfiguriert
- ✅ Auth: eingeloggt als `Toqsick` auf GitHub

## Configuration

- **Model:** Set via `copilot --model <model>` or in `~/.copilot/config.json`
- **Config dir:** `~/.copilot/`
- **Logs:** `~/.copilot/logs/`

## Tips

- **Prefer `-p` for quick tasks** — less overhead than ACP mode
- **Use `--allow-all`** in non-interactive mode to skip permission prompts
- **Set `workdir`** to the project directory so Copilot has full context
- **For Hermes integration**, ACP mode via `delegate_task` is the cleanest path
- **Copilot CLI v1.0.61+** is installed on this system (as of 2026-06-13)
- **copilot-instructions.md** — use `templates/copilot-instructions.md` as a starting point for project-specific Copilot guidance
- **VS Code ACP** — see `references/vscode-acp-setup.md` for detailed setup steps
