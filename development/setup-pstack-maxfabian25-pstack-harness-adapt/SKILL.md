---
name: setup-pstack
description: Configure which models pstack uses per role and at what reasoning budget, in Claude Code and Codex. Detects your available models, writes the shared pstack model config, and installs pstack's Codex custom agents. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack

Write `~/.config/pstack/models.md`, the config that sets pstack's model per role in both harnesses, and install pstack's Codex custom agents. Role names, value syntax, and defaults are in [harnesses.md](../poteto-mode/references/harnesses.md) (Models). Read it first.

## Steps

### 1. Detect available models

Detect what each harness can run. Never write a real model you have not confirmed is available. `inherit-parent` and `auto` are always valid even though they are not detected models.

- **Claude Code.** The `Agent` tool's `model` parameter lists the values it accepts, usually the aliases `opus`, `sonnet`, `haiku`, and `fable`. Write only values it lists. The `claude` CLI accepts the same aliases for a `claude:` seat, and `claude auth status` shows whether it is signed in.
- **Codex.** Read the model list from `~/.codex/models_cache.json` (entries with `visibility` `list`) or run `codex debug models` if it exists. Note whether `spawn_agent` exposes a `model` parameter in this session. Without it, native Codex seats inherit the parent model and only the effort applies.
- **Cross-harness CLIs.** Run `codex --version` and `claude --version`. A missing CLI means `codex:` or `claude:` values cannot run. Mark those roles as needing a choice.

If you cannot detect anything for a harness, ask the user to paste the models they have access to.

### 2. Load current state

Start from the defaults in harnesses.md (Defaults). If `~/.config/pstack/models.md` exists, read it and treat its `# budget:` line and its role values as the current choices. If the legacy Cursor rule `~/.cursor/rules/pstack-models.mdc` exists and the new file does not, read its role lines as hints for the user, but never copy a Grok or other unavailable model into the new file. A line whose role is not in the Defaults table, such as `how critics`, is from a retired role. Drop it.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Use the question tool (Claude Code `AskUserQuestion`, Codex `request_user_input`) over free text. Offer these four options with these exact labels, and name the current budget when the config records one. With no config, say that `large` matches the defaults.

- `unlimited — max reasoning`
- `large — xhigh reasoning`
- `medium — high reasoning`
- `small — medium reasoning`

**(b) Apply it.** Build the working table from the defaults, and on a re-run keep any role the user changed. `unlimited`, `large`, `medium`, and `small` set the `@<effort>` of every value, panel entries and cross-harness entries included, to `max`, `xhigh`, `high`, or `medium`. A model that cannot run at that effort uses its highest effort below it. `inherit-parent` and `auto` keep their meaning and take the new effort.

**(c) Show the roles and confirm.** Show every role with its Claude Code value and its Codex value, marking any value that step 1 could not confirm as needing a choice. Also list each line step 2 dropped. Ask whether to accept as-is or change specific roles, offering the detected models, the cross-harness forms (`codex:<model>` from Claude Code, `claude:<model>` from Codex), and `inherit-parent` as the options. Use the question tool over free text.

- Panel roles (`arena runners`, `architect runners`, `interrogate reviewers`) take a list. One seat runs per entry, alias entries included, so the list length sets the count. Keep at least one entry from each model family unless the user chooses a single family. A single-family panel gives weaker agreement signal. Say so when the user picks it.
- `arena cross-judge pool` is also a list. Arena picks the entry whose family differs from the parent's when possible.
- `swarm workers` is the default model for every worker unless a race or comparison assigns another model per arm.

### 4. Validate

Every real model written must be in the detected set for its harness. Every `codex:` or `claude:` value needs that CLI installed. `inherit-parent` and `auto` always pass. If a chosen value is not available, stop and ask again.

### 5. Write the config

Write `~/.config/pstack/models.md`. Create `~/.config/pstack/` if needed. Overwrite the whole file so re-runs stay idempotent. Shape:

```
# pstack model configuration. Read by pstack skills in Claude Code and Codex.
# One line per role. Delete a line to fall back to the default in harnesses.md.
# Value: <model>@<effort>, or a comma list for a panel. inherit-parent runs on the parent chat model.
# codex:<model> (from Claude Code) and claude:<model> (from Codex) run the seat in the other harness's CLI.
# budget: large (xhigh)

## claude-code
feature, refactoring: sonnet@xhigh
bug-fix: sonnet@xhigh
perf-issue: sonnet@xhigh
hillclimb: sonnet@xhigh
judgment and prose: opus@xhigh
hardest tasks: opus@xhigh
how explorer: sonnet@xhigh
how explainer: opus@xhigh
why investigators: sonnet@xhigh
why synthesizer: opus@xhigh
reflect tooling: sonnet@xhigh
reflect judgment, divergent, synthesizer: opus@xhigh
arena runners: opus@xhigh, codex:gpt-6.1-sol@xhigh
arena cross-judge pool: opus@xhigh, codex:gpt-6.1-sol@xhigh
swarm workers: sonnet@xhigh
architect runners: opus@xhigh, codex:gpt-6.1-sol@xhigh
interrogate reviewers: opus@xhigh, codex:gpt-6.1-sol@xhigh

## codex
feature, refactoring: inherit-parent@xhigh
bug-fix: inherit-parent@xhigh
perf-issue: inherit-parent@xhigh
hillclimb: inherit-parent@xhigh
judgment and prose: inherit-parent@xhigh
hardest tasks: inherit-parent@xhigh
how explorer: inherit-parent@xhigh
how explainer: inherit-parent@xhigh
why investigators: inherit-parent@xhigh
why synthesizer: inherit-parent@xhigh
reflect tooling: inherit-parent@xhigh
reflect judgment, divergent, synthesizer: inherit-parent@xhigh
arena runners: inherit-parent@xhigh, claude:opus@xhigh
arena cross-judge pool: inherit-parent@xhigh, claude:opus@xhigh
swarm workers: inherit-parent@xhigh
architect runners: inherit-parent@xhigh, claude:opus@xhigh
interrogate reviewers: inherit-parent@xhigh, claude:opus@xhigh
```

### 6. Install the Codex custom agents

pstack's skills spawn three Codex custom agents: `poteto-agent`, `comment-sicko`, and `pstack-reader`. Their definitions ship in this plugin's `agents/codex/` folder, two levels above this skill's directory. Copy each `.toml` file to `~/.codex/agents/`, creating the folder if needed. Before overwriting an existing file with the same name, compare it. If it differs from the shipped file and pstack did not write it, ask before replacing it. Re-run this step after a pstack update so the agents track the plugin. Claude Code needs no install step, because the plugin registers its agents as `pstack:poteto-agent` and `pstack:comment-sicko`.

### 7. Confirm

Tell the user the config was written, which Codex agents were installed or left unchanged, and that both apply to new sessions and new subagents. Re-running this skill updates them.

### 8. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." (In Codex, `$create-verification-skill`.) On yes, invoke the create-verification-skill skill. On no, move on without pushing.

### 9. Offer a formal verification skill (optional)

Check whether the project already has a formal verification skill (a project skill that runs a model checker, a proof, or another verifier against the code). If not, offer once: "want a formal verification skill, so agents can prove a key property of your code holds in every case in scope, not only the cases tests reach? I can generate one with /create-formal-verification-skill." (In Codex, `$create-formal-verification-skill`.) On yes, invoke the create-formal-verification-skill skill. On no, move on without pushing.
