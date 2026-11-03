---
name: check
description: Project Verification & Consistency Checking
version: 2.0.2
---

# AI4L - Project Verification & Consistency Checking

Handles consistency checking for all major files in the repo, including version numbers, item numbering, and overall consistency across files

### [project_files]

- `.claude/skills/er/SKILL.md`
- `.claude/skills/check/SKILL.md`

- `.claude/agents/er-auditor.md`
- `.claude/agents/er-creator.md`
- `.claude/agents/er-fixer.md`
- `.claude/agents/er-combiner.md`

- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `CONTRIBUTING.md`

- `prompts/ER.md`
- `prompts/PERSONA.md`

- `.grok/rules/rules.md`

- `docs/Using-Chat-UI.md`
- `docs/Using-Claude-Desktop.md`
- `docs/Using-CLI-Environments.md`
- `docs/Lessons-Learned.md`
- `docs/Limitations.md`

- `docs/Examples.md`

## Version

* Check all [project_files] version numbers
* Use the version stated in the `VERSION` file in the project root as a reference.
* Make sure that all targets are consistent with it, including the version in the badges.
* Some files do not have badges, just the version in the text. Make sure those are consistent as well.
* If a file has no version, leave it as it is

## Consistency Checking

* Check all target files for consistency and completeness
* Check the numbering of all items and the item count in ER.md
* Also check numbered step lists (`1.`, `2.`, `3.` …) in ER.md, not just `x.y` items
* Test each sequence for gaps and duplicates explicitly — a gap paired with a duplicate passes a count/min/max test

## Environment Configs

`.mcp.json` is the source for MCP servers; `.codex/config.toml`, `.grok/config.toml` and the Claude settings files are hand-maintained. The servers in scope are those AGENTS.md prescribes for the agents; other servers in `.mcp.json` are out of scope.

* For each server in scope, compare command and args in `.codex/config.toml` and `.grok/config.toml` with `.mcp.json`; report a server missing from a TOML and any argument that differs
* Compare the `mcp__*` entries in the allow lists of `.claude/settings.json` and, where present, `.public/.claude/settings.json` with the servers in scope; report a prescribed server that is not allowed
* Run `/sync` into a temporary directory and diff against the committed generated files; report any drift

# Reporting

* If there are any inconsistencies, report them and ask the user if you should fix them.
* Report what was fixed (if anything).
