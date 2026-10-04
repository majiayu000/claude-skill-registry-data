---
name: sflow-specify
description: Route a spec-driven Story toward an approved specification.
disable-model-invocation: true

---
# Specify — route toward an approved specification

<!-- sflow-output-contract: clarification-and-artifact -->
**Output contract:** Use governed inputs and pinned clarification; publish/show configured artifacts.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. Run `singularity-flow specify --json`. It returns the milestone, the checkpoint it stopped at, and the underlying kernel operations.
2. Relay `checkpoint.reason` and the ordered `next[]` actions. Never invent an action the router did not return.
3. If the checkpoint is `recovery`, route it first. Nothing else may proceed while a retained commit has not reached its remote.
4. If the checkpoint is `approval`, stop. Approval needs an authorized human Git identity; a governed agent cannot grant it.
5. At `model-generation`, require the first `NOW` action in the returned `next[]` to be `singularity-flow prepare specification`; run that exact returned command once and use its artifact path. If the action differs, stop and relay the returned route; never author a seeded or stale draft. With the resolved agent, approved inputs, pinned template/constitution, and required world-model views, author `spec.md` scenario-first: prioritized Given/When/Then scenarios, actors, empty/failure states, permissions, boundaries, and non-functional requirements. Fill `Agent brief` with approved intent only; the kernel preserves exact sections for review. Run `singularity-flow wm compose --phase specification` once for its `Active supporting evidence`; under `## Sources` cite each document used as `DOC-nnn — <name>` and list unreadable or unavailable ones as gaps. Where evidence is missing, write `[NEEDS CLARIFICATION: <one question grounded in the current Story evidence>]`, not an invented answer.
6. Before publication run `singularity-flow phase draft-check specification --json`, then `singularity-flow phase prepublish specification --json`. If unready, run read-only `singularity-flow recover <WORK-ID> --phase specification --json`; keep recovery in this phase. Repair every structured agent finding in this Copilot turn from the governed prompt and approved evidence only when `correction.sameTurn`; otherwise route to its producer or human. Allow at most three distinct changed fingerprints; stop on an unchanged fingerprint or still unready after three. Never blindly delete markers, invent facts, add padding, launch a nested Copilot/model invocation, or overwrite human-, deterministic-, or external-authored output. Publish only when prepublish `status` is `ready`. A race-time `ARTIFACT_AUTHORING_INCOMPLETE` permits one recheck and at most one publication retry if ready, never a loop. Never submit or approve.
7. Claim a milestone only when the router returns it.
8. State the underlying operations you ran.
9. For every returned next action, show its direct Copilot route first as `Next in Copilot: /sf-...`, followed by the exact `Terminal equivalent: singularity-flow ...`. Never omit or guess either route.
