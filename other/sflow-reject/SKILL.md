---
name: sflow-reject
description: Request changes to a submitted or closed Story, return an in-progress review step's source/test edits to its Code step after exact review, or safely abandon rework. Records authority and invalidation without rewriting Git history.
disable-model-invocation: true
argument-hint: "[WORK-ID] [--fetch] --to PHASE --reason 'explanation' [--repair] | roll-forward [CR-ID]"

---
# Request governed changes

<!-- sflow-output-contract: governed-review -->
**Output contract:** Show governed artifacts, hashes, identity warnings, and the exact confirmation before recording any decision.
<!-- sflow-execution-boundary -->
**Boundary:** `singularity-flow session current --json` → `ready`/`workId`, cwd=`repositoryPath`; use CLI/`workItemRoot` paths; never `$HOME`.

Sequence gates may be hard or soft. On `Out of sequence`, stop immediately and relay the error. On `Soft sequence warning`, show the full warning and leave the interactive `continue` decision to the human; never self-confirm. Use `singularity-flow nextsteps` only for read-only guidance and never edit managed state to bypass a gate.

1. Read status first. Show the current phase, artifact hashes, allowed `rejectTo` targets, reviewer Git identity, authority group, and governed agent.
2. Require a specific rejection reason and target phase; do not invent either. Present only the allowed targets, then preserve the human's exact comment.
3. For a phase awaiting approval, run `singularity-flow reject <phase> --work-id <WORK-ID> --fetch --to <earlier-phase> --reason "..."`.
   If an in-progress review step holds source/test edits and the engine names a return to its
   approved Code step, preserve them. Preview `singularity-flow reject <review> --to <code> --repair --reason "..."`
   in the bound worktree. Show paths and digest; request human confirmation. Only then
   rerun with `--confirm <sha256>`. Do not `--fetch` a dirty bound worktree. The return opens a new
   Code generation; retest and approve it before repeating the review.
4. For a closed Story, run `singularity-flow reopen <WORK-ID> --fetch --to <phase> --reason "..."`.
5. Stop on an unauthorized identity, disallowed target, disabled post-completion reopening, stale branch, or pending publication. Changing agents never grants decision authority.
6. Show which approvals and later phases will be invalidated before recording the decision. A later approved phase is kept (rule E1) only if nothing it decided over changes; the engine decides when the Story reaches it.
7. Report the change-request ID, comment, human identity, authority group, governed agent, reopened target, invalidated phases, commit, and push.
8. Stop after recording the request. Do not modify artifacts unless the user separately asks to address it.

If the user later decides to abandon everything changed after that return, do not reset Git and do
not manually copy artifacts. Preview the stored forward checkpoint first:

`singularity-flow story rework roll-forward --work-id <WORK-ID> --change-request <CR-ID> --json`

Show every restored path, the original phase, the local-backup guarantee, and the exact confirmation
digest. Only after explicit confirmation run the same command with `--confirm <sha256>`. Report the
backup path, governed commit, push, and restored phase. A missing checkpoint, a changed digest, a
cross-boundary rename, or a staged rework path is a hard stop; preserve the current bytes and relay
the engine's recovery instruction.
