---
name: sflow-inbox
description: Show what is waiting for your approval.
disable-model-invocation: true

---
# Open the pending approval inbox

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Collect every required choice explicitly; never infer or preselect; preserve errors, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. Run `singularity-flow inbox --json`. This fetches the configured Git remote and reads committed work-item state without checking out every branch.
2. If `items` is empty, report that the remote approval inbox is clear. Do not infer that uncommitted or unpublished work is ready for review.
3. Show every pending item with its work/Jira ID, title, phase, generation, approval count, waiting time, human authority groups, artifact path, remote commit, and self-approval warning.
4. Use Copilot's `ask_user` facility to let the contributor select one exact work/Jira ID. Never infer or preselect an item.
5. Run `singularity-flow session attach <WORK-ID> --json` once for that selection, then use its exact `repositoryPath`. It may create a tracking branch and fast-forward; never merge, rebase, reset, stash, or discard work. The phase agent does not change human authority. Do not attach again through `/sf-session`.
6. Run `singularity-flow phase show <PHASE> --json`; retain current `reviewBinding` and `displayBinding`. Reuse bodies only from a complete visible same-chat display with exactly matching non-null `displayBinding`. Otherwise render every text document/brief with ID/kind/path/bytes/generation/SHA-256 between `--- BEGIN <path> ---` / `--- END <path> ---`; binaries need path/metadata. New chat, changed/null binding, omissions or truncation require full display. Tool output or summaries are not review; incomplete review cannot offer approval.
7. Show current `reviewBinding`, identity/authority, checks and warnings even when bodies are reused. Body reuse never reuses approval consent. Mention `/sf-documents` for supporting evidence.
8. Stop. Offer `/sf-approve <PHASE-ID> --work-id <WORK-ID>` with actual IDs and `/sf-reject`; never decide or approve automatically.
