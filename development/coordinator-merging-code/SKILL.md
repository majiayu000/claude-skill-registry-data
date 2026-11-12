---
name: coordinator-merging-code
description: "Use the moment code is presented for merge - a merge report arrives, an agent says MERGE-READY or RECOMMEND MERGE or the branch is ready, you are asked to approve or land or ship a branch, you are about to run git merge, or you are consolidating review findings before a merge. Loads the full merge sequence - dual review as a PRECONDITION not the gate, the mechanical merge-worthiness pre-gate, DISPATCHING both merge gates to the Gate Runner rather than walking the lenses yourself, tripwire checks, gating the MERGED tree, the committed verdict artifact, and branch disposal."
---

# Coordinator: Merging Code — the full sequence, every time

**Check whether you are the merge king for THIS branch before running this
sequence.** Do not assume — read it from config:

```bash
jq -r --arg b "$(git branch --show-current)" \
  '.orchestration.merge_kings[$b] // "unset"' .thrum/config.json
```

If it names you, you are the merge king for this branch — proceed with the
sequence below. If it names someone else, route the merge to them instead of
running it yourself. Nothing lands except through this sequence, run by
whichever coordinator the map names.

**`orchestration.merge_kings` may not be populated for every branch yet** (the
jq command above will print `unset` in that case). An `unset` result does NOT
mean "nobody is merge king, proceed" — it means the map hasn't caught up to
this branch. Fall back to whichever coordinator has actually been the merge
authority for this branch in practice (check with your team, or your
project's own operational convention); if that is not you, route the merge
to them the same as if the map had named them explicitly.

## LAND ON GREEN — read this before anything else in this skill

**If a green gate run comes in, that is enough. Land it in the same turn.**
Sending a green change back costs hours on every landing and delays all
development. Nothing below in this skill overrides this section; where another
line seems to, this section wins.

1. **Green run + clean merge against trunk = merge now**, in the turn the
   verdict, or the request to land, arrives.
2. **Trunk moving never invalidates a green run.** The gate takes trunk once for
   its landing tree. Do not ask for a merge-forward, a fast-forward, a rebase or
   a re-run because trunk has moved since.
3. **No "delta gates".** A merge-forward followed by a second gate of the new
   tip is the same send-back loop under another name. So is a "validation run",
   a "confirmation run", a "re-pin", a "re-admit" or a "fresh full gate" of a
   change that already has a green run. Do not ask for any of them.
4. **Minor findings do not reopen a gate.** If a small commit on the branch
   already fixes them, land the tip and name that commit in the merge message.
   If they are not fixed, land and route the fix as a follow-up.
5. **Generated-file conflicts are the gate's to regenerate**, as a
   gate-authored commit on the landing ref, with no race re-run and no trip
   back to the implementer.
6. **No post-landing verification gate.** The next gate's landing tree contains
   the landing and covers it.
7. **Do not hold a ready change behind another landing** unless the two
   actually conflict when merged.
8. **A chain of branches built on top of each other lands as ONE merge.** They
   build on each other; gate the top of the chain once (it contains the rest)
   and merge it once. Do not gate or merge the links separately, and do not ask
   for four merges when the chain has four links.
9. **A request to land gets a merge or a named blocking finding**, with the
   failing test name or the file and line. Never a status report, and never a
   place in a queue.

### What the per-landing gate runs (owner ruling, 2026-10-11) — no race on every landing

**A full race is NOT run for every landing.** Landings go in on a non-race
gate, and trunk is raced in batches. **Nothing gets to deploy without a race.**

The per-landing gate:

1. Landing tree on trunk, taken once.
2. Build and vet (default and darwin).
3. The NON-RACE lane (the project test runner's `norace` lane, one concrete package per
   call) for the packages the diff touches. The non-race lane runs every test;
   the race lane runs the same tests with the detector on.
4. The structural checks (shard configs, census coverage, the guard tests the
   change names); the gate regenerates generated files itself.
5. Only where the change is itself a concurrency change — it adds or changes a
   lock, a channel, a goroutine, a context-cancellation path, or a fence
   against a concurrent actor — also the change's OWN focused race selectors
   (the tests it adds), not the whole package under race.
6. An explicit verdict with the landing ref. Green lands the same turn.

Batch the slow whole-system checks: full race, regression and load tests.

- These never run per landing. Gate-green candidates land immediately; nothing
  waits for them.
- After every N landings, run each check ONCE on trunk's tip (the race as the
  project test runner's `race all`, to one gate). N defaults to **5**; the user
  may set a different N.
- A race failure is attributed to a landing by test name and stack trace and
  fixed as a follow-up. A regression or load result worse than the last good
  run is bisected across that batch's landings. Landings are not unwound, and
  later landings do not wait.
- Gates do not hand per-candidate commits to the regression runner.
- **A bundle is built only from a trunk commit whose latest batch race and
  batch regression run are both green.** If either is older than trunk's tip,
  run it on the tip first.

A non-race run may take a pool slot above the cap (lower load); a race run
uses a normal slot.

### Changes with no production code — no gate, no load test

A gate or load test re-runs code the change did not touch, so it cannot find
anything in these diffs:

- **Comment-only or docs-only:** merge directly.
- **Test-only** (test files and test fixtures): the author reports that the
  changed tests ran and passed, with the runner's return code and the executed
  count. The coordinator confirms the diff touches no production file, then
  merges.
- **Any production line in the diff:** the normal per-landing gate.
  Regression and load tests do not run per landing (see the batch rule above).

A comment that carries meaning to the compiler (`//go:embed`, `//go:build`,
`//nolint`) and any file embedded into the binary count as production. See §5.

The only things that stop a landing: a failing test that the change itself
causes, named; a blocking review finding, with file and line; a hand-written
merge conflict (the implementer resolves that one conflict, and only the
conflicting part is checked again); or no gate run at all, in which case the
change goes on a gate as that gate's next job, not back to its author.

> 🔴 **THE ONE THING MOST OFTEN GOT WRONG: YOU DO NOT RUN THE GATES. YOU DISPATCH
> THEM TO THE GATE RUNNER.** See §3. A coordinator that walks the lenses inline
> burns the one resource it cannot replace and leaves **no auditable verdict** —
> and it will feel like diligence the entire time.

## 0. What this skill is, and what it is not

This is the **coordinator-facing index and running order.** The lens content lives
in the two gate skills; the runner's own discipline lives in the `gate` role
preamble.

**Do not duplicate lens definitions here.** Point at them and keep the order.

## 0a. OVERBUILD CHECK — first step, before any gate

Before a product branch goes to a gate, run one judgment-tier sub-agent with
`resources/overbuild-check-prompt.md` from this skill's folder. Fill in the
ask (issue, plan, dispatch message), later rulings and gate findings, the trunk
ref, the branch tip and the owner's report.

- **PROPORTIONATE:** continue to §1.
- **OVERBUILT:** send the findings to the owner for the simplest version, with
  a files-and-lines plan first. Do not dispatch a gate.
- **UNCLEAR:** read the findings against source and decide.

Run it on EVERY tip before you dispatch it, including a re-gate after review
rounds, and also when an owner reports scope or progress mid-build. A landing
recipe in your own notes or snapshot does not replace this step.

Tripwire, checked by eye before anything else: if the ask fits in one sentence
and the production diff is over 100 lines, or it adds any condition the ask did
not name, treat it as OVERBUILT until the check says otherwise. Each review
round that adds code is a reason to rerun the check, never a reason to skip it.

Test-only, docs and tooling branches skip this step.

## 1. PRECONDITION — dual review, and it is NOT the gate

Two axes, run in parallel, on the branch: **code-quality** and **spec-compliance /
verify-against-plan**.

**Before treating dual review as clean, confirm BOTH axes EMITTED** — name the
agent and either one finding or an explicit zero, per axis. **An absent report and
a clean report are different things**, and silence defaults to the reading you
want. If an axis goes silent twice, re-route it rather than re-spawning.

**A review verdict attaches to the change it read.** If the branch takes a new
commit that changes behaviour after review, a reviewer reads that commit before
it lands. A merge of trunk into the branch, a regenerated generated file, or a
commit that only fixes a minor finding the gate already named is NOT a new
object: the prior review and the green gate run stand, and nothing is
re-dispatched for it (see "LAND ON GREEN" above).

**Consolidate into ONE numbered list** across all severities before anything goes
back to the implementer. Never send partial findings; they fix batch 1 and miss
batch 2.

**Verify a finding against source before forwarding it, and verify pushback the
same way.** Reviewers misread files. Pushback is a feature, not insubordination —
and a trace-correction from an implementer is welcome.

## 2. MECHANICAL MERGE-WORTHINESS PRE-GATE — run every time, in this order

```bash
# 1. FETCH BRANCH-EXPLICITLY. A bare `git fetch` is not enough.
git fetch origin 'refs/heads/<branch>:refs/remotes/origin/<branch>'

# 2. RESOLVE FROM ORIGIN, NOT THE LOCAL CACHE. `origin/<branch>` is a cache of your
#    last fetch and will happily report a branch that never left the submitter's box.
git ls-remote origin <branch>

# 3. PROVE THE OBJECT EXISTS *BEFORE* ANY ANCESTRY CLAIM. A fabricated sha and an
#    unfetched one produce IDENTICAL not-ancestor output.
git cat-file -t <sha>

# 4. ANCESTRY — MIND WHICH PAIR. Doubtful thing on the RIGHT, known base on the LEFT.
git merge-base --is-ancestor <base> <tip>
# CONTROL: an invented/all-zeros sha must FAIL the same check.
```

🔴 **`--is-ancestor <merge-base> <tip>` is TRUE BY DEFINITION — a vacuous green.**
When you supply SHAs anywhere, **say which PAIR to test**: the tree WITHOUT the
change and the tree WITH it.

**Assert HEAD is attached** (`git symbolic-ref -q HEAD`) and that you are on the
merge target before merging.

## 3. THE MERGE GATES — DISPATCH BOTH TO THE GATE RUNNER

1. Select from your team of established long-running gate agents.
   **Spread the load:** if you have more than one gate runner, don't send everything to the same one. List them
   with `thrum team --all --role gate --compact`, compare against the assignees in `thrum queue list`, and spread
   gates across every idle runner. Only live rows (marker ◍) are candidates; ☓ retired and ☾ sleeping
   rows are not.
2. Choose an available pair for hot-path and philosophy.
3. Tell those agents where sensitive tests must execute.
4. Launch a new gate agent only if the persistent set is genuinely unavailable —
   never merely because an old candidate-specific session is stale.

**Combine, don't gate one branch at a time.** Each gate box builds ONE combined merge tree from
its queued items: related branches together, small ones folded in with the large, merged onto current trunk one
after another with a clean merge-tree check at each step. It runs the required lanes once on that tree. The
regression and load tests run on trunk per the batch rule above, not per gate batch. A branch that conflicts
or fails is named and dropped
from the set; it goes back to its owner, and the rest proceed. Stacked branches always travel together. The gate
reports conflicts to you and never resolves them.

Record the dispatch on your own queue (`thrum queue assign <bundle> <gate-runner>`) per `coordinator-dispatching-work`'s
queue step before sending the gate dispatch. Without a Pro licence (`not entitled` / `requires a license`), skip this
write and track it in the message thread instead.

🔴 **WHERE THE LONG / tmux-SENSITIVE LANES RUN — a DEDICATED NON-FLEET gate box, never
a populated one.** The integration lane and the rpc race suite create FIXED-NAME tmux
fixtures on the shared fleet socket; on any box with live agents they COLLIDE, and every
such red is a FALSE positive you then burn effort classifying as "pre-existing/env." Run
them where the verdict is TRUE — a box with zero live agents. The value is a CLEAN verdict,
NOT speed (wall-clock is not faster; lane invocation serializes regardless of the
parallelism flags). **The specific box + ssh/access for THIS fleet is in project_state
(`DEDICATED GATE BOX`), not here — this rule is general.** If you catch yourself dispatching
the gate to a populated box "because the runner lives there," that is the exact forgetting
this line exists to stop.

| Gate | Skill | Skippable? |
|---|---|---|
| Hot-path | `coordinator-hotpath-merge-gate` | **Only** if the diff touches zero `trigger_directories` |
| Philosophy | `coordinator-philosophy-merge-gate` | **NEVER** |

**Read the trigger directories and the lens count FROM `.thrum/hotpath-gate.json`,
at the tree under gate — never from prose, including this file.**

⚠️ **If your trigger-dir query returns EMPTY, treat it as a broken key until
proven otherwise.** A typo'd `jq` path and a clean skip are byte-identical in the
output.

**Skip BOTH only for a one-line config change, a typo, or a diff with no
production code** (see "Changes with no production code" above).

**Dispatch is the default at every diff size.** Diff size changes what you ask
for; it never changes who runs it. Only run a gate yourself when **no** gate-role
agent exists — and then say so explicitly in the merge record, so the gap is
visible rather than invisible.

A gate finding with no failing test or reproduction can never block. Label it UNMEASURED, state the
likely cost, and name the test that would prove it. The coordinator forwards it only if the fix is
clearly worth the cost, never as a 'real risk', and the owner can decline it. Same principle as the
OVERBUILD CHECK (§0a): do not let an unproven worry become a cost to the owner.

### What the dispatch must contain

The gate answers the question you ask it. Four required sections:

1. **The enumeration key AND any output filter.** A gate can narrow the key
   without touching the key — widest grep, then filter the *output* on incidental
   vocabulary — and produce an identical confident "none" about a population it
   silently excluded.
2. **"VERIFICATION EXECUTED — every command + its EXIT, or the words NONE RAN."**
   A CLEAN that never states its support is **unfalsifiable** and silently
   defaults to the lane-backed reading. A static-only CLEAN is legitimate and is a
   DIFFERENT CLAIM.
3. **Name ONE test runner, or serialize the lane.** Parallelism is free for
   reading and unsafe for executing. The rpc suite creates FIXED-NAME tmux
   fixtures on the SHARED FLEET SOCKET; the resulting `duplicate session` failure
   is indistinguishable from a genuine branch regression.
4. **Diff each gate's proposed gate-log line against its own report body** before
   it lands. One contradicted itself precisely in the half a busy runner pastes
   unread.

Also supply **the SHA pair**, **specific questions** (a gate briefed with "review
this" returns generic coverage), and **the pre-cleared non-findings list** — things
already ruled zero-diff on purpose.

**Fence: split it.** The runner gets `commit`/`push` path-fenced to its own gate
worktree; its sub-agents get READ-ONLY git. `checkout`/`reset`/`restore`/`stash`/
`clean`/`rebase` forbidden in **every** directory for both. Give an escape hatch
for instrument-and-undo (a `cp` copy, or edit-then-revert) or the careful agent
breaches the fence doing good work. **Use `rm -r`, NEVER `rm -rf`.**
**Pasting a fence is not enforcing it.** This same fenced commit capability is
what the sanctioned `GATE-AUTHORED` mechanical-bookkeeping-fix commit uses — it
is not a new permission grant.

## 4. THE EXECUTED VERIFY — SCOPED TO THE CHANGE

The §3 lens gates (hotpath + philosophy) are the judgement half. The per-merge
executed half is **scoped to the change**:

- Build the merged tree with the `build_merged_tree` command in `.thrum/gate-config.json`.
- Test and race scope: follow "What the per-landing gate runs" above. Never run
  it on primary (the shared fleet build box); run it on the gate box.
- The fast structural checks on the merged tree: every `structural_checks` entry in `.thrum/gate-config.json`
  (seconds each; they catch drift that does not depend on what the change touched).
- The `merge-base --is-ancestor` fast-forward check (§6).
- Any `*_tripwire_test.go` the change touches must stay green or the diff must
  state why its premise changed; a tripwire edited to accommodate the change is a
  finding, not a fix — **except** a mechanical follow-up (updating a stale
  expectation to merely track an already-landed, already-reviewed change: a
  renumbered line, a regenerated census key, and the like), which the gate may
  fix itself as a `GATE-AUTHORED` commit and re-run. A tripwire edit that changes
  what the tripwire actually *enforces* — any design or behavior judgment call —
  stays a finding, never a self-administered fix. Keep this distinction sharp;
  it is the highest-risk edit in this whole sequence.
- 🔴 **Checks that fire on a CLASS of change run on the merged tree every merge.** A check that fires on a pattern
  (a hand-rolled schema statement, a new writer of a guarded resource) rather than on the package it lives in is blind
  to changed-package scoping: the diff adds the violation without touching the check's package, and it surfaces only
  in the periodic full gate as a red trunk. Run every `structural_checks` entry and any class-firing test your
  project's gate config or role rules name, on the MERGED tree, regardless of which packages changed.

**Establish branch-attributable vs pre-existing from the full-race `-race`
result** — a regression adds failures the packages touched by the diff did not
have before. Do not classify a scoped change by replaying the whole known-red
suite.

🔴 **Do NOT run the project's full all-lanes gate for a merge.** The full suite —
every package across every lane, the integration lane, the UI lane, mutation and
reconciliation checks — is the **periodic full-gate cadence**, an agent run on the
dedicated isolation box, and it is its own skill: **`coordinator-full-gate`**. A merge never triggers it, and its merge-base
replay is not a per-merge step. Running it per merge is ~2h that on an already-red
trunk fails on the baseline every time. The RULING above
widens only the **race lane** to full-sharded per merge — it does not pull the
other lanes (integration, UI, mutation-check) into the per-merge path.

🔴 **Never kill a test run to stop a collision.** Killing skips Go's cleanup, which
leaks fixed-name tmux fixtures onto the shared socket and breaks that suite box-
wide. Let it finish, tell the other runner its results are contaminated, re-run
after.

## 5. GATE THE MERGED TREE, NOT THE BRANCH

A clean pre-merge build does not prove the merged result compiles or passes.
**Merge locally, then build and test, then push — guarded on the merge's exit
status, never on having reached the line.**

🔴 **A `//go:embed`-ed ASSET IS A TEST SURFACE. Run the embedding package's suite
on the merged tree even when the diff contains ZERO lines of Go.** "Docs-only" is
not a risk category; "compiled into the binary" is. Both static gates are blind to
this by construction — only execution sees it.

**Ask "did anything under an embed path change", never "did any `.go` change".
Carry the command, never the list:**

```bash
git grep -l -E '^//go:embed' <sha> -- '*.go'   # anchored ^ — unanchored pulls in prose
```

The role templates are not the risky entry — **skill files, references and
strategy docs are compiled in too**, so every skill edit and strategy-doc edit is
a code change, and those are exactly the diffs routed as low-risk `docs:`.

⚠️ **"Comment-only" is not a safe carve-out in Go.** `//go:embed`, `//go:build`
and `//nolint` are comments with semantics. A diff with zero non-comment changed
lines can still change what is compiled in. Assert zero changed lines matching
`//(go:|nolint|\+build)`, **with a control proving the key can fire.**

**Redirect test output to a FILE and read the file. Never pipe a test through
`tail`** — `$?` after a pipeline is `tail`'s status, so a FAILED run reports
success, and the dropped lines include the goroutine dump that separates a
deadlock from an assertion failure.

**When a suite is red, establish pre-existing vs introduced by running the same
suite at the merge-base** in a throwaway detached worktree — check the
discriminator, don't assume from the platform: `[ -L /tmp ]`. macOS (symlink)
needs `/private/tmp`; Linux (real dir) uses `/tmp` (`/private/tmp` may not
exist there and must not be created) — and **compare failing sets BY NAME, not
by count.** Sets differing in both directions indicate flakiness; a regression
adds failures without removing any.

## 6. RE-DERIVE ANCESTRY IN THE SAME TURN AS THE MERGE

**An ancestry check from ten minutes ago is not a check.** Trunk moves. Bind the
re-derivation to the irreversible ACT, not to a ceremony earlier in the sequence.

Resolve trunk through its **remote-tracking ref**, and prefer two instruments
agreeing (`rev-parse origin/<branch>` and `ls-remote`). **Assert the branch TIP**
— ancestry proves a merge EXISTS, never WHAT landed.

## 7. AFTER THE MERGE — four things, none optional

1. **The gate-log line.** The runner appends ONE line (date, gate, candidate SHA, target
   SHA, verdict, one short reason) to the project's verdict log (`verdict_log` in `.thrum/gate-config.json`) and commits it. That line is
   the only record a gate keeps: never commit per-gate report directories, logs, archives
   or evidence, and delete the gate's output once you confirm the candidate landed or was
   rejected (owner ruling 2026-10-17). The line must be able to carry a `CLEAN-WITH-GATE-FIXES`
   outcome, and when one applies it cites the `GATE-AUTHORED` commit SHA.
2. **One record only.** The only post-verdict record is the one line in
   the project verdict log (`verdict_log` in `.thrum/gate-config.json`) (gate output is deleted after the verdict).
3. **Commit accumulated agent state** under `.thrum/agents/` along with the merge.
   Uncommitted agent state exists in exactly one working tree, and it IS the
   agent's memory across restarts. **Never `git add -f`.**
4. **Delete the merged branch AND drop its queue bundle — one ritual, at merge time**, after the push is verified.
   `feature/*` and `fix/*` are one-shot — delete freely. **`agent/*`, `salvage/*`, the documentation deployment branch
   and `release/*` are ongoing or archival — do NOT delete.** Then, in the same turn: `thrum queue done <bundle>` +
   `thrum queue drop <bundle>` for the bundle that tracked this branch, and `bd close <id>` any beads this merge closed.
   A merge is not complete until the branch ref AND its queue bundle are both gone — the same act that lands the code
   retires its tracking.

## 7a. BEFORE YOU ACCEPT A VERDICT — CONFIRM THE RUNNER TORE ITS OWN THINGS DOWN

A gate leaves behind worktrees, agents AND tmux sessions. The worktree half is
covered in the runner's preamble; the agent/session half needs the same check.

**Ask for it in the verdict, and verify it yourself — it is one command:**

```bash
thrum tmux status | grep -E '^\s*g[0-9]+'    # gate sessions, agentless ones included
```

🔴 **`thrum team` CANNOT SEE an agentless session.** Five of
those nine had no registered agent, so a registry-based enumeration returns a
confident answer that omits most of the population. **Enumerate sessions, not
agents.**

🔴 **AND WATCH FOR `--force` IN THE TEARDOWN REPORT. `git worktree remove` REFUSES at rc=128 on untracked files — THE
REFUSAL IS THE PROTECTION, NOT THE ENUMERATION.** A clean enumeration therefore *invites* the flag that removes it.
**Any `--force` must arrive as an OVERRIDE with a justification, never as a pass**, and a clean guard result is not a
justification.

**A verdict is not complete until its runtime is gone.** Accept the finding, then
ask: which worktrees, which agents, which sessions, and what does the count read
now. **Never run `thrum agent cleanup --force`** to tidy up — its "orphans"
include live agents fleet-wide.

## 8. MERGED != INSTALLED != RUNNING

Three facts; only the third is behaviour. A merged fix to any `//go:embed`-ed
template or skill is **dead until a binary carrying it runs**, and the running
binary may rewrite generated files from its own stale embedded copy meanwhile.
**A generated file is never admissible evidence of what is merged.**

Say which of the three you verified. "Deployed" that silently covers all three
hides staleness.

## 9. Red flags — STOP

- Walking the merge-gate lenses yourself when a gate-role agent exists.
- Treating dual review as the gate.
- Carrying a prior verdict onto a new SHA.
- A gate-log line that contradicts its own report body.
- Reading `--is-ancestor <merge-base> <tip>` as a check.
- A zero from a trigger-dir query, accepted without a control.
- `go test … | tail`, or `$?` read after any pipe.
- Pushing without guarding on the merge's exit status.
- Declaring a class closed on a count you did not re-derive.
- Deleting `agent/*`, `salvage/*`, the documentation deployment branch or `release/*`.
- Pushing a merge without dropping the queue bundle that tracked it.

## See also

- `coordinator-hotpath-merge-gate` · `coordinator-philosophy-merge-gate` — the lenses
- `coordinator-running-review-cycles` — the dual-review cycle feeding §1
- `coordinator-branch-split-on-block` — when a gate blocks one concern of a bundled branch
- the project verdict log (`verdict_log` in `.thrum/gate-config.json`) — the one-line-per-gate record
- `.thrum/hotpath-gate.json` · `.thrum/philosophy.md` — the configs; read these, not prose

## Project-specific rules (already loaded)

Load the /thrum:project-rules-protocol skill and follow it.

If you accumulate a new rule mid-session (the user corrects you), capture it via
the Memory section of your role preamble — it references the
`thrum-memory` skill for the canonical `thrum memory create` shape.
