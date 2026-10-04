---
name: sflow-worldmodel
description: Build, verify, inspect, and compose the repository-owned world model used to ground governed phase prompts.
disable-model-invocation: true

---

# World model

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Collect every required choice explicitly; never infer or preselect; preserve errors, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

- **Bare `/sf-worldmodel` is read-only.** Run only `singularity-flow wm status --json` and `singularity-flow wm ast status --json`; report source, assurance, views, and blockers. Preserve `unavailable` and `current: null` exactly. Never infer mutation consent.
- Before mutation show revision, views, depth, routing, writes, and target; confirm.
- Configure/inventory: `singularity-flow wm init`; `singularity-flow wm light [--phase PHASE] [--local]`. `--local` is a private rehearsal and is not reusable from the shared state branch.
- For a shared refresh during a Story, inspect its pinned format. With `legacy-v3`, review `singularity-flow wm light --format legacy-v3 --views all --state-only`: zero model calls, committed source, governed remote state publication, no Story-branch commit. Show revision, views, remote/state target, and exact command before confirmation. For `registered-v4`, use its reviewed Plan/build route. Never switch formats or run ordinary `singularity-flow wm light` on the Story branch.
- Build: `singularity-flow wm build [--phase PHASE] [--views VIEW,...] [--depth light|quick|standard|deep] [--workers N]`. Check readiness with `singularity-flow wm availability --json`.
- Inspect: `singularity-flow wm check`; `singularity-flow wm context <PHASE>`; `singularity-flow wm compose [--phase ID] [--work-id ID] [--dry-run|--render-only]`.
- Recovery: `singularity-flow wm cleanup --json` removes stale, process-owned temporary worktrees; `--force` only on request. `singularity-flow wm recovery publish <ID> --confirm <ID>` reuses retained output.
- AST: `singularity-flow wm ast doctor|status --json`, bounded `singularity-flow wm ast context --paths <ROOT> --max-facts 50 --max-output-bytes 32768 --json`, or `singularity-flow wm ast query`. Symbol gates require explicit syntax policy.
- FWM reads: `singularity-flow wm read-views`, `singularity-flow wm read-contract <VIEW>@<REVISION>`, `singularity-flow wm read <VIEW>`. Preserve provenance and unknowns; never execute `draft`.

No active Story is valid. Never invent scope, add `--local`, use `singularity-flow wm ensure` for a read, or run competing builds. Report freshness and reuse location.

Reuse ready exact-source/scope snapshots. Ordinary ensure never upgrades light; automation cannot replace removed, stale, divergent, invalid, offline-unverified, or different-source authority. Offer generation only when asked.

Polyglot facts are text-assurance leads; semantic assurance needs a reviewed pack. Missing AST falls back to bounded files. Dirty-byte previews cannot govern. Copilot reads use `sflow_resolve`, then `sflow_read`; agents cannot remove required views or approve.
