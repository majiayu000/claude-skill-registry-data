---
name: superctx:add
description: Use when the user wants to start tracking a local custom instruction file (like .agy/ANTIGRAVITY.md or .github/copilot-instructions.md) in SuperCtx. Requires a path argument.
---

# SuperCtx Add

Add a local candidate file to the SuperCtx manifest to begin tracking it.

If SuperCtx is not set up yet (no `.ctx/` directory exists), do not run this command first. Use `/superctx:sync` for the global setup/check/repair flow, then use `/superctx:add <path>` for targeted file connection after the shared context hub exists.

If `.ctx/` exists but the configuration manifest is missing or invalid, the command will raise an error with inspect guidance.

## Before Running (Consent Boundary)

1. **Direct User Invocation**: If the user explicitly typed `/superctx:add <path>` or asked you to connect a file, you have consent. Announce the action:
   > Using SuperCtx to connect <path> as a local context file.
2. **Agent-Initiated Flow**: If you detect an untracked candidate file during a task and want to add it, you **MUST** obtain explicit natural-language user consent first. Offer to connect it, explain what it does, and run the command internally only after getting consent.

## Check File Existence First

Before running the add command, check whether the file exists in the project.

**If the file exists:** Run the add command normally:

```bash
PYTHONPATH="${CLAUDE_PLUGIN_ROOT}/scripts" python3 -m superctx add "$ARGUMENTS"
```

**If the file does not exist and is a known standard convention** (e.g. `GEMINI.md`, `.claude/CLAUDE.md`, `.codex/AGENTS.md`, `.github/copilot-instructions.md`):

Explain that the file does not exist yet, and offer to create it as a generated shim:

> I do not see an existing `<path>`. I can create it as a generated shim pointing to `.ctx/SUPERCTX.md`. Proceed?

After the user confirms, run with `--create-shim`:

```bash
PYTHONPATH="${CLAUDE_PLUGIN_ROOT}/scripts" python3 -m superctx add --create-shim "$ARGUMENTS"
```

Do not create any file before receiving the user's explicit consent.

**If the file does not exist and is not a known standard convention:**

Explain clearly that the file must exist before it can be tracked:

> `<path>` does not exist yet. SuperCtx tracks existing instruction files. Please create the file first or let me know if you would like me to create and connect it for you.

## Then report to the user

Present the result printed by the command. On the healthy path, keep the report concise: confirm the file is now connected and that `.ctx/SUPERCTX.md` is the canonical context.
