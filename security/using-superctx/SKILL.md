---
name: using-superctx
description: Use when entering a repository with a .ctx/ hub, or when the user asks about project context, agent instructions, tool configuration, health, candidates, broken shims, repair, or cross-tool context.
---

# SuperCtx Reference Guide (Agent Reference / Advanced)

This is an agent reference and advanced skill. Normal users do not need to run this; the agent uses it automatically to orient itself on how to interact with the project-local SuperCtx context hub.

## When to Use

Use this skill whenever:
- A `.ctx/` directory exists in the project root.
- The user asks about project context, agent instructions, or tool configuration.
- The user asks about sync, health, candidates, broken shims, or cross-tool context.
- The user asks to update or apply context changes across agents.

## Core Model

SuperCtx provides a central project-local context layer using a hub-and-shim model:

- **`.ctx/SUPERCTX.md`** is the canonical project context hub.
- **Tool-specific instruction files** (e.g. `.claude/CLAUDE.md`, `.codex/AGENTS.md`) are generated shims/adapters pointing to the hub.
- **`.ctx/sources/`** contains inactive recovery copies of original instruction files.

## Edit Policy

When updating shared project context, the agent edits `.ctx/SUPERCTX.md` directly. The other managed files are not authoring surfaces.

| File | Policy |
| --- | --- |
| `.ctx/SUPERCTX.md` | Author here. Canonical editable hub. Edit it to update shared project context. `/superctx:sync` preserves these edits. |
| Tool files (`.claude/CLAUDE.md`, `.codex/AGENTS.md`, `.agy/ANTIGRAVITY.md`, …) | Generated shims. Do not edit. Edit `.ctx/SUPERCTX.md` instead. |
| `.ctx/sources/**` | Backup only. Do not read, import, or edit as active context. Not live context. |

## Agent Rules

1. **Stay quiet about internals.** Do not explain hub/shim/backup mechanics unless the user asks. Use SuperCtx context naturally without announcing how it works.
2. **Announce SuperCtx interactions.** When SuperCtx is relevant or actively shaping the work, announce in one short sentence before taking action:
   `Using SuperCtx to <purpose>.`
   Keep the announcement task-specific.
3. **Do NOT ask users to manually edit `manifest.toml` or `SUPERCTX.md`, or manually run `/superctx:sync` or `/superctx:add` as the happy path unless they explicitly ask for commands.** Prefer agent action and internal command execution. If `/superctx:sync` reports setup, add, repair, or migration opportunities, offer the action in natural language and ask for consent.
4. **Avoid saying "sync context" unless actually running `/superctx:sync`.**
5. **Do NOT read, import, or edit `.ctx/sources/**` as active context.** `.ctx/sources/` contains inactive recovery copies of original pre-SuperCtx files. These files are for recovery and audit only, not canonical editable context. When updating project context, edit `.ctx/SUPERCTX.md`.
6. **Do NOT edit generated shims as the source of truth.** Tool-specific files are thin generated pointers to `.ctx/SUPERCTX.md`.
7. **Use `/superctx:sync` for convergence.** It handles initialization, health checks, and repairs.
8. **Offer agent-guided setup with explicit user consent when relevant.** If a candidate repository is detected (no `.ctx/` folder but candidate files exist), do not run `/superctx:sync` or mutate files without the user's explicit natural-language consent. Present the detected files, explain what setup will do, and ask for confirmation. Use this exact consent prompt:
   > Using SuperCtx, I can set up one shared context hub for this repo.
   >
   > This will:
   > - create `.ctx/SUPERCTX.md`
   > - back up the original instruction files under `.ctx/sources/`
   > - replace the live instruction files with generated shims pointing to the hub
   >
   > Proceed?

   Once the user confirms, run `/superctx:sync`. If the user declines, leave the repo unchanged.
9. **Guide legacy or broken setups to repair/migration/inspection.**
   - If `/superctx:sync` reports `managed_needs_repair` and the recommended action is `repair`, offer to repair the broken or missing shims and run `/superctx:sync` internally after getting consent.
   - If it reports `inspect` (due to missing or invalid manifest), explain the problem clearly and do not run `sync` or `init`.
   - If it reports `legacy` layout, explain the situation clearly, warning that migration/recovery is required. Preserve existing instruction contents and use explicit user-approved migration steps.
   Never run `/superctx:sync` or mutate files on a legacy/inspect state without explicit user consent.

### Action Cues (Before Action)

Announce these cues *before* starting the corresponding action or command. Replace `<path>` with the actual file path.

| Situation | Phrase |
| --- | --- |
| Updating instructions | `Using SuperCtx to update the shared project context across connected agents.` |
| Syncing/Checking health | `Using SuperCtx to synchronize and verify project context.` |
| Adding a local file | `Using SuperCtx to connect <path> as a local context file.` |
| Offering setup | `Using SuperCtx to offer project context management setup.` |

### Result Confirmation Phrases (After Action)

Use these phrases to report successful execution when the command output is healthy.

| Situation | Phrase |
| --- | --- |
| Healthy result | `All SuperCtx context links are healthy.` |

## Command Guide

- `/superctx:sync`: Global setup, check, repair, and report command.
- `/superctx:add <path>`: Tracks a local custom candidate file.
- `/using-superctx`: Agent-facing reference skill.

## Example Workflows

### Workflow 1: Updating project instructions
- **User:** "Update the project instructions to include Y."
- **Agent Action:** Update `.ctx/SUPERCTX.md`, then run `/superctx:sync` to verify that registered shims are still healthy.

### Workflow 2: Checking context for a specific tool
- **User:** "What context does Codex have?"
- **Agent Action:** Inspect the registered Codex shim, then read `.ctx/SUPERCTX.md` as the canonical project context. If freshness matters, run `/superctx:sync`.

### Workflow 3: Checking connection and health
- **User:** "Is everything connected?"
- **Agent Action:** Run `/superctx:sync`.

### Workflow 4: Repairing generated shims
- **User:** "The Codex instruction file is missing."
- **Agent Action:** Run `/superctx:sync`. If the registered shim is missing or broken, explain the issue and offer to repair the shims. Once the user gives consent, run `/superctx:sync` internally.

### Workflow 5: Tracking a new instruction file
- **User:** "I added a new tool instruction file at .agy/ANTIGRAVITY.md."
- **Agent Action:** Explain that you can connect the new instruction file to the shared context hub, and offer to do so. Once the user gives consent, run `/superctx:add .agy/ANTIGRAVITY.md` internally.

### Workflow 6: Agent-guided setup in a candidate repo
- **Context:** Session starts; hook reports `candidate_repo` with detected files `.claude/CLAUDE.md` and `.codex/AGENTS.md`.
- **Agent Action:** Present the detected files and make the consent-based offer (see Rule 8). Do not run `/superctx:sync` yet.
- **User:** "Yes, go ahead."
- **Agent Action:** Announce `Using SuperCtx to set up the shared project context for this repo.`, then run `/superctx:sync`. Report the result concisely.
