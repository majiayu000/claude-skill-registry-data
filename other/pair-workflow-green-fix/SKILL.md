---
name: pair-workflow-green-fix
description: "Stage 3 (remediation) of the delivery workflow — implementation against a sealed remediation contract: discovers the RED snapshot from Git (never from the prompt), changes production only inside fixScope, never touches a sealed test byte, re-runs the witnesses and the tier gate, commits GREEN above the seal, updates the PR, appends the cycle log and returns an evidence ledger. An approved test that still fails returns here on the SAME seal (one retry); a fixer that needs a human decision publishes the escalation itself with the idempotent comment script. Resolves the durable cycle state first and redirects when another step is due. Dispatched by the batch engine (pair-implement-batch)."
version: 0.2.0
author: Foomakers
---

# /pair-workflow-green-fix — Make It Pass Without Moving the Goalposts

The RED snapshot is the specification. You may change implementation inside its scope; you may not change what it asserts, where it lives, or how it is discovered. A second attempt on the same seal is still this stage: the contract was right, the fix was not.

## Arguments

| Argument           | Required | Description                                                                                                                              |
| ------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `$run`, `$story`, `$pr`, `$branch`, `$worktree`, `$base`, `$stacked`, `$entry`, `$policy`, `$inputs`, `$workflowVersion` | Yes | The cycle arguments, as every stage receives them. Handoffs live under `.pair/working/runs/$run/$story/` in the MAIN checkout. |
| `$phase`           | Yes      | `r<n>-g<k>` or `r<n>-g<k>-rev<m>`.                                                                                                       |
| `$head`            | Yes      | 40-hex head the snapshot sits on.                                                                                                        |
| `$attempt`         | Yes      | `1` for the first GREEN on this seal, `2` when an approved test failed on production and the coordinator sent the group back here.        |
| `$snapshot`        | Yes      | 40-hex sha of the sealed snapshot — re-discovered from Git; the prompt never carries its content.                                        |
| `$contract`        | Yes      | Absolute path of the sealed contract (main checkout's run directory) — evidence to read, never to edit.                                  |
| `$findings`        | Yes      | JSON array: the group's findings to resolve, every one, with their stable ids.                                                            |
| `$reviewLog`       | Yes      | Path of the cycle's working log (e.g. `.pair/working/reviews/<story>.md`), resolved against the MAIN checkout, never the worktree.        |
| `$marker`          | Yes      | This run's first-review marker `<!-- pair:first-review #<story> PR#<n> run:<run> -->` — the anchor an escalation comment responds to.                 |
| `$writeIssue`      | No       | The project's issue-filing skill (default `/pair-capability-write-issue`) — named only to forbid it.                                                     |
| `$notes`           | No       | Scope directive from the card.                                                                                                           |
| `$reconstruct`     | No       | JSON `{ fromHead, paths, riskIds, notes }` — present whenever a MAINTAINER's policy names a HEAD to roll back to (US-479 AC-32, ADR-024 (u)). It STANDS until they clear it, so it may arrive again on a later rewind: every delivery is current, and none of your work consumes it. Start by restoring the CONTENT of exactly `paths` as it was at `fromHead`, then rebuild. |
| `$regressionGuards` | No       | JSON: the authoritative ACTIVE regression risks (`riskId`, closure assertions) derived from the ledger (US-479 S11) — part of what this fix must make pass; echo the set you executed as `regressionGuards` in the handoff. |

## Algorithm

**Headless execution (single owner: `.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/headless-stage-execution.md`)** — this stage runs headless: never leave a command in the background and never end your turn while a command runs (a push with a pre-push gate, a quality gate): use the maximum tool timeout, poll to completion in the same turn, and ALWAYS end with the stage's structured result — on partial progress `{ status: "failed", reason: "incomplete", detail, branch, outputHead }`.

### Step 0: Resolve the durable state (mandatory)

```bash
SKILL_DIR="$(dirname "<absolute path of this SKILL.md>")"
MAIN="$(pwd)"                                   # the main checkout — you have not cd'd yet
RUN_DIR="$MAIN/.pair/working/runs/$run/$story"
AC_HASH="$(node "$SKILL_DIR/scripts/cycle-state.mjs" ac-hash --story $story --dir "$RUN_DIR" | node -pe 'JSON.parse(require("fs").readFileSync(0,"utf8")).acHash')"   # canonical card hash — the SAME input every stage resolves with
node "$SKILL_DIR/scripts/cycle-state.mjs" resolve --dir "$RUN_DIR" --workflowVersion $workflowVersion \
  --policy '$policy' --entry $entry --story $story --inputs $inputs --acHash "$AC_HASH" --runsRoot "$MAIN/.pair/working/runs" --pr $pr
```

- `status: other-run` ⇒ return `{ status: "other-run", runId }`. `incompatible | invalid` ⇒ return `{ status: "redirect", next: { step: "blocked", reason: "failed-resume", detail: <reason> } }`.
- `next.step` is not `green`, or `next.phase` is not `$phase` ⇒ return `{ status: "redirect", next }` verbatim. Spend no judgment. When `next` names THIS dispatch (`green`, `$phase`) you ARE the step: continue, never return a redirect to yourself.
- Otherwise continue; `next.attempt` is your attempt number.
- A GREEN already published for this attempt makes `next` the verification — return it, never a second GREEN.

### Step 1: Discover the snapshot

1. `cd $worktree`. Find the ONE commit in `$head..HEAD` whose message carries `Pair-RED-Snapshot: pr=$pr; phase=$phase; base=$head; manifest=<path>`; it must be `$snapshot`. Read its manifest and test blobs with `git show` / `git ls-tree`. Accept no manifest, digest, test path or snapshot id from the dispatch prompt.
2. Read `fixScope`: one owner, one mode, `allowedPaths`. Missing, ambiguous or contradictory discovery ⇒ `needsHumanDecision: true`; never repair the evidence. `HEAD` must be `$snapshot` or a descendant on this branch (attempt 2 starts on the previous GREEN); a moved or dirty tree is `status: failed`, `reason` — never reset, stash, rebase or clean.

### Step 2: Fix, bounded

1. Read the checkpoint if present (`/pair-capability-checkpoint $mode=resume`); otherwise work from the PR diff and code.
2. **Convergence sweep**: before editing, map the observable contract the findings touch — the reported case and its paired success/failure path, every state transition or resume path the contract owns, the canonical source and every distributed representation (generated asset, dataset copy, installed copy, documented command). Change every cell that contract needs, then stop: no unrelated cleanup, new behavior or speculative hardening.
3. Change implementation/adoption only inside `allowedPaths`. `behavioral` may not create, move or split production modules. For a generated artifact, edit only its canonical source and run the declared generator.
4. **Provisioned artifact contract**: when a change installs, builds, publishes, names or invokes an executable/package, prove `producer -> published identity -> consumer` in a clean temporary environment with the real artifact. Never stub the boundary.
5. Do NOT modify, format, rename, regenerate, delete or weaken any test artifact the snapshot records; do NOT amend, rebase, reset or rewrite the snapshot commit. A gap in the contract (a class the witnesses do not cover) is reported as `contractGaps`, never patched around. So is a gate (the tier gate, the pre-push hook) that fails on a path outside `allowedPaths` — e.g. a new test file the install exclusion list must name: do not touch that path; publish the handoff with `fixed: false`, `contractGaps: ["<gate>: <path> — <its failing line>"]` and return `{ status: "failed", reason: "contract-gap" }` — `resolve` routes a revision of the group's contract that owns the path, never a dead stop. A generated mirror (`.claude/**`, `.pair/knowledge/**`… byte-identical to its dataset file) is never such a path: run the adopted `mirror-realign-command` (`pnpm mirrors:regenerate`) and commit its output with the fix — custody judges a mirror by its dataset origin.
6. **Finite-state completeness**: make the whole decision table pass — every supported state and its invalid/boundary pair, the smallest interaction cross-product (test the actual collision resolver). A unit test of the function being changed cannot establish external semantics: prove an external command, format or runtime claim at its real producer/consumer.
7. **Lossless diagnostics**: an error that reports user input keeps actual, expected and candidate values distinguishable.
8. Resolve **every** finding in place. Never file a follow-up issue, never invoke `$writeIssue`, never leave a "tracked separately" note. If a finding is genuinely larger than the story, fix what belongs here and say plainly in the log what remains — the human decides at the merge gate.
9. `$attempt=2`: the verifier proved an approved witness still fails on your GREEN. Start from its exact failing command; do not re-plan, do not touch the contract, do not widen the scope.

### Step 3: Prove and commit

0. **Changeset**: Changeset: `.changeset/<story-id>.md` mirrors the PR description and states the bump (below 1.0 a breaking change is `minor`); write it, or refresh it when the description changed, and commit it with the change. A PR with no release-relevant change takes the `no-changeset` label instead. Never touch a sealed test artifact for it.
1. Re-run every witness command from the manifest (all green), every control (still green), the findings' evidence commands and the mapped boundary cases. Record each run's `command`, `identity` (`cycle-state.mjs test-identity --cwd $worktree --command "<cmd>"`) and `exitCode`.
2. Run `/pair-capability-verify-quality` for the story's tier. Record any forced decision with `/pair-capability-record-decision`.
3. Commit GREEN strictly on top of the snapshot (or the previous GREEN on attempt 2); remove only the transient manifest path in that commit. Push.
4. Re-invoke `/pair-capability-publish-pr` (create-or-update): it rewrites the PR body to describe the CURRENT head and keeps tags and `pr-state:*` in sync. It emits `Review: review-dispatch-required`; expected — the coordinator drives the final verification.

### Step 4: Log, escalate if you must, persist

1. Append to `$reviewLog` a compact `## Round <n> — <phase> attempt <a>` table: `finding id | severity | location | what changed | commit`, then `## Evidence ledger`: `claim | authoritative oracle | exact command/fixture/revision | observed output` — one row per measured or factual claim the fix asserts or propagates. One row per line.
2. If you must return `needsHumanDecision: true`, publish the escalation comment yourself — schematic: the rounds so far, the still-open findings by id, what the human must decide — with the idempotent script shipped beside this file: `node "$SKILL_DIR/scripts/pr-comment.mjs" upsert --pr $pr --marker "<!-- pair:escalation #$story PR#$pr run:$run -->" --body-file <draft.md> --dir "$RUN_DIR"` (it reads back the PR's comments first and edits THIS run's existing escalation in place; the first-review comment and earlier cycles' comments are never touched).
3. Publish the handoff (`skill: "green-fix"`, `inputHead: $head`, `snapshot`, `attempt`, `fixed`, `needsHumanDecision`, `outputHead`, `remediationBatchId: "r<n>"` — `<n>` is `$phase`'s round, the same value every group/commit of this round shares (US-479 T-21, S4: one batch is all dependency-ordered corrective groups from one review baseline before the next complete review) — `findings: [{ id, transition, … }]` — an ARRAY, one entry per finding you received, carrying the transition your fix gives it (`resolved` when the witnesses prove it closed, `open` when it remains); the object shape `{ received, resolved }` belongs to red-spec only and `publish` refuses it here as `findings-not-an-array` (canary v9) — `evidenceLedger`, `testRuns`, `contractGaps`, `published: { escalation }`, `elapsedMs`) with `cycle-state.mjs publish … --workflowVersion $workflowVersion --attempt $attempt --predecessor $phase-red-verify --pr $pr` (`publish` requires `--workflowVersion`) (attempt 2: predecessor `r<n>-review-phase`), run `resolve` again and return its `next` **verbatim** — copy the whole object the script printed; never retype, summarize or drop a field it carries because another field in your answer already seems to say the same thing (e.g. `contract`, next to a `contractHash` you also state). The orchestrator checks the object's shape, not your restatement of it; a hand-reconstructed `next` missing one field is refused as unusable.

**US-479 S11 — active regression guards.** `$regressionGuards` arrives with the group's findings: those guards are part of what you must make pass, alongside the original obligations. Fix FORWARD only — no `git revert`, reset, rebase, force-push, seal deletion or history rewrite is ever part of this algorithm, and `lastCleanReviewedHead` is never checked out as the branch position. It is a source of CONTENT, which is a different thing: see `$reconstruct` below. Preserve every guard and every sealed byte, and never declare the batch complete: only the independent review that closes the original findings AND discharges every active risk does that.

**US-479 S12 — no production work without the complete seal.** Start only from a sealed contract
whose applicable matrix rows are present and validated: if the seal is missing, partial, or its rows
were reduced after validation, stop and return the typed refusal instead of coding. You may never
edit, weaken or drop a sealed row — including a regression guard — to make your change pass.

**US-479 S13 — `$reconstruct`: rebuild from the head a human chose.** This argument appears only because a maintainer read the escalation and named `fromHead` — a 40-hex commit they read from `git log` — rather than keep patching. They own that call: you do not re-litigate it, and the workflow did not infer it. It may arrive again on a later rewind: the directive stands while the maintainer's policy names that head, and only they clear it (ADR-024 (u)). If your rebuild is already what `paths` contain, restoring them at `fromHead` is what the standing decision asks for — say so in what you report overwriting. Start over from there:

1. restore the content of exactly `paths` as it was at `fromHead` (`git show <fromHead>:<path>` into the working tree, or the equivalent) — those paths and nothing else, in your worktree only;
2. rebuild the fix from there, carrying the group's obligations and every guard in `riskIds`;
3. carry `notes` into the rebuild: `notes.obligations` are what is still owed, `notes.regressions` the live guards, and `notes.worked` the decisions a review already VERIFIED as right in the work being discarded — reuse them instead of rediscovering them, which is the whole reason the field exists;
4. commit FORWARD on the current head.

This is a CONTENT operation. The branch stays where it is, the sealed snapshot stays an ancestor, every sealed test byte stays identical, published reviews stay valid — `verify-chain` proves all of it. Nothing specified is lost by starting over: the contract you hold IS the inventory of what must work again, and the guards make the old defect impossible to reintroduce silently. If restoring the content cannot be confined to `paths` — a consumer outside them breaks, or the rebuild would grow past your `fixScope` — stop and return the typed refusal with what you found; do not restore partially and do not widen the scope yourself. Report what you had to overwrite: the maintainer who named the head is entitled to know what it cost.

## Output Format

`{ status: fixed | failed | human, fixed, needsHumanDecision, outputHead, evidenceLedger: [{ claim, oracle, probe, observed }], contractGaps?, reason?, next }`. `evidenceLedger` is `[]` only when the fix made no empirical or boundary claim.

## Notes

- A `mode: test` group never reaches this skill: the guard is the fix, and the final verifier checks it directly on the sealed head.
- `mode: doc` (prose-only, `.pair/knowledge/guidelines/collaboration/automation/doc-remediation-groups.md`): edit ONLY the prose files in `fixScope.allowedPaths`; there are no witnesses to run — re-read each `checklist` item against its authority and return an `evidenceLedger` with one entry per checklist item id (`{ checklistId, file, line, text }`: the changed sentence). Run the project's usual conformance/link tests for the files you touched.
- Do NOT post any other PR comment; the final verifier publishes the synthesis. Never merge.
- Blind: read nothing under `.pair/working/` except the checkpoint, `$reviewLog` and `$RUN_DIR`.
- Your handoff publish is observed by the host runtime (`cycle-runtime.mjs`, US-479 T-25) as a phase-level progress point, through `cycle-state.mjs` — never something you invoke yourself.
