---
name: closeout
description: Prove session release through scoped evidence; distinguish completed work from durable handoff and estate health.
---

# Closeout

Authority: `AGENTS.md` → Full Lifecycle Closure. Zero dangling items means zero
unowned obligations on this session. A filed task remains unfinished until its own
acceptance predicate passes. Session release does not authorize checkout retirement.

1. Resolve the exact native session, its worktree, and its existing owner/continuation.
   Preserve the caller worktree separately from the installed protocol root. Inspect
   only the accepted scope; never adopt a sibling checkout to obtain a green result.
2. Finish the authorized work or publish a handoff in its existing owner. Preserve
   private artifacts through their custody owner. Record exact owned paths and explicit
   retained-work owners in the existing continuation's `session-closeout.json` using
   `limen.session_closeout.v1`, or v2 with explicit roots for multi-repository sessions
   (see `docs/session-closeout.md`). Unknown ownership fails
   closed. Commit and publish the receipt and owned artifacts through the normal PR rail.
3. Reuse passing verification for unchanged implementation. Run implicated scoped gates
   once per changed tree, including credential-wall evidence for secrets used by the
   session. Whole-repository verification is required only for a whole-repository claim.
4. Run `scripts/no-tasks-on-me.sh --session-id ID --worktree PATH --receipt RECEIPT --json`
   from the resolved protocol root with the authenticated conduct environment. For a
   legacy unregistered Codex session, also supply its exact `--native-transcript PATH`.
   With v2, keep `--worktree` bound to the native caller and supply every declared
   `--scope-root ID=PATH`; never substitute a child repository for the native anchor.
   This read-only predicate checks publication, ownership, custody, scoped verification,
   retained broker obligations and surviving processes. Exit 2 is unmeasured, never pass.
   No-argument `no-tasks-on-me.sh` and `closeout-fast.sh` remain estate diagnostics.
5. A successful recheck on unchanged owned evidence creates no files, issues, leases,
   worktrees or provider runs. Do not replay a green full suite. A completed session
   needs no successor capsule. A handoff reuses its existing durable owner; successor
   creation requires separately admitted continuation work and never renews a budget.
6. Honor existing merge/deployment authority. A genuine external gate is stated once
   as `BLOCKED: <atom>` and homed with its owner, predicate and next command. Do not
   weaken custody or relabel unknown ownership to pass. Report the scoped result;
   task completion, session release, estate health and deletion eligibility stay distinct.

Only after the session predicate exits 0 may the terminal statement be emitted:
CLOSEOUT COMPLETE — idempotent fixed point, zero dangling items
Nothing follows that statement. If the predicate fails, preserve the precise owner
receipt and report the actual outcome without claiming a successful closeout.
