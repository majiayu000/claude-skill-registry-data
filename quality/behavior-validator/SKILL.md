---
name: behavior-validator
description: "Source-blind user behavior validation against a prewritten contract for apps, CLIs, APIs, and generated artifacts."
---

# Behavior Validator

Validate observable behavior without inspecting source. Use this as the black-box companion to code-aware review: `autoreview` judges the change bundle, while `behavior-validator` judges the running product, CLI, API, or generated artifact against a behavior contract.

## Contract

- Read the behavior contract first. If none exists, write a short one from the user request before testing. See `references/contract-template.md`.
- Stay source-blind. Do not inspect source files, diffs, tests, git history, implementation notes, build internals, or review bundles.
- Interact only through user-visible or operator-visible surfaces: browser, CLI, API, generated files, public logs, screenshots, accessibility trees, or documented runtime output.
- Treat implementation-looking evidence as contamination. If source access is required to continue, stop and report `blocked_source_required`.
- Report findings against contract clauses and observable steps, not code locations.
- Do not mark a workflow as passing until each relevant contract clause is pass, fail, blocked, or out of scope.

## Isolation

Prefer a source-blind workspace:

```sh
validator_dir="$(mktemp -d "${TMPDIR:-/tmp}/behavior-validator-run.XXXXXX")"
chmod 700 "$validator_dir"
cp behavior-contract.md "$validator_dir/"
cd "$validator_dir"
```

Launch or connect to the target from the contract. Keep only the contract, allowed fixtures, and redacted captured evidence in the private validator workspace. Supply credentials through approved secret tooling or exact environment variables; never copy credential values into the workspace, report, screenshots, or logs. Do not use fixed shared paths for contracts or captured evidence. If the app must be started from the source checkout, start it from a separate terminal and do not read source while validating.

## Workflow

1. Parse the contract into user tasks, expected behavior, anti-cheat probes, setup, and evidence requirements.
2. Prepare runtime access: target URL, CLI command, API endpoint, fixture data, credentials, or generated artifact path.
3. Exercise each user task as a real user or operator would.
4. Run anti-cheat probes: vary fixture data, refresh/retry, test empty and invalid inputs, verify persistence, inspect generated output, and confirm buttons/commands perform real work rather than only displaying success text.
5. Capture evidence as compact redacted notes, screenshots, terminal excerpts, response summaries, file summaries, or accessibility observations. Omit credentials, tokens, cookies, private user data, and unrelated log content.
6. Emit a structured report. Use `references/report-schema.md` when a machine-readable report is useful.
7. If the orchestrator fixes a finding, rerun only the affected contract clauses plus any nearby regression probes.

## Finding Rules

- Fail when observable behavior violates the contract, a task cannot be completed, expected state is fake/static, or evidence is insufficient for a claimed pass.
- Block when required runtime access, credentials, fixtures, network, or tools are missing.
- Mark out of scope only when the contract explicitly excludes the behavior or the task depends on a user-owned product decision.
- Reject purely aesthetic, code-quality, or implementation-style concerns; those belong to code-aware review.

## Final Report

Include:

- target exercised
- contract file or inline contract used
- pass/fail/blocked/out-of-scope summary
- accepted behavioral findings with reproduction steps and evidence
- anti-cheat probes run
- remaining blockers, if any
