---
name: teach-the-system
type: Skill
title: "teach-the-system — teach the platform one body of expertise until it breaks, fix it, continue"
description: "Trial protocol for teaching AI Matrx an expert's knowledge until the platform breaks, fixing it. Use when asked to run an expertise trial, distil a person/creator/recent video into a Masterwork, or test the capture product. NOT for a known-missing feature (use build-sub-feature)."
tags: [masterwork, distillation, expertise, trial, platform-testing, doctrine]
timestamp: 2026-09-14T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/teach-the-system/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# teach-the-system — teach the platform one body of expertise until it breaks, fix it, continue

**Companion file — read only the branch your run reaches:**

- **[lessons.md](lessons.md)** — every dated lesson from past trials (§8). **Read it once end to end
  before you choose a subject** (like the REGISTER walls table), **and again before you judge a run, call
  it a success, or trust a verdict.** Also read it when your run hits a stop (a wall, a silent or failed
  run, an access refusal, a red CI check, a Conductor or agent claim you are about to believe), when you
  drive the product headless or from a cloud container, when you face a pile of draft rules to review,
  and at §7 to append your own.

**What this is.** Arman wants an army of Fable-class developers who each pick one real body of
expertise, teach it to AI Matrx exactly the way a non-technical Expert would, run it on real cases
until the platform stops or breaks, fix the platform (never the trial), and continue — and who
report **what improved in the system**, not what happened to the run. The why, in his words, is
`common-docs/systems/masterwork/VISION.md` — read it once before your first trial.
**The architecture mandate every trial serves is his brief
`common-docs/systems/masterwork/VISION.md` (authority: owner, 2026-09-12):** capture the
tacit and the controversial across modalities, atomize with provenance, keep schools of thought and
dissent navigable, treat "weirdness" as the asset.
Night 1's full evidence trail is the sibling `REGISTER.md`; read its walls table before choosing
a subject so you inherit the fixes instead of re-hitting them.

**How victory is scored: the number of things the system could not do before the
trial and can do after.** Keep a capability ledger in the register — one row per "could not / can now" —
and lead the morning report with its count. The best rows are bridges: a way to move a person's or a
source's unique knowledge into an agent's instructions, a workflow step, a tool or a function. The
built desk is a by-product; a run that succeeded without a new row is worth nothing here (PROGRAM.md
ruling 6).

**"The developer" running a trial can be a dispatched Sonnet 5 subagent. Dispatch it in the `coordinator` lane (`model: sonnet`) with a dispatch budget — the only lane that can dispatch fixers.**
Driving the product as a non-technical Expert, judging outputs, logging walls, and writing the
register is not complex code — it is exactly the discovery/big-task work the Sonnet lane is for.
An owning session dispatches a Sonnet driver for the trial itself, and that driver in turn
dispatches fixers for the bounded platform code fixes each wall needs (Sonnet for a wall with a known
repro and files, Opus only for one with no known cause); Fable/default stays
reserved for planning and heavy reasoning, never for driving a trial end to end. If you are a
dispatched Sonnet driver reading this: you are authorized to run the whole trial loop (§4) and
dispatch your own fixes — do not hand the trial back up as "too big" or "campaign-scale". The
stop condition in your dispatch brief (a deliverable reached, or a pushed build to wait on — §5) is
your bound; treat it as the actual scope of the job, not a reason to escalate.

**This skill improves itself.** Everything Arman teaches you during a trial, and every mistake that
cost you an hour, goes into this skill in the same session (§7). A trial that ends without a skill
edit either learned nothing or lost it.

## 0. The mandate every trial is measured against

🚨 **The ruling authority for everything in this skill is
`common-docs/systems/masterwork/doctrine/CORE.md`** (Arman, 2026-09-14) and its companion parts,
`core-mandate-and-trial-program.md` and `advantage-stack.md`, in the same directory. Read CORE.md
in full before your first trial and whenever a rule here seems to conflict with it — CORE.md wins,
and this skill gets fixed. The checks below still apply on top of it.

🚨 Read `common-docs/systems/masterwork/VISION.md` (Arman, 2026-09-12, `authority: owner`)
before choosing a subject, and answer its seven checks in your register before you build: which acquisition
**modality** you add; whether the knowledge is genuinely **tacit** (if the expert could have written it down,
you are working on the cheap half); whether the output is **executable** (rubrics, checklists, if-then rules,
decision trees, annotated exemplars — never prose a desk must re-interpret); whether every atom carries
**provenance** and opens to it; **how you resist consensus collapse**; whether the expert can **validate in
their own modality**; and whether the platform can now execute something **previously inexpressible**.

🚨 The trap with a name: **pooling**. Fitting several experts — or several sittings of one expert — into one
merged model, one averaged verdict, or one consensus rulebook destroys exactly what the mandate calls the
principal source of value. Keep per-expert or per-school profiles as the unit, be able to show a minority
position that survived, and never resolve a disagreement by averaging.

## 1. Choose the subject — the Moat Gate

🚨 **Authority: `common-docs/systems/masterwork/doctrine/CORE.md` §3–4 (Arman, 2026-09-14).** This
section restates it for trial use; when the two disagree, CORE.md wins and this section is wrong.

REQUIRED before anything else: write the subject choice into your trial register (§3) with the
gate answers below. A subject that fails the gate is rejected.

1. **The Moat Gate — screening question: do this expert's own peers disagree with them?** A
   subject is worth a trial only if the expertise is **scarce**, locked in a head or a private
   corpus, **idiosyncratic** to one person, **non-stationary** (it keeps changing), or **private**.
   Disqualifiers: **if you could fine-tune it, fine-tune it** — that means it is not tacit; a
   memorized benchmark; anything a frontier model already does well raw.
2. **Gate by measurement, never by assumption — the A0 probe.** Run the best frontier model raw,
   with only the subject's byline instruction (no corpus, no our-artifacts), and score it on the
   seven-metric spine (§4 below). **If it already makes the heterodox calls, the subject fails —
   evidenced, not guessed.** For any public-figure subject, contamination-screen the *target
   artifact* (never the source corpus) so it postdates every model's cutoff in every arm, checked
   and logged before you run anything else.
3. **Recency is the proving ground.** Anything published in the last ninety days is guaranteed
   outside every model's training data — prefer these subjects while living experts stay in
   reserve (§4 below, readiness gate).
4. **Can the result be judged without you?** Prefer subjects with a judge built in: a real viral
   post fed to a verification desk, a described family situation fed to two parenting masterworks,
   or — strongest — the expert's own withheld real work as blind ground truth in the bench pool
   (the GT arm, §3 below). Name the judge now.
5. **Does the subject hold more than one school, and will you keep both?** Two sources that
   disagree are two schools of one body of knowledge, not one Rulebook to reconcile. Name the
   schools in the register before distilling; a rule that one source holds and the other rejects
   is the trial's most valuable output, never a "coherence tension" to settle. Trial 3 planned the
   pair and attached both to one Rulebook — 139 drafts, one desk, every disagreement resolved to a
   side: that is the consensus trap, and it is now a wall (§4 below).

**The bright line.** Every input that existed before the engagement began belongs to the raw
arms too — the corpus, retrieval, tools, web, a large budget, a competent prompt. Raw arms never
get the elicitation transcript, the distillate, the contrastive analysis, the decision tree, the
negative-space list, the rubric, or the correction log — those are engagement artifacts, ours
alone. Never build a "fair" comparison that hands a raw arm something we made.

**A public book is an input, not a subject that proves anything on its own.** Given the same book
in context, the raw frontier model matches or beats a Masterwork distilled from it (trial 2,
re-run 2026-09-14) — a book trial can find platform walls, but it cannot prove the product. Treat
a book the way CORE.md does: as one input among the acquisition doors (organizational exhaust,
past work, interviews, video), never as the default subject.

🚨 **Arman is never the subject.** He is not interviewed as the Expert, and no trial is built
around his own knowledge, until the readiness gate in CORE.md §8 is met: three consecutive
resource trials driven end to end by agents as non-technical users with zero unfixed walls, the
interview lane completing a full simulated session with the new probes with zero walls, and the
bench live so his own session yields a scored result the same day. Until then, a subject involving
him is out of scope for this skill.

Prefer subjects that need **no external service**. Fancy APIs make the distillation neither harder
nor easier — the barrier is never technology, it is whether the system captures the skill. When the
method genuinely needs a primitive (reverse image search, a records lookup), build it in the shared
layer and log it as platform capability, not as the trial's achievement.

The source must be freely and legally available (public domain, CC, the author's own site, a blog,
a recent video with a transcript). Record the licence and the link in the register.

**Acquisition doors, not subject classes.** CORE.md §5 lists the source lane, the body-of-work
lane, the YouTube link with time-anchored transcript, the monologue recorder, and the chat-import
lane as intake doors — pick whichever door the Moat Gate's chosen subject actually lives behind,
never as three parallel "kinds" of trial to rotate through. If the subject is expertise that only
lives in a person's head and that person is not Arman (§ above), the interview lane is that door;
if the interview does a shitty job, that IS the wall — fix the interview lane itself, in the shared
layer, before blaming the subject.

## 2. The rules of the trial

- **You are the non-technical Expert.** Product UI only: Masterwork guided start, distillation
  lanes, the Conductor by conversation, the run box, the pause forms. No API calls to author, no
  SQL to fix data, no hand-written workflow JSON. Reading the database to diagnose a wall is fine;
  writing to it to pass is cheating.
- **The source is the ONLY knowledge input.** Never hard-code its rules; never vibe-code an app
  that "does what the book does"; never pre-digest the text into rules yourself. The platform
  distils, the Conductor authors, you answer questions the way the author would.
- **Real cases from the world this week.** Never self-authored easy examples. Find them the way the
  job would (a viral post, a real family scenario from a forum, a real blog post).
- **Never collapse consensus.** The platform's principal value is the
  tacit, the idiosyncratic and the disputed. A rule seen once is a rule; recurrence is a signal on
  it, not a gate to existence. You never Approve-all a corpus, never answer a contradiction by
  picking a side when both could be true (say so — "both are right" with the condition that
  separates them), never let the Conductor fold two schools into one desk, and never let an
  interviewer rewrite the earlier position out of existence. Record every place the product pushed
  you toward one of these as a wall.
- **Cheat honestly.** A browser instead of an email tool, a pasted chapter instead of the whole
  PDF — allowed, logged as a cheat in the register with what the honest version would need.
- **Sign in without typing a password, ON YOUR OWN HOSTNAME.** Production browser pane signed out?
  Use the local preview (`pnpm preview:start`, port 3001) and then `pnpm dev-login /<route>`, which
  mints your session's single-use nonce and prints the URL to open. Never type a credential into a
  field.
- **🚨 Never open `localhost:3001` — open the hostname the harness prints.** Several trials run on
  one machine at once, and cookies are scoped to a HOST and ignore the PORT: on 2026-09-12 five
  sessions shared one cookie jar on `localhost`, so one agent's dev-login signed every other agent
  in as somebody else mid-form and the page correctly paused itself with "Account Changed…". Each
  session now gets its own `<label>.localhost` (printed by `pnpm preview:start` and
  `pnpm preview:status`; set `MATRX_PREVIEW_SESSION=<name>` to claim a readable one), which gives it
  its own cookie jar, storage and dev-login nonce on the SAME one server. Two more consequences for
  a trial: the slot being "taken" by a server serving THIS checkout is no longer a refusal — take
  the hostname it offers you — and your failed navigation can no longer burn another trial's nonce.
  Mechanics and forcing proof: `matrx-frontend/docs/official/browser-testing.md`,
  `pnpm check:preview-session`.
- **Cost is a measured result, graded on the five-arm bench, never a two-arm comparison.** Track
  model spend from `chat.request` for every arm you run (§3 below): A0 frontier raw, A1 frontier
  with the full corpus in context, A2 frontier plus retrieval/tools/web to a reported budget
  ceiling, B the cheap model raw, C our workflow on the cheap model, GT the expert's real withheld
  work blind in the pool. A "vibe-coded app vs. our build" comparison, or any report naming only
  two arms, is not a grade under this doctrine — see CORE.md §4 and advantage-stack.md §4.
- **Lanes:** [subagent model ladder](/policies/subagent-model-ladder.md); driving a trial is `quick` (Sonnet) work.
- **Done:** [deployment is the deploy agent's job](/policies/reality-is-the-referee.md) — commit, confirm on localhost, continue.

## 3. The register and the bench — the single source of state and the only valid grade

Create `common-docs/projects/<trial-slug>/REGISTER.md` on the first action, modelled on
`expert-book-challenge/REGISTER.md`: rules, source + licence, walls table
(`| W# | Where | What happened | Class | Status/fix |`), real test cases, a UTC timeline, "where
it stands", spend. Update it **as you go**, never at the end — a compaction or restart loses
anything not written. Also write a memory note (`project_<slug>.md`) with the state.

**Grading is the five-arm bench, never fewer arms.** Per CORE.md §6 / advantage-stack.md §4: run
A0 (frontier raw), A1 (frontier + full corpus in context), A2 (frontier + retrieval/tools/web to a
reported budget ceiling of 100× our cost), B (cheap model raw), and C (our workflow on the cheap
model, air-gapped by tool removal), then score all of them plus GT (the expert's real withheld
work, blind in the pool) on the seven-metric spine — heterodoxy retention and consensus drift
first, then decision selection, reason overlap, commitment, restraint, calibration — plus rule
fidelity, fabrications, cost-to-parity, capture cost in expert-hours, and walls hit. Record dollars
and seconds on every arm. **The trial is void if GT does not win the blind panel.** Name which of
the three wins (ceiling / quality / efficiency, CORE.md §6) the trial is claiming, or claim none.

**Until the bench UI exists, grade from the CLI.** `aidream/services/masterworks/bench` (being
built now) is the way to run and score the arms — check there first for the current entrypoint
before hand-rolling a comparison. **A report naming only two arms is not a grade under this
doctrine**, no matter how it is worded; if the bench CLI cannot yet run an arm you need, that is a
wall (§4), not a reason to fall back to a smaller comparison.

## 4. Hit a wall → fix the class → continue (the loop)

Every stop is one of these; do the matching thing and keep the trial moving:

| Wall | Do |
|---|---|
| Platform defect (silent drop, dead default, wrong error, stale cache, engine gap) | Fix the class (law 3, [the laws](/policies/the-nine-laws.md)) in the shared layer, push, rerun. |
| Missing primitive the method needs | Build it as a platform node/tool in the shared layer (lane named, subagent if it is bounded), wire it through the Conductor by conversation, never by hand. |
| Third-party switch (enable an API, approve an app, a console toggle) | Fix it yourself if you can (you have Arman's machine and logins), else write a ten-minute prompt for a Codex agent, hand it to Arman, start a watcher that wakes you when it is done, and **continue on the parts that do not need it**. It never stops the trial. |
| **Consensus collapse** — the product merged, deduped, synthesized-by-recurrence, excluded a once-seen rule from a build, framed two positions as a problem to settle, or offered Approve-all as the only way through a large review | A wall of the shared layer, not a review step. Keep BOTH positions verbatim in the register, log the wall with the mechanism (the live ones: the evidence standing and its 3-piece knob, statement-key dedupe, cross-piece-only synthesis, the tension card's recommendation, in-place `update_rule`), fix the class on the rule atom (retained dissent, school, history), continue with both schools alive. |
| The agent (Conductor) is wrong or stuck | Talk to it the way the Expert would; when it repeats a defect class, that is a platform wall (its instructions or tools), not a prompt to fix. |
| A stream detaches / a turn hangs | Read the server-side truth (request rows, `system_errors`) before re-sending; a hung turn with no message to the person is itself a wall. |

Dispatch subagents for bounded fixes ([ladder](/policies/subagent-model-ladder.md)) and keep driving the trial yourself. Two threads at once is the norm: a fix in flight, the trial advancing.

## 5. What "done for the night" means

Before you call a run a success, read [lessons.md](lessons.md) again.

A run reached the deliverable on a real case, OR the platform is blocked on a build you pushed. In
both cases the register says exactly where it stands, every wall has a status and an owner, and the
morning report exists (§6). "I got tired" is not a stopping point; a blocked deploy is.

## 6. The morning report — the capability ledger leads, never a run story

Written for Arman: plain sentences, no paths, no codes, no doc pointers (law:
`common-docs/policies/talk-to-arman-like-a-person.md`). **Every report opens with the capability
ledger** — one row per "could not → can now" (CORE.md §6) — never with what the trial did or how
the session went; a run that added no row is worth nothing and the report says so plainly rather
than padding with narrative. Immediately after the ledger:

- **Walls a real user hit — a first-class metric, counted and named, not folded into prose.**
  Capture *is* the product (CORE.md §4), so every wall the trial hit while driving the product as
  a non-technical Expert is reported at the same weight as a capability gained, fixed or open.
- **Every UI defect, however small, logged** — a dead control, a false "saved", a caveated finding
  shown instead of dropped, a stray pixel. Nothing is too minor to log; an unlogged defect is a
  defect the next trial re-discovers.
- **The tacit ledger:** how many rules the trial kept that a frontier model would not have produced
  unprompted (verified against the A0 probe, §1), how many disagreements it kept alive as two
  positions, and how many the product tried to collapse.
- **The bench result**, named by which of the three wins it claims or that it claims none, with the
  arm costs and seconds — never a "we compared it to X and it did better" sentence with fewer than
  five arms.

Then the trial's honest state, the cost, and the pending list — items only he can do, each with the
prompt already written. Never ask him to decide something you can find out or do yourself; never
send him a question without your recommendation.

## 7. Improve this skill before you stop

REQUIRED: append to [lessons.md](lessons.md) (§8) what you learned, one dated line (Arman's own words go verbatim to the node's `VISION.md`), then
run `python3 common-docs/meta/scripts/sync_skills.py`, commit common-docs and every synced repo.
If a lesson changes a rule above, edit the rule — do not only append. Keep the body under 500
lines by relocating trial-specific detail into the trial's register.

## 8. Lessons (append, dated)

Every dated lesson from past trials — the Conductor, headless and cloud driving, draft review, CI and
access refusals, concurrent trials. **Before you choose a subject and again before you judge a run, call it
a success, or trust a verdict — read [lessons.md](lessons.md) end to end.** Also on a stop in your run,
headless or cloud driving, a draft pile, or §7; append new lessons there.
