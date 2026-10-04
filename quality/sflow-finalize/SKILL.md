---
name: sflow-finalize
description: Finalize a fully approved developer Story into an exact hash-bound packet for Product Owner spec-to-code review.
disable-model-invocation: true

---

# Finalize a Story

<!-- sflow-output-contract: deterministic-mutation -->
**Output contract:** Let the CLI validate and mutate state; preserve its exact result, warnings, publication status, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

1. Run `singularity-flow progress` and confirm every configured Story phase is approved.
2. Run `singularity-flow finalize`.
3. The command verifies a clean tree, the governed seed, parent and Story specification hashes, every phase artifact, approvals, quality evidence, model/token records, and exact source/test tree.
4. Show the finalization packet path/hash, source commit/tree hash, commit, and push.
5. Do not approve or promote the Story. Finalization changes delivery state to `finalized_for_review`; Product Owner review is a separate decision.
