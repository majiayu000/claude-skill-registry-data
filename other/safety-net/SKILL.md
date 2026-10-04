---
name: safety-net
type: Skill
title: "safety-net — real tests written before a big change, proven to fail, run by a fresh agent after"
description: "Real tests around a big code change: written first, proven to fail on a planted break, run by a fresh agent in the live product before and after. Use when told to use safety-net, or before a change wide enough that one agent cannot see every way it breaks. NOT for one test (forcing-function-tests)."
tags: [testing, migration, verification, doctrine, adversarial]
timestamp: 2026-10-01T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/safety-net/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# safety-net

**Arman, 2026-10-01, verbatim:** *"I'm not talking about tests that run automatically or each time we
build… I'm talking about what I call REAL TESTS. The ones you run yourself right after big changes and
just confirm the results are what they need to be. Not automated, not blocking, not stuff like that.
They're blocking because if they fail, you stop and address it, not because some system blocks you…
one passing test means hundreds of things had to have worked perfectly."*

A **real test** is a playbook: a plain-language procedure that a fresh, cheap agent walks in the live
product against the live database as `admin@admin.com`, plus a **sealed check-sheet** that agent never sees. It is
written **before** the change, **proven to fail** on a break it was not told about, run on the
unchanged product, and run again after the change. Pass → ship. Fail → you stop and fix the product.

This is not a test suite, not CI, not a gate, not a dashboard. Nothing here runs on its own and
nothing here blocks anyone. The playbooks are documents, and the discipline is yours.

**Mechanics live elsewhere; this skill only orders them:**
| Need | Owner |
|---|---|
| Planting a break in a shared checkout and restoring it no matter what (`plant.py`) | `forcing-function-tests` §3, §4a |
| Finding every consumer and trigger path, including rows that are configuration | `safe-cutover` Step 1 |
| Briefs that can return what you do not already believe | reality-is-the-referee · `subagent-dispatch` §1 |
| Realistic data and people | test-data-looks-real · `@ai-matrx/records/use-cases` · persona factory |
| The database tests run on | the live database, as `admin@admin.com`, on disposable records (Arman, 2026-10-03). The nightly clone is only for rehearsing destructive migrations or jobs that lock live 10+ minutes (`operations/clone/CURRENT.md`) |

## 0. When, and how much

- **Fires** when the person says "use safety-net", and on your own judgment before a change wide
  enough that one agent cannot see every way it breaks: a shared primitive or package with many
  consumers, a cross-repo contract, a rewrite of a path many surfaces reach.
- **Does not fire** for a change inside one feature (`forcing-function-tests` is enough) or one
  replaced contract (`safe-cutover`).
- **Budget — this is where agents waste the owner's money, so it is a ceiling, not a target:**
  three to six playbooks in total; each one under fifteen minutes for the runner; one blind fault
  per playbook. Wide beats narrow: one playbook that crosses five channels is worth more than five
  that cross one each, because one pass then proves the whole chain.
- If the net takes longer to build and prove than the change takes to make, the change is too big
  for one net. Split the change.

## 1. Order is law, and the commits are the clock

1. **Weakness list** (§2) — written by a fresh agent from reality.
2. **Playbooks** (§3) — written by a different agent than step 1 when you can arrange it; at minimum,
   step 1's list reaches step 2 as a file, never as your summary.
3. **Baseline run** — a fresh runner (§4) walks every playbook on the **unchanged** product. All must
   PASS. One that does not means the playbook or the product is already broken; find out which
   before step 4. A product defect found here is fixed now, under its own commit.
4. **Fault proof** (§5) — one planted break per playbook, blind, fresh runner. Each must FAIL for
   the right reason.
5. **Commit the net** — playbooks and ledger, one commit, pushed. **This commit precedes every
   commit of the change.** No script checks this. Anyone who doubts the order reads the history,
   which cannot be rewritten on the shared remote.
6. **The change.**
7. **After-run** — a fresh runner walks every playbook through every trigger. All PASS → ship. Any
   FAIL → stop. Fix the product. Rerun the failed playbook and every playbook that shares the
   broken channel. **A playbook is never edited to make it pass.** It changes only when the intended
   behavior changed, and the ledger row says what changed and why.
8. **Keep the playbooks** (§6). They are the asset; the next change in this area starts from them.

The three cheats this order exists to stop, all observed in agents: writing the tests after the
change so they describe what was built instead of what must hold; one agent writing, running and
grading its own test; and a test that passes because nothing could make it fail.

## 2. The weakness list comes from reality

Everything downstream can only catch a weakness somebody listed. This step decides whether the net
is worth anything, so it is never written from memory of the code.

**Recipe — generalize channels, never copy a feature's list:**
- **Input channels:** what the user typed, attachments, page context, internal resources attached,
  variables, settings and knobs, which organization the person is acting in.
- **Output sinks:** database rows, the rendered page, the tool-call ledger, notifications, files.
- **Entry points:** every trigger that can perform the same job — chat, a context-menu shortcut, a
  surface binding, an agent-filled mandate, a schedule, an API call.

**Sources, each found by a command whose output can be shown:** every consumer and trigger path of
what the change touches, including stored definitions and configuration rows (`safe-cutover` Step 1
table) · the surfaces and routes that reach them · **what broke before** in this area: the error
ledger, `FOUND_DEFECTS.md`, patrol sightings, the feature's Change Log · the owner's own words
about the change.

**Each weakness** gets a stable id (`W-01`…), one line on what would go wrong *silently*, the
channel it rides, and the sink where it would show. A weakness that would show in no sink is marked
**UNTESTABLE**, stays on the list, and appears in the report. It is never dropped to make the
coverage look complete.

**Brief the list author like a discovery, not a confirmation:** the change, the outcome wanted, the
area of the product. Not the files, not the words to search for, not your own list. What you already
suspect you withhold and use as the test of what comes back.

## 3. A playbook

One file per playbook, two halves under one id, template beside this skill: `playbook-template.md`.

**STEPS — the half the runner gets.**
- Precondition: which real-use-case dataset, and how the state is reached — created by the runner
  through the product, or seeded on live by you (as `admin@admin.com`, disposable records) before the run and named here.
- The steps in the language a person would use: what to open, what to type, what to attach, what to
  click, what to wait for.
- What to **capture** afterward, as raw observations: the exact text of this note, the list of tool calls
  shown in the conversation, a screenshot of this panel, and **every entry in the Error Inspector** (copy all)
  at the end of the run. Capture, never judge. Database reads belong to the GRADER, run right after the run:
  a browser-only runner has no database, and a human runner should not need one (learned 2026-10-01).

**SEALED CHECKS — the half the runner never gets.**
- One **marker** per channel the change touches: a unique, realistic fact from the use-case library,
  planted in exactly one input channel. Never a placeholder-looking value.
- For each marker: the sink where it **must** appear, and the sinks where it **must not** appear. The
  second half is what catches a swap, a leak, or content delivered through the wrong door.
- Which weakness ids each marker covers.

**Every link must be addressable by the agent under test.** If the chain needs an agent to call another
agent, the skill or context it reads must carry that agent's id, because the agent-call tool takes an id and
nothing finds an agent by name (round 1, 2026-10-01: the tool arrived, the agent could not connect "lane
planner" to it). A link the agent cannot reach is a flaw in the playbook, not a finding against the product.

**Design for the chain.** Put the deciding marker at the end of the longest chain the change
touches. "The note now contains the pickup time from the attached file" is one check that cannot be
true unless the file was received, parsed, placed in context, the page tool was offered, the agent
chose it, the confirmation appeared, the person approved, the write landed, and the page re-rendered.
That is what makes one passing test worth hundreds of smaller ones.

**Triggers are a slot, not a copy.** The same playbook names every entry point that can perform the
job, and a run is one playbook through one trigger. The after-run covers every trigger.

**Reference playbook (chat, client side):** the agent must edit a note on the notes page so it
matches an attached markdown file and includes a detail that exists only in an attached internal
resource. The run must show the confirmation control, the runner approves it, and the note must end
up holding the file's marker and the resource's marker, in the note and nowhere else.

**Server side, for later:** a chain of agent calls where a marker coming back in a reply proves
several AI providers, dozens of tools and the state between them. The same playbook shape with the
reply as the sink. Not expanded here.

## 4. The runner

- A **fresh agent** with no part in the change. Lane `quick` (Sonnet) by default; raise it only when
  a baseline run is INCONCLUSIVE for reasons of the runner, never of the product.
- **Gets:** the STEPS half, its own localhost hostname and the dev-login route, signed in as `admin@admin.com`, plus the
  read queries the steps name. **Never gets:** the checks, the markers' expected placement,
  whether a fault is planted, the diff, or the change's purpose.
- **Tools:** the provider's in-app browser on the runner's own hostname, and read-only queries on the
  live database. No write tools, no file edits, no API calls outside the product. With only the product in
  hand, the end state can be made true only by the product doing its job.
- **Returns** raw observations in the ledger's run shape, or "could not complete step N because…".
  It never returns PASS or FAIL.
- **You grade** by laying observations against the sealed checks: **PASS**, **FAIL** (the product
  produced the wrong state), or **INCONCLUSIVE** (the runner did not finish). INCONCLUSIVE is never a
  pass. Twice on one playbook means the steps are unclear or the product is unusable at that step,
  and you find out which.
- The product under test is localhost (the page, the local aidream, the one database at `https://db.matrxserver.com`), signed in as
  `admin@admin.com` (Arman, 2026-10-03: test on live; the clone is no longer a test target). The runner touches only
  that account's disposable records. A run during which another session changed the shared localhost server's build is
  INCONCLUSIVE. Never Arman's Chrome. Never a sign-in or sign-out on a Matrx host outside the runner's own hostname.

**The fix loop is cheap or it does not happen.** After the first run that reaches the end, the runner's own
transcript is the script: a browser-only `quick` agent replays the same sheet for every fix and every fault
run, and the owner grades from captures without re-reading the product. A fresh, unscripted runner is used
twice only: the baseline and the final after-run. Never let the expensive owner model drive the browser.

**Reset, then verify, before every run.** The grader restores the start state (the fixture's canonical content,
values, chips) and PROVES it with the same queries the sealed checks use, before handing out the sheet. A run on a
dirty start state is INCONCLUSIVE whatever it shows (2026-10-01: a fault proof ran on a note still holding the
previous run's finished line; the agent "corrected" it instead of filling it, and the proof had to be repeated).
A shared preview that other lanes are editing hot-reloads the runner's page mid-run; sequence runs after fixes
land, and treat "page changed by itself" as INCONCLUSIVE.

## 5. Fault proof — a test is trusted only after it catches a break it was not told about

- **One per playbook**, each aimed at a different channel, so that across the set every channel's
  marker has been seen to fail at least once.
- **Subtle, at a boundary, everything else working:** an attachment type dropped at the edge, a
  resource's content replaced by the previous version, a tool silently absent from the agent's set,
  a denied write that returns as if it succeeded, channel A's payload delivered to channel B. A crash
  or a blank page proves nothing, because anything catches those.
- **Prefer breaking disposable data over breaking code** (`admin@admin.com`'s own records on live, never anyone else's). Detach the resource, remove the tool from
  the agent's definition, flip the binding, point the mandate at the old version. Reversible, no edit on the shared checkout. Restore it and read it back before the next run.
- **Code faults only through `plant.py`**, with the runner dispatch as the planted command. It holds
  the repository lock, restores in `finally`, and screams with exit 5 if a peer commit captured the
  mutation. The preview hot-reloads, so the fault is live the moment it lands and gone the moment it
  is restored. Keep the window short and never across a turn boundary: `sync-main` commits every
  uncommitted file and a fault left on disk is in a release within thirty minutes.
- **Blind.** The runner is not told. The grade must be **FAIL**, and the marker that failed must be
  the channel the fault hit. A PASS, or a FAIL for a different reason, means the playbook cannot see
  that channel: rewrite it before anything else counts.
- **Every attempt is a ledger row**, caught or missed.

**Where the fixtures live.** A chat or agent run goes through the production server, so a real test of chat runs on live, as the
test admin (`admin@admin.com`), on disposable records in a test-fixture organization. Faults that touch data touch only those
disposable records. Check the organization is not archived before installing (a 2026-10-01 install went into an archived
twin; the server admitted it and the doors refused it).

**The channel is part of the test — a rehearsal that runs as a privileged database role proves nothing
about the production channel.** On 2026-10-01 the production final switch was refused twice (the copy
fence refused the press's own writes because the server presses as `app.actor_tier=code`, then an
organization wall refused the presser, who was not a member) after every clone rehearsal (a migration rehearsal, which is still what the clone is for) had passed: the
rehearsal synthesised the person's token and called the database functions as the store-owner role, which
every fence and wall lets through. A dress rehearsal drives the SAME doors the person's click reaches
(the server route, with a real session from the product's own auth) as a person shaped like the real one
(the admin lane, and NOT a member of what the step touches), so that the server channel's actor settings,
caller role, request headers and the person's memberships are the ones judged. Prove the rehearsal red
against the pre-fix bodies before trusting it green; a rehearsal that never saw the production sentence
cannot vouch for the fix. Method and proof: the retired data-doctrine lane report `v5/PROGRESS-PRESS-FENCE.md` (git history)
(the honest rehearsal, lane PRESS-FENCE-HONEST).

**Runners on one machine.** The provider's in-app browser pane is one per machine: every runner and every fixer takes
a lock before its first browser step — `mkdir /tmp/matrx-browser-lane.lock && echo <name> > …/owner` — checks the
owner is itself before every browser step, releases only its own lock, and never removes another's (2026-10-01: a
fixer tested without the lock and deleted a runner's; the runner's tab was navigated away twice). Each seat gets its
own preview hostname (`MATRX_PREVIEW_SESSION=<name> pnpm dev-login …`); the plain host is shared and other
sessions navigate it. A run during which the shared preview changed database mode, or another lane's edit raised a
build error, is INCONCLUSIVE; say so and rerun.

**Many playbooks, one lane: the owner serialises, the runner never parks.** Eight runners dispatched at once
on 2026-10-02 did eight minutes of work: one took the lane, the other seven started a background wait for the
lock and ENDED THEIR TURN, returning "queued, no captures" as a completed task — a background wait dies with the
turn. The owner dispatches one runner at a time, after a wait that sees the lock directory absent for thirty
seconds, and the runner brief says in so many words: a report with no captures is a failed run; if the lane
is held, wait in the foreground and walk the sheet in this same turn. Budget one lane-run at a time: eight
playbooks of ten to twenty minutes each is two to three hours of wall clock, not ten minutes.

**Performance is a capture, not an opinion.** Every rerun records, with the runner's own clock (`date +%s` before
step one, before each send, at the first visible word, at the finished state) and the page's navigation timing
(`performance.getEntriesByType("navigation")`: ttfb, domReady, load, resource count), how long each step, each
turn and each page load took; the grader adds the server's own per-turn rows (iterations, tool calls, model and
tool milliseconds, tokens, cost) and the runner's harness usage. Numbers from two runs of the same sheet are the
only honest "faster"/"slower"; a run file without them is a story. The capture rules are `RUNNER-ADDENDUM.md` CX4.

## 6. Where it lives

`common-docs/operations/real-tests/<area>/` — the playbooks and one `LEDGER.md`. Playbooks walk
the product, not a repository, so they live in common-docs (`docs` skill). The ledger holds
three small hand-written tables: the weakness list; playbook × weakness coverage, with the marker
that covers each cell; and the runs — date, playbook, trigger, runner lane, commit, fault planted or
none, grade, which marker decided it. Weakness ids and playbook ids are stable across changes in
the area, so the next net starts from this one.

## 7. Report — plain language, in chat

Where the weaknesses came from and how many · each playbook and the chain one pass proves · every
fault, caught or missed, and what was rewritten when missed · the after-run grade per playbook per
trigger · what is UNTESTABLE and why. End with **"shipped"** or **"stopped, because X"**. Never
"tests pass" as the whole report, and never a pointer to the ledger in place of the words.

## Rationalizations

| Excuse (observed) | Reality |
|---|---|
| "Tests are green" offered as done (`forcing-function-tests`, 2026-09-10 reps) | Green from the builder's own tests on the builder's own data is a claim about the data. A fresh runner on the live product is the test. |
| "I'll write the regression checks once the change settles" | Written after, a test describes what was built. Written before, it describes what must hold. Only the second can fail. |
| "The existing test already covers this" — said before the fault proof | Until a planted break has made it fail, nobody knows what it covers. |
| "I know the expected values, I'll run it myself to save a dispatch" | A runner who knows the answer can make the state true by other means. The dispatch is the test. |
| "The change is urgent; the net can follow the first commits" (shared-checkout pressure) | The first commit is the change. A net that follows it has no baseline and proves nothing about the before. |

## Red flags — thoughts that precede the violation

- "This is basically a one-feature change" — said about something with consumers in another repo.
- "Let me adjust the playbook; the step was ambiguous" — right after an after-run FAIL.
- "A quick fault, I'll just edit the file and put it back" — on the shared checkout.
- "The runner clearly got confused; I'll call it a pass."
- "Eight playbooks is fine, they're small."
- "I'll seed the final state directly so the run is quicker."

## Banned

Tests written after the change · one agent writing, running and grading · a runner with write tools
or the sealed checks · PASS or FAIL from the runner's mouth · INCONCLUSIVE counted as a pass ·
editing a playbook to make it pass · an obvious fault offered as proof · a hand-edited fault left on
the shared checkout · a fault that touches anything but `admin@admin.com`'s disposable records · more than six playbooks · placeholder-looking
markers · "tests pass" as the report · turning any of this into something that runs on its own.
