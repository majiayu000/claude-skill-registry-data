---
name: ai-maxxing-skills
description: Install, update or remove skills of the ai-maxxing package on this server with hermes-setup (connect-tool, create-landing, create-software, verify, grill-me, lumail, stripe-checkout...). Use when the owner asks which skills exist, asks to install, add, update or remove a skill, or asks for a job a package skill does that is not installed yet.
---

# Skills of the ai-maxxing package

Every skill on this server lives in `~/.agents/skills`: you read that folder, and Claude Code here reads it through `~/.claude/skills`. `hermes-setup` installs the skills of the ai-maxxing package there, from a copy it keeps up to date in `~/.cache/ai-maxxing-skills`.

| ask | command |
|---|---|
| "which skills can you install?" | `hermes-setup catalog`: one line per skill, `installed`, `available` or `own`, `base` when it is in the default pack, and what it does |
| "install the default pack", "the base skills" | `hermes-setup add base` |
| "install every skill" | `hermes-setup add all` |

The default pack is the list in `~/.cache/ai-maxxing-skills/skills/setup-vps/hermes-pack`, with why each skill is in it.
| "install connect-tool", "add the landing skill" | `hermes-setup add <skill> [<skill>...]` |
| "update your skills" | `hermes-setup update`: every skill it installed, from the latest package |
| "remove stripe-checkout" | `hermes-setup remove <skill>`: moved to `~/.cache/removed-skills`, recoverable |

1. Match the owner's words to names in `hermes-setup catalog` ("my landing page skill" is `create-landing`). If two could fit, name both in one line and ask which.
2. Run `hermes-setup add` with the names. Never restart the chat service for it: new skills load on their own in the next conversation. Tell the owner in one line what you installed and what each one lets them ask, and that it is ready from their next conversation (`/new`). If they want it right now, read its `~/.agents/skills/<name>/SKILL.md` and follow it.
3. When the owner asks for a job you have no skill for and the catalog has one (connect a tool, build a landing page), say which skill does it and install it after their yes.

`own` means the owner has their own skill under that name: `add` and `update` never replace it and `remove` never deletes it. Skills that only run on the owner's computer (`connect-vps`, `setup-*`, `dev-browser`, `install-skills`) are not in the catalog: tell the owner to run them from Claude Code on their computer. The personal dashboard is the exception: you do it yourself with `create-dashboard`. Never install a skill from another source unless the owner gives you its link and says to.
