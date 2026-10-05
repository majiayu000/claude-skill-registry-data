---
name: mk:llms
description: Generate llms.txt files from project documentation following the llmstxt.org spec. Use when asked to create AI-friendly documentation indexes, generate llms.txt, or make a project discoverable by AI assistants.
argument-hint: '[path] [--full] [--output path] [--url base]'
source: local
original_path: .claude/skills/llms/SKILL.md
adapted_for: claude-code
keywords:
  - llms
  - llms-txt
  - llm-friendly-docs
  - ai-discoverability
  - agentic-content
when_to_use: Use when generating llms.txt or LLM-friendly documentation for AI consumers.
user-invocable: true
owner: docs
criticality: medium
status: active
runtime: claude-code
---

# llms.txt Generator

Generate [llms.txt](https://llmstxt.org/) files — LLM-friendly markdown indexes of project documentation.

> **Path convention:** Commands below assume cwd is `$CLAUDE_PROJECT_DIR` (project root). Prefix paths with `"$CLAUDE_PROJECT_DIR/"` when invoking from subdirectories.

## When to Use

- Project needs LLM-friendly documentation index
- User asks for "llms.txt", "LLM documentation", "AI-friendly docs"
- Publishing docs site and want AI discoverability
- After major documentation updates (Phase 6 Reflect)

Explicit: `/mk:llms [path] [--full]`

## Workflow Integration

Operates in **Phase 6 (Reflect)** or on-demand. Output supports the `documenter` agent.

## Arguments

| Flag            | Effect                                            |
| --------------- | ------------------------------------------------- |
| (no args)       | Scan `./docs` directory                           |
| `path`          | Scan specific directory                           |
| `--full`        | Also generate `llms-full.txt` with inline content |
| `--output path` | Custom output location (default: project root)    |
| `--url base`    | Base URL prefix for links                         |

## Scripts

**Script-first approach** — the Python script handles all deterministic work (scanning, extracting, categorizing, generating). Claude only reviews and improves the output.

```bash
# Generate llms.txt (script does the heavy lifting)
.claude/skills/.venv/bin/python3 .claude/skills/llms/scripts/generate-llms-txt.py \
  --source ./docs [--output .] [--base-url https://example.com/docs] [--full]

# Preview metadata first (Claude reviews before generating)
.claude/skills/.venv/bin/python3 .claude/skills/llms/scripts/generate-llms-txt.py \
  --source ./docs --json
```

## Process

1. **Run script** — execute `generate-llms-txt.py --source <path> --json` to preview metadata
2. **Review metadata** — check project name, description, file categorization
3. **Generate** — run script again without `--json` to produce llms.txt
4. **Review output** — read generated llms.txt, improve descriptions if needed
5. **Validate** — check: H1 present, blockquote summary, valid link format, Optional section last
6. If `--full`: review llms-full.txt for completeness

## Output Format

```markdown
# {Project Name}

> {Brief project description with essential context.}

## {Section Name}

- [{Doc Title}]({url}): {Brief description}
- [{Another Doc}]({url}): {What this covers}

## Optional

- [{Less Important Doc}]({url}): {Supplementary info}
```

## References

| Reference                                             | When to load        | Content                              |
| ----------------------------------------------------- | ------------------- | ------------------------------------ |
| **[llms-txt-spec.md](./references/llms-txt-spec.md)** | Step 4 — generating | Full llmstxt.org specification rules |

## Failure Handling

| Failure                  | Recovery                                  |
| ------------------------ | ----------------------------------------- |
| No .md files found       | Report "No documentation found in {path}" |
| No H1 in doc file        | Use filename as title, warn user          |
| Output path not writable | Suggest alternative path                  |

## Constraints

- Never fabricate documentation content — only index what exists
- Follow llmstxt.org spec strictly
- Keep descriptions concise — one sentence per entry

## Gotchas

- **Python venv required**: run `.claude/scripts/bin/setup-workflow` once from the project root before invoking this skill. Re-run after upgrading the toolkit.
