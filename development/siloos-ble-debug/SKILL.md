---
name: siloos-ble-debug
description: "Troubleshooting TopBrewer BLE connection, GATT errors, and WebSocket relay issues."
---

# SiloOS BLE Debug Skill

## When to Use
- TopBrewer is not responding to commands
- BLE connection drops repeatedly
- Notifications are not being received
- GATT read/write operations timeout

> **First rule out the network.** If the dashboard can't reach the bridge at all (WebSocket won't open, `siloos.local` unreachable, page won't load), that's a connectivity problem — use the **`siloos-pi-recovery`** skill, not this one. This skill assumes the bridge is up and reachable and the issue is at the BLE/GATT layer.

## Prerequisites
- SSH access to Raspberry Pi (`ssh -i siloos_key siloos@siloos.local`)
- TopBrewer machine is powered on and within BLE range
- `ble_bridge.py` service is running

## Procedure

### Step 1: Check Service Status
```bash
ssh -i siloos_key siloos@siloos.local "sudo systemctl status scale_bridge"
```
Expected: `Active: active (running)`

### Step 2: Check Recent Logs
```bash
ssh -i siloos_key siloos@siloos.local "sudo journalctl -u scale_bridge -n 50 --no-pager"
```
Look for:
- `BLE connected` — TopBrewer connection established
- `BLE disconnected` — Connection lost (check range, power)
- `GATT error` — Protocol issue (check characteristic UUIDs)

### Step 3: Verify BLE Adapter
```bash
ssh -i siloos_key siloos@siloos.local "bluetoothctl show"
```
Expected: `Powered: yes`, `Discovering: no` (scan should be off when connected)

### Step 4: Reset BLE Adapter (if stuck)
```bash
ssh -i siloos_key siloos@siloos.local "bluetoothctl power off && sleep 2 && bluetoothctl power on"
```

### Step 5: Scan for TopBrewer
```bash
ssh -i siloos_key siloos@siloos.local "python3 find_machine.py"
```
Expected: Device with MAC `88:6B:0F:BC:00:A1` should appear

### Step 6: Restart Bridge
```bash
ssh -i siloos_key siloos@siloos.local "sudo systemctl restart scale_bridge"
```

### Step 7: Verify WebSocket
From development machine, check if WebSocket is accepting connections:
```bash
curl -s -o /dev/null -w "%{http_code}" http://siloos.local:8765/
```
Expected: HTTP response (indicates aiohttp is listening)

## Expected Outcomes
- BLE connection re-established
- WebSocket relay operational
- Notifications flowing from TopBrewer to dashboard

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Powered: no` | BLE adapter disabled | `bluetoothctl power on` |
| Device not found | Out of range or powered off | Move Pi closer, check TopBrewer power |
| `GATT error` | Stale connection | Restart bridge service |
| `Permission denied` | Missing BLE permissions | Run `sudo usermod -a -G bluetooth siloos` |
| WebSocket refused | Bridge crashed | Check logs, restart service |
