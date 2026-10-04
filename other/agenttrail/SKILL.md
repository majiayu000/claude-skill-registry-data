---
name: agenttrail
description: >-
  Live map of a multi-agent build in the browser: which plan component is being
  worked on, by which agent or harness, what is done and what is stuck. Use when
  a multi-agent pipeline starts (/startcycle, /startcycle-graph,
  /teamwork-preview) or after a plan-canvas approve, or when the user asks to
  see what the agents are doing.
category: bdb-core
metadata:
  version: "0.2.0"
  origin: sodiumsun/agenttrail@e4ba2da
  license: MIT
---

<!-- Source: sodiumsun/agenttrail bin/agenttrail.mjs + public/index.html — MIT, see THIRD_PARTY_NOTICES.md -->

# agenttrail — live pipeline map

agenttrail serves a browser board that mirrors a multi-agent build in real time: which plan component is being worked on, by which agent or harness, what is done and what is stuck. It observes only — it never runs agents and never marks tasks done.

## Start the map

```bash
aos-trail . --plan production_artifacts/00_execution_plan.md --no-open
```

It prints the URL (default http://localhost:5330, next free port if taken). Open that URL for the user. If running inside AO (env var `AO_BROWSER_CAPABILITY` is set), run `ao preview <url>` so it shows in AO's Browser tab. Without a plan file, start it with just `aos-trail .` — it then shows file activity only.

## Ensure (auto-start)

```bash
aos-trail --ensure [--cwd <dir>] [--plan <file>] [--session <id>] [--json]
```

Starts the map detached if none runs for this repo (matched via `/whoami` `repoPath` on 127.0.0.1:5330-5344). `repoPath` is the repo's main checkout, so every git worktree of a repo finds the same map; the map shows each worktree as its own lane (branch and folder) and files hook events by their `cwd`. `/whoami` also lists `worktrees`, opens it at most once per session (state in `$TMPDIR/aos-trail-ensure/`), and always exits 0. Plan: `--plan`, else `production_artifacts/00_execution_plan.md`, else the single `production_artifacts/*/00_execution_plan.md`; it needs a `{#id}` marker. No open under `CI`, SSH, or headless Linux; with `AO_BROWSER_CAPABILITY` it runs `ao preview <url>`. `--json` prints `{url,started,opened,reason,plan,hint}`. Test overrides: `AOS_TRAIL_OPENER` (opener command), `AOS_TRAIL_PORTS=lo-hi` (probe range).

Lanes: main first, then at most 11 worktrees; the slots go to the most recently active ones (a lane with events in the last 10 min keeps its slot), and events from any further worktree of the repo are filed in one `other worktrees` lane, never in main. `/whoami` carries `protocol: 2`. `--ensure` replaces a daemon on this repo (or one of its worktrees) that lacks it: the new map starts first, then the old one is asked to quit via `POST /shutdown` (JSON body naming its own `repoPath`); a daemon that cannot (older ones have no such API) keeps running and `hint` says which port to stop. Two concurrent `--ensure` runs share a lock file in `$TMPDIR/aos-trail-ensure/`. `/setup` on a map with several lanes needs `{"lane": "<key>"}` and writes into that checkout.

## Plan convention

The plan file uses components and tasks:

- `## Plain-language name {#id}` = a component (5-9 per plan), stable ids
- under it optional lines: `needs: [id, id]`, `links: [id]`, `files: [src/**]`, `url: production_artifacts/00_architecture.html`
- tasks: `- [ ] Outcome {#task-id}`; mark `[~]` BEFORE starting, `[x]` when done, `[!]` when stuck, and add an indented `by: <agent>` line (claude, codex, agy, opencode)
- save the file immediately after each status change; never batch updates to the end
- Mermaid blocks and prose may stay in the file; the map ignores them.

## Live agent events

The AOS installer registers `.claude/hooks/trail-relay.mjs --agent <harness>` for Claude Code (PreToolUse, PostToolUse, SessionStart, Stop, SubagentStop), Antigravity and Codex (PreToolUse, Stop). The OpenCode plugin and mcsc (for the CLI workers it delegates to) post events directly. Events are fire-and-forget (300 ms cap) and never block a tool call; with no map running they are dropped.

A component's `url:` may be a path under `production_artifacts/` — the map serves that folder, so e.g. `url: production_artifacts/00_architecture.html` opens the archify diagram from the card.

## Stop

The daemon runs until its terminal/process ends; `aos-trail up` relaunches saved boards.

## Rules

- Never create a root `PLAN.md` in a user repo during an AOS pipeline — always point at the pipeline's plan with `--plan`.
- Never mark `[x]` without evidence in the code.
