---
name: radio-sdr
description: "Use for authorized RF/SDR security research including signal identification, replay feasibility study in shielded labs, and wireless protocol analysis outside classic Wi-Fi."
version: 1.0.0
license: MIT
metadata:
  package: unleash-skills
  author: NetVar1337/unleash
  category: reverse-skill
  upstream: https://github.com/zhaoxuya520/reverse-skill
---

> Bundled with Unleash skills pack. Upstream: https://github.com/zhaoxuya520/reverse-skill

# RF / SDR Security Research

## ACTION REQUIRED (execute immediately after reading)

1. `NOW`: **spectrum and transmission are strictly regulated by law**; authorized bands/shielded rooms/lab targets only
2. `NOW`: scope states devices, frequency bands, whether transmission is allowed (receive-only by default)
3. `ACT`: receive-only identification → demodulation analysis → lab reproduction assessment

## Applicable Scenarios

- Non-Wi-Fi RF such as wireless remotes/sensors (authorized)
- ADS-B/remote-control and similar protocol research (legal reception)
- Division of labor with wifi-wireless: this skill leans toward **general-purpose SDR RF**; Wi-Fi offense/defense goes to R29

## Workflow

```text
□ Regulatory and licensing confirmation
□ Receive only: identify center frequency and modulation
□ Analyze with GNU Radio / URH
□ Replay only in a shielded room and with written permission
□ Conclusions focus on: whether unauthorized control is possible / hardening recommendations
```

## Toolchain

| Tool | Purpose |
|------|------|
| RTL-SDR / HackRF (compliant) | RX/TX hardware |
| URH / GNU Radio | Analysis |
| Inspectrum | Signals |

## References

- `references/sdr-lab-rules.md`
- `../wifi-wireless/` `../ot-ics/` `../hardware-security/`

## Routing Context

**Upstream**: MASTER R38  
**MUST NOT**: interfering with public communications, unauthorized transmission

## Task Completion Self-Check

- [ ] Receive-only by default with regulatory boundaries recorded?
- [ ] Checklist?
