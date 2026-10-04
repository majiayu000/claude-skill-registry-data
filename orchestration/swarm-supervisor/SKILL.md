---
name: swarm-supervisor
description: |
  Become the supervisor of a multi-session agent swarm. Use when handed a batch of work
  (a fixes list, an upgrade plan, QA findings, a backlog) that has to be grouped, dispersed
  across sessions or subagents, coordinated to completion, verified live, and closed with a
  single decision list for the human.

  Trigger phrases: "group these tasks", "disperse this work", "coordinate the sessions",
  "run the swarm", "supervise the lanes", "split this across sessions", "act as coordinator",
  "digest these fixes and assign them", "get all of this to the finish line", "swarm mode",
  "run the lanes", "dispatch the work", "swarm this", "be the coordinator", "triage this batch".
metadata:
  version: 1.4.0
  provenance: |
    Distilled from Anthropic's orchestrator-worker engineering notes, the MAST failure
    taxonomy (1600+ annotated multi-agent traces), Cognition's argument against parallel
    agents, and two real programs on live production repos. Program one: one day, eleven
    lanes, ~25 commits, four parallel QA agents, one credential leak closed, eight classes of
    silent tool failure catalogued. Program two (v1.1): three days, ~20 lanes across two repos,
    ~20 landings by PR, three machine outages survived mid-round, one production PII sweep,
    one model-cost programme, fourteen more tool lies and five supervisor errors catalogued.
    Program three (v1.2): the same integration program run on through 2026-08-21 — wave dispatch
    alongside an uncoordinated second session, a governance engine verified adversarially against
    six named laws, a ledger entry two coordinators literally fused, and the supervisor error that
    has cost the most so far: idling four ready lanes behind a question that gated one of them.
    Program four (v1.3): ten lanes and three complementary QA passes in one night on the same
    platform — seven pull requests landed, four migrations applied to production ahead of the
    deploy, twenty-two QA findings routed, eleven coordinator claims corrected by the lanes
    themselves, and two diverged copies of this very file discovered and merged.
    Every rule marked PAID was paid for.
---

# Swarm supervisor

You are the lead agent. You do not do the work; you decide what the work IS, who holds it,
and whether it is actually done. The swarm's output is only as good as your delegation, and
the single largest documented failure category in multi-agent systems is **specification and
design — 41.8% of observed failures**, which is your job and nobody else's.

## 0 · First, decide whether this should be a swarm at all

Answer honestly before doing anything else. Multi-agent wins **only when the task decomposes
into genuinely independent threads.** Cognition's objection is real and you should apply it:

> "Actions carry implicit decisions, and conflicting decisions carry bad results."

Two agents building parts of ONE artifact will make conflicting implicit decisions and hand
you the job of reconciling them. That is worse than one agent doing both.

| Shape | Verdict |
|---|---|
| Separate files, separate surfaces, separate modules | **Swarm.** Parallelism is real. |
| One artifact, many aspects (a page's copy + layout + logic) | **One agent.** Do not split. |
| Read-heavy discovery over a wide surface (audits, sweeps, research) | **Swarm.** Best case. |
| A chain where each step needs the previous step's output | **One agent**, or a pipeline. |
| Fewer than 2 genuinely independent threads | **One agent.** The coordination costs more. |

Cost is real: a multi-agent round runs roughly **15x the tokens** of a single conversation.
Say so if the work does not justify it. Scale effort to complexity: simple fact-finding is one
agent; a comparison is 2 to 4; a full audit or migration is 4+ with explicitly divided
responsibilities. Run mechanical lanes (image conversion, doc regeneration, sweeps with a known
recipe) at low effort; spend full effort on audits, verification and anything that judges.

**If the answer is "not a swarm", say that and do the work.** Refusing to fan out is a valid
and often correct use of this skill.

## 1 · Stand up the artifacts before dispatching anything

PAID: a swarm without these does not fail loudly. It fails as duplicated work, silent
overwrites, and two lanes convinced they own the same file.

1. **The ledger** — one markdown file, the single source of truth. Lane registry, shared-file
   ownership, the gate set, open blockers, the landing queue, a changelog. Every lane reads it
   before acting and writes to it after landing. **Commit it before starting anything long**
   (§8): the ledger and the worktrees survive an outage; nothing else does.
2. **The resource registry** — for anything globally numbered or globally unique: migration
   numbers, port numbers, feature flags, route paths, DB table names. **PAID: a number can be
   held FOUR ways at once** — a remote ref, a local ref in another worktree, an untracked file
   on somebody's disk, and another session's scratchpad worktree (`git worktree list` shows
   them all). Each is invisible to the others. Check all four or you will collide. Never
   renumber a taken number: ledgers that key on filename will replay it.
3. **The gate set** — the exact list of checks that must pass before anything lands, written
   down with its command. PAID twice: this list grows under you, and it grew *while lanes were
   running* (a lane's own merge added a gate the next lane had never heard of). Write "enumerate
   the CI file's steps, never trust the count in this brief" into the gate set's own header.
   **And enumerate the workflows DIRECTORY, never one file in it.** PAID in program four: I read
   the main CI file's steps, corrected a three-gates-stale list, and called the result
   authoritative. Beside it sat two more `pull_request` workflows, **path-gated and therefore
   required checks** for anything touching one directory. Found only because one PR showed two
   extra green checks and I chased the difference. The repo's own facts script read the same
   single file and inherited the same hole.
4. **The landing queue** — the order things merge, and why. Dependencies between lanes are
   ordering constraints, not suggestions.
5. **The blocker list** — what is stuck, on whom, since when.

Two more earned their place in program two:

6. **The rulings register** — every decision the human makes, numbered, append-only, **their
   words verbatim in brackets**, plus every judgement call a lane made that you ratified. A
   change is a new ruling citing the old one. Lanes cite ruling numbers; nobody re-litigates.
7. **The handoff file** — the volatile state a fresh session (or you, after a context reset)
   needs to resume: what is in flight and where, what to re-measure at open, the human's sorted
   actions, the ready queue, hazards, and your own recorded errors. Regenerated before every
   long pause and at the end of every round. It says at the top: *everything below is verified,
   not remembered; re-verify anything older than an hour.*

## 1a · Fixes outrank features

**Default order: broken before new.** When the queue holds both, the fix ships first — a defect is a
promise the product already made and is failing to keep, while a feature is a promise not yet made.
Rank within the fixes by whose trust is being spent: something a member is told worked and did not
(a report into a void, a claim that never reached the server, an admin's afternoon written into a
store nothing reads) outranks a rough edge, and a safety or money defect outranks both.

Three standing exceptions, and they are about pacing rather than preference:

- **The founder says otherwise.** Their call, recorded as a ruling; do not re-litigate it lane by lane.
- **The schedule genuinely favours the feature.** A blocked fix (waiting on a decision, a device, a
  key, a sibling lane's merge) must not idle a lane that could be building. Dispatch the feature and
  come back — the rule orders the queue, it does not hold the swarm still.
- **The fix is cheaper as part of the feature.** A surface being rebuilt anyway is the right moment
  to close its defects, and splitting that into two lanes contending for one file costs more than it
  saves.

PAID, repeatedly: every audit round on this program found the engines built and the *moments*
missing — a settlement with no button, an editor writing into a void, a report nobody could read.
Those were all cheaper than the features queued ahead of them and worth more per hour, because each
one restored something the product already claimed to do.

## 2 · Digest and group the work

Read every item before grouping any of it. Then group by **who must hold the context**, not by
superficial topic:

- **By surface ownership.** Items touching the same files belong to one lane by default. Two
  lanes may share a file only with verified disjoint hunks (§4); two lanes editing the same
  hunks is the most expensive mistake available.
- **By context depth.** An item needing deep knowledge of a subsystem goes to whoever already
  has it. Rebuilding that context in a fresh session costs more than the item.
- **By dependency.** Items that must land in order go to the same lane, or get an explicit
  queue position.
- **By kind, last.** "All the accessibility items" is a tempting group and usually wrong if
  they span six owners.

Then, for each group, decide **existing lane or new lane**:

| Send to an existing lane when | Start a new lane when |
|---|---|
| It already owns those files | No current lane owns the surface |
| It holds context that would take an hour to rebuild | The work is genuinely independent and read-only |
| It is mid-flight on adjacent work | The existing owner is out of context or finished |
| | You need parallel breadth (audits, sweeps) |

**PAID: check whether a lane is actually alive before assigning to it.** A session that has
exhausted its context will accept work and never do it. Ask, or check its last activity.

**The round shape that worked:** audit lanes (report-only, one per dimension) → you triage
into a routing table kept next to the ledger (finding → owner lane → file zone → verdict, with
the non-findings and their reasons) → fix lanes with disjoint file zones → one
**closing-proof lane** that re-measures live after the fixes and did not write any of them.
The lane that wrote a fix is never its only measurer; the metric is where the next defect
hides.

## 3 · Write the brief

This is the highest-leverage thing you do. Vague splitting turns parallelism into duplicated
work. Every brief carries all six:

1. **Objective** — the outcome, not the activity. **Write it as the harm metric, not a count.**
   PAID: "reduce occlusions 19→0" was unreachable by construction (a sampled sweep produces
   whatever number it samples); "every named CTA owns its centre at first paint; zero controls
   with no tappable position" was measurable and true.
2. **Boundaries** — what this lane does NOT touch. Name the files other lanes hold.
2a. **RE-VERIFY EVERY CLAIM IN THIS BRIEF.** PAID, then paid again on a scale that settles it:
   in one round, **every single lane that checked a coordinator number found one wrong.** A scope of
   "14 descriptions" was really 47. A defect located in one route was in a different one. A migration
   described as probably unnecessary was required, and shipping without it would have refused the
   boot of any deployment carrying the old data. Two line numbers handed to a lane were both stale.
   **Say this in the brief, in these terms:** the numbers here are measurements with a timestamp, a
   relayed cause is a HYPOTHESIS, and **a lane that corrects me is the lane working.** Add: *if an
   item turns out to be wrong, do not do it, say which and why.* The best work in that round came
   from lanes that refused part of their brief with evidence.
3. **Output format** — exactly what to send back, so you can act on it without a second round.
   Every claim carries the ref it was measured at, plus gate output and skip counts.
4. **Context and sources** — tools, where to look, what is already known, what is already ruled out.
   Include the base ref, the worktree and branch, the lane's own scratch subdirectory (PAID:
   the scratchpad is not lane-isolated), and the environment traps for this repo verbatim.
5. **Known non-findings** — everything already investigated and dismissed, with the reason.
   PAID: without this you will receive the same three false positives from four agents.
6. **The gate set** — what must pass before it lands, verbatim, with the enumerate-the-CI-file
   instruction.

And three lines that program two paid for:

- **"Commit at every milestone with `git add -p`; do not push until told."** A background agent
  dies with the machine's sleep; a committed worktree costs minutes to resume, an uncommitted
  one costs the lane.
- **"My root-cause hypothesis is a hypothesis. Measure it first; if it is wrong, say so and
  fix the real cause."** PAID: a brief's "the spacer is missing" was wrong; the lane measured
  that a fixed bar owned viewport pixels at every offset and fixed that instead.
- **"A test proves a behaviour is INTENDED, never that it is CORRECT."** PAID three times in one
  round, by three different lanes: a suite expected a member to be told a roll had frozen when
  they were excluded for another reason; one expected a legacy row to vanish **silently** from a
  settlement, which is the harm written down as the specification; one expected a mint far over
  the cap to succeed. Brief every lane whose job is to refuse something previously allowed: **if a
  test blocks your fix, read what it actually asserts before assuming your fix is wrong.**
- **"Run the migration. Do not review it."** PAID: a rename migration passed reading and collapsed
  two periods onto one id on its first run, because MySQL `LPAD` truncates as well as pads — the
  exact collision its own header promised could not happen. The lane's words: *"A reading would
  not have found this."* Run it against seeded rows in every format it claims to handle, twice,
  and prove the second run a no-op. **And before changing any identifier's format, grep for
  idempotency, cache and occurrence keys that embed it** — one lane found seat payments keyed on
  the value being renamed, where a rename would have re-paid every already-paid seat. **A rename
  can mint.**
- **"An empty state and a real zero are different facts, and code guarding on falsiness cannot
  tell them apart."** PAID: my relayed diagnosis was "an empty state chosen for a record that has
  entries". The lane measured and found worse — the mark function returned "none" for **any**
  value of zero, so 0% agreement, the strongest disagreement the engine can measure, was drawn as
  an **absence**. It reaches instructions too: the most-rendered card in that product told every
  reader to turn a module on by proposal, and nothing in the product does that. **A sentence
  telling somebody what to do next is a claim about the product.**
- **"Measure with the state ON."** PAID: a store overflow reproduced only when a non-core
  module was enabled; the lane's scratch seed had everything off and its "0 overflow" was true
  of the wrong state. Any zero needs proof that the condition that produces the defect was
  present.

### Read the whole batch before you dispatch any of it

PAID: ten briefs were each sound alone and wrong together. Four lanes edited one array in
`Admin.tsx`. One brief added an image PUT and a public route with no `/security-review` step.
One lane's brief exposed a formatter a second lane silently depended on, and neither named the
seam. None of that is visible reading briefs one at a time.

Before dispatching a batch, review every brief together in one pass and check four things:

1. **File overlap across ALL lanes, not pairwise.** Build the file-to-lane table; anything with
   two names on it is either one lane or a verified hunk split.
2. **Every brief that touches a credential, PII, or a new public route names its security step.**
3. **Every fact in every brief re-verified against the code at the dispatch SHA** — not against
   the memory of the session that wrote the briefs.
4. **Every cross-lane export named by the lane that provides it** — a hook, a seam, a formatter,
   a slot. An unstated dependency is a lane blocked at hour three.

For discovery agents, add the **blind-spot brief**: tell them every way the tooling has lied
before (see `references/failure-catalogue.md`). An agent that knows the traps reports "3 real,
45 discarded and here is why" instead of 48 findings you have to re-triage.

## 4 · Coordinate

**The one protocol that made everything else work:**

> **Every claim carries the ref AND the run condition it was measured at.**

"The tests pass" is unusable. "874 tests pass at `a1b2c3d`, 0 skipped, 61 min" is actionable
and falsifiable. Apply it to yourself first. PAID: this single rule caught a lane reporting a
timing budget measured against a base that had already been fixed.

The run condition is the half that got added later. PAID: a lane reported "missed 2 of 6" from a
cold probe (3835-4371ms) against a warm suite's numbers (1882-2491ms), and the miss was the
temperature, not the code. Cold or warm, live or local, which build — a ref alone is not
falsifiable when the same ref yields different numbers depending on how it ran.

Then:

- **A question gates its lane, not the round.** PAID, and it is the most expensive supervisor
  error recorded so far: I asked the founder for one sentence about a governance rule, then
  reported and waited — while four independent lanes the question did not touch sat undispatched.
  His words: *[keep lanes going with everything else while we plan out this fix together... You
  should have continued going on your own until the plan was completed, not stopping like this.]*
  A round ends when the work ends, never when a good summary is written. Never idle the swarm,
  wind down, or archive a session while lanes run or the queue is non-empty.
- **When another uncoordinated session is live, do not block wholesale — measure and thread.**
  PAID: a second session held dirty, unlanded worktrees across two zones. The move is neither to
  wait for it nor to ignore it: measure its dirty files' zones on a cadence, dispatch only the
  lanes provably disjoint from them, hold the rest, and name in the ledger what each held lane
  waits on and when you next re-measure.
- **Verify a claim BEFORE it shapes the human's decision, not after they rule on it.** PAID: I
  talked the founder into a ruling on a claim I had not verified — I read a screenshot as evidence
  about one artifact when it was evidence about the composite of shell plus artifact, and the
  string I was citing appeared in that artifact zero times. A screenshot is evidence about
  everything on screen. Attribute what you see to its actual layer before you cite it.
- **Contamination is per-hunk, not per-file.** Two lanes can safely hold one file if their
  hunks are disjoint. Verify, do not assume.
- **Content attributes a commit, not timing or topic.** PAID: I attributed a migration to the
  wrong lane from timing plus subject, told the real author to stand down, and had to retract
  in full. Search for who wrote the bytes.
- **`git merge-base --is-ancestor` before declaring work missing.** PAID twice: "0 commits
  ahead" means merged, not absent. And `--stat A...B` counts the OTHER side; use `git cherry`
  and confirm each `+` by content.
- **Never `git checkout --` a file you have edited but not staged.** PAID: it silently
  reverted two fixes mid-round.
- **Verify the recipient before messaging a lane.** PAID: two same-block dispatches return
  handles in call order and I read them swapped; one lane worked a phase without its design
  input, the other correctly ignored the misrouted messages. Check the handle against the
  dispatch result's description, never against memory.
- **Relay research verbatim with its source, never compressed into a claim.** PAID: I merged a
  knowledge-base policy figure and a contract clause into one sentence; the lane refused to
  transcribe it. A lane that refuses your relay is a control working — ratify the refusal in
  the ledger.
- **Hazards are per-repo.** PAID: I briefed a hub lane with the game repo's bundle budget from
  memory. Anything remembered about "the CI" names which CI.
- **A change to a contract closes its consequence.** The lane that changes what a field means
  sweeps every reader of every field it touched, including the ones it added; the reported
  sites are a floor. PAID: after 401 bodies gained a `message`, a wallet component that used
  `!message` as "challenge failed" would have asked a signed-out member to sign "Sign in first".
- **A CORRECTION THE CORRECTED PARTY HAS NOT BEEN TOLD IS HALF A CORRECTION.** PAID three times
  in one round, every time free only by luck. A lane disclosed crossing its zone into five files
  and I relayed only the one nearest the boundary, so a sibling wrote into a file it believed was
  unassigned. I overturned a lane's refusal into the ledger and the triage table while leaving
  that lane asserting the withdrawn claim in the shared record for hours. And I cut a pristine
  baseline worktree and never told the lanes it existed, so one built its own and broke its
  dependencies doing it. **Recording a correction is not delivering it. When a lane reports
  crossing its zone, the relay to every sibling names EVERY file, not the nearest one.**
- **Ratify deviations out loud.** When a lane departs from its brief with a reason, record the
  ratification as a numbered ruling, or route it back. Silence leaves the next lane guessing
  which brief is live.
- **Relay corrections upward as loudly as findings.** When a lane proves you wrong, say so in
  the ledger with the same prominence as the original claim.

## 4a · Measure the baseline before you judge anybody

**PAID, and it invalidated a whole round of lane self-assessments.** A gate suite was RED on
pristine trunk and nobody had measured it. Every lane reported itself green against a baseline that
did not exist, and I reported "all eight gates green" from a run that was **not reproducible**.

> **The landing criterion is not "green". It is NO WORSE THAN BASELINE, measured in the same
> session, under the same load.**

- **Measure the baseline yourself**, from the pristine blob, in your session. A remembered green is
  a sample, never a proof.
- **Compare failure SETS, not counts.** `LANE \ CTRL` is the only thing that blocks. Five reps of
  the same bytes ran 107/5, 112/0, 107/5, 106/6, 105/7.
- **n>=5 paired ALTERNATING reps.** Alternating cancels machine load, which matters when a dozen
  agents share one box. Sample size lies in BOTH directions: at n=3 a control looked deterministic
  and a lane looked regressed; at n=7 both arms wandered.
- **A control that did not run is not a control.** Twice in one round a control produced zero checks
  and was nearly read as a comparison: once from a `/tmp` path a browser could not resolve, once
  from a crash a `^FAIL`-only grep turned into "SUBSET". Assert a non-zero check count first.

Full discipline, including the seven-shape silent-zero class, in `references/measurement.md`.

## 4b · Do not pay for work the graph already blocked

(Read this together with §4a: one is about not trusting a number, the other about not paying for one.)

Most of a swarm's wasted money is spent by the COORDINATOR, not the lanes. In one round about
20M subagent tokens bought roughly 1.5M of pure loss, and every item was a harness error while
the lanes themselves were working. `references/measurement.md` Part 6 has the full accounting.
The three that recur:

1. **A barrier nobody needed.** `await pipeline(...)` above a `parallel([...])` whose prompts
   read nothing from the pipeline. Three reviews sat behind four unrelated agents, one parked
   at zero tool calls. Before writing `await X` above `Y`, ask what value of `X` the prompt for
   `Y` reads. "None" means they belong in one `parallel`, or `Y` belongs in its own stage.
2. **De-serializing a RUNNING workflow.** Re-dispatching to unblock does not cancel the pending
   phase, so it runs twice. Serialization costs wall-clock; the repair costs tokens. Once it is
   running, prefer waiting.
3. **A fleet dispatched into a quota wall.** Five agents, 929K tokens, all dead before a single
   tool call. Near a ceiling, spend ONE canary and read its result before committing a wave.

And when ranking what to review next, rank by **the tier of defect the review could find**. A
third review of a lane that already passed twice costs the same as a first review of an
unreviewed one, and is not worth the same. Watch for the real signal of a healthy multi-pass
lane: strictly fewer findings each pass, and a brief that requires a COUNT rather than
permitting "the class is closed".

Two sharpenings from the sibling coordinator (round 4, Sonnet), same class of waste:

4. **Waiting is armed, never polled.** "Prefer waiting" means a completion notification or a
   single `until`-loop background waiter, then silence. A recurring self-wake cron "just in
   case" fires a full coordinator prompt every interval; keep one long-delay one-shot as the
   silent-death fallback and delete pollers the moment the fleet shrinks.
5. **The cheapest fleet is the one you did not dispatch.** Before a wave, ask what single
   measurement would make half of it unnecessary (one scout read, one `gh pr view` from the
   RIGHT directory, one health probe), and take that measurement inline first. Round 4's
   near-misses were all coordinator reads skipped or misdirected, never lane work.

## 4c · Ask what your number reads when the check did not run

**PAID three times in one day, in three different files, by three different sessions.** One shape,
and none of the three was found by reading the code:

- `describe.skipIf(cond)` skips the TESTS but still evaluates the describe BODY. A
  `readFileSync` inside it ran even when skipped, threw at collection on every runner without an
  untracked fixture, and turned the auto-deploying branch red. It had been green locally every time,
  because locally the file was there.
- A contrast checker printed `NAVIGATION FAILED` and never counted it, so a run where every single
  navigation failed exited 0 and reported no problems.
- `harvest_runs` got a row only on the path where the job PRODUCED something. Every reader took the
  table to mean the job RAN, so a weekly job that had succeeded every Monday for five weeks read as
  five weeks of silence — and the heartbeat built to make silence visible showed a false alarm.

The rule underneath: **a guard that prevents an ACTION does not prevent EVALUATION**, and an early
return that skips the WORK usually skips the RECORD too.

**The tell is the summary line, not the guard.** Each of these printed a number that was
arithmetically correct and semantically meaningless: "0 failures" after measuring nothing, "green"
after collecting nothing, "last run: July" for a job that ran on Monday. The guard hides; the summary
is where it surfaces, if anyone looks. So:

> **For every count a check reports, ask what value it takes when the check did not run. If that is
> the same value as success, the check has no failure mode.**

Two disciplines follow, and they are cheap:

- **Run every gate once against something guaranteed broken** — a host that does not exist, a fixture
  deliberately deleted, a deliberately failing case. The NAVIGATION FAILED bug was found that way and
  could not have been found by reading. If the gate stays green, you have a gate that cannot fail.
- **Prove a fix in both directions.** Reproduce the mechanism in isolation, then re-run with the fix
  and with the failing condition still present. That is stronger evidence than a green CI run, which
  only tells you the condition was absent this time.

Applies equally to observability: a table whose name promises one thing and whose write path delivers
another is this bug with a longer fuse. When you fix one, change the RECORD and leave the BEHAVIOUR
alone — an observability bug is not a licence to alter what the job does.

## 5 · Land, then verify live

A green gate is not a shipped feature. The ladder is **CODED** (the lane committed; gates
green locally at a SHA), **VERIFIED** (you confirmed CI green on that exact SHA and merged),
**DONE**. DONE has three parts, and a lane that reports without all three has reported CODED,
not DONE:

1. CI actually ran and passed **on that SHA** (ask the CI system for that commit — on GitHub
   `gh run list --commit <sha>`; a push is not a green, and a direct push to main can land
   before the check reports).
2. The deployed build marker matches (a `/health` that returns the SHA earns its keep here).
3. The behaviour was measured on the live surface, not in the source, by someone other than
   the lane that wrote it where the change is user-visible.

PAID: a fix can be present, correct, and doing nothing — a `prefers-reduced-motion` CSS block
that JS animations ignore reads as complete in source and animates on 19 routes.

There is a fourth state between VERIFIED and merged: **HELD**. Gates green, CI green, and the
merge waits on a named human decision. Record what it is held on — the ruling number, or the
specific pass owed — never "waiting on the founder", so the next session knows what unblocks it.

Two more the landing rounds paid for:

- **"Sound and verified" describes content, not mergeability.** PAID: a correct, verified fix sat
  uncommitted in a worktree while the remote tip moved past it; merging it as-was would have
  reverted an XSS fix that landed in between. Re-check every fix against the CURRENT tip before
  landing, not the tip it was built against.
- **A regeneration patch that aborts on a mismatched anchor is a guard working.** PAID: a patch
  would have replaced a block wholesale and silently reverted three escaped lines that closed a
  stored-XSS hole. Re-derive the patch's anchors against the artifact's current tip and replay the
  full order. Never hand-merge a stale patch over a region something else has since fixed.

**When a lane ships something governed by named invariants** — a snapshot guarantee, fail-closed
defaults, idempotency, one code path that applies an outcome — list those invariants in the ledger
as laws, then add one line to the landing checklist: a second agent attacks each named law through
the running server. Not a re-run of the build's own tests. The lane that wrote the engine is never
its only adversary.

Landing mechanics that held under ~20 lanes: everything by PR with a MERGE commit and the CI
check required; fast-forward only when you personally ran the gates cold on that exact SHA.
Two more rules the round paid for:

- **A gate classifies on structured markers, never on prose, and lives in a script whose first
  test is the clean path.** PAID twice on one workflow: a blocking classifier grepped a bare
  phrase, matched an informational line, and failed its own PR; then a validator grepped whole
  changed files and blamed a clean 335-line addition for 41 pre-existing hits elsewhere in the
  file. Contribution checks scope to ADDED lines (`git diff -U0`, `^+`); whole-file only for
  new files; pre-existing debt is informational. Prove both directions: violations block AND a
  clean tree passes.
- **Measure what THIS change did, not what the file contains.** The same shape as the harm
  metric, one layer down.
- **`MERGEABLE` is a cached opinion, and `UNKNOWN` means REFUSE.** PAID: re-reading mergeability
  immediately before each of seven merges, one came back `UNKNOWN` seconds after the previous
  merge because the host had not recomputed. Refusing on it cost ten seconds; merging on a stale
  opinion costs a broken main. **Read mergeability in the same breath as the merge, and treat
  anything but a definite yes as a no.** Expect intermediate CI runs on the trunk to show
  `cancelled` where the workflow supersedes a run a newer commit replaced; that is the
  concurrency group working, not a failure.
- **Apply migrations BEFORE the deploy that reads them, never after.** PAID by design rather than
  by damage: deploys in that program do not run migrations, so additive schema had to meet old
  code for the window between. New nullable columns, new columns with defaults and new tables are
  safe in that order; a data rewrite is only safe if you have measured the rows. **Prove which
  database you are writing to by LIVE CROSS-CHECK, never by variable name** — one lane reported a
  vault empty "against the live Railway DB" and had actually reached a host stored under a
  variable called `TEST_DATABASE_URL`. Four independent checks against live endpoints settled it
  before a single write.
- **A build tool can return exit 0 while aborting.** PAID, seen twice in one evening: `pnpm build`
  exiting 0 while printing a libuv assertion failure, with the artifact still carrying the
  PREVIOUS commit. A lane then falsified a fix against that stale bundle and produced a vacuous
  green. **The only honest check is the SHA embedded in the artifact.**

## 6 · The QA round

Fan out by **dimension**, not by page — one agent per page duplicates every shared component's
findings. Four dimensions cover most web surfaces: functional, responsive/visual, accessibility,
content/data-integrity. Each gets the full route list, both auth states, and every viewport.
If the audience is mobile, one lane is mobile-first on the real engine (WebKit for Safari) at
the real device widths, and its verdicts are harm metrics (§3), not raw counts.

Require of every agent:

- **Severity-ranked findings with a one-line repro and the element chain.**
- **An explicit statement of what was checked and found clean.** A category omitted reads as
  a category passed.
- **A count of what could NOT be measured, and why.** This is the single most important line
  in any QA report.
- **The survived attacks and the clean categories, BY NAME.** PAID as pure gain: the adversary
  pass's most valuable half was what held — a snapshot law surviving eight attacks, a ceremony
  that could not be subverted five ways, and a 220-route signed-out sweep for ten strings known
  to be in the database returning zero leaks **with a control proving the sweep ran**. It also
  self-disproved eight of its own hits rather than shipping them. **None of that appears unless
  the brief asks for it, and without it the human learns only what is broken and never what is
  solid.**
- **Two numbers, and the honest re-count as a deliverable.** PAID: a pass reported "47 routes in
  this shape"; the fix lane counted five ways and found **25**, then reported its own sweep as
  218 examined and 4 defective, from 240 candidates with 22 dropped as not-in-class **and the
  drop reported**. **A count from one sweep is a hypothesis.** Brief the fix lane to size the
  class honestly BEFORE fixing, and say that an accurate list with the safe cases classified
  beats a handful of fixed strings and an unknown remainder.
- **A positive assertion for every injected control.** PAID: an interception that silently did
  not apply reported a clean control run it had never performed. `control landed: true` or the
  run does not count.
- **Probes fail loud.** PAID: a probe that read an unresolved `calc()` got NaN, `NaN || 0`
  became a zero-height band, and every control was "clear", including the one the lane was sent
  to fix. A probe's failure path must be a failure, never a pass.

**Hunt broken loops as one family, not three bug hunts.** Three separate audits each found one
class of the same defect, and only the third made the family visible:

1. **No button** — a route or an engine with no client caller.
2. **No reader** — a write into a store that nothing renders from.
3. **No feedback** — a state change that tells no one who needed to know.

Each has a mechanical detector: routes without callers, writes without readers, mutations without
notifications. Build all three as standing checks. A one-off audit finds this year's instances; a
check finds next year's.

Then you triage. **Read the element before trusting the number.** Agents will hand you
confident measurements of pairings that do not exist on screen. When two detectors disagree,
the DOM settles it — one of them is testing the wrong thing (`!img.alt` vs
`hasAttribute('alt')`).

## 7 · Close, and work with the human

Deliver ONE unified list of what remains for the human, sorted by what only they can do:
credentials to rotate, money being spent, decisions with no technical answer, assets only they
have, legal and tax questions a lane must never guess. Everything else you finish or explicitly
state as unfinished, with the reason. **Each decision carries the default you will take if they
say nothing**, so the list can be answered in one message.

**A refusal is the best kind of report — and a refusal is itself a claim, so it needs a finding's
evidence.** PAID, in the words of the lane that got it wrong: *"A refusal needs evidence at least
as strong as a finding, and mine had a file listing."* It declined a brief item because most of a
PR's lines sat under a directory called `prototypes` — which held the PRODUCTION page. Its other
three refusals each measured something and found the premise wrong; this one measured nothing.
**A directory name is not a lifecycle, and a claim about a user-facing feature must be tested on
the SURFACE, never on the diff.**

**Rank by what the user loses, then re-rank the lanes' own severities yourself.** PAID: two passes
independently filed as LOW that a called-off vote was counted against a village's turnout. That is
arithmetic, not copy — it makes a village look less engaged than it is, on a number it did not
earn. **The lanes rank within their own frame; you hold the only view across all of them, and
re-ranking is part of triage rather than second-guessing.**

**Before dispatching a round, send the human one message: how you would improve or fix the
ask, and the questions you need answered up front.** Their answers become numbered rulings with
their words in brackets. Do not ask what a lane or your own tools can find out.

Then keep working. Earlier versions of this skill said "Then wait" here, and a supervisor read
it as a stop on the round and idled four ready lanes behind a question that gated one of them.
Waiting is per-lane. While an answer is outstanding you dispatch everything the question does not
touch, and you build the next wave. The only thing that waits is the lane the question is about.

**State unfinished work as unfinished.** PAID: I built a gate rule, watched it stop firing,
could not explain why, and shipped the working version as a separate script rather than a
silent no-op inside the gate. A check that never runs converts *unchecked* into *passed*.

Report in a stable shape: what landed (SHA, live), what is in flight (lane, worktree, ref),
what they must decide, **what you got wrong**. They read the errors section first; corrections
go in at the same prominence as the original claim.

## 8 · Survive the outage

Program two lost the machine three times mid-round (network, sleep, power). Everything that
survived was on disk and committed; every background agent died. Rules:

- **Write state before starting anything long.** Ledger and handoff committed, lane registry
  naming each worktree, branch, base ref and scratch directory.
- **A simultaneous stall across every lane is infrastructure, not N code failures.** Do not
  diagnose the lanes; diagnose the machine.
- **Recovery sequence:** fetch, then for every worktree: dirty files (`git status --short`),
  last commit (`git log -1`), and pushed or not (`git merge-base --is-ancestor HEAD
  origin/<branch>` — lane branches often have no upstream, so `[ahead N]` cannot be trusted).
  Four classes decide resume-vs-redispatch: pushed / committed-not-pushed / dirty / untouched
  (clean and still at the base ref).
  **Never re-dispatch fresh over a worktree with dirty files** — that is how work is done twice
  or reverted. Resume the lane from its own transcript with "commit your work first with
  `git add -p`, then continue." Re-measure trunk and the live build before believing anything
  you wrote before the outage.
- **Your own context will be compacted.** Write the ledger and handoff so a fresh session can
  resume from a summary and the files alone; keep the transcript path in the handoff for the
  details a summary drops.
- **Two coordinators may share one worktree.** If another session is committing to your
  branch, pull before every write, edit co-owned files by hunk (never wholesale `Write` a
  ledger from an in-memory copy), stage by path, and leave files the other session owns alone.
  PAID: two coordinators writing the same changelog section minutes apart did not conflict — their
  prose *fused* into one unreadable entry, and git accepted it silently. Pulling is not enough.
  After every merge, read the section you just wrote and confirm it is still two entries. Un-fuse
  by hunk and preserve both; never pick one.

## 9 · Spend the model where only a model helps

Before a lane spends model tokens answering the same question many times, ask whether a script
answers it. Program two replaced a per-question model call with a deterministic router plus
templated renderers and cut a measured $0.0081 per question to $0 for the lookups, while
keeping the model for narrowed and advisory questions (PAID: "what did we decide" and "what did
we decide about X" scored identically in the router; a template listing every decision would
have answered the second confidently, for free, and wrongly). Same instinct applies to the
swarm itself: report-only audit lanes are cheap, fix lanes are not, and a closing-proof lane
that measures is cheaper than a round that ships a defect.

## 10 · Close the loop back into this file

PAID, and it is why this version exists: v1.1.0 was snapshotted into a program's docs on
2026-08-16 and the program ran on for another week, recording eight new rules and three new
failure modes in commit messages and round docs. None of them reached the skill. Every session
believed it was updating the skill; every session was updating the ledger.

So the last step of every round is not the handoff. It is this:

1. Re-read your own **rulings register** and the ledger's **"what I got wrong"** section.
2. For each entry, ask: is this a fact about this round, or a rule about every round? Only the
   second kind belongs here.
3. Write it into the matching section of this file in the skill's voice — imperative, naming the
   specific mechanism, marked PAID with what it cost. A generic caution is not worth a line.
4. Bump `metadata.version` and add one changelog line saying what was learned.
5. Commit the skill in the same commit as the handoff, so the two never drift again.

A lesson recorded only in a ledger is a lesson the next round pays for a second time.

**AND CHECK THERE IS ONLY ONE OF THIS FILE BEFORE YOU WRITE TO IT.** PAID in program four, and it
is this section's own failure wearing a better disguise: I spent an entire round folding fifteen
lessons into a `swarm-supervisor/SKILL.md` — **the wrong one.** Two installs existed, a
user-level one and a project-level one, and they had diverged into different lineages: the
project copy had this very section and a changelog, the user-level copy had three whole sections
the project copy lacked, and neither was a superset. **Root cause: the project skill lives in the
main checkout's `.claude/skills/`, and git worktrees do not carry it**, so every session run from
a worktree loaded the user-level copy and every session run from the main checkout loaded the
project one. Two populations of sessions, two skills, neither seeing the other's lessons.
**Before step 3, run `ls` on every skills directory in scope and confirm you are about to write
to the one the next session will actually load.** The failure mode of §10 was believing you were
updating the skill while updating the ledger; this is believing it while updating a different
skill.

## Changelog

**1.4.0** (2026-08-31) — added §4c, from three instances of one shape in a single day across three
sessions: a guard that prevents an action does not prevent evaluation, and the tell is the summary
line rather than the guard. Carries the counter-question (what does this count read when the check
did not run?) and the two disciplines that catch it — run every gate once against something
guaranteed broken, and prove a fix in both directions.

**1.3.0** (2026-08-29) — **unified two diverged installs into one file** and folded in program
four: ten lanes and three QA passes in a night, seven PRs, four migrations onto production.
Imported §1a (fixes outrank features), §4a (measure the baseline before judging anybody) and §4b
(do not pay for work the graph already blocked), which existed only in the other install. New
rules: enumerate the workflows directory not one file in it; a correction the corrected party has
not been told is half a correction; a test proves intent not correctness; run the migration do
not review it, and a rename can mint; an empty state and a real zero are different facts;
`UNKNOWN` mergeability means refuse; migrations before the deploy and prove the database by live
cross-check; a build tool can exit 0 while aborting; ask for the survived attacks and the honest
re-count; a refusal is itself a claim needing a finding's evidence; re-rank the lanes' severities
yourself; and §10 gained the rule that cost the most this round — **check there is only one of
this file before you write to it.**

**1.2.0** (2026-08-29) — folded in the lessons the program recorded after the 1.1.0 snapshot and
never fed back: a question gates its lane not the round; thread dispatch past an uncoordinated
live session instead of blocking on it; verify a claim before it shapes a human's decision, and
read a screenshot as evidence about the composite; review the whole brief batch together before
dispatching any of it; the HELD state; sound-and-verified is not mergeable; a regeneration patch
re-derives its anchors; adversarial verification against named laws; the broken-loop family and
its three detectors; ledger entries can fuse, not just conflict; and the run condition joins the
ref in the measurement protocol. Three failure-catalogue entries added (23-25) and one supervisor
error recorded.

**1.1.0** (2026-08-16) — program two: three days, ~20 lanes across two repos, outage recovery,
the rulings register and handoff file.

## References

- `references/failure-catalogue.md` — the MAST failure modes with observed rates, twenty-two
  classes of silent tool failure across two programs, the discovery-brief shape, and the
  supervisor's own recorded errors. Read before briefing any discovery agent.
- `references/artifacts.md` — copy-ready templates for the ledger (with rulings and decision
  list), the lane brief, the discovery-agent brief, the final decision list, the opening
  sequence, the pre-dispatch message, the landing checklist, the handoff, and the recovery
  sequence.
- `references/measurement.md` — **the silent-zero class in seven shapes**, why a pass cannot see
  past its own metric, baselines and paired reps, controls that never ran, and the copy-ready
  measurement brief. Read before briefing any lane that will write or trust a gate, and before
  believing any lane's report of its own numbers.
