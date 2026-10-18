---
name: hi-cli
description: Operates the Harness Intelligence CLI (`hi`, alias `hint`) through init, update, diff, check, tools, report, upgrade, operator-skill, and post-command flows. Use when a user runs or asks about `hi`, `hint`, the Registry Baseline, or generated `.devpunks/` work.
metadata: {"Harness Intelligence":{"entrypoint":true}}
---

# hi-cli

Use `hi` for the Harness Intelligence CLI; `hint` is an alias. The npm package remains `@punks/cli`.

The CLI installs one Baseline from the public Registry into the repository. The lifecycle commands are `hi init`, `hi update`, `hi diff`, and `hi check`.

## Commands

```bash
hi --help
hi init
hi update
hi update --yes
hi diff
hi check
hi tools ensure
hi report --help
hi upgrade --help
hi operator status
```

Read [references/commands.md](references/commands.md) when choosing or explaining a command.

## Workflow

For managed lint setup, Software Scope changes, policy migration, conflicting commands, or lint findings, read [references/managed-lint.md](references/managed-lint.md). Review the Software Scopes `hi init` saved before relying on managed lint; `--yes` accepts detection's proposal, which is not a deliberate owner decision.

1. Run the bounded command requested by the user.
2. Classify its result as init, update, diff, check, tools ensure, report, upgrade, or operator.
3. Follow only that branch in [references/post-command-flow.md](references/post-command-flow.md).
4. Stop when that branch's completion criterion is verified or its exact blocker is reported.

Existing `.devpunks/` files do not create work by themselves. The current command result and its reported paths control follow-through.

An assigned execution worker runs its bounded command and reports the result. It does not delegate again.
