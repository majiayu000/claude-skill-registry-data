---
name: gnss-gps-integration
description: Use when integrating a UART GNSS/GPS module (u-blox M8/M9/M10, Quectel Lxx), parsing NMEA GGA/RMC/GSA/GSV or UBX-NAV-PVT, or debugging no-fix, TTFF, checksum, or PPS issues
---

# GNSS GPS Integration

## Overview

Use this skill to connect a GNSS/GPS module to an MCU over UART and turn raw output into a trusted fix. The hard parts are proving the byte stream is intact (NMEA XOR checksum, UBX sync), rejecting invalid fixes, and getting acceptable TTFF given antenna, sky view, and backup-power constraints.

## When To Use

Use this skill when:

- The user integrates u-blox `NEO-M8N`, `NEO-M9N`, `MAX-M10`, or Quectel `L76`/`L80`/`LC76` over UART.
- The work involves parsing `$GxGGA`, `$GxRMC`, `$GxGSA`, `$GxGSV`, the `*hh` XOR checksum, or the UBX binary protocol (`0xB5 0x62`, `UBX-NAV-PVT`).
- Symptoms include no satellites, TTFF too long, `RMC` status `V`, lat/lon of 0, truncated NMEA frames, or PPS not toggling.
- Configuration uses the legacy `UBX-CFG-PRT`/`UBX-CFG-MSG` messages (M8-era), the config-key interface `UBX-CFG-VALSET`/`UBX-CFG-VALGET` (M9/M10), or PMTK sentences (`PMTK251`, `PMTK220`, `PMTK314`).

Do not use this skill when the UART link itself is unproven; confirm bytes arrive at the correct baud first.

## First Questions

Ask for:

- Exact module and vendor (u-blox M8/M9/M10 vs Quectel Lxx), since protocol and config differ.
- UART baud (u-blox default `9600`, Quectel L76 default `9600`), wiring (TX/RX crossed, CMOS 3V3 levels).
- Active vs passive antenna, its supply/bias-T, and current sky visibility (indoors vs open sky).
- Backup power: is `V_BCKP`/RTC battery or supercap fitted, or does the module lose power fully each cycle?
- Whether the design needs continuous or low-power periodic fixes, and if PPS time sync is required.
- Current raw output (paste a few NMEA lines) and the observed failure.

## Integration Checklist

1. Prove the raw stream.
   Log UART bytes at the module's default baud before parsing; confirm `$G...` ASCII lines or UBX `0xB5 0x62` frames, not garbage from a baud mismatch.

1. Validate every sentence.
   Compute the XOR of all chars between `$` and `*`, compare to the two hex digits after `*`, and drop the line on mismatch or missing CR/LF instead of parsing junk.

1. Gate on the fix flag.
   Trust position only when `RMC` status is `A` (not `V`) and `GGA` fix quality is nonzero; treat lat/lon `0,0` as no-fix, and read satellite count/HDOP from `GGA`, sats-in-view from `GSV`.

1. Configure output intentionally.
   On u-blox M8 use the legacy `UBX-CFG-PRT` (baud/protocols) and `UBX-CFG-MSG` (per-message rate); on M9/M10 use the config-key interface `UBX-CFG-VALSET`/`UBX-CFG-VALGET`, since the legacy `CFG-*` messages are deprecated there. Poll or enable `UBX-NAV-PVT` for a binary fix. On Quectel/MTK use `PMTK314` (sentence selection), `PMTK220` (update rate), `PMTK251` (baud). Save config if the module supports it.

1. Handle startup and backup power.
   Expect cold start (~30 s to minutes) when ephemeris is lost; keep `V_BCKP`/RTC powered so warm/hot starts (seconds) work. Issuing a cold start (`PMTK103`) or a full cold start (`PMTK104`, which also clears config) clears aiding data and forces a long TTFF.

1. Wire PPS and low-power correctly.
   If timing matters, latch the PPS edge in an ISR and pair it with the time from `RMC`/`UBX-NAV-PVT`; for periodic duty cycling, allow re-acquisition time and avoid killing backup power between wakeups.

## Common Failures

- No satellites: passive antenna with no bias voltage, antenna indoors/blocked, or open/short on the active-antenna feed (no current = open, excess = short).
- Baud mismatch: reading a `115200` module at `9600` yields framing errors and random bytes.
- Checksum failures or truncated lines: undersized RX buffer, UART overrun, or parsing before a full `\r\n` line arrives.
- Every fix is a cold start (long TTFF): `V_BCKP`/RTC unpowered, so ephemeris/almanac are lost on each power cycle.
- Position stuck at `0,0` or status `V`: parser ignores the validity flag and publishes an unfixed solution.
- UBX ignored: wrong sync bytes, class/ID, or a mis-computed 8-bit Fletcher checksum (`CK_A`/`CK_B`) on the `CFG` message.

## Verification

Before claiming the GNSS link works:

- State module, baud, antenna type/power, and protocol (NMEA and/or UBX).
- Show a captured sentence with a checksum you recomputed and confirmed.
- Confirm a real fix: `RMC` status `A`, nonzero `GGA` quality, plausible lat/lon, sat count and HDOP.
- Report measured TTFF from cold and from warm/hot start, and confirm backup power behavior.
- If used, confirm PPS toggles at 1 Hz and aligns with the reported time.

## Example

User:

```text
NEO-M8N 接上了,UART 有数据,但一直定位不了,$GNRMC 的状态一直是 V。
```

Agent:

1. Confirms baud (`9600` default) and captures a few raw lines to verify checksums pass and sentences are complete.
1. Reads `GGA` fix quality and `GSV` sats-in-view; asks about antenna type/power and whether the module is under open sky.
1. Explains `V` means no valid fix yet, checks for a cold start with no `V_BCKP` backup, and moves the antenna to clear sky to let ephemeris download before expecting status `A`.
