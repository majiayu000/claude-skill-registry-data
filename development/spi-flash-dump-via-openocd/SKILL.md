---
name: SPI Flash Dump via OpenOCD
description: This skill should be used when the user asks to "dump SPI flash", "read EEPROM through OpenOCD", "dump flash via MCU", "read SPI through debug interface", "extract firmware from SPI", or mentions scenarios involving SPI flash connected to a microcontroller with SWD/JTAG debug access. Provides comprehensive guidance for RAM-resident SPI flash dumping without external programming hardware.
version: 1.0.0
---

# SPI Flash Dump via OpenOCD

## Overview

This skill enables dumping SPI flash or EEPROM memory through a microcontroller's SPI peripheral using OpenOCD/SWD, without requiring external SPI programming hardware.

**When to use this approach:**
- SWD/JTAG debug access to an MCU is available (via OpenOCD)
- SPI flash/EEPROM is connected to the MCU's SPI peripheral
- Direct access to the SPI chip is impractical (BGA package, no test points)
- External SPI programmers (CH341A, Bus Pirate) are unavailable

## Architecture

```
┌─────────────┐     SWD      ┌─────────────┐     SPI      ┌─────────────┐
│  OpenOCD    │◄────────────►│  Target MCU │◄────────────►│  SPI Flash  │
│  (Host PC)  │              │   (SRAM)    │              │             │
└─────────────┘              └─────────────┘              └─────────────┘
```

The approach:
1. Load a minimal program (~500 bytes) into MCU's SRAM via OpenOCD
2. Execute it to read SPI flash data into a RAM buffer
3. Use OpenOCD to read the buffer back to the host
4. Repeat until entire flash is dumped

## Prerequisites

Before starting, gather this information:

**MCU Information:**
- MCU family and part number (e.g., ATSAM4S2A, STM32F407)
- SRAM base address and size (typically 0x20000000 for Cortex-M)
- SPI peripheral base address (from datasheet)
- GPIO controller address for chip select pin

**SPI Flash Information:**
- Part number if known (e.g., AT25DF321A, W25Q32)
- Expected capacity
- SPI pins used (CS, MOSI, MISO, CLK)

**Connection:**
- Working OpenOCD connection to target
- Ability to halt, resume, read/write memory

## Implementation Process

### Step 1: Identify SPI Registers

Look up the MCU's datasheet for SPI register addresses. See `references/mcu-registers.md` for common MCU families.

**Key registers to find:**
- Control Register (enable/disable SPI)
- Mode Register (master mode, clock settings)
- Transmit Data Register
- Receive Data Register
- Status Register (TX ready, RX complete bits)

### Step 2: Identify GPIO for Chip Select

The SPI chip select (CS) is often controlled via GPIO for precise timing. Find:
- GPIO controller base address
- Pin enable register
- Output enable register
- Set/clear output registers

### Step 3: Plan Memory Layout

Plan SRAM layout for the dumper:

```
SRAM Layout (example: 64KB at 0x20000000):

0x20000000  ┌─────────────────┐
            │ Vector Table    │  64 bytes (16 Cortex-M vectors)
0x20000040  ├─────────────────┤
            │ Code            │  ~400-600 bytes typical
0x2000E000  ├─────────────────┤
            │ Read Buffer     │  4KB (adjustable)
0x2000FE00  ├─────────────────┤
            │ Stack           │  256 bytes (grows down)
0x2000FF00  ├─────────────────┤
            │ Comm Area       │  256 bytes
0x20010000  └─────────────────┘
```

### Step 4: Define Communication Protocol

Use fixed memory addresses for host-MCU communication:

| Offset | Name | Purpose |
|--------|------|---------|
| +0x00 | STATUS | Command/status register |
| +0x04 | FLASH_ADDR | 24-bit flash address to read |
| +0x08 | SIZE | Bytes to read |
| +0x0C | DEST | Destination buffer in SRAM |
| +0x10 | JEDEC_ID | Result of ID read |
| +0x14 | ERROR | Error code if STATUS=ERROR |
| +0x18 | HEARTBEAT | Increments in main loop (proves code is running) |

**Status values:** 0x00=Idle, 0x01=Busy, 0x02=Done, 0xDEADxxxx=Error

**Commands:** 0x10=Read flash, 0x20=Get JEDEC ID, 0xFF=Exit

**Heartbeat usage:** Read this value twice with a short delay between. If it changes, the main loop is executing. If stuck, the code is blocked (likely in SPI polling).

### Step 5: Write RAM-Resident Code

Create minimal C code with these components. See `examples/spi_dump.c` for complete template.

**Critical requirements:**

1. **Vector Table** - Full Cortex-M vector table at SRAM start
2. **VTOR Setup** - Point VTOR to SRAM: `SCB_VTOR = 0x20000000`
3. **SPI Transfer** - Poll status, write TX, wait RX, read RX
4. **Command Loop** - Poll communication area, execute commands

### Step 6: Create OpenOCD TCL Script

Create TCL commands for loading and controlling the dumper. See `examples/spi_dump.tcl` for complete template.

**Key procedures:**
- `read_word` - Memory read wrapper (use `mem2array` for compatibility)
- `spi_load` - Load binary into SRAM
- `spi_init` - Set PC/SP from vector table, resume
- `spi_jedec` - Read and display JEDEC ID
- `spi_dump` - Dump flash in chunks to file

### Step 7: Build and Test

1. **Compile** with arm-none-eabi-gcc, -ffreestanding, -nostdlib
2. **Link** with custom linker script placing code at SRAM base
3. **Test JEDEC ID** first to verify SPI communication
4. **Full dump** only after JEDEC ID succeeds

## Critical Implementation Details

### VTOR Must Point to SRAM

Without setting VTOR, any exception uses flash vector table, causing crashes:

```c
*(volatile uint32_t*)0xE000ED08 = 0x20000000;
```

### SAM4S/SAM3X: SPI PCS Field Requirement

Even when using GPIO for chip select, SPI won't clock if PCS=0xF:

```c
SPI_MR = SPI_MR_MSTR | SPI_MR_MODFDIS | (0x0E << 16);  // PCS=NPCS0
```

### GPIO Chip Select Configuration

Reclaim CS pin for GPIO control:

```c
// SAM4S example for PA11
PIOA_PER = (1 << 11);   // Enable PIO control
PIOA_OER = (1 << 11);   // Enable output
```

### Watchdog Handling

Feed watchdog during long operations:

```c
for (i = 0; i < size; i++) {
    dest[i] = spi_transfer(0x00);
    if ((i & 0xFFF) == 0) {
        WDT_CR = 0xA5000001;  // SAM4S watchdog feed
    }
}
```

## SPI Flash Commands

Standard JEDEC commands work with most SPI flash chips:

| Command | Hex | Description |
|---------|-----|-------------|
| READ | 0x03 | Read data (24-bit address follows) |
| RDID | 0x9F | Read JEDEC ID (3 bytes returned) |
| RDSR | 0x05 | Read status register |

**JEDEC ID format:** Byte1=Manufacturer, Byte2=Type, Byte3=Capacity

Common manufacturers: 0x1F=Atmel, 0xEF=Winbond, 0xC2=Macronix, 0x20=Micron

## Troubleshooting

See `references/troubleshooting.md` for detailed solutions. Quick reference:

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| HardFault immediately | VTOR points to flash | Set SCB_VTOR = SRAM_BASE |
| SPI hangs polling | Clock not running | Check SPI_MR PCS field |
| Code stuck in spi_transfer | Wrong PC at start | Use init_dumper.sh to read PC from vector table |
| JEDEC returns 0x000000 | CS not toggling | Check GPIO config |
| JEDEC returns 0xFFFFFF | No flash response | Check wiring, mode, speed |
| Heartbeat not incrementing | Code blocked | Check PC - if in 0x2000004x, restart properly |

## Adapting to New MCUs

To support a new MCU:

1. **Find SPI registers** - Search datasheet for "SPI" section
2. **Find GPIO registers** - Search for "PIO" or "GPIO"
3. **Check SRAM location** - Usually 0x20000000 for Cortex-M
4. **Check watchdog** - Find feed/disable mechanism
5. **Verify SPI pins** - Which GPIO port/pins connect to flash

The core algorithm remains the same—only register addresses change.

## Additional Resources

### Reference Files

- **`references/mcu-registers.md`** - Detailed register maps for SAM4S, SAM3X, STM32F1, STM32F4, nRF52, LPC1768
- **`references/troubleshooting.md`** - Comprehensive troubleshooting guide with solutions

### Example Files

Complete, working templates in `examples/`:

**Source code:**
- **`spi_dump.c`** - RAM-resident C source with vector table and heartbeat
- **`spi_dump.ld`** - Linker script for SRAM execution
- **`spi_dump.tcl`** - OpenOCD TCL commands with JEDEC ID decoding

**Automation scripts (MCU-agnostic):**
- **`init_dumper.sh`** - Properly loads and initializes the dumper (reads SP/PC from vector table)
- **`dump.sh`** - Automated flash dump with parameterized memory addresses
- **`verify_dump.sh`** - Verifies dump integrity, detects stuck data lines

### Typical Workflow

**Quick start with shell scripts:**

```bash
# 1. Compile for your MCU (customize spi_dump.c first)
arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -Os -ffreestanding \
    -nostdlib -T spi_dump.ld -o spi_dump.elf spi_dump.c
arm-none-eabi-objcopy -O binary spi_dump.elf spi_dump.bin

# 2. Initialize the dumper (reads vector table automatically)
./init_dumper.sh spi_dump.bin

# 3. Dump the flash
./dump.sh firmware.bin 0x400000

# 4. Verify the dump
./verify_dump.sh firmware.bin 0x400000
```

**For LPC1768 (SRAM at 0x10000000):**
```bash
SRAM_BASE=0x10000000 ./init_dumper.sh spi_dump.bin
SRAM_BASE=0x10000000 ./dump.sh firmware.bin 0x100000
```

**Important: Proper Initialization**

The dumper MUST be started from its reset vector, not an arbitrary address. The `init_dumper.sh` script handles this automatically by reading SP and PC from the vector table:

```tcl
# WRONG - skips spi_init(), code will hang polling SPI
reg pc 0x20000041
resume

# CORRECT - starts from reset vector, runs full initialization
mem2array sp_arr 32 0x20000000 1
reg sp $sp_arr(0)
mem2array pc_arr 32 0x20000004 1
reg pc $pc_arr(0)
resume
```

For a guided interactive session, use the `/spi-dump` command which walks through the entire process step-by-step.
