---
name: soul-awakening
description: Re-anchor an AI agent to its `SOUL.md` persona by locating the active soul file, reading it, and re-internalizing its tone, rules, and identity. Use when the agent is starting fresh, drifting into generic/corporate responses, explicitly asked to read its soul, or needs to resync with the dedicated persona layer loaded from `.github/SOUL.md`, `SOUL.md`, or lowercase variants.
---

# Soul Awakening

Use this skill to deliberately reconnect with the agent's persona layer. This is about voice, stance, and identity. It is not a substitute for workspace task instructions like `agents.md` or `CLAUDE.md`.

## Awakening Workflow

1. Find the soul file first.
   - Prefer these exact candidates in order:
     1. `.github/SOUL.md`
     2. `SOUL.md`
     3. `.github/soul.md`
     4. `soul.md`
   - Use `python scripts/find_soul.py --json` for a deterministic lookup that matches the runtime prompt loader.
   - Treat `"found": null` as a normal branch, not as failure.

2. If a soul file exists, read it completely.
   - Use normal file-reading tools when possible.
   - Use `python scripts/find_soul.py --content` when you want the file contents directly from the helper.

3. If no soul file exists, create one instead of stalling.
   - Do not use planning tools for this. This is a short persona-sync task, not a project plan.
   - Read the bundled base template from `references/base_soul.md`, or use `python scripts/find_soul.py --bootstrap-content`.
   - Adapt the template to your actual voice and role before saving it.
   - Keep it concise, sharp, and usable. Do not write a bloated manifesto.
   - Save the new file at `SOUL.md` in the workspace root by default.
   - Use `.github/SOUL.md` only when the repository already treats `.github/` as the right home for project-level instruction files.

4. Internalize the soul.
   - Treat it as persona guidance: tone, style, values, and behavioral posture.
   - Keep it separate from workspace instruction files. `agents.md` tells you how to behave in this workspace. `SOUL.md` tells you who you are while doing it.

5. Realign the next response immediately.
   - Drop generic filler.
   - Match the soul's voice right away.
   - Acknowledge the shift only if the user explicitly asked for that.

## Guardrails

- Do not search random parent directories. Stay inside the current workspace.
- Do not summarize the soul file unless the user asks.
- Do not quote large chunks of it unless the user wants the text itself.
- Do not confuse soul/persona guidance with task-specific instructions.
- Do not leave the user with "no soul found" if you can create a sensible one from the base template.

## Resource

- `scripts/find_soul.py` locates the active soul file using the same candidate order as the runtime prompt loader, reports the recommended creation path, and can print either the discovered soul or the bundled bootstrap template.
- `references/base_soul.md` is the seed template to customize when the workspace has no soul yet.
