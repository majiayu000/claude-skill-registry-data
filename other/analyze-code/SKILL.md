---
name: analyze-code
description: Use when asked to analyze a file, a directory, or the whole codebase to understand structure, architecture, dependencies, complexity, duplication, dead code, or technical debt — e.g. "analyze this", "análisis total", "explain this codebase", "mapa del código", "how does X work", "technical debt". Produces a complete, structured picture with verified commands, not guesses. Distinct from review-* skills (which judge quality); this skill explains and maps.
---

# Code / File Analysis

You build a complete, verified picture of code: what exists, how it is
structured, how pieces connect, where the complexity and debt live. You always
ground conclusions in actual file reads and command output — never from memory
of what a codebase "probably" looks like.

## Steps

1. **Inventory mechanically** — use Glob/Grep/Bash to map the scope before
   reading anything:
   - List all files: `rg --files <scope>` (or `ls -R`), grouped by type.
   - Count per type and per directory; note sizes with `wc -l` on the big
     files (`rg --files -g '*.go' | xargs wc -l | sort -n | tail`).
   - Note unusual names: `_test.go`, `_test.py`, minified bundles, lockfiles.
2. **Read in dependency order** — read entrypoints first (`main.go`, index
   files, workflow files), then what they call. Read imports/requires to learn
   the dependency graph. Do not read 200 files; read the ones that matter and
   sample the rest.
3. **Map the architecture** — produce:
   - Layers/components and their responsibilities.
   - Data flow: entrypoint -> handlers -> services -> storage/external.
   - Cross-cutting concerns: config, logging, error handling, auth.
   - Shared state and its accessors.
4. **Measure quality signals** (mechanical where possible):
   - Duplication — similar blocks across files (`rg` a distinctive line, or
     look for copy-pasted comments/handlers).
   - Dead code — exported/unused functions, orphaned files, unreachable
     branches (grep for references of suspect symbols).
   - Complexity — deeply nested functions, god-functions (>100 lines with
     many branches), switch/if chains that scream for a table or dispatch.
   - Coupling — files that import from many places, globals, magic strings.
   - TODOs/FIXMEs/hacks — `rg -n 'TODO|FIXME|HACK|XXX' <scope>`.
   - Stale artifacts — commented-out blocks, unused deps, obsolete config.
5. **Trace one real end-to-end path** — pick the core feature, follow it from
   trigger to result, and verify each step against the code. This is the
   difference between a map and a guess.
6. **Report** in the output format below.

## Output format

1. **Overview** — what the scope is, what it does, how big (files, lines).
2. **Architecture map** — components, layers, dependency graph (text/Mermaid
   on request), data flow.
3. **Verified facts** — each claim about the code with `file:line`.
4. **Quality findings** — duplication, dead code, complexity, coupling,
   debt — each with `file:line`, evidence, and severity (Low/Med/High).
5. **Answers** — the original question (how does X work, what happens on
   startup, where is state stored) answered directly and precisely.
6. **Commands run** — the exact inventory commands and their key output.
7. **Open questions** — what is ambiguous, unknown, or needs confirmation
   from the user or a runtime.

Rules: no hypotheticals — every structural claim cites `file:line`; when you
cannot verify something, say so explicitly rather than guessing.
