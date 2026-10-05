---
name: Blender
description: Control Blender from the shell via Flue - a Python bridge to bpy without an MCP server.
---
This skill lets a coding agent operate **Blender** on the desktop through [Flue](https://github.com/SFKislev/flue), a local shell-to-application bridge. The agent pipes Python into `blender_bridge.py` and gets structured JSON back. Flue is **not an MCP server** — it is a thinner, simpler shell contract that drives Blender's own `bpy` runtime directly.

> agent shell -> `blender_bridge.py` -> bpy -> JSON result

## When to use
The human requests work performed **inside Blender** — inspect the open scene, collections, objects, meshes, materials, selection; make bounded edits; run small `bpy` scripts. A CLI agent cannot act inside Blender without a bridge like Flue.

## How to proceed
1. **Read `FLUE.md` in this directory first.** It explains how Flue works, the bridge contract, a worked `bpy` example, and safety expectations.
2. **If Flue is installed:** also read `C:\Users\fredd\.claude\skills\flue\SKILL.md` and `adapters/blender_adapter/APP.md` for the operational contract, then work from there.
3. **If Flue is not installed:** tell the human. The install command is `pip install flue && flue setup`. Do not install without explicit approval in the current session.

## Other apps
Flue also supports Photoshop, Illustrator, Premiere, After Effects, InDesign, Audition, Houdini, 3ds Max, Unity, and Microsoft Office through the same stdin/stdout contract. One install covers all adapters.

## Safety
Flue acts inside professional desktop software. Treat the human as the driver; prefer small, inspectable steps; avoid destructive actions unless explicitly requested. Flue is MIT-licensed and reviewable on GitHub / PyPI before use.
