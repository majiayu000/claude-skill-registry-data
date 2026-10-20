---
name: add-plugin-component
description: >-
  Load this skill when adding or changing anything under plugins/ in this repo (a skill, agent,
  hook, script, or new ceh-* plugin): templates, frontmatter rules, and the registration chores CI
  checks. Trigger on "add a skill", "create a plugin", or validate.py failing. Overrides plugin-dev
  and skill-creator.
argument-hint: "[skill-or-agent-name]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Adding a Component to This Repo

Every new `SKILL.md` or `agents/*.md` starts as a copy of its template, then gets registered in
the same commit. The content is the easy half. The half that gets forgotten is registration: the
same fact lives in the plugin README and `docs/CATALOG.md`, both manifests, and sometimes `docs/CROSS_REFERENCES.md`, and CI
fails when they drift.

## 1. Pick the plugin and the component type

Plugins split on **use case**, not tech domain or lifecycle phase. Load exactly one plugin per
use case, so each must be self-contained. The tiers are defined in `CLAUDE.md`.

Check the component against `docs/VISION.md` first, whether it is new or a change: it passes the
scope test, and it answers the **Ask** question of every principle it touches. A component the
vision does not allow is changed until it does, or not built. Record the reason in `docs/IDEAS.md`
when it is rejected.

- A skill triggers on a **moment** (a verb: "I'm opening a PR", "I'm writing a migration"), never
  a **topic** (a noun: "PostgreSQL"). Topic-named skills either never auto-trigger or restate what
  the model already knows. If you cannot name the moment, the skill is not ready.
- Framework variants do **not** get their own plugin when their skills trigger on disjoint file
  types — `sveltekit` and `react-vite` share `ceh-web-frontend`.
- A foundational standard needed by two use-case plugins is **duplicated into both**, never
  extracted into a shared base plugin. Register the duplication (step 4).
- App-specific patterns are not standards. Anything bound to one application's schema or design
  gets removed, not filed as a niche plugin.

If no existing plugin owns the use case, create one first — see [New plugin](#new-plugin) — then
continue at step 2.

Then pick the component type by what the need is:

| Need                                                                             | Component                                   | Settle before writing                                                                            |
| -------------------------------------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| Knowledge or a procedure Claude applies at a moment, or a user-invoked `/action` | Skill                                       | Trigger phrases, what it adds beyond model knowledge, arguments, tools, interactive or automated |
| An autonomous task whose output or cost should stay out of the main session      | Agent                                       | Proactive or on request, tool set, model, output format                                          |
| A rule that must hold on every event, whether or not Claude remembers it         | Hook                                        | Which events, prompt or command, what blocks vs warns                                            |
| An external service or API                                                       | MCP server                                  | Server type, authentication, which tools                                                         |
| User or project configuration                                                    | Environment variable, never a settings file | Variable names, required vs optional, defaults                                                   |

New slash commands are skills (`skills/<name>/SKILL.md`), never the legacy `commands/` layout.
Answer the "settle" column from the request and the code. Ask the user only for what neither
settles.

## 2. Write the component

Editing an existing skill instead? Check `docs/CROSS_REFERENCES.md` first (step 4).

Creating any component, including one migrated from agent-skills, starts by loading its
authoring skill. Where that skill's advice conflicts with this repo, this skill wins — see
[the override table](#when-plugin-dev-or-skill-creator-skills-are-also-loaded).

| Creating   | First                                                                                                                                                                                                         |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Skill      | Invoke the Skill tool with skill="skill-creator:skill-creator". Never `plugin-dev:skill-development`. Skip its eval loop (test runs, benchmark, viewer, description optimization) unless the user asks for it |
| Agent      | Invoke the Skill tool with skill="plugin-dev:agent-development"                                                                                                                                               |
| Hook       | Invoke the Skill tool with skill="plugin-dev:hook-development"                                                                                                                                                |
| MCP server | Invoke the Skill tool with skill="plugin-dev:mcp-integration"                                                                                                                                                 |

**Skill** — copy `${CLAUDE_SKILL_DIR}/assets/SKILL.template.md` to
`plugins/standalone/ceh-<plugin>/skills/<name>/SKILL.md`, `name` matching the directory. Fill every
placeholder, then delete the `TEMPLATE-GUIDANCE` comment. Content stays inline. `references/` is
for two cases only: a schema or template shared by several skills, or a standard too large to
inline. A file shared by skills of the same plugin goes once in `plugins/standalone/ceh-<plugin>/references/`,
cited as `${CLAUDE_PLUGIN_ROOT}/references/<file>`. A file used by one skill goes in that skill's
own `references/`, cited as `${CLAUDE_SKILL_DIR}/references/<file>`.

**Agent** — copy `${CLAUDE_SKILL_DIR}/assets/agent.template.md` to
`plugins/standalone/ceh-<plugin>/agents/<name>.md`, `name` matching the file name. Auto-delegation is driven
entirely by `description` (include "use proactively" to encourage it).

**Migrating from agent-skills** — still start from the template: move the old frontmatter and
sections into the template's order and headings rather than copying the old file whole. Old files
mix heading case and section names, and the templates exist to end that.

**Hook or script** — hook wiring goes in `plugins/standalone/ceh-<plugin>/hooks/hooks.json`, scripts in
`plugins/standalone/ceh-<plugin>/scripts/`, referenced as `${CLAUDE_PLUGIN_ROOT}/scripts/<file>`. Keep
`*.sh` LF-only: a CRLF checkout breaks bash with `$'\r'`.

**MCP server** — config goes in `plugins/standalone/ceh-<plugin>/.mcp.json` with `${CLAUDE_PLUGIN_ROOT}`
paths.

**Configuration** — environment variables only, never a `.claude/*.local.md` settings file or
other config file. Hooks, MCP servers, and scripts use HTTPS and never hardcode a credential: read
it from an environment variable and document every variable in the plugin README.

**`description` is always a folded block scalar (`>-`)** — never quoted, never plain. `validate.py`
rejects anything else.

```yaml
description: >-
  Load this skill when doing X: the colon is literal here, as are "quotes" and 'apostrophes'.
  Wrap at ~98 chars with a uniform 2-space indent and no blank lines.
```

It is the only style with no escaping burden. A plain scalar cannot contain `: `, single-quoted
needs `''` doubling, double-quoted needs `\` and `"` escaping — all three have silently produced
invalid YAML in this repo. Keep the indent uniform (a more-indented line becomes a literal newline
instead of folding) and avoid blank lines. Any _other_ key containing `: ` gets single quotes.
Put the key use case first: Claude Code truncates long descriptions in the skill listing.

Claude Code silently ignores a frontmatter field it does not recognize, so a typo reads as
working config. Use only fields from the official
[skills](https://code.claude.com/docs/en/skills#frontmatter-reference) and
[subagents](https://code.claude.com/docs/en/sub-agents#supported-frontmatter-fields) references.
`validate.py` rejects any other key. Frontmatter worth reaching for before writing prose that does
the same job:

| Field                      | Use it for                                                                                   | Watch out                                                                                                                                                            |
| -------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `paths`                    | Skills whose trigger really is a file type                                                   | **Narrows** auto-loading. A skill with real non-file triggers ("a `uv` command is run") loses them                                                                   |
| `effort`                   | Reasoning-heavy skills                                                                       | Default inherits the session level. Set it only when the skill needs a different one                                                                                 |
| `disable-model-invocation` | Workflows with side effects the user should trigger by hand                                  | The skill can then never be preloaded into an agent or called with `Invoke the Skill tool`                                                                           |
| `disallowed-tools`         | Skills that must not write                                                                   | Check the body first; most "review" skills here do apply fixes                                                                                                       |
| `context: fork`            | Heavy, self-contained task skills                                                            | The subagent does **not** see the conversation and runs in the background with the reduced tool set below. Set `background: false` if a step needs a tool outside it |
| `argument-hint`            | Skills the user invokes as `/name <arg>`                                                     | Cosmetic but free                                                                                                                                                    |
| `${CLAUDE_SKILL_DIR}`      | Referencing a file bundled with the skill                                                    | Substituted in the body _and_ in `allowed-tools` Bash rules                                                                                                          |
| `${CLAUDE_PLUGIN_ROOT}`    | Referencing a plugin-level script or `references/` file shared by several skills             | Substituted in plugin skill bodies and `allowed-tools`, not in project skills                                                                                        |
| `memory`                   | Agents that should learn across sessions                                                     | Auto-enables Read/Write/Edit on that agent                                                                                                                           |
| `compatibility`            | Skills that need software the machine may lack (`git`, `gh`, `uv`, `bun`, a server, network) | `>-` scalar, max 500 chars. Name runtime + minimum version and what fails without it. Omit for read-files-emit-Markdown skills                                       |

**Cross-plugin calls** — when a skill must call a skill in another plugin on _every_ run, add the
target plugin to `dependencies` in `plugin.json` (never in `marketplace.json`; bare strings, no
ranges) and call it explicitly: `Invoke the Skill tool with skill="ceh-<plugin>:<skill>"`.
Conditional handoffs and negative routing ("Not for X, use ...") stay prose with no dependency. A
cross-cutting plugin may depend only on other cross-cutting plugins. `validate.py` rejects a call
whose target does not resolve, is not a declared dependency, or sets
`disable-model-invocation: true`.

**Plugin-agent gotchas** — Claude Code ignores `permissionMode`, `hooks`, `mcpServers`, and
`initialPrompt` on plugin agents (security restriction). Do not add them; they read as working
config and are not. Grant edit permissions via session `permissions.allow` in `settings.json`
instead. Subagents run in the **background by default**, and background subagents keep only a
reduced built-in tool set — if an agent needs a tool outside `Read/Grep/Glob/LSP/Bash/PowerShell/
Edit/Write/NotebookEdit/WebFetch/WebSearch/TodoWrite/Skill/ToolSearch/EnterWorktree/ExitWorktree/
Monitor/TaskStop/SendMessage/Artifact`, it will be stripped silently. `AskUserQuestion` is stripped
from _every_ subagent, foreground or background — an agent can never stop to ask.

`skills:` entries must be fully qualified as `plugin:skill`; an entry that does not resolve is
skipped with only a debug-log warning. The preload is also the only route a hook-loaded standard
has into an agent: `SessionStart` hooks never fire for subagents.

**No agent sets `isolation: worktree` in its frontmatter.** Subagent worktrees branch from the
repository's **default branch**, not the parent session's `HEAD`, unless `worktree.baseRef: "head"`
is set in `settings.json` — and their changes stay in the worktree rather than landing in your
checkout. In frontmatter it would apply to every run, and under this repo's feature-branch rule
that hands the agent a copy of `main` without your work. Isolation is the dispatcher's call per
run instead: `ceh-coding-conduct:agent-coding-contract` passes `isolation: "worktree"` on the
`Agent` call when parallel subagents edit files, checks each worktree's base, and merges the
branches back.

## 3. Update the catalog and the plugin README

- `docs/CATALOG.md` — add a row under the correct plugin group in **Skills** or **Agents**. If the
  plugin has no group there yet, add a `### <Plugin> (\`ceh-<plugin>\`)` subsection.
- `plugins/standalone/ceh-<plugin>/README.md` — add a row to that plugin's own table. The plugin README also
  carries anything a user must do before the component works: prerequisites, when a hook fires,
  and every environment variable the plugin reads, with its default and whether it is required.
  A new variable also gets a row in `docs/ENVIRONMENT_VARIABLES.md`, the index across plugins.

## 4. Register any duplication

Before editing an existing skill, check `docs/CROSS_REFERENCES.md`. If the section appears there,
propagate the edit to **every** listed file in the same session — canonical file first, then the
copies. If you introduce new duplication, add an entry naming the canonical source, every copy,
what is shared, and what deliberately diverges. Skills of one plugin share a file once in the
plugin's `references/`, so that needs no entry. Duplication plus an entry is for content shared
across plugins.

## 5. Bump the version in both manifests

Same commit, both files, or CI fails:

- `plugins/standalone/ceh-<plugin>/.claude-plugin/plugin.json`
- `.claude-plugin/marketplace.json`

**PATCH** for content/description updates, **MINOR** for a new skill or agent or for adding or
removing a `dependencies` entry, **MAJOR** for renaming or removing the plugin. Bump at commit
time, not during iterative edits. The PR also adds its `CHANGELOG.md` entry under the date it is
opened and updates `docs/PLUGIN_VERSIONS.md` — see Versioning in `CLAUDE.md`.

## 6. Validate

```bash
python tools/validate-plugins/validate.py
```

Same gate CI runs via `.github/workflows/validate.yml`. It checks:

- manifests: `plugin.json` ↔ `marketplace.json` sync, semver, `name` matching the directory
- frontmatter: `name` format and match, `description` present, `>-`, ≤ 300 chars;
  `compatibility` ≤ 500 chars; only documented keys; no plugin-agent keys Claude Code ignores;
  `disable-model-invocation`, `user-invocable`, and `license` stated on every skill
- `docs/PLUGIN_VERSIONS.md` matches every `plugin.json`, and so does each plugin's newest
  `CHANGELOG.md` Plugin versions row, under the date `PLUGIN_VERSIONS.md` gives it; cross-cutting plugins depend only on
  cross-cutting plugins; a skill a hook names is `user-invocable: false`
- no `TEMPLATE-GUIDANCE` comment left from a template
- `references/...`, `${CLAUDE_PLUGIN_ROOT}/{scripts,references}/...`, and `${CLAUDE_SKILL_DIR}/...` mentions
  resolve to real files, and `ceh-<plugin>:<component>` mentions resolve
- `dependencies` resolve and the graph is acyclic
- every `Invoke the Skill tool with skill="..."` call is resolvable, declared, and invocable
- bundled `*.sh` / `*.py` scripts parse

`validate.py` does not parse YAML strictly. For a YAML syntax check, also run
`claude plugin validate plugins/standalone/ceh-<plugin>`.

A green validator proves the files are well-formed, not that the component works. Load the plugin
in a fresh session with `claude --plugin-dir plugins/standalone/ceh-<plugin>` and check what you added:

- Skill: a prompt using a description trigger phrase loads it; `/ceh-<plugin>:<skill>` runs it
- Agent: a prompt matching its description delegates to it
- Hook: `claude --debug` shows it firing on its event
- MCP server: `/mcp` lists the server and its tools

When one wording carries the component (a trigger phrase, a rule the model keeps breaking) and the
user asks to check it, micro-test it before a full `skill-creator` eval: run the same prompt five
times in fresh `claude -p` sessions with the plugin and five without, and compare. Results that
vary across the five runs are the signal that the wording is weak, more than one pass or fail.
Every run is a billed model call, so this waits for a request like any eval.

When the user asks for eval cases (`claude plugin eval init`, or a skill's `evals/evals.json`),
write each case at three strictness levels over the same task, so a score drop comes from the
wording alone:

- **Supportive** — the prompt names the moment the skill is for ("I'm opening a PR, write the
  body").
- **Neutral** — the task only, with no hint of the skill ("here's my branch, get it merged").
- **Competing** — the task plus a pull away from the skill's rule ("make it quick, the reviewer
  is waiting"). It tempts and never orders: "skip the tests" is an instruction the contract says
  the model must obey, and grading compliance as a failure punishes the right behavior.

Failing at neutral points at the description. Failing even at supportive points at the body. A
required step that fails at all three levels and shows in a tool call (a path, a command, a file
written) is a candidate for a hook rather than another rewording.

Report any check you did not run as not run. Do not imply it passed.

## New plugin

Only when step 1 finds no plugin that owns the use case. The layout is fixed by this section and
the Structure section of `CLAUDE.md`, so do not load `plugin-dev:plugin-structure`. Decide the
tier (cross-cutting, use-case workflow, stack/build — see `CLAUDE.md`) and the lifecycle stage,
and plan every component with the step 1 table before creating anything, then:

1. `plugins/standalone/ceh-<name>/.claude-plugin/plugin.json`, under `plugins/standalone/` with no tier folder:

   ```json
   {
     "name": "ceh-<name>",
     "version": "1.0.0",
     "description": "CEH <name>: <one sentence on the use case>.",
     "author": { "name": "cheneeheng", "email": "eeheng.chen@gmail.com" },
     "repository": "https://github.com/cheneeheng/ceh-claude-code-library",
     "license": "Apache-2.0",
     "keywords": ["agent", "<keyword>"]
   }
   ```

   Add `"dependencies": ["ceh-<other>"]` only per the cross-plugin rule in step 2.

2. `plugins/standalone/ceh-<name>/README.md` with the plugin's own skill/agent table.
3. `.claude-plugin/marketplace.json` — a new entry whose `source` (`./plugins/standalone/ceh-<name>`),
   `version`, and `description` mirror `plugin.json`. `validate.py` fails on a plugin missing from
   the marketplace or a version mismatch.
4. Root `README.md` — a row in the **Plugins** table and the plugin in the **By lifecycle stage**
   table. Its Skills/Agents rows go in `docs/CATALOG.md`. Install commands live only in
   `docs/GETTING_STARTED.md`.
5. `CLAUDE.md` — the plugin in the tier table.
6. `docs/GETTING_STARTED.md` — an entry for the moment it serves, under its stage in step 3
   (with the slash command that starts it) if it is on the lifecycle route, or a row in step 4 if
   users add it only when that moment arrives. Record any new
   dependency edge in `docs/PLUGIN_DEPENDENCIES.md`.

In the same PR, `CHANGELOG.md` lists the plugin at `1.0.0` under `### Added` and
`docs/PLUGIN_VERSIONS.md` gains its row.

## When plugin-dev or skill-creator skills are also loaded

Step 2 loads `skill-creator` and the plugin-dev authoring skills on purpose, and
`plugin-dev:create-plugin` triggers on the same phrases as this skill. They give generic advice.
Where it conflicts with this repo, this skill wins:

| They say                                                                                     | This repo does                                                                          |
| -------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `plugin-dev:skill-development` for skills                                                    | `skill-creator:skill-creator`                                                           |
| Run test prompts, benchmark, open the viewer, optimize the description                       | Only when the user asks. Otherwise stop after the draft                                 |
| `plugin-dev:plugin-structure` for layout                                                     | The layout in [New plugin](#new-plugin) and `CLAUDE.md`                                 |
| `plugin-dev:plugin-settings`, `.claude/<plugin>.local.md` settings files                     | Environment variables, documented in the plugin README                                  |
| Lean SKILL.md, detail in `references/` and `examples/`                                       | Content inline. `references/` only for shared schemas or oversized standards            |
| "This skill should be used when…" descriptions, any scalar style                             | `>-` folded scalar, "Load this skill when…" (agents: "Use this agent to…")              |
| Write the file from scratch, or generate an agent with the `agent-creator` agent             | Start from the template in `${CLAUDE_SKILL_DIR}/assets/`                                |
| Skills in the legacy `commands/` layout                                                      | `skills/<name>/SKILL.md` only                                                           |
| Hook scripts in `examples/`                                                                  | `scripts/`, referenced as `${CLAUDE_PLUGIN_ROOT}/scripts/...`                           |
| New plugin at `0.1.0`, marketplace entry optional                                            | `1.0.0`, marketplace entry in the same commit                                           |
| `plugin-validator` / `skill-reviewer` agents, `validate-agent.sh`, `validate-hook-schema.sh` | `python tools/validate-plugins/validate.py` is the gate, then the live checks in step 6 |
| Agent `<example>` blocks and `color`                                                         | Prose `description`, no `<example>` blocks; `color` optional                            |
| Eval workspace next to the skill directory                                                   | `.agents_workspace/skill-evals/<skill>/`, git-ignored, never inside `plugins/`          |
| Wait for user confirmation at each phase, ask where to create, `git init`                    | Autonomous mode, `plugins/standalone/`, existing repo                                   |

Everything else in those skills applies — hook event payloads, prompt-based hooks, MCP server
types, agent system-prompt design, skill-creator's drafting guidance.
