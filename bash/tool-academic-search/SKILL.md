---
name: tool-academic-search
description: Search and download academic papers from the terminal across arXiv, PubMed, bioRxiv, medRxiv, and Google Scholar. Search one source or all at once, download PDFs (arXiv via the fast arxiv-dl path), and extract a paper's full text to stdout. Use when the user says "find papers on X", "search arxiv/pubmed for X", "download this paper", "get me the PDF for <arXiv id/DOI/PMID>", or wants academic literature from the command line. Hands a downloaded PDF off to vault-source-digest when the user wants it filed into the EmptyOS KB. NOT for reading an already-local PDF (use tool-pdf-reader) and NOT for digesting a standard/textbook into the KB directly (use vault-source-digest).
---

# Academic Search Skill

Search and download research papers from the terminal. Wraps `paper-search-mcp`
(arXiv, PubMed, bioRxiv, medRxiv, Google Scholar) + `arxiv-dl` (fast arXiv PDF
downloads).

`SKILL_DIR` below = this skill's own directory — `skills/tool-academic-search/` in a clone, or `~/.claude/skills/tool-academic-search/` in the per-machine store.
Reference the script with that absolute path.

## Isolation (important)

The underlying tools live in a dedicated venv at
`%LOCALAPPDATA%/eos/envs/academic/` — **NOT** the EmptyOS daemon env. They drag
in `rich>=14` / `starlette>=1.0` which conflict with the daemon's pins, so they
were deliberately isolated (per `.claude/rules/environment.md` § user-home
Python envs). `academic.py` re-execs itself under the venv python automatically,
so you can call it with a plain `python` — no activation needed.

## Setup (one-time, already done)

```bash
uv venv --python 3.13 "%LOCALAPPDATA%/eos/envs/academic"
uv pip install --python "%LOCALAPPDATA%/eos/envs/academic/Scripts/python.exe" arxiv-dl paper-search-mcp
```

## Usage

### 1. Search

```bash
python "<SKILL_DIR>/academic.py" search "diffusion models" --source arxiv -n 5
python "<SKILL_DIR>/academic.py" search "crispr gene editing" --source pubmed
python "<SKILL_DIR>/academic.py" search "battery degradation" --source all -n 3
python "<SKILL_DIR>/academic.py" search "graph neural network" --json     # machine-readable
```

- `--source`: `arxiv` (default) | `pubmed` | `biorxiv` | `medrxiv` | `scholar` | `all`
- `-n`: max results per source (default 8)
- `--json`: emit a JSON array (`id, title, authors, date, source, url, doi`) — use this when you need to parse results to pick one to download.

Per-source failures are soft (printed to stderr) so `--source all` never dies on one bad backend.

### 2. Download a PDF

```bash
python "<SKILL_DIR>/academic.py" download 1706.03762 --dir ./papers --pdf-only
python "<SKILL_DIR>/academic.py" download https://arxiv.org/abs/1512.03385 --dir ./papers
python "<SKILL_DIR>/academic.py" download 42318429 --source pubmed --dir ./papers
```

- arXiv targets route through `arxiv-dl` (fast, parallel, clean filenames).
- `--source pubmed|biorxiv|medrxiv` use the respective backend; pass a PMID or DOI.
- `--pdf-only` (arXiv) skips the accompanying notes file.

### 3. Read a paper's full text (stdout)

```bash
python "<SKILL_DIR>/academic.py" read 1706.03762 --source arxiv
```

Downloads then extracts the paper text. **Costs context** — prefer this only for
short papers or when you need the content in-conversation. For a long paper,
`download` it then use `tool-pdf-reader`'s `dump` mode (token-cheaper).

## Workflow: find → download → file into KB

1. Search and show the user candidates:
   ```bash
   python "<SKILL_DIR>/academic.py" search "<topic>" --source all -n 5
   ```
2. On their pick, download the PDF to a scratch or vault attachments dir:
   ```bash
   python "<SKILL_DIR>/academic.py" download <id> --dir "{vault}/99_Attachments/papers" --pdf-only
   ```
3. To file it into the EmptyOS KB, hand the downloaded PDF to **vault-source-digest**
   (creates the `reference` landing note + `clause`/`case` notes). To just read it
   locally, use **tool-pdf-reader**.

## Sources covered

| Source | search | download | read | id format |
|---|---|---|---|---|
| arXiv | ✓ | ✓ (arxiv-dl) | ✓ | `2606.20554` / abs URL |
| PubMed | ✓ | ✓ | ✓ | PMID |
| bioRxiv | ✓ | ✓ | ✓ | DOI |
| medRxiv | ✓ | ✓ | ✓ | DOI |
| Google Scholar | ✓ | — | — | (search only) |

Google Scholar is search-only (no stable PDF endpoint); use it to discover a
title, then download from arXiv/PubMed if available.

## When NOT to use this

- The PDF is already on disk → **tool-pdf-reader**.
- Goal is digesting a standard/textbook into the KB → **vault-source-digest** (hand it the downloaded PDF).
- You need a Google Scholar PDF directly → not supported; find the paper on arXiv/PubMed instead.
