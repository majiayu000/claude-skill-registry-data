---
name: saga-labs-engineering-orbit
description: Enforces the SaGa Labs Metisa Orbit engineering standard across all UI surfaces, tools, firmware generators, and client documentation, matching professional motorsport ECU calibration standards (Ecumaster/MoTeC benchmark) with dark obsidian titanium palettes, zero emojis, hairline vector iconography, right-aligned physical units, and factual architecture.
---

# SaGa Labs Engineering Orbit Standard

The SaGa Labs Metisa Orbit standard governs all visual, technical, and architectural interfaces across SaGa Labs products. It establishes an uncompromising, motorsport-grade engineering ethos inspired by industry benchmarks such as Ecumaster and MoTeC. Quality is demonstrated strictly through high data density, physical accuracy, and deterministic system architecture—never through marketing slogans, decorative fluff, or consumer emojis.

## Use when

- Authoring, modifying, or reviewing user interfaces (HTML, CSS, JS, desktop clients, mobile HMIs, dashboards).
- Writing documentation, field integration guides, manuals, or engineering specifications.
- Implementing configuration tools, firmware generators, calibration tables, or serial telemetry decoders.
- Creating prompts, subagent configurations, or system directives for any AI agent working on SaGa Labs repositories.

## Procedure

1. **Eliminate All Emojis & Toy Symbols**:
   - Strictly prohibit Unicode emojis (e.g., no 🔌, 🔋, 🚴, ⚙️, 🔑, 📱, ❓, ⚠️, 🚀).
   - Use only 1.5px monochrome hairline stroke vector SVGs (`currentColor`) or clear typographical status beacons (`[V]`, `[A]`, `[W]`, `[km/h]`, `[ms]`, `[ADC]`).
   - SVG icons must scale within a 14x14px to 18x18px bounding box in neutral slate (`#64748b`), switching to high-contrast cyber-orange (`#ff6200`) only when active or hovered.

2. **Apply the High-Density Motorsport Palette**:
   - Background Canvas: Deep Obsidian (`#08090d`).
   - Structural Panels & Cards: Titanium Gray (`#121620`, `#151a26`).
   - Borders & Separators: Hairline 1px Slate (`#1e2638`, `#273248`).
   - Primary Accent & Traces: Cyber-Orange (`#ff6200`).
   - Status LEDs / Beacons: Green (`#10b981`), Amber (`#f59e0b`), Red (`#ef4444`), Cyan (`#06b6d4`).
   - Monospace Typography: JetBrains Mono / SF Mono / Consolas for all parameters, values, and units.

3. **Enforce Factual Motorsport & Power Electronics Terminology**:
   - Use precise engineering vocabulary: *DC Bus Primary Feed*, *Inverter Endstufe*, *Cadence Dynamics*, *Throttle Transfer Function*, *Solid-State Brake Interlock*, *ECE-R 50 Flash Timing*, *Track & Dyno Calibration Authorization*.
   - Never use colloquial marketing phrases (*"Keine Grenzen"*, *"Ein Gehirn. Jede Maschine."*, *"Das Kernversprechen"*, etc.).
   - Values must always display explicit physical units enclosed in square brackets aligned to the right (e.g., `42.0 [V]`, `25.0 [A]`, `250 [W]`, `2200 [mm]`).

4. **Maintain Deterministic Calibration Hierarchies**:
   - Level 0: Standard Regulatory Derating (Active on cold boot / MCU reset, 25 km/h, 250 W, PAS mandatory).
   - Level 1: Sport Calibration (32 km/h, 500 W).
   - Level 2: Track & Dyno Closed-Course Calibration (Up to 99 km/h, 3000 W, decoupled throttle).
   - Never generate or store plain-text unlock PINs inside configuration clients. PIN generation must remain isolated in dedicated authorization portals with cryptographically salted hashes tied to hardware serial numbers and recorded legal waivers.

5. **Verify Contract Parity & Zero Regression**:
   - Run `python tools/test_configurator_contract.py`.
   - Run `python tools/source_contract_test.py`.
   - Run `python tools/testbench_harness.py`.
   - Run `python tools/validate_project_context.py`.

## Constraints

- Never weaken or bypass safety interlocks (brake cutoff &lt; 2 ms, low-voltage cutoff, thermal horn timeout).
- Never claim MCU safety qualification from a build without physical hardware test evidence.
- Never reintroduce consumer emojis or marketing slogans into any file or document.
- Never invent unverified hardware pinouts, ADC dividers, or shunt values.

## Done when

- All affected files adhere 100% to the SaGa Labs Orbit palette and design tokens.
- Zero consumer emojis exist across code, templates, and documentation.
- All test contracts and project context validation scripts pass with 0 errors.
