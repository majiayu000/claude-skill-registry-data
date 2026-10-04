---
name: Autodesk
description: Control Autodesk desktop apps - 3ds Max and friends - from the shell via Flue, without an MCP server.
---
This skill lets a coding agent operate **Autodesk desktop applications** through [Flue](https://github.com/SFKislev/flue), a local shell-to-application bridge. Flue currently covers **Autodesk 3ds Max** through a consistent stdin/stdout contract; further Autodesk adapters are in scope.

> agent shell -> `3dsmax_bridge.py` -> MAXScript / Python -> JSON result

## When to use
The human requests work performed **inside an Autodesk desktop app** — inspect the open scene, objects, modifiers, materials, selection; make bounded edits; run small scripts. A CLI agent cannot act inside these apps without a bridge like Flue.

## How to proceed
1. **Read `FLUE.md` in this directory first.** It explains how Flue works, the bridge contract, a worked example, and safety expectations.
2. **Identify which Autodesk app the human is working in** (currently 3ds Max) and use the matching adapter (e.g. `adapters/3dsmax_adapter/3dsmax_bridge.py`).
3. **If Flue is installed:** also read `C:\Users\fredd\.claude\skills\flue\SKILL.md` and the matching `adapters/<app>_adapter/APP.md` for the operational contract, then work from there.
4. **If Flue is not installed:** tell the human. The install command is `pip install flue && flue setup`. Do not install without explicit approval in the current session.

## Other apps
Flue also supports Photoshop, Illustrator, Premiere, After Effects, InDesign, Audition, Blender, Houdini, Unity, and Microsoft Office through the same stdin/stdout contract. One install covers all adapters.

## Safety
Flue acts inside professional desktop software. Treat the human as the driver; prefer small, inspectable steps; avoid destructive actions unless explicitly requested. Flue is MIT-licensed and reviewable on GitHub / PyPI before use.
