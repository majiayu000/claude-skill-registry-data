---
name: simple-readme
description: >-
  Create or update a project README in a developer-focused layout: Requirements,
  Quick Setup, and Structure. Use when the user asks to write, create, update,
  or refresh a README, or mentions simple-readme.
metadata:
  author: denniemok
  version: "1.0.0"
license: MIT
---

# Simple README

Write a practical, scannable README for developers cloning the repo, not a marketing page. Direct and neutral, short paragraphs, bullets and tables over walls of text. No emojis unless the project already uses them.

## Required sections

Every README has these three, in this order, with a short intro before them:

1. Requirements: runtime, services, and external dependencies
2. Quick Setup: install, env, run (dev and prod when applicable)
3. Structure: ASCII folder tree with short comments on key paths

Everything else is optional. Add an optional section only when it helps someone run, deploy, or integrate the project. Skip it if there is nothing substantive to say.

See [template.md](template.md) for the skeleton.

## Workflow

1. Mode: no README means write from scratch. If one exists, update in place, keep accurate content, and align it to this format. If the user gives a section list, follow it and still include the three required sections.
2. Gather facts. Read the repo before writing and never invent ports, env vars, or commands.

   | Source | Extract |
   |--------|---------|
   | `package.json`, `pyproject.toml`, `requirements.txt` | Scripts, runtime version, framework |
   | `.env.example` | Env var names, defaults, required or optional |
   | `docker-compose.yml`, `Dockerfile` | Docker steps |
   | SQL setup files, migrations | Database step |
   | Entry files, `src/` layout | Structure tree |
   | Existing README | Unique content worth keeping |

3. Optional sections. Ask the user which to include when several could apply, such as Scripts, Deployment, Security, Logging, Integration, Routes. Skip the question if the request already says. Include these without asking when the file exists: `.env.example` (env table), `docker-compose.yml` (Docker step), SQL setup file (Database step).
4. Draft from the template, then verify:
   - Requirements list real dependencies only
   - Commands match the project's scripts
   - Env table matches `.env.example`
   - Structure tree matches the actual folders
   - No placeholder text left

## Section notes

- Intro: 1 to 3 sentences on what it does, the stack, and key external services or sibling repos.
- Requirements: bullets, with optional integrations marked optional.
- Quick Setup: numbered `###` steps. Use exact commands, and note non-default ports and build-time env vars.
- Env table: columns Variable, Required, Description.
- Structure: repo root name, comment important paths inline, do not list every file. Add a small table for folder conventions if the layout is not obvious.
- Optional sections go before Structure.

## Updating an existing README

- Keep accurate URLs, license, warnings, and integration notes.
- Replace outdated commands and env vars using the repo as the source of truth.
- If it is a public marketing page (badges, screenshots, disclaimers), ask whether to convert to dev style or only refresh the setup parts.

## Avoid

- Generic filler like "a modern, scalable solution"
- Commands that are not in the project
- Full API docs, link to them instead
- Optional sections with one vague sentence
