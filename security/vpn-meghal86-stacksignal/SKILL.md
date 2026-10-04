---
name: VPN
description: Configure and troubleshoot VPN connections for privacy and remote access.
metadata: {"clawdbot":{"emoji":"🔒","os":["linux","darwin","win32"]}}
---

## Privacy Misconceptions
- VPN shifts trust from ISP to VPN provider — provider sees all traffic, not eliminated
- "No logs" claims are marketing — unverifiable without independent audits
- VPN doesn't provide anonymity — browser fingerprinting, account logins, payment methods still identify
- Free VPNs monetize traffic data — if not paying, you're the product
- Self-hosted VPN exits from your IP — no privacy benefit, services see your home address

## DNS Leaks
- DNS queries can bypass tunnel — reveals visited sites despite encrypted traffic
- Test after every setup — leak test sites show if DNS goes through ISP instead of tunnel
- System DNS settings may override VPN — force DNS through tunnel in client settings

## Kill Switch
- Brief VPN disconnects expose real IP — happens without user noticing
- Kill switch blocks all traffic when tunnel drops — essential for privacy use cases
- Test by forcing disconnect — traffic should stop completely, not fall back to direct

## Split Tunneling Risks
- Misconfiguration sends sensitive traffic direct — defeats VPN purpose
- Full tunnel safer default — split only when deliberately excluding specific apps
- Local network access often requires split — printing, casting break with full tunnel

## Protocol Traps
- PPTP encryption is broken — trivially cracked, never use regardless of convenience
- UDP blocked on some networks — TCP fallback needed for restrictive firewalls
- WireGuard uses fixed ports — easier to block than OpenVPN on 443

## Mobile Issues
- WiFi calling fails through most VPNs — carrier limitation, not fixable
- Banking apps detect and block VPN — may need exclusion in split tunnel
- Battery drain varies significantly — WireGuard most efficient by large margin

## Connection Failures
- "Connected" but no internet — usually DNS misconfigured, not routing issue
- Works on phone not laptop — local firewall or antivirus interfering
- Constant reconnects — try TCP instead of UDP, increase keepalive interval

## Self-Hosted Traps
- Exit IP is your home IP — services see where you live, no geo-bypass benefit
- Requires static IP or dynamic DNS — clients can't find changing endpoints
- Unmaintained server becomes liability — security updates are your responsibility
