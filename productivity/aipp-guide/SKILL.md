---
name: aipp-guide
description: "Explain how to use the AIPP toolkit (this repo, also called aipp): installing it, linking it into a project, enabling skills and agents, choosing a workflow, understanding why a hook blocked something, and adding new skills, agents or hooks. Use when user says 'how do I use aipp', 'how does this toolkit work', 'how do I install aipp', 'enable a skill in this project', 'which workflow should I use', 'why did this hook block me', 'how do I add a skill to aipp', 'como usar o aipp', or 'como funciona este toolkit'. Do NOT use to pick the best skill for a specific task (use skill-advisor), to run a workflow itself, or for ai-memory, rag-rat, caveman or ponytail usage, which have their own skills."
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# AIPP Guide

AIPP is a catalog of skills, agents, commands, instructions and hooks that gets symlinked into each project's harness folder. This skill answers how to operate that toolkit. It routes by intent and loads only the reference needed.

## Steps

1. Match the request to one row below and read only that reference.
2. Before stating a command, flag or default as fact, confirm it in the source listed in the reference. The code is the truth: when a reference disagrees with the code, follow the code and tell the user the reference is stale.
3. Answer with the exact command and what it changes. Say so first when it changes files outside the project or the repo.
4. Answer only. Do not run install, clean or uninstall commands unless the user asks for that.

| The user wants to                                                                                 | Read                                               |
| ------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| Install, link a project, enable or disable items, use aliases, uninstall, fix a missing skill     | [references/setup.md](references/setup.md)         |
| Choose a workflow, know which agent or command to use, understand a blocked commit or tool call   | [references/workflows.md](references/workflows.md) |
| Add or change a skill, agent, instruction, hook or external tool, regenerate indexes, commit here | [references/extend.md](references/extend.md)       |

## Finding the toolkit

Paths in the references are relative to the toolkit root, which is `$AI_PROJECT_ROOT_DIR` (set by the installer in `~/.zshrc` and `~/.bashrc`). From another project, read `$AI_PROJECT_ROOT_DIR/<path>`. If the variable is empty, the bootstrap has not run: see the install section of `references/setup.md`.

## Hand off instead of answering

| Question                                         | Use                                                                      |
| ------------------------------------------------ | ------------------------------------------------------------------------ |
| Which skill fits this specific task              | `skill-advisor`                                                          |
| Which skills exist for a theme, enabled or not   | `skills-discovery`                                                       |
| How to find and call a tool behind mcp-manager   | `mcp-manager-instructions`                                               |
| How to write a hook script                       | `author-claude-hook`                                                     |
| How ai-memory, rag-rat, caveman or ponytail work | Their own skills (`ai-memory-*`, `rag-rat:*`, `caveman:*`, `ponytail:*`) |

The first four are disabled by default. If one is not available locally, fetch it with the skill-loader MCP tool `get_remote_skill(name)`, or enable it (see `references/setup.md`).

## Examples

User says: "Instalei o aipp mas a skill sd-planning não aparece neste projeto."
Actions: read `references/setup.md`, go to Troubleshooting, check the project's entry with `ats`.
Result: the cause and the exact command that fixes it.

User says: "Quero planejar uma feature, qual fluxo uso?"
Actions: read `references/workflows.md`, compare the full and lean paths for the size of the change.
Result: one recommended slash command, and the command that follows it.

User says: "My commit was rejected for mentioning a tool name."
Actions: read `references/workflows.md`, find the commit-msg gate.
Result: which check rejected it and how to reword the message. Never suggest `--no-verify` unless the user asks for it.
