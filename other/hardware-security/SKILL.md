---
name: hardware-security
description: >
  Discover and triage hardware debug interfaces (UART, JTAG, SWD) on an authorized embedded
  device — read boot logs, land a root console, interrupt the bootloader, and extract flash
  for offline analysis. Load when handed a physical device, PCB, or IoT/embedded target in
  scope, exposed test points or header pins, a serial console, U-Boot prompt, or a flash chip
  to dump. Signals: TX/RX/GND pads, silkscreen labels, baud-rate guessing, IDCODE enumeration.
domain: hardware
type: methodology
stability: learning
modes: [pentest]
severity: medium
tools: [usb-ttl, logic-analyzer, j-link, cmsis-dap, bus-pirate, openocd, flashrom, binwalk]
schema_version: 1
---

# Hardware debug-interface triage (UART / JTAG / SWD)

## When it applies
You have **physical access to a device you own or are explicitly authorized to open** — a router,
IoT gadget, embedded controller, or a board pulled from a larger system — and you need console
access or a firmware image. Hardware work is governed by the same envelope as everything else:
load `tradecraft-scope-roe` first and confirm the physical device and the teardown itself are in
`scope.txt`. Never open or probe a device that isn't yours or in writing.

## Why it works
Vendors leave debug and factory-test interfaces on the board: a UART serial console for boot logs
(often a root shell), and JTAG/SWD for chip-level debugging and memory readout. These ports bypass
all software authentication on the running system — if you can electrically reach them and match
the logic levels, the device talks to you. Bootloader consoles (U-Boot) additionally let you alter
boot arguments or read flash before the OS locks anything down.

## Method
1. **Open, photograph, label.** Photograph both board sides before touching anything; note
   silkscreen near pad clusters: `TX RX GND VCC` (UART) and `TDI TDO TCK TMS` (JTAG), `SWDIO/SWCLK`
   (SWD). Mind ESD — ground yourself; default to read-only probing.
2. **Identify the UART pinout with a multimeter, not guesses.** Find GND (continuity to a shield or
   ground pour), VCC (stable rail at power-on), TX (pulses during boot — confirm with a logic
   analyzer if ambiguous), RX (floating/pulled line next to TX). **Measure the logic level first —
   1.8 V, 3.3 V, or 5 V — and match your adapter to it** before connecting anything.
3. **Attach read-only first.** Connect only GND + the board's TX to a USB-TTL adapter and watch the
   boot log: `screen /dev/ttyUSB0 115200` (or `minicom`). If the output is garbage, sweep common
   baud rates (9600/38400/57600/115200) until the log is legible; record the rate. Boot logs alone
   leak flash layout, kernel version, and often credentials.
4. **Work the console.** Many devices drop to a root shell with no password. Interrupt U-Boot at
   the countdown (usually any key) and dump `printenv` — note the environment, but **do not
   `saveenv` casually**: a wrong write bricks the boot.
5. **Probe JTAG/SWD if UART is dead or locked.** With a J-Link or CMSIS-DAP adapter under OpenOCD,
   enumerate the chain and read the IDCODE: `openocd -f interface/jlink.cfg -f target/<chip>.cfg`.
   A populated IDCODE means the debug port is live; an all-zeros/all-ones response means it's
   fused off or your wiring/level is wrong.
6. **Extract flash for offline analysis.** In-circuit SPI dumps with a cheap programmer:
   `flashrom -p ch341a_spi -r dump.bin` (verify with a second dump and compare hashes). Immediately
   record `shasum -a 256 dump.bin` for evidence integrity, then hand the image to
   `reverse-eng-firmware` for extraction and analysis; individual binaries go to
   `reverse-eng-binary-triage`.
7. **Assess secure-boot/encrypted-flash feasibility non-destructively first** (signed-image checks
   in the boot log, eFuse hints from JTAG behavior) before considering chip-off or glitching — those
   are destructive and need explicit sign-off.

## Gotchas
- **Wrong logic level kills ports.** Connecting a 5 V adapter to a 1.8 V UART can destroy the SoC
  pins. Measure first; use a level shifter when in doubt.
- **Garbage output ≠ no console** — it's usually the wrong baud rate. Sweep before concluding the
  port is mute. Truly silent UARTs may be disabled in firmware; fall back to JTAG.
- **TX/RX are named from the board's perspective** — your adapter's RX listens to the board's TX.
  Read-only logging only needs GND + board TX.
- **A locked JTAG (empty IDCODE) is a finding too** — it tells you the vendor spent effort on
  debug-lockout, which shapes the rest of the assessment (chip-off vs. software attack surface).
- **Every write is a bricking risk.** `saveenv`, flash erase/program, and eFuse operations are
  one-way doors; get explicit approval and a verified dump before any of them.

## Verify success
You have a labeled pinout photo with measured logic levels, the recorded baud rate, and at least
one of: a working console (shell or U-Boot prompt), a live JTAG/SWD chain (valid IDCODE), or a
SHA256-hashed flash dump ready for `reverse-eng-firmware`. If everything is locked, you can state
precisely which interfaces exist and how each is disabled — that negative result is deliverable.

## References
OpenOCD and flashrom documentation; `reverse-eng-firmware` for what to do with the dump.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
