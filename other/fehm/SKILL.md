---
name: fehm
description: Use FEHM's local code graph for focused source context, caller/callee relationships, architecture explanations, and change-review evidence in a developer's repository.
---

# FEHM repository evidence

Use the installed `fehm` CLI or the available FEHM MCP tools for the user's selected repository. Resolve the intended repository root from the workspace (use `git rev-parse --show-toplevel` when applicable); do not assume the assistant's launch directory is the project. Pass `--root "/absolute/project"` when working elsewhere.

Run `fehm doctor --root "/absolute/project" --json` to check the installation and saved graph. Missing, corrupt or stale state needs `fehm scan --root "/absolute/project"`; this writes local `.fehm/` state and does not execute project code. Follow the host's normal permissions. If scanning is unavailable, report the limitation and use ordinary source tools.

For a question, begin with a focused packet:

```sh
fehm context "authentication flow" --root "/absolute/project" --budget 4000 --json
fehm relationships "authenticateUser" --root "/absolute/project" --json
fehm flow "authenticateUser" --root "/absolute/project" --depth 2 --json
```

Use `fehm architecture --json` for system structure, `fehm guardrails analyze --json` for working-tree impact, and `fehm health --json` for static engineering findings. Run from the intended root or pass `--root`. Only request the reports relevant to the user's task. For exact syntax and supported options use `fehm help`.

MCP is optional. `fehm_context`, `fehm_relationships`, `fehm_system_map` and `fehm_practices` expose bounded local evidence when configured. MCP requires a fresh saved graph and reports when a scan is needed; it does not silently refresh or execute checks.

Cite returned source paths and line locations. Distinguish directly extracted relationships from heuristic/inferred ones and unknown links. Static edges do not prove runtime behavior, tests passing or a vulnerability. Token budgets are estimates. After edits, refresh the graph before relying on saved MCP results. When a symbol is ambiguous, resolve the specific file or identifier rather than inventing a match.

Use normal repository search, source inspection and targeted tests when FEHM cannot answer. Report unsupported language coverage, incomplete relationships and missing evidence. Test execution, external models and network-dependent advisory checks are separate actions requiring the host's normal authorization. Skill installation grants none of those permissions.
