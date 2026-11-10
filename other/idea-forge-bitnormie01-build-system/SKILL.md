---
name: idea-forge
description: >
  Use this skill at Step 0 of a hackathon build — BEFORE the architect — when the builder has a blank
  start and needs to go from "I want to build something for <hackathon>" to ONE scoped, shippable
  project idea. It diverges (generates many varied candidates), then converges on an external,
  event-tied weighted rubric to a single committed brief, and hands that brief to the architect in the
  exact format it ingests. Trigger it when the user says "help me come up with a hackathon idea",
  "what should I build for <hackathon>", "I need a project idea", "brainstorm hackathon ideas", "pick
  an idea for this hackathon", or shows up with a theme / sponsor tracks but no project yet. Do NOT use
  it once an idea is already chosen — that's the architect's job. The architect shapes an idea you
  have; this skill invents the idea you don't.
---

# Idea Forge — Step 0: blank start → one scoped hackathon brief

## What this is

Idea Forge is **Step 0 of the build pipeline — upstream of the architect.** The architect shapes an
idea you already have into a spec; Idea Forge invents the idea you don't. It takes a builder from a
blank start to **exactly one scoped, shippable hackathon project**, then hands that project to the
architect in the format it ingests — so Step 0 feeds Step 1 with zero reformatting.

Three moves: **diverge** (many varied candidates) → **converge** (score on an external, event-tied
rubric and commit to one) → **hand off** (emit one brief the architect can run).

**Announce at start:** "I'm using the idea-forge skill to take you from a blank start to one scoped,
shippable hackathon brief."

## The one output

One **brief** — never a list. A ranked shortlist is an intermediate artifact you pass through on the
way to the answer; it is never what you deliver. If you find yourself ending on "here are 3 ideas,
which do you like?", you have failed the skill. Drive to one.

## Step 1 — Elicit the inputs (before generating anything)

Ask these **one at a time**, multiple-choice where you can, and do not generate a single candidate
until you have all five **required** inputs (1–5). They set the rubric weights and what counts as
buildable here. Input 6 is **optional** and never gates generation.

**If a resource pack exists** at `docs/resources/<event>/` (produced by `resource-extractor`, Step 0a),
sync the project repo (the kickoff's `REPO:` — `../references/repo-bootstrap.md`) and read it FIRST —
it is your primary, pre-verified source. Its `event.md` (published
judging criteria + weights), `tracks.md`, and `prior-art.md` satisfy inputs 1, 2, and 6 directly, so
confirm those back from the pack instead of re-fetching, and use its `sponsors/*` and `seeds.md` as
accurate divergence fuel and feasibility grounding. Only fetch or search live for what the pack doesn't
cover. With no pack, run the inputs below as normal.

1. **Hackathon + URL** — which event, and its rules / judging page. Read it; the published judging
   criteria drive the rubric in Step 3.
2. **Target tracks** (max 3) — which sponsor / prize tracks to aim at. More than 3 splits focus.
3. **Team / build capacity** — who actually builds this. Default: an autonomous multi-agent pool
   (architect → executor pool → reviewer) plus the builder, which builds far faster than a solo human
   typing. This is *not* an hours budget — idea-forge does not ask for or reason about a deadline;
   whether the chosen idea fits the calendar is the builder's call later, outside the skill.
4. **Builder skill set** — e.g. Solidity/DeFi, TypeScript/React, Python/ML. Candidates must be
   buildable by *this* builder, not a hypothetical team.
5. **Risk appetite** — `safe-feasible` (a clean, certain demo) vs `novel-wow` (a bolder swing). This
   nudges the Novelty/buildability balance within the rubric, never past intrinsic buildability — a
   bolder pick must still reach a real working demo with no external blocker.
6. **Prior art (optional)** — links or descriptions of existing / past projects in this space: prior
   hackathon winners (e.g. past Sui Overflow / Walrus / DeepBook winners), shipped ecosystem projects,
   sponsor showcases, or specific projects the user pastes. Consulted **only at Step 3** to sharpen the
   Novelty score against the white space — it does **not** seed or gate divergence. **When the
   session has web access, don't wait to be handed it:** spend ONE bounded search pass — past winners
   of this event series, the sponsors' showcase / "built on X" pages, obvious shipped competitors —
   and treat whatever it yields as this input. One pass, then move on. If the user gives none and the
   pass finds nothing useful, **skip the prior-art steps and run the normal flow** — never block,
   stall, or invent competitors.

If the user pre-supplied these (e.g. via `../prompts/INVOKE_IDEA_FORGE.md`), confirm them back in one
line and proceed. **In an autopilot campaign** (your kickoff carries an `AUTOPILOT CAMPAIGN` block
— `../references/campaign-contract.md`) the locked contract supplies inputs 1, 2, 4, and 5 the
same way — confirm-and-proceed, no interrogation — while input 3 keeps its kit default (the
autonomous pool + the builder), and the contract's BUDGET field binds Step 3's gate below; an
input the contract leaves open ("idea-forge decides within contract") is yours to decide and
record.

## Step 2 — Diverge (quantity and variety first, no filtering)

Goal: a wide, varied candidate field. Do not judge yet — judging now kills variety.

1. **Load seeds.** For a Web3 event, load `../references/web3-seed-pack.md` (a16z Big Ideas + ETHGlobal
   track archetypes). For a non-Web3 event, build an equivalent seed list from the event's own theme,
   its sponsor list, and current trends in the builder's domain. Seeds are spark material, not ideas.
   **The pack is a dated snapshot — the floor for variety, not the ceiling:** when web access exists,
   augment it with the current quarter's narratives (the event's own announcements, the sponsors'
   latest releases) before generating.
2. **Generate ≥20 candidates.** Cross seeds × target tracks × the builder's skill set. Each candidate
   is one line: *problem → solution → the demo moment*. Force the quantity; reach past the obvious
   first five. Cover several distinct seeds — not 20 variations of one idea.
3. **Bolder-pass (the diversity move that actually works).** Take the ~8 most generic / me-too
   candidates and **rewrite each to be bolder and more demo-able** — sharper problem, a surprising
   mechanism, a clearer "money shot" a judge would remember. Keep both versions in the field. This
   chain-of-thought "make it bolder" rewrite is the measured-diversity step; do it every run.

Output of Step 2 is the **full candidate field (≥20)** — still unranked.

## Step 3 — Converge on the external rubric (never on preference)

Score **every** candidate with `../references/ideation-rubric.md`. Do not pick by taste, and never ask
"which do you prefer?" — the rubric is the decider.

- **Buildability gate first.** Drop any candidate that can't reach a *real, on-chain working demo*
  because of an **external blocker the builder doesn't control** — missing data, a third-party approval
  / KYC, a service / oracle / indexer you can't run, a human-in-the-loop, a deploy you can't perform, or
  a money shot riding on live external markets. Knockout, before scoring — an un-demoable idea is out,
  however brilliant. Build *speed* is not the test (the agent pool builds fast); external *blockers*
  are, so an ambitious-but-buildable idea passes. **Budget knockout:** when the campaign's locked
  BUDGET is `$0` (`../references/campaign-contract.md` §Budget), a candidate whose real demo
  requires any paid resource — a paid API tier, paid RPC, paid dataset, paid hosting — is out at
  this gate too; free tiers, faucets, and testnet must suffice end-to-end.
- **White-space check — only if prior art was provided or found** (after the gate, feeding the score
  below). Map each surviving candidate against the prior art and classify it: *duplicate* (substantially
  an existing project), *incremental* (a marginally-better clone — treat as weak), or *white-space* (an
  unoccupied angle, novel combination, or missing wedge). This is a **differentiation** call, not a
  "make it nicer" one: steer toward the unoccupied angle, never toward a slightly-better version of
  something already shipping — that re-introduces the me-too trap the bolder-pass exists to kill. Feed
  the verdict into the **Novelty axis only**: duplicates and incremental clones score LOW, genuine
  white-space scores HIGH. Do not add an axis or change the weights — prior art replaces Novelty
  guesswork with evidence. Buildability still leads: a white-space idea that isn't demoable loses to a
  buildable one — differentiation informs Novelty, it never overrides the buildability gate. **If no
  prior art:** note "no prior art available — scoring Novelty on first principles" and proceed — no
  stall, no invented competitors.
- **Judge's-eye head-to-head — only if prior art was provided or found** (layers on the white-space
  check; both run, in order — and although listed here, this step *executes after* the **Score the
  survivors** step below, on its top 2–3, then feeds the verdict back into WOW + Novelty + Fit). Once
  the weighted score below ranks the survivors, take the **top 2–3**
  and simulate a judge scoring each against the **strongest 1–3 prior-art projects** on the **event's
  actual published criteria** (read them off the rules page; for demo-first events: working-demo
  strength, genuine on-chain / Sui-stack usage, usefulness, "wow"). Per decisive criterion, state **win
  / tie / lose vs. the best prior art, with the specific demonstrable reason** (e.g. "wins on demo: our
  money shot is a live on-chain tx vs. their mocked UI"). A candidate advances as winner only with a
  defensible **win on ≥1 decisive criterion AND no clear loss** on the rest. **Evidence-bound, never
  grandiose:** a "we win" claim counts only when it names a concrete edge on a real axis — no vague
  superiority, no "10× better", no puffery; if a candidate can't honestly claim an edge, switch to a
  *different* candidate rather than inflate it. **A field whose best can only tie is not winning** — go
  back to the candidate pool for a stronger one before committing. Feed the verdict back into the
  existing **WOW + Novelty + Fit** scores (a head-to-head loser drops even with high raw Novelty; a
  clear evidence-bound winner rises) — **add no new axis**, and it **never overrides the buildability
  gate**: an idea that wins on paper but isn't demoable, or needs something the builder doesn't control,
  still loses. **If no prior art:** skip this (as with white-space), score on first principles, and say
  so — no fabricated competitors, no invented "we beat them" claims.
- **Score the survivors** on the weighted rubric. Default weights (adapt to the event's *published*
  criteria, but keep buildability highest):
  **Intrinsic buildability 35 · Demo WOW + story 25 · Theme + sponsor-track fit 20 · Novelty 20.**
  Buildability leads on purpose: an LLM's novelty edge erodes once an idea is actually built (the
  Ideation–Execution Gap), so a demoable idea beats an un-demoable brilliant one. Buildability is about
  external blockers, not human-hours — the agent pool builds fast, but it can't conjure missing data or
  approvals.
- **Pressure-test the top 3** for hidden *blockers* — the un-obvious dependencies that make a demo
  impossible, not the ones that just take time: external approvals / API keys you can't get, data you
  don't have, a model you can't train, a service / oracle / indexer you can't run, anything needing a
  human in the loop. Re-score on buildability if a blocker surfaces — never on hour-counting (sheer
  amount of work isn't a knockout).
- **Commit to the winner.** One candidate. If two tie, the higher buildability score wins.

The ranked table is an intermediate; the moment you have a winner, drop the list and write the brief.

## Step 4 — Commit to one brief and hand off to the architect

Write the winner as a single brief with **all** of these fields (no placeholders):

- **Problem** — who hurts and why, one or two sentences.
- **Solution** — one line.
- **Must-have demo features** — 2–3, the minimum that makes the money shot land.
- **Target sponsor track(s)** — from Step 1.
- **Judging criteria (published)** — the event's actual rubric/weights, read off the rules page
  (e.g. "Real-World Application 50% · Product & UX 20% · …"). The architect and the demo plan
  optimize against these downstream; a brief without them forces the next stage to re-research the
  event.
- **Why it wins / Why it's novel** — *with prior art*, title it **"Why it wins"** and name **both** the
  white space (the gap: "unlike <existing project / category>, this …") **and** the head-to-head edge on
  a real judging axis ("vs. <strongest prior art>, ours wins on <criterion> because <demonstrable
  reason>") — one or two **evidence-bound** sentences, no grandiosity. *Without prior art*, title it
  **"Why it's novel"** and give the first-principles novelty claim, as before.
- **Demo money shot** — the single ~15-second moment the judge will remember.
- **Out of scope (explicit)** — what you are deliberately NOT building, to keep the build focused on the
  money shot.
- **Feasibility notes for the architect (primitives, not design)** — the concrete build facts the
  architect needs, transcribed **verbatim** from the resource pack's `sponsors/*` when it exists (or
  your own research): testnet package / contract / object addresses, entry-point signatures, the
  integration model (branch, SDK, codegen), and the one external dependency to request on day 1.
  Facts, not design. Omit only if the build touches no sponsor SDK/protocol — this section is what lets
  the architect plan without guessing interfaces (see the reference brief's section of the same name).

**Write the brief to `docs/idea-forge/<YYYY-MM-DD>-<slug>-brief.md`, then commit and push it, BEFORE
you offer the hand-off.** Mandatory on a real run: the architect boots in a *fresh session* and syncs
the canonical repo before reading anything (the repo is the single source of truth), and the kickoff
block's `DOCS:` points at this exact path. If the brief is only written to a local file and not
pushed, the architect's first move — reading the brief from the synced repo — fails. So: write the
file, then `git add` + `git commit` + `git push` it to the canonical branch, *then* offer the block.
Writing to disk is not enough; local files are never trusted — the same two-sided repo rule every role
in this kit runs on.

**The repo you push to is the project repo — and this is the step that names it**
(`../references/repo-bootstrap.md`). The winning brief is the moment the project gets a name, so:

- **Step 0a ran and created an event-named repo** (`<event-slug>-<YYYY>`): right after pushing the
  brief, upgrade it — `gh repo rename <project-slug> -R <owner>/<event-slug>-<YYYY> --yes`, then
  `gh repo edit <owner>/<project-slug> --description "<the brief's one-line solution>"`, then
  `git remote set-url origin <new URL>` — and state the new name so the guide records it in the
  runsheet. Always pass the explicit `-R <owner>/<repo>` target: the bare form resolves the repo
  from the cwd's origin, and run from the wrong directory (the kit checkout) it would rename
  **build-system** with `--yes` suppressing the confirmation. (Skip the rename if the user provided
  the repo themselves — only pipeline-created repos get renamed.)
- **No project repo exists** (Step 0a skipped): create it now, project-named —
  `gh repo create <project-slug> --private --description "<one-line solution>" --clone` — and commit
  the brief there. Never commit the brief into the build-system kit checkout.

Then **offer the hand-off**: "Hand this to the architect?" and emit the kickoff block below, filled
from the brief. **Paste it into a new, fresh session** — opened at the architect's session
settings (`../references/model-routing.md` §Seat settings; `../prompts/INVOKE_ARCHITECT.md` shows
how to set them) — **the architect does not continue this conversation**; it plans from the
committed brief as the single source of truth, with a clean context window (not from idea-forge's
divergence noise). This is the exact shape `../architect/SKILL.md` Stage 1
and `../prompts/INVOKE_ARCHITECT.md` ingest, so Step 0 feeds Step 1 with no reformatting:

```
SESSION SETTINGS: tier top · effort xhigh, or high for a one-task plan-bug fix
(references/model-routing.md §Seat settings). Start by stating the exact model id you are running
as. If it is below this campaign's top-tier binding, warn me and wait for my go before anything
else. (In an autopilot dispatch, just state it — the autopilot logs drift.)

You are the ARCHITECT for this build. Load and follow architect/SKILL.md (and its references/).
Do not write product code. Your only deliverables are: an approved spec, executor-ready plan
documents, docs/superpowers/manifest.json, and the pre-filled docs/gates/submission-draft.md
(build-time facts marked TBD-post-build).

PROJECT: <one-line solution>

REPO: <owner>/<project-slug> — the project repo (canonical; sync it before reading anything)

DOCS: docs/idea-forge/<YYYY-MM-DD>-<slug>-brief.md, docs/resources/<event>/ (the resource pack, if extracted), <hackathon URL>

CONSTRAINTS: <chain/platform>, <language/runtime + versions implied by the skill set>, hard deadline
<hackathon end — absolute date/time; builder fills this in, idea-forge did NOT gate on it>, team =
solo + AI. Target track(s): <tracks>. Must land the demo money shot. Out of scope: <out-of-scope list>.

EXECUTION TARGET: built in Claude Code by the orchestrator — the main session dispatches a fresh
subagent per task (orchestrator/SKILL.md). Every task must be self-contained per
references/task-contract.md — paste upstream signatures into each task, declare Provides/Requires, and
give exactly one gate command per task. Hand off at the reviewed plan + manifest (the default —
omit the manifest only when the build has no deploy/key/fund tasks) and the
orchestrator builds it. (For an external multi-account pool instead, stop at the manifest for a kernel.)
```

## Hard guardrails

- **Strongest model only.** Rubric mapping and buildability judgment are model-bound. Run idea-forge on
  your top reasoning seat (tier `top`, at its §Seat settings effort —
  `../references/model-routing.md`). Never let a cheap executor run it — a weak model mis-maps
  the rubric and mis-calls buildability *silently*, and a mis-weighted rubric still produces a
  confident-looking brief. This is the skill's top residual risk.
- **One brief, never a list.** A ranked list is an intermediate only. The deliverable is one scoped
  brief. Ending on a menu is a failure.
- **The rubric decides, not taste.** Converge on the external, event-tied rubric with buildability
  weighted highest — never on model self-preference or "which do you like?". Models over-rate their
  own novelty; the rubric is the correction.
- **Intrinsically buildable is a wall.** An idea is out if it can't reach a real on-chain working demo
  because of an external blocker the builder doesn't control — missing data, a third-party approval /
  KYC, a service or oracle you can't run, a human-in-the-loop, a deploy you can't perform, or a money
  shot riding on live external markets — however winnable. Build *speed* is not the constraint;
  external *blockers* are. Enforce the buildability gate before scoring.
- **No secrets, ever.** No private keys, mnemonics, or secret values appear in any candidate, brief, or
  hand-off — only env-var names. (Same rule the rest of the kit runs on.)
- **Hand off, don't build.** Idea Forge stops at the brief + kickoff block. It does not spec, plan, or
  code — that's the architect and the pool downstream.

## When NOT to use this skill

- You already have the idea — go straight to the architect.
- You're past ideation and need a spec, plans, or code — that's architect / executor.
- Not a hackathon-style, demo-judged build — the buildability-first rubric is tuned for "land a real
  working demo a judge verifies" and will mis-weight open-ended product work.

---

*Original instructions, informed by two MIT-licensed sources: the forced-quantity, multi-lens
divergence of `phuryn/pm-skills` → `brainstorm-ideas-new` (MIT © 2026 Pawel Huryn) and the
feasibility-gated, demo-first convergence of `davila7/claude-code-templates` →
`hackathon-ai-strategist` (MIT © 2025 Daniel (San) Ávila). No substantial passages are reproduced;
the divergence/convergence design and rubric weights are this kit's own.*
