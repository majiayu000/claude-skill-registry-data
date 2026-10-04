---
name: Smart Home
description: Set up, automate, secure, and troubleshoot smart home devices with protocol selection, network isolation, and ecosystem-agnostic automation patterns.
---

## Decision Tree

| Situation | Action |
|-----------|--------|
| Starting from scratch | Check `setup.md` for protocols, hubs, and first purchases |
| Inheriting existing devices | Check `takeover.md` for reset, claiming, and security audit |
| Adding automations | Check `automations.md` for patterns by room and scenario |
| Security/privacy setup | Check `security.md` for VLAN, credentials, local-first options |
| Device not working | Check `troubleshooting.md` for common issues by device type |
| Renting (no permanent changes) | Check `renters.md` for portable and non-invasive options |

---

## Universal Rules

**Protocol choice matters more than brand.** Matter and Thread are the future. Zigbee and Z-Wave are mature and reliable. WiFi devices clog your network. Pick a protocol, build around it.

**Local control beats cloud.** When the internet dies, your lights should still work. Home Assistant, Hubitat, and HomeKit prioritize local. Google Home and Alexa are cloud-first.

**Network segmentation is non-negotiable.** IoT devices belong on a separate VLAN. They don't need access to your laptop, NAS, or anything else. One compromised bulb shouldn't expose your network.

**Start small, expand deliberately.** Buy 3 devices, live with them for a month, then add more. Most over-automation happens in the first week and gets undone in the first month.

---

## Quick Reference

**Protocol comparison:**

| Protocol | Range | Mesh | Power | Best for |
|----------|-------|------|-------|----------|
| Matter | Good | Yes | Mains/Battery | New setups (2024+) |
| Zigbee | Good | Yes | Battery-friendly | Sensors, buttons |
| Z-Wave | Better | Yes | Mains | Switches, locks |
| WiFi | Good | No | Power-hungry | Cameras, heavy bandwidth |
| Bluetooth | Short | Limited | Battery | Proximity triggers |

**Hub vs hubless:**

| Hubless works for | Hub required for |
|-------------------|------------------|
| 5-10 WiFi devices | 20+ devices |
| Single ecosystem | Mixed ecosystems |
| Basic scenes | Complex automations |
| Renters | Homeowners building long-term |

---

## Security Essentials

1. **Change default passwords** on EVERY device — cameras, routers, hubs
2. **Disable UPnP** on your router — manual port rules only
3. **Enable MFA** on accounts controlling locks, cameras, alarms
4. **Check firmware** monthly — or enable auto-updates where available
5. **Audit network** quarterly — remove devices you don't recognize

---

## When to Load More

| Situation | Reference |
|-----------|-----------|
| Choosing protocols, hubs, first devices | `setup.md` |
| Taking over devices from previous owner | `takeover.md` |
| Room-by-room automation patterns | `automations.md` |
| Network isolation, privacy, local-first | `security.md` |
| Device offline, won't pair, wrong behavior | `troubleshooting.md` |
| Non-permanent, portable solutions for renters | `renters.md` |
