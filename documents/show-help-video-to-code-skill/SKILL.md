---
name: show-help-video-to-code-skill
description: Displays the full README.md for this plugin. Use when the user wants help, documentation, installation steps, usage examples, parameters, outputs, or troubleshooting for video-to-code-skill.
license: MIT
compatibility: Requires access to `${CLAUDE_PLUGIN_ROOT}/README.md`.
disable-model-invocation: true
metadata:
  author: Piotr Lason
  version: "1.3"
---

# Show plugin help

Displays the full `README.md` for `video-to-code-skill`.

## Instructions

**Display this banner as the very first output when the skill is invoked:**

```
 ██╗   ██╗██╗██████╗ ███████╗ ██████╗
 ██║   ██║██║██╔══██╗██╔════╝██╔═══██╗
 ██║   ██║██║██║  ██║█████╗  ██║   ██║
 ╚██╗ ██╔╝██║██║  ██║██╔══╝  ██║   ██║
  ╚████╔╝ ██║██████╔╝███████╗╚██████╔╝
   ╚═══╝  ╚═╝╚═════╝ ╚══════╝ ╚═════╝
████████╗ ██████╗      ██████╗  ██████╗ ██████╗ ███████╗
╚══██╔══╝██╔═══██╗    ██╔════╝ ██╔═══██╗██╔══██╗██╔════╝
   ██║   ██║   ██║    ██║      ██║   ██║██║  ██║█████╗
   ██║   ██║   ██║    ██║      ██║   ██║██║  ██║██╔══╝
   ██║   ╚██████╔╝    ╚██████╗ ╚██████╔╝██████╔╝███████╗
   ╚═╝    ╚═════╝      ╚═════╝  ╚═════╝╚═════╝ ╚══════╝
   SKILL HELP v1.3
```

1. **Notify the user**:
   - Tell them "Displaying video-to-code-skill help from `${CLAUDE_PLUGIN_ROOT}/README.md`..."

2. **Read the README**:
   - Read `${CLAUDE_PLUGIN_ROOT}/README.md`

3. **Display the README content as Markdown**:
   - Output the README content directly to the user as Markdown so it renders naturally in the CLI and in the VS Code Claude Code extension.
   - Preserve headings, paragraphs, bullet lists, numbered lists, tables, inline code, and fenced code blocks from the source file.
   - Do **not** wrap the entire README in one outer fenced code block.
   - Do **not** paraphrase, summarize, or omit sections unless the user explicitly asks for a shorter version.

4. **If the README cannot be read**:
   - Tell the user: "Could not read `${CLAUDE_PLUGIN_ROOT}/README.md`"
   - Also tell them to run `/video-to-code-skill -> setup-video-to-code-skill` or reinstall the plugin if the bundle looks incomplete.
