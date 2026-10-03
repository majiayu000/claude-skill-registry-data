---
name: battery-trend-scout
description: Build a polished macOS battery utility that shows charge, power source, energy mode, significant energy users, and local drain trends from a menu bar surface.
---

# Battery Trend Scout

Use this skill when the user wants a better battery experience than the stock macOS panel: menu bar first, compact at a glance, and deeper when opened.

## Presentation

- Make the surface feel like a polished Apple utility, not a diagnostics dump.
- Lead with one calm status line and one clear trend cue.
- Keep the visual language dark, minimal, and readable at a glance.

## Build shape

- Prefer an AppKit status item with SwiftUI content in the popover or detail window.
- Show battery percentage, charging state, power source, low power mode, and energy mode first.
- Add a compact trend strip for recent charge or drain samples if local history exists.
- Surface significant energy users only when the system exposes them.
- If the Mac has no battery, fall back to power source and energy load signals without pretending to show laptop-only data.

## Guardrails

- Do not invent health, temperature, or history metrics that the system does not expose.
- Keep the menu bar icon simple and professional.
- Use one clear primary action: open details, not a crowded command sheet.
- Make the detail panel readable on a small screen and graceful on desktop Macs.

## Good defaults

- Use restrained typography and monochrome system symbols.
- Prefer one clean summary line over multiple noisy badges.
- Keep trend logic local and reversible.
- If exporting, prefer a small text or markdown snapshot over a heavy report.

## When extending

- Add history sampling only if it improves a visible user decision.
- Add settings only if they affect battery visibility, refresh rate, or alert thresholds.
- If the user asks for a bigger product, turn the skill into a menu bar app plus a details board, not a full dashboard.
