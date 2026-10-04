---
name: sflow-goal
description: Create personal outcomes or operate repository-owned governed Goal Executions.
disable-model-invocation: true
argument-hint: "[personal|propose|govern|inspect|impact|plan|approve-plan|run-next|verify|change|pause|resume|abandon|trace]"

---
# Goals — outcomes above governed work

<!-- sflow-output-contract: explicit-selection -->
**Output contract:** Collect every required choice explicitly; never infer or preselect; preserve errors, artifacts, and next actions.
<!-- sflow-execution-boundary -->
**Boundary:** machine-local; no repository or Story required. Use explicit arguments or SFlow-returned paths; never search `$HOME` or infer a repository.

A Goal has two modes. `GOL-*` is personal advisory state. `GEX-*` is repository-owned governed
execution. Neither replaces a linked Story or Initiative lifecycle.

1. Start with `singularity-flow goal list --json`; durable state, not chat memory, is authoritative. With no action, show the active Goal and run `singularity-flow goal next [GOAL-ID] --json`.
2. For **create**, collect an outcome and observable success. Never invent Work IDs or repositories. Preview, use `ask_user`, then run:
   `singularity-flow goal create "<OUTCOME>" --success "<CRITERION>" [--success "<CRITERION>"] [--work-id <ID> --kind story|initiative --repository <ID>] --json`.
3. For **use/link/unlink**, show the Goal, require explicit Goal/Work selection, preview, and use `ask_user`. Linking never modifies governed work.
4. For **complete**, show criteria and live links. Stop for active/unavailable links. Call completion acknowledgement—not proof—then require the exact ID.
5. For **abandon**, require a reason and exact ID; say linked work is untouched before `ask_user`.
6. Start governed work with read-only `singularity-flow goal propose "<OUTCOME>" --success "<CRITERION>" --json`; it creates no branch or plan.
7. Promotion creates a new identity. Show `singularity-flow goal show <GOL-ID> --json`, list copied fields, use `ask_user`, then `singularity-flow goal govern <GOL-ID> --json`. Preserve the personal Goal.
8. For `GEX-*`, use `singularity-flow goal inspect <GEX-ID> --json`. Use `singularity-flow goal impact <GEX-ID> --json` for read-only scope. Compile with `singularity-flow goal plan <GEX-ID> --json`; show generation, steps, stops, write set, and full `planSha256`. Use `ask_user` before exact-hash approval.
9. Run one step with `singularity-flow goal run-next <GEX-ID> --json`. Follow its Story/Initiative skill and gates. Never turn `singularity-flow goal run-until-blocked` into a loop; bounded autonomy is closed.
10. `singularity-flow goal verify <GEX-ID> --json` uses typed oracles. Preserve `verified`, `mixed`, `acknowledged`, and `unassessed`; terminal work does not prove human judgment.
11. Inspect before pause, resume, change, trace, or governed abandon. Change is read-only. Abandon needs exact `GEX-*` ID and reason and leaves linked work untouched.
12. If publication retains a local Goal commit, show the exact recovery and use `singularity-flow goal sync <GEX-ID>` only after remote access is restored.
13. Preserve refusals/actions and re-read after mutations.

Never claim that plan approval approved a Story, that navigation executed a Story transition, or that a
human judgment was deterministic proof. Never invent a plan hash, Goal ID, oracle result, Work ID,
repository, authority, or confirmation.
