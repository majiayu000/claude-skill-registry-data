---
name: t3-code
version: 0.1.3
license: MIT
description: Use when configuring or troubleshooting T3 Code projects, multi-machine environments, desktop or headless servers, project names or icons, updates, launchers, or private remote access. Trigger on stale project entries, wrong workspace identity, missing favicons, update banners, saved backend setup, server reachability, Tailscale exposure, SSH tunnel fallback, or T3 service setup.
---

# T3 Code

Manage T3 Code without tying the setup to one machine, package source, repository layout, or private network.

## Start with the surface

Identify the failing surface before changing anything:

1. Desktop application state and launch method.
2. T3 server state under the selected base directory.
3. Project registration, title, workspace root, or favicon.
4. Headless server process or user service.
5. Private remote access through Tailscale.
6. Update source for the desktop application and CLI.
7. Multi-machine topology, saved environments, pairing, or tunnel fallback.

Record the installed version and supported flags first:

```bash
t3 --version
t3 project --help
t3 serve --help
```

Nightly flags and storage details can change. Prefer the installed CLI help over copied commands.

## Inspect before changing

- Find the actual executable with `command -v t3`.
- Identify the configured base directory. The usual default is `~/.t3`, but `--base-dir` or `T3CODE_HOME` may override it.
- Determine how the desktop application was installed: package manager, AppImage, source checkout, or another channel.
- Determine whether the server runs interactively, through a wrapper, or as a user service.
- Read `references/multi-machine.md` before setting up one desktop to manage projects on other hosts.
- Read `references/windows-remote.md` when a remote T3 backend runs on Windows.
- Read `references/project-state.md` before changing project records or icons.
- Read `references/remote-tailscale.md` before exposing a headless server.
- Read `references/updates-and-launchers.md` before installing T3 or changing release channels, updates, wrappers, or services.

## Prefer supported commands

Use T3 project commands before considering direct database edits:

```bash
t3 project add --base-dir "$HOME/.t3" --title "Project (Workstation)" /path/to/repository
t3 project rename --base-dir "$HOME/.t3" /path/to/repository "Project (Workstation)"
t3 project remove --base-dir "$HOME/.t3" /path/to/repository
```

Do not use `--force` with `t3 project remove` unless the user explicitly intends to delete the project and its threads.

Use host-qualified titles only when the same repository is active on more than one machine and the distinction helps the user select the right workspace. Do not change the Git remote to solve a display-name problem.

## Keep local integration outside release artifacts

Do not patch an installed AppImage, generated bundle, or package directory for a durable fix. Put local behavior in user-owned locations such as:

- `~/.local/bin/` for launch, update, or tunnel wrappers.
- `~/.local/share/` for local-only assets.
- `~/.config/systemd/user/` for user services and timers.

Keep machine-specific paths, hostnames, ports, and network addresses in local configuration, not in the reusable skill.

## Verify the result

Run the checks that match the change:

- The T3 command exits successfully.
- The active project list shows the intended title and workspace root.
- The selected favicon exists and does not dirty the repository when it is meant to stay local.
- The desktop launcher opens the intended installed version.
- Every remote environment resolves to the intended host and uses a distinct display name.
- Each headless service is active and its logs show the expected bind address and base directory.
- Each Windows Scheduled Task reports the intended principal, launcher, listener, and restart state.
- The controller can reach each remote environment through its selected Tailnet, Tailscale Serve, or local tunnel URL.
- Desktop and server components report the expected versions after an update.

If the project documents a specific verification command, run that check as well.

## Rules

- Inspect state before mutation.
- Prefer supported CLI operations over SQLite writes.
- Treat project title, workspace identity, Git remote identity, and saved backend identity as separate concerns.
- Confirm installed flags before copying nightly commands.
- Keep remote access private by default. Do not bind to a public interface unless the user explicitly asks and the authentication boundary has been reviewed.
- Give every remote environment and local tunnel a unique label and port.
- Never publish real Tailnet addresses, hostnames, credentials, pairing codes, or absolute user paths.
- Ask before deleting project threads, replacing an installation, or changing public exposure.

## Common mistakes

- Renaming a project when the stale selection is actually stored in desktop browser state.
- Editing the database while T3 is running, then losing the change or corrupting state.
- Updating the CLI but leaving the desktop application on an older build, or the reverse.
- Reusing one vague title or one local tunnel port for several machines.
- Treating a successful Tailnet ping as proof that the T3 TCP port is reachable.
- Assuming Tailscale Serve and direct Tailnet binding produce the same URL and port behavior.
- Patching release artifacts instead of keeping wrappers and services in user-owned paths.
