---
name: create-plugin
description: "Create or package an installable Claude Code + Codex plugin in this repo: scaffold, manifests, marketplace catalogs, validation. Triggers: create plugin, new plugin, package as a plugin, plugin marketplace, plugin not loading (skill not showing, Codex not finding it)."
---

# Create Plugin

Scaffold, wire, register, and validate an installable plugin that works in
**both Claude Code and Codex** from one source tree. Use the scripts for the
deterministic parts; use the references for the per-runtime spec.

## When NOT to use
- Authoring the SKILL.md *content* → that's `skill-creator`.
- Authoring an agent's *content* → that's `create-subagent`.
- A throwaway/project-local skill that won't be distributed → just put it in
  `.claude/skills/` and skip everything here (it is not a plugin).

## Component support at a glance

| Component | Claude Code | Codex | Where it lives |
|---|---|---|---|
| Skill | ✅ | ✅ | `skills/<name>/SKILL.md` |
| Agents / subagents | ✅ plugin agents | ❌ (standalone TOML only) | `agents/*.md` |
| MCP servers | ✅ | ✅ | `.mcp.json` |
| Hooks | ✅ | ✅ | `hooks/hooks.json` |
| Slash commands | ✅ | ⚠️ verify | `commands/*.md` |
| Apps / connectors | ❌ | ✅ | `.app.json` |
| LSP servers | ✅ | ❌ | `.lsp.json` |

The skill is the portable core (one `skills/<name>/SKILL.md` serves both).
Agents are Claude-Code-only — in Codex the skill covers the work inline. Detail:
read [references/claude-code-plugins.md](references/claude-code-plugins.md) and
[references/codex-plugins.md](references/codex-plugins.md).

## Workflow

### 1. Intake
Confirm: plugin **name** (kebab-case), one-line **description**, **author**,
**category**, and **which components** it ships (see the matrix). If packaging
something that already exists, note where that content currently is.

### 2. Scaffold
Run the scaffolder — it creates the dir, both manifests, requested component
stubs, a README, and registers the plugin in both marketplace catalogs
(idempotent):
```bash
python3 .claude/skills/create-plugin/scripts/scaffold_plugin.py <name> \
  --description "..." --category "..." --components skill,agents,mcp,hooks,commands
```
Default `--components` is `skill`. Run from the repo root. Use `--help` for all
options (`--display-name`, `--author`, `--keywords`, `--repo-url`, `--force`).

### 3. Fill the content
- **Skill**: write `skills/<name>/SKILL.md` (invoke `skill-creator` for the
  body). Reference its own bundled files with relative `references/…` paths.
- **Agents**: write `agents/*.md` (invoke `create-subagent`). To read the
  skill's bundled files from an agent, you MUST anchor with
  `${CLAUDE_PLUGIN_ROOT}/skills/<name>/references/…` — relative paths do not
  resolve across the `agents/` ↔ `skills/` boundary. Likewise the SKILL.md
  references agents via `${CLAUDE_PLUGIN_ROOT}/agents/…`.
- **MCP / hooks / commands**: fill `.mcp.json`, `hooks/hooks.json`,
  `commands/*.md`. Use `${CLAUDE_PLUGIN_ROOT}` for bundled script paths.
- If packaging existing content, `git mv` it into place so history is preserved.

### 4. Repo bookkeeping
If the plugin ships a distributable library skill, update
`skills-registry.yaml`, `skills-app/src/data/skills.ts`, and `CLAUDE.md` — see
[references/repo-conventions.md](references/repo-conventions.md). (Project-local
`.claude/skills/` skills are exempt.)

### 5. Validate (gate)
```bash
python3 .claude/skills/create-plugin/scripts/validate_plugin.py <name>
```
Fix every `FAIL`; review `WARN`s (the "Codex can't bundle agents" warning is
expected and fine). Require a clean run before committing.

### 6. Ship
Commit/push only when asked. Marketplace installs pull from GitHub, so after
pushing the user must Update/reinstall in each host (`/reload-plugins` in Claude
Code; `/plugins` browser or "Add to Codex" in Codex). If a skill still doesn't
appear: `rm -rf ~/.claude/plugins/cache`, restart, reinstall.

## Plugin container: multiple skills + named agent(s)

A plugin is a **container**, not a single skill. One plugin can bundle several
skills side by side under `skills/<skill-a>/`, `skills/<skill-b>/`, … plus one
or more named agents under `agents/`. `design-forge/` is the living example
(multiple bundled files + a named agent, cross-referenced via
`${CLAUDE_PLUGIN_ROOT}`). The `design-studio` case — brand-forge +
ship-polished-ui + design-elevation as skills, with a `visual-qa-inspector`
agent — is exactly this shape.

Scaffold it directly:
```bash
python3 .claude/skills/create-plugin/scripts/scaffold_plugin.py design-studio \
  --description "..." --category "Design" \
  --skills brand-forge,ship-polished-ui,design-elevation \
  --agents visual-qa-inspector
```
- `--skills a,b,c` creates one `skills/<each>/` (SKILL.md + `references/` +
  `assets/`) per entry. Omit it → single skill named after the plugin (legacy).
- `--agents x,y` creates `agents/<each>.md` with frontmatter `name: <each>`.
  Omit it → no agent unless `--components agents` is set, which falls back to the
  legacy `<plugin>-agent`.
- Each agent stub anchors bundled files with
  `${CLAUDE_PLUGIN_ROOT}/skills/<skill>/references/…` — pick the skill that owns
  the file (relative paths do NOT cross the `agents/` ↔ `skills/` boundary).

### Importing EXISTING skills into the container
When the skills already exist (as standalone repo skills or under
`.claude/skills/`), don't hand-recreate them — import the whole directory:
1. `git mv <existing-skill-dir> <plugin>/skills/<skill>/` (preserves history).
   Move the ENTIRE folder: `SKILL.md` + `references/` + `assets/` + `scripts/`.
2. Verify the SKILL.md's own `references/…` paths still resolve — they are
   relative to the SKILL.md, so a whole-folder move keeps them valid. Fix any
   that assumed a different location.
3. Adapt anything that referenced `~/.claude/…`, an absolute path, or the skill's
   old repo-root location — inside a plugin, bundled paths use
   `${CLAUDE_PLUGIN_ROOT}` and cross-skill refs go through
   `${CLAUDE_PLUGIN_ROOT}/skills/<other-skill>/`.
4. Do the registry anti-duplication bookkeeping (below), then `validate_plugin.py`.

## Scripts
- `scripts/scaffold_plugin.py` — generate the plugin skeleton + manifests +
  marketplace entries (deterministic).
- `scripts/validate_plugin.py` — check layout, manifests, `${CLAUDE_PLUGIN_ROOT}`
  cross-refs, and registration in every catalog. Exit 1 on FAIL.
