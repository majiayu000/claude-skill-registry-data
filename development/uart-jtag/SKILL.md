---
name: uart-jtag
description: Use when working with embedded hardware on an authorized
  assessment or lab device you own. Covers finding UART consoles with a
  logic analyzer, getting a root shell over serial, identifying JTAG and
  SWD headers, and dumping memory with OpenOCD. Also use when a device
  boots but you have no software access and need a hardware debug path.
version: 1.0.0
domain: hardware
lifecycle: stable
last_verified: '2026-10-23'
requires: []
extends: []
relates: [firmware-analysis, firmware-extraction, ghidra-basics]
tools:
  - name: OpenOCD
    version: 0.12.0
  - name: Python
    version: '3.12'
---

UART and JTAG are the hardware backdoors left on almost every embedded
board: serial consoles that drop to root shells, and debug ports that
can halt the CPU and read memory. This skill covers the authorized lab
method: identifying the pins, getting a console at the right baud rate,
and using JTAG or SWD to inspect and dump a device you own or have
permission to test. Work only on your own hardware or with written
permission; never probe devices you do not own.

## Quick Workflow

1. Inspect the board: look for unpopulated headers, test points labeled
   TX, RX, GND, and debug header footprints.
2. Identify power and ground with a multimeter before connecting
   anything.
3. Find the UART transmit pin by watching for boot text at common baud
   rates.
4. Connect a USB to serial adapter (3.3V, never 5V unless the board
   needs it) and capture the boot log.
5. Try the console: interrupt the bootloader, check for a shell, and
   note the privilege level.
6. Identify JTAG or SWD pins and confirm with an OpenOCD scan.
7. Halt the CPU and dump flash or RAM regions you are authorized to
   read.
8. Document pinout, baud rate, and every command that gave access.

## 1. Finding the UART console

The transmit pin chatters during boot. Find it without guessing the
baud rate by trying the common ones.

```bash
# List serial adapters
ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null

# Try common baud rates against the suspected TX pin (connect GND + RX
# of adapter to TX of target; never connect VCC between boards)
for baud in 115200 57600 38400 9600 230400; do
  echo "=== trying $baud ==="
  timeout 4 picocom -b $baud --imap lfcrlf /dev/ttyUSB0 2>/dev/null | head -5
done
# Readable boot text (U-Boot, Linux) means you found TX and the baud rate
```

```bash
# Capture the full boot log once the console works
picocom -b 115200 --logfile /tmp/uart_boot.log /dev/ttyUSB0
# In another terminal, power cycle the board and watch for:
# - bootloader prompt (Hit any key to stop autoboot)
# - kernel messages revealing flash layout and interfaces
# - a login or shell prompt at the end
```

If the bootloader stops on keypress, check its commands (`help`, `printenv`):
bootloader access often means you can change boot arguments or load your
own kernel in a lab setting.

## 2. JTAG and SWD with OpenOCD

JTAG gives CPU level control: halt, read and write memory, and load
code. Identify the pins (TCK, TMS, TDI, TDO, or SWDIO and SWCLK for
SWD), connect a debug probe, and scan.

```bash
# Scan the JTAG chain with a generic probe config
openocd -f interface/ftdi/dp_busblaster.cfg -f target/stm32f1x.cfg \
  -c "init; scan_chain; exit" 2>&1 | head -30
# A listed TAP with a valid IDCODE confirms the pinout
```

```bash
# Halt the CPU and dump a flash region (lab device, authorized)
openocd -f interface/stlink.cfg -f target/stm32f1x.cfg \
  -c "init; halt; dump_image /tmp/flash_dump.bin 0x08000000 0x40000; exit"
ls -l /tmp/flash_dump.bin
# Analyze the dump with firmware-extraction and firmware-analysis skills
```

```bash
# Read the option bytes / security fuses status (know before you poke)
openocd -f interface/stlink.cfg -f target/stm32f1x.cfg \
  -c "init; halt; stm32f1x options_read 0; exit" 2>&1 | head -20
# If readout protection is level 2, the debug port is closed; do not
# attempt bypasses outside the agreed scope
```

## Edge cases

- No readable text at any baud rate. The console may be disabled, use
  an unusual baud (try 1500000 on some ARM boards), or TX may be a
  different test point.
- Text is garbled at every rate. Check voltage levels: a 1.8V target
  read by a 3.3V adapter gives garbage; use a level shifter.
- JTAG scan finds nothing. The port may be disabled by fuses, or the
  pins are shared with GPIO and need a boot mode pin strapped.
- The board has no marked headers. Use a multimeter in continuity mode
  to trace test points to the SoC pins, then check the datasheet.
- USB serial adapter backpowers the board. Disconnect the adapter's
  power pin and use a common ground only.

## Escalation

- Bootloader is password protected: check for default credentials in
  the vendor docs, or move to JTAG memory reads if in scope.
- Console drops to a limited shell: enumerate it like any restricted
  shell (check `help`, busybox applets, writable paths).
- JTAG fused off: document it as a positive finding and pivot to
  firmware update file analysis instead.
- SWD works but flash reads as all 0xFF: readout protection is on;
  reads are blocked by design and that is the finding.

## Detection and defender view

For hardware, the "defender" is the device designer. They see these
attacks coming through unpopulated headers, verbose boot logs, and
unlocked debug ports on production boards. Defenses that work: remove
or disable UART consoles in production firmware, blow the debug
disable fuses, enable readout protection, and sign firmware updates so
a console alone cannot load unsigned code. A board that ships with an
active root console has no meaningful hardware security boundary.

## Key references

- OpenOCD 0.12.0 documentation: JTAG scan and flash commands.
- CWE-1191 (On-Chip Debug and Test Interface With Improper Access
  Control).
- CWE-1242 (Inclusion of Undocumented Features or Chicken Bits).
- OWASP IoT Top 10: insecure debug interfaces.
