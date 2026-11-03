---
name: sandbox-macos
description: "Use when a Mac command is refused by confinement. Explains the five activity classes (research, project, build, offline, media), what each Seatbelt profile lets a command read, write and reach, why the network opens only with a grant, why the keychain and home secrets are never reachable, and how to ask the owner instead of working around a refusal."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
metadata:
  hermes:
    tags: [iclone-os, sandbox, confinement, seatbelt, macos, security]
    related_skills: [sandbox-linux, sandbox-windows, consent]
---

# Confinement on macOS — Seatbelt profiles

## When to use
- A terminal command fails with `Operation not permitted`, exit 126, or `Refused by icloneOS confinement`.
- You need to know whether a command may write a path, reach the network, or run a binary before you run it.

On macOS, icloneOS runs every terminal command, `execute_code` and the file tools (`read_file`, `write_file`, `patch`
run through the terminal backend) inside a Seatbelt profile the app generates. The profile starts from **deny by
default**: anything it does not name is refused, so `write_file` outside the project is refused even when the
permission mode would allow it. MCP servers and the browser are not inside it — the permission mode governs those.
A network grant opens the internet only: `localhost`, `127.0.0.1`, `::1` and this Mac's own addresses stay refused.

## The five activity classes
| Class | Reads | Writes | Network |
|---|---|---|---|
| research | the OS, toolchains, the project, its scratch | its scratch only | only with a grant |
| project (default) | same | the project and its scratch | only with a grant |
| build | + package caches (npm, pip, cargo, go, gradle, maven, bun) | + those caches | only with a grant |
| offline | same as project | the project and its scratch | never |
| media | the project and one output folder | the output folder and its scratch | never |

- **The project** is the git root above the session's folder, fixed when the session starts. A `cd` elsewhere never
  makes that folder writable. Your home, `/`, `~/Library` and the app's own state are never a project: the session
  then works in its scratch dir (`$TMPDIR` points there).
- **Plan mode** keeps the project read-only. **Ignore permissions** skips the asks, never the confinement.
- **The network** opens only when the permission mode allows it or the owner granted it for this session, project or
  standing. An "Allow once" on a command does not open a socket in the middle of it.

## Never, in any class or mode
`~/.ssh`, `~/.aws`, `~/.gnupg`, `~/.config/gh`, `~/.netrc`, `~/.npmrc`, `~/.pypirc`, `~/.docker`, `~/.kube`, the
keychains (`~/Library/Keychains`, `/Library/Keychains`) and their services, the app's own data, Hermes' `.env`,
`auth.json` and `config.yaml`; `launchctl`, `osascript`, `open`, `security`, `sudo`; other apps' processes; unix
sockets other than DNS.

## Hard links into the project
Seatbelt judges a path, not an inode, so before every command the app scans the project and the session's scratch
for files that are hard links to inodes outside them, and refuses to start (`confinement refused to start in …`,
exit 126) until the owner removes them or allows them, one folder group at a time, in the Dock's **Containers**
window. A folder the scan cannot list, or whose contents it cannot stat (`cannot scan …`), is refused the same way
until its permissions are fixed; a link that appears while a command runs is recorded when it exits. In the Build
class alone, a link whose every other name is inside the pnpm store (`~/Library/pnpm`, `~/.local/share/pnpm`,
`$PNPM_HOME` — a real directory, not a symlink, with pnpm's `store/v<N>` layout and never a denied folder) runs
without a gesture; each name counts once, so a file with any name elsewhere still asks. A store is never a project: a
command run from inside one gets its scratch folder instead. Package caches (npm, pip, cargo, pnpm…) are not scanned for hard links: a Build
command may read and fill them anyway.

## When a command is refused
1. Do not try another route to the same effect (a different binary, a copy, a symlink): the refusal is the answer.
2. Say what you needed and why. If the network is the blocker, ask the owner for a network grant through the consent
   door (`~/.iclone-os/bin/acp consent request webBrowsing --reason "…"`).
3. If a path outside the project is needed, ask the owner to open that folder as the project instead.

The owner sees every confined command, every refusal and the rule that fired in the Dock's **Containers** window.
