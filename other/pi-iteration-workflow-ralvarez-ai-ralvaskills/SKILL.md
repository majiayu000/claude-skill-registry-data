---
name: pi-iteration-workflow
version: 1.0.0
description: Edit-test workflow for the voldemorbot robot codebase — Windows-to-Pi SSH deploy loop, pixi/ROS2 rebuild triggers, flaky-WiFi survival via screen, PowerShell SSH quoting pitfalls, sudo caching on the Pi Zero. Use when pushing platform/robot changes to hardware, restarting the robot service, or a Pi SSH session misbehaves.
---

# Pi Iteration Workflow

Fast loop for editing `platform/robot` code on Windows and testing it live on real hardware over SSH. Companion to [ros2-architect](../../robotics/ros2-architect/SKILL.md) for the ROS2/Pixi workspace conventions this loop deploys — this skill owns the deploy mechanics, not the workspace architecture. Full host table and command sequences in [RECIPES.md](RECIPES.md).

## 1. Access

- **Prefer `rpi-5-direct`** (`192.168.250.2`, direct Ethernet) over WiFi aliases or the Cloudflare tunnel — the tunnel is often broken/unauthenticated and shouldn't be relied on. Full alias table in [RECIPES.md](RECIPES.md#host-access-table).
- **Account is `ralvarezdev`, not `pi`**, on both boards. Identity file: `D:\Secrets\ssh\raspberrypi\id_ed25519_ralvarezdev`.
- **Pi 5 has passwordless sudo; the Pi Zero does not.** Any `sudo` command touching the Pi Zero needs an interactive password — run those in the user's own terminal, never through a non-interactive tool call.
- **mDNS (`.local`) resolution flakes** on this network. Fall back to the raw IP with an explicit `-i` — the raw IP doesn't match the `~/.ssh/config` `Host` pattern, so the identity file isn't picked up automatically.

## 2. The edit-test loop

1. Edit `platform/robot/...` locally on Windows.
2. Commit + push to `master`.
3. `cd ~/voldemorbot && git pull` on the target Pi.
4. `pixi.toml`/`pixi.lock` changed → `~/.pixi/bin/pixi install -e dev`.
5. Any `ros2_ws/src` source changed → `~/.pixi/bin/pixi run -e dev build-ws`. **Editing source alone does nothing** — this step is what actually installs launch files and `console_scripts`.
6. Restart the service: `sudo systemctl restart voldemorbot-pi-zero.service` (or `-pi5`).
7. Verify it stuck with `systemctl status ... --no-pager -l`, then `journalctl -u ... --since 'HH:MM:SS' --no-pager -l` for the actual node output — status alone truncates it.

## 3. Regenerating `pixi.lock`

**Always lock on the Pi 5, never Windows** — Windows can't cross-build several aarch64 conda-forge sdists (e.g. `netifaces`) and `pixi lock` just hangs. The Pi 5 has 16GB RAM and is the real target arch, so it resolves cleanly and fast. Full lock-and-sync-back sequence in [RECIPES.md](RECIPES.md#regenerating-pixilock).

## 4. Surviving a flaky connection

WiFi/mDNS on this network drops mid-session often enough that anything long-running (`pixi install` fetching packages, a `colcon build`) must run inside `screen`, not foreground SSH — the process then survives the disconnect independent of the SSH session. Detach with `Ctrl+A` `D` (not `Ctrl+C`); reattach with `screen -d -r work` (the `-d` force-detaches a stale "Attached" state a plain `-r` would refuse). `/tmp` is wiped on every reboot, so anything staged there needs re-copying after one. Command sequence in [RECIPES.md](RECIPES.md#long-running-commands-over-screen).

## 5. PowerShell SSH gotcha

Don't build one SSH command string with nested double-quotes and `|` for PowerShell to parse — pipe characters get read as PowerShell's own pipeline operator mid-string, and `\"` escaping doesn't survive it. Instead, `ssh -t` into the box with no trailing command, then run the actual multi-line command block directly in the resulting Pi shell.

## 6. Sudo credential caching

A successful interactive `sudo` on the Pi Zero caches for ~15 minutes (`/run/sudo/ts/<uid>`), so a `sudo systemctl restart ...` issued non-interactively shortly after will succeed silently. Don't assume the window is still open, though — if `sudo` reports "a password is required," hand the command back to the user to run interactively rather than retrying it yourself.
