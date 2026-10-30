---
name: vpn
description: >-
  VPN setup, repair, and verification: GUI client one-button setup (v2RayTun),
  system-wide stack bootstrap and self-reflection (broken wrappers, RU-zone
  whitelists, TUN mode, autorun), sing-box TUN tunnel reference on
  Fedora/Linux, and Android VPN/proxy detection. One contract; the parts under
  parts/ carry the procedures.
---

# vpn — tunnel setup and verification

> Home branch in Memora: `root/skill/vpn`.
>
> Network, TUN, routing, and DNS changes alter machine connectivity — confirm via
> `ask_questions` with a named rollback step before applying.

## Choosing a part

| Task | Part |
|---|---|
| VPN via GUI client (v2RayTun) down to one button: deeplink import, disabling whitelists, TUN | `parts/vpn-gui-setup/` |
| Repair a broken system-wide VPN stack: direct core launch, RU-zone leak fix, TUN, Task Scheduler | `parts/vpn-stack-fix/` |
| Fedora/Linux reference for a system TUN tunnel through sing-box (`systemd`, `CAP_NET_ADMIN`) | `parts/singbox-tun/` |
| Android app detecting VPN/proxy servers (VLESS/xray/sing-box) via local SOCKS5 exposure | `parts/yourvpndead-vpn-detection/` |

## Rules

- Walk `root/skill/vpn` in Memora before modifying `_scripts/vpn-tools/` or browser rules (`gen_zeroomega_rules.py`).
- Describe verification state in plain text in chat (no caps labels).
- Confirm tunnel mode (browser-only ZeroOmega vs. system TUN) via `ask_questions` before changing routing.

## Related

`desktop` (adapter and route diagnostics), `ship` (infrastructure changes behind an approval).
