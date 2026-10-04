---
name: sovereign-lockdown
description: "Apply the full DSH sovereign lockdown: kill known phone-home daemons (Google, Zoom, CodeWhisperer), pin DNS to dnscrypt-proxy, enable firewall + stealth, install a pf anchor blocking telemetry endpoints, and permanently remove unauthorized LaunchAgents. Verifies with audit.sh + dome-check.sh and surfaces any remaining gaps."
---

You are hardening the local machine into a sovereign state where nothing calls home, no unauthorized background daemon persists, and network traffic is policy-gated. This is invasive — every step needs the user's sudo once, and you MUST surface what each phase changes before running.

## 1. Confirm intent

Before touching the system, show the user what will happen:

```
Sovereign Lockdown will:
  • enable macOS firewall + stealth mode (blocks unsolicited inbound)
  • remove ~/Library/LaunchAgents entries not in the approved list
    (Google updater, Zoom daemon, CodeWhisperer, etc.)
  • pin DNS to 127.0.0.1 (dnscrypt-proxy must be running)
  • install a pf anchor blocking known telemetry endpoints
  • set pmset: no sudden-motion-sensor, no powernap, destroy FV key on standby
  • disable AirPlay Receiver (closes ports 5000/7000)
```

Require an explicit "yes" to proceed. If the user hesitates, offer to run only `lock-down.sh` (phase 1, least invasive) and skip phases 2–4.

## 2. Run phase 1 — kill daemons + pin DNS

```bash
bash "$DOME_ROOT/scripts/lock-down.sh"
```

Prompts for sudo once, keeps credential alive for the whole run. What it does:

- `launchctl unload -w` + `rm` on unauthorized user LaunchAgents
- `launchctl bootout system` on unauthorized system daemons
- `sudo networksetup -setdnsservers Wi-Fi 127.0.0.1`
- `sudo brew services start dnscrypt-proxy`
- Kills any running processes of the daemons it just removed

Verify before proceeding:

```bash
pgrep -x dnscrypt-proxy >/dev/null && echo "✓ dnscrypt-proxy running" || echo "✗ MISSING"
scutil --dns | grep -m1 nameserver | awk '{print $3}'   # should be 127.0.0.1
```

## 3. Run phase 2 — firewall + stealth + hardware tuning

```bash
bash "$DOME_ROOT/scripts/lock-down-phase2.sh"
```

Enables the application firewall, stealth mode (no ICMP reply), logging; sets pmset for secure standby; disables sudden-motion-sensor; increases file/proc limits.

Verify:

```bash
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate     # "State = 2" = blocking
/usr/libexec/ApplicationFirewall/socketfilterfw --getstealthmode     # "on"
```

## 4. Run phase 3 — pf anchor for telemetry endpoints

```bash
bash "$DOME_ROOT/scripts/lock-down-phase3.sh"
bash "$DOME_ROOT/scripts/pf-reload.sh"
```

Writes `/etc/pf.anchors/com.dsh` with block rules for known telemetry TCP/UDP ports (5228/5229/5230 Google push, 5353 mDNS, etc.) and reloads pf.

Verify:

```bash
sudo pfctl -sa | grep com.dsh        # anchor loaded
sudo pfctl -a com.dsh -s rules       # rules active
```

## 5. Run phase 4 — daemon audit + permanent removal

```bash
bash "$DOME_ROOT/scripts/lock-down-phase4.sh"
```

Strictest phase: scans `/Library/LaunchDaemons` and `~/Library/LaunchAgents` in a loop, permanently removes any plist not matching the approved allowlist (`homebrew.*`, `com.apple.*`, `com.openssh.*`, `org.cups.*`). Logs every removal to `logs/daemon-watch.log`.

Prompt before: some apps (e.g. Dropbox, 1Password) install LaunchAgents the user may actually want. If you see a removal that looks legitimate, pause and ask.

## 6. Verify the end state

Run the three audit commands and require all green:

```bash
bash "$DOME_ROOT/scripts/audit.sh"         # security posture check
bash "$DOME_ROOT/scripts/dome-check.sh"    # full protocol enforcer (includes machine-probe refresh)
"$DOME_ROOT/.venv/bin/python" -c "
import sys; sys.path.insert(0, '$DOME_ROOT')
from agents.core.machine import security_posture
import json
print(json.dumps(security_posture(), indent=2))
"
```

Expected `security_posture()` after lockdown:

```json
{
  "filevault": true,
  "sip": true,
  "gatekeeper": true,
  "firewall": true,
  "dns_private": true,
  "secrets_backend_present": true
}
```

If any value is `false`, tell the user exactly which check and the exact fix command (see the per-phase verify steps above).

## 7. Schedule ongoing enforcement

The setup script should have installed a cron entry for `dome-check.sh` every 6h. Confirm:

```bash
crontab -l | grep dome-check
```

If missing, add it:

```bash
(crontab -l 2>/dev/null | grep -v dome-check; echo "0 */6 * * * cd $DOME_ROOT && bash scripts/dome-check.sh >> logs/dome-check.log 2>&1") | crontab -
```

## 8. Report

Single-block summary for the user:

```
✅ Sovereign Lockdown complete
✅ Firewall + stealth active
✅ DNS pinned to dnscrypt-proxy
✅ pf anchor loaded (com.dsh)
✅ N unauthorized LaunchAgent(s) removed → logs/daemon-watch.log
✅ dome-check.sh scheduled every 6h
```

If any step was skipped or failed, say so explicitly. No lockdown theater.

## Non-negotiables

- **Never proceed past a failing phase.** If phase 1 fails (dnscrypt-proxy won't start), phase 3's pf anchor will leak DNS.
- **Never remove a daemon the user depends on without asking.** 1Password Agent, Dropbox, Tailscaled are legitimate.
- **FileVault cannot be auto-enabled.** If `security_posture()['filevault']` is False, tell the user to enable it manually in System Settings → Privacy & Security → FileVault.
- **SIP cannot be enabled from a running system.** It requires a reboot into Recovery — if disabled, that's a user task, not this skill's.
- **Reversing lockdown** is not this skill's job. If the user wants to undo, point them to `sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off` and `sudo networksetup -setdnsservers Wi-Fi empty`.
