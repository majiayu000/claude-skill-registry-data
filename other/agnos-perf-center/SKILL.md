---
name: agnos-perf-center
description: "AGNOS performance center: monitors how the process runs on a project (not code speed). From agnos-graph's state graph, built if absent, writes an HTML page and its data: coverage, quality score, findings. USE FOR: checking MANDATORY TRACEABILITY at session end or before a release; what cites a requirement; with --call-graph, its functions; with --history, who changed what and what was delivered."
argument-hint: "--process <dir> [--sources <dir>...] [--graph <file>] [--rebuild] [--out <file>] [--ext <.x>...] [--exclude <pattern>...] [--title <t>] [--generated-at <t>] [--call-graph] [--history [--history-since <date|duration>] [--history-depth <n>]]"
---

# AGNOS Performance Center

<!-- RQ-TRC-017, RQ-TRC-098, DEC-TRC-050, RQ-PLG-005; RQ-TRC-131, RQ-TRC-132 / DEC-TRC-075, DEC-TRC-076 -->

Needs Python 3.9 or later, standard library only. It reads the project's state from the graph file of the `agnos-graph` skill,
and runs that skill itself when the graph is absent or `--rebuild` is given. Run it; do not read the scripts.
`<skill-folder>` is the folder holding this file.

1. Invoke the `agnos-index` skill first: the graph reads `process.idx.md`, never the documents' headings.
2. From the project's root (`python` on `windows`, `python3` on `linux` / `macos`):
   `python <skill-folder>/scripts/perf_center.py --process agnos-process --sources <source folder> --rebuild`

| Parameter | Meaning |
|---|---|
| `--process <dir>` | The folder holding `process.idx.md` |
| `--graph <file>` | The graph read; default `<process>/4.knowledge/agnos-graph.json` |
| `--rebuild` | Runs `agnos-graph` even when the graph exists: without it, an existing graph is read as it is, at its own date |
| `--sources <dir>` | Repeatable; needed to build the graph: every folder whose files should carry IDs (code, tests, build, CI), not a documentation folder quoting IDs as examples |
| `--ext .x`, `--exclude`, `--call-graph`, `--history`, `--history-since`, `--history-depth` | Passed to `agnos-graph` when it builds the graph: its `SKILL.md` gives their meaning and default lists |
| `--out <file>` | Default `<process>/PERF-CENTER.html` |
| `--title <t>`, `--generated-at <t>` | The page's title; a fixed timestamp makes the page, and a graph it builds, byte-identical |

**Outputs:** the page, `<page>.json` and `<page>.data.js` beside it: generated, never edit them; the project decides whether to commit or ignore
them; share the three together. The page loads its libraries from cdnjs, so it needs the network once. A link can open it
on an element, `<page>#RQ-XXX-001`, or on a view, `<page>#view=<tab>` (`matrix`, `graph`, `quality`…, any tab the page shows).
<!-- RQ-TRC-016, RQ-TRC-121 / DEC-TRC-066 -->

**Exit codes:**
- `0`: written. The last line reads `agnos-perf-center: <n> elements, <n> files; RQ <n>: covered <n>, indirect <n>, uncovered <n>;
  quality: <grade> <score>/10; checks: <key> <score>, …; findings <n>; <page> written in <s.mmm> s`, with the call graph and the history before
  the page when the graph holds them. A `no history: <cause>` warning on the error stream still means the page is written.
- `1`: input error on the error stream, nothing written: a graph absent with no `--sources`, unreadable, or that `agnos-graph` could not build. Apply the Error Recovery Protocol.

**Report** to the user the line as it is, the checks scoring under 10, the path of the page, which tells the rest to its reader, and, when `agnos-graph` built the graph, the lines it printed before, as its `SKILL.md` says.

**When asked to explain or maintain, read only the file concerned:**

| Question | File |
|---|---|
| What a finding, a check, a score, the call graph, the history or a delivery figure means | `references/rules.md` |
| What `<page>.json` holds | `references/data-format.md` |
| How to run the tests, change a library or a visual value | `references/maintaining.md` |
