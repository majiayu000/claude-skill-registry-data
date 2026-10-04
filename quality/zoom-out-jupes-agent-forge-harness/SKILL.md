---
name: zoom-out
description: Produce a higher-level architecture and context map for unfamiliar code. Use when you need to understand how a file, module, feature, or issue fits into the bigger picture, including relevant modules, callers, callees, dependencies, and next context.
---

# zoom-out

Use this skill when the user asks you to zoom out, says they do not know an area of code well, or needs a broader map before changing code.

## Goal

Go up one layer of abstraction. Explain how the relevant code fits together before recommending implementation details.

## Process

### 1) Anchor the question

Identify the smallest useful focus:

- The file, symbol, feature, route, command, workflow, or Beads issue the user is asking about.
- The user-facing behavior or agent workflow it supports.
- Any alignment document, interface contract, or `bd show <id>` output that defines the current task.

If the focus is unclear, ask one targeted clarifying question before exploring broadly.

### 2) Load knowledge first

Read the relevant harness knowledge before source code:

- `knowledge/_shared.yaml`
- `knowledge/repos/<repo>.yaml` for sub-repo work, when present
- Nearby plans, protocols, workflows, or skill docs that already describe the area

Use the knowledge files to name likely modules and boundaries, then verify those claims in source.

### 3) Map the code surface

Find the important pieces around the focus:

- Entrypoints: commands, routes, scripts, hooks, workflows, components, or public exports.
- Core modules: domain logic, shared types, parsers, adapters, persistence, or UI surfaces.
- Callers: files or commands that invoke the focus.
- Callees and dependencies: modules the focus imports, shells out to, reads from, writes to, or expects as data contracts.
- Tests and fixtures: behavior examples that show intended use.

Prefer exact searches for symbols, imports, filenames, and route names. Expand outward only until the caller/callee map explains the behavior.

### 4) Trace the flow

Summarize the path through the system:

- What starts the flow.
- What data or control decisions move through each module.
- Which side effects occur, such as filesystem writes, Beads updates, network calls, git operations, or UI state changes.
- Where errors, validation, or quality gates happen.
- What depends on this behavior staying stable.

### 5) Report the context map

Keep the response concise and actionable. Use this shape:

```md
## Zoomed-Out Map

<2-4 sentence overview of what this area does and why it exists.>

| Area | Files / Symbols | Role | Callers | Callees / Dependencies |
|------|-----------------|------|---------|------------------------|
| ... | `path` / `symbol` | ... | ... | ... |

## Flow

1. <entrypoint starts the behavior>
2. <core module transforms or validates>
3. <outputs, side effects, or UI/result>

## Boundaries And Risks

- <important invariant, ownership boundary, or coupling>
- <test or quality gate that protects it>

## Next Context

- <the next file, test, or decision to inspect if implementation continues>
```

Do not turn the zoom-out into a full implementation plan unless the user asks for one. The output should make the surrounding architecture legible enough for the next coding or review step.
