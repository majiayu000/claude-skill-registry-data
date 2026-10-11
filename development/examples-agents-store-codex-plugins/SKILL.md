---
name: examples
description: Use this skill when the user wants a worked, end-to-end scenario for a Microsoft Teams app on Teams SDK 2.1 — a full walkthrough for an echo bot, an AI quote agent, an Adaptive Card form, a message-extension search command, or an SSO + Microsoft Graph bot. Triggers on "Teams bot example", "full example Teams", "end-to-end Teams scenario", "echo bot example", "Teams SSO example".
---

# Examples — end-to-end scenarios

Each scenario is complete: CLI commands, the files to create or edit, code that compiles against `@microsoft/teams.apps`, `.api` and `.cards` 2.1, the registration steps, and a verification block. Pick the closest match and adapt.

| Scenario | What it demonstrates | File |
|---|---|---|
| Echo bot | Scaffold, register, tunnel, test in the Agents Playground and in Teams | `references/scenarios/echo-bot.md` |
| AI quote agent | `openai` + `runTools` with streaming in 1:1 and history in turn state | `references/scenarios/ai-quote-agent.md` |
| Adaptive Card form | A card with inputs, `SubmitData` routing and a `card.action.<action>` handler | `references/scenarios/adaptive-card-form.md` |
| Message-extension search | `message.ext.query` with preview cards and the manifest command | `references/scenarios/message-extension-search.md` |
| SSO + Graph bot | An Azure bot, `addOAuthFlow`, and calendar events through a Graph client | `references/scenarios/sso-graph-bot.md` |

## How to use a scenario

1. Read it top to bottom once.
2. Prerequisites for all of them: Node 22.12 or newer, `npm install -g @microsoft/teams.cli`, `teams login`, a tenant that allows custom apps (`teams status` tells).
3. Scaffold with the listed `teams project new typescript …` command, or apply the diffs to an existing project.
4. Run `npm run dev`, test in the Agents Playground (`agents-playground`), then register and test in Teams as the scenario says.
5. Cross-links go to the deep-dive skills: `messaging`, `adaptive-cards`, `message-extensions`, `ai-agents`, `authentication`, `graph-integration`.

The official guide `teams-sdk-teams-dev` covers the same registration steps (bot, credentials, tunnel, SSO) in more detail; the scenarios link to it instead of repeating it.