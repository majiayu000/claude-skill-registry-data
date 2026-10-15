---
name: cua-driver
description: Drive a native macOS app via the cua-driver CLI (default) or MCP server — snapshot its AX tree, click/type/scroll by element_index, verify via re-snapshot. Use when the user (or an agent persona) asks to operate, drive, automate, or perform a GUI task in a real macOS application on the host (e.g. "open a file in TextEdit", "navigate to /Applications in Finder", "click the Save button in Numbers", control creative tools, etc.).
metadata:
  provided-by: "@islee23520/lfg (Grok Build adapter)"
  requires: "cua-driver CLI + daemon on the host (Accessibility + Screen Recording permissions)"
---

# cua-driver (Computer Use for Grok Build via LFG)

This skill is provided by the LFG Grok Build adapter (`npx @islee23520/lfg setup`).

It gives Grok agents and custom personas the ability to perform real Computer Use / desktop automation on macOS using the external `cua-driver` tool (the same foundation used by Codex-style computer-use flows).

## What you get after `lfg setup`

- The skill becomes available at `~/.grok/installed-skills/cua-driver/SKILL.md`.
- Agent/persona configs (including the bundled LFP-style "artistry" family) can delegate actual UI driving to a worker that uses this skill.
- Any Grok session using the lfg adapter can invoke cua-driver loops for native app control while the user keeps their foreground editor active.

## Prerequisites (must be satisfied on the user's machine)

1. `cua-driver` binary is on PATH.
2. Permissions granted: Accessibility + Screen Recording for CuaDriver.app (run `cua-driver check_permissions`).
3. Daemon started: `open -n -g -a CuaDriver --args serve` (or `cua-driver serve &`).

The skill will guide the user with the exact commands if any of these are missing.

## Recommended usage pattern (always snapshot before + after)

```
launch_app({bundle_id: "..."})           # or with urls for documents
  → get_window_state({pid, window_id})   # before
  → click / type_text / scroll / press_key / hotkey / ... (pass pid + window_id + element_index when possible)
  → get_window_state({pid, window_id})   # after — this is mandatory verification
```

Use `element_index` (from the AX tree) for reliable backgrounded actions. Fall back to pixel coordinates (`click({pid, x, y})`) only for canvas / custom-drawn surfaces that have no useful AX nodes. The screenshot returned by `get_window_state` is the source of truth for pixel coordinates.

## Backgrounded by default (no focus steal)

The driver is designed so the user's real foreground app (editor, terminal, browser, etc.) is not disrupted. Most operations work on hidden / off-Space / minimized windows (with known limitations documented in the full cua-driver skill).

Only use `osascript ... activate` when the user has explicitly said they want the target app brought to the front.

## Relation to LFG-bundled personas

The "artistry" agent family (artistry, artistry-gen, artistry-qa, multimodal-looker, visual-engineering, ...) that ships with LFG is pre-wired to use Computer Use workers. The "gen" worker performs the observe-act-verify loop via this skill; QA workers only consume screenshots for judgment.

You can do the same: when an agent needs to click/type/drive a native macOS tool, route through cua-driver (directly or by delegating to a suitable worker persona).

## Safety

- Never perform destructive or high-stakes actions (delete files, send communications, submit orders, close unsaved work) without the user explicitly confirming the exact step.
- The skill will refuse or ask for confirmation on obviously dangerous operations.

## Fallbacks

If `cua-driver` is not available on the host:
- Clearly explain the missing prerequisite and the exact setup commands.
- Offer degraded paths (Browser Use against a visible browser, or high-level guidance without actual GUI actions).

This makes full Codex-style Computer Use available to Grok Build users who install the LFG adapter.
