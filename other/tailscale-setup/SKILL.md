---
name: tailscale-setup
description: This skill should be used when the user asks to set up Tailscale, automate it via Ansible, debug "Could not connect to Tailscale / Invalid response from local service", or decide between the GUI app and a headless CLI install on macOS.
---

# Tailscale Setup (macOS dotfiles)

## Architecture — read this first

The dotfiles use the **standalone GUI app** (bundle `io.tailscale.ipn.macsys`), NOT the
brew headless `tailscale`/`tailscaled` CLI.

- The real daemon is a **macOS system extension** (`io.tailscale.ipn.macsys.network-extension`,
  runs as root). It maintains the connection and is managed by macOS, NOT by launchd.
- The **GUI app** (`/Applications/Tailscale.app`) is only a menubar controller.
- The **CLI** `/usr/local/bin/tailscale` is a symlink shipped by the app; it talks to the
  system extension directly.

Consequence: `tailscale status` can succeed while the GUI fails — they reach the extension
by different paths.

## "Could not connect / Invalid response from local Tailscale service"

This is a **GUI↔extension handshake desync** (app restarted/updated while the extension
was already running), NOT a config problem. The connection itself is fine.

**Fix (no downtime — the extension keeps the tunnel up):**
```bash
osascript -e 'quit app "Tailscale"'; sleep 2; open -a Tailscale
```
Only if that fails, restart the extension (drops the tunnel for a few seconds, needs sudo):
```bash
osascript -e 'quit app "Tailscale"'
sudo launchctl kickstart -k system/io.tailscale.ipn.macsys   # or reboot
open -a Tailscale
```

## GUI vs headless — keep the GUI on a Mac desktop

The standalone GUI is already seamless: with `TailscaleStartOnLogin = 1` it starts at login
and reconnects on its own. Going headless (brew `tailscaled` as a launchd service) loses
MagicDNS/split-DNS native integration, Sparkle auto-update, and seamless login — a net loss
on a desktop. Only go headless on a true server with no GUI.

## Ansible automation (this repo)

Two changes — see `ansible-dotfiles-setup` skill for repo structure/lint rules.

1. **Cask** in `group_vars/all/main.yml` → `brew_casks`:
   ```yaml
   - tailscale-app   # standalone GUI app, bundle io.tailscale.ipn.macsys, auto_updates
   ```
   `tailscale-app` is the GUI app. The bare `tailscale` cask name now also resolves to it,
   but use `tailscale-app` explicitly. Do NOT use the brew formula `tailscale` (headless CLI).

2. **Start-at-login** in `roles/macos/tasks/main.yml` (idempotent):
   ```yaml
   - name: Enable Tailscale start-at-login
     community.general.osx_defaults:
       domain: io.tailscale.ipn.macsys
       key: TailscaleStartOnLogin
       type: bool
       value: true
       state: present
     tags: macos
   ```

## Manual step (cannot be automated)

First install: approve the **system extension** in System Settings → Privacy & Security,
then sign in once via the menubar app (login flow goes through the GUI on macsys). Add to
the macos role's manual-steps reminder, like Karabiner.

## Verify

```bash
tailscale status                                              # CLI path (talks to extension)
defaults read io.tailscale.ipn.macsys TailscaleStartOnLogin   # → 1
ps aux | grep -i tailscale | grep -v grep                     # extension (root) + GUI (user)
```
