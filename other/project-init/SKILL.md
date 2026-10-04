---
name: project-init
description: Scaffold this project's Claude Code setup — a lean CLAUDE.md, AGENTS.md interop, path-scoped rules for the languages actually in use, and gitignore entries. Invoke explicitly when setting up a repo for the first time.
argument-hint: [optional languages to scope rules to]
disable-model-invocation: true
---

Set up this project's `.claude/` from the preflight templates: $ARGUMENTS

Templates live under `${CLAUDE_PLUGIN_ROOT}/templates/`. Never write state into the plugin directory — it's replaced on every plugin update.

## 1. Look before you write

Detect what's already here: `CLAUDE.md`, `AGENTS.md`, `.claude/`, existing rules, `.gitignore`.

**Never overwrite a file that already exists.** If a target exists, read it, then propose a merge and let the human decide. Clobbering someone's hand-written CLAUDE.md is the worst thing this skill could do.

Detect the real stack from the repo — `package.json`, `pyproject.toml`, `Cargo.toml`, actual source extensions. Install rules for languages the project *uses*. A Rust rule file in a pure TypeScript repo is dead weight that loads on a glob that never matches.

## 2. CLAUDE.md and AGENTS.md interop

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. Which file holds the content depends on what's already there:

**No AGENTS.md yet** — copy `templates/CLAUDE.md.template` to `CLAUDE.md`, then point AGENTS.md at it so other tools read the same conventions:

```bash
ln -s CLAUDE.md AGENTS.md
```

**AGENTS.md already exists** — it's the source of truth. Don't duplicate it. Create a `CLAUDE.md` that imports it, with any Claude-specific notes below:

```markdown
@AGENTS.md
```

On Windows, symlinks need Administrator or Developer Mode. If linking fails, use the import form instead — it's portable and it's the docs' primary recommendation.

## 3. Rules

Copy the matching files from `templates/rules/` into `.claude/rules/`. Each carries `paths:` frontmatter so it loads only when Claude reads a matching file, keeping per-language conventions out of always-on context.

Always include `git.md` — it has no `paths:` and applies everywhere.

## 4. Settings and gitignore

Copy `templates/settings.json.template` to `.claude/settings.json` if absent. It's permissions only — no secrets, ever.

Append `templates/gitignore.snippet` to `.gitignore` if those entries aren't already there. Check before appending; don't duplicate lines.

## 5. Fill in what only a human knows

Read the codebase and fill in what you can verify: real build and test commands, actual directory layout. Leave `TODO` markers for what you can't — and tell the human exactly which ones to fill.

Delete every placeholder you didn't fill. A template comment shipped as-is is context cost with no payload.

## 6. Report

Print what you created, what you skipped and why, and the specific TODOs left. Keep it to a few lines.

Then check the result against the standard: **is CLAUDE.md still under a screen?** If it isn't, cut it now. Every line loads in every session, and adherence degrades as the file grows. Anything path-specific belongs in a rule; any procedure belongs in a skill; anything a linter enforces belongs in a hook.
