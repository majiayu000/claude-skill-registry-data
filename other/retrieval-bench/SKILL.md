---
name: retrieval-bench
description: "Use only when the user asks to benchmark retrieval skills against a local or GitHub repo. One command writes benchmark.html. Do not use for ordinary search, graph recall, or wiki query."
---

# Retrieval bench

`<skill>` is the directory that contains this SKILL.md.

Point this at a checkout, a GitHub URL, an Obsidian vault, or use `--demo multihop`. Scores sibling `graph-memory`, `fde-kb`, and `llm-wiki`. Writes `benchmark.html`.

**No model API.** Ingest for llm-wiki is the harness agent's job (Poolside / Codex / Claude Code), per that skill's `SKILL.md`. This bench:

- queries only, or
- uses script `compile-extracts` as a stand-in for wiki pages, or
- scores `--wiki` if the agent already wrote pages.

Retrieve for all three skills is code-only. Output goes to the OS temp folder and opens in the browser.

## STOP

Run exactly one launcher command. Show the printed path. Do not invent scores. Do not ask for an OpenAI API key for this skill. Do not call a model to write the benchmark questions.

## Launcher

From the kit root:

```bat
py -3 scripts\retrieval-bench.py --demo multihop
py -3 scripts\retrieval-bench.py --repo C:\path\to\checkout
```

```bash
python3 scripts/retrieval-bench.py --demo multihop
python3 scripts/retrieval-bench.py --repo /path/to/checkout
```

After Poolside ingests a wiki, score it:

```bash
python3 scripts/retrieval-bench.py --repo /path/to/sources --wiki /path/to/wiki
```

## Output

Temp-dir `benchmark.html` + `results.json`. Opens by default (`--no-open` to skip).
