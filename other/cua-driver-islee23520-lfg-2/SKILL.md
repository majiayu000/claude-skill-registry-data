---
name: cua-driver
description: Drive a native macOS app via the cua-driver CLI (default) or MCP server — snapshot its AX tree, click/type/scroll by element_index, verify via re-snapshot. Use when the user (or an agent persona) asks to operate, drive, automate, or perform a GUI task in a real macOS application on the host.
metadata:
  provided-by: "@islee23520/lfg (Grok Build adapter)"
  requires: "cua-driver CLI + daemon on the host (Accessibility + Screen Recording permissions)"
---

# cua-driver (Computer Use)

Bundled by LFG for Grok Build. See the full version under the materialized plugin or the host's cua-driver skill for the complete guide.

Core contract: always snapshot (get_window_state) before and after every action. Prefer element_index over raw pixels. Never foreground the target unless the user explicitly asked for frontmost state.

This skill lets Grok agents drive real desktop apps (creative tools, Finder, browsers in controlled ways, etc.) while the user continues working in their foreground editor.
