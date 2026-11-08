---
name: mac-network
description: Read a Mac's network state from the shell — which interface is live, IP and gateway, Wi-Fi signal, DNS servers, proxies, what is listening on which port, and whether a host is reachable — and the two safe fixes (flush DNS, renew DHCP) that need a human's password. Use when you say "what's my IP", "am I on Wi-Fi or ethernet", "what's on port 3000", "something is already using this port", "is DNS broken", "flush my DNS", "is there a proxy set", "why can't I reach X". Read-only by default.
compatibility: >-
  macOS (tested on macOS 26, Apple silicon). Built-in tools only: networksetup, route, ipconfig, ifconfig, scutil, lsof, nc, dscacheutil, system_profiler. No network hosts of its own.
metadata:
  grounded: "2026-11-03 — every read run live on macOS 26.6; no setting changed"
---

# Mac network state

## Which interface, which address

```bash
route -n get default | grep -E "interface|gateway"   # the interface traffic actually uses
ipconfig getifaddr en0                               # IPv4 of an interface
ifconfig en0 | grep -E "inet |status"
networksetup -listallhardwareports                   # port name <-> device (Wi-Fi = en0 on most Macs)
networksetup -listnetworkserviceorder
```

Use the **interface from `route get default`**, not an assumed `en0`; on a docked laptop the
live link is often a USB/Thunderbolt Ethernet (`en3`, `en5` ...). `networksetup` commands
take the *service name* (`"Wi-Fi"`, `"USB 10/100/1000 LAN"`), not the device.

## Wi-Fi

```bash
ipconfig getsummary en0 | grep -E "^\s*(SSID|Security)"
system_profiler SPAirPortDataType | grep -E "PHY Mode|Channel|Signal / Noise|Transmit Rate" | head -4
```

- **The SSID is redacted on modern macOS** (`SSID : <redacted>`) unless the calling app has
  Location Services. Verified on macOS 26.
- **`networksetup -getairportnetwork en0` says `You are not associated with an AirPort
  network.` even while connected**, for the same reason. Don't conclude Wi-Fi is down
  from it; check `ifconfig en0 | grep status` and `route get default`.
- The `airport -I` binary older guides use was removed. Signal (`-57 dBm / -96 dBm` noise)
  from `system_profiler` still works; above about -67 dBm is fine for calls.

## DNS

```bash
scutil --dns | grep nameserver | sort -u        # the resolvers actually in use
networksetup -getdnsservers Wi-Fi               # manual override, if any
dscacheutil -q host -a name example.com         # resolve through the system resolver
```

`There aren't any DNS Servers set on Wi-Fi.` means **DHCP-provided DNS**, which is normal.
Use `dscacheutil` (or `ping`, `curl`) to test resolution, not `dig`/`nslookup`: those skip
the system resolver, so `/etc/hosts`, VPN split DNS and profiles don't apply to them.

Flush the cache (needs the user's password, harmless):

```bash
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

## Proxies and VPN

```bash
scutil --proxy                                   # effective proxy config
networksetup -getwebproxy Wi-Fi; networksetup -getsecurewebproxy Wi-Fi
scutil --nc list                                 # configured VPNs and their state
```

A proxy here, or a VPN in `scutil --nc list` showing `(Connected)`, explains "curl works
but the app doesn't" (or the reverse).

## Ports: what is listening, who holds port N

```bash
lsof -nP -iTCP -sTCP:LISTEN                      # everything listening, with process + pid
lsof -nP -iTCP:3000 -sTCP:LISTEN                 # who has port 3000
lsof -nP -iUDP:5353
```

- `-n -P` skip DNS and port-name lookups; without them `lsof` is slow and prints `http`
  instead of `80`.
- You only see **your own** processes without `sudo`. A port that's busy but shows nothing
  is held by root or another user.
- On recent macOS, AirPlay Receiver (`ControlCenter`) **listens on 5000 and 7000**, the
  classic "port 5000 already in use" for local dev servers. Pick another port, or the user
  can turn off AirPlay Receiver in System Settings > General > AirDrop & Handoff.
- Freeing a port means stopping the process that holds it. Name it and its pid; stopping it
  is the user's call.

## Reachability

```bash
nc -z -w2 example.com 443 && echo open           # TCP port reachable
curl -sS -o /dev/null -w "%{http_code} %{time_total}s\n" https://example.com
ping -c 3 192.168.1.1                            # gateway from route get default
networkQuality -s                                # Apple's speed test (uses Apple's servers)
```

## Changing settings (only when asked)

All of these change the machine and most need an admin password:

```bash
sudo ipconfig set en0 DHCP                       # renew a DHCP lease
networksetup -setdnsservers Wi-Fi 1.1.1.1 8.8.8.8   # set manual DNS
networksetup -setdnsservers Wi-Fi empty             # back to DHCP DNS
networksetup -setairportpower en0 off && networksetup -setairportpower en0 on
```

Toggling Wi-Fi drops every connection, including the session you're running in if it's
remote. Say so first.
