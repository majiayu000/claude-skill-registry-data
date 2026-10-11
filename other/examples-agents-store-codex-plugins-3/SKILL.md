---
name: examples
description: This skill should be used when the user asks "show me a complete grammY example", "give me a full grammY bot file", "example of a Telegram bot with menu", "complete echo bot in grammY", "example session counter", "example webhook bot Cloudflare Workers", "example conversation form bot", or wants end-to-end scenario walkthroughs rather than isolated snippets.
---

# grammY — Complete Examples

Index of end-to-end scenario walkthroughs. Each scenario lives in `references/scenarios/` and is a fully runnable file with imports, types, and entry point — copy/paste ready.

| Scenario | Goal | File |
|---|---|---|
| Echo bot | Smallest possible bot — long polling, replies to any message | `references/scenarios/echo-bot.md` |
| Menu + callbacks bot | Inline keyboard with state, edits message in place | `references/scenarios/menu-and-callbacks-bot.md` |
| Form conversation bot | Multi-step input wizard using `@grammyjs/conversations` | `references/scenarios/form-conversation-bot.md` |
| Session counter bot | Per-user persistent counter using `session` | `references/scenarios/session-counter-bot.md` |
| Webhook on Cloudflare Workers | Production deploy, no servers | `references/scenarios/webhook-on-cloudflare-workers.md` |

## When to use this skill vs others

| Want | Use |
|---|---|
| Smallest reproducible example for a feature | This skill — open the right scenario file |
| Reference for a specific method signature | `api-reference` |
| Idiomatic patterns explained | `sdk-patterns` / `filter-queries` / `sessions` / etc. |
| Plugin overview | `plugins-catalog` |
| Why something is broken | `troubleshoot` |

## Reading order if you're new to grammY

1. `references/scenarios/echo-bot.md` — get the dev loop running.
2. `references/scenarios/session-counter-bot.md` — add state.
3. `references/scenarios/menu-and-callbacks-bot.md` — add interaction.
4. `references/scenarios/form-conversation-bot.md` — multi-step flows.
5. `references/scenarios/webhook-on-cloudflare-workers.md` — production deploy.