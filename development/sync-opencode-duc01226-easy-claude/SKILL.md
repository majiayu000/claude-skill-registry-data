---
name: sync-opencode
description: '[opencode] Use when running the opencode sync and verify pipeline: opencode.json reconcile, skill policy, hidden-skill commands, hooks bridge, sub-agent mirror, drift check.'
disable-model-invocation: true
---

> Codex compatibility note:
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Host-native execution: Codex runs a skill by loading its `SKILL.md` instructions and executing the required steps with available tools. No separate `Skill` tool is required; a loaded skill is already activated.
> - Source vs execution: prefer the registered `.agents/skills/<name>/SKILL.md` for Codex execution. `.claude/**` remains the canonical authoring source; reading it for a registry or source inspection does not switch this session to Claude Code.
> - Capability check: interpret Claude tool names through the active host before declaring a blocker. Continue when Codex can perform the required operation; stop and ask only when the actual capability is unavailable, naming the step and evidence. Host-native execution is not a protocol deviation and needs no extra approval.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - Use ask user tool to ask user.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, steps follow the guided contract in `$start-workflow` (gate steps fixed; other steps may flex with a logged reason); report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.
## Quick Summary

**Goal:** Reconcile the project-root `opencode.json` with the framework's recommended opencode defaults, compile `.claude/settings.json` into a portable opencode plugin (`.opencode/plugins/easy-claude-hooks.js`), and verify both. This runner is the **single and only** entrypoint for the opencode surface pipeline.

> **PORTABILITY CONTRACT — `.claude/` and `.opencode/` are portable, self-running and self-testing.**
> Copy them into ANY repository — a Python repo, a .NET repo, a repo with no `package.json` at all —
> and the sync / verify / test entrypoint still works, because it is a path INSIDE the bundle invoked
> with plain `node`. **Never** drive this framework through a host `package.json` script, and never
> document one: `npm run …` names a command that does not exist in most projects the bundle is copied
> into. The only external requirement is `node` >= 18 — no `node_modules`, no npm, no lockfile. The
> generated plugin imports only `node:` built-ins and spawns the canonical `.claude/hooks/*.cjs`
> scripts.
>
> Discover the roster instead of memorizing it:
> `node .claude/skills/sync-opencode/scripts/run-opencode-sync.mjs --list-stages`

**Summary:**

- opencode has **no shell-command hook system** — hooks are JavaScript plugin callbacks. This skill compiles `.claude/settings.json` into a bridge plugin whose runtime drives the original Claude hooks from opencode's plugin events.
- **Recommended opencode config is part of the framework.** `.opencode/opencode.recommended.json` is the single source of truth for the framework's opencode defaults; the `config` stage deep-merges it into the project-root `opencode.json` (recommended keys win, project-only keys survive).
- Scope is **hooks + recommended config + skill permissions + the sub-agent mirror**. opencode already auto-discovers skills from `.claude/skills` and `.agents/skills`, so there is **no skill mirroring** here (unlike `$sync-codex`). opencode ignores `disable-model-invocation`, so the `skills` stage enforces the selection policy through `permission.skill` in the project-root `opencode.json` instead, and writes a `.opencode/commands/<name>.md` per hidden skill so its explicit `/name` keeps working — see [Skill permissions](#skill-permissions). Sub-agents are NOT auto-discovered, so `.claude/agents/*.md` IS mirrored into `.opencode/agent/*.md` by the `agents` stage — that is what lets the workflow protocols dispatch the same specialists (`architect`, `code-reviewer`, `security-auditor`, …) on opencode.
- Keep `.claude` canonical: edit `.claude/settings.json` / `.claude/hooks/**` and re-run this pipeline; never hand-edit the generated `.opencode/plugins/easy-claude-hooks.js`.
- To change a default opencode setting, edit `.opencode/opencode.recommended.json`, then re-run this pipeline to propagate it into the root config of every project the `.opencode/` folder is copied into.
- The legacy hand-written `.opencode/plugins/notification.js` is superseded by the generated bridge; the runner backs it up under `tmp/opencode-legacy/` and removes it so notifications are not sent twice.

**Workflow:**

1. **Config** — `node .claude/scripts/opencode/sync-config.mjs` deep-merges `.opencode/opencode.recommended.json` into the project-root `opencode.json`.
2. **Sync** — `node .claude/skills/sync-opencode/scripts/run-opencode-sync.mjs` rewrites `permission.skill` in the project-root `opencode.json` together with its ownership ledger `.opencode/skill-permissions.generated.json`, writes a marked `.opencode/commands/<name>.md` per hidden skill, and regenerates the bridge plugin, the `.opencode/agent/*.md` mirror, and the sync report.
3. **Test** — the runner executes the opencode tooling tests (config + writer + generated-plugin runtime).
4. **Verify** — the runner re-merges/re-renders in memory with the REAL writers and byte-compares against the tracked files.
5. **Inspect** — on failure, re-run the failing stage with `--only=<stage> --verbose`.

**Key Rules:**

- MUST run stages in order — the orchestrator fails fast on the first non-zero exit
- NEVER hand-edit `.opencode/plugins/easy-claude-hooks.js`; regenerate it from `.claude/settings.json`
- **NEVER hand-edit a project-root `opencode.json` as the way to change framework defaults** — edit `.opencode/opencode.recommended.json` and re-run the pipeline
- `.opencode/opencode.recommended.json` MUST NOT be named `.opencode/opencode.json`; opencode auto-loads that path as project config
- The generated plugin and `.opencode/plugins/**` are the only opencode hook surface; no skill mirror is produced (skills are auto-discovered, sub-agents are mirrored into `.opencode/agent/**`)
- Only `node "$CLAUDE_PROJECT_DIR"/...` hook commands are compiled; other command shapes are reported as `unsupported-command-shape`
- Claude events opencode cannot reproduce are reported as `skipped-events` in the sync report — never silently dropped
- The `skills` stage changes only `permission.skill` keys recorded in `.opencode/skill-permissions.generated.json`; a user-set key is never adopted, overwritten or loosened, and a called skill is never hidden; it rewrites or deletes only `.opencode/commands/*.md` files that carry its generated marker
- Idempotent — re-running the sync produces byte-identical plugin, config, permission, and agent output

## Why a bridge plugin (not a config mirror)

> The `config` stage above reconciles framework-recommended opencode **defaults**; it is not a mirror of Claude settings. This section explains why the project's *hook* surface is generated as a plugin.

Codex supports lifecycle hooks and can be driven by `.codex/hooks.json`. opencode cannot: its only
extension point for lifecycle behavior is a JS/TS plugin under `.opencode/plugins/` (or an npm plugin).
So instead of transcribing commands into a JSON file, this pipeline emits a self-contained plugin that
spawns the canonical Claude hook scripts and translates both directions:

| Direction | Translation |
| --- | --- |
| opencode → Claude hook | event name, tool id → Claude matcher name, opencode args → `tool_input` field names |
| Claude hook → opencode | exit `0` = allow · exit `2` = block (throw) · stdout `hookSpecificOutput.updatedInput` = argument rewrite · stdout `hookSpecificOutput.additionalContext` = injected context · stdout `hookSpecificOutput.permissionDecision: "deny"` = block |

## Recommended opencode config (source of truth)

The framework ships recommended opencode defaults as a portable template and
reconciles them into whatever project the `.opencode/` folder is copied into.

| Item | Path |
| --- | --- |
| **Source of truth (edit this)** | `.opencode/opencode.recommended.json` |
| **Generated target (never hand-edit for defaults)** | `<project-root>/opencode.json` |
| Writer / verifier | `.claude/scripts/opencode/sync-config.mjs` (`--check` for verify) |

> **To change a default recommended opencode setting in the future, edit `.opencode/opencode.recommended.json`** and re-run `$sync-opencode`. Every project that receives the `.opencode/` folder then gets the updated default the next time the pipeline runs. The recommended file is deliberately NOT named `.opencode/opencode.json` because opencode auto-loads that path as project config — keeping the `.recommended.json` name makes it a template, not an active config.

**Merge semantics:** the writer deep-merges the recommended defaults into the existing root `opencode.json`. Recommended keys win at every leaf; object keys that exist only in the project survive untouched; arrays in the recommended file replace the project's array. A project with no root config receives the recommended defaults verbatim. A malformed existing root config is reported, never clobbered.

### Compaction: host default

The framework pins no auto-compaction budget on any of its three surfaces (Claude Code,
Codex, opencode), so each host applies its own default and each user sets their own.
The recommended file therefore carries no model `limit`: opencode takes the window from
the model's registry entry (models.dev). For the pinned model that is `context: 1000000`,
`output: 384000` (verified with `opencode models opencode-go --verbose`, v1.18.31).

opencode has no absolute compaction threshold — it compacts relative to the model's
declared window, so the window IS the knob. From `session/overflow.ts` (v1.18.31):

```text
usable = limit.input ? max(0, limit.input - (compaction.reserved ?? min(20_000, maxOutput)))
                     : max(0, limit.context - maxOutput)
maxOutput = min(limit.output, 32_000)          // OUTPUT_TOKEN_MAX
compaction happens once total tokens >= usable
```

So the registry window compacts at **968,000** tokens (1,000,000 − 32,000). A user who
wants an earlier point sets their own `limit` on the model — in the project-root
`opencode.json` or their global opencode config. For example, `limit.context: 500000` +
`limit.output: 384000` compacts at 468,000.

**Retiring the old pin:** the `config` stage removes the model's `limit` from the root
`opencode.json` only when it is exactly the formerly bundled
`{ "context": 500000, "output": 384000 }` (the deep merge alone never deletes a key). Any
other `limit` is the user's: it is kept and reported with one `kept user-set …` line. Keep
a personal 500K budget in the global opencode config if the root file must stay untouched.

Two traps for anyone setting their own `limit`, both verified against the released source:

- **`compaction.reserved` is inert here.** It is only read on the `limit.input` branch,
  and models.dev declares no `input` for this model. Raising it does nothing.
- **Do NOT express the budget as `limit.input`.** It is undocumented, and `limit.context`
  is what the rest of opencode reads as the window — the TUI context percentage, ACP usage
  reporting, and the `limits` handed to the AI SDK. Capping `input` while leaving `context`
  at 1M shows ~48% in the TUI at the moment it compacts.

**Copying the framework into a new project:** copy `.claude/` and `.opencode/` (including `.opencode/opencode.recommended.json`), then run `$sync-opencode` — it generates/updates that project's root `opencode.json`, bridge plugin, and reports. Do NOT copy `.opencode/skill-permissions.generated.json` or `.opencode/commands/`: both are generated per project by the `skills` stage, and a copied ledger is ignored anyway because it names the other project — why: a ledger from another project would otherwise claim the adopter's own `permission.skill` entries.

## Skill permissions

opencode lists every discovered skill to the model and ignores `disable-model-invocation`, so the `skills` stage (`.claude/scripts/opencode/sync-skills.mjs`) writes the framework's selection policy into `permission.skill` of the project-root `opencode.json`. A `deny` entry hides the skill from the model and rejects loading it through the skill tool.

| Skill | Effective tier or mark | `permission.skill` entry |
| --- | --- | --- |
| Command-only skill (`disable-model-invocation: true`) | — | `deny` |
| Workflow wrapper (skill name = a `.claude/workflows.json` id) | manual | `deny` |
| Workflow wrapper | confirm | `ask` |
| Workflow wrapper | auto | none |
| Skill in `skillProfile.nameOnly` | — | no entry from the profile; a stricter entry from a row above stays |
| Skill in `skillProfile.commandOnly` or `skillProfile.off` | — | `deny` plus a generated command, so `/name` still runs it |
| Any other skill | — | none |

- **Effective tier, team scope.** A wrapper follows its effective tier — the project override for that workflow, otherwise the stricter of its framework tier and the project default (`portability.workflowActivation` in the project config, default `docs/project-config.json`) — never the raw `workflows.json` value. The tier wins over the wrapper's own `disable-model-invocation` mark, so an override that loosens a manual workflow to `auto` removes its entry. `opencode.json` is a project file, so a developer's `.claude/.ck.local.json` never lands in it.
- **Called skills are never hidden.** A skill named as a step of any workflow (`sequence` or any `variants.*.sequence`), in an agent's `skills:` frontmatter list, or in the curated `calledByOthers` or `entrySkills` lists of `.claude/config/skill-profiles.json` gets no policy entry, and the run prints one line per skill: `skipped <name>: called by <callers>`. The called set has one owner, `resolveProfile().called` in `.claude/scripts/sync-skill-profile.cjs`. A `.claude/workflows.json` without a `workflows` map stops the stage instead of counting as empty.
- **Skill profile.** The `skillProfile` rows come from the same `resolveProfile()` as the Claude sync (read `.claude/config/README.md` → Skill profile when you need the presets and lists). `nameOnly` writes nothing, because an `ask` would stop every workflow step that loads the skill; it never loosens an entry the policy already writes. A called skill in `commandOnly` or `off` is refused unless `skillProfile.allowHidingCalledSkills` is `true`: the stage prints the resolver's message and `skill-profile: nothing was written`, exits non-zero, and `--check` fails the same way. With the opt-in the `deny` is written and a warning line names the skill. Resolver warnings print as `warning: skill profile: ...` only when `skillProfile` is declared. Profile entries go through the same ownership ledger, so a user key is never adopted, overwritten or loosened.
- **Ownership.** `.opencode/skill-permissions.generated.json` lists each key the generator owns, with the value it wrote. Only listed keys are updated or removed.
- **The ledger is bound to its project.** It records `project` = `project.name` from the project config (default `docs/project-config.json`; `.claude/.ck.json` `portability.projectConfigPath` relocates it), or `null` when there is none. A ledger whose `project` is missing or differs — copied from another project, or left over from a rename — is ignored with one line, `warning: ignored .opencode/skill-permissions.generated.json: it belongs to another project (...)`, owns nothing, and is rewritten for this project, so every entry already in `opencode.json` stays the user's. A project config that exists but is not valid JSON stops the stage before anything is written.

| Situation | Outcome |
| --- | --- |
| Key existed before the generator first wrote it | Kept and never recorded as owned; `conflict: permission.skill.<name> is <user value>, generator wants <value>; kept the user value` when it differs |
| Key listed only in a ledger from another project | Treated as the previous row: never owned |
| Owned key the user changed | Kept; the same conflict line |
| Owned key the user deleted | Restored to the policy value with no conflict line — set an explicit value such as `allow` to keep a skill loadable |
| `permission` or `permission.skill` is a single value, not a map | Unchanged; one conflict line; no skill entries written |
| Wildcard key such as `internal-*` | Always the user's; never rewritten |

- **Only the skill tool is restricted.** The stage writes no `read`, `edit` or other permission, so reading `.claude/skills/<name>/SKILL.md` by path keeps working for workflows that load a skill file directly.
- A skill folder whose name is not lowercase letters, digits and hyphens (`^[a-z0-9][a-z0-9-]*$`) is skipped with a warning.
- `--check` fails when `permission.skill`, the ledger or a generated command differs from a fresh sync. A kept user value or user command is not drift.

### Commands for hidden skills

A hidden skill keeps its explicit `/name`: the same stage writes `.opencode/commands/<name>.md` for every skill whose final exact `permission.skill` entry is `deny` — the policy's own entries and a user deny alike (wildcard keys are not evaluated). A skill the policy denies but whose kept user value is not `deny`, or whose entry could not be written because `permission` / `permission.skill` is not a map, gets no command.

```markdown
---
description: "<the skill description, whitespace collapsed, YAML-escaped>"
---

<!-- GENERATED OPENCODE COMMAND (sync-skills.mjs) for .claude/skills/<name>/SKILL.md — do not hand-edit; re-run:
     node .claude/skills/sync-opencode/scripts/run-opencode-sync.mjs -->

@.claude/skills/<name>/SKILL.md

Arguments: $ARGUMENTS
```

- **Name.** The command name is the skill folder name, never the `name:` inside the skill; the write path must resolve inside `.opencode/commands/`.
- **Marker ownership.** Only files carrying the `GENERATED OPENCODE COMMAND` marker are rewritten or deleted. A marked command whose skill is no longer hidden is removed.
- **Same-name user command.** A command without the marker that already uses a hidden skill's name — in `.opencode/commands/` or opencode's singular `.opencode/command/` folder — is kept unchanged, no generated command replaces it, and the run prints `conflict: <path> is a user command without the generated marker; kept it, no command generated for skill <name>`.
- **No shell in generated bodies.** Generated commands never contain `` !`…` ``. **Shell note:** opencode substitutes `$ARGUMENTS` before it runs `` !`cmd` `` injections, so typed arguments that themselves contain `` !`…` `` run as shell on that host. Do not paste untrusted text as command arguments.

## Hook mapping

| Claude hook event | opencode plugin surface | Notes |
| --- | --- | --- |
| `PreToolUse` | `tool.execute.before` | throw blocks the tool; `updatedInput` rewrites `output.args` |
| `PostToolUse` | `tool.execute.after` | `additionalContext` is appended to the tool output |
| `UserPromptSubmit` | `chat.message` | `additionalContext` is injected as a synthetic text part |
| `SessionStart` | `event:session.created` / `event:session.compacted` + `experimental.chat.system.transform` | `additionalContext` is injected into the system prompt |
| `SessionEnd` | `event:session.deleted` | |
| `Stop` | `event:session.idle` | |
| `Notification` | `event:question.asked` / `event:permission.asked` | matcher vocabulary `AskUserPrompt` / `permission_prompt` |
| `PermissionRequest` | `permission.ask` | blocked → `status: "deny"` |

**Tool id aliases** (opencode → Claude matcher names the hooks are written against):

| opencode tool | Claude matcher names |
| --- | --- |
| `bash` | `Bash` |
| `edit` | `Edit`, `MultiEdit` |
| `write` | `Write` |
| `read` | `Read` |
| `grep` | `Grep` |
| `glob` | `Glob` |
| `apply_patch` | `Edit`, `Write`, `MultiEdit`, `NotebookEdit` |
| `todowrite` | `TodoWrite`, task tracking, `TaskUpdate`, `update_plan` |
| `webfetch` / `websearch` | `WebFetch` / `WebSearch` |
| `question` | ask user tool |
| `skill` | skill invocation |
| `<server>_<tool>` (MCP) | `mcp__<server>__*` |

## Known limitations

- **MCP argument visibility.** opencode registers MCP tools as `<server>_<tool>`, and Claude matchers like `mcp__github__*` are matched against that convention. However, opencode does **not** expose MCP tool arguments to `tool.execute.before`, so an MCP `PreToolUse` hook that inspects `tool_input` cannot see them on this host.
- **`apply_patch` has no `file_path`.** The bridge reports it as `Edit`/`Write`/`MultiEdit` and passes `patchText` through as `patch`; hooks that require `file_path` (doc-sync-gate) allow/ignore it exactly as they do on other hosts.
- **Session resume.** `SessionStart` runs on `session.created` and `session.compacted`; when opencode resumes a session without either event, the bridge runs `source: "startup"` once on the first `chat.message`.
- **Claude-only stdout fields** other than `updatedInput`, `additionalContext`, and `permissionDecision` are ignored by the bridge.

## Usage

```bash
# Discover the stage roster:
node .claude/skills/sync-opencode/scripts/run-opencode-sync.mjs --list-stages

# Full sync + test + verify:
node .claude/skills/sync-opencode/scripts/run-opencode-sync.mjs

# Stream live child output:
node .claude/skills/sync-opencode/scripts/run-opencode-sync.mjs --verbose

# Every read-only gate (no mutation):
node .claude/skills/sync-opencode/scripts/run-opencode-sync.mjs --verify-only

# Just regenerate the plugin:
node .claude/scripts/opencode/sync-hooks.mjs

# Just verify the tracked plugin is current:
node .claude/scripts/opencode/sync-hooks.mjs --check

# Just reconcile the recommended root opencode.json:
node .claude/scripts/opencode/sync-config.mjs

# Just verify the root opencode.json is current:
node .claude/scripts/opencode/sync-config.mjs --check

# Just write the skill permissions:
node .claude/scripts/opencode/sync-skills.mjs

# Just verify the skill permissions are current:
node .claude/scripts/opencode/sync-skills.mjs --check

# Skip a stage while debugging:
node .claude/skills/sync-opencode/scripts/run-opencode-sync.mjs --skip=hooks
```

**Exit codes:** `0` all pass · `1` orchestrator failure · non-zero propagates from failing stage.

## Stages

9 stages, sequential — the complete opencode surface pipeline, owned entirely by this runner:

| # | Stage | Script | Effect |
| --- | --- | --- | --- |
| 1 | config | `.claude/scripts/opencode/sync-config.mjs` | Deep-merge `.opencode/opencode.recommended.json` into the project-root `opencode.json` |
| 2 | skills | `.claude/scripts/opencode/sync-skills.mjs` | Write `permission.skill` in the project-root `opencode.json`, the ownership ledger `.opencode/skill-permissions.generated.json`, and a marked `.opencode/commands/<name>.md` per hidden skill (see [Skill permissions](#skill-permissions)) |
| 3 | hooks | `.claude/scripts/opencode/sync-hooks.mjs` | Generate `.opencode/plugins/easy-claude-hooks.js` + `tmp/opencode-hooks.sync.report.json`; back up/remove legacy `notification.js` |
| 4 | agents | `.claude/scripts/opencode/sync-agents.mjs` | Mirror `.claude/agents/*.md` into `.opencode/agent/*.md` (`mode: subagent` + the canonical body verbatim) |
| 5 | tests | Runner discovers `.claude/scripts/opencode/tests/*.test.{mjs,cjs}` | Run opencode tooling tests; missing or empty discovery fails |
| 6 | verify-config | `.claude/scripts/opencode/sync-config.mjs --check` | Re-merge with the REAL writer and byte-compare with the project-root `opencode.json` |
| 7 | verify-skills | `.claude/scripts/opencode/sync-skills.mjs --check` | Re-plan with the REAL writer; fail when `permission.skill`, the ledger, or a generated command is missing, changed or stale |
| 8 | verify-hooks | `.claude/scripts/opencode/sync-hooks.mjs --check` | Re-render with the REAL writer and byte-compare with the tracked plugin |
| 9 | verify-agents | `.claude/scripts/opencode/sync-agents.mjs --check` | Re-render every agent with the REAL writer and byte-compare with the tracked `.opencode/agent/*.md` |

## Closing Reminders

**MUST ATTENTION** keep the `$sync-opencode` skill user-invoked-only; no unrelated skill, agent, or workflow may auto-run the mutating pipeline.
**MUST ATTENTION** edit `.claude/settings.json` and `.claude/hooks/**` as the source, then regenerate; NEVER hand-edit `.opencode/plugins/easy-claude-hooks.js`
**MUST ATTENTION** the framework's default opencode settings live in `.opencode/opencode.recommended.json` — edit THAT file to change defaults, then re-run this pipeline; never treat a project-root `opencode.json` as the source
**MUST ATTENTION** the generated plugin must import only `node:` built-ins so `.claude`/`.opencode` stay portable into any project
**MUST ATTENTION** the `config` stage deep-merges (recommended wins, project-only keys survive) and never clobbers a malformed root config — it reports instead
**MUST ATTENTION** the runner auto-resolves the repo root from its own path — do not pass a cwd flag
**MUST ATTENTION** the legacy `notification.js` is backed up, never destroyed, before removal

**Anti-Rationalization:**

| Evasion | Rebuttal |
| --- | --- |
| "Just edit the .opencode plugin directly" | Next sync overwrites it. Edit `.claude/settings.json` and regenerate. |
| "Just edit the project-root opencode.json to change the defaults" | The next sync re-merges the recommended file and your default is lost, and no other project gets it. Edit `.opencode/opencode.recommended.json` and re-run. |
| "Make the recommended file `.opencode/opencode.json`" | opencode auto-loads that exact path as project config, so it would stop being a template. Keep the `.recommended.json` name. |
| "Skip the tests stage" | The tests exercise the generated plugin against real hook subprocesses; skipping ships an untested bridge. |
| "Mirror skills too for symmetry with sync-codex" | opencode already discovers `.claude/skills`; a mirror would duplicate and drift. Out of scope by design. |

> **[FAILS FAST]** First non-zero stage exit aborts the chain. Re-run the failing stage with `--only=<id> --verbose`.
> **[REPO ROOT]** The orchestrator auto-resolves the repo root from its own path.
