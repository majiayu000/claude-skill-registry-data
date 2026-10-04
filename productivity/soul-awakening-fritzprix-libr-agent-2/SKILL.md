---
name: soul-awakening
description: Re-anchor an AI agent to its SOUL.md persona by re-internalizing tone, rules, and identity. Use when the agent drifts into generic/corporate responses, is explicitly asked to reconnect with its soul, or needs to bootstrap a missing SOUL.md. SOUL content is already injected into the system prompt as ## Persona Template — do not re-read existing soul files.
---

# Soul Awakening

Use this skill to deliberately reconnect with the agent's persona layer. This is about voice, stance, and identity—not workspace task instructions like `agents.md` or `CLAUDE.md`.

## Runtime context (read first)

The Rust prompt loader already:

1. Searches workspace candidates in order: `.github/SOUL.md` → `SOUL.md` → `.github/soul.md` → `soul.md`
2. Injects the first match into the system prompt as **## Persona Template**

**Do not** run `find_soul.py` or re-read an existing soul file—that duplicates content already in context.

## Awakening Workflow

1. Check whether a soul is already active.
   - Look for **## Persona Template** in the system prompt.
   - If present, skip all file I/O. Proceed to step 3.

2. If no Persona Template section exists, bootstrap one.
   - Do not use planning tools—this is a short persona task, not a project plan.
   - Read `references/base_soul.md` and adapt it to the agent's actual voice and role.
   - Keep it concise, sharp, and usable. Do not write a bloated manifesto.
   - Save at `SOUL.md` (workspace root) by default, or `.github/SOUL.md` if the repository already treats `.github/` as the home for project-level instruction files.
   - **Cache note**: New or edited SOUL.md may not appear in the stable system prompt until the next session resume or config invalidation. Still write the file; realign the next response from the content you just authored.

3. Internalize the persona.
   - Treat it as persona guidance: tone, style, values, and behavioral posture.
   - `SOUL.md` tells you who you are; `agents.md` tells you how to behave in this workspace.

4. Realign the next response immediately.
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

- `references/base_soul.md` — seed template to customize when the workspace has no soul yet.
