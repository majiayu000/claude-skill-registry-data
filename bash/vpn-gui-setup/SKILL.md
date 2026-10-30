---
name: vpn-gui-setup
description: >-
  Set up VPN via GUI client (v2RayTun) to a single button: installation,
  subscription import via deeplink without manual clicks, disabling
  "whitelists" at config level, TUN mode, one-button control.
  Self-reflection: GUI buttons are unreliable, Flutter doesn't support
  PrintWindow, deeplink is a deterministic path, config is JSON in
  shared_preferences. No real IP/country/provider. Triggers:
  "set up VPN", "v2raytun", "single VPN button", "disable whitelist",
  "vpn gui".
invocation: model+user
---
# VPN GUI Setup — single-button VPN

## When to use

- User wants VPN with GUI: "open → press button → it works"
- Subscription already exists, need to import it into client and disable whitelists
- No manual scripts/autorun needed — GUI-only control

## Core idea

GUI client (v2RayTun) is a working option when its button is functional.
Three things make it a "single-button solution":

1. **Subscription import without manual clicks** — via deeplink protocol
2. **Whitelists disabled at config level** — direct JSON editing
3. **TUN mode** — system-wide VPN (entire PC), controlled by one button

## Step 1. Installation (Windows)

- Official client website → Download → run `.exe` installer (Inno Setup)
- Silent installation with custom folder:
  `setup.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP- /DIR="<folder>"`
- IMPORTANT: without `/DIR` the installer may "succeed" without installing
  anything — always specify `/DIR` and verify the exe appeared
- Application is Flutter-based (app.so, native DLLs), core unpacks to Temp on launch

## Step 2. Data and config

Everything is stored in a single JSON (shared_preferences Flutter):
`%APPDATA%\<client>\<client>\shared_preferences.json`

Keys:
- `flutter.configurations` — list of config IDs (subscription expands per-server)
- `flutter.config_<id>` — JSON-string: `{configType, remarks, subscriptionId, xrayFullConfig}`;
  `xrayFullConfig` — string with FULL xray config (inbounds/outbounds/routing)
- `flutter.selected_config` — currently selected config
- `flutter.settings_pref_vpn_mode` — `tunnel` (system TUN) or `proxy`
- `flutter.subscriptions` — subscription ID

## Step 3. Subscription import via deeplink (no GUI)

Client registers a custom protocol (e.g. `v2raytun://`) in the registry:
`HKCR\<scheme>\shell\open\command` → `"<path>\client.exe" "%1"`

Import subscription:
```bash
client.exe "v2raytun://import?url=<URL-ENCODED-subscription-link>"
```

Log should show "Deeplink received" → subscription imported.
Verify: `flutter.subscriptions` and `flutter.configurations` are populated.

## Step 4. Disable whitelists at config level

Subscription configs contain a "RU zone → direct" rule — IP-checker sites
(e.g. 2ip) show the real IP even with VPN active.

Fix (script, across all configs):
```python
for key, value in prefs.items():
    if not key.startswith('flutter.config_'): continue
    obj = json.loads(value)
    xc = json.loads(obj['xrayFullConfig'])
    xc['routing']['rules'] = [r for r in xc['routing']['rules']
                              if not (r.get('outboundTag') == 'direct' and 'domain' in r)]
    obj['xrayFullConfig'] = json.dumps(xc, ensure_ascii=False)
    prefs[key] = json.dumps(obj, ensure_ascii=False)
```
→ restart the application. Now **all** traffic goes through VPN.

WARNING: the "Update subscription" button in the client will restore the rule — re-run the fix.

## Step 5. TUN mode and connection

- `flutter.settings_pref_vpn_mode = tunnel` — entire PC through VPN
- Connection: one button in GUI → core starts, listens on ports, TUN adapter rises, IP is foreign

## Step 6. VPN "connected" but traffic doesn't go — step-by-step diagnosis

Symptom: button is pressed, but IP-checker sites show local IP (or nothing).
Don't trust the GUI — check facts, in this order:

1. **Is the core alive?** `netstat -ano | grep LISTENING` on proxy ports (10808/10809).
   Empty → core didn't start/crashed. Restart the app; core configs are in the
   temp folder (`connection.json`/`tunnel.json`) — manual core launch with them
   shows if the core itself works (starts and listens → problem is in the wrapper).
2. **Whitelists?** The selected config has a `direct` rule for RU zone →
   Step 4 (remove) + restart.
3. **Is the server alive?** Most common "connected but doesn't work" cause —
   **selected location is dead**: TCP port of the server doesn't respond.
   Collect all subscription servers (address+port from `xrayFullConfig` of each config)
   and scan them in parallel (TCP connect, 3s timeout): out of ten locations 1–2 are dead.
   Switch `flutter.selected_config` to a live one → restart. Scanner takes ~3 seconds.
4. **TUN not rising?** First check RIGHTS, then theory: TUN requires launch
   **as administrator** — wintun without rights silently fails to create adapter
   (GUI says "doesn't work", no adapter). Check rights: taskkill-probe of the process
   ("Access denied" = elevated), CIM `Win32_Process` CommandLine empty for non-elevated reader = elevated.
   Elevated instance raises the adapter, routes and pushes traffic. Only if rights exist
   and TUN still doesn't work — examine core configs/logs (`connection.json`/`tunnel.json` in Temp).

Post-check (owner-authorized): `curl -x socks5h://127.0.0.1:10808 https://api.ipify.org`;
in read-only audit external fetch and system IP check remain `unverified`.

## Self-reflection — lessons learned (may repeat)

| Lesson | Detail |
|---|---|
| GUI buttons are unreliable | If another app overlays (chat, terminal) — software clicks miss; foreground-check is mandatory |
| Flutter doesn't support PrintWindow | GPU rendering: `PrintWindow(PW_RENDERFULLCONTENT)` gives empty; only CopyFromScreen of visible window |
| Coordinates drift | Window position and layout change between launches; blind clicks by %-coords are unreliable |
| Deeplink — deterministic path | Protocol `scheme://import?url=` imports subscription WITHOUT GUI — this is the main automation approach |
| Config — JSON in shared_preferences | Editable by script directly (whitelists, mode, selection); app re-reads on restart |
| GUI client kills other cores | On launch kills other xray-processes and conflicts for ports/TUN with manual stack |
| One click — for a human | Automation of clicks from under another window is unrealistic |
| "Connected but doesn't work" ≠ wrapper | Most often the selected location is dead — parallel scan of all servers in ~3s finds a live one |
| TUN works — the key is elevated | GUI without "Run as administrator" silently fails to create TUN adapter (wintun) |
| Deeplink commands | `v2raytun://control/start\|stop\|restart\|update\|reset-settings` processed per-instance, not globally |
| TUN requires elevated; elevated-process can't be killed without rights | Non-elevated instance doesn't create adapter; elevated does and works |
| Flutter window doesn't restore via ShowWindow | Window in tray (rect -32000,-32000): diagnose via deeplink and observable facts instead |

## What NOT to do

- Don't mix GUI client with manual stack (port and TUN conflict)
- Don't rely on blind clicks if the window is overlaid by another app
- Don't hardcode real IP/country/provider in skills and configs — only generalizations
- Don't forget: "Update subscription" restores whitelists — re-run the fix

## Success check

- [ ] Subscription imported (deeplink "Deeplink received", configs in shared_preferences)
- [ ] Whitelists removed: `domain:ru`/`category-ru` absent from configs
- [ ] Mode `tunnel`, after button press: core listens on ports, TUN adapter exists
- [ ] IP-checker site shows foreign IP, not local
- [ ] No autorun/scripts — control only by GUI button
