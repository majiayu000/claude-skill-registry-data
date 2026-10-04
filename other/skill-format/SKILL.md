---
name: skill-format
description: skill-format
---

# skill-format

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **skill-format**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/_RECENT-PROJECTS/ai-systems/clawhub-main/docs/skill-format.md`

## 🧠 Master Agent Prompt & Capabilities

---
summary: 'Skill folder format, required files, allowed file types, limits.'
read_when:
  - Publishing skills
  - Debugging publish/sync failures
---

# Skill format

## On disk

A skill is a folder.

Required:

- `SKILL.md` (or `skill.md`)

Optional:

- any supporting *text-based* files (see “Allowed files”)
- `.clawhubignore` (ignore patterns for publish/sync, legacy `.clawdhubignore`)
- `.gitignore` (also honored)

Local install metadata (written by the CLI):

- `<skill>/.clawhub/origin.json` (legacy `.clawdhub`)

Workdir install state (written by the CLI):

- `<workdir>/.clawhub/lock.json` (legacy `.clawdhub`)

## `SKILL.md`

- Markdown with optional YAML frontmatter.
- The server extracts metadata from frontmatter during publish.
- `description` is used as the skill summary in the UI/search.

## Allowed files

Only “text-based” files are accepted by publish.

- Extension allowlist is in `packages/schema/src/textFiles.ts` (`TEXT_FILE_EXTENSIONS`).
- Content types starting with `text/` are treated as text; plus a small allowlist (JSON/YAML/TOML/JS/TS/Markdown/SVG).

Limits (server-side):

- Total bundle size: 50MB.
- Embedding text includes `SKILL.md` + up to ~40 non-`.md` files (best-effort cap).

## Slugs

- Derived from folder name by default.
- Must be lowercase and URL-safe: `^[a-z0-9][a-z0-9-]*$`.

## Versioning + tags

- Each publish creates a new version (semver).
- Tags are string pointers to a version; `latest` is commonly used.

