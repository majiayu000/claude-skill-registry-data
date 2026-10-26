---
name: serena
description: "Semantic code navigation and precise symbol-level edits via Serena LSP (40+ languages): find symbols, references, callers/callees, rename/move across files. Use for refactors and blast-radius analysis when grep is too blunt. Serena runs as an independent tool (GPL-3.0)."
---
<!--
JARVIS skill: semantic code intelligence via Serena (oraios/serena, GPL-3.0).
Serena is used as an INDEPENDENT TOOL — its code is not copied into any MIT repo.
Binary: ~/workspace/.venv-tools/bin/serena
-->

# Serena — Semantic Code Toolkit

Serena exposes LSP-powered code intelligence over MCP (stdio) or CLI.
Use it as an external tool; never copy its code into MIT-licensed repos.

## Quick CLI usage

```bash
SERENA=~/workspace/.venv-tools/bin/serena
$SERENA --help
# Index a project, then query symbols/references via its MCP or CLI surface
```

## Typical agent flows

1. **Blast-radius before a change**: find the symbol, list references and
   callers, then decide the edit scope. (Complements `codegraph`'s static
   graph with live LSP accuracy.)
2. **Precise refactor**: rename/move a symbol across files via LSP instead of
   sed/grep, then run the project's typecheck/tests.
3. **Onboarding**: ask for the definition/call sites of an unfamiliar symbol
   rather than reading whole files.

## Rules

1. Serena is GPL-3.0: run it, don't vendor it. Findings (facts about code)
   are fine to use; its source stays out of MIT repos.
2. Prefer Serena over grep when the question is about symbols (definitions,
   references, renames). Prefer grep/ast-grep for plain text searches.
3. After any Serena-assisted refactor, run the repo's own verification
   (typecheck, tests) — LSP edits are precise, not infallible.
