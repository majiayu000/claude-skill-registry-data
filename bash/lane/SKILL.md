---
name: lane
description: Control the local Lane AI gateway from an agent or script.
---

# Lane CLI

Use `lane` to inspect or control the user's local Lane gateway. The user must
first open the packaged Lane app and choose **Settings → Command line →
Install…**. This is a one-time macOS authorization.

## Agent-safe commands

Always request JSON and disable prompts:

```bash
lane status --json --no-input
lane start --json --no-input
lane stop --json --no-input
lane connection --json --no-input
lane providers list --json --no-input
lane models --json --no-input
lane open --json --no-input
lane schema --json --no-input
```

Add an API-key provider without exposing the secret in process arguments:

```bash
printf '%s\n' "$OPENAI_API_KEY" |
  lane providers add --kind openai --api-key-stdin --json --no-input
```

Provider removal is destructive and requires explicit confirmation:

```bash
lane providers remove --id PROVIDER_ID --force --json --no-input
```

Set the fallback model and inspect redacted diagnostics:

```bash
lane models set-default --id PROVIDER_ID/MODEL_ID --json --no-input
lane activity --json --no-input
```

Read `lane schema --json` instead of guessing supported commands. Exit code `0`
means success, `2` means invalid usage, `4` means the integration is unavailable,
and `8` means a retryable service failure.

## Safety boundary

`lane connection` returns the Lane client key because it is required to call the
gateway. Provider API keys are write-only through stdin. Stored provider API keys
and OAuth tokens are never returned. UI-only preferences such as theme, Dock, and
menu bar visibility stay in the app.
