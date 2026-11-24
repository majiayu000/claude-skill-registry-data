---
name: cli-tool-traps
description: Use when working with gh, kubectl logs, or Tailscale SSH.
---

# CLI tool traps

## gh: pull requests

- Patch a PR body through the REST API: `gh api -X PATCH repos/<owner>/<repo>/pulls/<N> -F body=@file`. `gh pr edit --body-file` can no-op silently or exit 1 with only a deprecation warning. Re-read the body after the patch to confirm it.
- `gh search prs` matches only a PR's title and body, never its comments. Put any text you need to search for later, such as a rejection ledger or an audit trail, in the PR body.
- A PR whose branch conflicts with the base registers no CI at all: zero check runs, "no checks reported". Probe `mergeStateStatus`, and rebase onto a fresh base to register the checks.
- A body-only edit does not re-fire CI; close and reopen the PR does.

## kubectl logs with a label selector

- With `-l <selector>`, the default tail is 10 lines per container. Pass `--tail=-1` to read the whole logs.

## Tailscale SSH

- A connection to a node waiting for check mode prints a `https://login.tailscale.com/a/...` approval link and waits for approval.
- While the connection waits for approval, tailscaled ignores ssh keepalive requests. Run the ssh in the background with `-o ServerAliveInterval=0` to hold the wait open.
- Tailscale SSH runs each remote command under a `tailscaled be-child ssh ...` wrapper whose argv contains the command text. Over ssh, `pgrep -f` matches that wrapper's argv and counts the ssh session itself. Anchor the pattern at the start of the target's argv, for example `pgrep -fc "^python3 -c while True"`.
