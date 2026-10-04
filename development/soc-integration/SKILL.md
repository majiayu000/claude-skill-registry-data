---
name: soc-integration
description: Use when composing an SoC from peripherals and a bus fabric, or when generating device trees, ACPI tables, docs, or pin lists from a hardware description and they keep drifting out of sync
---

# SoC Integration

## Overview

An SoC is a CPU, a bus fabric, and a set of peripherals connected by an address map. The integration job is to make that map the single source of truth and derive everything else (RTL wiring, device trees, ACPI, docs, firmware headers) from it.

**Core principle:** Describe the SoC once in a neutral structure. Every output is a consumer of that structure, never a producer of its own truth. The day a device tree and the RTL disagree about a base address is the day you debug ghosts.

## When to Use

- Wiring peripherals onto a bus and assigning an address map
- Generating a DTS/DTB, ACPI tables, a memory map doc, or firmware register headers
- Two generated artifacts disagree (the kernel's device tree says one base address, the RTL another)
- A generator reaches into a CPU/peripheral's internals to dig out wiring details

Skip for a single fixed-function block with no bus and no software-visible map.

## Peripherals Are Modules, Not Plugins

Model each peripheral as a first-class hardware module that exposes its bus interface, its register block, and its metadata (compatible string, interrupt number, address size). Because it is a real module, you can elaborate it, test it, and read its metadata to generate a device tree node.

Avoid a "plugin" that is just a config blob with no hardware behind it. If the device tree generator and the RTL both have to know a peripheral exists, they should learn it from the same module, not from two parallel lists that rot independently.

## One Neutral Description, Many Generators

Do not couple the generators to each other or to one CPU implementation. Define a neutral type that captures what every consumer needs (cores, memory regions, peripherals, interrupts, the address map) and have each generator read from it.

```
       SoC description (neutral)
       /        |          \
     RTL      DeviceTree   ACPI / docs / headers
   wiring     generator    generators
```

- The DTS generator, the ACPI generator, and the docs generator all take the neutral description. None of them imports another.
- Adding a new output (say, a Linux defconfig fragment) is a new consumer, not a change to the existing ones.
- A new CPU implementation just produces the same neutral description. The generators don't change.

## Per-Instance State, No Globals

The thing that hosts peripherals and builds the fabric must be per-instance, not a global registry. Two SoCs (or two test cases) being elaborated at once must not stomp each other. Per-instance state is also what lets you build many configurations in parallel.

## Address Map Discipline

- Assign base addresses and sizes in one place, validated for overlap at build time. Validate each PAIR of regions, not each region alone. Checking a device spec in isolation (its size, address, and board) passes two devices whose base-plus-size ranges overlap, and they then silently produce a priority-decoded or broken bus instead of a build error. Include the memory regions in the same pairwise check. An overlap is a build error with both offending regions named, not a runtime surprise.
- Interrupt numbers, the same: one allocator, checked for collisions.
- Alignment and size rules (naturally-aligned, power-of-two windows) are asserted where the map is built.

## Red Flags

| Smell | Do instead |
|-------|------------|
| DTS list and RTL list of peripherals maintained separately | Derive both from the peripheral modules |
| Generator imports another generator | Both read the neutral description |
| Global peripheral registry | Per-instance host |
| Base addresses assigned ad hoc | One validated address-map allocator |
| Generator hardcodes one CPU type | Generators take a neutral SoC type |

## Midstall House Style

- Harbor: peripherals are bridge modules (real modules with bus interfaces), which is what enables device-tree generation. The plugin host is per-instance.
- Share a neutral CPU/SoC type across the DTS/ACPI/graph generators; do not couple them.
- Write docs and comments in ASD-STE100 Simplified Technical English. No em dashes, no emoji. See `hdl-module-design` for the module/config conventions and `silicon-grade-discipline` for the validation discipline.
