---
name: documenting-architecture
description: >
  Generate architecture overview documentation from codebase analysis.
  Uses tree-sitter-analyzer for precise code structure extraction.
  Generates Mermaid diagrams for visual representation.
  Triggers: architecture overview, project structure, module diagram,
  dependency graph, code structure, directory structure.
allowed-tools: Read, Write, Grep, Glob, Bash, Task
---

# docs:architecture - Architecture Overview Generation

Auto-generate architecture documentation from codebase analysis.

## Generated Content

| Section | Description |
| --- | --- |
| Project Overview | Tech stack, framework detection |
| Directory Structure | tree command output |
| Module Composition | Mermaid relationship diagrams |
| Key Components | Classes, functions with statistics |
| Dependencies | External/internal visualization |
| Statistics | File count, line count, etc. |

## Processing Flow

| Phase | Actions |
| --- | --- |
| 1. Init | Identify root, detect language/framework |
| 2. Structure | tree command, classify directories |
| 3. Code | tree-sitter-analyzer: classes, functions, imports |
| 4. Dependencies | Parse imports, map relationships |
| 5. Generate | Mermaid diagrams, populate templates |

## Analysis Commands

```bash
# Directory structure
tree -L 3 -I 'node_modules|.git|dist|build|__pycache__|.venv' --dirsfirst

# Code structure (per file)
tree-sitter-analyzer {file} --structure --output-format json

# Dependencies - TypeScript/JavaScript
grep -r "^import\|^export" --include="*.ts" --include="*.tsx"

# Dependencies - Python
grep -r "^import\|^from.*import" --include="*.py"
```

## Error Handling

| Error | Resolution |
| --- | --- |
| Root not found | Use current directory |
| tree-sitter unavailable | Fallback to Grep/Read |
| Large project | Sample top 100 files |

## Markdown Validation

After generation, validate output with:

```bash
~/.claude/skills/scripts/validate-markdown.sh {output-file}
```

Non-blocking (warnings only) - style issues don't block document creation.

## References

- [@~/.claude/agents/analyzers/architecture-analyzer.md] - architecture-analyzer agent
- Command: `/docs:architecture`
