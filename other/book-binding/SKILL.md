---
name: book-binding
description: Use when creating a new grimoire plugin (a book-of-* book), adding a skill or hook to an existing book, or preparing a book release. Covers the scaffold tool, the layout and frontmatter rules both harnesses accept, validation, and versioning.
metadata:
  plugin: archmage
  kind: authoring
---

# Binding a book

A book is one plugin directory under `plugins/` in the grimoire repository. This skill applies inside a checkout of that repository. If you are not in one, tell the user and stop.

## 1. Scaffold

From the repository root:

```
node tools/grimoire.mjs new-book book-of-<domain> --description "<one sentence>" [--category "<Codex category>"] [--skill <skill-name>]
```

The tool creates `VERSION` (0.1.0), `CHANGELOG.md`, both manifests, a `README.md`, and, with `--skill`, a first skill with its `agents/openai.yaml` sidecar. It then regenerates both marketplace files. Only `archmage` may omit the `book-of-` prefix.

## 2. Write skills

Each skill lives in `skills/<name>/SKILL.md` plus `skills/<name>/agents/openai.yaml`.

- Name the skill after its topic with the shortest name that identifies it (`tdd`, `adr`, `code-review`). A domain term beats a description of it; a gerund (`reviewing-pull-requests`) is fine when a verb is needed. Names are kebab-case, at most 4 words, contain no article (`a`, `an`, `the`), and must be unique across every book; `check` enforces all four.
- Frontmatter may use only `name`, `description`, `metadata`, `license`, `allowed-tools`. Put anything else under `metadata`. `name` must equal the directory name.
- Write the `description` as a trigger: "Use when ..." followed by what the skill does. Both harnesses pick skills by this text.
- Reference helper scripts through the interpreter (`node scripts/x.mjs`), never by bare path.
- Do not link to files in other books or outside the plugin root.
- The sidecar needs `interface.display_name`, `interface.short_description`, and `policy.allow_implicit_invocation` (false for skills the user must invoke explicitly).

## 3. Add a hook (optional)

Put `hooks/hooks.json` at the plugin root and set `"hooks": "./hooks/hooks.json"` in `.codex-plugin/plugin.json`. Use only events both harnesses support (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`, `SubagentStart`, `SubagentStop`, `PreCompact`, `SessionEnd`). Write matchers with Claude's tool names (`Bash`, `Edit|Write`, `Agent`); Codex aliases them. Commands look like `node "${CLAUDE_PLUGIN_ROOT}/scripts/x.mjs"`. Scripts are dependency-free Node 20+, read the JSON payload from stdin, and must exit 0 with no output on any internal failure.

Never add `commands/`, `bin/`, a root `plugin.json`, a symlink, or a `CLAUDE.md` inside the plugin. The checker rejects all of them, each for a harness-compatibility reason listed in `AGENTS.md`.

## 4. Validate

```
node tools/grimoire.mjs check
node tools/run-tests.mjs
claude plugin validate . --strict
```

Fix everything `check` reports before committing. It also regenerates nothing; if it says a marketplace is stale, run `node tools/grimoire.mjs stamp`.

To try the book in a real session, install this checkout into both harnesses from the repository root:

```
node tools/grimoire.mjs dev-install    # first time: swaps marketplace "grimoire" from GitHub to this checkout (asks before deleting Claude plugin data)
node tools/grimoire.mjs dev-refresh    # after every edit: both harnesses copy plugins into a cache, so re-copy
node tools/grimoire.mjs dev-uninstall  # when done: swap back to GitHub
```

Never register a second marketplace name or use `--plugin-dir` beside an installed copy; skills would appear twice and hooks would run twice. In Codex, a changed `hooks/hooks.json` must be trusted again in `/hooks`.

## 5. Release

1. Edit `plugins/<book>/VERSION` to the new semver.
2. Move the `[Unreleased]` notes in `plugins/<book>/CHANGELOG.md` under a `## [<version>] - <date>` heading.
3. Run `node tools/grimoire.mjs stamp <book>` to write the version into both manifests and the marketplaces.
4. Commit and tag `<book>/v<version>`.
