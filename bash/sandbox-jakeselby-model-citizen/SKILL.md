---
name: sandbox
description: Fence an autonomous or long-running agent loop with the built-in sandbox and network off, or a container with the worktree mounted. Use before any unattended loop, before `execute` autonomy on an unfamiliar repo, and whenever a task pulls untrusted input.
---

# Fence the loop

A permission mode decides whether a call runs. A sandbox decides what a command can reach once it
is running, and the OS enforces that on every child process. An unattended loop needs the second
kind: nobody is at the prompt to answer for the first.

## Runtime scope

The configuration and container example below are Claude Code-specific. Do not copy those
settings into Codex. For Codex, use its native sandbox and approval controls as documented in
[the configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).
A read-only sandbox constrains filesystem writes; approval policy is a separate control.
Native hooks are not a replacement for OS confinement. Custom Codex role defaults can be
superseded by the parent turn's permissions; see `docs/runtime-controls.md` before delegating
work that requires a hard boundary. Client qualification remains in the compatibility catalog.

## The Claude Code sandbox

It "runs on macOS, Linux, and WSL2. Native Windows is not supported"; Linux and WSL2 need
`bubblewrap` and `socat` installed first. Put this in `~/.claude/settings.json` to cover every
project; the `/sandbox` panel writes `enabled` to `.claude/settings.local.json` for one project.

```json
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false,
    "network": { "allowedDomains": [], "strictAllowlist": true },
    "filesystem": { "denyRead": ["~/.ssh", "~/.aws", "~/.config/gh"] }
  }
}
```

`strictAllowlist` over an empty `allowedDomains` is network off: Claude Code then "denies sandboxed
commands access to any host outside the allowlist instead of prompting". Only user, managed and
`--settings` settings set it; a repository's own file cannot. The deny entries are load-bearing —
the default read policy covers the whole disk, and "this default still allows reading credential
files such as `~/.aws/credentials` and `~/.ssh/`." Add `sandbox.credentials.envVars` entries with
`"mode": "deny"` to unset tokens for sandboxed commands too. `failIfUnavailable` makes a missing
dependency a hard stop rather than a silent unsandboxed fallback, and `allowUnsandboxedCommands:
false` removes the retry-outside escape hatch. Subagents inherit the session's sandbox; commands
you type at the `!` prompt do not.

For one session, writing no file: `claude --settings '{"sandbox":{"enabled":true}}'`. Confirm with
`/sandbox`: the **Config** tab shows the resolved settings, and a **Dependencies** tab appearing
means a package is missing. A prompt titled "Bash command (unsandboxed)" is the signal a command
left the boundary. Keys and defaults: https://code.claude.com/docs/en/sandboxing

## A container

Harder boundary, coarser tooling. Mount the worktree and nothing else, stay non-root, and let the
container be the isolation — do not nest the built-in sandbox inside it.

```bash
docker run --rm -it --network none \
  --user "$(id -u):$(id -g)" \
  -v "$PWD:/work" -w /work \
  <image-with-a-local-model-and-agent-cli> agent-cli -p "<the loop prompt>"
```

`podman` substitutes unchanged. `--network none` cuts every hosted API too, so this example requires
the image to contain its model and agent runtime. A hosted-model loop needs a separately reviewed
egress policy and is outside this recipe. Web search and fetch, every remote MCP server and every
package install remain unavailable. Losing all of it is the point when the task parses input you
did not write: a path the loop lacks cannot be talked into opening.

## Which one

Built-in sandbox for daily work: a settings change, every tool still works, the OS still enforces
the boundary. Container for a loop that runs while you sleep, a repo whose build scripts you have
not read, or anything handling untrusted content. Neither isolates branches — run inside a
worktree as well, per the `worktree-per-agent` skill.
