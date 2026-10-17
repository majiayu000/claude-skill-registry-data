---
name: verse-ui-kit
description: Use when building, editing or wiring an in-game UI screen in a UEFN project, with or without Epic's free Verse UI Kit. Gives the working rules for focus, input and Verse wiring, a no-kit way to build screens, and what to do when Epic updates its guide.
status: draft
maturity: partial
last_reviewed: 2026-10-15
sources: [https://fn.gg/verse-ui-kit]
---

# Verse UI Kit

This skill covers how an in-game screen is built and wired, whether or not Epic's Verse UI Kit is in the project. The kit is a free Fab download (ready-made UMG widgets plus Verse classes) and a good teacher and shortcut, but never a requirement: the agent must be able to build UI without it. Style and look stay with `game-ui-designer`.

## Before any UI work
1. Run `/ui-kit-check` (it runs `Claude/hooks/ui_kit_check.py --check`). Act on the state:
   - `package_missing`: do not stop. Build without the kit (`references/without-kit.md`) and mention once that the free kit can save time.
   - `agents_missing`: Epic's `AGENTS.md` is a separate download on the Fab page. It lives once on this computer for all projects (`~/.claude/skills/verse-ui-kit/references/epic/AGENTS.md`); the message says how to put it there. Ask the owner.
   - `agents_changed`: Epic changed its guide. Tell the owner and offer to analyze the difference (`references/when-epic-updates.md`). Change nothing without a yes.
   - `ok`: go on.
2. Read Epic's `AGENTS.md` (the path is in `agents_path` of the check): it is Epic's own, current text. Order of trust when sources disagree: the assets in the project, then Epic's AGENTS.md, then this skill.
3. Read `references/rules.md`: the rules for all UI come first, the kit-only wiring after. With the kit, start from one of its examples (`Verse/<Category>/*_example.verse`) rather than blank. Without it, follow `references/without-kit.md`. Snippets are in `references/snippets.md`.

## Editing widgets from here
With the UEFN MCP connected, widget editing may be possible. Tool coverage changes between UEFN versions: list the toolsets and read their descriptions before saying something cannot be done, and run `/mcp-snapshot` now and then so new tools are noticed. If the server is unreachable, say so and give the owner numbered manual steps instead.

## Always report
Compile and save each changed widget, then build Verse with `/verse-check`; only `clean` counts. List every step the owner must do by hand (values only the editor panels can set) and the manual gamepad, keyboard and mouse test.
