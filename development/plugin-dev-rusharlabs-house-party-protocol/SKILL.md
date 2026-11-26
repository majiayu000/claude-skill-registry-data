---
name: plugin-dev
description: Packages skills/hooks/commands into an installable Claude Code plugin — the real anatomy (.claude-plugin/plugin.json + hooks/hooks.json + ${CLAUDE_PLUGIN_ROOT}), no framework/build step. Use when the user wants to create a plugin, package an extension, or distribute a set of skills/hooks.
---

> **Auto-Trigger:** When the user wants to create a Claude Code plugin, package skills/hooks for distribution, or asks "how do I make an installable plugin".
> **Keywords:** "plugin", "create plugin", "package plugin", "claude-plugin", "marketplace", "plugin.json", "distribute skill"
> **Priority:** HIGH
> **Tools:** Read, Write, Edit, Glob, Grep, Bash

## When NOT to Activate
- Using an already installed plugin without modification, or debugging an existing plugin (read the files directly).
- **Creating the SKILL or the HOOK itself** — use `skill-writer`/`hookify` from this same module first; `plugin-dev` is only the PACKAGING that groups what already exists, it creates no new content.
- Do not confuse with an npm/TypeScript package — Claude Code plugins **have no build step, no `package.json`, no `src/index.ts`**. It is a directory with JSON manifests + files Claude Code already knows how to interpret (SKILL.md, Python hooks, .md commands).

## Contract

**INPUT:** a set of already created (or to be created) skills/hooks/commands that must become an installable plugin.

**OUTPUT:** a `<plugin-name>/` directory with a valid `.claude-plugin/plugin.json` (+ `hooks/hooks.json` if there are hooks).

**EXIT CODES** (from the manifest validator used in the Proof section):

| Exit | Meaning |
|---|---|
| 0 | manifest with all required fields |
| 1 | required field missing |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| `<plugin>/.claude-plugin/plugin.json` | Writes | plugin manifest (name, version, hooks, commands) |
| `<plugin>/hooks/hooks.json` | Writes (if there are hooks) | declarative hook registration — see the `hookify` skill |
| `<plugin>/skills/*/SKILL.md` | Reads (already existing) | the skills the plugin packages — see the `skill-writer` skill |
| `marketplace.json` (if distributing >1 plugin together) | Writes | index of several plugins — `/plugin marketplace add` reads this file |

## REAL anatomy of a plugin (it is not TypeScript/npm)

```
meu-plugin/
├── .claude-plugin/
│   └── plugin.json        # manifest — REQUIRED
├── hooks/
│   ├── hooks.json         # declarative hook registration (if any)
│   └── meu_hook.py        # the actual script(s) — see the hookify skill
├── skills/
│   └── minha-skill/
│       └── SKILL.md       # see the skill-writer skill
├── commands/               # optional — custom slash commands
│   └── meu-comando.md
├── scripts/                # optional — helper CLIs
└── README.md               # install + usage
```

No `src/`, `package.json`, `*.test.ts`, build step. If the plugin has Python logic (hooks/scripts), it runs directly via `python arquivo.py` — no transpilation, no bundler.

## `${CLAUDE_PLUGIN_ROOT}`

Every command reference inside `hooks.json` must use `${CLAUDE_PLUGIN_ROOT}` instead of a raw relative path — Claude Code resolves that variable to the plugin's real root AT INSTALL TIME, so it works no matter where the user installed it (they may have cloned it to a path completely different from yours).

```jsonc
// WRONG — breaks as soon as the plugin is installed at a different path
{ "type": "command", "command": "python meu-plugin/hooks/meu_hook.py" }

// CORRECT
{ "type": "command", "command": "python \"${CLAUDE_PLUGIN_ROOT}/hooks/meu_hook.py\"", "timeout": 30 }
```

## `.claude-plugin/plugin.json` — real fields (example from a module in this marketplace)

```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
  "name": "meu-plugin",
  "displayName": "My Plugin",
  "version": "1.0.0",
  "description": "What the plugin does + when to use it.",
  "author": { "name": "Your Name" },
  "license": "MIT",
  "keywords": ["category1", "category2"],
  "commands": "./commands"
}
```

`commands` is OPTIONAL — omit it if the plugin only ships skills. Do not list `hooks/hooks.json` in the
manifest: Claude Code loads it on its own, and earlier versions refuse a plugin that names it twice.
`hooks` in the manifest is only for ADDITIONAL hook files.

## `hooks/hooks.json` — declarative registration (see the `hookify` skill for the script itself)

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Edit|Write|MultiEdit", "hooks": [
        { "type": "command", "command": "python \"${CLAUDE_PLUGIN_ROOT}/hooks/meu_hook.py\"", "timeout": 30 }
      ]}
    ]
  }
}
```

## Real limitation: `statusLine` does NOT go in the plugin

Claude Code does not accept `statusLine` inside `plugin.json`/`hooks.json` — it has to go manually into the target project's `.claude/settings.json`/`settings.local.json`, even if the plugin ships a ready statusline (`statusline/statusline.py --statusline`). Document that manual step in the plugin's README; do not promise an "auto-installed statusLine".

## Install (1 plugin) or distribute (several in a marketplace)

```bash
# install 1 plugin from a local directory
/plugin marketplace add .
/plugin install meu-plugin@<nome-do-marketplace>
```

To distribute SEVERAL plugins together, create a `marketplace.json` at the root of the bundle:

```json
{
  "$schema": "https://json.schemastore.org/claude-code-marketplace.json",
  "name": "meu-marketplace",
  "description": "Plugin bundle",
  "version": "1.0.0",
  "owner": { "name": "Your Name" },
  "plugins": [
    { "name": "meu-plugin", "displayName": "My Plugin", "source": "./meu-plugin",
      "description": "...", "version": "1.0.0", "category": "productivity", "keywords": ["..."] }
  ]
}
```

## Process

1. **Create/gather** the skills (`skill-writer`) and hooks (`hookify`) the plugin will package.
2. **Build `.claude-plugin/plugin.json`** with the required fields (`name`, `version`, `description`) + `hooks`/`commands` if applicable.
3. **If there are hooks**, build `hooks/hooks.json` referencing each script via `${CLAUDE_PLUGIN_ROOT}`.
4. **Validate the manifest** (see Proof) before announcing it as ready.
5. **Document the installation** in the README (`/plugin marketplace add` + `/plugin install`), including any MANUAL step (e.g. statusLine).
6. **Actually test the installation** in a separate directory/project; do not just read the JSON.

## Executed examples

```console
$ python -c "
import json
def validate_plugin_manifest(data):
    required = ['name', 'version', 'description']
    return [k for k in required if k not in data]
sample = {'name':'exemplo-kit','version':'1.0.0','description':'kit de example','hooks':'./hooks/hooks.json'}
missing = validate_plugin_manifest(sample)
assert missing == [], missing
print('plugin.json valido: campos obrigatorios presentes')
"
plugin.json valido: campos obrigatorios presentes
```
<!-- executed: 2026-10-30 · exit=0 -->

```console
$ python -c "
def validate_plugin_manifest(data):
    required = ['name', 'version', 'description']
    return [k for k in required if k not in data]
bad = {'name': 'sem-versao'}
missing = validate_plugin_manifest(bad)
print('plugin.json invalido detectado:', missing)
import sys; sys.exit(1 if missing else 0)
"
plugin.json invalido detectado: ['version', 'description']
```
<!-- executed: 2026-10-30 · exit=1 -->
(a manifest without `version`/`description` is rejected BEFORE attempting to install — fails early, not in production.)

```console
$ mkdir -p meu-plugin/.claude-plugin meu-plugin/hooks && ls meu-plugin
hooks
```
<!-- executed: 2026-10-30 · exit=0 -->
(steps 2-3 of the process — directory skeleton before writing the manifests; plain `ls` hides the dot-directory, `ls -a meu-plugin` also shows `.claude-plugin`.)

## Anti-patterns

- ❌ `src/index.ts` + `package.json` + build step — Claude Code plugins are not npm packages; they are directories Claude Code already knows how to read.
- ❌ Raw relative path in `hooks.json` (`"command": "hooks/meu_hook.py"`) — breaks as soon as it is installed at a path different from yours. Always `${CLAUDE_PLUGIN_ROOT}`.
- ❌ Promising a `statusLine` "auto-installed by the plugin" — it is a real Claude Code limitation; document the manual step.
- ❌ Announcing the plugin as ready without actually testing the installation (only reading the JSON does not prove it installs).

## Proof

```bash
python -c "
def validate_plugin_manifest(d):
    return [k for k in ('name','version','description') if k not in d]
assert validate_plugin_manifest({'name':'x','version':'1.0.0','description':'y'}) == []
assert validate_plugin_manifest({'name':'x'}) == ['version','description']
print('self-test OK')
"
```
