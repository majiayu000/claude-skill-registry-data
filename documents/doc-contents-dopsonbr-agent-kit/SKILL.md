---
name: doc-contents
description: Generate project documentation including CONTENTS.md navigation files and AGENTS.md instructions. Use when creating documentation structure, project indexes, or AI agent configuration files.
license: MIT
metadata:
  author: agent-kit
  version: "1.0.0"
---

# Documentation Contents Generator

Generate CONTENTS.md and AGENTS.md files for project navigation and AI agent context.

## CONTENTS.md

A simple table listing files and directories with brief descriptions.

- **Format:** Table with Name and Description columns
- **Descriptions:** 1-2 sentences max
- **Nesting:** Place in any directory that benefits from an index

See [assets/contents-template.md](assets/contents-template.md) for the template.

## AGENTS.md

Context for AI coding agents (Claude Code, Cursor, Codex, etc.).

### Root AGENTS.md

Place at project root with:
- Build commands
- Code style conventions
- Testing approach
- Commit format
- Available skills

### Nested AGENTS.md

Place in subdirectories only when they have unique conventions not covered by the root file.

**Critical:** Never repeat instructions from parent files. Only include directory-specific guidance.

See [assets/agents-template.md](assets/agents-template.md) for the template.

## Generation Process

1. **Detect project type** - Parse package.json, pyproject.toml, go.mod, Cargo.toml, etc.
2. **Extract commands** - Build, test, lint, dev commands
3. **Infer conventions** - From existing code patterns
4. **Apply template** - Use the appropriate template

## Examples

### Generate CONTENTS.md

```
User: Create a CONTENTS.md for the src directory

Claude: [Scans src/, applies contents-template.md]

# src

| Name | Description |
|------|-------------|
| [index.ts](./index.ts) | Main entry point and exports. |
| [cli.ts](./cli.ts) | Command-line interface handler. |
| [utils/](./utils/) | Shared utility functions. |
```

### Generate AGENTS.md

```
User: Create an AGENTS.md for this project

Claude: [Detects Node.js from package.json, extracts scripts]

# AGENTS.md

CLI tool for managing project documentation.

## Build Commands

bun install
bun run build
bun test
```

## Validation

Validate that CONTENTS.md files include all files:

```bash
bun run scripts/validate-contents.ts [path]
```

Output (JSON):
```json
{
  "valid": false,
  "results": [
    {
      "contentsPath": "src/CONTENTS.md",
      "missing": ["newfile.ts"],
      "extra": ["deleted-file.ts"]
    }
  ]
}
```

- `missing`: Files in directory but not in CONTENTS.md
- `extra`: Links in CONTENTS.md that don't exist
