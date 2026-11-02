---
name: template-skills
description: "Use at the start of any task in this repository, and whenever a row in the AGENTS.md \"How we build\" table matches what you are about to do. This repository keeps its skills in .claude/skills/ (SKILL.md folders for feature design, web, iOS, macOS, tvOS, Android, Windows, TV platforms, CI, store submission and device testing). This skill is the pointer to them: it says how to find and load the right one."
---

# The skills live in `.claude/skills/`

This repository keeps one copy of its skills, in `.claude/skills/`, so
they never drift apart. This folder exists only so that agents that
look in `.agents/skills/` (Gemini CLI, Antigravity) can find them.

The three skills a learner asks for by name
(`learning-orientation-design`, `make-it-look-like-itself`, and
`human-shaped-review`) are linked here, so they load on their own. For
every other skill:

1. Read the "How we build" table in `AGENTS.md`. Each row names the
   skill to use for a situation.
2. Open `.claude/skills/<skill-name>/SKILL.md` and follow it as you
   would any skill. Read its `references/` files when it points to them.
3. When no row matches, scan `.claude/skills/README.md`, the catalog
   of every skill with what it is for.

Do not copy skills into this folder. Add or change them in
`.claude/skills/` and add a trigger row in `AGENTS.md`. A link here
(`ln -s ../../.claude/skills/<name> .agents/skills/<name>`) is for a
skill a stage asks a learner to call by name, and
`tools/test_agent_files.py` checks that every link resolves.
