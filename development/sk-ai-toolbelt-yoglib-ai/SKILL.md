---
name: sk-ai-toolbelt
description: Pointer to external AI tools and MCPs. Use when the user asks about the toolbelt, which tools are used, or how to install a recommended tool. This skill does not install tools.
---

# AI Toolbelt

External skills and MCPs used alongside this workflow. They are not installed by this repo; point the user to the upstream URL and tell them to install/enable it themselves.

## Skills

| Skill         | Use when                                 | Trigger                       | Upstream                                                                                                    |
| ------------- | ---------------------------------------- | ----------------------------- | ----------------------------------------------------------------------------------------------------------- |
| ponytail      | Laziest/minimal solution that works      | `/ponytail`                   | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)                                       |
| caveman       | Terse, caveman-style output              | `/caveman <level>`            | [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman)                                           |
| grilling      | Stress-test a plan or implementation     | `/grill ...`                  | [mattpocock/grilling](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) |
| rtk           | Save tokens on dev operations            | `rtk <cmd>`                   | [rtk-ai/rtk](https://github.com/rtk-ai/rtk)                                                                 |
| documentation | Write clear, maintainable technical docs | Use the `documentation` skill | [skills.sh/documentation](https://www.skills.sh/anthropics/knowledge-work-plugins/documentation)            |
| humanizer     | Remove signs of AI-generated writing     | Use the `humanizer` skill     | [skills.sh/humanizer](https://www.skills.sh/softaworks/agent-toolkit/humanizer)                             |

## CLIs

| CLI      | Use when                                                            | Trigger                                 | Upstream                                                  |
| -------- | ------------------------------------------------------------------- | --------------------------------------- | --------------------------------------------------------- |
| ripwire  | Symbol-level navigation: orientation, callers, blast radius, usages | `ripwire <dir> --for="..."`             | [redhat-et/ripwire](https://github.com/redhat-et/ripwire) |
| ast-grep | Structural search: declarations, AST patterns, multi-site rewrites  | `ast-grep --lang <lang> -p '<pattern>'` | [ast-grep.github.io](https://ast-grep.github.io)          |

## MCPs

| MCP                 | Use when                                    | Key tools                                    | Upstream                                                                                                         |
| ------------------- | ------------------------------------------- | -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| context7            | Up-to-date library docs or code examples    | `resolve-library-id`, `get-library-docs`     | [context7.com](https://context7.com/)                                                                            |
| serena              | Code-aware edits, search, symbol refactors  | `replace_content`, `search_for_pattern`, ... | [oraios/serena](https://github.com/oraios/serena)                                                                |
| grep                | Real-world code examples from public GitHub | `searchGitHub`                               | [mcp.grep.app](https://mcp.grep.app)                                                                             |
| sequential-thinking | Reflective, multi-step reasoning            | `sequentialthinking`                         | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) |

When asked about a tool: name it, give its trigger, and link upstream. Do not inline its rules or install it.
