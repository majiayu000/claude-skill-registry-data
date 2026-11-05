---
name: codebase-hygiene-reviewer
version: 1.1.0
description: Evidence-based declutter audit — dead code, unused exports, duplication, oversized files/functions, modularization candidates; shared libraries with several consumers. Proposes, never edits. Use when cleaning up a repo or library, hunting dead code, or sizing a split.
---

# Codebase Hygiene Reviewer

Audits a repo (or a library and its consumers) for clutter and reports **evidence-backed findings** ranked by payoff. It **proposes; it does not edit.** Every finding cites a tool output or a consumer search, never a hunch. Commands and the report template live in [RECIPES.md](RECIPES.md).

## 1. When to invoke

- "Clean up this repo", "find dead code", "what can we delete", "this package is too big".
- Before a release of a shared library, to find API nobody uses.
- As the evidence-gathering pass ahead of [improve-codebase-architecture](../../refactoring/improve-codebase-architecture/SKILL.md).

Not for expression-level polish ([logic-cleaner](../../refactoring/logic-cleaner/SKILL.md)) or for executing a split ([code-design-refactor](../../refactoring/code-design-refactor/SKILL.md)).

## 2. Scope first

1. **Roots.** Audit tracked files only (`git ls-files`). Exclude generated code (sqlc output, `*.gen.ts`, `schema.d.ts`, `dist/`, vendored) from findings, and note the exclusion in the report.
2. **Consumers.** For a library, enumerate real consumers *before* calling anything dead. "This repo does not use it" is not "nobody uses it".
3. **Tests.** Decide per run whether tests count as roots. Default: yes — otherwise every test helper looks dead.

## 3. Keep the categories apart

| Category | Question | Fix class |
|---|---|---|
| Dead code | Is it unreachable from every root? | Delete |
| Unused export | Exported, but no known consumer uses it? | Unexport or deprecate (semver) |
| Duplication | Is the same logic or generated artefact repeated? | Extract or share |
| Size | File/function/package over threshold? | Candidate only |
| Modularization | Is there a real seam inside it? | Hand off |

Mixing them produces reports that recommend deleting public API.

## 4. Tools

Prefer the language's own graph over grep. Concrete commands per ecosystem in [RECIPES § 1](RECIPES.md#1-tool-matrix).

- **Go:** `deadcode -test` for reachability; `-filter` and `go list -deps` to measure per-consumer usage. `unused` only sees unexported symbols — see [go-architect § 14](../../languages/go-architect/SKILL.md#14-tooling).
- **TypeScript/React:** `knip` for unused files, exports and duplicate exports; `tsc --noEmit` as the health gate first. See [react-architect § 10](../../frameworks/react-architect/SKILL.md#10-testing).
- **Any:** `git ls-files`, `wc -l`, `md5sum` (byte-identical generated files across modules), `jscpd` for clones across modules and non-code files ([RECIPES § 5](RECIPES.md#5-cross-module-duplication-with-jscpd)).

## 5. False-positive rules

Verify every hit before it reaches the report.

- Static tools miss dynamic dispatch: reflection, `//go:linkname`, cobra `RunE`, Bubble Tea `Update`, handlers stored in maps, string-keyed registries, framework conventions (Next.js route files).
- Do not flag migration `Down`/`Status`/`Version` functions because no service calls them.
- Do not flag interface implementations that exist only to satisfy an interface.
- Never recommend hand-editing generated code; fix the generator input or exclude it.
- A removal can orphan the next symbol — re-run the tool after each deletion batch and say so in the report.

## 6. Size is a signal, not a target

Report LOC, files per package, files over ~400 lines, functions over ~60 lines, cognitive complexity. Then apply the seam test from [code-design-refactor](../../refactoring/code-design-refactor/SKILL.md): a split needs a conceptual seam, not a file count. In Go, many well-named files in one package is normal; in a TS feature folder one component per file with a thin barrel is the norm. A finding without a named seam is "monitor", not "split".

## 7. Output

One report per run, written to the OS temp dir (`$TMPDIR` or `/tmp`) as `hygiene-report-<timestamp>.md`, not into the repo unless asked. Sections: repo table, dead code with evidence, unused exports with consumer search, duplication, split candidates with their seam, quick wins, **do not touch**, and a priority split of `now / later / won't do`. Template in [RECIPES § 6](RECIPES.md#6-report-template).

## 8. Guardrails

- Propose only. Deleting is a separate, user-approved step, one batch at a time, tests green between batches.
- Library API removals are semver-breaking: route them through deprecation, not deletion.
- Re-run the tools after changes and report the delta.

## 9. Cross-skill ties

- [code-design-refactor](../../refactoring/code-design-refactor/SKILL.md) — executes approved splits.
- [improve-codebase-architecture](../../refactoring/improve-codebase-architecture/SKILL.md) — consumes this report as exploration evidence.
- [logic-cleaner](../../refactoring/logic-cleaner/SKILL.md) — expression-level duplication inside a function.
- [go-architect](../../languages/go-architect/SKILL.md), [react-architect](../../frameworks/react-architect/SKILL.md) — language standards the findings are judged against.
- [performance-reviewer](../performance-reviewer/SKILL.md) — sibling reviewer; same "no finding without evidence" rule.
