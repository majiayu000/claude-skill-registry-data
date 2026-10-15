---
name: cua-driver
description: Drive a native macOS app via the cua-driver CLI (default) or MCP server — snapshot its AX tree, click/type/scroll by element_index, verify via re-snapshot. Use when the user (or an agent persona) asks to operate, drive, automate, or perform a GUI task in a real macOS application on the host (e.g. "open a file in TextEdit", "navigate to /Applications in Finder", "click the Save button in Numbers", control creative tools, etc.).
metadata:
  provided-by: "@islee23520/lfg (Grok Build adapter)"
  requires: "cua-driver CLI + daemon on the host (Accessibility + Screen Recording permissions)"
---

# cua-driver (Computer Use for Grok Build via LFG)

This skill is bundled by LFG so that agents and personas running under the Grok Build lazycodex/omo adapter (installed via `npx @islee23520/lfg setup`) can perform real desktop / native app automation on macOS.

It orchestrates the external `cua-driver` tool (the same one Codex/Grok Build environments use for Computer Use). The skill ensures the correct "snapshot before action, snapshot after verify, no unnecessary foreground" loop.

## Prerequisites on the host (user must have these)

1. `cua-driver` binary on PATH.
2. `cua-driver check_permissions` (grants Accessibility + Screen Recording to CuaDriver.app).
3. Daemon running: `open -n -g -a CuaDriver --args serve` (or `cua-driver serve &`).

If the prerequisites are missing the skill will tell the user exactly what to run.

## Core loop (always follow this)

```
launch_app({bundle_id}) or launch_app({bundle_id, urls:[...]})
  → pick window_id from the returned windows array (or list_windows)
  → get_window_state({pid, window_id})          # snapshot BEFORE
  → click / type_text / scroll / press_key / ... (always pass pid + window_id)
  → get_window_state({pid, window_id})          # snapshot AFTER — verify
```

Never skip the post-action snapshot. It is how you know the action actually happened and what the new AX state / visual is.

## Common patterns

- Open/launch an app (without stealing focus from the user's real foreground app): `launch_app`.
- Click, double-click, right-click, type, set whole field value, scroll, hotkeys, press individual keys: use the corresponding cua-driver tool with `(pid, window_id, element_index)` when possible.
- Pixel clicks (for canvas / WebGL / custom drawn areas that have no useful AX nodes): `click({pid, x, y})` etc. Coordinates come from the screenshot returned by `get_window_state`.
- Menu bar: only when the target is frontmost (rare in backgrounded flows). Prefer in-window controls.
- Backgrounded operation is the default and preferred — the driver is designed so the user's editor (or whatever they are typing in) stays frontmost.

## When to use this skill

- User says "click the ... button in <App>", "type ... into the field in Photoshop/Figma/Blender/...", "save the document", "export as PNG", "draw this shape", "navigate the UI of ...", "fill this form in the desktop app", control any native macOS GUI tool while the user keeps working elsewhere.
- Vision / screenshot inspection agents (multimodal-looker, artistry-qa, etc.) can request actions via this skill (or delegate to a worker persona that holds the cua loop).
- Any workflow that needs reliable desktop automation with before/after evidence.

## Relation to other skills / personas (LFG flavour)

The LFG-bundled "artistry" family (artistry, artistry-gen, artistry-qa, multimodal-looker, visual-engineering, ...) are pre-configured to delegate actual Computer Use execution to a worker that uses this skill. The "gen" worker does the observe → act → verify loop via cua-driver; the QA worker only looks at screenshots and gives verdicts.

You (the current agent) can do the same: when you need to drive the UI, invoke the cua-driver skill (or spawn a sub-task that uses it).

## Fallbacks if cua-driver is not installed on the host

- Clearly tell the user: "Computer Use requires cua-driver on this machine. Run: <exact install / permission commands>."
- Offer the Browser Use path (if a browser window is available) or pure prompt-based guidance as a degraded mode.
- Never pretend actions succeeded if the cua-driver calls are failing.

## Security / safety notes

- Never perform destructive actions (delete user files, send messages, submit financial forms, close unsaved work) without explicit confirmation of the exact step.
- The driver is intentionally backgroundable and does not steal focus by default. Respect the no-foreground contract.

This skill makes the full power of Codex-style Computer Use available to any Grok Build session that has the LFG adapter installed and enabled.
