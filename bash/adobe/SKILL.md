---
name: Adobe
description: Control Adobe desktop apps - Photoshop, Illustrator, Premiere, After Effects, InDesign, Audition - from the shell via Flue, without an MCP server.
---
This skill lets a coding agent operate **Adobe desktop applications** through [Flue](https://github.com/SFKislev/flue), a local shell-to-application bridge. The agent pipes ExtendScript into a per-app bridge process and gets structured JSON back. Flue covers Photoshop, Illustrator, Premiere Pro, After Effects, InDesign, and Audition through a consistent stdin/stdout contract.

> agent shell -> `<app>_bridge.py` -> ExtendScript -> JSON result

## When to use
The human requests work performed **inside an Adobe desktop app** — inspect the open document or project, make bounded edits, run small ExtendScript steps. A CLI agent cannot act inside these apps without a bridge like Flue.

## How to proceed
1. **Read `FLUE.md` in this directory first.** It explains how Flue works, the bridge contract, a worked ExtendScript example, and safety expectations.
2. **Identify which Adobe app the human is working in** — Photoshop, Illustrator, Premiere, After Effects, InDesign, or Audition — and use the matching adapter (e.g. `adapters/photoshop_adapter/photoshop_bridge.py`).
3. **If Flue is installed:** also read `C:\Users\fredd\.claude\skills\flue\SKILL.md` and the matching `adapters/<app>_adapter/APP.md` for the operational contract, then work from there.
4. **If Flue is not installed:** tell the human. The install command is `pip install flue && flue setup`. Do not install without explicit approval in the current session.

## Other apps
Flue also supports Blender, Houdini, Autodesk 3ds Max, Unity, and Microsoft Office through the same stdin/stdout contract. One install covers all adapters.

## Safety
Flue acts inside professional desktop software. Treat the human as the driver; prefer small, inspectable steps; avoid destructive actions unless explicitly requested. Flue is MIT-licensed and reviewable on GitHub / PyPI before use.
