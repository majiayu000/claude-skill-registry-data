---
name: jira
description: Create, read, comment on, and transition Jira Data Center tickets with a personal access token (PAT). Use when the user mentions Jira, a ticket key, issue status, transition, create issue, browse URL, or asks to update a company-hosted Jira ticket.
---

# Jira (Data Center PAT)

Company-hosted Jira Server / Data Center. Auth is **Bearer PAT**. Basic/password does not work (SSO).

## STOP — rate limit / 429 / "taking too long"

A 429 here is almost always **the coding agent's own quota**, not Jira. It happens when you write scripts, retry, or "fix" a failed run.

If you see 429, rate limit, or quota:

1. Stop. Do not retry. Do not write a new `.py` / `.ps1` / `.sh`.
2. Tell the user: "Poolside hit its own rate limit. Wait, then run one launcher command."
3. End the turn.

First action on a ticket request is **exactly one** launcher command (two only for transition: list, then apply). Show stdout/stderr. If it failed, stop.

**Never write a new HTTP client.** Never tell the user to install MSYS2, Git Bash, curl, or Python. Use the bundled launcher; it picks a runner that is already on the machine.

## Launcher (always this)

- **macOS / Linux:** `<skill>/scripts/jira` (no extension)
- **Windows:** `<skill>/scripts/jira.cmd`

There is **no** `scripts/jira.md`. `SKILL.md` is instructions, not a command. Never run `jira.md`, `SKILL.md`, or `README.md`.

Windows example (from the repo root):

```bat
.poolside\skills\jira\scripts\jira.cmd transition PROJ-123 "Done"
```

Do not choose bash vs PowerShell vs Python yourself.

Windows `jira.cmd` fallbacks (first hit wins):

1. Windows PowerShell (`jira.ps1`) — built-in. Prefer this; Git Bash often lacks `dirname`.
2. Git Bash or MSYS2 bash, if already installed (not WSL `System32\bash.exe`)
3. Python stdlib (`jira.py`) — only if `python`/`py` is already on PATH

Override: `set JIRA_RUNNER=powershell` (or `bash` / `python`).

## Setup (once)

Token file (primary, not in git):

- macOS/Linux: `~/.config/atlassian/jira.token`
- Windows: `%USERPROFILE%\.config\atlassian\jira.token`

One line, the PAT only, no quotes. Base URL in the repo-root `.env` (same folder as `.poolside`), not only in the current shell directory:

```
JIRA_BASE=https://jira.example.com
```

No quotes required. Not `.env.txt`. The launcher walks up from the script and from cwd to find that file. Do not hardcode a host in this skill.

Fallback order for the token: `JIRA_TOKEN` in the environment, then the token file (`JIRA_TOKEN_FILE` override), then `.env` / `JIRA_ENV_FILE`.

## Every request

```bash
# macOS / Linux
<skill>/scripts/jira get PROJ-123
```

```bat
REM Windows
<skill>\scripts\jira.cmd get PROJ-123
```

If the user pastes a browse URL, pass it through (`get` / `transition` / `comment` parse the key).

One user ask should be one or two HTTP calls. Do not retry in a loop. If the call fails, show the HTTP body and stop.

## Commands

| User says | Run |
|-----------|-----|
| show / read ticket | `jira get KEY` |
| change status / transition | `jira transitions KEY` then `jira transition KEY "In Progress"` |
| comment | `jira comment KEY "text"` |
| create ticket | `jira create PROJ "summary"` |
| raw REST | `jira GET /rest/api/2/myself` |

`--dry-run` prints curl with `Authorization: Bearer ***`. Never print the real token. Never ask the user to paste the PAT in chat.

## Red flags

- Writing a new `requests` / `httpx` / `urllib` script (use bundled `jira.py` only as the launcher last resort)
- Telling the user to install MSYS2, Git Bash, or Python
- `Authorization: Basic`
- Committing `.token` files or putting a real host in SKILL.md
- Dumping `curl -v` (leaks the Bearer header)
