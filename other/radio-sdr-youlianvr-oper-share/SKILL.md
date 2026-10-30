---
name: radio-sdr
description: Use for authorized RF/SDR security research including signal identification, replay feasibility study in shielded labs, and wireless protocol analysis outside classic Wi-Fi.
---

# RF / SDR Security Research

## Before you start

1. `NOW`: **Spectrum use and transmission are tightly regulated by law**; work only
   with authorized bands, shielded chambers, or lab targets.
2. `NOW`: the scope must state the devices, the bands, and whether transmission is
   allowed (reception-only is the default).
3. `ACT`: receive-and-identify only → demodulation and analysis → replay
   feasibility assessment in the lab.

## When to use

- Non-Wi-Fi RF such as wireless remotes and sensors (authorized).
- Protocol research such as ADS-B and remote control (legal reception only).
- Division of labor with `wifi-wireless`: this skill covers **generic SDR/RF**;
  Wi-Fi attack and defense lives in `wifi-wireless`.

## Workflow

```text
□ Confirm regulations and licensing
□ Receive only: identify the center frequency and the modulation
□ Analyze with GNU Radio / URH
□ Replay only inside a shielded chamber and only with written permission
□ Conclusions focus on: can an unauthorized party control it / hardening advice
```

## Toolchain

| Tool | Purpose |
|------|---------|
| RTL-SDR / HackRF (compliant models) | receive/transmit hardware |
| URH / GNU Radio | analysis |
| Inspectrum | signal inspection |

## References

- `references/sdr-lab-rules.md`
- `security/parts/wifi-wireless/`, `security/parts/ot-ics/`, `security/parts/hardware-security/`

## Routing context

**Upstream**: MASTER R38
**MUST NOT**: interfere with public communications, transmit without authorization

## Completion self-check

- [ ] Was reception the default, with the regulatory boundary recorded?
- [ ] Checklist?
