---
name: pcb-analysis
description: Use when analyzing a printed circuit board on an authorized
  hardware assessment or in your own lab. Covers visual inspection,
  component identification, power rail mapping, signal tracing with a
  multimeter, and spotting hardware implants or tampering. Also use when
  you need a board's schematic level understanding without vendor docs.
version: 1.0.0
domain: hardware
lifecycle: stable
last_verified: '2026-10-23'
requires: []
extends: []
relates: [hardware-reversing, uart-jtag, firmware-extraction]
tools:
  - name: Python
    version: '3.12'
---

PCB analysis reads the board itself: what is connected to what, where
power flows, and whether anything does not belong. This skill covers
the lab method for boards you own or may test: systematic visual
inspection, power mapping, signal tracing, and tamper checks. It feeds
every other hardware skill with the ground truth of the physical
device.

## Quick Workflow

1. Photograph the board front and back at high resolution before
   probing anything.
2. Do a visual pass: look for rework, extra components, cut traces, and
   anything that differs from a reference board.
3. Identify power input and map the power rails with a multimeter
   (device unpowered).
4. Trace key signals: UART, SPI, I2C, and debug headers from the SoC to
   their test points.
5. Power the board and verify rail voltages match the regulators.
6. Check for implants: unexpected components, extra wiring, or modified
   firmware indicators.
7. Draw the partial schematic of the security relevant parts.
8. Hand the pinout map to the uart-jtag and firmware-extraction work.

## 1. Visual inspection and power mapping

```bash
# Unpowered continuity mapping: build a net list of interesting points
# Use the multimeter beeper; record which test points connect to which pins
python3 - << 'PY'
nets = {
    "GND": ["TP1", "TP7", "USB shield"],
    "3V3": ["TP2", "U1 pin 8 (flash VCC)"],
    "UART_TX?": ["TP3 -> SoC pin 42"],
    "UART_RX?": ["TP4 -> SoC pin 43"],
}
for net, points in nets.items():
    print(f"{net}: {', '.join(points)}")
print("verify each with the meter before connecting anything active")
PY
```

```bash
# Powered rail check: confirm voltages before attaching logic tools
# Measure each regulator output against ground; note any rail that is
# dead or wrong, since the board may have a fault or a mod
echo "expected: 3V3, 1V8, 5V_USB"
echo "record actual readings in notes/rails.txt"
```

## 2. Signal tracing to debug interfaces

```bash
# Trace from SoC to header: continuity from the SoC UART pins to test
# points identifies TX and RX without powering the board
# Then confirm direction by scoping during boot (TX toggles, RX is idle high)

# Document the final pinout for the team
cat > /tmp/hwrev/notes/pinout.txt << 'PINOUT'
J3 debug header (unpopulated, 2.54mm):
  pin 1: GND
  pin 2: UART TX (SoC pin 42, 115200 baud)
  pin 3: UART RX (SoC pin 43)
  pin 4: 3V3 (do not connect to adapter VCC)
PINOUT
cat /tmp/hwrev/notes/pinout.txt
```

## 3. Tamper and implant check

Compare against a known good board or high resolution reference
photos. Look for:

```bash
# Photo comparison checklist (do visually, record results)
# - extra components not on the reference (implants)
# - rework: flux residue, hand soldering, lifted pads
# - cut or jumpered traces (bodges)
# - replaced chips (date codes that do not match the batch)
# - unexpected test point wiring
python3 - << 'PY'
checks = ["extra components", "rework residue", "cut traces",
          "date code mismatch", "added wiring", "replaced shielding"]
print("tamper checklist:")
for c in checks:
    print(f"  [ ] {c}")
PY
```

## Edge cases

- Multilayer board hides inner traces. Use continuity and behavior
  (scope during boot) instead of visual tracing for inner layers.
- No reference board exists. Document everything as found and flag
  anomalies as suspicious rather than confirmed.
- Conformal coating blocks probing. Scrape tiny windows at test points
  with a fiberglass pen, or use existing uncoated headers.
- The board is densely packed BGA. Limit tracing to the accessible
  interfaces and rely more on firmware analysis.

## Escalation

- Tracing inconclusive: X-ray imaging (service bureau) reveals inner
  layers and hidden components.
- Suspected implant: remove and analyze the component separately, and
  compare firmware hashes against a known good image.
- Need the full schematic: board reverse engineering services exist,
  but weigh the cost against the assessment value.

## Detection and defender view

Defenders against PCB tampering use tamper evident seals, potting,
intrusion switches that wipe keys, and supply chain controls with
board level attestation. They detect modifications through visual
inspection programs and firmware hash checks at boot. For high
assurance devices, assume the board will be probed and keep secrets
in tamper resistant elements, not in traces anyone can follow.

## Key references

- CWE-1191 (On-Chip Debug and Test Interface With Improper Access
  Control).
- NIST SP 800-161: supply chain risk management.
- IPC inspection standards for PCB rework identification.
