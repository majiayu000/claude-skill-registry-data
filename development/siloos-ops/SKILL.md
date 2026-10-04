---
name: siloos-ops
description: "Handles build, test, lint, and deployment operations for the SiloOS project."
---

# SiloOS Operations Skill

## Environment facts (read first)
- Pi = **Raspberry Pi 4**, hostname `SiloOS`, reachable at **`siloos.local`** (Wi-Fi `wlan0`; keep ethernet unplugged — see `siloos-pi-recovery`).
- Two systemd services, both **enabled + `Restart=always`**:
  - `scale_bridge` — Python bridge, WebSocket `:8765`.
  - `silo-dashboard` — Vite dev server (`vite --host`, dual-stack `:5173`).
- Access the dashboard at **http://siloos.local:5173/**.

## Commands

### Build Dashboard
- **Command**: `cd dashboard && npm run build`
- **Purpose**: Compile TypeScript and build the Vite production bundle.

### Lint Dashboard
- **Command**: `cd dashboard && npm run lint`
- **Purpose**: Check for code style and logic errors in the frontend.

### Sync to Raspberry Pi
- **Command**: `./sync-project.ps1`
- **Purpose**: Synchronize local changes to the Raspberry Pi and restart services.

### Manual Code Deployment (Pi)
1. **Copy Bridge**: `scp -i siloos_key ble_bridge.py siloos@siloos.local:/home/siloos/ble_bridge.py`
2. **Copy Config**: `scp -i siloos_key config.json siloos@siloos.local:/home/siloos/config.json`
3. **Restart Service**: `ssh -i siloos_key siloos@siloos.local "sudo systemctl restart scale_bridge"`
4. **Verify Logs**: `ssh -i siloos_key siloos@siloos.local "sudo journalctl -u scale_bridge -n 20 --no-pager"`

### Run Dashboard (Dev)
- **Command**: `cd dashboard && npm run dev -- --host`
- **Purpose**: Start the development server with external access enabled.

### Run Python Bridge (Local Debug)
- **Command**: `python3 ble_bridge.py`
- **Purpose**: Start the hardware bridge for local testing (requires BLE hardware).

## Managing the services
```bash
ssh -i siloos_key siloos@siloos.local "systemctl status scale_bridge silo-dashboard --no-pager"
ssh -i siloos_key siloos@siloos.local "sudo systemctl restart silo-dashboard"   # after dashboard changes
ssh -i siloos_key siloos@siloos.local "sudo journalctl -u silo-dashboard -n 30 --no-pager"
```
If a service is ever missing (`is-enabled` → `not-found`), reinstall it with `tools/install_bridge_service.sh` (bridge) or re-run `tools/pi_full_fix.sh` (both).

## Deploying over a flaky Pi link
Do NOT hand-run multi-step SSH commands when the link drops — they corrupt mid-stream. Push a script and launch it **detached** so it survives disconnects, then poll its log:
```bash
scp -i siloos_key tools/<script>.sh siloos@siloos.local:/home/siloos/
ssh -i siloos_key siloos@siloos.local "sudo systemd-run --unit=job --collect bash /home/siloos/<script>.sh"
# then: ssh ... "cat /home/siloos/<script>.log"   # poll for the completion MARKER
```
Tip: if `siloos.local` is flapping, SSH to the raw Wi-Fi IP (`10.0.124.199`) directly — flapping usually means the name is resolving to the dead `.5` (eth0).

## Deployment Procedure
1. Build local assets: `npm run build`
2. Sync to Pi using `sync-project.ps1` or manual `scp`.
3. Restart the affected service (`scale_bridge` and/or `silo-dashboard`).
4. Verify: `systemctl status scale_bridge silo-dashboard` and load http://siloos.local:5173/.
