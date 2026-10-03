---
name: victron-cerbo-modbus-device-onboarding
description: Use when a new Victron Modbus-TCP device (EV Charging Station, energy meter, inverter) is connected to the Cerbo GX LAN but does not appear in the Cerbo UI or D-Bus, despite being reachable via ping. Trigger on phrases like "EVCS not visible in Cerbo", "new Modbus device does not appear", "Cerbo does not detect wallbox", "dbus-modbus-client does not find device", "Victron device not showing in GX", "Cerbo Device List empty even though device is on the network". Do NOT load for VE.Can/VE.Bus devices (different bus protocol), for Cerbo-Setup-from-scratch (different skill scope), or for VRM cloud connectivity problems.
---

# Victron Cerbo GX — Onboarding a new Modbus-TCP device

> Pattern verified against a real Cerbo GX with a JK-BMS that remained invisible at the Modbus layer despite correct VLAN routing. The non-obvious cause is the per-port `Enabled=0` factory-default. The 5-step sequence + `dbus-send` fix is the deterministic onboarding workflow; the fallback branch covers `Enabled=1` cases where the device is still invisible.

## The non-obvious problem

`dbus-modbus-client` discovers new Modbus devices via TCP subnet scan (port 502, every 25 s) — creates settings in `localsettings` and sets **`Enabled = 0` as the default**. The device is registered but invisible. No hint in the log, no error in the UI.

Applies to all Victron Modbus-TCP devices: EV Charging Station, Carlo Gavazzi meters, SolarEdge, external inverters.

## Diagnostic sequence (5 steps)

SSH access pattern (replace placeholders with your own credentials and hosts):
```bash
ssh -J <your-jumphost-user>@<your-jumphost-ip> root@<cerbo-ip>
```

Note: the Cerbo's `root` SSH access is enabled via the Cerbo UI under **Settings → General → Access Level → Superuser**. Use `ssh-copy-id` to set up key-auth and avoid password prompts. Do NOT hardcode passwords into shell scripts or skill bodies.

### 1 — Network check
```bash
ping -c 2 <device-ip>
```
No response → LAN/VLAN problem, check DHCP. Response → continue.

### 2 — D-Bus check
```bash
dbus -y | grep -i "evcharger\|evc_\|<device-type>"
```
Empty → settings problem (`Enabled=0` candidate). Service visible → check UI refresh / VRM cache.

### 3 — Read the modbus-client log
```bash
cat /var/log/dbus-modbus-client/current | tr -d "\000" | grep -v "^$" | tail -30
```
Watch for these patterns:
- `Found EV charger: Victron Energy AC22NS` → device detected ✓
- `Setting /Settings/Devices/<id>/Enabled does not exist yet` → default-Enabled problem

### 4 — Check the Enabled value
```bash
dbus -y com.victronenergy.settings /Settings/Devices/<device-id>/Enabled GetValue
```
Returns `0` → that's the bug. Device-ID from log (format: `evc_<Serial>`).

### 5 — Fix: set Enabled to 1
```bash
dbus-send --system --print-reply \
  --dest=com.victronenergy.settings \
  /Settings/Devices/<device-id>/Enabled \
  com.victronenergy.BusItem.SetValue \
  variant:int32:1
```
Return `int32 0` = success. Device appears in D-Bus and the Cerbo UI within a few seconds.

### Fallback: Enabled=1 set but device still not visible

```bash
# Restart the service (re-reads settings)
killall dbus-modbus-client
# Cerbo waits ~25s for dbus-modbus-client to rescan — then check again:
dbus -y | grep -i evc_
```

## Alternative path (without SSH)

Cerbo Remote Console (web UI on port 80 or via VRM) → **Settings → Device List** → find device → toggle Enable.

## BusyBox compatibility on Venus OS

Standard GNU flags do not work on the Cerbo — use BusyBox variants:

| What you want | GNU (does not work) | BusyBox (works) |
|---|---|---|
| Limit bytes | `cat file \| head -c 2000` | `cat file` (truncate if needed) |
| Processes | `ps aux` | `ps` (no flag) |
| Read file with NUL bytes | `cat file` | `cat file \| tr -d "\000"` |

## Example setup (anonymized reference)

| Device | IP (example) | Serial (example) | D-Bus path |
|---|---|---|---|
| Victron EVCS NS | `<charger-ip>` | `<charger-serial>` | `com.victronenergy.evcharger.evc_<charger-serial>` |
| Cerbo GX | `<cerbo-ip>` | `<cerbo-serial>` | — |
| SSH Jump-Host (optional) | `<user>@<jumphost-ip>` | — | e.g. Tailscale, WireGuard |

SSH pattern (use key-auth, never hardcoded passwords):
```bash
ssh -J <user>@<jumphost-ip> root@<cerbo-ip>
```

## Background: TDD log (Bulletproofing-Log)

### Cycle 1 — 2026-05-27 (PASS)

- **RED sub-agent** (without skill): Suggested generic steps — check Modbus TCP settings, power-cycle, VLAN, firmware compatibility. Explicitly admitted "I don't know the concrete onboarding protocol for this device class". No knowledge of the `Enabled=0` default — would lead to long false-trail diagnostics.

- **GREEN sub-agent** (with skill): Directly applied the 5-step sequence, `dbus -y` → `dbus-send` fix within seconds. Self-reflection: missing fallback branch when `Enabled=1` but still no device → polish item integrated directly (`killall dbus-modbus-client`).

- **Refactor**: Fallback section added after step 5. Do-NOT-load clause added. No R1-R3 needed.

### Cycle-2 backlog (polish, non-blocking)

1. **Multi-device onboarding**: when 2+ Modbus devices appear on the LAN simultaneously — identify device IDs in the log when multiple `Found` lines appear
2. **VRM remote activation**: when SSH access is not possible (e.g. Cerbo behind NAT without VPN) — document the VRM Console path in more detail
3. **Automatic Enable on first discovery**: long-term a Cerbo update might change the default → check whether Venus OS 3.4+ handles this differently
