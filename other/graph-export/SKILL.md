---
name: graph-export
description: '[Code Intelligence] Use when exporting the code knowledge graph. --format={json|mermaid}.'
disable-model-invocation: true
---

> Codex compatibility note:
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Host-native execution: Codex runs a skill by loading its `SKILL.md` instructions and executing the required steps with available tools. No separate `Skill` tool is required; a loaded skill is already activated.
> - Source vs execution: prefer the registered `.agents/skills/<name>/SKILL.md` for Codex execution. `.claude/**` remains the canonical authoring source; reading it for a registry or source inspection does not switch this session to Claude Code.
> - Capability check: interpret Claude tool names through the active host before declaring a blocker. Continue when Codex can perform the required operation; stop and ask only when the actual capability is unavailable, naming the step and evidence. Host-native execution is not a protocol deviation and needs no extra approval.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - Use ask user tool to ask user.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, steps follow the guided contract in `$start-workflow` (gate steps fixed; other steps may flex with a logged reason); report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.
## Quick Summary

**Goal:** [Code Intelligence] Export the code review knowledge graph. `--format=json` (default) dumps all nodes (functions, classes, files) and edges (calls, imports, inheritance) from graph.db for external analysis; `--format=mermaid` renders a single file's internal call graph as a Mermaid flowchart in markdown (folds former `/graph-export-mermaid`).

**Workflow:**

1. **Detect** — classify request scope and target artifacts.
2. **Execute** — apply required steps with evidence-backed actions.
3. **Verify** — confirm constraints, output quality, and completion evidence.

**Key Rules:**

- **Format flag** (see [Format Mode](#format-mode---format)): `--format=json` (default) = full graph → `.code-graph/graph-export.json` (CLI `export`); `--format=mermaid` = single-file diagram, requires `<path>` (CLI `export-mermaid`).
- MUST ATTENTION keep claims evidence-based (`file:line`) with confidence >80% to act.
- MUST ATTENTION keep task tracking updated as each step starts/completes.
- NEVER skip mandatory workflow or skill gates.

## Prerequisites

- Graph must be built first: run `$graph-code --mode=build` if `.code-graph/graph.db` doesn't exist
- Requires Python 3.10+ with tree-sitter, tree-sitter-language-pack, networkx

## Format Mode (`--format=`)

| `--format`       | CLI verb                                  | Output                                                      | Requires |
| ---------------- | ----------------------------------------- | ----------------------------------------------------------- | -------- |
| `json` (default) | `code_graph export --json`                | Full graph dump → `.code-graph/graph-export.json`           | —        |
| `mermaid`        | `code_graph export-mermaid <path> --json` | Single-file Mermaid diagram → `.code-graph/<name>-graph.md` | `<path>` |

`--format=json` dumps ALL nodes + edges from the whole graph. `--format=mermaid` renders ONE file's internal call graph as a Mermaid flowchart (folds former `/graph-export-mermaid`). Pick `--format` FIRST (default `json`), then run the matching branch below.

## Steps

### `--format=json` (default) — full graph → JSON

1. **Export graph** — Run via Bash:

    ```bash
    python .claude/scripts/code_graph export --json
    ```

    Default output: `.code-graph/graph-export.json`

2. **Export specific files only** (optional):

    ```bash
    python .claude/scripts/code_graph export --files {source-root}/auth {source-root}/api --json
    ```

    This exports only nodes and edges belonging to the specified files.

3. **Custom output path** (optional):

    ```bash
    python .claude/scripts/code_graph export -o custom-path.json --json
    ```

4. **Report results:** File path, node count, edge count, file size.

### `--format=mermaid` — single file → Mermaid diagram

1. **Export file graph as Mermaid** — Run via Bash (positional or `--file` flag both work):

    ```bash
    python .claude/scripts/code_graph export-mermaid <relative-path> --json
    # OR
    python .claude/scripts/code_graph export-mermaid --file <relative-path> --json
    ```

    Default output: `.code-graph/<path-based-unique-name>-graph.md` (e.g., `docs--project-config-graph.md`)

2. **Custom output path** (optional):

    ```bash
    python .claude/scripts/code_graph export-mermaid <relative-path> -o custom-path.md --json
    ```

3. **Report results:** File path, node count, edge count.

**Mermaid scope:** functions/classes/test functions within the file + internal call relationships (caller AND callee in-file); class membership via nested subgraphs; edge types calls/imports/inherits/implements/tests/depends. Excludes external/stdlib calls, cross-file callers, and CONTAINS edges (shown structurally). Implicit `MESSAGE_BUS` / `TRIGGERS_EVENT` / `API_ENDPOINT` edges render when present.

## Output Format

**`--format=json`:**

```json
{
  "version": "1.8.4-easyclaude",
  "stats": { "total_nodes": N, "total_edges": N, "files_count": N, "languages": [...] },
  "nodes": [
    { "kind": "Function", "name": "login", "qualified_name": "auth.py::login", "file_path": "...", "line_start": 10, "line_end": 25, "language": "python" }
  ],
  "edges": [
    { "kind": "CALLS", "source": "api.py::handler", "target": "auth.py::login", "file_path": "...", "line": 15 }
  ]
}
```

**`--format=mermaid`:** a markdown file containing a `flowchart TD` — functions/classes as nodes, calls/imports as labelled edges, class membership as nested subgraphs (e.g., `login -->|calls| validate`).

## Implicit Edges in Export

The exported JSON includes ALL edge types, including implicit connections:

- `MESSAGE_BUS` — cross-service bus message producer-to-consumer links
- `TRIGGERS_EVENT` — entity CRUD to event handler links
- `PRODUCES_EVENT` — event handler to bus producer links
- `TRIGGERS_COMMAND_EVENT` — command to command event handler links
- `API_ENDPOINT` — frontend HTTP call to backend route links

These edges are created by the implicit connector and API connector during `build`/`sync`.

## Use Cases

- Inspect graph contents for debugging
- Feed into external analysis tools
- Verify graph correctness after build
- Share graph snapshot with team members

---

# Export Graph

Export the complete knowledge graph from `.code-graph/graph.db` to a readable JSON file.

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Export the code review knowledge graph — `--format=json` dumps the full graph to JSON, `--format=mermaid` renders one file as a Mermaid flowchart.

**IMPORTANT MUST ATTENTION — Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**


- **MANDATORY IMPORTANT MUST ATTENTION** break work into small todo tasks using task tracking BEFORE starting
- **MANDATORY IMPORTANT MUST ATTENTION** search codebase for 3+ similar patterns before creating new code
- **MANDATORY IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim (confidence >80% to act)
- **MANDATORY IMPORTANT MUST ATTENTION** add a final review todo task to verify work quality

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using task tracking.
