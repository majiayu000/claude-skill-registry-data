---
name: Premiere
description: Control Adobe Premiere Pro from the shell via Flue - ExtendScript bridges without an MCP server.
---
This skill lets a coding agent operate **Adobe Premiere Pro** on the desktop through [Flue](https://github.com/SFKislev/flue), a local shell-to-application bridge. The agent pipes ExtendScript into `premiere_bridge.py` and gets structured JSON back.

> agent shell -> `premiere_bridge.py` -> ExtendScript -> JSON result

## When to use
The human requests work performed **inside Premiere** — inspect the open project, sequences, clips, markers; make bounded edits; run small ExtendScript steps. A CLI agent cannot act inside Premiere without a bridge like Flue.

## How to proceed
1. **Read `FLUE.md` in this directory first.** It explains how Flue works, the bridge contract, a worked ExtendScript example, and safety expectations.
2. **If Flue is installed:** also read `C:\Users\fredd\.claude\skills\flue\SKILL.md` and `adapters/premiere_adapter/APP.md` for the operational contract, then work from there.
3. **If Flue is not installed:** tell the human. The install command is `pip install flue && flue setup`. Do not install without explicit approval in the current session.

## Other apps
Flue also supports Photoshop, After Effects, Illustrator, InDesign, Audition, Blender, Houdini, 3ds Max, Unity, and Microsoft Office through the same stdin/stdout contract. One install covers all adapters.

## Safety
Flue acts inside professional desktop software. Treat the human as the driver; prefer small, inspectable steps; avoid destructive actions unless explicitly requested. Flue is MIT-licensed and reviewable on GitHub / PyPI before use.
