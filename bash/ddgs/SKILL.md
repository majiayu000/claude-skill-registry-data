---
name: ddgs-search
description: Use the Python-based ddgs CLI (via `uvx ddgs`) for ad-hoc, unlimited web searches across multiple search engines. Trigger this skill when the user asks you to look something up online, compare sources, or gather search-based research.
---

# DDGS Search

## Workflow
1. Clarify the user’s intent and translate it into a concise ddgs query (e.g., “OpenClaw agent capabilities”, “台北市立大學 markeTech 2026”, “AI-generated music licensing summary”).
2. Choose the appropriate ddgs subcommand (`text`, `news`, `images`, `videos`, `books`) and supply the query via `-q/--query` plus any filters you need.
3. Run the CLI with the desired flags. Example:
   ```bash
   uvx ddgs text \
     -q "OpenClaw agent" \
     -b google \
     -p 1 \
     --output json \
     --verify False
   ```
4. Pull the most relevant titles, snippets, and URLs (or file paths) from the generated output, summarize key findings, cite the sources/engines, and ask if the user wants deeper digging.

## Command reference
- `uvx ddgs text` → General web search. Supports `-b/--backend` (e.g., `duckduckgo`, `bing`, `google`, `auto`), `-p/--page`, `-m/--max_results`, `-r/--region`, and `-t/--timelimit`.
- `uvx ddgs news` → News sources only; pair with `-r/--region` or `-t/--timelimit` to narrow to breaking stories.
- `uvx ddgs images`, `uvx ddgs videos`, `uvx ddgs books` → Media-specific metasearches; capture `title`, `href`, and any metadata exposed in JSON output (e.g., `ext`, `download` paths).

## Available backends
| Function | Backends |
| --- | --- |
| `text()` | bing, brave, duckduckgo, google, grokipedia, mojeek, yandex, yahoo, wikipedia |
| `images()` | duckduckgo |
| `videos()` | duckduckgo |
| `news()` | bing, duckduckgo, yahoo |
| `books()` | annasarchive |

## Mode-specific options
### text (general web searches)
- Pass the search phrase with `-q/--query` (text only); `-k/--keywords` is deprecated.
- `-r/--region` (e.g., `us-en`, `uk-en`, `ru-ru`) and `-s/--safesearch` (`on`, `moderate`, `off`) control localization and content sensitivity.
- `-t/--timelimit` accepts `d`, `w`, `m`, or `y` for day/week/month/year windows; omit for all-time.
- `-m/--max_results` limits how many entries ddgs returns (default 10) and `-p/--page` picks the page number (default 1).
- `-b/--backend` lets you pin engines (comma-delimited names or `auto` to pick automatically). Works with the backend list above.

### news (news-focused search)
- Same core flags as `text` (`-q`, `-r`, `-s`, `-t`, `-m`, `-p`, `-b`), but ddgs only queries news outlets.
- Use `-t` to keep results fresh (day/week/month), and prefer `bing`, `duckduckgo`, or `yahoo` backends for broader coverage.

### images
- Inherits the general `-q`, `-r`, `-s`, `-t`, `-m`, `-p`, `-b` flags with backend locked to `duckduckgo`.
- Extra filters include `--size` (`Small`, `Medium`, `Large`, `Wallpaper`), `--color` (`Red`, `Orange`, `Yellow`, `Green`, `Blue`, `Purple`, `Pink`, `Brown`, `Black`, `Gray`, `Teal`, `White`, `Monochrome`, `color`), `--type` (`photo`, `clipart`, `gif`, `transparent`, `line`), `--layout` (`Square`, `Tall`, `Wide`), and `--license` (e.g., `any`, `Public`, `Share`, `ShareCommercially`, `Modify`, `ModifyCommercially`).

### videos
- Core flags work the same (`-q`, `-r`, `-s`, `-t`, `-m`, `-p`, `-b`) with `duckduckgo` as the backend.
- Additional filters: `--resolution` (`high`, `standard`), `--duration` (`short`, `medium`, `long`), `--license` (`creativeCommon`, `youtube`).

### books
- Only supports `-q`, `-m`, `-p`, and `-b` (backend defaults to `annasarchive`). Use this mode to find e-books or archived copies.

## Flags & options
- `-q/--query`, `-r/--region`, `-s/--safesearch`, `-t/--timelimit`, `-m/--max_results`, `-p/--page`, and `-b/--backend` cover the shared behaviors across modes (text/news/images/videos/books).
- `-o/--output` writes structured CSV/JSON (or `filename.json`) for easy parsing.
- `--verify False` is often necessary here to bypass TLS certificate issues; `True` performs strict verification.
- `--download`/`--download-directory` fetch results locally—useful for images or videos that need inspection.

## Result files
- When you use `--output json`, ddgs saves the results to a timestamped file (`text_<query>_<YYYYMMDD>_<HHMMSS>.json`). Open that file to read titles, snippets, and URLs, then delete or archive it once the insight is shared.
- If `--download` runs, note the download directories (default `./downloads/` or the one you provided) and mention them to the user.

## Environmental notes
- Ensure `uvx` is on PATH before running anything (`which uvx`). On this system it now lives in `/usr/local/bin`, so the command is available globally.
- Re-run `uvx ddgs --help` occasionally to confirm the CLI has not changed.
- Record the exact command arguments you used so future agents can reproduce the search.

## Notes
- Always mention which search engine/backends you queried when it matters (some users trust DuckDuckGo’s privacy, others expect Google/Bing coverage).
- If ddgs returns sparse context, rerun with `--output json` and focus on the `body`/`snippet` fields before synthesizing your response.
