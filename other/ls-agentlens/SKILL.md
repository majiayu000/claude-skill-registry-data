---
name: ls-agentlens
description: Navigate and understand codebases using agentlens hierarchical documentation. Use when exploring new projects, finding modules, locating symbols in large files, finding TODOs/warnings, or understanding code structure.
metadata:
  version: "1.0"
compatibility: "Requires an existing .agentlens/ tree in the target repo. LocalSetup does not ship an AgentLens generator or agentlens command."
---

# AgentLens - Codebase Navigation

## Before Working on Any Codebase
Always start by reading `.agentlens/INDEX.md` for the project map. If the target repo has no `.agentlens/` directory, this skill is advisory only; fall back to normal repository discovery.

## Generation Requirement

This skill consumes AgentLens documentation but does not generate it. LocalSetup does not include an `agentlens` CLI, script, or wrapper for regenerating `.agentlens/` output.

- If the target repo already documents an AgentLens generation command, run that project-provided command from the target repo root.
- If an external `agentlens` command is installed in the environment, use the command and flags documented by that external tool.
- If no generator is available, treat `.agentlens/` as read-only navigation context and verify stale-looking claims against source files.

Do not assume `agentlens` is available from this repository or from `PATH`.

## Navigation Hierarchy

| Level | File | Purpose |
|-------|------|---------|
| L0 | `INDEX.md` | Project overview and module routing |
| L1 | `modules/{slug}/MODULE.md` | Module details, file list |
| L1 | `modules/{slug}/outline.md` | Symbols in large files, when generated |
| L1 | `modules/{slug}/memory.md` | Warnings and TODOs, when generated |
| L1 | `modules/{slug}/imports.md` | File dependencies, when generated |
| L2 | `files/{slug}.md` | Deep docs for complex files, when generated |

This is the public output hierarchy documented by the current [upstream AgentLens README](https://github.com/nguyenphutrong/agentlens/blob/e28f9395af4aba1ccb3cf2820bbf0234bd60c360/README.md#L30-L40). Do not infer additional filenames from older package guidance.

## Navigation Flow

```
INDEX.md -> Find module -> MODULE.md -> available sidecars -> Source file
```

## When To Read What

| You Need | Read This |
|----------|-----------|
| Project overview | `.agentlens/INDEX.md` |
| Find a module | INDEX.md, search module name |
| Understand a module | `modules/{slug}/MODULE.md` |
| Find function/class in large file | `modules/{slug}/outline.md` if present; otherwise search source |
| Find TODOs and warnings | `modules/{slug}/memory.md` if present; otherwise search source markers |
| Understand file dependencies | `modules/{slug}/imports.md` if present; otherwise inspect source imports |

## Best Practices

1. **Start with the generated map** for large codebases, then use `outline.md` when present to target source reads
2. **Check `memory.md` when present** before modifying code; otherwise search source markers for warnings and TODOs
3. **Use `outline.md` when present to locate symbols**; otherwise search source, then read only the needed sections
4. **Verify generated claims against source** before editing; source remains authoritative when documentation is absent or stale
5. **Regenerate only through a documented command** supplied by the target repo or an external AgentLens installation

## Sidecars and Provenance

An optional `_meta.json` sidecar may appear beside imported skill content in some framework workflows. For `ls-agentlens`, that file is provenance only: it is not read by this skill, not required for activation, and not a substitute for the frontmatter above. If present, preserve it during source review unless a packaging or release audit explicitly classifies it as generated/private state.

For detailed navigation patterns, see [references/navigation.md](references/navigation.md)
For structure explanation, see [references/structure.md](references/structure.md)
