---
name: graphify-triage
description: >-
  Use this skill when the user wants to turn code graph analysis into tracked GitHub issues —
  "audit the architecture", "find god nodes", "triage architectural debt", "run graphify and log
  issues", "what's over-coupled in this codebase", "create issues from graphify findings",
  "check for structural problems", "scan for architectural smells", or any request that combines
  codebase topology analysis with issue tracking. This skill runs graphify to build a dependency
  graph, parses GRAPH_REPORT.md for god nodes and structural patterns, converts findings into
  GitHub issue payloads, and optionally pushes them to the repo. It bridges static analysis and
  project management in a single automated pass. Requires graphify and gh CLI.
---

# Graphify Triage

## What This Skill Does

Graphify Triage is a two-phase pipeline:

1. **Audit** — runs graphify on the codebase, reads `graphify-out/GRAPH_REPORT.md`, and extracts god nodes (high-centrality over-coupled components) and suggested audit questions. Saves structured issue payloads to a JSON file for review.
2. **Sync** — pushes the reviewed payloads to GitHub as labelled issues via the `gh` CLI.

The separation matters: always audit first and review the payloads before syncing. This gives the user a chance to prune or edit before issues appear in the tracker.

## Dependencies

- **graphify** — AST extraction and graph generation. Must be installed and on PATH.
- **gh** (GitHub CLI) — authenticated (`gh auth login`) before running sync.

## Quick Start

```bash
# Phase 1: generate and review proposed issues
uv run ~/.claude/skills/graphify-triage/scripts/triage.py audit --path . --output payloads.json

# Inspect payloads.json, edit or remove entries as needed, then:

# Phase 2: push to GitHub
uv run ~/.claude/skills/graphify-triage/scripts/triage.py sync --input payloads.json
```

To target a specific repo (e.g. when the CWD origin differs):

```bash
uv run ~/.claude/skills/graphify-triage/scripts/triage.py sync --input payloads.json --repo owner/repo
```

## Workflow Steps

1. Confirm graphify is installed (`graphify --version`). If missing, install it first — the audit step will fail silently otherwise.
2. Run `audit`. The script calls `graphify . --update` internally, so the graph is always fresh.
3. Open `payloads.json` and review the proposed issue titles and bodies. Remove or edit any that are false positives.
4. Confirm `gh auth status` shows authenticated before proceeding to sync.
5. Run `sync`. Issues are created with `architecture`/`audit` labels. If the repo lacks those labels, `gh` may prompt interactively — create them in advance to keep the run non-interactive.

## What the Audit Parses

The script extracts three sections from `graphify-out/GRAPH_REPORT.md`:

| Section | What it becomes |
|---|---|
| `## God Nodes` | One issue: "[Architectural Refactor] Decouple God Nodes…" listing the top 3 |
| `## Surprising Connections` | Captured but currently informational only (not converted to issues) |
| `## Suggested Questions` | One issue per question: "[Audit] …" with context from the report |

## Pitfalls to Avoid

**Stale graph**: if you made significant changes since the last graphify run, the report may not reflect them. The `audit` command always passes `--update` to graphify, so this is only a risk if you're re-syncing an old `payloads.json`.

**Missing labels**: `gh issue create --label architecture` fails silently if the label doesn't exist in the target repo. Create labels upfront:
```bash
gh label create architecture --color 0075ca
gh label create audit --color e4e669
```

**Wrong repo**: `sync` infers the repo from the git remote. Pass `--repo owner/repo` explicitly when running from a clone that points somewhere other than the intended tracker.
