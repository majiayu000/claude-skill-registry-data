---
name: govee
description: Control Govee H6046 RGBIC TV Light Bars via Bluetooth Low Energy.
---

# Govee

## Introduction

This tool provides a CLI and Python API to control Govee LED lights. It communicates directly with the device over Bluetooth, requiring no cloud connection or Govee account.

## Prerequisites

- Linux system with Bluetooth adapter
- BlueZ installed (`bluez`, `bluez-utils`)
- Python 3.10+ with `bleak` library
- Device MAC address (obtain via `govee scan`)

## Installation

```bash
uv pip install -e .
```

## Configuration

Set your device MAC in `config.yml`:
```yaml
device: "C5:37:32:32:2C:43"
```

Or use environment variable:
```bash
export GOVEE_DEVICE="C5:37:32:32:2C:43"
```

Or pass `-m` flag to each command.

## Commands

### Scan for devices
```bash
govee scan
```
Returns list of Govee devices with MAC addresses.

### Power control
```bash
govee on    # Turn light on
govee off   # Turn light off

# Or with explicit MAC:
govee -m <MAC> on
govee -m <MAC> off
```

### Set color
```bash
# By name
govee color red
govee color blue
govee color warm

# By hex code
govee color "#FF5500"
govee color 00FF00

# By RGB values
govee rgb 255 128 0
```

Available color names: `red`, `green`, `blue`, `white`, `yellow`, `cyan`, `magenta`, `purple`, `orange`, `pink`, `warm`, `cool`

### Set brightness
```bash
govee brightness 50   # 0-100%
```

## Device Configuration Priority

1. `-m` / `--mac` command line flag
2. `GOVEE_DEVICE` environment variable
3. `device` field in `config.yml`

## Python API

```python
import asyncio
from govee import GoveeDevice

async def control_light():
    async with GoveeDevice("C5:37:32:32:2C:43") as device:
        await device.power_on()
        await device.set_color("red")
        await device.set_brightness(50)
        await device.set_rgb(255, 128, 0)
        await device.power_off()

asyncio.run(control_light())
```

## Example Workflows

### Set ambient lighting for movie watching
```bash
govee on
govee color warm
govee brightness 30
```

### Alert/notification flash
```bash
govee color red
sleep 0.5
govee color blue
sleep 0.5
govee color red
```

### Gradual wake-up light
```bash
govee on
govee color warm
for i in 10 20 30 40 50 60 70 80 90 100; do
  govee brightness $i
  sleep 60
done
```

## Known Limitations

- Only one Bluetooth connection at a time (disconnect Govee app first)
- Device must be powered on and in range (~10m)
- Some RGBIC features (segments, scenes) not fully implemented
- Connection may take 2-5 seconds

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Device not found | Run `govee scan`, ensure light is powered on |
| Connection timeout | Power cycle the light, close Govee phone app |
| Commands fail silently | Light may be off; run `govee on` first |
| Permission denied | Run with `sudo` or add user to `bluetooth` group |

## Device Compatibility

Verified:
- Govee H6046 RGBIC TV Light Bars

Likely compatible (untested):
- Govee H6102, H6072 (same MODE_1501 protocol)
- Other Govee RGBIC devices

## File Locations

- CLI source: `src/govee/cli.py`
- Device library: `src/govee/device.py`
- Command builders: `src/govee/commands.py`
- Protocol spec: `docs/SPEC.md`
- Config file: `config.yml`
