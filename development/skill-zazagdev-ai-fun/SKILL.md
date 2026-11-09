---
name: setup-map
description: Use when the user wants to see their Claude Code setup as a picture, asks for a setup map, a map or overview of their skills, plugins, agents, MCP servers, hooks, commands, rules and memory, wants to see which projects they work in or which have their own setup, or types /setup-map. Builds one local 3D HTML page from ~/.claude and every project Claude Code has worked in.
---

# Setup map

`$MAP` below is `python "$HOME/.claude/skills/setup-map/scripts/setup_map.py"`.

1. Run `$MAP --open`. It maps the global setup and every project Claude Code has
   worked in, from its session history (`cwd` and file dates only, never what was
   said) and `~/.claude.json`, so it does not matter which folder this runs from.
   If the user names a folder of projects Claude Code has never been opened in, pass
   it first: `$MAP "<folder>" --open`. It reads `~/.claude`, `~/.claude.json`
   and each project's own `.claude` folder, writes the page to
   `~/setup-map/setup-map.html`, opens it in the browser, and prints the counts.
   - Add `--out <file>` only if the user asks for another place.
   - Add `--projects-json <file>` only if the user keeps a JSON list of their projects
     (`{"projects": [{"name", "path"}], "scanRoots": [...]}`) and names it.
2. Reply with the page path, the counts line, how many projects have a setup of their
   own, and anything the script printed as "not shown".

The page holds the names of the user's projects, skills and memory folders. Never
publish it, upload it or commit it unless the user asks, and then only privately.
