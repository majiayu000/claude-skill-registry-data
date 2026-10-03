---
name: model-upgrade
description: Checklist for changing the default Copilot coding agent model. Use when upgrading from one model to another (e.g. gpt-5.3-codex to gpt-5.4) to ensure all locations are updated consistently.
user-invocable: false
---

# Changing the Default Copilot Agent Model

The default model is now stored in `tools/config.json`, and Rust tools read it via the shared `state-schema` helper. For normal model upgrades, you should only need to update the shared config plus the human-facing documentation references.

## Locations to update

### 1. Shared config — executable default

File: `tools/config.json`

Update `"default_model"` to the new preferred model. This is the runtime source of truth used by `record-dispatch` when `--model` is omitted, and tests in `record-dispatch` / `process-merge` derive from it.

### 2. System prompt — dispatch examples

File: `.github/workflows/orchestrator-prompt.xml`

The `agent_assignment` JSON blocks in the "How to dispatch agent tasks" section contain a `"model"` field. Update both examples (create-and-assign, assign-existing).

Search for: `"model": "<old-model>"`

### 3. System prompt — model selection table

Same file. The table under "Model selection" lists available models with descriptions. Update the table rows and the prose below it (`Prefer <model> for routine work...`).

### 4. System prompt — operating principles

Same file. Operating principle #6 references the preferred model by name. Update it.

### 5. Verify the shared config is wired through the tools

No Rust source edits should be needed for the executable default itself. Instead, verify that `record-dispatch` still loads the configured default and that related tests pass.

```bash
cd tools/rust && cargo test --quiet
```

All tests must pass after the update.

## Locations to NOT update

- **`backfill-sessions`** — This tool reconstructs historical session data. Its test fixtures reflect actual past dispatches and should retain the model that was used at the time.
- **`docs/state.json`** — Historical `agent_sessions` entries record the model that was actually used. Do not retroactively change them. Only new dispatches will use the new model.
- **Worklog/journal entries** — These are historical records. Never alter them.

## Quick grep to find remaining documentation references

```bash
grep -rn '"<old-model>"' .github/workflows/orchestrator-prompt.xml tools/config.json
```

## Common mistake

Updating only the system prompt but not `tools/config.json`. The system prompt tells the orchestrator what model to prefer, but `record-dispatch` uses the shared config when `--model` is omitted, so the config must stay in sync with the docs.
