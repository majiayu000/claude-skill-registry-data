---
name: synapse
description: Codex-led multi-model workflow (Codex + Claude + Gemini). Use when the user asks to run `synapse <cmd> ...` to generate draft diffs/audits and persist artifacts to `./.synapse/**`.
---

# Synapse (Codex Skill)

Synapse is a **project-local workflow runner** driven by **Codex (main controller)**.

## Models (roles)

- **Codex (main controller)**: decides routing, writes prompts, applies final code, runs verification, and delivers
- **Claude**: planning/architecture/risks + backend draft diffs + general code audit
- **Gemini**: frontend/UI draft diffs + UI/UX + accessibility audit (only when `task_type` includes frontend)

Artifacts are written under `./.synapse/**` in the *target project root*.

## Hard rules (must follow)

- Only handle requests that start with `synapse <cmd> ...` (no slash commands).
- Before running anything: open `references/<cmd>.md` and summarize (purpose, usage, models, writes/side effects, and any safety/confirmation requirements).
- If any **script-level** CLI args are unclear (`init/pack/plan/run/verify/ui`), run `synapse.py <cmd> --help` (via `uv`) and follow the output.
- Run Synapse scripts via `uv`:

```powershell
uv run --no-project python <SKILL_DIR>/scripts/synapse.py --project-dir <PROJECT_DIR> <cmd> ...
```

- Treat any external diff as a **draft**. Do **not** apply verbatim; Codex rewrites to production quality.
- Prompts are **not hardcoded in scripts**. Codex must generate prompts and pass them via `synapse run --prompt-file ...`.
- `workflow`/`feat` are end-to-end (Codex-orchestrated) meta commands. Treat `references/workflow.md` as the source of truth for the exact steps and Gate requirements (including `gate_prep` + single-round Gate).
- `task_type` rules:
  - If the user explicitly sets `--task-type`, respect it.
  - If omitted: default to `fullstack` (info-complete; higher cost) and still present `frontend/backend/fullstack` options + Codex recommendation at the Gate.
- Git safety:
  - Prefer a clean working tree. If it's dirty, surface it at the Gate and ask how to proceed (stash/commit/abort).
  - If the project is not a git repo, propose `git init` at the Gate (review quality is best with git).

## Global flags (common)

- `--project-dir <dir>`: directory inside the target project (default: `.`)
- `--resume-gemini <SESSION_ID>` / `--resume-claude <SESSION_ID>`
- `--resume <SESSION_ID>`: alias for `--resume-gemini` (back-compat)
  - If both `--resume` and `--resume-gemini` are provided with different values, Synapse errors to avoid silent confusion.

## Command map

User-level commands (typed in Codex chat):

- `workflow`, `feat`

Script-level subcommands (Codex runs via `uv`):

- `init`, `pack`, `plan`, `run`, `verify`, `ui`

## Script guarantees

- Project root detection: `git rev-parse --show-toplevel` (fallback: current directory).
- Artifacts always go under `./.synapse/**` (plans/context/logs/patches/state/index).
- Writes are guarded by `assets/defaults.json:safety.allowed_write_roots` (hard fail if a write would escape these roots).
- `init` only writes: `AGENTS.md`, `.gitignore`, `./.synapse/**` (idempotent).
- `verify` may create **project-local toolchain artifacts** (lockfiles, `.venv/`, `node_modules/`, build outputs) as a side effect.
- External model calls use local `claude` + `gemini` CLIs in stream-json mode (`session_id` captured; resume supported). Synapse never enables “auto-approve” modes (Gemini runs with `--approval-mode default`; Claude runs with `--permission-mode plan --tools "" --strict-mcp-config`).
- `ui` starts a local read-only web viewer for `.synapse/**` (prompts/outputs/patches/logs/state).
