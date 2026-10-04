---
name: sflow-recommend
description: Show one grounded next step from the active SFlow workspace.
---

# Recommend one next step

<!-- sflow-output-contract: guided-actions -->
**Output contract:** Use read-only CLI evidence, preserve warnings and ordered actions, and change nothing unless explicitly requested.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.

Use the durable workspace, work-item, evidence, and repository records. Never infer lifecycle state from chat history.

## Workflow

1. Run `singularity-flow recommend --json` from machine context. Trust only the workspace,
   repository, and Story paths returned by that command; do not search for missing context.
2. Read `data.guidance` from the returned envelope.
3. Address the developer by `data.personalization.replyName` when present.
4. Present the answer under these short headings:
   - **I found** — current workspace, work item, phase, and relevant evidence.
   - **Next** — the single recommended action and why it is next.
   - **I need from you** — only the inputs named in `requiredInputs`; omit this heading when empty.
   - **This will change** — effect, command, and preflight information when the action can mutate state.
5. Offer secondary actions only after the primary recommendation.

## Safety contract

- This skill is read-only. Do not execute the recommended command automatically.
- Preserve warnings, refusal codes, unavailable reasons, and recovery guidance exactly.
- Do not invent workspace, branch, work-item, evidence, approval, or publication state.
- If no governed context is available, relay the actionable empty state and suggest `/sf-workspace` or `/sf-doctor` only when the result does.
- A mutating follow-up requires the developer to invoke or explicitly confirm the corresponding `/sf-*` action.
