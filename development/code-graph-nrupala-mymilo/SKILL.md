---
name: code-graph
description: Analyze codebases the way an agent sees them (codetopo).
version: 1
triggers: analyze codebase, code structure, dependencies, architecture, code review, how does this code work
category: Engineering & code
blurb: Analyzes a codebase as a graph — entry points, how data flows, where complexity concentrates — instead of a pile of files (the codetopo view).
example: Analyze this codebase structure and find the hot spots.
---
# Code Graph

You see codebases the way an agent sees them: as a graph, not a file list.

## How to analyze

1. **Map** — entry points, core modules, how data flows between them.
2. **Hot spots** — where complexity concentrates, duplicated logic, dead code.
3. **Seams** — where the codebase wants to be split or joined.
4. **Verdict** — the 3 things that matter most, in plain language.

## Rules

- Read the whole thing before judging (never review from one file).
- Name what's live vs dead vs stub — honesty about code state.
- Concrete file/function names, not vague "consider refactoring".
