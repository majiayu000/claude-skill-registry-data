---
name: agnos-graph
description: "AGNOS project state graph: from the process index and the source folders, writes one dated JSON file of the project's state at a commit: the artifacts, their links with proofs, the IDs the sources cite, task tiers; on request the call graph and the history. Holds no score. USE FOR: giving a tool or agent the project's state; rebuilding the graph agnos-perf-center reads."
argument-hint: "--process <dir> --sources <dir> [--sources <dir>...] [--out <file>] [--ext <.x>...] [--exclude <pattern>...] [--generated-at <t>] [--call-graph] [--history [--history-since <date|duration>] [--history-depth <n>]]"
---

# AGNOS Graph

<!-- RQ-TRC-129, RQ-TRC-130, RQ-TRC-133, RQ-TRC-119 / ADR-TRC-022 (DEC-TRC-074, DEC-TRC-077), RQ-PLG-005 -->

Needs Python 3.9 or later, standard library only. It knows only the AGNOS ID grammar and index format, so it works on any AGNOS
project. Run it; do not read the scripts. `<skill-folder>` is the folder holding this file. `agnos-perf-center` runs it itself
when its graph is absent or when it is given `--rebuild`.

1. Invoke the `agnos-index` skill first: the graph reads `process.idx.md`, never the documents' headings.
2. From the project's root (`python` on `windows`, `python3` on `linux` / `macos`):
   `python <skill-folder>/scripts/graph.py --process agnos-process --sources <source folder>`

| Parameter | Meaning |
|---|---|
| `--process <dir>` | The folder holding `process.idx.md` |
| `--sources <dir>` | Repeatable: every folder whose files should carry IDs (code, tests, build, CI). Not a documentation folder quoting IDs as examples: they would be counted. |
| `--out <file>` | Default `<process>/4.knowledge/agnos-graph.json` |
| `--ext .x`, `--exclude <pattern>` | Repeatable; each **replaces** its default list (`--help` shows them), at the user's responsibility <!-- RQ-TRC-119 --> |
| `--generated-at <t>` | The state's date; a fixed timestamp makes the file byte-identical |
| `--call-graph` | Adds functions and calls. Needs once `pip install -r <skill-folder>/requirements-callgraph.txt`; without it the graph is written without them |
| `--history` | Adds who changed what and the deliveries, from git |
| `--history-since <date or duration>`, `--history-depth <n>` | Limit the history read (`6.months`, `2026-01-01`); only with `--history` |

**Output:** one JSON file, generated, never edit it: the state true at its `meta.generatedAt` and `meta.commit`; its format is in
`references/graph-format.md`. The project decides whether to commit or ignore it.

**Exit codes:**
- `0`: written. The last line reads `agnos-graph: <n> elements, <n> files, <n> tasks; <graph> written in <s.mmm> s`, with
  the call graph and the history before the file when asked. A `no history: <cause>` warning on the error stream still means
  the file is written.
- `1`: input error on the error stream, nothing written. Apply the Error Recovery Protocol.

**Report** to the user the line as it is, the `scanned extensions`, `scanned names` and `excluded` lines before it, saying whether
each is the default or the user's, and the path of the file.
