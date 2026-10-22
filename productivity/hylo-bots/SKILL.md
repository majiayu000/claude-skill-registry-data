---
name: hylo-bots
description: "Builds, changes, undoes and deletes the user's automations: bots (prompt, skills, folder) and triggers that run on a schedule or on vault events, on any bot including the main one. Use when they want something done regularly or automatically ('every morning send me…', 'when I save a clip…', '每天早上帮我…'), accept an automation you proposed, or want one changed, stopped or undone ('fewer news items', 'delete that bot', '新闻别发那么多了'). Not for one-off tasks done now."
---

# Hylo Bots — Router

## Tools

The tools named here are Hylo's MCP tools (server `hylo`); your client may show them prefixed, e.g. `mcp__hylo__bot_list`. If they are not in your tool list, search your deferred tools for "hylo". If they are still missing, tell the user bot management needs them and stop.

| Area     | Tools                                                                       |
| -------- | --------------------------------------------------------------------------- |
| Overview | `capabilities`: every bot with its skills and triggers, the catalog, events |
| Bots     | `bot_list`, `bot_get`, `bot_create`, `bot_update`, `bot_delete`             |
| Triggers | `trigger_add`, `trigger_update`, `trigger_delete`, `trigger_run`            |
| Skills   | `skills_list`, `skills_catalog`, `skills_add`, `skills_enable`, `skills_disable`, `skills_remove` |

---

## Workflows

| Intent                                           | Workflow             |
| ------------------------------------------------ | -------------------- |
| Make a new bot                                   | @workflows/create.md |
| Add an automation to the main bot or another bot | @workflows/update.md |
| Change a bot's name, prompt, skills or triggers  | @workflows/update.md |
| Remove a bot                                     | @workflows/delete.md |
| Undo a change, from a receipt or in their words  | @workflows/undo.md   |

Load the matching workflow. If the intent is unclear, ask with `choices` which they mean. If the user wants something that is none of these, say it isn't covered yet and stop.

Shared references, loaded by the workflows that name them:

- `references/system-prompt.md`: how to write a bot's system prompt.
- `references/cards.md`: the plan and receipt cards every workflow shows.
- `references/skills.md`: when a job needs a skill, and finding and adding one.
- `references/triggers.md`: schedule syntax, events, path filters and prompt placeholders.

---

## Rules for every workflow

- **The main bot keeps its identity.** It is the one in `bot_list` that `bot_get` marks `main`. Its triggers and skills can be added, changed and removed like any bot's, and a new automation goes there unless it belongs with an existing bot or needs rules of its own. Never rename it, change its system prompt, turn it off or delete it; if the user means that, say it is managed in Settings.
- **Ids come from the tools.** Resolve a bot by name with `bot_list`, then `bot_get` for its triggers. If two bots match, ask which with `choices`. Never guess an id.
- **Decide, then show.** Fill in what's open with a sensible default and let the plan card show it; they change it from there. Ask first only what you can't infer: free text for what only they know (what the bot is for), `choices` with your recommendation first for the rest. One question at a time; don't re-ask what they already said.
- **Confirm before writing.** Before the first call that changes anything, show the plan as a `proposal` card (`references/cards.md`). Deleting needs this even if the user just said "delete it". If they pick a bot of its own, switch to the create workflow; if they pick running it once first, build it, then `trigger_run` each new scheduled trigger.
- **Report with a receipt.** After the calls, end with a `receipt` card (`references/cards.md`) listing everything made, so it can be undone. If a call failed, say so in it; don't retry blindly.
- Reply in the user's language. Bot names, descriptions and system prompts are written in it too, unless the user chose otherwise.
