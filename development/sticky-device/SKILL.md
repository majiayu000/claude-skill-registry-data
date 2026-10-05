---
name: sticky-device
description: Hardware facts, ESP-IDF firmware patterns, ePaper/touch APIs, and Playground publishing rules for the Seeed Studio reTerminal Sticky (ESP32-S3, 3.97" 800x480 e-ink). Use when working on reTerminal Sticky or "Sticky" firmware, apps, pin assignments, display refresh, touch gestures, deep sleep, ESPHome/Home Assistant configs, or when submitting an integration to the Sticky Playground registry.
license: MIT
compatibility: Documentation-only skill. The bundled fetch script needs git and network access to github.com.
metadata:
  author: varo6
  version: "1.0.0"
  repository: https://github.com/varo6/reTerminal-sticky-skill
---

# reTerminal Sticky

Seeed Studio reTerminal Sticky: a magnetic ESP32-S3 e-ink note device. 3.97" 800x480
monochrome ePaper with 4-level grayscale, capacitive touch, 750 mAh battery.

Firmware is native **ESP-IDF v5.4 / target `esp32s3`** (C/C++). ESPHome is the
supported no-C path. Apps are distributed by flashing whole firmware images — there
is no on-device app sandbox or multi-app runtime.

## Read this first for any firmware task

Two rules cause most first-time failures on this device:

1. **Latch power on at boot.** The device powers off unless firmware drives the
   power-hold GPIOs within the first moments of `app_main()`. See
   [references/esp-idf-dev.md](references/esp-idf-dev.md).
2. **The panel is natively 800x480 landscape.** Your logical canvas orientation is a
   choice you implement with a rotation in the pixel-write path. Pick one and keep
   touch coordinates in the same space. See [references/display.md](references/display.md).

## Where to look

| Task | File |
|---|---|
| Pin map, buses, part numbers, electrical/physical specs | [references/hardware.md](references/hardware.md) |
| Toolchain, project skeleton, `sdkconfig.defaults`, build/flash, power latch, NVS, deep sleep | [references/esp-idf-dev.md](references/esp-idf-dev.md) |
| ePaper driver API, refresh modes, rotation, ghosting, partial-update strategy | [references/display.md](references/display.md) |
| Touch/GT911 gestures, buttons, IMU, SHT40, RTC, mic, buzzer, fuel gauge, SD | [references/peripherals.md](references/peripherals.md) |
| Publishing to Sticky Playground: `integration.json`, manifest, CI, review flow | [references/playground-registry.md](references/playground-registry.md) |
| Existing firmware projects, ESPHome/Home Assistant, official docs, where the wiki is | [references/ecosystem-and-docs.md](references/ecosystem-and-docs.md) |

## Getting known-good driver sources

The registry holds a complete, buildable ESP-IDF app (`sticky-2048`) whose drivers are
the practical reference implementation for this board: `seeed_epaper` (SSD1677 panel),
`gt911` (touch), `bq27220` (fuel gauge), plus `sticky_display` / `sticky_touch` /
`sticky_buzzer` / `sticky_ai_button` wrappers.

To pull them into a working directory:

```bash
scripts/fetch_sticky_sources.sh <dest-dir>
```

Read that source before writing a driver from scratch. It is the only public code that
is known to run on production hardware.

## Documentation reality check

There is **no `wiki.seeedstudio.com` page for the Sticky** (verified 404 on
`/reterminal_sticky/` and `/sticky/`). The Seeed wiki covers the older reTerminal
**E-series**, which is a different board — its pinouts do not transfer, though its
ESPHome cookbooks are conceptually useful.

Authoritative docs live at <https://www.seeedstudio.com/sticky/docs/>, and Seeed
states they are still under active development. When something is missing, the
fallback order is: registry source code → official docs → E-series wiki (concepts
only) → Discord/forum. Full link list in
[references/ecosystem-and-docs.md](references/ecosystem-and-docs.md).

## Conventions in this skill

- Pin numbers are ESP32-S3 **GPIO numbers**, not header positions.
- "Native" coordinates mean the panel's own 800x480 landscape frame; "logical" means
  whatever orientation the application chose.
- Facts marked **(unverified)** come from a single source or conflicting sources and
  should be confirmed against hardware before relying on them.
