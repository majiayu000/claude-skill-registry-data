---
name: roblox-localization-accessibility
description: Improve Roblox localization and accessibility readiness. Use for UI text scaling, language-ready copy, icon clarity, color contrast, younger-player comprehension, readable HUDs, input accessibility, and reducing text-heavy onboarding.
---

# Roblox Localization Accessibility

## Goal

Make the game understandable to more players across devices, languages, and abilities.

## Text

- Keep UI copy short and simple.
- Avoid idioms that translate poorly.
- Separate display strings from logic where practical.
- Leave room for longer translated text.
- Prefer icons plus short labels for repeated actions.
- Avoid tutorial walls.

## Readability

- Use strong contrast for HUD and buttons.
- Keep text readable on phone screens.
- Avoid placing text over busy backgrounds.
- Ensure numbers, timers, and reward deltas are legible.
- Use consistent icon meaning.

## Accessibility

- Avoid color-only state communication.
- Provide clear disabled/pressed/selected states.
- Keep tap targets large.
- Avoid core actions that require precise timing unless that is the genre.
- Reduce flashing and excessive screen shake for common actions.

## Review Output

Return:

- Localization risks.
- Accessibility risks.
- UI copy improvements.
- Mobile readability fixes.
- Highest-impact changes before launch.

## Next

Verify readability and input across devices with `roblox-mobile-playtest` and `roblox-playtest-qa`.

