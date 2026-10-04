---
name: campaign-pattern
description: "The doctrine for turning a vision into a finished, verified, deployed system with near-zero owner involvement. Use when launching, coordinating, resuming, or working any large build, module, campaign, or multi-agent project, or when writing its launch prompt."
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/campaign-pattern/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# The Campaign Pattern

**What this reproduces:** the HR-domain build — one vision message became a verified, deployed
production module in five days with near-zero owner involvement, surviving compactions,
disconnects, and usage-limit kills without losing a step. Worked example:
[`systems/human-resources/projects/hr-domain/PLAN.md`](/systems/human-resources/projects/hr-domain/PLAN.md) (its `COORDINATOR.md`, `EXECUTION.md`, `REGISTER.md`
templates are in git history under `projects/hr-domain/`, removed 2026-10-03). This doc is the recipe: **the owner's five launch moves** (Part 1), **the
coordinator's operating system** (Part 2), **the lifecycle with gates** (Part 3), and **the launch
protocol** (Part 4). Method skills carry the mechanics — this doc never restates them.

**The one-sentence version:** the owner spends his effort BEFORE the build, the coordinator
externalizes every piece of state so no session matters, and nothing is ever called done on the
word of whoever built it.

---

## Part 1 — The owner's five launch moves (this is where the magic actually was)

### 1. Assign a mandate with a theory of failure, not a feature list
The HR assignment's first paragraph named exactly what went wrong on prior rollouts
(*"insufficient upfront planning and poor compartmentalization... prevented us from maximizing
the capacity AI gives us"*) and prescribed the SHAPE of success, not the content: solid core
first (database), fully-resolved specs before any implementation (*"every page's behavior, each
feature's behavior, and every AI integration point fully defined in advance"*), then parallel
fan-out where server and client proceed independently *"because the APIs, data shapes, and flows
are already fully decided."* **Prescribe the process; let the agent derive the product.**

### 2. Demand discovery before design
The assignment ordered familiarization first: know what already exists — the live system as its
users meet it, the live database and its conventions — before designing anything; research the
best products in the world and pick one primary + one secondary reference (default set:
`policies/champions.md`); scope capabilities explicitly (what's IN, what's deliberately deferred).
The coordinator ran these as parallel zero-assumption recon agents whose reports went to FILES.
**Discovery is briefed so that it can return what the coordinator does not already know**
([reality is the referee](/policies/reality-is-the-referee.md)): the situation and the result
wanted, never the files to open, the words to search for, or the path to walk — a brief that
carries the answer is confirmation, and every later spec then stands on the coordinator's blind
spots. What the coordinator does know is withheld and used as the test of the report. The
coordinator has met reality itself — the product from the user's seat, the user's words verbatim —
before writing any brief; a brief written minutes after the vision arrives is the signature of the
disease, not of speed.

### 3. Order the adversarial review BEFORE commitment
Historical order: Arman asked for an independent reviewer to poke holes in plans before the team
proceeded. That order seeded the entire culture: from then on, every plan got attacked before it was
trusted, and every "done" got attacked before it was believed. Adversarialism was the OWNER'S
order, so no agent ever treated it as optional. (Mechanics: `plan-attack`.) Plan attackers run on Opus 5.5 (design judgment); verifiers of built work run on Sonnet unless the change is large or high-risk.

### 4. Rule the done-means-done law (the single most load-bearing message)
Verbatim, from launch: *"I don't want fake tests that take in fake data that the agents
manufacture to test their own work. All verification, testing, and validations must be done
independently of the agent who has done the work, and they must be done in a comparison of the
initial guidance documents and vision to the final production system, verified in the user
interface, with actual data... Features are only considered done when they are truly done."*
This became D15 — and it is why the campaign caught a live cross-tenant leak, a feature that had
never worked once, a dead engine, and a dozen lying screens that every builder had reported as
finished. **Without this law, the other four moves produce confident garbage.**

**Test data looks real or it is deleted** ([policy](/policies/test-data-looks-real.md)).

### 5. Answer through a defaults-carrying interview, then get out of the way
The final pre-build interview carried the team's recommendation on every item with the rule:
*"anything you skip ships with the stated recommendation as the platform default."* Only the
genuinely un-defaultable needed words (seven items). (Mechanics: `grilling`.) During the run,
the owner answered decision batches fast and decisively, taught PRINCIPLES instead of fixes
(org-scoping, knobs, platform primitives, package versioning), corrected focus bluntly when
needed (*"you are focused on the wrong things"*), and otherwise did not interfere.
**Trust, explicitly granted, is a mechanism: the coordinator never waited.**

## Part 2 — The coordinator's operating system (what the agent must do)

1. **Externalize everything; make yourself replaceable.** One register as the single tracking
   home (stable IDs; no parallel status docs; **an index, not a store** — a decision lives in
   its item and the register only points at it). The register opens with the owner's words
   verbatim and holds only decisions and reality-checked facts — each entry says how to check
   it against the live system; an item that changes nothing the user will see is suspect on
   sight, and a log line that changes no decision is not written. A register that records
   activity becomes the single source of lies every later lane inherits. Frozen specs. A rulings ledger. A log line for
   EVERY processed event, committed and pushed immediately — *unpushed work doesn't exist*. A
   `COORDINATOR.md` succession brief so any fresh session takes the chair with one sentence.
   This is why context wipes cost nothing: the head is a cache, the repo is the truth.
2. **Coordinate; don't build.** The chair dispatches fresh-context specialist agents with tight
   briefs (artifacts as file paths, never pasted history), adjudicates their findings, routes
   fixes, and flips register rows. Every brief passes down the laws (safety constraints, method
   laws, and the model ladder: every dispatch NAMES its lane and model — Sonnet the default
   worker, Opus with a stated reason (a large build, design judgment, a bug with no known cause;
   at most 2 at once), Fable only where the chair itself would struggle; every brief carries a
   "Done when" and a budget; workers never dispatch (only the `coordinator` lane can);
   effort medium unless the task needs sustained reasoning — `policies/subagent-model-ladder.md`).
   Every brief also carries the commit law verbatim: *"Commit locally, often, only
   with `git commit -m "<message>" -- <your paths>` — never push, never a branch or worktree;
   `./ship.sh` commits everything else in the checkout and pushes it live, constantly — that is
   the design, never a risk to report"* (`policies/shared-checkout.md`). **And, for any lane
   whose row names a build lock, the lease law verbatim: "Take leases only with
   `matrx-frontend/scripts/lib/lease.sh` — `lease.sh take <lock> <lane> <note>` / `renew` /
   `release`, or `lease.sh with <lock...> -- <command...>` to hold, heartbeat and release around
   a whole apply. Never hand-write the lock SQL: it is the same `campaign_watch.lock_take` /
   `lock_renew` / `lock_release` path `pnpm db:apply`, `pnpm db:rehearse` and
   `scripts/night/lib-night.sh` already call."* (lane LEASE-HELPER, 2026-09-23 — a hand-written
   lock query once read a column named `status` instead of `outcome`, always read "not held",
   and a lane applied to the branch twice with no lease held at all; nothing stopped it).
   Freeze contracts before fan-out so lanes can't collide; after the freeze a change is an
   amendment (register note + type regeneration), never a silent edit. **STEP ZERO
   before any lane scouts for unclaimed work: query `agent.review_queue` for the reviewable
   thing by name — never trust a fresh checkout's git state alone.** Confirmed 2026-09-12: a
   freshly cloned repo can come down materially behind `origin/main` through the session's git
   proxy, and a same-session `git fetch origin main` can silently re-serve that same stale ref —
   so "clone, fetch, then scout" still missed already-shipped work (surface write-targets for
   `quick-tasks` and others were rebuilt from scratch this way, twice). `git ls-remote --heads`
   under-reports too, because merged campaign branches are deleted. A direct row lookup in the
   queue by the target's name is the reliable dedup; treat a fresh git checkout as corroboration
   only, never as proof of non-adoption. **The ratchet:**
   a lane that discovers its task is bigger than briefed escalates the SHAPE (a ruling, a split,
   a lane up) — it never quietly shrinks the scope. Briefs, report statuses, the two-verdict
   review, the bounded fix loop, and the two rules that lose work outright — never end a turn while a
   background subagent is still running, and commit each unit as it lands rather than at the end:
   `subagent-dispatch` §1.
3. **Nothing flips on the builder's word.** A builder owes fresh evidence for every claim before
   handoff — that is the FLOOR. The BAR is independent, zero-authorship verification against the
   SPEC, on the deployed surface, with real identities driving real doors: verifiers try to BREAK
   things, pair every refusal-proof with a positive control that could fail, re-run every red
   before believing it, and state which build every verdict ran on. **A test that feeds
   manufactured data to its own author's code proves nothing and is filed as a defect.** Expect
   verdicts to be overturned in both directions; that is the system working. Reviewer findings are
   leads too: reproduce each on the current build, check it against recorded rulings, then
   CONFIRM, REFUTE with evidence, or RULE — ledgered as `Ruling: <decision> — <why> — <cost if
   wrong>`. Never pre-judge a reviewer's brief, never discard a finding silently, never fix a
   settled ruling away.
   **The battery — every campaign runs all five, and the plan names them:**
   - **Breadth sweep** — actuate EVERY control on every surface as every persona.
   - **Adversarial depth** — real non-member and anonymous identities through the real doors.
   - **Hostile re-verify** — every fix set re-attacked by someone who did not write the fix.
   - **Closing verifier + production sweep** — the held targets re-proven on the deployed SHA.
   - **The owner's own hands** — on the deployed surface; his phone catches what no agent can.
4. **Fix the class** (law 3, [the laws](/policies/the-nine-laws.md)): `diagnose` before any fix,
   guards per `forcing-function-tests`; a missing red-capable seam is itself the finding.
   **Type errors at any gate** (frontend `pnpm type-check`, `@ai-matrx/*`
   `pnpm typecheck`, dashboard `tsc`) are a fan-out under the frontend
   `type-safety` skill: one file per small agent, they never run `tsc`,
   they commit each assigned file locally with `git commit -- <file>` as they finish, the
   coordinator verifies centrally, at most six at a time. They are
   not a release halt and not a cast sweep.
5. **Bank lessons as laws.** Method traps (liveness oracles, session traps, seam classes) go into
   durable memory/docs the moment they bite, so they bite once. At each gate, and whenever a
   verifier overturns a builder, run a short retro and put each lesson where it bites cheapest:
   an automated check (best), a verifier-brief rule (the reviewer has the least context pressure —
   standards belong there), a navigation pointer, or a skill line. Delete steering text that
   changed no behavior.
6. **Rulings, not stalls — and route honestly.** A running lane never waits on a human. **Only
   four things stop a lane:** an irreversible or destructive act on real data; a security-sensitive
   change (grants, secrets, tenant boundaries) outside its brief; a side effect the owner reserved
   (money, external accounts, messaging real people, new schedules, a release); or a plan so broken
   that every path is a guess. Everything else is a ruling: decide it, ledger it with its cost if
   wrong, keep going — a wrong ruling costs visible rework; a parked lane costs the day. Agent-doable
   work never reaches the owner; **and the reverse holds: an agent never answers on the owner's
   behalf a question that is genuinely his** (vision, money, brand, legal, deleting real data). What
   reaches him: finished work to see, and genuine questions through [ask-arman](/skills/ask-arman/SKILL.md),
   while the lane proceeds on its stated reversible default. **At every close, the exhaustive list
   of rulings made in his absence**, each with its cost if wrong. A
   ruling that dies with the session was a decision made in secret.
7. **Survive on purpose.** Self-scheduled wake-ups as disconnect insurance. Recovery-first
   resumes: after any compaction or restart, regenerate and re-read the owner's own words FIRST (`user-ground-truth` — the compaction summary is a paraphrase and the register is a model), then trust the register + `git log` + origin content,
   never recollection — **re-dispatching finished work is the single costliest failure**, and a
   `Done` row is never re-run. Work products — not transcripts — are the liveness oracle for
   sub-agents; never relaunch-on-suspicion an agent holding real-state authority. Waiting is work:
   bounded stretches, reconcile live children between them, chase any that finished without
   reporting. In a shared checkout, touch only what you created — never remove another lane's
   worktree, stash, or files, and never `--force` a refused removal.
8. **A delta is not a status** (law 8, [the laws](/policies/the-nine-laws.md)).

## Part 3 — The lifecycle: gates with exit criteria (the spine that makes it reproducible)

Each gate's exit is checkable; a campaign that skips a gate is the failure mode Part 1 §1 named.

| # | Phase | Exit criterion |
|---|---|---|
| 0 | **Mandate** (owner) | The mandate names the vision, the theory of past failure, the process shape, and the done-means-done law (Part 1 §1, §4). |
| 1 | **Discovery** | The owner's words exist as a ground-truth file with a fresh summary beneath (`user-ground-truth` skill) and the register opens with them. Parallel recon agents (lanes named) have written to files: what already exists, found from the user's seat and verified against live code/DB, the champion for each discipline named with why it is the reference (`policies/champions.md` — parity is the floor), capability scope IN/DEFERRED — every load-bearing claim verified, not asserted, and every report checked against what the coordinator withheld (a report that misses what the coordinator already knew is discarded, and the brief is rewritten). |
| 2 | **Scope + attack** | A feature tree / scope list exists; a zero-authorship `plan-attack` has run; every finding adjudicated (FIX / REJECT with reason / OWNER-ONLY). The register is opened as the single tracking home; questions that are sharp-but-blocked are items, questions not yet phrasable stay named **fog** (never pre-sliced into fake items), and work past the destination is **out of scope** — closed with one line, never "deferred" back onto the frontier. |
| 3 | **Interview + readiness** | Each lane's readiness doc front-loads its unknowns and resolves what it can itself; the coordinator runs the residue through the `ask-arman` gate, then ONE `grilling` interview in rounds. A question that exists only because the owner is also a customer of one organization is the user's, not the boss's — it becomes an onboarding step or a knob, never his question. Exit: the frontier is empty (answered, decided-with-override, or deferred with a date). **After this, no lane ever stops to ask the owner** — a new unknown is a coordinator ruling. |
| 4 | **Freeze (G1)** | A fresh judge has read the owner's words and the plan and gone to the live product as him, and reports no drift (`user-ground-truth` §3). Specs, contracts, types/mocks, and fixtures are frozen and hashed; the core schema is certified. From here a contract change is an amendment (changelog + register note + regeneration), never a silent edit. |
| 5 | **Core** (serial) | The single critical-path core lands and certifies in order — never parallelized. |
| 6 | **Fan-out** (parallel) | Lanes dispatched with exclusive file/schema ownership and frozen interfaces; shared inputs verified to exist BEFORE parallel dispatch (a bad ref fails here, not inside six agents). |
| 7 | **First vertical (G2)** | One org runs one end-to-end path in production shape with real non-admin users — before the remaining lanes merge their surfaces. |
| 8 | **Verification + defect rounds** | Per lane: D15 — explicit targets (a real user action on a real surface, never "tests pass") proven by a zero-authorship verifier on the deployed surface with real data, briefed with the owner's words and the outcome — never the builder's file list or path (a verifier that inherits the builder's frame is the builder's hands); conformance gates green; a review-queue row filed; reopen-on-fail is normal. The five-pass battery has run and the plan names each pass: breadth sweep, adversarial depth, hostile re-verify, closing verifier + production sweep, owner's own hands (Part 2 §3). Defects are fixed by class (Part 2 §4), never by instance. |
| 9 | **Close (G3)** | The closing report to the owner is what he will see doing what he described, with the ground-truth judge's last verdict beside it. Every target Met on independent evidence and confirmed LIVE (deploy trains carried it; verify the deployed SHA, never the pushed one); the rulings list delivered to the owner; the retro banked (Part 2 §5); handoffs deleted, register and docs groomed; residual follow-ups filed where they'll be seen. |

## Part 4 — Launching one (the owner's copy-paste protocol)

1. Write the mandate: the vision, the theory of past failure, and the process shape (core →
   frozen specs → parallel fan-out → independent verification). Name what "done" means using
   the Part 1 §4 language verbatim.
2. Tell the agent to run discovery first (what exists, from the user's seat + market reference + scope), then
   bring the scope list — and order the hole-poking review on it (`plan-attack`).
3. Answer the defaults-carrying interview one round at a time (only un-defaultable items need
   words — skipping ships the default).
4. Say the sentence that grants the chair: *"You own this end to end. Make yourself
   replaceable, keep everything in the register, and only bring me finished work and real
   decisions."* Approve the standing wake-up/schedule if offered.
5. During the run: answer each round fast, teach principles not fixes, test with your own hands
   when asked (the owner's phone caught defects no agent could) — and let it run.

## Deliberately not adopted (benchmarked 2026-09-10 against mattpocock/skills and obra/superpowers)

- **A worktree per lane / merger subagents** — rejected by `policies/shared-checkout.md` ("the
  worktree is a tool, not a home"): held-back code goes stale and the deploy train builds `main`.
- **Diff-only review as the definition of done**, self-run test suites as closure, the TDD
  delete-and-restart ceremony, one-ticket-per-session, and human approval gates on every path —
  each contradicts done-means-done or near-zero owner involvement. Their clarity mechanisms were
  taken; their model of who owns correctness was not.
