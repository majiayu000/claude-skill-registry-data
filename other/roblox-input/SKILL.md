---
name: roblox-input
description: "Use when handling Roblox touch, gamepad, keyboard, mouse or motion input, on-screen action buttons, or cross-platform action binding."
when_to_use: "Also when a button fires by accident, controls don't work on mobile or console, a controller gets stuck in a menu, or button prompts show the wrong key."
last_reviewed: 2026-10-14
sources:
  - https://devforum.roblox.com/t/the-correct-way-to-design-mobile-buttons/2494558
  - https://create.roblox.com/docs/reference/engine/classes/UserInputService
  - https://create.roblox.com/docs/reference/engine/enums/PreferredInput
  - https://create.roblox.com/docs/input/mobile
  - https://create.roblox.com/docs/production/publishing/console-guidelines
  - https://create.roblox.com/docs/reference/engine/classes/ContextActionService
  - https://create.roblox.com/docs/reference/engine/classes/Tool
  - https://create.roblox.com/docs/studio/controller-emulator
  - original
  - https://create.roblox.com/docs/projects/server-authority
  - https://create.roblox.com/docs/ui/3D-drag-detectors
  - https://create.roblox.com/docs/ui/ui-drag-detectors
---

# Roblox Input

## When to Load

Touch, gamepad, keyboard, mouse or motion input, on-screen action buttons, cross-platform binding. Client-only; Server Authority simulation input uses the Input Action System.

## Quick Reference

- **Events:** `InputBegan/Changed/Ended` give `(input, gameProcessedEvent)`; filter it for gameplay. Wheel fires only `InputChanged`.
- **Bindings:** prefer `ContextActionService:BindAction(name, handler, touchButton, ...keys)`; gate on `state` (touch is `KeyCode.Unknown`); stack order, so `BindActionAtPriority`. Server Authority: `InputAction`/`InputContext` + `RunService:BindToSimulation()` (needs `Workspace.UseFixedSimulation`).
- **Mobile first, hybrid aware:** show controls from `UserInputService.PreferredInput` (`Enum.PreferredInput`), observed with `GetPropertyChangedSignal`, not from `TouchEnabled` cached once.
- **Touch action buttons:** fire only for touches that began on the button; camera drags across it never fire. Place from the measured jump button under `PlayerGui.TouchGui`; clear the thumbstick zone.
- **Gate gameplay:** block attacks while a game window is open, a `TextBox` is focused, `GuiService.MenuIsOpen`, or `GuiService.SelectedObject` is set.
- **Cancel is not release:** holds cancel on window open, `Cancel`, unequip, focus loss, input switch or pad disconnect.
- **Gamepad tools:** default controls bind `ButtonR2` through `BindActivate`; `Tool.ManualActivationOnly = true` disables it. Aim from the screen center on gamepad, not `GetMouseLocation()`.
- **Hints:** `GetStringForKeyCode(key, Enum.KeyCodeStringFormat.Abbreviated)`, `GetImageForKeyCode`, or `InputActionLabel`; never hardcode Xbox names.
- **Test:** Device Simulator + Controller Emulator; menu focus is in `roblox-gui`.

> Details: [references/full.md](references/full.md)
