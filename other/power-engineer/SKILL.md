---
name: power-engineer
description: >
  Use when setting up or starting a project and you want to install the optimal
  skill stack for it. Triggers on phrases like: "set up skills for this project",
  "install project skills", "what skills should I use", "power engineer setup",
  "configure my skill stack", "power engineer frontend", "power engineer status",
  or any request to set up Claude Code skills for a new or existing project.
  Also triggers on targeted requests like "power engineer backend",
  "power engineer devops", "power engineer ai", "power engineer data",
  "power engineer docs", "power engineer mobile", "power engineer quick",
  "power engineer catalog", "power engineer update", "power engineer configure",
  "power engineer drift". Even if the user just says "/power-engineer frontend"
  or similar shorthand, this skill handles it.
---

# Power Engineer

You are an intelligent project setup system. You scan codebases, conduct
adaptive interviews, install skills directly, and configure projects.

**Important:** This skill uses progressive disclosure. Read ONLY the files
needed for the current route. Never read all files upfront.

**Important:** All user-facing questions MUST use the `AskUserQuestion` tool.
Never ask questions as plain text in a response. This applies to interview
questions, confirmations, and any point where you need user input.

**Important:** When generating CLAUDE.md, include a behavioral rule that
enforces `AskUserQuestion` usage across ALL installed skills — not just
Power Engineer. Every skill that needs user input must use `AskUserQuestion`
for a seamless, consistent experience.

## Route the request

Check the user's message and follow the matching route:

| User says (examples)                     | What to do                                                |
| ---------------------------------------- | --------------------------------------------------------- |
| "power engineer status"                  | Read `references/flows/status.md`                         |
| "power engineer update"                  | Read `references/flows/update.md`                         |
| "power engineer drift"                   | Read `references/flows/update.md`                         |
| "power engineer catalog"                 | Read `references/flows/catalog-browse.md`                 |
| "power engineer help"                   | Read `references/flows/help.md`                           |
| "power engineer info <skill>"            | Read `references/flows/info.md`                           |
| "power engineer uninstall <skill>"       | Read `references/flows/uninstall.md`                      |
| "power engineer configure"             | Read `references/flows/configure.md`                      |
| "power engineer save-phase"            | Read `references/flows/save-phase.md`                     |
| "power engineer frontend"               | Read `references/flows/frontend.md`                       |
| "power engineer backend"                | Read `references/flows/backend.md`                        |
| "power engineer devops"                 | Read `references/flows/devops.md`                         |
| "power engineer ai"                     | Read `references/flows/ai.md`                             |
| "power engineer data"                   | Read `references/flows/data.md`                           |
| "power engineer docs"                   | Read `references/flows/docs.md`                           |
| "power engineer mobile"                 | Read `references/flows/mobile.md`                         |
| "power engineer quick"                  | Read `references/flows/quick.md`                          |
| anything else (or just "power engineer") | Read `references/flows/full-interview.md`                 |

After routing, follow the instructions in that file completely.
