---
name: sflow-return
description: Safely reconstruct a published Story on this machine from durable remote evidence.
disable-model-invocation: true
argument-hint: "<WORK-ID>"

---
# Return to published governed work

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Collect every required choice explicitly; never infer or preselect; preserve errors, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

Run `singularity-flow return <WORK-ID> --json` first. Show the configured remote, source ref and commit, destination branch, locator integrity hash, freshness, and whether the worktree is clean. If it is dirty, stop; never stash, reset, clean, commit, or discard changes. Ask the user to explicitly confirm the exact Work ID. Only after they provide it, run `singularity-flow return <WORK-ID> --apply --confirm <WORK-ID>`. Report the reconstructed phase and governed agent, then refresh with `/sf-home`. Never generate the confirmation yourself and never substitute `singularity-flow resume` when the Story must be discovered from another machine.
