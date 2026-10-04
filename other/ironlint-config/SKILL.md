---
name: ironlint-config
description: Authors, modifies, or removes checks in an IronLint .ironlint.yml policy.
license: MIT
metadata:
  author: dynamik-dev
  version: 2.1.0
---

# IronLint policy authoring

IronLint runs project-owned shell commands after a change or before work is
accepted. A policy is `.ironlint.yml` with a required `version: 1` and a
nonempty `checks` mapping:

```yaml
version: 1

execution:
  timeout_secs: 30
  total_timeout_secs: 300

checks:
  format:
    files: ["*.rs", "Cargo.toml"]
    on: [change, accept]
    timeout_secs: 10
    run: cargo fmt --all --check

  tests:
    timeout_secs: 180
    run: cargo test --locked
```

Every check has one nonempty `run` command. `files` is an optional glob or list
of globs. Bare filename globs such as `*.rs` match at any depth. `on` defaults
to `[accept]`; the other valid form is `[change, accept]` (either order).
Acceptance is required for every check.

`accept` runs every check once in check-ID order. `change` runs only checks that
opt into change feedback. Known `--file` paths filter those checks through
`files`; without known paths, every change-enabled check runs. A check owns any
iteration over files. `files` selects a check; it does not restrict what the
command can read or modify.

The optional `execution` block accepts positive integer `timeout_secs` and
`total_timeout_secs`. Their defaults are 30 and 300 seconds. A check's optional
positive integer `timeout_secs` overrides the command default for both events;
it may be shorter or longer, but the remaining total budget always caps it.
Timeout values cannot be null, zero, negative, fractional, or strings.

Check overrides require evaluator 1.1.0 or newer. Update the evaluator before
adding the field; older binaries reject it. Remove it before downgrading and
review/renew consent after either edit. Verdict schema 7 is unchanged.
`show-resolved-config` and `explain` expose the override and resolved command
budget before the total cap.

The total deadline covers selection, policy/script verification, commands,
output handling, and final verification. Initial capture and consent lookup
precede it. Expired final verification denies pass even when commands passed;
filesystem deadline checks are cooperative and cleanup has a bounded grace.
Put command sequences in a reviewed script under `.ironlint/scripts/` and
invoke that script from `run`.

## Command contract

IronLint executes `run` as `sh -c` from the selected root, with stdin closed.
The reserved variables are:

- `IRONLINT_ROOT`: canonical evaluated root.
- `IRONLINT_EVENT`: `change` or `accept`.
- `IRONLINT_BIN`: current IronLint executable.

Commands inspect the evaluated tree on disk. Never splice an untrusted path
into `run`; read paths from environment variables or quote fixed paths in the
command. Exit 0 passes. Exit 1–125 reports a policy violation. Exit 126/127,
signals, timeouts, or launch failures are execution errors.

On a violation, print a concise file/line when known, the pattern required to
repair the code, and a relevant project document or rule reference. For example,
`src/api/orders.py:4: use OrderService instead of importing project.db; see
docs/architecture.md`. Both output streams may be shown to the agent, but
diagnostics are advisory text; check success still depends only on exit 0.

## Workflow

Validate and review before granting local execution consent:

```sh
ironlint validate
ironlint trust
ironlint check --event change --file src/lib.rs
ironlint check --event accept
```

Use `ironlint explain PATH` to inspect change selection,
`ironlint show-resolved-config` to inspect the loaded policy, and
`ironlint check --format json` for schema-7 machine output.

When editing a policy, preserve existing check IDs unless the requested change
requires renaming one. Prefer the smallest command that enforces the stated
rule. Re-run `ironlint validate`, review the final command, re-run
`ironlint trust`, then exercise both a passing and a violating example.
