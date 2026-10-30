---
name: vpn-stack-fix
description: >-
  Self-reflection and bootstrap of a system-wide VPN stack: client wrapper
  broken → cores launch directly; "whitelists" RU-zone in subscription →
  IP-checker sites show local IP; TUN mode for entire PC; autorun via
  Task Scheduler; scripts for on/off/server switch. No real IP, country
  or provider — only generalized formulations. Triggers: "fix VPN",
  "vpn doesn't work", "happ doesn't work", "2ip shows my IP",
  "raise vpn-stack", "vpn-on", "how to fix vpn".
invocation: model+user
---
# VPN Stack Fix — how to fix and how to launch

## When to use

- User asks "fix VPN" and the GUI path doesn't work: no admin rights (UAC),
  need full control, GUI client won't fix
- On IP-checker sites (e.g. 2ip) you see **local IP** although VPN is "connected"
- VPN needed **system-wide** (entire PC), not just in browser; "without separate whitelists"
- After PC reboot VPN didn't start itself

## Core idea

**First GUI with admin rights** (see vpn-gui-setup): TUN mode of v2RayTun client was
previously observed, but current functionality is not confirmed (`unverified`) —
the key is launching with admin rights (wintun without rights doesn't create adapter).
The manual stack is a **fallback path**, when GUI isn't an option: no UAC rights, need
custom config, GUI client doesn't fit. Stack idea: launch cores directly, bypassing GUI:
xray (proxy ports 10808/10809) + sing-box TUN (entire PC). The alternative subscription/servers
were previously observed, but current accessibility is not confirmed (`unverified`);
the stack can be raised manually only after a separate check.

The second classical problem is **"whitelists" inside subscription**: the rule for
"RU zone → direct" zone. IP-checker sites with such a rule show local IP even with VPN
working. Remove the rule — and all traffic goes through VPN.

## How to fix this (self-reflection, by steps)

### Step 0. Diagnosis — what's actually broken

Don't trust "the app crashed". Check facts:

```bash
netstat -ano | grep -E "10808|10809"          # is proxy core listening
tasklist | grep -iE "xray|sing-box"            # are cores alive
ipconfig | grep -iE "tun"                      # is TUN adapter present
```

Symptom "everything empty" = core doesn't start. That's the fix point.

Fourth cause (most common for "connected but doesn't work") — **selected location is
dead**: server TCP port doesn't respond. Core listens on ports, GUI shows "connected",
outbound to server hangs. Diagnosis — parallel TCP-scan of all subscription servers
(3s timeout per server): dead ones are usually 1–2 out of ten. Switch to a live location
("Auto | Best server" if available) — and VPN works without fixing the wrapper.

### Step 1. Proxy layer: core with subscription config

Subscription gives a mass of ready configs (per location): each contains
socks-inbound on `127.0.0.1:10808` + http on `10809` + pool of vless-servers + routing.

```bash
xray.exe run -c <config_location.json>   # cwd = core folder (there geoip/geosite)
```

Check: `curl -x socks5h://127.0.0.1:10808 https://api.ipify.org` → foreign IP.
Proxy layer works without admin.

### Step 2. TUN layer: entire PC via VPN (alternative recipe, current check `unverified`)

Working sing-box config (proxy-core holds socks on 10808, TUN wraps
all system traffic into this socks):

```json
{
  "log": { "level": "info" },
  "dns": {
    "servers": [{ "type": "udp", "tag": "dns-remote", "server": "8.8.8.8", "detour": "proxy" }],
    "final": "dns-remote"
  },
  "inbounds": [{
    "type": "tun", "tag": "tun-in", "interface_name": "vpn-tun",
    "address": ["172.18.0.1/30"], "mtu": 1492,
    "auto_route": true, "strict_route": false, "stack": "mixed",
    "route_exclude_address": ["<addresses of all subscription servers>/32", "8.8.8.8/32", "8.8.4.4/32"]
  }],
  "outbounds": [
    { "type": "socks", "tag": "proxy", "server": "127.0.0.1", "server_port": 10808 },
    { "type": "direct", "tag": "direct", "bind_interface": "<real interface name>" }
  ],
  "route": {
    "final": "proxy",
    "rules": [
      { "protocol": "dns", "outbound": "dns-out" },
      { "ip_is_private": true, "outbound": "direct" },
      { "process_name": ["xraycore.exe","xraycore","xray","sing-box.exe","sing-box"], "outbound": "direct" }
    ]
  }
}
```

Each detail is a tested finding (without it TUN doesn't work):
- **`stack: mixed`** — tested variant for manual stack: process_name-rule matches.
- **`route_exclude_address` = addresses of all subscription servers (`/32`)** — core
  goes to servers directly, bypassing TUN. Without this, a loop even in mixed.
- **`bind_interface` on direct-outbound** — otherwise sing-box creates direct-connections
  with TUN address, packets go out with wrong src.
- **`strict_route: false`** — strict_route sets WFP-filters that break after kill -Force.
- **Adapter DNS forced to `8.8.8.8`** — otherwise Windows resolves via TUN address (dead peer).
- **Before starting, delete old adapter** (`Remove-NetAdapter vpn-tun`) —
  wintun after kill -Force is inaccessible ("already exists / not found").
- **Clean stale default-routes without interface** (remnants of previous launches) —
  otherwise auto_route can't create a new default.

Startup order (script, elevated): wait for proxy port (up to 90s) → kill old sing-box →
delete adapter → start sing-box → wait 8s → DNS 8.8.8.8 on adapter → if default through TUN
didn't appear — `route add 0.0.0.0 mask 0.0.0.0 172.18.0.2 metric 5 IF <ifIndex>`.

TUN requires admin (Wintun). Any `Start-Process -Verb RunAs`, adapter deletion, route
change or task launch is an external system mutation, only after explicit authorization;
without that use read-only status/help fallback of the scheduler (RunLevel Highest).

### Step 3. Remove "whitelists" (if IP-check lies)

In subscription routing there's a rule with `domain: ru-zone` → `direct`. IP-checker sites
in this zone show local IP. Delete the rule:

```python
rules = [r for r in cfg["routing"]["rules"]
         if r.get("outboundTag") != "direct" or "domain" not in r]
```

After this **all** traffic goes through VPN — "without separate whitelists".

### Step 4. Fallback path: system proxy

WinINET-proxy from registry HKCU (doesn't require admin) — duplicate path for browsers:

```powershell
Set-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' -Name ProxyEnable -Value 1
Set-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' -Name ProxyServer -Value '127.0.0.1:10809'
```

+ refresh WinINET (`InternetSetOption` 39/37) so apps pick it up immediately.

### Step 5. Autorun on login

One Task Scheduler task instead of two: script itself waits for proxy, raises TUN,
fixes DNS and route (idempotent — repeated launch restarts the stack):

```powershell
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-NoProfile -ExecutionPolicy Bypass -File <path>\tun-on.ps1'
$trigger = New-ScheduledTaskTrigger -AtLogOn
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -RunLevel Highest -LogonType Interactive
Register-ScheduledTask -TaskName 'VPNTunStack' -Action $action -Trigger $trigger -Principal $principal -Force
```

Proxy-core since 2026-08-04 starts itself (ensure-block in `tun-on.ps1`: if 10808 doesn't
listen and xraycore isn't alive — launches `~/.vpn-stack/core/xraycore.exe run --path proxy.json`;
core and geoip/geosite are pre-copied to `~/.vpn-stack/core/`, GUI client for the stack isn't needed).
Post-reboot check requires separate owner-authorized launch; `schtasks /run /TN VPNTunStack`
and system IP check remain `unverified` in read-only audit.

## How to launch (bootstrap)

Everything is in `~/.vpn-stack/` (variables, no hardcoding):

| Command | What it does |
|---|---|
| `powershell -File ~/.vpn-stack/vpn-on.ps1` | raise stack: task + system proxy, show IP |
| `powershell -File ~/.vpn-stack/vpn-off.ps1` | stop cores + TUN, disable proxy (direct internet) |
| `python ~/.vpn-stack/pick-server.py` | list of subscription locations |
| `python ~/.vpn-stack/pick-server.py "Germany"` | select location → rewrite core.json → restart |

Result check (no concrete values — only invariant):

- `https://api.ipify.org` / `2ip.ru` → **foreign IP**, not local
- system `curl https://api.ipify.org` (without proxy, through TUN) → foreign IP
- `netstat -ano | grep 10808` → LISTENING

## What NOT to do

- **Don't launch GUI client and stack simultaneously** — GUI on start kills other cores and
  conflicts for port 10808/TUN; first decide which path is main (GUI with admin — default)
- Don't fix GUI client as "broken" without checking process rights — most often TUN doesn't
  work due to launch without admin (see vpn-gui-setup)
- Don't hardcode real IP, country or provider in configs, logs and skills — only generalizations
- Don't trust "the app crashed" — check ports and processes
- Don't launch a second TUN-instance over a live one — interface is taken, second silently fails

## Success check

- [ ] Proxy-core listens on 10808/10809
- [ ] TUN adapter exists (`ipconfig | grep tun`)
- [ ] Default route goes through TUN (`route print -4`)
- [ ] IP-checker shows foreign IP
- [ ] No GUI client running simultaneously
