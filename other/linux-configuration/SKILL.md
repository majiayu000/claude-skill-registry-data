---
name: linux-configuration
description: >-
  v1.0.0 — Mandatory rules for any task on this machine that touches Linux desktop
  configuration: GNOME Shell extensions, gsettings, themes, hotkeys, systemd
  user services, or a repository install.sh. Requires console-only, silent
  deployment; activates edited extension code via the sanctioned in-place X11
  run-dialog reload (`xdotool` `Alt+F2 r`) and forbids destructive session
  restarts, logout, `gnome-shell --replace`, and shell-kill commands. Covers
  clean-install compatibility and the root-optional (sudo-free) installer
  pattern.
---

# Linux Desktop Configuration Guidelines

These rules bind every change that touches GNOME Shell, desktop settings,
hotkeys, systemd user services, or any repository `install.sh`. Follow them
exactly even when the user's prompt does not restate them. Never reach for a
destructive shortcut — logout, `gnome-shell --replace`, killing the Shell — to
"just make it apply". When a reload is genuinely required, use only the
in-place X11 run-dialog reload described below, which preserves the running
session.

## Ownership boundary

This is the reusable Linux desktop and installer policy for every project that
selects it. Project `AGENTS.md` files may document local component ownership,
installer entry points, dependencies, and verification commands, but should
not copy the clean-install, root-optional, reboot, or GNOME reload rules here.
When project guidance and this skill disagree on the shared safety procedure,
use this skill and retain only the project-specific exception if it is truly
required and explicitly documented.

## Apply Changes Silently (required default)

Most desktop changes need **no** GNOME Shell reload. Reloading flashes the
panel, resets the overview and animations, and steals focus — it interrupts the
human's active work. Only edited extension *code* requires it (next section).
For everything else, use the narrowest command-line mechanism that takes effect
live, in place, with no visible disruption:

| Change | Silent live mechanism |
|---|---|
| Hotkeys, `org.gnome.desktop.*` / `org.gnome.shell.*` keys, themes, app behavior | `gsettings set …` — immediate in the running session |
| An extension's own settings (its GSettings schema, read at runtime) | `gsettings set` / `dconf write` on that schema — applies live |
| systemd user service (trackers, daemons, helpers) | `systemctl --user restart <unit>` — that unit only, no GUI flash |
| Enabling/disabling an extension (state, not code) | `gnome-extensions enable/disable <uuid>` — runs in place |

Always state the exact silent command you ran, and verify it took effect —
read the gsettings key back, `systemctl --user status`,
`gnome-extensions info <uuid>`.

## Reboot and Poweroff Safety

Never invoke `reboot`, `shutdown`, `poweroff`, `halt`, `systemctl
reboot|poweroff`, or their `loginctl` equivalents directly. When the user
explicitly authorizes a genuinely required reboot or poweroff, route it through
the setup framework's `safe_system_action.sh reboot|poweroff`, which must keep
its audible 10→1 countdown, extended alert at 0, and a Ctrl+C/SIGTERM
cancellation path before requesting the action.

- Installer code calls the shared `safe_system_action` wrapper from
  `linux_installation_scripts_functions/installer_helpers.sh` — never a local
  `sleep 10` reimplementation.
- Runtime programs install and invoke the same helper as
  `~/.local/bin/safe-system-action`.
- Refuse the destructive action when the shared helper is unavailable.
- Never execute the helper while developing, testing, deploying, or validating
  a change. Verify with static source checks, shell syntax checks, and mocked
  call-site tests only — a test must never reach a real reboot or poweroff.

## Extension Code Changes (deploy, then in-place reload)

Editing a loaded extension's **code** (`extension.js` / installed files) still
needs a fresh Shell process: the Shell imports each extension's JS once per
process lifetime and caches the module. There is no sanctioned, non-disruptive
hot-reload for edited source —

- `gnome-extensions disable && enable` calls the *cached* module's
  disable/enable; it does not re-read the edited source.
- The `org.gnome.Shell.Extensions.ReloadExtension` D-Bus method is locked down
  (like `Eval`) and refuses external calls.
- A newly added extension directory is invisible to the running Shell until it
  reloads.

So: deploy the files from the console, verify the installed files and settings,
then activate the new code with the reload that matches the session type —
check `echo "$XDG_SESSION_TYPE"` (or `loginctl show-session`):

**X11** — trigger GNOME's own run-dialog reload, which restarts the Shell in
place while preserving the session, open windows, and enabled extensions:

```sh
xdotool key --clearmodifiers alt+F2
sleep 0.5
xdotool type 'r'
xdotool key Return
```

This is the same `Alt+F2 r` a human would type and the only sanctioned
automated reload. Verify the result afterwards (below).

**Wayland** — there is no in-place run-dialog reload. Do NOT force one. Deploy
and verify the files, then ask the user to log out and back in. Waiting for the
user is always better than losing their open work.

Regardless of session type, never force changes through with any of:

- `gnome-session-quit` / `--logout` / `--force`
- `loginctl terminate-session …` / `loginctl kill-user …`
- `systemctl --user stop gnome-session*` or similar unit stops
- `pkill -HUP gnome-shell`, `killall gnome-shell`, or any Shell-ending signal
- `gnome-shell --replace` — it can disrupt the session and leave user
  extensions globally disabled

After extension work, verify `gsettings get org.gnome.shell
disable-user-extensions` is `false` and previously enabled extensions are still
active.

A Shell reload is never needed when the change only affects a systemd user
service or installer-side gsettings — restart just the affected unit and leave
the GUI alone.

## Clean Installation Compatibility

Every repository change must stay compatible with a clean installation through
`installation_scripts/install.sh` and the repository's own `install.sh`. Do not
rely on packages, files, settings, or manual steps that exist only on the
current machine — add every required dependency, asset, configuration step, and
migration to the installer so a fresh checkout reproduces the complete setup.
Keep installation steps idempotent and verify the clean-install path for every
change.

## Root-Optional Installers (avoid sudo)

All project `install.sh` scripts must run sudo-free in user mode; only
`linux_installations_setup` hard-requires root. When writing or modifying
installers:

- Default invocation is `bash install.sh` with no sudo. Root-only steps
  (`apt install`, udev rules, files under `/etc` or `/usr`) are skipped,
  collected in a `SUDO_REQUIRED_STEPS` list, and reported at the end with the
  exact `sudo` command to apply them.
- When invoked via sudo (clean-install chain), use a `run_as_target` helper
  (`sudo -H -u "$TARGET_USER" env …`) so user-level work lands in the desktop
  user's session, never in root's home.
- Prefer user-level mechanisms that need no root at all: `gsettings`; GNOME
  extensions in `~/.local/share/gnome-shell/extensions/` (user-owned — patch
  and reconfigure without root); `gnome-extensions enable/disable`;
  `systemctl --user` units; files under `$HOME` (`~/.claude`, `~/.config`,
  `~/.local`).
- sudo is genuinely required only for package management (`apt`), system-wide
  extension dirs (`/usr/share/gnome-shell/extensions/`), and root-owned paths
  (`/etc`, `/usr/lib`, udev rules).
- Never bake an unconditional `sudo` into a step that a non-root run will hit;
  it stalls unattended/agent runs on a password prompt.
