---
name: superdev-setup
description: Configure a repository for SuperDev with its issue tracker, triage labels, Wayfinder setup, domain docs, per-role models, and routing. Use for /superdev-setup, first-time setup, or changes to repository conventions or model configuration.
---

# SuperDev setup

On Codex, read the [platform mapping](../superdev-mode/references/codex-tools.md), including its per-skill notes, before following this skill.

On GitHub Copilot, read the [platform mapping](../superdev-mode/references/copilot-tools.md), including its per-skill notes, before following this skill.

On Muse, read the [platform mapping](../superdev-mode/references/muse-tools.md), including its per-skill notes, before following this skill.

Read [the portable runtime contract](../superdev-mode/references/portable-runtime.md) before following this workflow.

On GitHub Copilot, follow [the Copilot setup](copilot.md) in place of steps 1, 3, 4, and 7 and step 6's header.

On another runtime, read [Other runtimes](#other-runtimes) below for where the sheet lives and how it loads; the steps are the same.

## Setup scope

Repository setup adds the conventions consumed by the engineering skills. It does not replace the runtime-aware model setup below, including role models, reasoning effort, routing, and the verification-skill offers.

For a first-time setup or a general rerun, complete both parts in order:

1. Read and follow [repository setup](references/repository-setup.md).
2. Follow the model setup steps below.

When the user asks to change only the issue tracker, GitHub labels, triage mappings, or domain docs, run only repository setup and finish without running model setup. Within repository setup, run only the sections needed for that change. When the user asks to change only models, reasoning effort, or routing, run only model setup. A workflow invoking this skill to repair a missing or invalid model sheet is also a model-only request.

Inspect current files before editing. Preserve choices outside the requested change and update existing configuration instead of creating duplicates.

For model setup, write the current runtime's per-role model override sheet, using the path in [Other runtimes](#other-runtimes). Each superdev skill names a default model inline; the override sheet adapts those defaults to the models you actually have access to.

Claude Code has no auto-applied "rules" mechanism like Cursor's `.mdc`. The Claude Code config directory is `$CLAUDE_CONFIG_DIR` when that variable is set and `~/.claude` otherwise. This skill calls it `<config>`. Inclusion is explicit: the user adds a line to `<config>/CLAUDE.md` (or their project `CLAUDE.md`) such as:

```text
@<config>/superdev-models.md
```

with `<config>` written as the resolved path, so the file is loaded as context for every session.

The Codex home directory is `$CODEX_HOME` when that variable is set and `~/.codex` otherwise. This skill calls it `<codex-home>`.

## Model setup

### 1. Detect available models

Enumerate the model names the `Agent` tool's `model` parameter accepts in this session. That is the dependable source. On Claude Code they are the family names listed in [Models](#models) below, each running that family's current model, and a full model ID is rejected. The default panel is listed there too. The panel is chosen for cross-family diversity. Ask the user to confirm or paste any additional slugs they want available. Never write a real slug you have not confirmed is available. The aliases `inherit-parent` and `auto` are always valid even though they are not detected slugs. Both mean the role runs on the parent session's model, which the `Agent` call expresses by omitting `model`.

### 2. Load current state

The default role-to-model mapping is the rule shape shown in the Write the override sheet step below. If the current runtime's sheet already exists, read it and treat its values as the current choices. Otherwise start from those defaults. A line whose role is not in that shape, such as `how critics`, is from a retired role. Drop it. An older sheet may name full model IDs that start with `claude-`, which the `Agent` tool rejects. Replace each with its family name, the word after `claude-`.

### 3. Map and confirm

Show every role with its current model, marking any real slug not in the detected set as needing a choice. Also list each line step 2 dropped or rewrote. Ask whether to accept as-is or change specific roles, offering the detected models plus `inherit-parent` and `auto` as the options. Prefer `AskUserQuestion` over free text. For panel roles (arena runners, architect runners, interrogate reviewers) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list, but Arena selects one value from it whose model family differs from the parent's when possible. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

Then ask for the default reasoning effort, the `default effort` line. It is `session`, which keeps the parent session's effort, or one of the levels in [Models](#models). Start from the default listed there. Every role value without a suffix runs at it. Then ask whether any role should run at another level. On Claude Code a role value may carry one after its slug, as in `<slug> @xhigh`; panel entries take their own, as in `<slug> @xhigh, <slug> @max`. Each level is passed as the dispatch's effort, so the choice holds without changing the session. Leave the suffix off for the default effort.

### 4. Choose whether the session hook routes tasks

On Claude Code and Codex, the plugin's `SessionStart` hook injects the superdev-mode mandate on startup, resume, clear, and compact. Codex asks the user to trust plugin hooks through `/hooks` before running them. On Pi, the superdev extension adds the same mandate to the system prompt at every agent start. On Muse, the native plugin's `SessionStart` hook injects the mandate once the user approves the plugin's hooks with `muse plugins approve superdev`. Ask whether to keep the hook. The default is on. The answer is the `session hook` line in the current runtime's sheet: `on` or `off`. With no sheet or no line, the hook injects. The line is inert on other runtimes.

### 5. Validate

Every real slug written must be in the detected set. `inherit-parent` and `auto` always pass. Validate the slug without any `@<level>` suffix, and the level against the effort levels in [Models](#models). The `default effort` value is one of those levels or `session`. On Codex, the levels are the `reasoning_effort` values your Codex models accept instead. If a chosen real slug or level is not available, stop and ask again.

### 6. Write the override sheet

Write the current runtime's sheet with the shape below. Overwrite the whole file so re-runs stay idempotent.

```markdown
# superdev model configuration

Per-role model overrides for superdev skills. Each superdev SKILL.md names its defaults in a Models section; the values here override those defaults. Delete a line to fall back to the skill default. A value of `inherit-parent` or `auto` runs that role on the parent session's model (the `Agent` call omits `model`); an alias entry in a panel list still counts toward that panel's fan-out. A model may carry a reasoning effort, as in `opus @xhigh` (levels: low, medium, high, xhigh, max); the role's subagent then runs at that level, each entry of a panel list on its own. `default effort` sets the level for a value without one; `session` keeps the parent session's effort. `session hook: off` stops the Claude Code, Codex, or Muse SessionStart hook, or the superdev Pi extension, from injecting the superdev-mode mandate; any other value, or no line, leaves it on.

feature, refactoring: sonnet
bug-fix: opus
perf-issue: opus
hillclimb: opus
judgment and prose: opus
strongest judgment: fable
how explorer: opus
how explainer: opus
why investigators: opus
why synthesizer: opus
reflect tooling: opus
reflect judgment, divergent, synthesizer: opus
arena runners: opus, fable, sonnet, haiku
arena cross-judge pool: opus, fable, sonnet, haiku
swarm workers: opus
architect runners: opus, fable, sonnet, haiku
interrogate reviewers: opus, fable, sonnet, haiku

default effort: session
session hook: on
```

### 7. Wire it in

On Claude Code, if `<config>/CLAUDE.md` does not already include `<config>/superdev-models.md`, append an `@` line naming the sheet's resolved path, such as `@~/.claude/superdev-models.md`, so the model rows load on every session. If the user prefers project scope, add the include to the project's `CLAUDE.md` instead.

On Codex, paste the model rows and the `default effort` line into `<codex-home>/AGENTS.md`; Codex has no `@` include. Do not paste the `session hook` line there: the plugin hook reads it directly from `<codex-home>/superdev-models.md`.

On Muse, no include line is needed: the plugin hook reads the sheet directly and injects its role lines at session start. It runs only after the user approves the plugin's hooks, so name `muse plugins approve superdev` when the hook has not run yet.

### 8. Confirm

Tell the user where the override was written, how its model rows load, and whether the plugin hook is on. Re-running this skill updates the override sheet.

### 9. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a project `verify` or `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, invoke [`/create-verification-skill`](../create-verification-skill/SKILL.md). On no, move on without pushing.

### 10. Offer a formal verification skill (optional)

Check whether the project already has a formal verification skill (a project skill that runs a model checker, a proof, or another verifier against the code). If not, offer once: "want a formal verification skill, so agents can prove a key property of your code holds in every case in scope, not only the cases tests reach? I can generate one with /create-formal-verification-skill." On yes, invoke [`/create-formal-verification-skill`](../create-formal-verification-skill/SKILL.md). On no, move on without pushing.

## Other runtimes

The role lines are the same everywhere. What differs is the sheet path, how the runtime loads it, and how you list models. Detect models with the runtime's own tool and never write a slug you have not seen listed. A runtime whose subagent call has no model parameter still gets the sheet, as the record of the user's choice, and applies it where it can. The `session hook` line applies to the Claude Code, Codex, and GitHub Copilot plugins and to the superdev Pi extension.

| Runtime | Sheet | Load | List models | Status |
| --- | --- | --- | --- | --- |
| Claude Code | `<config>/superdev-models.md` | `@<config>/superdev-models.md` in `<config>/CLAUDE.md` | the `Agent` tool's model parameter | verified live |
| Codex | `<codex-home>/superdev-models.md` | model rows: paste into `<codex-home>/AGENTS.md`; hook setting: read by the plugin | your configured Codex models, see [codex-tools.md](../superdev-mode/references/codex-tools.md#model-names) | hook contract tested; discovery verified |
| Pi | `superdev-models.md` in the Pi agent directory, `$PI_CODING_AGENT_DIR` or `~/.pi/agent` | read by the superdev Pi extension, model rows and hook setting both; no include line | `pi --list-models`, see [pi-tools.md](../superdev-mode/references/pi-tools.md#model-names) and its `superdev-setup` note | extension contract tested offline; live results in the repository's `docs/pi-equivalence.md` |
| GitHub Copilot (CLI and app) | `${COPILOT_HOME:-~/.copilot}/superdev-models.md` | the plugin hook checks it and injects its role lines at session start; skills-only installs read it with `view` | the `task` tool's `model` enum, see [copilot-tools.md](../superdev-mode/references/copilot-tools.md#model-names) | hook contract tested; CLI install smoke-tested |
| Muse | `${XDG_CONFIG_HOME:-~/.config}/muse/superdev-models.md` | the plugin hook reads it and injects its role lines at session start, once hooks are approved; no include line | the model catalog (`muse model-profile show <model>` names each one), see [muse-tools.md](../superdev-mode/references/muse-tools.md#model-names) | hook contract tested; plugin install verified |
| opencode | `~/.config/opencode/superdev-models.md` | add the path to the `instructions` array in `opencode.json` | the `models` slash command in the session | from published docs, no live session |
| Gemini CLI | `~/.gemini/superdev-models.md` | `@~/.gemini/superdev-models.md` in `~/.gemini/GEMINI.md` | the `model` slash command in the session | from published docs, no live session |
| Prime Agent | no documented sheet path; Prime's configuration chooses models | | | no live session |

## Models

Stamped from `plugins/superdev/models.json` (edit there, rerun `tools/generate.mjs`).

- Available Claude models: `opus`, `fable`, `sonnet`, `haiku`
- Default panel: `opus`, `fable`, `sonnet`, `haiku`
- Reasoning effort levels: `low`, `medium`, `high`, `xhigh`, `max`
- Default reasoning effort: `session`
- Single-role default: `opus`
