---
name: siloos-pi-recovery
description: "Diagnose and recover SiloOS 'not connecting' when the Pi's IP has drifted, a rogue local mock is impersonating the Pi, or the Pi's SSH/bridge services are down."
---

# SiloOS Pi Recovery Skill

## When to Use
- The dashboard "won't connect" but you're not sure where the failure is.
- `siloos.local` / a hardcoded Pi IP no longer works.
- You suspect the Pi's DHCP address drifted again.
- A previous session left a local mock (`ble_bridge.py` / `tools/mdns_publisher.py`) running on the dev laptop.

## Key Facts (learned 2026-08-10)
- **The Pi is a Raspberry Pi 3B+**: its MAC starts with the Raspberry Pi OUI **`b8:27:eb`** (older Pis) or `dc:a6:32` / `e4:5f:01` (Pi 4+). Use this to find it in the ARP table regardless of IP.
- **Target static IP**: `10.0.124.5`, mask `255.255.255.0`, gateway `10.0.124.1`. Setup script: `tools/set_pi_static_ip.sh`.
- **The dashboard's runtime WebSocket URL is dynamic** (`dashboard/src/bluetooth/SiloManager.ts` builds it from `window.location.hostname:8765`). Only Vite HMR (`vite.config.ts`) and deploy tooling (`sync-dashboard.ps1`) ever hardcode the Pi address — now set to `siloos.local`.
- **`tools/mdns_publisher.py` is a DEV-ONLY MOCK.** It advertises `siloos.local` as the *laptop's* IP. If left running it hijacks the name away from the real Pi. Never leave it running against real hardware.

## Diagnostic Procedure (run from the Windows dev laptop)

### Step 1: Rule out a rogue local mock FIRST
A prior agent may have left a fake bridge + mDNS advertiser on this laptop. These make things look "connected" while nothing reaches real hardware.
```powershell
# Is anything impersonating the bridge locally?
Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue |
  ForEach-Object { Get-CimInstance Win32_Process -Filter "ProcessId=$($_.OwningProcess)" |
  Select-Object ProcessId, CommandLine }
# Look for python running ble_bridge.py or tools/mdns_publisher.py
```
If found, **kill them** (they are not the real Pi):
```powershell
Stop-Process -Id <PID> -Force
```

### Step 2: Confirm what `siloos.local` resolves to
```powershell
[System.Net.Dns]::GetHostAddresses("siloos.local") | Select-Object IPAddressToString
Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like '10.0.124.*' } | Select IPAddress
```
If `siloos.local` resolves to **this laptop's own IP**, the mDNS name is hijacked (see Step 1).

### Step 3: Find the REAL Pi by MAC in the ARP table
```powershell
arp -a | Select-String "b8-27-eb|dc-a6-32|e4-5f-01"
```
The matching IP is the real Pi. (On 2026-08-10 it was `10.0.124.125`.)

### Step 4: Probe the Pi's services
```powershell
$pi = "10.0.124.125"   # <-- the IP from Step 3
Test-Connection $pi -Count 2 -Quiet                                   # ICMP up?
(Test-NetConnection $pi -Port 22   -WarningAction SilentlyContinue).TcpTestSucceeded   # sshd
(Test-NetConnection $pi -Port 8765 -WarningAction SilentlyContinue).TcpTestSucceeded   # bridge
```
Interpretation:
| ping | ssh(22) | bridge(8765) | Meaning |
|------|---------|--------------|---------|
| ✅ | ✅ | ✅ | Healthy — go debug at the app layer (`siloos-ble-debug`). |
| ✅ | ✅ | ❌ | OS up, bridge service down → `sudo systemctl restart scale_bridge`. |
| ✅ | ❌ | ❌ | OS up but sshd down → **need console/ethernet access** (see below). |
| ❌ | ❌ | ❌ | Wrong IP or Pi offline → recheck ARP / power. |

## Gotcha: IPv4 dead while IPv6 works (dead preferred route)
Symptom: `curl http://siloos.local:5173/` returns 200 but `curl -4 http://siloos.local:5173/` returns `000`; TCP to the Wi-Fi IP fails; SSH to `siloos.local` flaps but SSH to `10.0.124.199` is instant. Cause: the Pi is multi-homed and a **dead interface is the preferred IPv4 route**, black-holing IPv4.
```bash
# On the Pi — find the dead-but-preferred interface:
ip route                                   # lower metric = preferred
ping -c2 -I eth0  10.0.124.1               # 100% loss = dead link
ping -c2 -I wlan0 10.0.124.1               # 0% loss  = healthy
```
Fix: take the dead interface out of the routing. Keep its cable unplugged; and/or:
```bash
ETHCON=$(nmcli -t -f NAME,DEVICE connection show | awk -F: '$2=="eth0"{print $1;exit}')
sudo nmcli connection modify "$ETHCON" connection.autoconnect no
sudo nmcli connection down "$ETHCON"
```
Then `siloos.local` re-resolves to the working Wi-Fi IP and IPv4 works. Script: `tools/pi_eth0_off.sh` (includes a 5-min auto-restore safety — cancel it with `sudo systemctl stop eth0-safety.timer` once verified).

## Dashboard must bind dual-stack
`siloos.local` has an IPv6 (AAAA) record. If the dashboard binds IPv4 only (`vite --host 0.0.0.0`), IPv6 mDNS clients get a dead port while the bridge (dual-stack) still answers — looks "port-specific." Run Vite with `--host` (no value) so it binds `*:5173` (IPv4+IPv6). Verify: `ss -tln | grep 5173` should show `*:5173` or both `0.0.0.0` and `[::]`.

## Recovery: when SSH is down (console or ethernet access required)
You cannot fix a Pi with no SSH remotely. Options:
1. **Ethernet cable** direct to the Pi — it will pull a DHCP address on `eth0`; find it via ARP (Step 3) and SSH to that.
2. **Keyboard + monitor** on the Pi for direct console.
3. **SD card** in a reader on another machine to inspect/repair boot + service config.

Once you have a shell on the Pi:
```bash
# Bring services back
sudo systemctl enable --now ssh
sudo systemctl status scale_bridge --no-pager
sudo systemctl enable --now scale_bridge
sudo journalctl -u scale_bridge -n 50 --no-pager   # why did it die?

# Pin the address so this never recurs
bash tools/set_pi_static_ip.sh        # sets 10.0.124.5 static (see script header)
```

## Verify end-to-end
```powershell
ping 10.0.124.5
ssh -i siloos_key siloos@10.0.124.5 "systemctl is-active ssh scale_bridge"
curl -s -o NUL -w "%{http_code}" http://10.0.124.5:8765/    # bridge listening?
```
Then load the dashboard against `siloos.local` / `10.0.124.5` and confirm a live weight stream + BLE status.

## Prevention
- Keep the Pi on a **static IP** (`tools/set_pi_static_ip.sh`) or a router DHCP reservation for its MAC.
- Never leave `tools/mdns_publisher.py` running — it's a mock for laptop-only dev.
- Prefer `siloos.local` over raw IPs in tooling so an IP change doesn't require code edits.
