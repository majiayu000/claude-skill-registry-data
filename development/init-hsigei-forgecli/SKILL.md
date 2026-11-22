---
name: init
description: Study this project and write a FORGE.md with how to build, run and test it, its structure and conventions
---
# Init: write FORGE.md

Forge reads FORGE.md (or CLAUDE.md / AGENTS.md) from the project folder into every conversation,
so this file should hold what a new teammate needs and can't guess quickly.

1. Look around: list_dir the root, read the README, package files (package.json, pyproject.toml,
   requirements.txt, Cargo.toml, go.mod…), CI config, and a couple of central source files.
2. Find the real commands: install, run/dev server, build, test, lint, format. Prefer ones you saw in
   config files or scripts; run the test command once if it's quick, to confirm it works.
3. Write FORGE.md (if CLAUDE.md or AGENTS.md exists, update that instead) with short sections:
   - Commands (copy-pasteable)
   - Layout: the main folders and what lives in each, in a few lines
   - Conventions you saw: code style, naming, how errors are handled, where tests go
   - Gotchas: anything surprising (env vars needed, generated files not to edit, slow steps)
4. Keep it under ~80 lines. No generic advice ("write clean code") — only things specific to this project.
