---
name: battery-charger-fuel-gauge-integration
description: Use when integrating or debugging Li-ion charger/fuel gauge ICs (BQ24295, BQ27441, MAX17048) over I2C, covering charge start, watchdog host mode, NTC/JEITA faults, and SOC jumps
---

# Battery Charger and Fuel Gauge Integration

## Overview

Use this skill to bring up a Li-ion/LiPo charger IC (TI `BQ24xxx`/`BQ25xxx`) and a fuel gauge (TI `BQ27xxx` Impedance Track, or Maxim/Analog `MAX1704x` ModelGauge, e.g. `MAX17048`) over I2C. The hard parts are keeping the charger in host mode past its watchdog, and getting an accurate SOC before the gauge has a matching battery profile.

## When To Use

Use this skill when:

- Charging never starts or restarts in a loop: check input current limit (`IINLIM`, `REG00[2:0]`), `EN_HIZ`, the `CE` pin, and the I2C watchdog resetting registers to default.
- The charger reports faults: `REG09` latched faults, `NTC_FAULT` (`REG09[2:0]`, with a real thermistor such as `103AT` on the `TS` pin), safety timer expiration, or JEITA temperature de-rating.
- SOC from `BQ27441`/`MAX17048` is wrong or jumps at power-up: profile not loaded, no learning cycle, or bad OCV calibration.
- I2C reads to the charger/gauge fail or the wrong 7-bit address is used.

Do not use this skill when the I2C bus itself is dead (no ACK on any address) or the board rails are wrong; debug the bus and power tree first with `hardware-interface-debug`.

## First Questions

Ask for:

- Exact charger and gauge part numbers, cell count/chemistry, pack capacity (mAh), and charge voltage (4.2 V vs 4.35 V — picks `BQ27441-G1A` vs `-G1B`).
- 7-bit I2C addresses, bus speed, and pull-up values; whether `INT`/`GPOUT` is wired.
- NTC/thermistor part and TS resistor network (`RT1`/`RT2`), plus target charge/discharge temperature window.
- Whether a battery profile (TI golden image `.gm.fs`/`.df.fs`, or a Maxim `RCOMP`/custom-model INI) exists, or a golden image must be created.
- Current symptom: register dump, fault code, measured `VBAT`/`ICHG`, or reported SOC vs true SOC.

## Integration Checklist

1. Confirm the device on the bus.
   ACK the charger and gauge 7-bit addresses; read a known register (charger `REG0A` Vendor/Part/Revision, or gauge `Control()` `DEVICE_TYPE` subcommand) before writing anything.

1. Take and hold host mode on the charger.
   Set `IINLIM` in `REG00[2:0]`, clear `EN_HIZ` (`REG00[7]`), enable charging via `CE`/`CHG_CONFIG` (`REG01[4]`), then feed the I2C watchdog (write `REG01[6]`) on a timer, or disable it (`WATCHDOG` = `REG05[5:4]` = 00), so registers do not reset to default and drop charging.

1. Configure charge parameters and protection.
   Program fast-charge current (`ICHG`, `REG02`), pre-charge/termination current (`REG03`), charge voltage (`VREG`, `REG04`), and enable NTC/JEITA limits; confirm the thermistor scaling (e.g. `103AT`) on the `TS` pin.

1. Load the fuel gauge battery profile.
   For `BQ27441`: `UNSEAL` via `Control()`, enter `CFGUPDATE`, poll `Flags()` until bit 4 is set, write `Design Capacity`/`Design Energy`/`Terminate Voltage`/`Taper Rate` in the data-memory block, fix `BlockDataChecksum` (`255 - x`, where `x` is the byte-wise sum of the block), then `SOFT_RESET`. For `MAX17048`: load a custom model / set `RCOMP0` (`CONFIG` default `0x97`) or accept EZ defaults.

1. Calibrate SOC at first power-up.
   Let the pack rest for a valid OCV read, then issue `MAX17048` `QuickStart` (`MODE` = `0x4000`) or check `BQ27441` `Flags()` `ITPOR` cleared; do not `QuickStart` under load.

1. Run temperature compensation and status polling.
   Update `MAX17048` `RCOMP` from measured temperature at least once/minute; on `BQ27441` feed `Temperature()` if host-reported. Poll charger `CHRG_STAT` (`REG08[5:4]`) and read `REG09` twice to get fresh faults (it latches, clears on read).

## Common Failures

- Charging restarts every ~40 s: I2C watchdog expired (default 40 s), resetting the writable control registers to defaults; feed it or disable `WATCHDOG`.
- No current with valid adapter: `IINLIM` too low, `EN_HIZ` set, `ILIM` pin resistor, or `CE` held high disabling charge.
- Charge stuck in pre-charge or never terminating: `BATLOWV` threshold (`REG04[1]`), wrong termination current, or safety timer expiring (`REG09` charge safety timer fault).
- `NTC_FAULT` / no charge in a comfortable room: TS resistor network wrong, floating `TS` pin, or JEITA cold/hot fold-back.
- SOC reads 0/100 % or jumps tens of percent: profile (`Design Capacity`) not written, `BlockDataChecksum` wrong so writes silently rejected, or `ITPOR` still set.
- Gauge writes ignored: device still `SEALED`, or not in `CFGUPDATE` mode before writing the data-memory block.
- I2C NAK: wrong 7-bit vs 8-bit address, missing pull-ups, or gauge in hibernate/shutdown.

## Verification

Before claiming charging and gauging work:

- Dump charger `REG00`–`REG0A`; confirm `IINLIM`, `VREG`, `ICHG`, watchdog state, and `CHRG_STAT` transitions Not Charging → Fast Charging → Termination Done.
- Force a fault (unplug NTC or overheat pack) and confirm `REG09`/`INT` reports it and clears on re-read.
- Compare gauge SOC against a coulomb-counted or bench-measured charge/discharge; verify it tracks within a few percent and survives a reset (`ITPOR` clear, profile persists).
- Confirm charging continues across a full watchdog interval without host register rewrites (or with the feeding task running).

## Example

User:

```text
BQ24295 一充电就每隔几十秒重启,SOC 还老是乱跳,怎么查?
```

Agent:

1. Asks for I2C address, adapter/`IINLIM` setting, whether the watchdog is fed, NTC network, and whether a `BQ27441` profile was loaded.
1. Reads `REG00`/`REG08`/`REG09`; if registers reverted to defaults, enables watchdog feeding (write `REG01[6]`) or disables `WATCHDOG` to hold host mode.
1. Checks the gauge: `UNSEAL`, verifies `Design Capacity` and `BlockDataChecksum`, clears `ITPOR`, then `QuickStart`/rest-OCV calibrates SOC and re-tests across a charge cycle.
