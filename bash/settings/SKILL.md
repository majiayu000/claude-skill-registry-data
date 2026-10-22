---
name: settings
description: Inspects or changes the Codex reviewer model, reasoning effort, and review-round limit for check-loop.
argument-hint: "[--project] [--model ID|default] [--effort LEVEL|default] [--max-rounds N] [--implementer-model ID|default]"
---

# Check-loop settings

Inspect and change only the settings the user requests. Do not edit configuration files directly.

**In pi:** pi does not substitute `${CLAUDE_PLUGIN_ROOT}`; replace it with the absolute path two directories above this SKILL.md. `$ARGUMENTS` is the text appended after `/skill:settings`.

## Interface

Treat `$ARGUMENTS` as flags for:

```text
config [--cwd PATH] [--project] [--model ID|default] [--effort LEVEL|default] [--max-rounds N] [--implementer-model ID|default]
```

Resolve `TARGET_CWD` from `--cwd` when supplied; otherwise use the current working directory. Use that same absolute target for inspection, project scope, and the write command. Do not treat `--cwd` as a setting to persist.

- `--project` selects project scope. Without it, setters use user scope.
- `--model default` and `--effort default` store `null`, clearing that scope's override so Codex configuration is inherited.
- `--max-rounds` must be an integer from 1 through 40. Its default is 6.
- `--implementer-model` sets the model `execute` requests for its implementer and fixer subagents. It is not a Codex setting. `default` stores `null`, which inherits the session model. Use the host's model naming: a Claude Code alias or ID such as `opus` or `sonnet`, or a pi `provider/id`.
- Reject unexpected options and positional arguments. Never silently ignore a requested setting.

Settings resolve independently per key in this order:

1. CLI value for the current invocation.
2. Project `.claude/check-loop.json` under `--cwd`.
3. User `check-loop/config.json` under `$CLAUDE_CONFIG_DIR` when set, otherwise `~/.claude/check-loop/config.json`.
4. Defaults: `model: null`, `effort: null`, `maxRounds: 6`, `implementerModel: null`.

A higher-precedence `null` model or effort intentionally clears a lower-precedence value and selects the Codex default.

## Inspect first

Always inspect the effective settings before proposing or applying a change, using the resolved target directory:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" config --cwd "TARGET_CWD"
```

The command prints exactly one resolved JSON object:

```json
{"model":null,"effort":null,"maxRounds":6,"implementerModel":null}
```

Explain null `model` or `effort` as `Codex default` and null `implementerModel` as `session model`, not as a particular model or effort. This command reads configuration; it does not prove that a model is available.

If no setters were supplied, show the effective values and let the user choose:

- which of model, effort, maximum review rounds, or implementer model to change;
- user scope or project scope;
- the new value for each chosen key.

Do not write anything until the user chooses at least one setting. If setter flags were supplied, use exactly those setters. The default setter scope is user scope unless `--project` is present.

For an exact model ID, use the user's known Codex selection or an ID supported by actual availability evidence already obtained from Codex. Do not invent model IDs or present a guessed catalog. Use the exact effort value the user supplies or one supported by actual Codex evidence. Offer `default` whenever the user wants Codex to choose.

## Apply the requested subset

Construct one command containing `--cwd`, the selected scope, and only the requested setter flags. Examples:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" config \
  --cwd "TARGET_CWD" \
  --model "EXACT_USER_SELECTED_ID"

# Project scope: inherit Codex effort and change only the round limit
node "${CLAUDE_PLUGIN_ROOT}/scripts/codex-invoke.mjs" config \
  --cwd "TARGET_CWD" \
  --project \
  --effort default \
  --max-rounds 8
```

Never add an omitted model, effort, round-limit, or implementer-model flag. The command persists only the specified keys and prints the newly resolved JSON object.

Inspect once more with the no-setter command, then report:

- scope written (`user` or `project`);
- keys changed and their requested values;
- effective `{model, effort, maxRounds, implementerModel}` after precedence;
- that model availability is checked only when a review starts.

Do not claim that `setup` or configuration inspection tested model access. Do not start a review, alter unrelated settings, or create a durable loop state from this skill.
