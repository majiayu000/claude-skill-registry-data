---
name: pair-workflow-red-verify
description: "Stage 2 of the delivery workflow — independent contract validation and deterministic seal in one execution: reproduces every witness and control of a prepared acceptance contract against the unfixed base, re-derives the inventory's classes and interactions from the authoritative producer, checks discriminance (a witness fails for the intended defect, a control may pass, a test-only fix fails on the injected regression), fixture consumption and fixScope, emits ALL concrete gaps it found in one typed rejection with stable row ids — and, when the contract is verified, runs red-snapshot.mjs seal in the same execution and returns the snapshot. Never repairs a contract, never edits production. Dispatched by the batch engine (pair-implement-batch)."
version: 0.2.0
author: Foomakers
---

# /pair-workflow-red-verify — Prove the Contract, Then Freeze It

A contract is evidence only once someone who did not write it reproduces it. You are that someone. You never repair the contract: you name every gap you find, once, with the row it concerns — or you seal it. Sealing is Git custody, not reasoning: the script decides.

## Arguments

| Argument           | Required | Description                                                                                                                              |
| ------------------ | -------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `$run`, `$story`, `$branch`, `$worktree`, `$base`, `$stacked`, `$entry`, `$policy`, `$inputs`, `$workflowVersion` | Yes | The cycle arguments, as every stage receives them. Handoffs live under `.pair/working/runs/$run/$story/` in the MAIN checkout. |
| `$phase`           | Yes      | `a0` · `a0-rev<m>` · `r<n>-g<k>` · `r<n>-g<k>-rev<m>`.                                                                                     |
| `$head`            | Yes      | 40-hex head the contract was prepared on; `HEAD` of the worktree must be exactly this.                                                    |
| `$contract`        | Yes      | Absolute path of the prepared contract JSON (main checkout's run directory — pass it to the script as-is, never relative to the worktree). |
| `$contractHash`    | Yes      | The hash the preparation stage recorded; `node "$SKILL_DIR/scripts/cycle-state.mjs" hash --file $contract` must reproduce it.             |
| `$pr`              | No       | PR number, when one exists.                                                                                                              |
| `$findings`        | No       | JSON array: the obligations the contract must cover (finding ids are the inventory ids you check `covers` against).                       |
| `$regressionGuards`| No       | The authoritative ACTIVE regression risks the resolver derived (US-479 S11/F-RR-03). Compare this set against the contract AND the ledger: a guard missing, extra, mutated or weakened is a rejection BEFORE the seal, and your answer echoes the exact `riskId` set you validated. |
| `$scope`           | No       | JSON `{ groupId, owner, mode, allowedPaths, widen? }` of the planned group; the contract's `fixScope` may be narrower, never wider — unless `widen: true` (a revision a GREEN's contract gap opened): then it may ADD the paths the `contract-gap` findings require, each tied to its gap in the inventory. |

## Algorithm

**Headless execution (single owner: `.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/headless-stage-execution.md`)** — this stage runs headless: never leave a command in the background and never end your turn while a command runs (a push with a pre-push gate, a quality gate): use the maximum tool timeout, poll to completion in the same turn, and ALWAYS end with the stage's structured result — on partial progress `{ status: "failed", reason: "incomplete", detail, branch, outputHead }`.

### Step 0: Resolve the durable state (mandatory)

```bash
SKILL_DIR="$(dirname "<absolute path of this SKILL.md>")"
MAIN="$(pwd)"                                   # the main checkout — you have not cd'd yet
RUN_DIR="$MAIN/.pair/working/runs/$run/$story"
AC_HASH="$(node "$SKILL_DIR/scripts/cycle-state.mjs" ac-hash --story $story --dir "$RUN_DIR" | node -pe 'JSON.parse(require("fs").readFileSync(0,"utf8")).acHash')"   # canonical card hash — the SAME input every stage resolves with
node "$SKILL_DIR/scripts/cycle-state.mjs" resolve --dir "$RUN_DIR" --workflowVersion $workflowVersion \
  --policy '$policy' --entry $entry --story $story --inputs $inputs --acHash "$AC_HASH" --runsRoot "$MAIN/.pair/working/runs" ${pr:+--pr $pr}
```

- `status: other-run` ⇒ return `{ status: "other-run", runId }`. `incompatible | invalid` ⇒ return `{ status: "redirect", next: { step: "blocked", reason: "failed-resume", detail: <reason> } }`.
- `next.step` is not `validate`, or `next.phase` is not `$phase` ⇒ return `{ status: "redirect", next }` verbatim. Spend no judgment. When `next` names THIS dispatch (`validate`, `$phase`) you ARE the step: continue, never return a redirect to yourself.
- Otherwise continue; `next.attempt` is your attempt number.

### Step 1: Read the contract, verify the tree

1. Parse `$contract`; its `contractHash` must equal `$contractHash` and the script's `hash` output — a mismatch is a finding (`location: $contract`), `verified: false`.
2. `cd $worktree`; `HEAD == $head`; the uncommitted diff contains ONLY the listed artifacts. Every artifact path is repository-relative; `sha256sum` of each equals its stated digest. Anything else ⇒ finding, `verified: false`.
3. Every artifact PASSES the project's format gate (US-479, canary 481-v1). Run the adopted check over the listed artifacts (`pnpm format:check`, or whatever `way-of-working.md` adopts; a project with none skips this). An artifact the formatter would rewrite is a gap like any other — name it with its path, `verified: false` — and NOT a reason to reformat it yourself: you never edit. This is not tidiness. The seal you are about to place makes these bytes untouchable, so an unformatted artifact hands the fixer a round it cannot finish: it cannot reformat (sealed) and cannot push (the pre-push hook runs the gate). Canary 481-v1 died there with the fix already written and green.
4. `fixScope` has one owner, one mode, only the paths the contract needs, and is not wider than `$scope` (with `$scope.widen: true`, only by paths a `contract-gap` finding requires — any other added path is a gap). A `repair` or `revision` (`-rev<m>`) is not NARROWER than the contract it revises: same `mode`, every predecessor `allowedPaths` entry still present — the sealer re-checks this against the predecessor snapshot's manifest and refuses `fixScope-narrowed`; name the dropped paths as a gap.

### Step 2: Reproduce (every row, every artifact)

1. Run every `redTests[]` `command` yourself while production is unfixed, and KEEP what each run printed (US-506 AC-10): a `baseline: red` witness must FAIL as `observed` says; a `baseline: pass` control must PASS. Record every run as `reproduced: [{ rowId, baseline, command, exitCode, observed }]` — the command exactly as you ran it (no shell syntax), its real exit code, the output you saw. A witness that exits 0 here CANNOT FAIL (`toHaveReturnedWith` on an async mock, an assertion the setup already satisfies): that is a finding, and `publish` refuses a verified handoff whose witness has no failing run (`witness-cannot-fail:<rowId>`) or whose control has no passing one (`control-cannot-pass:<rowId>`). A verified handoff without these rows is refused (`reproduced-missing`) — the claim "reproduced" is proven, never asserted. For a `mode: test` contract reproduce the injected regression the author describes: the guard fails there AND passes on the current source; a guard that cannot be made to fail proves nothing.
2. Run every `matrix[]` `oracle`; the result must equal `expected`. A `not-applicable` row's `rationale` is re-derived from the producer — if the class can occur, that is a finding on that row.
3. Trace each `kind: fixture` artifact to the exact failing assertion of its `consumedBy` test. A declared fixture column that no expectation reads is not a test.
4. Treat any unsupported claim ("does not compile", a count, a version fact, a prose-regex standing in for behavior) as a finding unless its stated oracle demonstrates it.

### Step 3: Re-derive the inventory

Independently derive, from the authoritative producer named by each `inventory` item (the function that mutates the state, the grammar, the command — never a downstream consumer), every class the producer recognises including the ordinary complement and the smallest interaction cross-product. Every class must be `covers`-ed by a row that discriminates; a missing class is a finding **even when every supplied row passes**. Equivalence between two classes is accepted only with a shared behavioral/grammar rule stated in `rationale`, never because outputs agree today.

**Enumerate first, only then decide** — for every inventory producer list, and check each has a discriminating row:

- (a) every representation/consumer: the pure function AND every CLI/script entry that wires it;
- (b) every value of every enumerated input dimension the guard is generic over (each channel, mode, kind — never one standing for all);
- (c) the interaction pairs between (a) and (b).

Every missing entry is a gap in THIS rejection; a later pass may not raise one that existed now.

### Step 4: Decide — ALL gaps in one answer

Report **every** concrete gap found in this pass as findings `{ rowId?, mechanismId?, location, severity, description (the failing example / the violated rule), recommendation (the evidence required), obligationIds?, sourceRef?, observedHead?, closureAssertions?, reproducer?, applicability?, counterexampleToCurrentContract?, changedRows? }` — stable `rowId`s so the repair can be traced. Never return the first gap and stop; a second pass on the repaired contract may only add gaps that the repair introduced or that need new evidence.

**US-514 T-2 (#514/AC1, revised — a FLOOR compared by RANK, never a list) — which gaps REJECT is `rank(gap.severity) >= rank($policy.blockingFloor)`, `$policy.blockingFloor` absent ⇒ the KB default floor `Minor` (today's behaviour: every gap except a `Questions`-ranked one blocks). Ranks are resolved by `publish` itself, in order — `policy.severityRanks`, then the on-disk resolved template contract, then pair's own default table; the handoff's top-level `severityRanks` (never a per-gap field), when stated, is checked ONLY for agreement with whichever `publish` resolved (a disagreement is the typed refusal `severity-ranks-mismatch`, never an alternate ranking). A gap no resolved rank covers blocks (fail-safe), an unrankable floor releases nothing (fail-safe).** A gap AT OR ABOVE the floor blocks: `verified: false`, no seal this pass. A gap BELOW the floor is recorded on the contract as a **non-blocking note** — it does NOT by itself refuse `verified: true`, and does not consume the repair budget. **Structural shape is never a severity-filtered gap**: `contractErrors()` (the shape check `publish` runs before you are even dispatched, US-514 T-5) is orthogonal to this — a shape defect never reaches you as a finding to weigh at all. `verified: true` requires zero BLOCKING findings and every command reproduced; a run with only non-blocking notes still seals, and the notes travel with it (a Minor gap on a project declaring the floor `Major` is the concrete case: it seals on the first pass, the note visible on the contract).

**Naming a mechanism makes it a debt you must close in THIS answer (US-479 T-20, S3):** when a gap concerns a distinct mechanism (e.g. one of several independent producers/rewriters this contract touches), give it `mechanismId` and either:

- `closureAssertions: [{ id, command | testRef, expected }]` — at least one executable reference, never a prose description standing in for behavior (a hand-built stand-in that was never actually run through the real producer proves nothing — Step 3 already requires independent re-derivation from the authoritative producer; a `reproducer.command` you cite must be the command you actually ran, never shell syntax pasted for later execution), or
- `applicability: 'not-applicable'` with a non-empty `applicabilityRationale` — an independently approved reason the class cannot occur, never a shortcut to skip evidence.

When you declare `mechanismsIdentified: [ids]` (the complete set of mechanisms you found broken THIS pass), `publish` refuses the handoff unless every declared id is closed by a finding and no finding names an undeclared one — this is what stops one rejection naming rewriter A while rewriter B, already known broken in the same pass, waits for a second round (canary run 3: two independent Markdown rewriters split across successive rejections). Declaring the set is optional per rejection, but once you do, it is checked exactly.

### Step 5: Seal (only when verified) — the script decides

```bash
cd $worktree && node "$SKILL_DIR/scripts/red-snapshot.mjs" seal --pr $SEAL_PR --phase $phase --base $head --contract "$contract" --root "$MAIN" \
  --static-gates '<JSON: the repo static gates, e.g. [{"name":"lint","command":["pnpm","exec","eslint","{file}"]},{"name":"tsc","command":["pnpm","exec","tsc","--noEmit","-p","<the tests tsconfig>"]}]>'   # SEAL_PR: 0 for the initial chain (a0, a0-rev<m> — it predates the PR and keeps that identity), $pr for a remediation group
```

**The pre-seal guard (US-506 AC-9)** runs inside `seal`, before anything is committed, and refuses with a typed reason naming the file: `static-gate-failed` (a listed test fails one of the repo's static gates — pass the ones `way-of-working.md` adopts, `{file}` runs a gate per test file, `{files}` once over all; `'[]'` only when the repository has none: the flag is required, the sealer never seals blind). Independently of the flag the sealer also runs each listed test's OWNING package `lint` script (nearest `package.json`, the root included; cwd = that package dir, so its own config and rules apply — what the pre-push hook enforces) and refuses `static-gate-failed` (gate `package:lint`) only for a lint message located in a LISTED test file: a violation in another file never blocks, a lint run that fails without any report fails closed, an unparseable `package.json` is refused `package-json-unparseable`. `ts:check` is NOT derived (a RED witness may import what does not exist yet): pass the tests' tsc gate yourself when the repo adopts one. A gate that hangs is killed with its whole process tree. So `'[]'` can no longer seal a test the package lint rejects (defect AQ), `test-spawns-gh` / `test-reaches-network` (every witness command is probed once with a `gh` trap first on PATH and a preload that refuses non-loopback sockets — a test stubs its own `gh`, never reaches the real one), `predecessor-hash-unmatched` (a `predecessorContractHash` that is no sealed predecessor's contract hash), `changed-rows-omit-witness` (a revision whose rows leave a witness file its diff modifies uncovered — a genuine gap). Each is a gap in the contract: return it as a finding, never work around it.

**Revision mechanics the sealer handles (US-587), never gaps:** `changedRows` is DERIVED — the agent's list unioned with every row the diff adds or edits (widening only), the merged list recorded in the manifest; a revision witness unchanged at HEAD seals as a `reattest` with the visible reason `witness unchanged at head` (an explicit `reattest` is untouched); a revision `red` witness that already passes at the GREEN head is recorded as a control (`baseline: pass`, its rows too — `preSeal.reclassified` lists them) unless that would leave no red witness.

The script (shipped beside this file, [scripts/red-snapshot.mjs](./scripts/red-snapshot.mjs)) validates the contract path ONCE against the declared main checkout (`--root`: no `..`, under `<root>/.pair/working/runs/`, real path inside it — a symlink pointing elsewhere is an escape; a relative path resolves against the root, never the worktree), then verifies `HEAD == $head`, every artifact's `sha256`, that the tree is dirty only at those artifacts (a `pass` control may be unchanged), writes `.pair/red-snapshots/pr-$pr-$phase.json`, and creates exactly one local `--no-verify` commit carrying `Pair-RED-Snapshot: pr=…; phase=…; base=…; manifest=…`. It is idempotent: re-running after a lost response returns the existing snapshot. A revision (`-rev<m>`) seals as a SUCCESSOR snapshot on `$head`; the earlier seal stays history. Do not retry with a different contract, edit any file, amend, rebase, reset, push or post to make it seal: `{ sealed: false, reason }` is the answer, returned as `sealed: false` with `reason`.

**`fixScope.mode: test` — push the seal yourself.** A sealed `mode: test` group has no green step (`resolve` routes it straight to the re-review: the sealed tests ARE the fix), and `green-fix` is what normally pushes the seal with its GREEN commit — so without this the snapshot stays a local commit and the final verifier's custody check breaches `snapshot-missing`. Right after a successful seal of such a group, run `cd $worktree && node "$SKILL_DIR/scripts/red-snapshot.mjs" push --snapshot <the snapshot sha> --branch $branch` (it first makes the same manifest-removal commit `green-fix` makes — the repository's pre-push hygiene gate rejects a tracked `.pair/red-snapshots/*.json` — directly on top of the seal, then a plain, never-forced, never-`--no-verify` push read back with `ls-remote`; idempotent; the snapshot stays an ancestor and the verify-chain allows the removal). `{ pushed: true }` ⇒ record `pushed: true` and `outputHead` (the remote head, the removal commit) in your handoff. Any `pushed: false` (`push-rejected`, `push-not-confirmed`, …) ⇒ do not report the group as verified-and-ready: return `{ status: "failed", reason: "seal-not-pushed", detail }`. Other modes never push here.

**`fixScope.mode: doc` — validate the checklist, not tests.** A doc contract (`.pair/knowledge/guidelines/collaboration/automation/doc-remediation-groups.md`) has no `redTests` and nothing to reproduce: check the inventory, that `allowedPaths` are prose only, and every `checklist` item against its authority (one typed gap per item id). Your handoff carries `contractMode: "doc"` and `checklistValidated: [<every item id you validated>]` instead of `reproduced`; then seal (the snapshot is the manifest alone). Nothing is pushed here: `green-fix` follows (a doc group is not routed past it).

### Step 6: Persist and hand off

Publish the handoff (`skill: "red-verify"`, `inputHead: $head`, `inputsDigest`, `attempt`, `verified`, `findings`, `sealed`, `snapshot?`, `manifest?`, `contractHash`, `contractPath` (the file you validated — `$contract`; `publish` stamps it from the phase's latest preparation when omitted and refuses a different one, `contract-path-mismatch`, so every rejection points at its own attempt's file), `reproduced: [{ rowId, baseline, command, exitCode, observed }]` (Step 2.1 — required when `verified: true`), `elapsedMs`) with `cycle-state.mjs publish … --workflowVersion $workflowVersion --attempt $attempt --predecessor $phase-red-spec ${pr:+--pr $pr} --policy '$policy'` (`publish` requires `--workflowVersion`; omitting it is `workflowVersion-invalid`, not a published handoff), run `resolve` again and return its `next` **verbatim** — copy the whole object the script printed; never retype, summarize or drop a field it carries because another field in your answer already seems to say the same thing (e.g. `contract`, next to a `contractHash` you also state). The orchestrator checks the object's shape, not your restatement of it; a hand-reconstructed `next` missing one field is refused as unusable.

**US-479 S11 — active regression guards.** When `$regressionGuards` is given, every guard is part of the contract you validate: reproduce each one on the failing head named by its risk, confirm the obligation it cites still passes on `lastCleanReviewedHead`, and reject the contract when a guard is missing, unexecutable or non-discriminating. A guard is not a row you may waive.

**US-479 S12 — reject an incomplete transition matrix.** When the contract changes a persisted
state, a ledger transition, a terminal gate or an evidence identity, a single positive path is NOT
proof of the transition. Check that every applicable negative family of S12 is present with a
deterministic witness and a typed expected refusal, and that the authority you were handed
(`$regressionGuards`, the heads, the batch identities) agrees with the contract. A missing family is
`contract-incomplete:<transition>:<family>`; an inconsistent one is a gap like any other. Never seal
a matrix you could not reproduce.

**Handoff hygiene (publish refuses otherwise).** The handoff envelope ALWAYS carries `run`, `story`, `phase`, `skill`, `inputHead` (a 40-hex sha) next to the stage fields — a missing one is `missing-field:<name>`. Every command you record (`reproduced[].command`, witness/control commands, `counterexample.command`) is a single command that must not start with `cd … &&` nor contain `;`, `&`, `|`, a backtick, `$(`, a redirection or `../` — the validator refuses it as `*-command-unsafe`. Run it from the right directory with the tool's own flag instead: `pnpm --dir <dir> exec <tool> …` / `pnpm --filter <pkg> exec …` / `node <path>`.

## Output Format

`{ status: verified | rejected, verified, findings: [{ rowId?, mechanismId?, location, severity, description, recommendation, closureAssertions?, reproducer?, applicability? }], mechanismsIdentified?, sealed, snapshot?, manifest?, contractHash, regressionGuards?, reason?, next }`.

## Notes

- Read-only on the repository except the seal commit the script makes. Never edit, format, push, publish, comment, create a card or merge; never rehash a changed artifact into approval.
- Blind: read nothing under `.pair/working/` except `$RUN_DIR`.
- A typed rejection is the cycle's answer: the coordinator routes it to ONE repair; a second rejection exhausts the unchanged budget. Never soften a gap's SEVERITY to let the contract through — `$policy.blockingFloor` is the only thing that ever changes whether a correctly-severed gap blocks.
- A repair naming `changedRows` that drops one of this rejection's `rowId`s (when this rejection's findings carried one) is refused by `publish` before it is written — verify every prior closure assertion holds before treating anything as newly closed.
- Your handoff publish is observed by the host runtime (`cycle-runtime.mjs`, US-479 T-25) as a phase-level progress point, through `cycle-state.mjs` — never something you invoke yourself.
