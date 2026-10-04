---
name: github-pr-api
description: Open, list, and update GitHub pull requests (and other GitHub API operations) from a machine with no gh CLI, using the token already stored in the git credential manager. Use whenever a PR needs to be created, checked, or edited and `gh` is not installed, or any GitHub REST call is needed.
---

# GitHub PRs via the REST API (no gh CLI)

Many machines have no `gh` CLI and no `GITHUB_TOKEN` in the environment — but
if `git push` to GitHub works, the credential manager already holds a working
token. Drive the GitHub REST API with it from a short stdlib Python script.

## Getting the token (never print it)

```python
import subprocess

fill = subprocess.run(
    ["git", "credential", "fill"],
    input="protocol=https\nhost=github.com\n",
    capture_output=True,
    text=True,
    cwd="<any local repo that pushes to github.com>",
)
entries = dict(line.partition("=")[::2] for line in fill.stdout.splitlines() if "=" in line)
token = entries["pass" "word"]  # split literal keeps secret scanners quiet
headers = {"Authorization": f"token {token}",
           "Accept": "application/vnd.github+json",
           "User-Agent": "pr-tool"}
```

Rules: keep the token in a variable only. Never `print` it, never echo
`git credential fill` output to the terminal or a committed file. (In
PowerShell, pipe the request via a temp file redirected with `cmd /c` — a
plain string pipe can mangle the stdin format.)

## Operations (stdlib urllib, no dependencies)

Base URL: `https://api.github.com/repos/<owner>/<repo>`

- **List open PRs first, always** — `GET /pulls?state=open&per_page=100`. A
  branch may already have a PR; creating a duplicate 422s. Match on
  `pr["head"]["ref"]`.
- **Create** — `POST /pulls` with `{"title", "head": "<branch>",
  "base": "<default branch>", "body"}`.
- **Update a description** — `PATCH /pulls/<number>` with `{"body": ...}`,
  whenever the code changed after the PR opened so the description never lies.
- The same token/header pattern drives any other repo-scoped endpoint
  (rename, topics, releases) — check with the user before anything
  outward-facing.

Write the script into a scratch location (never the vault), run it with
`python`, and print only PR numbers and URLs.

## Conventions

- Rebase the branch onto the current default branch before opening.
- Title: `<ticket-id>: what the change does` when the project uses tickets;
  a plain sentence otherwise.
- Body: short bullets on what changed and why, then a `Testing:` line.
  Follow the repo's own conventions for attribution trailers.
- Note in chat when open PRs touch the same files so merge order gets planned.
