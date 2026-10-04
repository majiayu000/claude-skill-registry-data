---
name: sflow-next
description: Execute one valid Singularity Flow lifecycle action without chaining later actions.
disable-model-invocation: true

---
# Execute the next workflow action

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. First run `singularity-flow session current --json`; require `ready`/`workId` and use its returned `repositoryPath` as cwd for every subsequent command. There run `singularity-flow nextsteps <WORK-ID> --json`; refuse `ACTIVE_SUBJECT_MISMATCH`. Use the shared repository model; `singularity-flow wm ensure` needs explicit consent. Do not start it while waiting. Never derive `--task`.
2. Never run `singularity-flow next`. Load one returned SFlow skill route (any `/sf-*` or `/sflow-*` route), use its configured producer/channel, complete its preflight, execute at most its one authorized action, and stop. Before approval run `singularity-flow phase show <phase> --json`; validate authority, report the automatic phase agent, and require the exact phase name. Every recorded approval must produce its own commit and push.
3. Sole no-skill exception: when snapshot `state=publication_pending` and its first `NOW` command equals `singularity-flow sync`, show it and explain it retries only the retained commit. Run `singularity-flow sync <WORK-ID>` once in the verified cwd, then stop; never follow `THEN`, invoke `/sf-nextsteps` or `/sf-next`, or retry.
4. Follow the selected skill; never rewrite it to `/sf-phase`. If the selected action is `/sf-code`, do not imitate or inline it: report `Next in Copilot: /sf-code` and stop; preserve `/sflow-code` likewise. The selected skill must run draft-check and correct every agent finding. Never publish a delegated action.
5. On failure run read-only `singularity-flow recover <WORK-ID> --phase <phase> --json`. Never add `--apply` without the reviewed plan and exact confirmation. `ARTIFACT_AUTHORING_INCOMPLETE` permits one recheck and correction handoff, not a retry loop.
6. Run `singularity-flow phase show <phase> --json`; show bounded previews, hash-bound references, and binary metadata.
7. Preserve sanitized `telemetry/<phase>-gen<N>.json`; report resolved model and token/cost status, action, commit/push, authority, and agent. Separate **Completed action** from **Next action**; never claim the next action was taken. After mutation rerun `singularity-flow nextsteps <WORK-ID> --json` once. Copy the first `NOW` action's `copilotCommand` and `command` from that same action object and render `Next action (choose one surface):`, `Copilot: /sf-...`, `Shell: singularity-flow ...`. Never mix action fields: `/sf-next` pairs with `singularity-flow next`; `/sf-phase` pairs with returned `prepare` or `phase` command. Never pair `/sf-phase` with `singularity-flow next`. Do not automatically submit a generation you just published.
8. After approval context `new`, run `/clear` and then `/sf-next`; after `compact`, run `/compact` and then `/sf-next`. After either reset, reapply the Boundary before artifact reads.
