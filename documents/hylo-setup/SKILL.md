---
name: hylo-setup
description: "Walks the user through setting up Hylo itself in chat, one step at a time, and picks up where they left off. Use only when told to run hylo-setup (the first chat after onboarding is), or when the user explicitly asks to set up, continue or redo the setup of Hylo, e.g. 'continue Hylo setup', 'run Hylo setup again', '继续 Hylo 设置', '重新运行 Hylo 设置'. Do not use for setting up anything else (a tool, project, bot or app), for one-off changes like adding a bot or trigger, or for questions about how Hylo works."
---

# Hylo Setup — Router

## Tools

The tools named here are Hylo's MCP tools (server `hylo`); your client may show them prefixed, e.g. `mcp__hylo__read`. If they are not in your tool list, search your deferred tools for "hylo". If they are still missing, tell the user setup needs them and stop.

---

## Progress file

Progress lives in `/_setup/progress.md`, visible to the user:

```markdown
---
started: <YYYY-MM-DD>
language: <BCP 47 tag, once confirmed>
completed: <YYYY-MM-DD, once wrap-up is done>
---
- [x] intro — [[Getting started with Hylo]]
- [x] language — zh-Hans
- [x] about-you — product designer, into AI tools
- [ ] news-bot
- [ ] compile
- [ ] channels
- [ ] wrap-up
```

`[x]` done, `[-]` skipped (with the reason), `[ ]` pending. Keep each note after the dash to a few words.

Read it with `read {"path": "/_setup/progress.md"}`. If it doesn't exist, this is a first run: write it with every step below pending. Write it back with `create {"path": "/_setup/progress.md", "content": "<content>", "force": true}` each time a step ends.

---

## Steps, in order

| id          | Sub-skill            |
| ----------- | -------------------- |
| `intro`     | @steps/intro.md      |
| `language`  | @steps/language.md   |
| `about-you` | @steps/about-you.md  |
| `news-bot`  | @steps/news-bot.md   |
| `compile`   | @steps/compile.md    |
| `channels`  | @steps/channels.md   |
| `wrap-up`   | @steps/wrap-up.md    |

A progress file from an older version may miss a step or list one that's gone: add the missing ones as pending, drop the unknown ones.

---

## Running

1. Take the first step that's neither done nor skipped, and load its sub-skill.
2. If its condition doesn't hold, mark it skipped with the reason and go on to the next.
3. When a step ends, update the progress file, then go straight into the next step in the same reply. Don't ask whether to continue.
4. A step that asks the user something ends your turn with that question. Their answer finishes the step.
5. If they want to stop ("later", "skip the rest", "以后再说"), mark the remaining steps skipped, and tell them in one line they can say "continue Hylo setup" anytime.
6. If they ask something unrelated, help them, then come back in one line.
7. If setup is already complete, say so and offer to redo a step they name.

Speak in the progress file's `language` once it's set; before that, in the language you were told to use, or else the user's.

Keep replies short: setup should feel like a quick chat, not a form.
