---
name: implement-input-handler
description: "Use when you have an input mapping spec (input_mapping.md) and need to generate the ActionID enum, platform binding tables, and InputHandler abstraction."
---

## 1. Overview
Generates cross-platform input abstraction layer: translates raw hardware (KBM, Gamepad, Touch) to semantic `ActionID`s from `input_mapping.md`. Gameplay queries independent of device handling; analog signals pass through standardized filtering.

## 2. When to Use

Use when:
- You have an `input_mapping.md` and need the ActionID enum, platform binding tables, and InputHandler abstraction generated.
- Your game supports multiple input devices (keyboard/mouse, gamepad, touch) and you want a single abstraction.
- Gameplay code is checking raw keys/buttons instead of semantic actions.

Do not use when:
- The input mapping spec doesn't exist yet — define player controls first with `define-player-controls`.
- You're building a single-platform prototype with no plan to support other inputs.

## 3. Core Pattern

1. **Environment Analysis**: Scan config for target platforms/language.
2. **Semantic Definition**: Single `ActionID` enum + typed hardware enums (Key, Button, Stick, DPad, TouchInput).
3. **Binding Synthesis**: Platform-specific tables (KBM, Xbox, PS, Touch) mapping `ActionID`s → physical inputs per spec.
4. **Abstraction**: Analog signal processing (DeadZone filtering/curve shaping) + core `InputHandler` interface + `MockInputHandler` for testing.

## 3. Interaction Protocol
- **[Hardware Leakage]**: Raw key check in game logic → "Use semantic ActionIDs instead of raw keys. Refactor to InputHandler abstraction?"
- **[Platform Ambiguity]**: Target unclear → "Need target platform (Mobile vs PC) for binding tables. Default to [Platform X] or specific requirements?"

## 4. Quality Gates - STOP
- **Hardware Abstraction**: Use semantic ActionIDs exclusively in gameplay logic
- **Platform Alignment**: Hardware assumptions translate across touch/controller via abstraction layer
- **Filtered Analog**: Apply deadzone/filtering for smooth, responsive analog controls

## 5. Final Integrity Audit
- [ ] All semantic actions in unique `ActionID` enum entries
- [ ] Binding tables for every target platform
- [ ] Analog signals include deadzone + response curve
- [ ] Gameplay code uses only ActionIDs, not raw hardware constants
- [ ] `MockInputHandler` available for testing
