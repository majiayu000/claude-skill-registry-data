---
name: setup-huajar-stack
description: Configure which models huajar-stack uses per role, and at what reasoning budget. Detects your available models and writes an always-applied rule that overrides the skill defaults. Use for /huajar-stack:setup-huajar-stack, "configure huajar-stack models", "huajar-stack budget", or changing huajar-stack's model choices.
---

# Setup huajar-stack

In Claude Code, read [the Claude Code adapter](../../docs/harness/claude-code.md) once per session before you follow this skill. It maps the Cursor names in pstack skills to Claude Code.

Write `~/.claude/rules/huajar-stack-models.md`, an always-applied rule that sets huajar-stack's model per role.

## Steps

### 1. Detect available models

Enumerate the model slugs you can run as an `Agent` subagent in this session. `Agent` takes a model alias and an effort level as two parameters. A slug joins the model ID that your system prompt gives for an alias with an effort level that `Agent` accepts, so `opus` and `xhigh` make `claude-opus-5-5-xhigh`. That is the dependable source. If you cannot detect any, ask the user to paste the slugs they have access to. Never write a real slug you have not confirmed is available. The aliases `inherit-parent` and `auto` are always valid even though they are not detected slugs.

Then detect seats, models that another agent CLI runs in its own `hc` terminal, per `<huajar-stack>/skills/huajar-mode/references/seats.md`. Skip this when `HC_TERMINAL_ID` is empty. A seat entry is `<agent>:<model>-<effort>`.

- `agy models` lists each id with its effort, such as `gemini-4-neon-xhigh` or `claude-opus-5-5-medium`. Each id makes the entry `agy:<id>`.
- `codex debug models` prints JSON. Each model whose `visibility` is `list` makes one entry per effort in its `supported_reasoning_levels`, such as `codex:gpt-6.2-sol-high`.

A CLI that is not installed, or whose command fails, adds no entries.

### 2. Load current state

The default role-to-model mapping is the rule shape shown in step 5 below. If `~/.claude/rules/huajar-stack-models.md` already exists, read it and treat its `# budget` line and its role values as the current choices. Otherwise start from those defaults. A line whose role is neither in step 5 nor one of step 3's two `swarm mechanical` lines, such as `hardest tasks`, `architect runners`, `reflect tooling`, or `why investigators`, is from a retired role. Drop it. A `# quota cap` or `# local ceiling` line is from a retired setting. Drop it too.

A rule without the `# defaults: 3` line comes from an older setup. That setup wrote a line for every role, so some of its values are old defaults, not choices. Before step 3, replace these values:

- A `claude-sonnet-*` value in `feature, refactoring`, `bug-fix`, `perf-issue`, or `hillclimb` takes the role's step 5 default.
- An `arena runners` list of exactly one `claude-opus-*` entry and one `claude-haiku-*` entry, or an `interrogate reviewers` list of exactly one `claude-opus-*` entry and one `claude-sonnet-*` entry, in either order, takes the role's step 5 list.
- A `# budget: unlimited` line becomes `large`, because no role runs above `xhigh`.

Every other value is the user's choice and stays, including every `inherit-parent` or `auto` value. Tell the user which values you replaced.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Prefer AskUserQuestion over free text. Offer these three options with these exact labels, and name the current budget when the rule records one. With no rule, say that `medium` matches the skill defaults.

- `large — xhigh reasoning`
- `medium — medium reasoning`
- `small — low reasoning`

**(b) Apply it.** Build the working table from the skill defaults, and on a re-run keep any role you changed by family, list, or alias (`inherit-parent`, `auto`). Families are the ones Phase A of the **arena** skill defines, so Fable is its own family. `large`, `medium`, and `small` set the effort token of every real slug, panel entries included, to `xhigh`, `medium`, or `low`. No role runs above `xhigh`. The effort token is the last token, in the order `xhigh` > `high` > `medium` > `low`. If the result is not a detected slug, use the same family's detected slug with the highest effort at or below the target, else mark the role as needing a choice. `inherit-parent`, `auto`, and seat entries do not change, because a seat's levels are not Claude's. So `large` turns `claude-opus-5-5-medium` into `claude-opus-5-5-xhigh`, `medium` keeps the defaults, and `small` turns them into `claude-opus-5-5-low`, `claude-fable-5-2-low`, and `claude-sonnet-5-5-low`.

**(c) Show the roles and confirm.** Show every role with its model, marking any real slug not in the detected set as needing a choice. Also list each line step 2 dropped. Ask whether to accept as-is or change specific roles, offering the detected models at `xhigh` or below plus `inherit-parent` and `auto` as the options. Both mean the role runs on the parent chat model. Prefer AskUserQuestion over free text. For panel roles (arena runners, interrogate reviewers) the value is a list, and one subagent runs per entry, alias entries included, so the list length sets the count. `arena cross-judge pool` is also a list. Its default is one Opus entry, which runs the cross-judge. `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm. Offer the detected seat entries too, at any level. Two lines have no default and are written only when the user picks a value. `swarm mechanical code` and `swarm mechanical text` run the swarm slices whose brief fixes the result, a check proves it, and no design choice is left, split by whether the slice changes code or prose. Other slices, and verification, stay on `swarm workers`.

### 4. Validate

Every real slug written must be in the detected set and at `xhigh` or below. `inherit-parent` and `auto` always pass. A seat entry must be in step 1's seat entries. If a chosen real slug or seat entry is not available, stop and ask again.

### 5. Write the rule

Write `~/.claude/rules/huajar-stack-models.md` with no frontmatter, a `# budget` line with the chosen label and its target effort, and one line per role, using the same labels huajar-mode uses. Claude Code loads a rule without `paths` frontmatter in every session. Overwrite the whole file so re-runs stay idempotent. Shape:

```
# huajar-stack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit-parent` or `auto` as a value: the role runs on the parent chat model (omit Agent `model` and `effort`). Alias entries in a panel list still count toward its fan-out.
# A slug is `claude-<family>-<version>-<effort>`. Pass `<family>` as Agent `model` and `<effort>` as Agent `effort`; the version is not used.
# A seat entry is `<agent>:<model>-<effort>`, such as `agy:gemini-4-neon-xhigh`: an hc seat per seats.md, never an Agent call.
# defaults: 3
# budget: medium (medium)
feature, refactoring: claude-opus-5-5-medium
bug-fix: claude-opus-5-5-medium
perf-issue: claude-opus-5-5-medium
hillclimb: claude-opus-5-5-medium
judgment and prose: claude-opus-5-5-medium
arena runners: claude-fable-5-2-medium, claude-opus-5-5-medium, claude-sonnet-5-5-medium
arena cross-judge pool: claude-opus-5-5-medium
swarm workers: claude-opus-5-5-medium
interrogate reviewers: claude-fable-5-2-medium, claude-opus-5-5-medium, claude-sonnet-5-5-medium
```

### 6. Confirm

Tell the user the rule was written and that it applies to new sessions. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /huajar-stack:create-verification-skill." On yes, invoke `/huajar-stack:create-verification-skill` (resolves wherever huajar-stack is installed: workspace, user, or plugin). On no, move on without pushing.

### 8. Offer a formal verification skill (optional)

Check whether the project already has a formal verification skill (a project skill that runs a model checker, a proof, or another verifier against the code). If not, offer once: "want a formal verification skill, so agents can prove a key property of your code holds in every case in scope, not only the cases tests reach? I can generate one with /huajar-stack:create-formal-verification-skill." On yes, invoke `/huajar-stack:create-formal-verification-skill` (resolves wherever huajar-stack is installed: workspace, user, or plugin). On no, move on without pushing.
