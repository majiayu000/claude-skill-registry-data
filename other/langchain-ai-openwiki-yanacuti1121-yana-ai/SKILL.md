---
name: langchain-ai--openwiki
description: "Use when the user wants to generate or keep repository documentation up to date via OpenWiki (langchain-ai/openwiki) — an LLM-driven CLI that writes a wiki for a codebase (or a personal knowledge base from Notion/Gmail/Slack/X/web search) and keeps it fresh via a scheduled CI pull request. Examples: \"set up OpenWiki for this repo\", \"keep the docs updated automatically\", \"generate an agent wiki\"."
origin: https://github.com/langchain-ai/openwiki
license: MIT
---

# OpenWiki (langchain-ai/openwiki)

CLI that writes and maintains an **agent wiki** for a codebase, or a personal
knowledge wiki from configured connectors (Notion, Gmail, Slack, X, web
search, Hacker News). Unlike a purely graph/index-based tool, OpenWiki uses an
LLM to *synthesize* documentation from ingested sources, and ships a CI
workflow to keep that documentation current automatically.

Not a duplicate of `gitnexus-cli` in this repo: GitNexus builds a knowledge
graph + embeddings for structural code queries; OpenWiki synthesizes prose
documentation via an LLM and can pull from non-code sources too. Use GitNexus
for "trace calls to X" style structural queries, OpenWiki for "keep readable
docs current."

## Install

```bash
npm install -g openwiki
# or: pnpm add -g openwiki
```

Bun install can fall back to compiling a native `better-sqlite3` dependency —
prefer npm/pnpm unless Visual Studio Build Tools (Windows) or build essentials
are already set up.

## Two modes — pick one explicitly

```bash
openwiki code --init        # repository documentation, written to openwiki/
openwiki personal --init    # personal knowledge wiki, written to ~/.openwiki/wiki/
```

Bare `openwiki --init` is not supported — mode is required on init.

## Commands

| Command | Effect |
|---|---|
| `openwiki` | Interactive CLI, stays open for follow-up messages |
| `openwiki "<request>"` | Interactive, with an initial request |
| `openwiki -p "<request>"` | One-shot, non-interactive, prints final output and exits |
| `openwiki code --update` | Refresh repo docs (creates them first if missing) |
| `openwiki --update` | Refresh personal wiki (defaults to personal mode) |
| `openwiki auth <slack\|gmail\|x\|notion>` | Authenticate a connector |
| `openwiki ngrok start` | Tunnel for Slack OAuth callback during first-time auth |
| `openwiki --help` | Full command reference |

In an interactive session: `/api-key` updates the provider key, `/langsmith-key`
sets/clears optional LangSmith tracing credentials. Both use masked prompts —
**never paste a real key into a non-interactive transcript this skill's own
guidance produces**; direct the user to run these interactively themselves.

## CI auto-update (the main reason to reach for this over a one-off doc gen)

Copy the example workflow into the target repo so docs stay current without
manual reruns:

- GitHub Actions: `examples/openwiki-update.yml` → `.github/workflows/openwiki-update.yml`
- GitLab CI: `examples/openwiki-update.gitlab-ci.yml` → include from `.gitlab-ci.yml`

In CI, use `openwiki code --update --print` — `--update` creates the initial
`openwiki/` docs if none exist yet, so `--init` isn't needed in that path, as
long as the workflow provides the provider/model env vars. The scheduled run
opens a PR/MR with the documentation delta, not a direct push to the default
branch.

## AGENTS.md / CLAUDE.md integration

Each `code` run maintains both files at the repo root inside a managed
`<!-- OPENWIKI:START -->…<!-- OPENWIKI:END -->` block — created if absent,
otherwise only that block is rewritten and the rest of the file is left
alone. Safe to run in a repo that already has a hand-written `CLAUDE.md`.

## Rules

- Mode (`code` vs `personal`) must be explicit on `--init` — don't guess which one the user wants; ask if it's ambiguous from context.
- Config and secrets land in `~/.openwiki/.env` on the user's own machine — never read, log, or echo this file's contents on the user's behalf.
- Connector auth (`openwiki auth ...`) opens an interactive OAuth flow — run it and let the user complete auth themselves, don't attempt to script credentials into it.
- Recommend the CI workflow (auto-PR) over manual reruns when the user's actual goal is "keep docs from going stale," not "generate docs once."

## Anti-patterns

```
❌ Running `openwiki auth <provider>` and trying to supply credentials non-interactively
❌ Reading/printing ~/.openwiki/.env "to check the config"
❌ Suggesting a direct push to main from the CI workflow instead of the tool's own PR/MR flow
❌ Treating this as a replacement for gitnexus-cli's structural graph queries — different job
```

## Verification

After `openwiki code --init` or `--update`, confirm the `openwiki/` directory
(or `~/.openwiki/wiki/` for personal mode) was actually written and `AGENTS.md`/
`CLAUDE.md` contain the managed block, rather than assuming success from the
CLI's exit code alone.
