---
name: hackathon
description: "User-invoked side-route for a judged, time-boxed hackathon day: turns the event brief into a scored project choice, an over-full scope ladder re-planned from measured pace at fixed clock checkpoints, a production-grade build with a visible factory, and a table demo with judge Q&A drilled from a decision log. Not for an unjudged proof of concept (that's /lfg), not for production features, not model-invoked."
disable-model-invocation: true
sources:
  primary:
    - "Shape Up — Ryan Singer"
    - "Hit Makers — Derek Thompson"
  secondary:
    - "The Pragmatic Programmer — Andrew Hunt & David Thomas"
    - "Noise: A Flaw in Human Judgment — Daniel Kahneman, Olivier Sibony & Cass Sunstein"
    - "The Checklist Manifesto — Atul Gawande"
---

# Hackathon

Plan, build, and demo one project inside a judged event's fixed build window.

A hackathon asks three questions that the normal pipeline does not, and this
skill exists to answer them:

1. **Which project wins?** The most useful project and the winning project are
   different choices. Judges see many tables in a row, rate noisily, and remember
   the best moment and the last one more than the average. Projects that win are
   *familiar surprises*: a frame the judge already knows, with one twist they
   did not expect, understood in seconds (Thompson's MAYA, "most advanced yet
   acceptable").
2. **How much fits?** Do not estimate in hours. An agent-assisted build does not
   move at human rates, and a model estimating its own throughput borrows human
   ones. Fix the time, vary the scope (Shape Up): plan more rungs than seem
   possible, **measure** how long rungs actually take on the day, and re-plan at
   fixed clock checkpoints from that measured pace. Your own measured rung time
   is the only reference class that counts.
3. **What does "done" mean when judges inspect it?** Many events judge the
   process as well as the product: tests, security, observability, and whether
   you can explain your decisions. The build keeps its tests and gates, and the
   process that produced the code (the *factory*) is something you show.

The time box is fixed. Scope, never the deadline, absorbs every surprise.

## Invocation Position

**Side-route, user-invoked only.** It fires when a human types `/hackathon
<brief-url-or-nothing>`; `disable-model-invocation: true` keeps its description
out of every other session's context. Send it as its own message, never as the
first message of a fresh workspace: a host that prepends text to a first message
displaces the slash command, and because this skill is hidden from the model it
cannot be looked up afterward (the same failure `/lfg` § Invocation Position
records).

It runs in **two sittings**: prep before the event (Phases 0–2) and the build day
(Phases 3–4). A second `/hackathon` with no argument resumes from the newest
dossier (see **State**).

**Boundary with `/lfg`.** `/lfg` takes an ask to an unattended proof-of-concept
PR and ends in `/pre-merge --loop`. Use it for a spike nobody judges. Use
`/hackathon` when a panel will judge the result inside a fixed window: it adds
project selection, clock checkpoints, and the demo, and it keeps a human in the
loop all day.

**Reconnects to the main workflow:** nowhere by default; the event is the end of
the line. If the project continues after the event, start it at `/shape` with the
dossier and `DECISIONS.md` as input. If the day exposed friction in the pack
itself, recommend `/improve-pipeline`.

**Mode.** HITL by default, one question per turn. A rung runs AFK only after its
row in the ladder names its done-condition and its tracer test.

**What this skill never does.** It never invents a judging rubric, weight, or
prize the brief does not state. It never pushes to the event repo before the
event's start time. It never moves the freeze or the submission deadline: when
time runs short it cuts rungs. It never writes the review-currency stamp, never
merges, and never runs `/closeout`.

## Locked vocabulary

Every phase reads these values. Change one here and nowhere else.

| Name | Value |
|---|---|
| Candidate count | 5–8 projects scored in Phase 1 |
| Score scale | 1–5 per dimension, anchored in **Phase 1** |
| Disagreement threshold | a blind second scorer differs by 2 or more on a cell |
| Ladder minimum | 6 rungs, at least 2 of them marked `~` (stretch) |
| Kickoff block | the first 20 minutes of the build window |
| Checkpoint interval | every 90 minutes from the end of the kickoff block, until the freeze |
| Freeze | 75 minutes before the submission deadline |
| Submission buffer | submit at least 15 minutes before the deadline |
| Table script length | 60 seconds |
| Dossier prefix | `hackathon-` |

## State

Two homes, split on purpose.

- **Prep lives off-tree**, in the project's sidecar (the pack's private, local
  git repo outside the working tree), as one dossier:
  `<sidecar>/research/hackathon-<YYYY-MM-DD>.md`. Events often require the repo
  to be empty until the start, so nothing from prep may be committed there.
  The dossier's shape is
  [references/dossier-template.md](references/dossier-template.md).
- **From the start time on, two files live in the event repo:** `PLAN.md` (the
  ladder) and `DECISIONS.md` (the decision log). This is a scoped exception to
  the pack's rule that durable state never lives in the project tree. Here the
  repo *is* the judged deliverable, and judges read the decision log. The
  exception covers those two files in an event repo and nothing else.

Set up the sidecar in the directory that will become the event repo. Create it
with `git init` and **no commits and nothing pushed**, so the empty-until-start
rule holds. Ask the user for the event repo's remote URL (the empty repo they
create on the forge) and record it with `git remote add`, which pushes nothing,
**before** `init`: `init` reads the remotes once to set `forge.kind` and the
write permissions, so a sidecar created with no remote records `none` and
routes PRDs, slices, and the review stamp to the sidecar instead of GitHub. The
resolver has no command that re-derives `forge.kind` later (`config set mode`
re-derives only the write permissions), so if the URL is not known yet, do not
leave the remote off. Ask which forge host the event repo will use, put a
placeholder on that host in the `<event repo remote URL>` slot below (for
example `https://github.com/placeholder/event-repo.git`), and when the real URL
arrives run `git remote set-url origin <real URL>`; the sidecar still resolves
and `forge.kind` stays as recorded. The resolver is the bundled
[references/sidecar.sh](references/sidecar.sh), at its absolute installed path:

```bash
SC="<this skill's directory>/references/sidecar.sh"
git rev-parse --git-dir >/dev/null 2>&1 || git init -q
# The URL the user gave for the event repo. Adds the remote only; pushes nothing.
git remote get-url origin >/dev/null 2>&1 || git remote add origin "<event repo remote URL>"
if git rev-parse --verify -q HEAD >/dev/null; then
  echo "note: this repo already has commits; if the event requires an empty repo until the start, stop and use a fresh directory" >&2
fi
SC_ERR="$(mktemp)"
if bash "$SC" resolve 2>"$SC_ERR"; then
  echo "sidecar: resolved (a hit; do not run init)"
elif grep -q '^SIDECAR MISS' "$SC_ERR"; then
  cat "$SC_ERR" >&2
  echo "sidecar: miss; ask the mode question below, then run init" >&2
else
  cat "$SC_ERR" >&2
  echo "sidecar: resolve failed without a SIDECAR MISS line; stop and relay it as printed" >&2
  rm -f "$SC_ERR"
  exit 1
fi
rm -f "$SC_ERR"
```

Creating a sidecar is a human decision, so run `init` only on the `SIDECAR MISS`
line above. On any other failure, stop and relay what the block printed, with no
questions and no `init`. On a miss, ask **one question**: is the event repo
`owned` (the user's own, so the pack may write issues and PRs on its forge) or
`guest` (the organizer's or someone else's, so the pack writes nothing to its
forge)? Recommend `guest` when the repo sits in an organizer's or sponsor's org.
Then run `init` with the miss line's suggested `--name` and the answer:

```bash
SC="<this skill's directory>/references/sidecar.sh"
bash "$SC" init --name <suggested name from the miss line> --mode <owned|guest> --write sidecar --in-tree-path none --no-migrate-archive
```

Relay an `init` refusal as printed. Then, on a hit or after `init`:

```bash
SC="<this skill's directory>/references/sidecar.sh"
research_dir="$(bash "$SC" path research)" || exit 1
echo "dossier: $research_dir/hackathon-$(date +%F).md"
```

Commit the dossier to the sidecar at the end of each phase. Set the dossier's
`phase:` first, to the phase that comes next (`choose` after Phase 0, `shape`
after Phase 1, `build` after Phase 2, `demo` at the freeze, `done` after
Phase 4), so a resume starts where the work stopped:

```bash
SC="<this skill's directory>/references/sidecar.sh"
bash "$SC" commit -- "<dossier path>" -m "hackathon: <phase name>"
```

**Resume.** With no argument, find the newest dossier, read it, and continue
from the `phase:` its frontmatter records (`demo` resumes at Phase 4). A `build`
resume skips the kickoff block when `PLAN.md` is already committed in the event
repo:

```bash
SC="<this skill's directory>/references/sidecar.sh"
research_dir="$(bash "$SC" path research)" || exit 1
newest="$(find "$research_dir" -maxdepth 1 -name 'hackathon-*.md' | sort | tail -n 1)"
if [ -z "$newest" ]; then
  echo "no dossier in $research_dir; start at Phase 0" >&2
  exit 1
fi
echo "$newest"
sed -n '2,/^---$/p' "$newest"
```

## Process

### Phase 0. Event profile

Take the brief as a URL (fetch it, and any rules, FAQ, or judging page it links)
or as pasted text. Fill the dossier's **Event profile** table. Mark every field
`stated` (with a short verbatim quote) or `not stated`:

- start time, build window, submission deadline, and submission platform
- judging format (stage pitch, floor or table visits, video) and length
- judging criteria and any weights
- tracks and prize categories, including sponsor prizes
- team size; rules on pre-built code, templates, and installed tooling
- allowed tools and models; required artifacts (repo, video, write-up)

Never fill a `not stated` field with a typical value. A rubric you invented
steers every later score toward a judge who does not exist. Instead, list each
gap as a question for the organizers in the dossier's **Open questions**.
Whether your own installed tooling counts as pre-built code is always on that
list unless the rules state it.

**Recheck before the build.** When a rules guide or judging guide arrives later,
redo this phase against it before Phase 3.

**Team.** Then ask, one question at a time, who is on the team and what each
person will do on the day: who writes code, and who does not. Record each person
in the dossier's **Team** table with the accounts they need logged in. A team is
rarely all builders. A common shape is one developer driving agents plus a
product, design, or domain person who writes no code, and that person is not a
spare pair of hands. They are the one independent reader the build has, and
Phases 1–4 give them work only a non-builder can do well (see **Lanes** in
Phase 2).

### Phase 1. Choose the project

1. **Reference class.** Look at what this event, or the same series, picked
   before: a past-winners gallery (Devpost and similar list them), a recap post,
   or sponsor-track winners. Note in one line each what the winners had in
   common. If there is no history, record `none found` and move on.
2. **Generate candidates.** Ask the user, one question at a time, what problems
   they care about and what the tracks invite. Then propose candidates up to the
   Locked count. Include at least one that is *familiar* and one that is
   *ambitious*, so the scoring has range.
3. **Score each dimension across all candidates before totaling anything.**
   Score dimension by dimension, column by column, never candidate by
   candidate. A strong first impression of one candidate then cannot raise its
   other scores (Noise's decomposition move: independent assessments first, one
   holistic judgment last). Anchors, 1 → 5:

   | Dimension | 1 | 5 |
   |---|---|---|
   | **Fit** | fits no stated track or criterion | squarely in a stated track and hits every stated criterion |
   | **Familiar surprise** | either a clone of a known thing, or nothing a judge can map to anything | sayable as "a known X, for / with an unexpected Y" |
   | **Peak moment** | nothing visibly happens in a demo | one moment where a judge watches something surprising happen live |
   | **60-second legibility** | needs a setup talk before it makes sense | a judge gets it from the first screen and one sentence |
   | **Factory showcase** | the process behind it would be invisible | building it exercises tests, gates, and agents you can tour |
   | **Slow-dependency risk** (higher is safer) | needs approvals, hardware, scarce data, or a paid tier | runs on accounts you already have, with public or synthetic data |
   | **Why you** | no reason you, specifically, built this | a reason you can say in one sentence that a judge will believe |

   Weights follow the brief's stated weights. When none are stated, weight the
   dimensions equally and say so; do not invent a weighting.
4. **Blind second scorer.** Spawn one fresh sub-agent. Give it only the event
   profile, the candidate one-liners, and the anchor table, never this
   conversation. Have it score the same grid. Discuss only the cells where the
   two grids differ by the Locked disagreement threshold. That spread is the
   noise in your own judgment. When the team includes a non-builder, have them
   score the grid too, on their own and before seeing either grid. A person who
   thinks like a user is the closest stand-in for a judge you have, and their
   column is worth more than a third model.
5. **Compare, then commit.** The Locked candidate count, scored on seven dimensions,
   meets the comparison threshold in
   [references/next-step-menu.md](references/next-step-menu.md) § Show the
   comparison before you take the choice. Show the grid as a table first, then
   ask the user to pick with an `AskUserQuestion` menu. The menu's option cap
   (see the same reference) is smaller than the candidate count, so offer only
   the top scorers that fit, top scorer first and marked recommended; the
   free-text "Other" hatch takes a pick from the rest of the table.
6. **Write the two lines everything else hangs on** into the dossier:
   - the **high-concept line** ("a known X, with Y"), and
   - the **peak moment**: the one thing the judge watches happen.

### Phase 2. Shape

Use `/shape`'s discipline compressed to one sitting; point at it rather than
re-deriving it. Fill the dossier:

- **Scope ladder.** List at least the Locked minimum of rungs, in build order.
  Plan more than seems possible on purpose: cutting a planned rung at a
  checkpoint is cheap, and an empty ladder at mid-afternoon wastes the day.
  - **Rung 1 is a tracer bullet** (Hunt & Thomas): the thinnest path that runs
    end to end through every real layer, demoable on its own, built with
    production structure rather than as a throwaway prototype. If only rung 1
    ships, you still have a demo.
  - Each later rung adds one thing a judge would notice, and it must be able to
    land on its own.
  - Mark nice-to-haves `~` (Shape Up's scope hammer). They are the first cut.
  - Give each rung a done-condition and the tracer test that proves it. A rung
    without both is not ready to run AFK.
  - Put the peak moment as early on the ladder as it can go.
- **Rabbit holes and no-gos.** Name what you will not build, and the parts most
  likely to swallow an hour, along with what you will do instead.
- **Slow-dependency work goes first.** Move to the kickoff block and rung 1
  everything an agent cannot speed up: API keys and quotas, OAuth and auth, the
  deploy target (its final hostname), the riskiest third-party integration, and
  data access. These fail slowly, and they fail late if left late.
- **Factory plan.** Decide which process artifacts to stand up at kickoff and
  show at the table: the pipeline hooks from `/init-pipeline`, CI running the
  tests on every push, a dependency or secret scan, structured logging or a
  health endpoint, and the decision log. Pick what the event's criteria reward.
  If the brief names none, default to tests, CI, and logs.
- **Lanes.** Split the day by lane, not by person, then give each lane an
  owner from the **Team** table. Record the owners in the dossier.
  - **Build lane** (whoever writes code, with agents): the rungs, the factory,
    and the deploy. With several builders, give each a rung from the same
    ladder, choosing rungs that touch different files where possible.
  - **Demo lane** (a non-builder when there is one): owns the clock and calls
    each checkpoint; accepts each rung by using it on the deployed URL against
    its done-condition, not by reading code; seeds the demo data and rehearses
    the peak moment; keeps `DECISIONS.md` current by asking "why that one?" as
    decisions happen; drafts the submission write-up and table script during
    the build instead of after the freeze; asks mentors and organizers the
    **Open questions** on the floor.
  - **Solo:** you hold both lanes. Put the demo-lane work into the checkpoint,
    so it happens at fixed times instead of never.
- **Seed the decision log.** Copy each decision made so far (project, stack,
  cuts), with the alternatives you rejected and why. Judges ask "why X over Y?",
  and the answer should already be written down.
- **Pre-flight checklist** for the night before (dossier template § Pre-flight):
  accounts logged in on the build machine, keys tested, the deploy target
  reachable, chargers and adapters packed, and the rules guide read with
  Phase 0 rechecked against it.

End prep: set `phase: build`, commit the dossier, and print the clock plan from
the next section so the user sees the day.

### Phase 3. Build day

**Clock plan.** Compute from the event profile, using the Locked vocabulary:

- the kickoff block's end (start time + kickoff block)
- each checkpoint (every checkpoint interval after that, while before the freeze)
- the freeze (deadline − freeze)
- the submit-by time (deadline − submission buffer)

Write the four kinds of times into `PLAN.md` and the dossier. Then hold them:
nothing in this phase moves the freeze or the submit-by time.

**Kickoff block** (after the start time and never before):

1. If the build actually starts at a time other than the event profile's start
   time, recompute the kickoff block's end and the checkpoints from the actual
   start, in `PLAN.md` and the dossier alike. The freeze and the submit-by time
   come from the deadline, so they stay. Add `PLAN.md` (the ladder plus the clock plan) and `DECISIONS.md` (copied from the
   dossier's seeded log), make the first commit, then push it to the remote added in
   prep with `git push -u origin HEAD`.
2. Run `/init-pipeline` to scaffold the hooks and pre-commit gates. Add CI that
   runs the commands in `lefthook.yml`, the one source for what the hooks run,
   with the staged-files placeholder replaced by the whole repo. Never write a
   different command into CI: a CI step that checks other files than the hook
   fails on files every local commit passed.
3. Deploy a hello-world to the deploy target, so the slowest unknown is resolved
   first.

**Rung loop.** For each rung, in ladder order:

1. Record its start time in the dossier.
2. Write the rung's tracer test first, then the code. Delegate to `/tdd` for
   behavior-heavy logic; invoking it creates `.claude/.tdd-active`. Once
   `/init-pipeline` has installed its hook, an implementation write is blocked
   unless a classification marker exists, so a rung that is visual, layout,
   styling, or copy only, and so does not go through `/tdd`, first creates
   the skip marker at the project root, where the hook looks, not in the
   current directory:

   ```bash
   ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"
   mkdir -p "$ROOT/.claude" && touch "$ROOT/.claude/.tdd-skipped"
   ```
3. Run the tests, commit, and push. Then watch every CI run for the pushed
   commit until each finishes ([`gh run watch`](https://cli.github.com/manual/gh_run_watch)).
   A repo with a deploy workflow gets more than one run per push, and watching
   only the newest can report the deploy's green while CI is red. A run can take
   a few seconds to register, so the block polls for up to two minutes. It exits
   2 when `gh run list` fails and 3 when no run appears: neither is a CI result,
   so neither is green, and 3 means CI has no run for this commit (check that
   the push landed and that a workflow triggers on it):

   ```bash
   SHA="$(git rev-parse HEAD)"; IDS=
   for _ in $(seq 12); do
     IDS="$(gh run list --commit "$SHA" --json databaseId -q '.[].databaseId')" || exit 2
     test -n "$IDS" && break
     sleep 10
   done
   test -n "$IDS" || { echo "no CI run for $SHA" >&2; exit 3; }
   FAIL=
   for id in $IDS; do
     gh run watch "$id" --exit-status || FAIL=1
   done
   test -z "$FAIL"
   ```

   On red, do not deploy and do not start the next rung: fixing the run is
   this rung's work: leave the classification marker in place, go back to
   step 2 to fix it, and repeat this step. Do not tick the rung yet (step 6
   does). Once every run is green, remove the rung's classification marker, as
   `/execute` Step 6 does, so the next rung classifies afresh and the gate
   stays closed between rungs:

   ```bash
   ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"
   rm -f "$ROOT/.claude/.tdd-active" "$ROOT/.claude/.tdd-skipped" "$ROOT/.claude/.lfg-active"
   ```
4. Deploy the green commit to the deploy target, or confirm CI's deploy
   shipped it, then give the demo-lane owner the URL. Acceptance below happens
   on that URL, so a rung that is not deployed cannot be accepted.
5. Append to `DECISIONS.md` any decision the rung forced, with the rejected
   alternative.
6. The demo-lane owner (you, when solo) accepts the rung: they use it where a
   judge would, and either tick it in `PLAN.md` or name the gap. A rung is
   done only when accepted, so a builder's green commit does not make it done.
7. Record its end time when it is ticked.

The lanes from Phase 2 run in parallel. The checkpoint re-plan below still runs
on the whole ladder, and the demo-lane owner calls it.

**Checkpoint** (at each checkpoint time; stop what you are doing):

1. **Measure.** From the dossier, compute the median time per accepted (ticked) rung.
   Leave rung 1 out once two later rungs exist, because it carries setup time.
2. **Re-plan from measured pace, never from a fresh estimate.** Rungs that fit
   ≈ (freeze − now) ÷ median rung time. Keep that many of the remaining rungs in
   ladder order. Cut `~` rungs first. If the time left exceeds the remaining
   ladder, add rungs: the ladder ran short, not the day.
3. **Circuit breaker.** If rung 1 is not green at the first checkpoint, make it
   thinner: stub the dependency that blocks it behind the same interface, and
   say so in `DECISIONS.md`. Pivot projects only if the idea itself is broken.
   A thinner tracer is almost always cheaper than a new idea.
4. Record the re-plan (kept, cut, added) in the dossier and `PLAN.md`. A
   changed ladder is a real fork, so confirm it with the user before going on.

**Freeze.** At the freeze, stop adding rungs. Whatever is unfinished either
works behind a flag or gets reverted. Set `phase: demo` and commit the dossier.
From here on, the only work is demo readiness.

### Phase 4. Freeze → demo

1. **Pre-demo checklist** (dossier template § Pre-demo). Run it DO-CONFIRM
   style: do the work, then read the list aloud and confirm each item (Gawande).
   Things fail at the worst moment, so the checklist assumes the live demo will
   break; the template holds the one list.
2. **Submission.** Fill the platform's write-up from the dossier and `PLAN.md`:
   the problem, the high-concept line, what shipped (the ticked rungs), how it
   was built (the factory), and what was cut. Submit by the submit-by time.
3. **Table script** (Locked length): open on the high-concept line, show rung 1's
   path, and **end on the peak moment**. Judges remember the peak and the
   ending. Rehearse it until it fits the time, then rehearse the 15-second
   version for a judge who is already walking away.
4. **Judge Q&A.** From `DECISIONS.md`, draft the five most likely "why X over Y?"
   questions with a one-sentence answer each, plus a two-minute factory tour:
   the hooks, CI, the tests, and the decision log. Drill both with the user, one
   question at a time.
5. **Who says what at the table.** With a non-builder on the team, they open:
   the problem, the high-concept line, and the demo through the peak moment.
   The builder takes the factory tour and the "how did you build it" questions.
   Each "why X over Y?" goes to whoever made that decision in `DECISIONS.md`.

Before `phase: done`, tick the template's § Pre-handoff confirmations, then commit the dossier.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We can estimate this rung at about an hour." | That number borrows a human's pace. Measure the first rungs and re-plan from them. |
| "Push the freeze back 20 minutes; we're close." | The freeze protects the demo, which is what gets judged. Cut a rung instead. |
| "Skip the tests, it's only a hackathon." | When the criteria judge tested, secure, observable work, the tests are part of the score. |
| "This idea is the most useful, so it wins." | Usefulness that takes three minutes to explain loses to a familiar surprise a judge gets in ten seconds. Score legibility and the peak moment. |
| "The rubric probably weights technical depth." | If the brief does not say so, it is `not stated`. Ask the organizers. |
| "Score each idea as we go." | The first idea's halo then sets every later score. Score each dimension across all candidates first. |
| "Push the scaffold the night before to save time." | Most events require an empty repo until the start. Prep stays in the sidecar. |

## Red Flags

- A score or weight in the dossier with no `stated` quote behind it.
- A ladder with fewer rungs than the Locked minimum, or no `~` rungs.
- A checkpoint that re-estimated remaining rungs instead of using the measured median.
- A commit in the event repo dated before the start time.
- No recorded fallback video at the freeze.
- `DECISIONS.md` unchanged since kickoff.

## Handoff

- **Expected input:** the event brief (a URL or pasted text) and the user, present for both sittings, plus who else is on the team and whether each writes code; a local directory that will become the event repo.
- **Produces:** the sidecar dossier (event profile, scored candidates, ladder, rung timings, checkpoint re-plans); in the event repo, `PLAN.md`, `DECISIONS.md`, the pipeline hooks, and CI; a submitted entry; a rehearsed table script and judge Q&A.
- **May invoke:** `/init-pipeline` (kickoff block), `/tdd` (rung loop), one blind-scorer sub-agent (Phase 1).
- **Returns control to:** the user at the judging table.
- **Comes next by default:** nothing. To continue the project after the event, start at `/shape` with the dossier and `DECISIONS.md`. For pack friction, use `/improve-pipeline`.

Print, substituting the real values:

```
**Next session:** /shape (only if the project continues)
**Input:** dossier <path> and DECISIONS.md in <repo> — a hackathon build; read its cut rungs before reshaping
```
