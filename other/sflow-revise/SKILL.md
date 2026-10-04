---
name: sflow-revise
description: Preview and run one exact, bounded revision interval for the active code Candidate.
disable-model-invocation: true
argument-hint: "<feedback> [--criteria <CLAUSE-ID>] [--attachment-set <SHA256>] | status | card [INTERVAL-ID] | show <INTERVAL-ID> | resume [INTERVAL-ID] | capture | abandon <LOOP-ID|INTERVAL-ID>"
---

# Revise the active code Candidate

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. Require a ready session, exact `repositoryPath`/`workId`, saved buffers, and an open generation whose registered task is `code`; never infer this from a phase name. Run `singularity-flow revision status --json`. Stop on recovery, publication, terminal, wrong phase, or stale Candidate.
2. For inspection run only `singularity-flow revision status --json`, `singularity-flow revision card [<INTERVAL-ID>] --json`, or `singularity-flow revision show <INTERVAL-ID> --json`. Relay exact lineage, precheck, budgets, and recovery.
3. Send the same bounded UTF-8 feedback through standard input only—never argv, environment, logs, or repository files. Preserve explicit `--criteria <ID>` and registered `--attachment-set <SHA256>` selections; never infer or rewrite them.
4. Preview once: `singularity-flow revise --dry-run --feedback-stdin --saved-buffers-confirmed [--criteria <ID>] [--attachment-set <SHA256>] --json`. Show source snapshot/retained head, classification, criteria/disposition, effects, budgets, routing, and full digest. Preview retains no parent. A routing-required result creates no Human Request and cannot be confirmed: relay `routing`; explain that `/sf-recommend` only re-evaluates current state; stop.
5. For a ready plan, require the user to type that full digest. Send the same bytes and selectors once with `--saved-buffers-confirmed --confirm sha256:<PLAN>`. Assent or skill invocation is not confirmation. First confirmation retains the previewed source as immutable parent.
6. Ask the developer to edit and save only returned code/test scope manually. This build has no admitted model/code executor: never edit through Copilot tools, shell, Git, `/sf-code`, or fallback; never process/configuration paths, Git, workflow state, approvals, criteria, proof policy, or external systems.
7. Preview capture with `singularity-flow revision capture --preview --note <NOTE> --saved-buffers-confirmed`; after review, repeat with `--plan sha256:<PLAN> --confirm sha256:<PLAN>`. Never fabricate tests, screenshots, claims, or receipts. Later Testing/Verification is authoritative.
8. Run `singularity-flow revision resume [<INTERVAL-ID>]` only when returned. It may finish exact durable opening, frozen-Candidate precheck, abandonment, or journal/pointer reconciliation; it never repeats an uncertain attempt. Abandon only when offered with `singularity-flow revision abandon <LOOP-ID|INTERVAL-ID>`; use the loop ID when no interval has been captured yet. It closes the loop while preserving the head. Stop at local precheck evidence. Never publish, submit, approve, merge, deploy, or amend intent.
