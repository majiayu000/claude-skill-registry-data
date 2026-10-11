---
name: game-studios-init
description: "Initializes a game project workspace for the Game Studios plugin: scaffolds directories, copies per-project seeds (technical-preferences, architecture registries, settings, rules), generates AGENTS.md with the anti-compression anchor, and merges .gitignore. Invoke when the user asks to initialize or set up a new game project, says 初始化/新项目开工, or right after installing the plugin in a fresh workspace."
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# Game Studios Project Initialization

Turns the current workspace into a Game Studios project. Idempotent: safe to
rerun; **existing files are never overwritten** — the managed anchor block in
`AGENTS.md` and the managed block in `.gitignore` are the only content ever
replaced in place. All mechanical work is done by a cross-platform (Windows /
Linux / macOS) POSIX-sh script (bash + awk — the same runtime the hooks already
require), so behavior is identical on every host and every run.

## What the script copies (and why)

| Workspace path | Source | Why |
|---|---|---|
| `.studio/technical-preferences.md` | plugin `docs/technical-preferences.md` | Per-project config with `[TO BE CONFIGURED]` placeholders; filled by `/game-studios:setup-engine`; **marker file that activates all hooks** |
| `.claude/settings.json` + `.studio/statusline.sh` | skill assets | Host plumbing for Claude Code: permission guardrails + production-stage status line (statusline script lives in the neutral `.studio/` dir). ZCode reads no project-level settings file, so none is written for it |
| `.claude/rules/` (11 files) | plugin `rules/` | Path-scoped coding standards, auto-enforced by Claude Code (verified). Other hosts: reference-only via the plugin copy (`${CLAUDE_PLUGIN_ROOT}/rules/`) — no third copy is seeded |
| `.codex/agents/` (51 files) | plugin `codex/agents/` | Codex-format subagents (TOML, `developer_instructions`) generated from `agents/*.md` by `codex/build_agents.sh`. Codex plugins cannot bundle subagents, so the workspace copy is the delivery mechanism (loaded only in trusted projects) |
| `CLAUDE.md` | skill asset template | **Standalone** Claude Code entry (collaboration protocol, stack placeholders, `@.studio/technical-preferences.md`) — not an `@AGENTS.md` shell. Created if missing; if present, only its managed anchor block is refreshed |
| `docs/registry/architecture.yaml` | plugin `docs/registry/architecture.yaml` | Empty scaffold; `/game-studios:architecture-decision` appends with user approval |
| `docs/architecture/tr-registry.yaml` | plugin `docs/architecture/tr-registry.yaml` | Empty scaffold; keeps TR-IDs stable across runs |
| `AGENTS.md` | skill asset template | Collaboration protocol, stack placeholders, anti-compression anchor (created only if missing) |
| directories | — | `src/ assets/ design/ design/gdd/ docs/ docs/architecture/ docs/registry/ tests/ tools/ prototypes/ production/*` |
| `.gitignore` | skill asset block | Framework ignores appended between managed markers |

## Procedure

1. **Survey first.** Check whether `AGENTS.md`, `.studio/`, `src/`, `design/`,
   `docs/` already exist and whether this is a brownfield project. If files
   the script would create already hold user content, confirm scope with the
   user before applying (copies skip existing files, so nothing is lost).
2. **Locate the script**: `scripts/init_workspace.sh` next to this file. The
   script resolves the plugin root from its own location; no environment
   variable is needed. It runs with bash and uses awk only — no sed multiline, no Python.
3. **Run with `--check`** to survey without writing, review the report with
   the user, then run without flags to apply:
   `bash <skill-dir>/scripts/init_workspace.sh "<workspace-dir>"`
4. **Post-run polish** (interactive): put the project name/title into
   `AGENTS.md`; remind the user that `/game-studios:setup-engine` populates
   `.studio/technical-preferences.md` — until then all hooks stay dormant
   by design.
5. **Verify**: the script prints `[created]`/`[skipped]`/`[updated]` per path
   and the hooks-marker status. Confirm `AGENTS.md` and `CLAUDE.md` contain both
   `<!-- GAME-STUDIOS:BEGIN -->` and `<!-- GAME-STUDIOS:END -->`.
6. **Environment inventory (optional functional extension).** Run
   `bash <skill-dir>/scripts/env_inventory.sh` (add `--no-launch` to keep it
   strictly read-only) and walk the user through the four sections. These
   checks only enrich the setup — the workspace core (scaffold, rules,
   registries, hooks marker) is fully functional without any of them; skip
   freely if the user is not interested.
   - **Game engines** — detects Godot / Unity / Unreal (PATH, program
     directories, drive-root scan, registry). If none are found, recommend
     https://godotengine.org/download (free, open source).
   - **Blender / MCP** — probes the Blender MCP addon socket on
     `127.0.0.1:9876` and the `blender-mcp` bridge CLI. If the socket is down:
     Blender installed but not running → the script launches Blender and
     re-probes; if it is still down (or Blender is not installed at all), tell
     the user that if they need Blender they should follow
     https://www.blender.org/lab/mcp-server/ (Blender 5.1+, add-on + MCP server).
   - **ComfyUI** — discovers the install (`COMFYUI_HOME` → Desktop registry →
     shallow scan, same order as the comfyui-headless skills), then checks
     which of the expected Qwen-Image-2.1 and Pixal3D/TRELLIS.2 weight files
     are actually registered (server API on port 8188 when running, otherwise
     the registered model roots). image21 needs one file per type; pixal3d
     needs all 8.
   - **Open Design** (Windows only) — locates the desktop app (registry
     `InstallLocation`) and reports whether its sidecar pipe is live. The
     plugin's `open-design-windows` MCP server resolves everything at runtime
     via `mcp/opendesign-mcp.sh` (install dir + a live `open-design-sidecar-*`
     pipe) — **Windows only: auto-discovery uses the Windows registry and
     Windows named pipes.** On macOS/Linux this server is not provided
     automatically; tell the user to configure the open-design MCP server
     manually instead (the app can generate its MCP registration) — official
     site and downloads: https://open-design.ai .
7. **Next steps**: `/game-studios:setup-engine` (engine choice) or the full
   onboarding flow (`game-studios:start`).

## Notes

- Brownfield projects: run the script first (it only fills gaps), then
  `game-studios:adopt` for format compliance and migration planning.
- The plugin repo itself is never modified; the workspace owns everything
  created. Refusing to run inside the plugin repo is built into the script.
