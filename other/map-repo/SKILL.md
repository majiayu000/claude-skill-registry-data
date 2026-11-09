---
name: map-repo
description: "Maps a repository for orientation: its languages and size, where complexity concentrates, and how the most complex files connect to the rest. Use when the operator or an agent is new to a repository, asks for an overview, a map, a tour, or where to start reading."
---

# Map Repo

This skill maps a repository with the act-lite MCP tools. It reports the
languages and size of the repository, the files where complexity
concentrates, and for each of those files what it depends on and what depends
on it. It ends in a report and never edits a file.

## Adapt

An operator instruction wins over every default below: the scope, the number
of files to detail, whether tests are included.

The tools are the `act-lite` MCP server's. The same results come from the
`act-lite query` and `act-lite analyze` commands, so a session without the MCP
server runs the commands instead.

## Inputs

- **`paths`:** the files or directories to map, relative to the workspace
  root. Default: `[]`, the whole workspace.
- **`top`:** the number of hotspot files to detail, 1 to 1000. Default: 10.
- **`include_tests`:** `false`, unless the operator asks for tests to be
  included. Pass it to `analyze_hotspots` and `graph` only then.

## Procedure

1. **Languages and size.** Call `repo_outline` once per `paths` entry, with
   that entry as `path` (omit `path` for the workspace root), `max_files` =
   500 and `symbols` = `false`. Sum the files and the lines per language over
   the calls.
   - If any call has `truncated: true`, the report says the outline is
     partial.

2. **Where complexity concentrates.** Call `analyze_hotspots` with `paths` and
   `limit` = `top`. Its findings are the top files, highest score first.

3. **How the top files connect.** Call `graph` with `paths`, `focus` = the
   `file` of each step-2 finding, `direction` = `both`, `max_depth` = 1 and
   `limit` = 1000. Its findings are the direct dependencies and the direct
   dependents of each top file.
   - If step 2 returned no file (`findings` is `[]`), skip this step and say so
     in the report.
   - A top file in a language without dependency support is listed in
     `details.focus_files_not_analyzed`. For such a file the report shows only
     its dependents, and says that its own dependencies are not analyzed.

4. **Report.** Write the report below from the three results: their findings,
   `total`, `truncated`, `status`, `complete`, `coverage`, `excluded`,
   `incomplete` and `details`. Write nothing else, and change no file.

## Report

```
## Repository map: <scope>
Languages: <language — files, lines> … (repo_outline<, partial>)
### Where complexity concentrates
| Rank | File | Score | Functions | Top function |
Ranking: <hotspots details.formula>.
### How the top files connect
- <file>: depends on <n> files (<to>, …); depended on by <m> files (<file>, …)
Relationship kinds: <details.kinds>.
### Not analyzed and limits
Dependency support: <supported languages>; not supported: <languages>. Unresolved relationships: <n> (<first entries>). Depth limit: 1 (<limits_hit detail>). Regions not analyzed (<file>:<range>: <reason>). Exclusions and truncation.
```

- **`<scope>`:** the `paths`, or "the workspace" for `[]`.
- **Languages:** one entry per language of the summed outline, largest first,
  as `<language> — <files> files, <lines> lines`. Add ", partial" after
  `repo_outline` when a call was truncated.
- **Where complexity concentrates:** one row per step-2 finding, in result
  order. Rank is 1, 2, …; File, Score and Functions are `file`, `score` and
  `functions`; Top function is the first of `top_functions`: its `function`
  (or `(anonymous)` for `null`) at its `range`. Then the `details.formula`
  line. With no file, write "No analyzed file has a function."
- **How the top files connect:** one line per top file. For an edge, `file`
  depends on `to`; a top file's dependencies are the edges with that `file`,
  its dependents the edges with that `to`. Count each related file once, and
  list the files. A related file that is not analyzed (`to_analyzed: false`)
  is listed and marked as such. For a file in
  `details.focus_files_not_analyzed`, write only "depended on by …" and add
  "its own dependencies are not analyzed". With no top file, write "No top
  file, so no connections were mapped." Then the `details.kinds` line.
- **Not analyzed and limits:**
  - the `coverage.languages` entries with `supported: false` (from the
    `graph` result, else from the `analyze_hotspots` result) and the
    languages that have dependency support;
  - `details.relationships` of the `graph` result (its `total`, `resolved`,
    `external` and `unresolved` counts); `incomplete.counts.unresolved`, which
    is the unresolved count that bears on the top files, and the first entries
    of `incomplete.unresolved` (`file`, `kind`, `target`, `reason`); and a note
    that an unresolved relationship can hide a dependency or a dependent;
  - each `limits_hit` entry of the `graph` result, which at depth 1 shows
    that the top files' neighbours have relationships that are not shown;
  - the `excluded.counts`, `incomplete.skipped_files` and
    `incomplete.parse_failures` of each result;
  - the `details.regions_not_analyzed` entries of the `analyze_hotspots`
    result, each entry (`file`, `range`, `reason`) once, the
    `details.regions_not_analyzed_total` when it is more than the entries
    listed, and `details.files_without_analyzed_code`. In component files
    (`.vue`, `.svelte`, `.astro`), only script regions are analyzed: the
    template and style regions are not, so no score comes from them.
    Component files are not graph sources: the `graph` result reports Vue,
    Svelte and Astro as `supported: false`, so their own dependencies are not
    analyzed;
  - each truncation (`total` against what is shown), and a partial outline
    from step 1.
  A result with `complete: false` can miss findings in that evidence; say so.
  Scores rank files by complexity × lines, and an edge is a file relationship
  read from the source; neither shows that a change to a file breaks its
  dependents.
