---
name: review-change
description: "Reviews a change for code health: structural problems in the changed functions and duplication that touches the change. Use when the operator asks to review a diff, branch, commit range or pull request for complexity, size, nesting, parameter lists or duplicated code."
---

# Review Change

This skill reviews one change for code health with the act-lite MCP tools.
It reports structural problems in the functions the change touches and the
duplication the change takes part in. It ends in a report and never edits a
file.

## Adapt

An operator instruction wins over every default below: the base to compare
against, the files to review, whether tests are reviewed.

The tools are the `act-lite` MCP server's. The same results come from the
`act-lite analyze` command (`act-lite analyze patterns …`), so a session
without the MCP server runs the commands instead.

act-lite does not run `git`; you do. Run only the read-only `git` commands
below. Never stash, reset, check out or commit.

## Inputs

- **Base:** a git ref. Default: the merge base of `HEAD` with the default
  branch (`git merge-base HEAD origin/HEAD`, else `main`, else `master`).
  The change is the working tree against the base.
- **Or a file list:** the files to review. Every line of each listed file
  counts as changed, and step 1 is skipped.
- **`include_tests`:** `false`, unless the operator asks to review tests too.
  Pass it to both tools only then.

## Procedure

1. **Changed files and changed lines.** Skip this step for a file list.
   - Files: `git diff --name-only --diff-filter=AMR <base>`, plus the
     untracked files from `git ls-files --others --exclude-standard`.
     Every line of an untracked file counts as changed.
   - Lines: `git diff -U0 --diff-filter=AMR <base>`. Each hunk header
     `@@ -a,b +c,d @@` marks the new-side lines `c` to `c + d - 1` as
     changed. A hunk that only deletes lines (`d` = 0) marks the new-side
     line `c` at the deletion point as changed, so the function around a
     deletion is reviewed.
   - Paths are relative to the repository root, which is the workspace of
     the act-lite server.

2. **Nothing to review, or nothing in scope.**
   - If no file changed, write the report with "No file changed against
     `<base>`." and call no tool.
   - If a tool call returns the error that starts with `no files to analyze
     in the requested scope` (for example every changed file is a test),
     quote the message in the report's Not analyzed section, and still run
     the other step.

3. **Structural problems.** Call `analyze_patterns` with
   `paths` = the changed files and `limit` = 1000.
   - Keep each finding whose `range` (`"L:C-L:C"`, lines inclusive) overlaps
     a changed line of its `file`.
   - If the result has `truncated: true`, split the file list in two halves
     and call once per half, again while a result is truncated and its list
     has more than one file. Concatenate the findings in file order. A single
     file that is still truncated contributes its first 1000 findings, and
     the Limits section gives its `total`.

4. **Duplication.** Call `analyze_clones` with `paths` = `[]` (the whole
   workspace), `focus` = the changed files and `limit` = 1000.
   - Keep each clone class with a member whose `file` is a changed file and
     whose `range` overlaps a changed line of that file.
   - A result lists at most 20 `members` of a class; `members_total` gives
     the full count. When no listed member overlaps a changed line and
     `members_total` is more than the members listed, keep the class too: a
     member that is not listed can overlap the change. Mark it "overlap not
     determined". Members in `focus` files are listed first, so this occurs
     only when at least 20 members are in changed files.
   - If the result has `truncated: true`, split `focus` in two halves and call
     once per half, again while a result is truncated and its list has more
     than one file. A single file that is still truncated contributes its
     first 1000 classes, and the Limits section gives its `total`. Each call
     analyzes the whole workspace, so a split is the rare case.

4a. **Files exposed to the change.** Call `analyze_impact` with `paths` =
   `[]` (the workspace), `focus` = the changed files that exist in the working
   tree and `limit` = 100.
   - A deleted path in a file list is dropped from `focus` and named in the
     section.
   - A changed file in a language without dependency support still gets its
     dependents (for example the importers of a changed CSS file). It is
     listed in `details.focus_files_not_analyzed`.
   - If the change only deletes files, there is no focus: skip this step. The
     section lists the deleted files (`git diff --name-only --diff-filter=D
     <base>`) and says that relationships that pointed at them now appear as
     unresolved in the Limits section (from step 4b).
   - Steps 4a and 4b run whenever the change adds, modifies, deletes or
     renames a file. The rule in step 2 that no tool is called when no file
     changed applies to steps 1 to 4 only.
   - Pass `include_tests` to `analyze_impact` and `analyze_cycles` only when
     the operator asks to review tests too.

4b. **Cycles that involve the change.** Call `analyze_cycles` with `paths` =
   `[]` and `limit` = 1000. Keep every cycle when the change can re-resolve a
   relationship of an unchanged file, that is, when the change:
   - (a) adds, deletes, renames or changes the type of a file
     (`git diff --name-only --diff-filter=ADRT <base>`, plus the untracked
     files). A file list has no base, so (a) cannot be decided and every cycle
     is kept;
   - (b) touches a resolution input or a discovery input: a file named
     `package.json`, `go.mod` or `Cargo.toml`, any `*.json` file (a `tsconfig`
     `extends` target can have any name), `.gitignore`, `.git/info/exclude`,
     `pyvenv.cfg` or `CACHEDIR.TAG`. (b) also holds when the change touches
     any file listed in the `analyze_cycles` result's
     `details.resolution_inputs` (for example a `tsconfig` `extends` target
     named `base.jsonc` or with no extension). When
     `details.resolution_inputs_total` is more than the entries shown, every
     cycle is kept. A listed input that is a symbolic link is read through its
     target, which the list does not name: when any listed input, or a
     directory above it, is a tracked symbolic link (`git ls-files -s` mode
     `120000`), every cycle is kept;
   - (c) changes a `.rs` file that contains a module declaration (`mod
     <name>;` or `mod <name> {`, also inside a macro invocation) or a
     `#[path` attribute, before or after the change (the Rust module tree); or
   - (d) modifies a Python `__init__.py` file. Its bound names decide whether
     `from pkg import n` in an unchanged file resolves to `pkg/__init__.py` or
     to the submodule `pkg/n.py`, so a change to them can create a cycle with
     no changed member. (A module file `x.py` has no submodules, so its
     bindings cannot redirect an edge to another file.) It also holds when the
     change modifies a Python file that a package's `__init__.py` is a
     symbolic link to, because that file's bound names are the package's:
     when the repository tracks a symbolic link named `__init__.py`, or one
     to a directory (`git ls-files -s` mode `120000`), treat a change to any
     `.py` file as (d).

   Otherwise keep each cycle that has a changed file among its `members`. When
   `members_total` is more than 20 and no shown member is a changed file, keep
   the cycle and mark it "members not all shown". If `truncated` is true, say
   how many of `total` were examined.
   - The kept set holds every cycle that the change creates: a new cycle needs
     an edge that did not exist before. An edge appears only when a
     relationship of a changed file changes (that file is then a member of the
     cycle), or when an unchanged relationship resolves differently, which
     happens only in (a), (b), (c) or (d). The kept set can also hold older
     cycles. The report does not claim that each cycle is new: comparing with
     the base needs an analysis of a second checkout.

5. **Report.** Write the report below from the kept findings and classes and
   from each result's `status`, `complete`, `coverage`, `excluded`,
   `incomplete` and `details`. Write nothing else, and change no file.

## Report

```
## Code health review: <base>..<working tree>
Scope: <n> changed files; patterns <status>, complete <bool>; clones <status>, complete <bool>.
### Structural problems in changed functions
| Location | Function | Rule | Value | Threshold |
### Duplication that touches the change
- <kind> clone, <tokens> tokens, <members_total> members: <file>:<range> (variant <v>), …
### Files exposed to the change
<n> dependents (<direct> direct, <transitive> transitive) of <changed> changed files (<focus_files> focus files; not analyzed themselves: <focus_files_not_analyzed>).
| Dependent | Depth | Reaches | Through |
A dependent is a file that imports a focus file, directly or through other files. It is exposed to a change in the focus file. This is not proof that it will break, and a file that is not listed is not proof that it is safe: relationships that act-lite does not model (see the README) are not followed.
### Cycles that involve the change
<all cycles kept, because the change <adds, deletes or renames a file | touches a resolution or discovery input | changes a Rust file with a module declaration | modifies a Python __init__.py file>> | <n> cycles with a changed file>.
- <members_total> files: <path as <file> → <to> → …>[ (path of <path_total> steps, <n> shown)]; members: <file>, …[ (members not all shown)]; changed members: <file>, …
### Not analyzed
Unsupported languages, excluded counts (tests, generated, vendored, ignored), skipped files, parse failures, component regions not analyzed (regions_not_analyzed).
### Limits
A clone class shows that code has the same syntax tree, apart from formatting, comments and, for renamed clones, identifier names and literal values. It does not show that the members behave the same, that they can share one function, or that extracting them is safe. Findings are measurements against fixed thresholds (<details.thresholds>).
```

- **Structural problems:** one row per kept finding, in result order.
  Location is `<file>:<range>`; Function is `function`, or `(anonymous)` for
  `null`; Rule, Value and Threshold are `rule`, `value` and `threshold`.
  With no kept finding, write "None in the changed functions."
- **Duplication:** one line per kept class, in result order, with its
  `members` (each `<file>:<range> (variant <variant>)`); when
  `members_total` is more than the members listed, add "and <n> more".
  For a class marked "overlap not determined", end its line with
  "— overlap not determined (<listed> of <members_total> members shown)".
  With no kept class, write "None that touches the change."
- **Files exposed to the change:** the `details.direct`, `details.transitive`,
  `details.focus_total`, `details.focus_files` and
  `details.focus_files_not_analyzed` counts, then one row per finding, in
  result order: Dependent is `file`, Depth is `depth`, Reaches is `reaches`,
  Through is `chain` written as `<file> → <to>` steps. Then the statement
  line, word for word. With no finding, write "No dependent." If step 4a was
  skipped, name the deleted files instead of the table.
- **Cycles that involve the change:** the reason that all cycles were kept
  (the case of (a), (b), (c) or (d) that applies), else "<n> cycles with a
  changed file". One line per kept cycle, in result order: `members_total`;
  the `path` steps, from the cycle's `file` back to it, written as
  `<file> → <to>` steps (the first step's `file`, then each step's `to`), with
  "(path of <path_total> steps, <n> shown)" when `path_total` is more than the
  <n> steps shown; the `members`, listed separately, with "(members not all
  shown)" when `members_total` is more than the members listed (this includes
  each cycle marked "members not all shown" in step 4b); and the changed
  members. The `members` are sorted by path, not in traversal order: never
  write them as a path. The section
  says that the cycles are those that involve the change, not only those that
  it creates. With no kept cycle, write "No cycle involves the change."
- **Not analyzed:** from each result, the `coverage.languages` entries with
  `supported: false`, the `excluded.counts`, the `incomplete.skipped_files`
  and the `incomplete.parse_failures`, and any empty-scope message from step
  2. A result with `complete: false` can miss findings in that evidence; say
  so. Also add each `details.regions_not_analyzed` entry (`file`, `range`,
  `reason`) of the `analyze_patterns` calls, and `details.files_without_analyzed_code`;
  when `details.regions_not_analyzed_total` is more than the entries shown,
  give the total. Do not use the list of the `analyze_clones` call: that call
  analyzes the whole workspace. In component files (`.vue`, `.svelte`,
  `.astro`), only the script regions are analyzed; the template, style and
  other regions are not.
- **Limits:** the sentence above, the thresholds from the `analyze_patterns`
  result's `details.thresholds`, and, for each split that stayed truncated,
  the file and its `total`.
- **Dependency limits:** add to the Not analyzed and Limits sections, from the
  `analyze_impact` and `analyze_cycles` results: the `coverage.languages`
  entries with `supported: false`; the `details.relationships` counts (`total`,
  `resolved`, `external`, `unresolved`); the relevant `incomplete.counts.unresolved`
  and the first entries of `incomplete.unresolved` (`file`, `kind`, `target`,
  `reason`), with a note that an unresolved relationship can hide a dependent
  or a cycle; each `limits_hit` entry; the `excluded.counts`,
  `incomplete.skipped_files` and `incomplete.parse_failures`; and each
  truncation (`total` against what is shown). A result with `complete: false`
  can miss dependents or cycles; say so.
