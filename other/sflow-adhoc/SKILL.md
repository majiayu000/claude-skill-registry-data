---
name: sflow-adhoc
description: Inspect, confirm, verify, and safely land work that began without a Singularity Flow Story.
disable-model-invocation: true
argument-hint: "[start|status|land|intent|claim|preview|publish|promote]"
---
# Land ad hoc work safely

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Collect every required choice explicitly; never infer or preselect; preserve errors, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** no Story required; cwd=opened Git root or verified `repositoryPath` from `singularity-flow workspace current --json`; refuse if neither resolves; never search `$HOME`/parents.

1. Run `singularity-flow adhoc status --json`. If no session exists and the contributor wants to inspect existing work, run `singularity-flow land --json`.
2. Show every observed resource and the exact change-set digest. The candidate objective is advisory and must never be described as pre-existing intent.
3. Ask the contributor for the objective and at least one observable success criterion. Only after they answer, run `singularity-flow adhoc intent confirm <SESSION-ID> --objective "..." --success "..." --confirm <CHANGE-SET-SHA256> --json`.
4. Show unresolved resources. Apply only the exact claimed/deviation/split/revert choices the contributor gives; never claim a resource automatically.
5. Run `singularity-flow adhoc landing preview <SESSION-ID> --json`. If multiple allowlisted tests exist, show the IDs and ask which one to use.
6. If the result is promotion-required, preserve the reasons and offer `singularity-flow adhoc promote <SESSION-ID>`. Do not weaken protected-path, branch, resource, or verification checks.
7. Show the complete packet digest. Publish only after the contributor explicitly confirms that exact digest, using `singularity-flow adhoc publish <SESSION-ID> --confirm <PACKET-SHA256> --json`.
8. Report that direct landing is reverse-converged ad hoc work (`workflowExecuted: false`), together with the exact commit, push status, authority receipt, and any pending recovery.
