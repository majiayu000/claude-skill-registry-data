---
name: prompt-converter
description: 'Convert between Claude Code command markdown files (*.md) and GitHub Copilot prompt files (*.prompt.md). Use when porting custom prompts or CLI commands between ecosystems.'
---

# Prompt Converter

This skill automates the bidirectional conversion between Claude Code `.md` command files and Copilot `.prompt.md` files, ensuring metadata and instructions are correctly mapped.

## Environment Detection

Before executing any operations, the skill defines the `skills_source` path:

```python
import os
skills_source = os.path.expanduser('~/.copilot/skills') if os.name == 'nt' else os.path.expanduser('~/.copilot/skills')
```

## Workflow

1.  **Analyze Source**: Read the source file (Claude `.md` or Copilot `.prompt.md`) to extract metadata (name, description, agent, tools) and instruction content.
2.  **Map Metadata**:
    *   **Claude to Copilot**: Convert frontmatter keys, ensuring `name`, `description`, and `agent` (default: 'agent') are present.
    *   **Copilot to Claude**: Convert frontmatter to Claude's expected format (often simpler description/tools).
3.  **Transform Content**:
    *   Adjust template variables (e.g., `\$ARGUMENTS` in Copilot).
    *   Ensure markdown structures are preserved.
4.  **Execute Conversion**: Use the provided script to perform the transformation.
    ```bash
    python {skills_source}/prompt-converter/scripts/convert_prompt.py --src "my-command.md" --to copilot
    ```
5.  **Verify**: Confirm the new file exists in the target directory (e.g., `prompts/` for Copilot).

## Principles

*   **Metadata Integrity**: Preserve as much context as possible during mapping.
*   **Target Specifics**: Use `${input:...}` for Copilot parameters and `$ARGUMENTS` for CLI inputs where appropriate.
*   **Idempotency**: Converting back and forth should result in minimal structural drift.

## Usage

### Convert Claude to Copilot
```bash
python scripts/convert_prompt.py --src path/to/claude.md --to copilot -o ./prompts
```

### Convert Copilot to Claude
```bash
python scripts/convert_prompt.py --src path/to/copilot.prompt.md --to claude -o ./claude-commands
```

## Resources

### scripts/
*   `convert_prompt.py`: Core logic for conversion.

### templates/
*   `copilot.prompt.md.template`: Boilerplate for Copilot prompts.
*   `claude.md.template`: Boilerplate for Claude commands.
