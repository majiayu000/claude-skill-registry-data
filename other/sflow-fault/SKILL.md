---
name: sflow-fault
description: Record, list, or inspect an immutable Singularity Flow fault without treating the report as repair authority.
disable-model-invocation: true

---

# Fault intake

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

Use this skill when a developer, test runner, CI job, IDE, or monitoring tool says something is broken.

1. For an existing fault, run `singularity-flow fault show <FAULT-ID> --json` and reproduce its observed fields without upgrading them into conclusions.
2. For a new report, collect source, environment, failure type, failing command, exit code, message, build/commit, Story when known, and immutable evidence references. Do not request or reveal credentials, tokens, raw hidden reasoning, or unrestricted chat history.
3. Preview the exact command. Prefer structured argv so Windows paths and quoting remain exact: `singularity-flow fault report --source <SOURCE> --environment <ENVIRONMENT> --type <TYPE> [--build <ID>] [--commit <SHA>] [--story <WORK-ID>] [--command-argv '<JSON-ARRAY>'] [--exit-code <UNSIGNED-32-BIT-CODE>] [--message <TEXT>] [--log <FILE>]... [--idempotency-key <KEY>] --json`. Retain `--command <COMMAND>` only for compatibility with simple shell input.
4. Explain that the fault is evidence, not authority. Reporting it does not permit code changes, approval, merge, release, deployment, or production mutation.
5. Offer `/sf-fix <FAULT-ID>` for deterministic diagnosis and a policy-bounded repair plan.

Never invent evidence hashes, claim a model hypothesis is observed, or start a recursive repair from inside a repair attempt. Secret redaction is a last safety boundary, not permission to solicit or knowingly submit credentials.
