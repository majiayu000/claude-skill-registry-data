---
name: secrets-cli
description: Operates the DP Secrets CLI (`secrets`) for installation, authentication, project membership, environments, dotenv files, pulls, and secret values. Use before any agent runs a `secrets` command or when the user mentions the Secrets CLI, `secrets login`, `secrets projects`, `secrets envs`, `secrets files`, `secrets values`, or the compatibility `secrets secrets` tree.
metadata: {"DP Secrets":{"entrypoint":true}}
---

# secrets-cli

Operate the `secrets` executable without exposing secret material or guessing selectors.

## 1. Activate Before Execution

Before running any `secrets` command, explicitly announce: `Activating secrets-cli before running secrets.`

If this skill is unavailable, stop. Install it, then activate it before continuing:

```bash
npx skills add https://github.com/wearedevpunks/skills/tree/main/skills/misc/secrets-cli --skill secrets-cli --global --yes
```

Never run `secrets`, including `secrets --help` or `secrets --version`, without this activation.

## 2. Load the Needed Reference

- Read [references/command-reference.md](references/command-reference.md) before constructing or checking command syntax.
- Read [references/workflows.md](references/workflows.md) for install, auth, membership, setup, pull, value, and cleanup sequences.
- Read [references/safety-and-errors.md](references/safety-and-errors.md) before handling values, stdin, pulls, destructive work, failures, or exit codes.

## 3. Establish Context

1. Confirm the CLI is installed with `secrets --version`; install or update only when needed.
2. Confirm identity with `secrets whoami`; use `secrets login` when unauthenticated or expired.
3. Resolve the project, environment, file, and value scope before mutation. Prefer explicit selectors when inference is uncertain.
4. List the target immediately before destructive or overwrite-capable work.

Context is established when identity and every selector needed by the chosen leaf command are known.

## 4. Execute the Smallest Workflow

Use one leaf command at a time. Prefer `secrets values`; use `secrets secrets` only for compatibility with existing automation.

Send sensitive input through `--stdin`. Never place secret values in commentary, logs, summaries, command echoes, or verification output. For pulls, inspect the plan and target paths before approval.

## 5. Verify Completion

Completion requires all applicable checks:

- the command exited `0`
- a follow-up list, identity check, or filesystem check confirms the intended state
- pulled files exist at the configured paths and overwrite impact was accepted
- output and handoff text contain key names only, never secret values
- destructive cleanup followed leaf-to-root order and no intended active resource remains

If any check fails, report the exact failing command, safe error text, exit code, and next action. Do not claim completion.
