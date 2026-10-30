---
name: singbox-tun
description: 'Fedora/Linux reference for a system TUN tunnel through sing-box. Installation, systemd, CAP_NET_ADMIN, routing and DNS changes are mutation procedures requiring explicit authorization.'
---


# singbox-tun — all system traffic through proxy (TUN)

Full system-level tunnel: all applications (browser, torrents, messengers)
go through the selected proxy. Provider sees only the proxy IP, DNS requests
also go through the proxy (domains are hidden).

Diagram:

```
Applications → TUN (sing-tun) → urltest (best proxy selection) → SOCKS5 proxy → internet
                                   └─ DNS: tls://1.1.1.1 via proxy (domains hidden)
```

## Installation (Fedora, official repository)

```bash
sudo dnf config-manager addrepo --from-repofile=https://sing-box.app/sing-box.repo
sudo dnf install sing-box          # verify: sing-box version
```

The package already installs the systemd unit `/usr/lib/systemd/system/sing-box.service`
with `AmbientCapabilities=CAP_NET_ADMIN CAP_NET_RAW` and user `sing-box` —
TUN works WITHOUT root and without sudo hacks.

## Config

File: `/etc/sing-box/config.json`. Full working example (verified on 1.13.18) —
in `references/config.example.json`. Key nodes:

- **inbound**: `tun` (`auto_route: true`, `strict_route: true`, `stack: "system"`) — pulls all traffic
- **outbounds**: SOCKS5 with `username`/`password` (auth supported!) + `urltest` group for auto-switching
- **DNS**: `tls://1.1.1.1` with `detour: "auto"` — resolving through proxy
- **route**: `final: "auto"` — all unmatched traffic into proxy; local network (`ip_is_private`) — direct (so printers/router don't break)

## Running and verification

```bash
sudo systemctl enable --now sing-box
systemctl is-active sing-box                 # active
