---
name: readme-writer
description: Use when writing a README, improving or rewriting an existing README.md, documenting a project for new users or contributors, or preparing a repository to be published or open-sourced.
---

# README Writer

## Overview

A README answers, in order: what is this, why should I care, how do I run it in five minutes, and where do I go next. Every fact comes from the codebase. Nothing is invented.

## Method

1. **Collect facts from the code** before writing a word:
   - Manifests: `package.json`, `pyproject.toml`, `pom.xml`, `go.mod`, `Cargo.toml` — name, description, scripts, engines/versions.
   - Entry points, CLI flags (`--help` output if runnable), exported API.
   - Configuration: `.env.example`, config files, required environment variables.
   - Setup steps hidden in scripts, Dockerfiles, Makefiles and CI workflows.
   - License file, contributing guide, existing docs.
2. **Verify every command** you will document exists (script name, binary, flag). Do not document `npm run dev` unless the script is there.
3. **Pick the audience:** users of a library or CLI, operators of a service, or contributors. Lead with what that audience needs.
4. **Write** using [template.md](template.md). Drop sections that have no real content.
5. **Mark unknowns.** If a fact cannot be found (deployment URL, support channel), leave a clearly marked `TODO:` or ask; never guess.

## Rules

| Rule | Why |
|---|---|
| First two lines say what it is and who it is for | Readers decide in seconds |
| Quickstart works copy-paste on a clean machine | Prerequisites and versions listed first |
| Show one real usage example with real output | Examples beat feature lists |
| Configuration table: variable, required, default, description | Most setup failures are config |
| No badges, links, screenshots or features that do not exist | Broken trust is hard to win back |
| Keep it short; link to `docs/` for depth | Long READMEs are skimmed, not read |

When improving an existing README, keep correct content, fix what is wrong or stale, and list the changes you made.

## Common mistakes

- Generic filler ("This project is a powerful, scalable solution...").
- Install steps that skip a required environment variable or service (database, API key).
- Documenting scripts or flags that were renamed or never existed.
- Copying the whole API reference into the README.
- Wrong license name compared with the LICENSE file.

---

Made by **Wageesha Tripathi** · [LinkedIn](https://www.linkedin.com/in/wst2002/) · [Email](mailto:tripathiwageesha2002@gmail.com) · [More skills](https://github.com/WST2002/claude-code-skills)
