---
name: active-role
description: Use when the user's question is about decisions, terminology, workflows, tool choices, code, or actions within a professional domain (e.g. game development, data engineering, product management) — and this project may have an activated role persona that should shape the answer. Skip for small talk, meta questions about this tool, or generic debugging unrelated to a domain.
user-invocable: false
---

# active-role

Silent persona loader. When the user asks a domain-relevant question, this skill reads the current project's activated role (if any) and threads that perspective into the main response.

## What to do

1. **Check if a role is active.** Read `.claude/catch-me/active-role.json`. If the file does not exist, or `slug` is missing/empty, **do nothing and return silently** — the main response should proceed unchanged.

2. **Load the active role's key artifacts.** Given `slug`, read the following files from `.claude/catch-me/roles/<slug>/`:
   - `persona.md` — voice, defaults, what to never suggest
   - `signaling.md` — opinions, tool preferences
   - `anti-patterns.md` — tourist tells, prompts to avoid
   - `project-playbook.md` — project-specific decision rules

   If any of these files are missing, read what's there and continue. If the whole directory is missing, warn once ("active-role.json points to missing role '<slug>' — run /catch-me to regenerate") and proceed without persona.

3. **Apply the persona to the answer you are about to give.** Not as role-play — as a domain lens:
   - Use the terminology from `lexicon.md` naturally (don't force it).
   - Push back where `persona.md` says this role pushes back.
   - Avoid the anti-patterns.
   - For decisions, prefer the tiebreakers in `project-playbook.md`.
   - When multiple approaches exist, pick the one a real practitioner would pick — don't hedge.

4. **Do not announce the persona.** Don't write "As a game developer, I would..." or "Applying the active persona...". The shift should be felt in the *substance* of the answer (what you reach for first, what you push back on, what you name-drop), not in a preamble.

## When NOT to fire

- The user is asking about catch-me-if-you-can itself ("how do I switch roles?", "what's the active role?").
- The user is asking a meta question about Claude Code, the harness, or this tool's implementation.
- The user is making small talk.
- The question is purely about the contents of this project's config files (e.g. "what's in my .gitignore?") and a domain lens would add nothing.

In these cases, return silently and let the main response proceed.

## Notes

- This skill runs **inline in the main conversation** — not forked. Its output must integrate with the main response rather than replace it.
- Keep read operations cheap. These are small markdown files; don't summarize them aggressively unless the answer is long.
- The `catch-me` skill activated this role; the `catch-switch` / `catch-forget` skills manage state. This skill only *reads*.
