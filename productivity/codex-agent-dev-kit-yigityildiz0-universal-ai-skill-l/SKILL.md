---
name: codex-agent-dev-kit
description: Convert Claude Code agent-kit setups into Codex-compatible skills, project instructions, guardrail scripts, command workflows, subagent guidance.
---

# Codex Agent Dev Kit

Use this skill to translate Claude-oriented agent setup material into Codex-native files. Do not copy `.claude` files verbatim unless the user explicitly wants archival copies; map each concept to a Codex-supported artifact.

## Default Targets

- Global reusable skill: `%USERPROFILE%\.codex\skills\<skill-name>\SKILL.md`
- Project memory and conventions: `<repo>\AGENTS.md`
- Repo-local plugin bundle: `<repo>\plugins\<plugin-name>\.codex-plugin\plugin.json`
- Plugin marketplace entry: `<repo>\.agents\plugins\marketplace.json`
- Deterministic guardrails: helper scripts under a skill or plugin `scripts/` folder

## Migration Workflow

1. Inventory the source material.
- Identify Claude concepts: `CLAUDE.md`, `.claude/commands`, `.claude/hooks`, `.claude/rules`, `.claude/agents`, `.claude/settings.json`, plugin manifests, and screenshots.
- Separate reusable behavior from repo-specific conventions.

2. Choose the Codex destination.
- Put reusable workflows in a global Codex skill.
- Put repo architecture, commands, test expectations, naming, and local conventions in `AGENTS.md`.
- Put shareable bundles in a local Codex plugin only when the user needs plugin UI discovery or team distribution.
- Put ongoing skill maintenance behavior in `skill-updater` rather than mixing health checks into every skill.

3. Translate, do not clone.
- `CLAUDE.md` memory becomes `AGENTS.md` or skill instructions.
- Claude slash commands become named workflow sections, default prompts, or executable scripts.
- Claude hooks become explicit guardrail scripts and preflight checks; a skill cannot enforce every tool call by itself.
- Claude rules become `AGENTS.md` project rules or skill body guidance.
- Claude agents/subagents become delegation guidance. Codex subagents are used only when the user explicitly asks for delegation or parallel agent work.
- Claude `settings.json` permissions and model values do not port directly. Do not weaken Codex safety settings during migration.
- Claude plugins become Codex plugins with `.codex-plugin/plugin.json`, `skills`, optional assets/scripts, and a marketplace entry.

4. Validate the result.
- Run the Codex skill validator for every skill folder.
- Validate plugin JSON, marketplace JSON, and relative paths.
- Run bundled guardrail scripts with a harmless target before relying on them.

## Reference Files

- Read `references/claude-to-codex-map.md` when converting screenshots or `.claude` folders.
- Read `references/codex-plugin-layout.md` when creating or fixing a Codex local plugin package.
- Use `$skill-updater` after migration when a generated skill fails, becomes stale, references old models, or needs a health audit.

## Guardrails

- Never import Claude permission allowlists as Codex permissions without reviewing each entry.
- Do not add destructive commands, force-push workflows, or hidden automatic commits.
- Prefer small, explicit scripts over broad "run everything" automation.
- Keep skill frontmatter to `name` and `description`; Codex uses those fields for triggering.
- Keep `agents/openai.yaml` UI metadata short and synchronized with `SKILL.md`.

## Verification Helper

Use `scripts/check_codex_agent_kit.ps1` to check that a skill or plugin bundle has the expected Codex files.

## Changelog
- [2026-05-08] [HEALTH] Added skill-updater routing so migrated skills can be maintained through failure-driven and usage-based updates.
