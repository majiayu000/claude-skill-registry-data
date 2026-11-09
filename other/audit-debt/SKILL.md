---
name: audit-debt
description: "Audits technical debt in a repository or directory: where complexity concentrates, which functions exceed structural thresholds, and where code is duplicated. Use when the operator asks for a tech-debt audit, a code-health audit or where to start cleaning up."
---

# Audit Debt

This skill audits the code health of a repository or a directory with the
act-lite MCP tools. It ranks the files where complexity concentrates, lists
the structural problems in those files, and shows the largest duplicated
code. It ends in a report and never edits a file.

## Adapt

An operator instruction wins over every default below: the scope, the number
of files to detail, whether tests are audited.

The tools are the `act-lite` MCP server's. The same results come from the
`act-lite analyze` command (`act-lite analyze hotspots …`), so a session
without the MCP server runs the commands instead.

## Inputs

- **`paths`:** the files or directories to audit, relative to the workspace
  root. Default: `[]`, the whole workspace.
- **`top`:** the number of hotspot files to detail, 1 to 1000. Default: 10.
- **`include_tests`:** `false`, unless the operator asks to audit tests too.
  Pass it to every call only then.

## Procedure

1. **Where to start.** Call `analyze_hotspots` with `paths` and `limit` =
   `top`. Its findings are the top files, highest score first.
   - If it returns no file (`findings` is `[]`), no analyzed file has a
     function: skip step 3, and say so in the report.

2. **Counts for the whole scope.** Call `analyze_patterns` with `paths` and
   `limit` = 0. Its `total` and `details.counts_by_rule` give the findings
   per rule in the whole scope; it returns no finding.

3. **Structural problems in the top files.** Call `analyze_patterns` with
   `paths` = the `file` of each step-1 finding and `limit` = 1000.
   - If the result has `truncated: true`, the report shows the first 1000
     findings and says how many of `total` are not shown.

4. **Largest duplicates.** Call `analyze_clones` with `paths` and `limit` =
   20. Its findings are the largest clone classes first.

4a. **Dependency cycles.** Call `analyze_cycles` with `paths` and `limit` =
   20. Its findings are the largest cycles first.

4b. **Most coupled files.** Call `analyze_coupling` with `paths` and `limit` =
   `top`. Its findings are the most connected files.

   - Pass `include_tests` to both calls only when the operator asks to audit
     tests too.

5. **Empty scope.** If a call returns the error that starts with `no files to
   analyze in the requested scope`, quote the message in the report's
   Coverage and limits section, and still run the other steps.

6. **Report.** Write the report below from the four results: their
   findings, `total`, `truncated`, `status`, `complete`, `coverage`,
   `excluded`, `incomplete` and `details`. Write nothing else, and change no
   file.

## Report

```
## Technical debt audit: <scope>
Summary: <analyzed_files> files analyzed; supported and unsupported languages; each call's status and completeness;
findings by rule (<counts_by_rule>); <total> clone classes.
### Where to start
| Rank | File | Score | Functions | Top function (complexity × lines) |
Ranking: <details.formula>.
### Structural problems in the top files
| Location | Function | Rule | Value | Threshold |
### Largest duplicates
- <kind> clone, <tokens> tokens, <members_total> members: …
### Dependency cycles
<total> cycles over <cyclic_files> files.
- <members_total> files, <edges_total> edges: <path as <file> → <to> → …>[ (path of <path_total> steps, <n> shown)]; members: <file>, …[ (members not all shown)]
### Most coupled files
| File | Fan-in | Fan-out | Instability | Unresolved |
Instability = fan_out / (fan_in + fan_out). Fan-in counts only files in <scope>.
### Coverage and limits
Unsupported languages and rules (<not_applicable>), exclusions, skipped files, parse failures, regions not analyzed (<file>:<range>: <reason>), truncation.
A clone class shows that code has the same syntax tree, apart from formatting, comments and, for renamed clones, identifier names and literal values. It does not show that the members behave the same, that they can share one function, or that extracting them is safe.
```

- **`<scope>`:** the `paths`, or "the workspace" for `[]`.
- **Summary:** `coverage.analyzed_files` of the hotspots result; the
  `coverage.languages` entries, supported and not; for each call, `status`
  and `complete`; `details.counts_by_rule` and `total` from step 2; the
  clones result's `total`.
- **Where to start:** one row per step-1 finding, in result order. Rank is
  1, 2, …; File, Score and Functions are `file`, `score` and `functions`;
  Top function is the first of `top_functions`: its `function` (or
  `(anonymous)` for `null`) at its `range`, with its `complexity` × `lines`.
  Then the `details.formula` line. With no file, write "No analyzed file has
  a function."
- **Structural problems:** one row per step-3 finding, in result order.
  Location is `<file>:<range>`; Function is `function`, or `(anonymous)`;
  Rule, Value and Threshold are `rule`, `value` and `threshold`. With no
  finding, write "None in the top files."
- **Largest duplicates:** one line per step-4 finding, in result order,
  with its `members` (each `<file>:<range>`); when `members_total` is more
  than the members listed, add "and <n> more". With no class, write "No
  clone class."
- **Coverage and limits:** the `coverage.languages` entries with
  `supported: false`; `details.not_applicable` of the patterns results; the
  `excluded.counts`; the `incomplete.skipped_files` and
  `incomplete.parse_failures`; the `details.regions_not_analyzed` entries
  of the `analyze_hotspots`, `analyze_patterns` and `analyze_clones` results,
  each entry (`file`, `range`, `reason`) once, and each
  `details.regions_not_analyzed_total` that is more than the entries listed;
  any empty-scope message from step 5; each truncation (`total` against what
  is shown); then the sentence above. A result with `complete: false` can
  miss findings in that evidence; say so. In component files (`.vue`,
  `.svelte`, `.astro`), only script regions are analyzed: the template and
  style regions are not, so no finding comes from them.
- **Dependency cycles:** `total` and `details.cyclic_files` of the step-4a
  result, then one line per finding, in result order: `members_total` and
  `edges_total`; the `path` steps, from the cycle's `file` back to it, written
  as `<file> → <to>` steps (the first step's `file`, then each step's `to`),
  with "(path of <path_total> steps, <n> shown)" when `path_total` is more
  than the <n> steps shown; and the `members`, listed separately, with
  "(members not all shown)" when `members_total` is more than the members
  listed. The `members` are sorted by path, not in traversal order: never
  write them as a path. With no cycle, write "No cycle."
- **Most coupled files:** one row per step-4b finding, in result order: File,
  Fan-in, Fan-out, Instability and Unresolved are `file`, `fan_in`, `fan_out`,
  `instability` and `unresolved`. Then the formula line and the fan-in scope
  line, word for word, with `<scope>` as in the heading. With no file, write
  "No file with a relationship."
- **Dependency limits:** add to the Coverage and limits section, from the
  `analyze_cycles` and `analyze_coupling` results: the `coverage.languages`
  entries with `supported: false`; the `details.relationships` counts (`total`,
  `resolved`, `external`, `unresolved`); the relevant
  `incomplete.counts.unresolved` and the first entries of
  `incomplete.unresolved` (`file`, `kind`, `target`, `reason`), with a note
  that an unresolved relationship can hide a cycle or a dependency; each
  `limits_hit` entry; the `excluded.counts`, `incomplete.skipped_files` and
  `incomplete.parse_failures`; and each truncation (`total` against what is
  shown). A result with `complete: false` can miss cycles or dependencies;
  say so.
