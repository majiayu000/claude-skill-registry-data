---
name: gh-cli-setup-skill
description: >-
  GitHub CLI missing or unauthenticated — per-OS install
  (brew/apt/dnf/winget), gh auth login, auth verification, repo-scope
  check. Fallback for ticket and PR flows when `command -v gh` fails.
  Triggers: gh not installed, install github cli, gh auth login, gh setup.
license: Apache-2.0
compatibility: opencode
category: Git/Workflow
---

## What I do

Set up the GitHub CLI so ticket- and PR-creation flows can continue in
environments where `gh` is missing or unauthenticated. I am the fallback
referenced by `ticketing-skill` (§Platform Detection tooling tier;
`references/github.md` §Tooling fallback) and
`civiltekk-pr-workflow-skill` (`references/create.md` §Steps
step 6, the create route): they invoke me when
`command -v gh` fails, then resume their flow.

## When to use me

- `command -v gh` fails inside a ticket/PR flow
- `gh` installed but `gh auth status` is not valid
- Fresh machine setup before any GitHub operation

## Steps

### 1. Verify absence

```bash
command -v gh || echo "MISSING"
gh auth status 2>&1 || true
```

If `gh` exists and is authenticated, return to the calling flow — nothing to do.

### 2. Install per OS

| OS | Command |
|----|---------|
| macOS | `brew install gh` |
| Debian/Ubuntu | `sudo apt update && sudo apt install -y gh` (needs `gh` apt repo on older images: see https://github.com/cli/cli/blob/trunk/docs/install_linux.md) |
| Fedora/RHEL | `sudo dnf install -y gh` |
| Windows | `winget install --id GitHub.cli` (or `choco install gh`) |

Confirm: `gh --version`.

### 3. Authenticate

```bash
gh auth login
```

Device flow is the default for headless/SSH environments: pick
`GitHub.com` → `SSH` protocol (matches this config's git operations) →
`Login with a web browser`, then open https://github.com/login/device and
enter the one-time code. In a browser-less session, `gh auth login`
prints the code and URL regardless — copy it to the user.

### 4. Verify

```bash
gh auth status
```

- `✓ Logged in to github.com account <login>` → done; report the login and
  return to the calling flow.
- Token present but missing `repo` scope → re-auth with
  `gh auth refresh -s repo` (ticket/PR creation requires `repo`); if the
  refresh fails, redo step 3.

## Common Issues

- **No browser available** — the device flow works from any second device;
  hand the user the code + URL.
- **`gh` not found after install** — new install path not on `$PATH`;
  `hash -r` (bash) or reopen the shell.
- **Corporate proxy** — export `HTTPS_PROXY` before `gh auth login`.

## Return

Report: installed-or-already-present, authenticated login name, scopes.
The calling flow resumes with `gh` usable; author/assignee attribution
resolves to this login (`@me`).
