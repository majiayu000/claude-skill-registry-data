---
name: rsk-guide
version: 0.4.0
description: Operator's guide for the rsk CLI — manage ralvaskills via the .rsk/ project manifest (rsk new, rsk install, rsk pin), bundle/global installs and the official Anthropic cache, and the `rsk mcp` server the agent queries for project standards. Use when the user mentions rsk, asks how to install/pin/update skills, wants to add a skill to a project, is starting work in a new project or scaffolding (to learn which standards apply), or wants to set up ralvaskills on a new machine. Companion to cli-tool-architect (CLI design), mcp-architect (server design) and skill-builder (authoring new skills).
---

# RSK Guide

> **Draft (v0.3.0).** The `rsk` CLI is in progress. Verify against `rsk --help` once shipped. For creating *new* skills (vs managing existing ones), use [`skill-builder`](../skill-builder/SKILL.md). For designing CLIs in general, see [`cli-tool-architect`](../../tooling/cli-tool-architect/SKILL.md).

## Always ask the user before taking action

Installing, pinning, updating, or uninstalling skills changes what tools and standards future agents will load in this and other projects. These are **architectural decisions**, not housekeeping. **Never run `rsk install`, `rsk uninstall`, `rsk update`, `rsk new`, `rsk destroy`, `rsk pin`, or `rsk unpin` without explicit user confirmation.**

For every proposed action:

1. **State the action plainly** — which skills/bundles, target scope (`--global` / `--for` / project manifest), and what changes on disk (including `.rsk/CLAUDE.md` and `./CLAUDE.md` edits when pinning)
2. **Quote the exact command** you'd run
3. **Wait for the user to confirm**, redirect, or decline
4. **Use `--dry-run`** when available if the user wants to see the effect first

Read-only commands (`rsk list`, `rsk catalog`, `rsk status` without `--stack`) are safe to run without asking — they only display state. Anything that touches symlinks, the manifest, the project `CLAUDE.md`, the official cache, or makes network calls (`rsk status --stack`) needs an explicit go.

If the user gives a blanket "yes" up front (e.g. "set everything up for this project"), still pause and confirm before each *bundle* or *pin*. A slip from `go-grpc` to `go-rest`, installing globally when they meant locally, or pinning a skill they didn't want auto-loaded is hard to undo silently.

## Two workflows

Pick the one that matches the user's intent.

### A. Project manifest (`.rsk/`) — preferred for per-project skill sets

Mirrors `go.mod`: a declarative `rsk.mod` lists the skills this project depends on, `rsk.lock` records resolved versions, and pinned skills are auto-imported into `./CLAUDE.md` via `@.rsk/CLAUDE.md`. Lives in `<project>/.rsk/`.

```bash
rsk new                                # creates .rsk/rsk.mod + .rsk/CLAUDE.md + appends import to ./CLAUDE.md
rsk install <name[@version]>           # adds to manifest, symlinks into .rsk/skills/, updates rsk.lock
rsk install <name> --pin               # also imports skill into .rsk/CLAUDE.md (auto-loaded in this project)
rsk pin <name>                         # pin an already-installed skill
rsk pin <name> --remove                 # remove the import (skill stays installed; `rsk unpin` still works)
rsk list                               # show manifest entries with pinned/installed marks
rsk update <name>                      # re-resolve + re-link to latest available version
rsk install                            # (no args) re-installs everything in rsk.mod (after clone, after edits)
rsk destroy                            # delete .rsk/ and remove @.rsk/CLAUDE.md import
```

**Pin vs install** — installed skills are present on disk but not auto-loaded; pinned skills are imported in `.rsk/CLAUDE.md` and load every turn in that project. Pin only what truly needs auto-loading.

### B. Bundle / global install — fastest path for stack-standard setups

Install a curated bundle or single skill into the project (`.rsk/skills/`) or globally with `--global` (`~/.claude/skills/`, `~/.config/opencode/skills/`).

```bash
rsk install <name...>                              # project: bundle or skill → .rsk/skills/, writes rsk.mod
rsk install <name...> --global                     # global: all configured tool dirs, no manifest
rsk install <name> --global --for claude-code      # global, one tool only
rsk install <name> --include personal            # personal/ skill, explicit opt-in (`--personal` still works)
rsk install <name> --dry-run                       # preview without writing
```

Names are auto-resolved against the catalog: a name that matches a bundle expands to that bundle's skills; otherwise the name is treated as a single skill. Bundles win on name collisions.

> Project installs land in `.rsk/skills/` and always update `rsk.mod`. Use `--global` if you want the skill linked system-wide without manifest tracking.

## Quick reference

### Discover (read-only — safe)

| Command | Purpose |
|---|---|
| `rsk catalog` | All available skills |
| `rsk catalog bundles` | All available bundles |
| `rsk catalog bundle <name>` | Skills in a specific bundle |
| `rsk catalog --source local\|official` | Filter by source |
| `rsk catalog --include personal` (`--personal` still works) | Include personal skills |
| `rsk catalog -o json` | Machine-readable output |
| `rsk list` | Project manifest entries (installed/pinned marks) |
| `rsk list --global` | Skills linked in global tool dirs |
| `rsk list --global --for <tool>` | Scope global listing to one tool |
| `rsk status` | What's installed across project + global; bundle tags; pinned tags (no network) |
| `rsk status --global` / `--project` | Restrict scope |
| `rsk status --for <tool>` | Scope `--global` to one tool |

### Setup (state-changing — ask first)

```bash
rsk init                              # once per machine — writes ~/.config/rsk/config.json
rsk init --force                      # overwrite existing config
```

`rsk init` prompts for:
1. **Skill source**: local clone (path to your `ralvaskills` repo) **or** hosted registry (`skills.ralvarez.dev`)
2. **AI tools to support**: `claude-code`, `opencode`, or both
3. **Global skills dir** per selected tool (defaults: `~/.claude/skills/`, `~/.config/opencode/skills/`)
4. **Default scope** for bare `--global` (`all` configured tools, or a single tool)

### Update (state-changing — ask first)

```bash
rsk update [name...] [--global] [--for <tool>] [--include official,personal] [--dry-run]
```

- Local-clone mode: `git pull` on the repo (symlinks update automatically). Add `--include official` (legacy `--official`) to also pull `anthropics/skills` cache.
- Registry mode: fetches latest index, re-downloads + re-links any skill whose installed version is behind.

### Uninstall (state-changing — ask first)

```bash
rsk uninstall <name...> [--global] [--for <tool>] [--include personal] [--dry-run]
```

Project uninstall also cleans the matching entries from `rsk.mod` / `rsk.lock` and unpins them from `.rsk/CLAUDE.md` (or `opencode.json`).

### Status with live fetch (network — ask first; **not yet implemented**)

```bash
rsk status --stack [--refresh]        # planned: fetch latest versions from proxy.golang.org / pypi.org
```

Per the spec this is opt-in with a 24h cache; the current build returns an explicit "not yet implemented" error. Don't promise drift checks until it ships.

## Common workflows

**First-time machine setup** (confirm each step with the user)
1. `rsk init` — pick local clone or registry, configure tools
2. `rsk install global --global` — universal skills, machine-wide

**Set up a new project with tracked manifest**
1. `cd <project>` then `rsk new`
2. `rsk install <name>` per skill (use `--pin` for ones that should always auto-load)
3. Commit `.rsk/rsk.mod`, `.rsk/rsk.lock`, `.rsk/CLAUDE.md`, and the `@.rsk/CLAUDE.md` import line in `./CLAUDE.md`

**Set up a new project with a stack bundle**
1. `cd <project>` then `rsk new`
2. `rsk install <stack-bundle>` — e.g. `rsk install go-grpc`

**Bring an existing manifest project up to date after `git clone`** — `rsk install` (no args)

**Add a single skill mid-project**
- Tracked: `rsk install <name>` (+ `--pin` if it should auto-load)
- Untracked, system-wide: `rsk install <name> --global`

**Update everything** — `rsk update` (local clone) or `rsk update --include official` (also refresh Anthropic cache)

**Upgrade a single manifest skill** — `rsk update <name>`

## Bundle quick map

| Bundle | Source | Use for |
|---|---|---|
| `global` | local | Every machine — universal workflow + meta skills |
| `docs` | official | Document creation (docx/xlsx/pdf/pptx/find-docs) |
| `design` | mixed | Frontend / UI projects |
| `go-grpc` | local | Go gRPC services |
| `gin` | local | Go REST services (Gin) |
| `nethttp` | local | Go REST services (stdlib net/http) |
| `go-cli` | local | Go command-line tools |
| `fastapi` | local | Python REST services (FastAPI) |
| `python-grpc` | local | Python gRPC services |
| `python-cli` | local | Python command-line tools |
| `llm-app` | local | LLM apps / RAG pipelines |
| `ros2` | local | ROS2 robotics |
| `event-driven` | local | Schema-first messaging (NATS/Kafka/RabbitMQ) |
| `observability` | local | Signals + dashboards/alerts |
| `code-review` | local | Reviewer triad: security, contracts, performance |

## What's in `.rsk/`

```
.rsk/
├── rsk.mod         # TOML: version, pinned[], skills{name = version-constraint}
├── rsk.lock        # TOML: resolved {name, version, source, path} per skill
├── skills/         # symlinks into the local repo or registry cache
│   └── <name>/     # → ralvaskills/skills/.../<name>/  or  registry cache
└── CLAUDE.md       # one `@skills/<name>/SKILL.md` line per pinned skill
```

`./CLAUDE.md` gets a single appended line: `@.rsk/CLAUDE.md`. Both `rsk new` (creates it) and `rsk destroy` (removes it) are idempotent.

## MCP server (`rsk mcp`)

`rsk new` can register the rsk MCP server in the project (`.mcp.json` for Claude Code, `opencode.json` for OpenCode) and write a short pointer into `./CLAUDE.md`. Re-run `rsk new` to register later — it is idempotent and never drops other MCP servers. `rsk destroy` removes the registration.

The server exposes, over stdio:

| Primitive | Name | Does |
|---|---|---|
| Tool | `project_profile` | Detects the project's stack (citing the file that proves each trait) and proposes the skills that apply. Read-only. |
| Tool | `search_skills` | Keyword search over the catalog. Read-only. |
| Tool | `install_skills` | Installs skills/bundles into the project or globally. |
| Resource | `rsk://catalog` | The catalog, with descriptions truncated. |

Recommended flow: `project_profile` → propose to the user → `install_skills` once approved. Installed skills appear automatically in the client's skill list, so no extra skill is needed to discover them.

**Approval is on the client, not the server.** The server marks `install_skills` with `anthropic/requiresUserInteraction`, so Claude Code forces its approval prompt on every call — this holds even if the model never read this skill. Never install skills yourself without the user's confirmation; state which skills and which scope.

The server is launched by the client, so **`rsk` must be on PATH**. `rsk new` warns and skips registration when it is not.

## Full reference

For the complete CLI specification — exhaustive flag list, `config.json` shape, catalog overrides, discovery rules, edge-case behavior — see `docs/SPECS.md` in the [ralvaskills](https://github.com/ralvarezdev/ralvaskills) repo.
