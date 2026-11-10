---
name: open-design-integrations
description: Show which services Open Design can use directly (Canva, Figma, Notion, Google Drive, Slack, social posting), whether each is connected, and how to set one up — use whenever the user asks which integrations, connectors or services Open Design can use, what's connected, or how to connect Canva, Figma, Notion, Google Drive, Slack or a social posting service
---

<!-- generated:open-design-agent-kit -->

Show the user Open Design's integrations and whether each one is connected here.

Request: the rest of the user's message (if there is none, ask the user: "Anything you'd like to connect? (or leave empty to just see the list)")

**How to talk to the user.** Many people using Open Design don't write code, so:
- Use the user's own words. If they say "artifact", "design tokens" or give a file path, use those terms back; otherwise use the plain words below.
- Keep the machinery out of replies: no tool names, no ids like `od:prototype:poster-hero`, no internal files (`.artifact.json`, `.comments.json`, `config.json`), and not the words "register", "manifest", "sidecar", "entry" or "surface", unless the user used them first.
- Explain a print term the first time it comes up, in one short clause, and not again.
- Say where a file is the way the user would find it ("in your Open Design folder, under seed-swap-flyer"). Give a raw path only where the user can click it (Claude Code, Claude Desktop's Code tab, VS Code) or asks for it.
- End each reply that finishes a step with one line on what they can do next, with at most two options ("Want it in Instagram sizes too, or is it ready to print?").

| Instead of | Say |
|---|---|
| artifact, entry, registered | your design, saved |
| design system, active design system | your style (the first time: "a saved style: colours, fonts and spacing") |
| surface, skill, template, recipe | kind of design, starting layout, or nothing |
| workspace, output directory | your folder, your Open Design folder |
| bleed | print edge ("a few millimetres extra that the printer trims off") |
| trim size | final size |
| preflight findings, errors | "I checked it and fixed…", "one thing to look at:" |
| export | save as PDF, save as an image |
| inline preview, MCP App | the preview above |

## 1. Get the list

Call `list_open_design_integrations` with no arguments. It returns every integration grouped by purpose, each with what it does, the tool names that show it's connected on this agent, whether it can be set up here, and how to manage without it.

## 2. Work out each status

Use exactly three statuses:
- 🟢 **Connected**: your own tools include one matching its "Connected if your tools include" hints. Check deferred or on-demand tools too (search for them) before deciding one is missing.
- 🟡 **Installed, not connected**: it's configured but its tools aren't available (it needs sign-in, failed to connect, or needs a restart). If you can run shell commands, run the read-only `claude mcp list` (Claude Code) or `codex mcp list` (Codex) and look for its server name or URL; a configured server without matching tools is 🟡. Run nothing else.
- ⚪ **Not installed**: neither of the above.

If you can't run those commands, use only 🟢 and ⚪, and say that an integration you've already added may need a restart to show up.

## 3. Reply

Show one short table per group (Design, Docs & storage, Team, Social posting), in the order the list gives:

| | Integration | What it does in Open Design | Next step |
|---|---|---|---|

- The first column is the dot only.
- Next step: "Ready to use" for 🟢; "Sign in or restart (`/mcp` in Claude Code, `codex mcp login <name>` in Codex)" for 🟡; "Ask me to set it up" for ⚪ when it can be set up here, otherwise "Manual setup" plus one line from its manual path.

End with a one-line legend (🟢 connected · 🟡 installed, not connected · ⚪ not installed) and offer to set up any ⚪ integration the user names.

## 4. Setting one up (only when asked)

Don't install anything from the list itself. If the request above, or the user's answer, names an integration to set up: call `list_open_design_integrations` with that `integration`, and follow its setup steps and rules. That means asking for and getting the user's yes before installing anything, and never asking for or writing an API key.
