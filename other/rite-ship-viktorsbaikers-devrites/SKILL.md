---
name: rite-ship
description: Commit, push, tag, archive, or close a sealed feature after /rite-seal GO. Use for repository mutation; not for GO/NO-GO readiness.
argument-hint: "[feature-slug]"
user-invocable: true
---

<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/candidate-integrity.md","devrites-lib/reference/standards/git-workflow.md","devrites-lib/reference/standards/definition-of-done.md","devrites-lib/reference/standards/release/ship-checklist.md","rite-ship/reference/git-ship.md","rite-ship/reference/rollout.md","rite-ship/reference/close-out.md","rite-ship/reference/ship-template.md","rite-ship/reference/anti-patterns.md"],"triggers":{"afk":["devrites-lib/reference/standards/afk-hitl.md"]},"workspace":["brief.md","spec.md","state.md","decisions.md","assumptions.md","questions.md","decision-coverage.md","architecture.md","plan.md","tasks.md","traceability.md","eng-review.md","test-plan.md","gates.md","evidence.md","touched-files.md","review.md","seal.md"],"rootOnly":["devrites-lib/reference/standards/afk-hitl.md"]} -->
> Read-set manifest: `devrites-engine context --skills-root .pi/skills <slug> --phase ship` bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.


# /rite-ship: ship + close the task

`/rite-seal` decides; `/rite-ship` mutates Git and closes. Read the active workspace;
if absent, route to `/rite-spec <feature>`. Ship only with current **GO** in `seal.md`.

## Rules consulted (read on demand from `.pi/skills/devrites-lib/reference/standards/`)
**Step 0:** Read [`core.md`](../devrites-lib/reference/standards/core.md), then pull as needed:
- [`git-workflow.md`](../devrites-lib/reference/standards/git-workflow.md): Conventional Commits, atomicity, never-commit list.
- [`afk-hitl.md`](../devrites-lib/reference/standards/afk-hitl.md): AFK pause rules for irreversible actions (the type-GO gate itself: [`git-ship.md`](reference/git-ship.md), [`rollout.md`](reference/rollout.md)). Trigger `afk` — load when `.devrites/AFK` exists.
- [`definition-of-done.md`](../devrites-lib/reference/standards/definition-of-done.md): acceptance, evidence, drift, rollback, docs.
- [`release/ship-checklist.md`](../devrites-lib/reference/standards/release/ship-checklist.md): final pass/fail sweep.

## Operating rules
- **GO is prerequisite.** No current `seal.md` GO → stop at `/rite-seal`.
- **Ship is candidate-read-only.** Follow
  [`candidate-integrity.md`](../devrites-lib/reference/candidate-integrity.md).
  Ship must not change any candidate path or `touched-files.md`; it may write only
  workspace `ship.md`, `state.md`, and archive bookkeeping. Project/manifest mutation
  returns through Prove → Review → Seal.
- **Bindings stay exact.** Rerun candidate/Seal checks; require the digest bound in
  evidence, optional browser evidence, review, and seal. Any mismatch stops.
- **Fresh approval.** Disclose the exact Git attempt; literal `GO` authorizes it once.
  Change/retry means re-prompt. Native approval remains separate/authoritative.
- **Archive, never delete,** every audit `.md`.

## Workflow
1. **Orient.** Snapshot; read seal, state, spec, touched files, evidence, and any UI
   brief. Confirm GO/closed digest, then run:
   ```bash
   devrites-engine check candidate <slug>
   devrites-engine check seal <slug>
   ```
   Nonzero/mismatch stops; never reinterpret it.
1a. **Health (advisory).** Apply `/rite-doctor` read-only; surface WARN/FAIL without
   repair. If ACTIVE is flagged, confirm the slug.
2. **Prepare the exact Git candidate.** Follow
   [`git-ship.md`](reference/git-ship.md): refuse out-of-manifest staged work; stage
   exact manifest paths only after Seal GO; compare NUL-delimited staged state/path
   sets, require identical index/worktree bytes, and rerun candidate/Seal checks.
   From the verified index, build the exact project-conformant message/trailers,
   branch, tag/PR, commands, and skips.
2a. **Credential guard (HIGH blocks).** Scan staged blobs and any PR body. HIGH stops
   and requires rotation/redaction; MEDIUM needs confirmation recorded in `ship.md`;
   LOW is FYI.
   ```bash
   devrites-engine secret-scan --staged
   ```
   Scan a PR body with `devrites-engine secret-scan --stdin` only through non-logging
   process stdin, then close it—never command/argv/env/heredoc/log/temp file. If that
   channel is unavailable, stop. **rc=3 → STOP:** no type-GO/commit/push/archive.
2b. **Reconcile residuals before type-GO.** Scan `strategy.md` deferrals,
   `decisions.md` FYIs/revisit triggers, unresolved `review.md` non-blocking/if-minor/
   FYI findings, and `seal.md` follow-ups. Deduplicate only rows with identical
   obligation + disposition, preserving every source pointer. Each residual appears
   once in the pending `ship.md` table as `tracked` (durable path/ID) or `no-action`
   (prior decision or explicit human acceptance + reason/revisit). Type-GO never
   implies `no-action`. Missing/vague/conflicting disposition blocks; `none` requires
   empty sources.
3. **Type-GO.** Render [`git-ship.md`](reference/git-ship.md)'s prompt and wait.
   Literal `GO` proceeds once; anything else records cancellation in `ship.md` and
   stops. Any command/scope/branch/message/tag/PR change or retry needs a fresh prompt;
   native approval is still required.
4. On GO, commit; verify committed state/path set and exact candidate digest; then push →
   tag/PR as applicable via `git-ship.md`. Record SHA and push state in `ship.md` before
   push (git-ship 7a); a push/tag/PR failure stops, and a rerun resumes at push under
   fresh type-GO. Capture branch, tag/PR URL. Mismatch stops before push/tag; retry
   needs fresh approval.
4a. **PR only:** render [`git-ship.md`](reference/git-ship.md#pull-request-body)'s
   structured body; omit empty sections.
5. Re-scan the four residual sources; any new/missing/changed item blocks archive.
   Write [the template](reference/ship-template.md) with shipment metadata and the
   unchanged pre-GO reconciliation.
6. **Close.** Set `state.md` phase `done`; follow
   [`close-out.md`](reference/close-out.md) and run `devrites-engine state close <slug>`
   to move `.devrites/work/<slug>` → `.devrites/archive/<slug>` and clear `ACTIVE`
   only if it names this slug; preserve another active feature's cursor.
   Preserve every `.md`; stable hierarchical instructions need no active-workspace sync.
   Report the recorded `Next step` verbatim — the exact `/rite-spec <parent>-<n> "<objective>"`
   when a continuation sequence remains — so the next increment starts from one line,
   never from chat memory.

> **Mid-flight discipline.** No seal GO, skipped type-GO, out-of-manifest stage, or
> deleted workspace. Stop and use [`anti-patterns`](reference/anti-patterns.md).
