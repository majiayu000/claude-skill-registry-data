---
name: zread
description: Produce and consume a wiki-style knowledge base for a code repository via the `zread` CLI and its on-disk output under `./.zread/wiki/`. Use this skill whenever the user wants to understand, onboard onto, explore, summarize, map, or get an overview of an unfamiliar codebase; asks for architecture docs, a project wiki, a repo walkthrough, module/package explanations, or "what does this repo do"; wants to generate, regenerate, resume, browse, or serve code documentation locally; or mentions zread / zread.ai directly. Also use it proactively before diving into a large unknown repo — if `./.zread/wiki/current` exists, read the generated pages instead of crawling source file-by-file; if it doesn't, consider offering to run `zread generate`. The trigger is the intent (understand a codebase through generated docs), not the literal word "zread".
---

# zread skill

`zread` is a CLI that generates wiki documentation from code in the current
workspace using an LLM. Output lives under `./.zread/wiki/` in the workspace;
public repos can also be viewed at https://zread.ai.

This skill is intended for agent use. Read generated files directly from disk,
and use `--stdio` as the default mode for any zread command instead of trying
to parse the human TUI.

## On-disk layout (read these directly)

Always run `zread` from the workspace root. After a successful generation:

- `./.zread/wiki/current` — text file containing the active version id
  (e.g. `2026-03-12-010203`).
- `./.zread/wiki/versions/<id>/wiki.json` — TOC: `{id, generated_at, language,
  pages: [{slug, title, file, section, group, level}]}`.
- `./.zread/wiki/versions/<id>/<file>` — page markdown referenced by `pages[*].file`.
- `./.zread/wiki/drafts/` — in-progress generation; presence means a previous
  run did not finish. `drafts/wiki.json` exists once the catalog phase
  completed.
- `~/.zread/config.yaml` — global config (LLM provider, language, concurrency).
- `~/.zread/login.json` — presence indicates the user has logged in.

To answer questions about a codebase that already has zread output, read these
files directly with the file tools — do not invoke `zread browse`.

## Commands

| Command | Purpose | Key flags |
|---|---|---|
| `zread generate` | Generate wiki for cwd | `-y/--yes`, `--draft resume\|clear\|cancel`, `--skip-failed`, `--stdio` |
| `zread browse` | Serve docs at http://localhost:9681+ and open browser | `--generate`, `--version <id>`, `--host`, `--port`, `--stdio` |
| `zread login` | OAuth into BigModel/Z.AI to obtain an API key | `--custom`, `--model`, `--stdio` |
| `zread config` | Edit `~/.zread/config.yaml` | `--stdio` |
| `zread update` | Self-update CLI | `--stdio` |
| `zread version` | Print version | `--stdio` |

`--stdio` is supported on every command and turns the process into a JSON-line
machine protocol on stdin/stdout. See
[references/stdio-protocol.md](./references/stdio-protocol.md) for the wire
format (events, `waiting_for`, `done`, `quit`). Load it whenever zread is
invoked from another program/agent.

## Decision tree for an AI agent

1. **User wants to read existing wiki content?**
   - Check `./.zread/wiki/current`. If present, read `wiki.json` and the page
     markdown directly. No CLI invocation needed.
   - For known *public* GitHub repos, prefer the `mcp__zread__*` tools
     (`get_repo_structure`, `read_file`, `search_doc`) over running the CLI.

2. **User wants to (re)generate docs?**
   - Confirm with the user first — `generate` is long-running, calls an LLM,
     and writes files. Get explicit consent in unfamiliar directories.
   - Verify `~/.zread/login.json` exists or `~/.zread/config.yaml` has an
     `llm.api_key`. If neither, run `zread login` first.
   - If `./.zread/wiki/drafts/` exists, decide:
     - resume previous run → `zread generate --draft resume -y`
     - throw away and start fresh → `zread generate --draft clear -y`
   - Otherwise: `zread generate -y`.
   - To not block on a few failing pages: add `--skip-failed`.

3. **User wants to view docs in a browser?**
   - `zread browse` (add `--generate` to bootstrap if no wiki exists yet).

4. **User wants to script zread / consume output programmatically?**
   - Use `--stdio` and follow stdio-protocol.md. Do not screen-scrape the TUI.

## Non-interactive invocation rules

- Always pass `-y` to `generate` when running unattended; otherwise it stops
  at a catalog confirmation gate.
- Always set `--draft` explicitly when a draft may exist, so the command does
  not prompt.
- For any command run from another agent/script, use `--stdio` so output is
  parseable JSON instead of ANSI TUI frames.
- `zread` writes logs to `~/.zread/log/zread.log` — read this if a run fails
  silently.

## Safety / blast radius

- `generate` consumes LLM tokens (real cost) and can run for many minutes on
  large repos. Confirm before launching.
- `generate` writes only under `./.zread/` and does not commit anything to
  git. It is safe to delete `./.zread/wiki/drafts/` to recover from a stuck
  state.
- `update` replaces the zread binary in place and is hard to reverse — only
  run it when the user explicitly asks.
- `login` opens a browser for OAuth; do not run it in a non-interactive
  context unless the user has asked for it.

## Reference files

- [references/stdio-protocol.md](./references/stdio-protocol.md) — JSON-line
  wire protocol shared by every command's `--stdio` mode. Load when
  programmatically driving zread.
