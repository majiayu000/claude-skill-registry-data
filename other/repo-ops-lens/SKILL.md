---
name: repo-ops-lens
description: A repo audit panel that turns a GitHub link into a crisp operating brief, risk pass, and next-step suggestion.
---

# Repo Ops Lens

Use this skill when the user wants a polished macOS surface for A repo audit panel that turns a GitHub link into a crisp operating brief, risk pass, and next-step suggestion.

## Presentation

- Make the surface feel like a premium Apple utility.
- Lead with one calm summary line and one clear action.
- Keep the visual language restrained, dark, and readable at a glance.

## Build shape

- Prefer a menu-bar popover or compact status-item panel.
- Show the primary state first, then the useful detail lines.
- Takes a repository URL and reduces it to what matters next.
- Makes risk and architecture notes visible without a long read.
- Builds a clean bridge between research and action.

## Guardrails

- Do not invent unsupported metrics or background services.
- Keep the app simple enough to feel native on macOS.
- Use one primary action and a small set of supporting actions.

## Prototype

- SwiftUI starter files live in `prototype/`.
- The prototype should stay menu-bar first and easy to transplant into a real macOS target.

## When extending

- Add more depth only when it improves the single workflow the skill is meant to solve.
- If the skill grows, keep the menu-bar path short and the detail panel readable.
