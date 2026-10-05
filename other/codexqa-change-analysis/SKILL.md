---
name: codexqa-change-analysis
description: >
  Change-impact analysis for one diff: use CodexQA diff indexing
  (`index --diff-base` tags nodes and files `add` / `change` / `delete`, then
  `change-groups` / `symbol-diff` / `file-base`) to write one HTML report
  (affected entries, changed methods, test plan, coverage verdict, sensitive
  paths) and add runnable test files in the analyzed repo for uncovered points
  (add only; do not edit existing test files).
  Use when the user mentions change impact, change analysis, blast radius,
  affected entries, added methods, changed methods, test plan, generate or
  recall tests, link existing tests, entry points, 变更分析, 变更代码分析, 影响面,
  影响入口, 测试方案, or 召回测试用例.
  Requires the codexqa CLI. One change only.
  Whole-repo analysis with no diff, and general symbol-graph Q&A, are
  codexqa-code-analyzer, not this skill. Former skill name: change-impact-analysis.
license: Apache-2.0
compatibility: >
  Requires Node.js >= 18 and the `codexqa` CLI (`npm i -g @openqa-cn/codexqa`).
  Diff indexing and queries need no LLM. Data lives in ~/.codexqa/.
  Without codexqa, follow Degraded mode.
  Generating cases requires the analyzed repo to start; the end-to-end layer
  also needs a browser (L1/L2 in references/generate-cases.md).
metadata:
  author: openqa-cn
  version: "1.0.0"
  open-standard: agentskills
---

# Change Impact Analysis

One sentence: build a **trusted diff index**, then deliver two artifacts — a 7-section HTML report (key findings / risks and unknowns / affected entries / change list / test plan / coverage verdict / sensitive paths) plus **runnable test files** for points that are not covered.
`codexqa` has **no** `diff` or `review` subcommand. Change analysis always follows this path:

```text
index --diff-base <base> --full  →  change-groups / files --change  →  symbol-diff
   →  reach --direction in (entries)  →  tested_count / reach --edge-kinds tests  →  test-file text recall
```

## Deliverables (both required)

| ID | Deliverable | Form |
|---|---|---|
| A | **HTML report**: key findings / risks and unknowns / affected entries / change list / test plan / coverage verdict / sensitive paths | **One self-contained HTML file** at the repo root: `change-impact-<repo-slug>-YYYYMMDD-HHMM.html` |
| B | **New test files**: turn every test-plan row whose disposition is "add" into a runnable case | **New files** in the repo's existing test tree (at least one API/integration file; add an end-to-end file when a browser is required). **Add only; do not edit existing test files.** Layer rules, names, and fallbacks: [references/generate-cases.md](references/generate-cases.md) |

**Recalled existing cases are not a separate deliverable.** They land in the test-plan table's "case file" column and in the coverage-verdict section.

Template: `assets/report-template.html` (shipped with this skill). Fill contract: [references/report.md](references/report.md) — **read it before writing the report**.
`cp` the template and edit by id. **Do not read the whole template into context** (the 23 ids and the structure are in report.md).

**Default language is English.** The report is not Markdown in the chat; the chat only returns the HTML path. **Copy the template, then Edit the slots. Do not change CSS. Do not invent a new layout.** Delete the trailing mermaid loader as step 5 of "Diagrams must be static" in [references/report.md](references/report.md). Do not touch it otherwise.

Section order is fixed: results first, process last. The body answers only the four questions a reviewer cares about (which methods changed / which APIs or pages can trigger them / what to test / which existing cases can be reused).
Method and process data **never enter the report** (no process appendix, no "confidence / analysis scope" section). They stay in the analysis.

## Hard rules (a violation means rewrite)

1. **Do not conclude without a trusted diff index.** `--diff-base` must be paired with `--full`. Re-run whenever the base changes (incremental mode does not refresh change tags; see [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) item 1).
2. **"An entry is a method with no upstream caller" cannot rest on `to_count == 0` alone.** Cross-file call edges are missing in dynamic-language repos. Cross-check with text search / `imports`, or a function called by `router.get('/api/...')` will be reported as an entry.
3. **Test coverage comes only from a `tests` edge or a real assertion in a test file.** A filename containing `*test*`, or a symbol with the same name, is not coverage.
4. **Every conclusion must be checkable**: command, node id, and `file:line`. Do not replace query results with README, docs, or name guesses.
5. Report only changes introduced by this diff. Pre-existing issues found along the way go in their own note, not in the change list.
6. **Do not enumerate call sites with `codexqa query search`.** It is file-chunk BM25: one hit per file, no call line. Use `edges` / `reach` when the graph has the edge, and `grep` when it does not. See the split below.
7. **The report is a result for a reviewer, not an analysis log.** Process data (true-entry criteria, missing-edge fix counts, stub ratios, query fields, command names) never enters the report (no process appendix, and no confidence paragraph under "Risks and unknowns"). Headline numbers, key findings, and the entry table describe only the change's impact and risk, in business / API language. See "Iron rule" in [references/report.md](references/report.md).
8. **Line numbers in the report are editor lines (1-based).** CodexQA `start_line` / `end_line` / `search` lines are **0-based**. `grep -n` and editors are 1-based. **Add 1 to every CodexQA line** before writing `file:line`, or the reader lands one line off (measured on one JS repo: all 11 method locations were off by 1). See [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) item 8.
9. **Generated cases are add-only. Do not edit existing test files** (and do not edit `package.json`). Write the missing assertion as a **new case**; do not edit the old one. "Add only" **does not cap the file count** — if a point needs a browser, **create a new end-to-end file**; do not mark it "cannot cover". Layer rules, file names (follow the repo language and existing test style), and fallbacks are in [references/generate-cases.md](references/generate-cases.md). **You must actually start the service and run the files**, and write pass / fail counts back into the report. A case that was never run was not delivered. See [references/generate-cases.md](references/generate-cases.md).

## Why git / grep are still used

Change detection **always belongs to codexqa** (`index --diff-base --full` → `change-groups` / `files --change`).
git and grep fill only measured CodexQA gaps. They do not bypass CodexQA:

| Tool | Role in this skill | Why CodexQA alone is not enough |
|---|---|---|
| `codexqa index/query` | Change detection, patches, edge walks, blast radius, tests edges — **primary path** | — |
| `git rev-parse` / `git diff --name-only` | Resolve the base and branch; **check whether CodexQA change tags are stale** | Incremental indexes keep the previous diff tags (measured; [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md) item 1) |
| `grep -rn` | Enumerate **call sites missing from the graph**, and locate route registration / `main` and other text entries | When edges are missing, `edges` / `reach` return nothing; `search` is file-level and misses the real call (items 2 and 6) |
| `git diff` (degraded mode) | Fallback when CodexQA or the index is unavailable | Only then |

Rule: **if the graph can answer it, use the graph** (who is affected, where the entry is, whether a `tests` edge exists).
Fall back to text search only when the graph is clearly missing an edge, or there is no CodexQA index. **Whether evidence came from the graph or from text is a criterion; do not write it into the report.** When the whole report is degraded, mark `#meta-line` with one phrase: "Degraded: graph incomplete".

## Index trust gate (do this first)

```bash
cd <repo>                                   # prefer a local checkout
git rev-parse --abbrev-ref HEAD             # current branch
git diff --name-only <base>...HEAD          # files git considers changed (the reference set)

codexqa index . --diff-base <base> --full   # --full is required
codexqa query --repo . change-groups        # empty groups = the index is not in diff mode
codexqa query --repo . files --change add,change,delete
```

Choose `<base>` in this order: user-specified → `origin/main` → `main` / `master` → `HEAD~1`.
If there are several branches and the base is unclear, **ask the user**. Do not guess.

Consistency check: the `git diff --name-only` set must match `files --change add,change,delete`.
If they differ, re-run `index --diff-base <base> --full`. If they still differ, mark `#meta-line` "Degraded: index untrusted" and degrade.

## Workflow (8 steps)

| Step | What | Detail |
|---|---|---|
| 1 | Change list: added / changed / deleted methods and files | [references/analysis.md](references/analysis.md) §1 |
| 2 | Read the patch; classify the change (signature / behavior / add / delete) | §2 |
| 3 | **Entry resolution**: walk up to methods with no upstream caller, then force a cross-check | §3 |
| 4 | Regression scope: direct and transitive callers | §4 |
| 5 | Test plan: case matrix by entry, plus sensitive paths | §5 |
| 6 | **Recall existing tests**: layer A `tests` edges → layer B text recall (results go into the test plan and are written in step 8). **On a re-run, move the previous `change-impact-*` artifacts out of the repo first**, or recall will treat them as existing cases | [references/test-recall.md](references/test-recall.md) |
| 7 | **Generate case code**: turn rows whose disposition is "add" into runnable cases (file count and names follow the layer rules). Run them and record `file:line` plus pass / skip counts | [references/generate-cases.md](references/generate-cases.md) |
| 8 | **Write the report**: copy the HTML template → fill by id (including generated-case results) → tell the user the path | [references/report.md](references/report.md) |

Read [references/analysis.md](references/analysis.md) first. Read [references/test-recall.md](references/test-recall.md) only at step 6. Recalled cases go into the test-plan "case file" column and the coverage-verdict section. **Do not add a separate recall section.**
**Step 7 must finish before the report is written.** The `file:line` of rows marked "add", the "now covered" lines in `#coverage`, and the pass / skip counts in `#testplan-artifact` all come from a real run of the generated files. Writing the report first means filling those slots twice.
Read [references/generate-cases.md](references/generate-cases.md) at step 7. Read [references/report.md](references/report.md) before step 8, and use the shipped `assets/report-template.html`. Do not preload the whole tree.

Field cheat sheet: `to_count` = in-degree (caller count; used to judge entries); `from_count` = out-degree (who it calls; not blast radius); `tested_count` = number of `tests` edges pointing at it.
Commands live next to each step in [references/analysis.md](references/analysis.md). They are not repeated here.

## Degraded mode (no CodexQA, or the index is unusable)

Do not drop the delivery. Use git plus text search. The deliverable is still one HTML file. Mark `#meta-line` with "Degraded: no symbol graph" (the reader needs to know how strong the conclusion is). Do not write the degraded details into the report:

| Step | Degraded approach |
|---|---|
| Change list | `git diff --name-status <base>...HEAD`; use `git diff -U0` hunk headers to locate method bounds |
| Patch | `git diff <base>...HEAD -- <file>` |
| Entries | `grep -rn "<symbol>"` for every call site; walk those callers upward; route registration / `main` / an export is an entry |
| Test recall | Go straight to layer B in [references/test-recall.md](references/test-recall.md) |

Rewrite conditions (any one means rewrite the whole report) are in "Rewrite the whole report if" in [references/report.md](references/report.md). That list is the complete one; it is not repeated here.

## When blocked

Symptom → action is item 10 in [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md).
