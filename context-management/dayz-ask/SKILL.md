---
name: dayz-ask
description: "Answers a plain English question about vanilla DayZ with checked path:line citations. Use when the user asks how vanilla does something, where it lives, or what a vanilla class or config value does."
argument-hint: "\"<question>\" [--top-k N] [--excerpt-lines N] [--file-type T] [--folder F] [--grep] [--json]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-ask

A script finds and checks the evidence. You read it and write the answer. Every claim in the answer cites a line the script read from disk. The script runs the RAG search, checks every hit against the file on `P:\`, and falls back to a keyword Grep of the vanilla folders when there is no `VOYAGE_API_KEY` or index.

Follow `skills/_shared/dayz-conventions.md`. Format the answer per `skills/_shared/answer-formatting.md`.

## How to run

```cmd
python "<skill-dir>\ask.py" "<question>" [--top-k N] [--excerpt-lines N] [--file-type T] [--folder F] [--grep] [--json]
```

Narrow the search whenever the question allows it: `--file-type cpp` for a `config.cpp` value, `--file-type c` for script behaviour, `--folder gui` for a layout. For example:

```cmd
python "<skill-dir>\ask.py" "what does the food config set for spoil time" --file-type cpp --folder dz
```

| Argument | Notes |
|---|---|
| `"<question>"` | The user's question in their words. |
| `--top-k N` | Search hits, or Grep files, to keep (1 to 25, default 5). |
| `--excerpt-lines N` | Longest excerpt printed per citation (1 to 300, default 60). Raise it to see whole functions. |
| `--file-type T` | Only one file type: `c`, `cpp`, `hpp`, `h`, `layout`, `cfg`, `rvmat`, `xml`, `json` or `csv`. Use `cpp` for `config.cpp` questions and `c` for script questions. |
| `--folder F` | Vanilla folder for the Grep fallback: `scripts`, `dz`, `gui`, `core`, `graphics` or `languagecore`. Repeat it for more than one. The default is `scripts` and `dz`. |
| `--grep` | Skip RAG and use the Grep fallback. |
| `--json` | Print the report as JSON after the verdict line. |

## What the script does

1. Runs `search_dayz_source` from the `dayz-rag` server when the index is built and `VOYAGE_API_KEY` is set. Each run is a new process, so the dayz-rag server's in-memory cache does not carry over between `/dayz-ask` runs; the MCP tool `search_dayz_source` in a session does reuse it.
2. Reads every hit's lines from `P:\`. A hit is `verified` when the cited lines still hold the indexed text, or `moved` when the text now sits at other lines, in which case the citation points at the new lines. A hit whose text is gone is dropped and listed under `dropped`. `verified` says only that the citation is real, not that it answers the question.
3. Re-cites a checked hit longer than 60 lines at its best term lines. The index can return a whole config class (the `CfgVehicles` hit in `P:\dz\gear\food\config.cpp` spans lines 240 to 14564), and the first 60 lines of it rarely hold the answer. The lines inside the span are scored the way the Grep fallback scores a file's lines, and each window (two lines either side of a matching line, up to three per hit) becomes its own citation, with `within` naming the whole span. A long hit with no term line inside it is dropped as off topic.
4. Drops a checked hit as off topic when its distance is above 1.15 (`RAG_MAX_DISTANCE`), or when neither its excerpt nor its class context holds a search term from the question. A term inside a quoted asset path ("food" in `model="\dz\gear\food\BoxCereal.p3d"`) does not count. A cooking config class returned for a food spoilage question is dropped this way. Each one is listed under `dropped` with its reason.
5. Falls back to Grep when there is no key, no index, the search fails, or no hit survives the checks. It splits the question into search terms (common words and words under three letters are dropped, except a two-letter word written in capitals or one of `AI`, `HP`, `UI`, `ID`, `NV`, `UV`; a two-letter term matches only as its own word or name part, so `AI` finds `EntityAI` but not `FAIL`), scans the vanilla folders, and ranks files by how many of the rarer terms they hold. A file that declares a class or function whose name holds a term ranks higher. Debug and GUI files (a `gui` folder, or `debug` in a folder or file name) count half, so gameplay classes come before debug readouts. Grep citations are lines read from disk, so they count as checked.

## Output and exit codes

The first line is the verdict: `EVIDENCE` (exit 0), `NONE` (exit 1, nothing found) or `ERROR` (exit 2: empty question, a question made only of common words such as "how does it work", bad argument (reported before the common-words check), `P:\` not mounted, or the script crashed, for example when the `dayz-rag` server fails to load). Notes follow, then each citation with the lines read from disk:

```
EVIDENCE 2 citation(s) via rag
[1] P:\scripts\4_world\classes\bleedingsources\bleedingsource.c:7-203  verified  distance=0.708  BleedingSource
    | class BleedingSource
    | ...
```

`via` is `rag`, `grep`, or `rag+grep` when RAG gave no surviving hit (none returned, or all dropped as stale or off topic). An excerpt shows at most 60 lines.

With `--json`, the report holds `verdict`, `question`, `mode`, `notes`, `citations` and `dropped`. Each `dropped` entry has `cite` and `reason`. Each citation has `cite` (`path:line_start-line_end`), `path`, `line_start`, `line_end`, `status`, `source` (`rag` or `grep`) and `excerpt`; RAG citations add `distance` and `context`, and `within` when the hit was re-cited from a longer span; Grep citations add `match_line` and `terms_in_file`.

## Writing the answer

- Answer only from the excerpts. When the answer needs lines past an excerpt, read them with `get_dayz_file` or `Read` first.
- Cite every claim as `path:line_start-line_end`, using the `cite` value or a narrower range inside it.
- Lead with the answer in a sentence or two, then the supporting citations.
- A kept citation is real and shares a word with the question, but may still not answer it. Grep results match words, not meaning. Use only the citations that answer the question and ignore the rest.
- If the evidence does not answer the question, say so, and suggest a narrower question or a `--file-type` or `--folder`. Do not fill the gap from memory.
- Pass on each note that names a fix: a missing key, a missing index, or dropped hits that call for `/dayz-search-index --full`.

## Limits

- It reads vanilla files only, never your mod.
- Grep ranks by words, so a question about behaviour can return lines that only share a word with it. The RAG search ranks by meaning.
- It checks that `P:\` is mounted itself and does not run `/dayz-preflight`, since it only reads files. Mount the drive with `/dayz-workdrive`.
