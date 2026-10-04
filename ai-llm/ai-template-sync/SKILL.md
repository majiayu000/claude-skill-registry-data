---
name: ai-template-sync
description: UPSERT the smooth-ai-stockanalysis agentic scaffold into an existing repo. Asks which tools (Claude Code, Codex, Copilot) to configure, whether to copy .NET solutioning, and whether to overwrite existing agentic files.
allowed-tools:
  - Bash(.agents/skills/ai-template-sync/scripts/sync.sh:*)
  - Bash(git clone:*)
  - Bash(mktemp:*)
  - Bash(bash:*)
  - Bash(rm:*)
models:
  claude: opus      # high-complexity; interactive multi-turn Q&A + conditional file sync across tools
  copilot: auto
  codex: gpt-5.5
---

# AI Template Sync — Skill

Sync the **smooth-ai-stockanalysis** agentic scaffold into a landing repo (UPSERT — safe merge, not destructive replace).

## TL;DR

0. If the template isn't checked out locally (running as a skill via web / hosted agent), clone it to a temp dir first.
1. Ask which AI tools to configure.
2. Optionally copy .NET solutioning.
3. Pre-flight: if `.agents/rules` isn't a symlink to `.github/instructions`, ask whether to move the rules.
4. Detect conflicts; ask for overwrite scope.
5. Copy files per tool selection.

---

## Phase 0 — Acquire Template (remote / web runs)

**Run this ONLY when the template repo is not already checked out at the current location** —
i.e. the skill is invoked as a *landing-repo* skill (web / hosted agent / a repo that doesn't
contain the template). If you are already inside a checkout of the template repo, skip Phase 0
and let `--template` default to the current git toplevel.

The sync scripts copy **from** the template tree (`.agents/`, `.github/instructions/`,
`copilot-instructions.md`, optional `src/`/`tests/`). None of that lives under the skill folder,
so pulling just the skill is **not** enough. The script self-acquires the whole template: pass
`--template-url <git-url>` (`-TemplateUrl` on Windows) instead of `--template` and it shallow-clones
to a temp dir and cleans up on exit. Add `--template-ref <tag|sha>` to pin for reproducibility.

```bash
bash sync.sh --template-url https://github.com/generic-automation-and-it/smooth-ai-stockanalysis \
  --landing "$PWD" --tools <claude,codex,copilot> --overwrite <global|none> [--dotnet]
```

Caveats (one line): the runner needs **Bash + git + network**; a **private** template needs
`gh`-auth or a token embedded in the clone URL.

> The interactive phases below (1–3) still apply — gather intent and run the pre-flight before
> invoking the cloned script. Phase 0 only solves *getting the files*, not the decisions.

---

## Phase 1 — Gather Intent (ask, then stop for answers)

Ask the user all questions in **one message**:

```
1. Which AI tools to configure? (comma-separate any combo)
   a) Claude Code   b) OpenAI Codex   c) GitHub Copilot

2. Copy .NET solutioning? (only asked if the landing repo has no *.slnx / *.sln)
   Includes: smooth-ai-stockanalysis.slnx · Directory.Build.props · Directory.Packages.props
             NuGet.Config · src/ · tests/
   [y/n]

3. Overwrite mode for agentic files?
   A) Global overwrite — replace every agentic file without further prompting
   B) Selective — show me a conflict table first; I'll pick what to overwrite
   (Dotnet files are never overwritten regardless of choice.)
```

Wait for user answers before proceeding.

---

## Phase 2 — Rules-Layout Pre-flight (ALWAYS run, even in Global mode)

The template's contract is: **`.github/instructions/` is the real directory** that holds the rule files, and **`.agents/rules` is a symlink pointing to it**. A landing repo may not follow this — it may keep `.agents/rules` as a real directory of its own rules, or symlinked somewhere else.

This matters because Section D of the sync (`scripts/sync.sh`) **unconditionally** runs `rm -rf .agents/rules` and re-points the symlink — in *both* overwrite modes. If `.agents/rules` is a real directory, that step **destroys the repo's own rules**. So this check runs regardless of the Phase 1 overwrite choice, and only when `copilot` is among the selected tools (Section D runs only then).

Inspect the landing repo:

```bash
readlink "<LANDING_REPO>/.agents/rules"   # prints ../.github/instructions in a conforming repo; empty/non-zero exit if it's a real dir
```

If `.agents/rules` exists but is **not** a symlink resolving to `.github/instructions` (i.e. it is a real directory, or a symlink pointing elsewhere), **stop and ask** before running the sync:

```
Your repo's `.agents/rules` is NOT a symlink to `.github/instructions`
(it is <a real directory | a symlink to X>).

The template keeps rule files in `.github/instructions/`, with `.agents/rules`
symlinked to it. The sync would otherwise delete `.agents/rules` and re-point it,
losing your existing rules.

Move your existing rules into `.github/instructions/` and re-point
`.agents/rules` at it as part of this update? [y/n]
```

- **y** → before invoking the script, move the existing rule files into `.github/instructions/` (merge, don't clobber the template rules), then let Section D re-point the `.agents/rules` symlink. The repo's own rules are preserved.
- **n** → do **not** run with `copilot` in `--tools` (Section D would still `rm -rf .agents/rules`). Either drop `copilot` from the tools list, or sync the other tools first and handle Copilot's rules dir manually. Leave the existing layout untouched.

If `.agents/rules` already symlinks to `.github/instructions`, or neither path exists, take no action and proceed.

---

## Phase 3 — Conflict Detection (Selective mode only)

Skip if user chose **Global overwrite**.

### Agentic file inventory

| Category | Files / paths |
|----------|--------------|
| Base scaffold | `.agents/**` (all files recursively) · `AGENTS.md` |
| Claude Code | `.claude` (symlink) · `CLAUDE.md` (symlink) · `GEMINI.md` (symlink) |
| Codex | `.codex` (symlink) |
| Copilot | `.github/copilot-instructions.md` · `.github/instructions` (**real directory** — holds the rule files; `.agents/rules` symlinks to it) |
| Setup scripts | `.agents/setup/scripts/agents-setup.sh` · `.agents/setup/scripts/agents-setup.ps1` · `.agents/setup/scripts/agents-terminals.sh` · `.agents/setup/scripts/agents-terminals.ps1` |

Check each file/path against the landing repo. Build a conflict table for every item that **already exists**:

| # | Name | Purpose | Action |
|---|------|---------|--------|
| 1 | `.agents/hooks/load-agents-context.sh` | PostToolUse hook — emits AGENTS.md context | skip |
| … | … | … | … |

Print the table, then ask:

```
Enter IDs to overwrite (e.g. "1 3 5"), "all", or "none":
```

Collect the response before moving to Phase 4.

---

## Phase 4 — Execute Sync

The mechanical copy/symlink work (Sections A–E) is performed by **`scripts/sync.sh`**
(`scripts/sync.ps1` on Windows). You decide the flags from the Phase 1–3 answers; the script
executes them. It is idempotent and supports two overwrite modes — `global` (clobber) and
`none` (additive, never clobber).

> **Never touch dotnet files** (`.slnx`, `.sln`, `Directory.*.props`, `NuGet.Config`, `src/`, `tests/`) during agentic sync, even if the user requests it here. The script's `--dotnet` path only ever *adds* them when no solution exists, and never overwrites.

```bash
.agents/skills/ai-template-sync/scripts/sync.sh \
  --landing <LANDING_REPO> \
  --tools claude,codex,copilot \
  [--dotnet] \
  --overwrite global|none
```

```powershell
.agents/skills/ai-template-sync/scripts/sync.ps1 `
  -Landing <LANDING_REPO> `
  -Tools claude,codex,copilot `
  [-Dotnet] `
  -Overwrite global|none
```

| Flag | Maps to | Notes |
|------|---------|-------|
| `--tools` / `-Tools` | Phase 1 Q1 | Comma-separated subset of `claude,codex,copilot`. Drives Sections B/C/D. |
| `--dotnet` / `-Dotnet` | Phase 1 Q2 | Section E. Skipped automatically if a `.slnx`/`.sln` already exists. |
| `--overwrite global` | Phase 1 Q3 = A | Clobber every agentic file. |
| `--overwrite none` | Phase 1 Q3 = B (after selection) | Additive only — never clobber existing files. |
| `--template` / `-Template` | _(auto)_ | Template repo root; defaults to the current git toplevel. |
| `--template-url` / `-TemplateUrl` | Phase 0 | Git URL of the template; the script shallow-clones it to a temp dir and cleans up on exit. Mutually exclusive with `--template`. Use for remote / web runs. |
| `--template-ref` / `-TemplateRef` | _(optional)_ | Tag/branch/SHA to pin the `--template-url` clone to. Use for reproducible rule installs. |
| `--rules-only` / `-RulesOnly` | _(optional)_ | Sync ONLY the rule system — see Rules-Only Distribution below. |

What each section does (now inside the script):
- **A — `.agents/` base tree**: `rsync` (global = overwrite, none = `--ignore-existing`); never deletes landing-only files.
- **B — Claude Code**: `.claude`→`.agents`, `CLAUDE.md`/`GEMINI.md`→`AGENTS.md` symlinks + `git config core.symlinks true`.
- **C — Codex**: `.codex`→`.agents` symlink.
- **D — Copilot**: copies the real `.github/instructions/` dir, re-points `.agents/rules` symlink at it, copies `copilot-instructions.md`.
- **E — .NET**: copies `Directory.*.props`, `NuGet.Config`, `*.slnx`, `src/`, `tests/` only when absent. **Rename `SmoothAiStockAnalysis.*` → `<ActualProjectName>` afterwards** (the script prints this reminder; the rename itself is the agent's job).

> **Selective overwrite (Phase 1 Q3 = B):** the script handles `global` and `none` only. For true per-file selection, copy the user-approved files manually first, then run the script with `--overwrite none` so it adds the remainder without clobbering anything.

---

## Rules-Only Distribution (`--rules-only`)

Distribute or update the **rule system as a package** — `.github/instructions/` (the real rules dir, shared by Claude/Cursor/Copilot via symlinks) plus the `.agents/rules` symlink — without touching skills, hooks, setup scripts, or dotnet files:

```bash
.agents/skills/ai-template-sync/scripts/sync.sh \
  --template-url https://github.com/generic-automation-and-it/smooth-ai-stockanalysis \
  --template-ref v1.2.0 \
  --landing "$PWD" \
  --rules-only \
  --overwrite global|none
```

Semantics:

- `--overwrite global` updates same-named rule files to the pinned version; `none` only adds missing ones. **Landing-only rule files are never deleted** in either mode (UPSERT) — a consumer's own rules survive updates.
- `--tools` / `--dotnet` are ignored; Phases 1 and 3 don't apply. The Phase 2 rules-layout pre-flight is **built into the script** here: it refuses (exit 65) if `.agents/rules` is a real directory.
- Re-run with a newer `--template-ref` to upgrade — this is the supported way to consume this repo's rules from other repositories.

---

## Phase 5 — Post-Sync Checklist

After all copies/symlinks are done, report:

```
✅ Sync complete. Next steps for the landing repo:

□ Run the setup script once:
    bash .agents/setup/scripts/agents-setup.sh   # Mac/Linux
    pwsh .agents/setup/scripts/agents-setup.ps1  # Windows

□ Update AGENTS.md — replace template placeholder content with real project context.

□ [Claude Code] Verify `.claude/` symlink resolves:  ls -la .claude

□ [Codex] Verify `.codex/` symlink resolves:  ls -la .codex

□ [Copilot] Verify `.github/instructions/` is a real dir and `.agents/rules` symlinks to it:  ls -la .github/instructions .agents/rules

□ [.NET] Rename SmoothAiStockAnalysis.* → <ActualProjectName> everywhere (if .NET was copied).

□ Commit the agentic scaffold with:  git add -A && git commit -m "chore: add smooth-devex agentic scaffold"
```

---

## Guardrails

- **Never overwrite dotnet files** (`.slnx`, `.sln`, `Directory.*.props`, `NuGet.Config`, `src/`, `tests/`) during agentic sync.
- **Never delete** landing-repo files absent from the template.
- **Always confirm** before executing file writes/copies; show the plan first.
- In Selective mode, skip any file not explicitly approved by the user.
- Symlinks require `git config core.symlinks true`; remind the user if the repo was cloned with symlinks off.
