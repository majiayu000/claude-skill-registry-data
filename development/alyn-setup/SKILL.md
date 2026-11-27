---
name: alyn-setup
description: Sets up a complete skill stack for the user's kind of work with one of Alyn's curated bundles (design, engineering, startup founder, writing, SEO and GEO, marketing, office documents, video, token saving). Use when the user asks which skills to install, wants to set up Claude Code, Cursor or Codex for a role, says "set me up for design" or similar, or is new to agent skills.
license: MIT
---

# Alyn setup

Installs a curated set of skills that work well together, so the user does not have to pick them one by one. Each bundle is maintained by [Alyn](https://alyn.dev/bundles) and installs with one command.

## Bundles

| Bundle | For | Install |
| --- | --- | --- |
| Design setup | Designers, frontend developers, indie hackers. Taste, polish and no AI slop in UIs. | `npx alyn-cli add bundle:design` |
| Engineering workflow | Software engineers. Brainstorm, plan, test first, debug, review, ship. | `npx alyn-cli add bundle:engineering` |
| Startup founder setup | Founders. Idea to PRD to launch, with a CEO-style review. | `npx alyn-cli add bundle:founder` |
| Human writing | Anyone writing with AI. Text that does not read like a chatbot. | `npx alyn-cli add bundle:writer` |
| SEO and GEO | Marketers and site owners. Rank on Google and get cited by AI answers. | `npx alyn-cli add bundle:seo-geo` |
| Marketing team | Marketers. CRO, copy, launches, emails and ads. | `npx alyn-cli add bundle:marketing` |
| Office documents | Everyone. Real PDF, Word, Excel and PowerPoint files. | `npx alyn-cli add bundle:documents` |
| Video studio | Creators. Launch videos, explainers and captions. | `npx alyn-cli add bundle:video` |
| Token saver | Heavy users. Shorter answers, fewer tokens. | `npx alyn-cli add bundle:lean` |

The current list with every skill in each bundle: https://alyn.dev/bundles

## Steps

1. If the user did not say what they work on, ask one question: "What do you mostly use your agent for?" Offer the bundle names as options.
2. Pick one bundle, two at most. Say in one line what it contains and why it fits.
3. Ask before installing. Then run the command. Add `-a <agent>` if the user named an agent and `-g` to install for every project. The agent ids and folders are in [references/agents.md](references/agents.md).
4. Tell the user the skills are active in the next agent session.

If the Alyn MCP tools are connected, `get_bundle` returns the exact skills of a bundle and works without a shell.
