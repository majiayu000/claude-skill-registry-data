---
name: host-connect
description: "Use when the user wants work to run on their VPS or another machine, or a host is missing or broken in team_host. Walks them through connecting it."
user-invocable: false
---
# Host connect
Gate: get the user's OK before adding a host, changing a server's settings or starting Remote Control (G3, G6). See gates.md in the skill house-rules.
Job: Get a remote machine to where the hub can hand it runs: reachable over Tailscale, key-only ssh, Claude Code signed in, listed in `team_host`.
Takes: the user's wish to use a machine.   Gives: a working host name, or the one step only the user can take.

## Check first

Run these before saying anything is missing. Each is read-only.

1. `team_host {action: list}`. If the machine is there, try a small read run on it and stop if it answers.
2. The user's ssh aliases: `ssh -G <alias>` shows where an alias points.
3. `ssh -o BatchMode=yes -o ConnectTimeout=10 <alias> true`. Success means key-only login already works.
4. `tailscale status`, to see whether the machine is on their tailnet and online.
5. Once key login works, probe how agents may run there: `ssh <alias> 'id -u'`, then `ssh <alias> 'claude -p --permission-mode auto "say ok"'`. As root, Claude Code refuses the bypass mode and auto works `[reported]`. `team_host add` records `asRoot` in the host entry; say which modes started.

## Two paths

**Key login already works.** Do the rest yourself, with the user's OK for each gate:

- `team_host {action: add, name, ssh}` registers it and records the agents installed there.
- If Claude Code is missing there, say so. Installing it is the user's call (G3).
- A remote shell can't sign Claude Code in for them. Signing in is theirs: `ssh <alias>`, then `claude auth login`.

**Key login doesn't work yet.** That needs a password typed once, or a Tailscale approval, and both belong to the user. Don't ask for a password, and never put one in a command. Tell them to run this in their own terminal:

```
damistack connect <name>
```

It walks them through every step, checks first, and skips what is already done:

| Step | What it does |
|---|---|
| Local tools | Checks for ssh and Tailscale |
| Find the machine | Picks it from the tailnet, or puts it on the tailnet over its public address |
| Key | Makes `~/.ssh/dami_<name>`, a key for this machine only |
| Let the key in | Adds the key, with the password typed into ssh itself, once |
| ssh shortcut | Adds `Host <name>` to `~/.ssh/config`, after a backup |
| Lock it down | Offers to turn password login off, and says if the firewall still lets ssh in from the internet |
| Claude Code there | Installs it and signs it in if needed |
| Join the hub | Registers the host, and can start Remote Control |

It changes nothing without a yes. For an agent-driven rerun, `--yes --no-harden --no-rc` takes only the safe defaults and asks nothing.

When they say it's done, check from step 1 again before you use the host.

## Using it

- `team_ask {to: claude, host: <name>, message: <packet>}`. A remote run gets the working folder as it is now and runs on its own worktree there. Write mode brings its commit back as a branch. See levels.md in the skill house-rules.
- `team_host {action: remote_control, name, control: start}` lets the user drive sessions there from claude.ai/code. It runs until stopped.
- `team_ask` starts Claude in acceptEdits for write and the default mode for read, on any host, and `asRoot` changes neither. A command such a run needs must already be allowed in that machine's Claude settings `[assumed]`. For a run you start over ssh on a root host, use the auto permission mode: it starts as root where bypass doesn't.
- When the user says stop, stop the hub's Remote Control with `control: stop`, and say whether any other Claude process is still running there.

## Done when

- A small read run on the host answered `[observed]`, or the user has the one command left to run.
- Whether agents run as root there, and which permission modes start, is recorded.
- Nothing on the server changed without their yes, and no password passed through you.
