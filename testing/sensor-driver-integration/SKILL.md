---
name: sensor-driver-integration
description: Use when integrating, porting, calibrating, or debugging MCU sensor drivers, register maps, I2C/SPI transport, interrupts, FIFO, timing, or data conversion
---

# Sensor Driver Integration

## Overview

Use this skill to integrate sensors by proving transport, identity, configuration, timing, data readiness, conversion, and calibration in order. Sensor bugs often look like algorithm bugs but start with bus timing, register paging, or unit conversion.

## When To Use

Use this skill when:

- The user wants to add or debug accelerometers, gyroscopes, magnetometers, barometers, temperature sensors, ADC sensors, IMUs, ToF sensors, or environmental sensors.
- The issue involves no response, wrong ID, noisy data, stale samples, FIFO overflow, interrupt storms, calibration drift, or impossible physical values.
- The project uses I2C, SPI, UART, ADC, GPIO interrupts, DMA, low-power modes, or RTOS tasks.

Do not use this skill when the electrical bus itself has not been proven. Use `hardware-interface-debug` first.

## First Questions

Ask for:

- Sensor part number, datasheet link, breakout/module schematic, and supply voltage.
- Bus type, address/chip select, speed, pull-ups, interrupt pins, and reset pins.
- Driver source, initialization sequence, register dump, and current raw sample values.
- Sampling rate, FIFO use, interrupt mode, low-power mode, and timestamp source.
- Expected units, scale, calibration data, and observed symptom.

## Integration Checklist

1. Prove physical and bus identity.
   Check power rails, reset state, WHOAMI/device ID, and basic register reads before configuration.

1. Freeze the register plan.
   Document mode, range, bandwidth, output data rate, FIFO, interrupts, and low-power settings.

1. Read raw data first.
   Convert bytes with the correct endian, signedness, resolution, and scale only after raw values move plausibly.

1. Add readiness and timing.
   Poll or interrupt on data-ready, avoid reading faster than ODR, and timestamp close to acquisition.

1. Validate calibration.
   Keep offset, sensitivity, temperature compensation, and factory calibration separate from transport logic.

1. Test stress cases.
   Cover FIFO overflow, suspend/resume, bus errors, hot reset, and sensor disconnect.

## Common Failures

- I2C address is shifted incorrectly or SPI mode is wrong.
- Register pages/banks are not selected before access.
- Multi-byte samples are read with wrong endian or signed extension.
- Driver reads stale data because data-ready or FIFO status is ignored.
- Interrupt polarity/latched mode is misconfigured.
- Calibration is applied twice or in the wrong unit.

## Verification

Before claiming a sensor works:

- State part number, bus settings, sample rate, range, and interrupt/FIFO mode.
- Confirm device ID and a representative register dump.
- Confirm raw and converted values under at least two physical conditions.
- Confirm behavior across reset, suspend/resume, and bus error recovery if relevant.

## Example

User:

```text
IMU 数据一直跳，姿态算法不稳定。
```

Agent:

1. Reads WHOAMI, range, ODR, bandwidth, FIFO, and interrupt registers.
1. Checks raw accel/gyro values before the fusion algorithm.
1. Verifies timestamp, endian, scale, and calibration before tuning filters.
