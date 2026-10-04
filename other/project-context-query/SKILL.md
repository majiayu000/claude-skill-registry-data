---
name: project-context-query
description: Answer questions about the project using the vault's layered memory — Graphify code graphs, the compiled LLM Wiki, then raw files — instead of re-reading code or transcripts. Use for any question about the project, the codebase, the process, the people, or past decisions.
---

# Project Context Query (3-Layer Traversal)

Route every question to the cheapest layer that can answer it. Escalate only
when a layer comes up short. All commands run from the vault root (`python` on
Windows, `python3` on macOS/Linux).

## Route by question type

| Question is about… | Go to | How |
|---|---|---|
| Code structure, "what calls X", "where is Y implemented", architecture | **Layer 1: Graphify** | `graphify query`, `explain`, `path`, `affected` |
| Change impact ("what breaks if I change X") | **Layer 1** | `graphify affected "X" --graph graphify/<repo>/graph.json` |
| Business process, decisions, people, environments, constraints, history | **Layer 2: Wiki** | `python scripts/wiki_tool.py search-catalog --query "..."` → open top 1–3 notes |
| What happened in a meeting / exact wording | **Layer 3a: Raw sources** | open the specific `Raw/Sources/` file the wiki note cites |
| Exact current code needed for an edit | **Layer 3b: Raw code** | open the specific repo file, narrowly |

When a question spans layers (e.g. "how should the new handler validate
input?"), take **decided rules from Layer 2** and **code shape from Layer 1**,
then only open the files you will actually edit.

## Layer 1 — Graphify (code)

On Windows/PowerShell set `$env:PYTHONUTF8=1` first — without it graphify's
final print can crash on Unicode (output still arrives; exit code is dirty).

```bash
# from the vault root, against the committed snapshots:
graphify query "how does authentication work" --graph graphify/<repo>/graph.json
graphify explain "<NodeName>" --graph graphify/<repo>/graph.json
graphify path "<A>" "<B>" --graph graphify/<repo>/graph.json
graphify affected "<function>" --graph graphify/<repo>/graph.json

# from inside a repo, the default graph is ./graphify-out/graph.json:
graphify query "where are sessions created"
```

- Human-readable entry points: `graphify/<repo>/_GRAPH_REPORT.md` and the
  `_COMMUNITY_*.md` notes (named clusters).
- Budget answers with `--budget 1500` when you only need orientation.

## Layer 2 — Compiled Wiki (knowledge)

```bash
python scripts/wiki_tool.py search-catalog --query "<topic>"
```

Open only the top matches. Key hubs: the topic note(s) in `Wiki/Topics/` and
the active project note in `Wiki/Projects/` (status, open questions). Wiki
notes carry `sources:` back to transcripts/docs when you need Layer 3a.

## Layer 3 — Raw (last resort)

- **Raw sources:** only the file a wiki note cites, for verification or exact
  wording.
- **Raw code:** only the specific files you are editing or that Layers 1–2
  pointed at. Never sweep a repo.

## Memory feedback (optional but encouraged)

After a graph query materially helps (or misleads), record it so the graph's
memory improves:

```bash
graphify save-result --question "..." --answer "..." --outcome useful   # or dead_end / corrected
graphify reflect    # occasionally: aggregate outcomes into LESSONS.md
```

## Freshness

If code changed significantly since the graphs were built, refresh before
trusting Layer 1: `python scripts/sync_graphs.py` (fast, AST-only), or a full
`/graphify <repo> --update` + re-export for the browsable notes.

## Never

- Never re-read whole repos or all Raw sources to "get context".
- Never answer business-rule questions from code alone — the wiki carries the
  decided rules (and their open questions).
- Never edit generated files (`graphify/`, catalogs, indexes) by hand.
