---
name: dual-led-constant-power
description: Calibrate and control a dual LED Arduino UNO modulation setup using YYNMOS MOS switch modules and a Waveshare INA219 Current/Power Monitor HAT. Use when working on DualLampHI-style wiring, I2C monitor detection, PWM upload, CSV/PNG power capture, calibrated LUT constant-power crossfades, flicker reduction, or interpreting per-LED voltage/current/power telemetry.
---

# Dual LED Constant Power

Use this skill for the two-LED Arduino/MOS/INA219 setup where the goal is smooth spectral modulation while keeping measured total electrical power approximately constant.

## Default workflow

1. Prefer the calibrated LUT controller over RL or fast feedback.
2. Confirm I2C sees the Waveshare monitor at `0x40`, `0x41`, `0x42`, and `0x43`.
3. Upload `firmware/dual_led_constant_power_lut/dual_led_constant_power_lut.ino`.
4. Capture with `scripts/capture_dual_led_power_plot.py`.
5. Inspect the runtime section of the plot, not only the calibration sweeps.
6. Commit and push firmware, documentation, and lightweight final measurement outputs when working inside the repo.

## Hardware assumptions

Use Arduino UNO with two YYNMOS-1 MOS modules and Waveshare Current/Power Monitor HAT.

Important monitor wiring:

```text
Monitor pin 1 / 3V3 -> Arduino 3.3V
Monitor pin 3 / SDA -> Arduino A4 / SDA
Monitor pin 5 / SCL -> Arduino A5 / SCL
Monitor pin 6 / GND -> Arduino GND
```

Important logical mapping:

```text
PWM A / Arduino D9  -> logical LED A -> monitor 0x41
PWM B / Arduino D10 -> logical LED B -> monitor 0x40
```

## Commands

```powershell
arduino-cli board list
arduino-cli compile --fqbn arduino:avr:uno firmware\dual_led_constant_power_lut
arduino-cli upload --fqbn arduino:avr:uno -p COM3 firmware\dual_led_constant_power_lut
python scripts\capture_dual_led_power_plot.py --port COM3 --duration 70 --out-dir measurements
```

## Algorithm preference

Do not use reinforcement learning as the first approach. The system is monotonic enough for calibration:

```text
duty -> measured LED power -> inverse LUT -> target power -> duty
```

Use fast feedback only for diagnostics. Real-time feedback from raw INA219 values can create visible flicker because the MOS PWM carrier and INA219 conversion timing alias.

## Reference

Read `references/workflow.md` when needing details about the final wiring, data columns, final performance, or troubleshooting.
