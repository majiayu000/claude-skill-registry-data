---
name: vision-to-fleet
description: "Pipeline that turns a big system idea into briefs for an agent fleet. Use when Arman says 'let's plan out X', 'build or overhaul the X system', 'create the vision and plan for X', 'do the full discovery process', 'get this ready for a fleet', or 'do what we did for education', or when carrying forward a VISION, COMPETITIVE_INSIGHTS, roadmap, or briefs doc. NOT for one feature in a live system (use build-sub-feature)."
---

# Vision → Fleet: the discovery-to-execution pipeline

The paved road from "Arman has some ideas about X" to "N agents are building X in parallel from
briefs they can execute blind." First run: the Education Hub (2026-06/07) — its converged
record, including what went wrong the second time around, is
`common-docs/systems/education/STATE.md`; every template referenced below names a live
worked example in `references/templates.md`.

**The one-sentence job:** produce documents so good that a capable agent, handed one brief and
the repo, ships the right thing without ever talking to you — and keep every document truthful
at every step along the way.

Phases run in order, but this is a pipeline you can enter mid-stream: figure out which artifacts
already exist (vision? insights doc? briefs?), verify them instead of trusting them, and continue
from there. Templates for every artifact: [references/templates.md](references/templates.md).
Research mechanics: [references/research-playbook.md](references/research-playbook.md).

**Not this skill:** a single feature inside a live system → `build-sub-feature`; auditing one
existing feature → `feature-deep-dive`. This one is system-scale work that ends in many parallel
agents.

---

## Cross-cutting laws (apply in every phase)

1. **Ground everything in the live system.** Claims about code cite file paths; claims about
   data cite live row counts (Supabase MCP `execute_sql`). A doc claim older than a few days is
   stale in this repo — many concurrent sessions land on main daily. Re-verify before building
   on anything, including your own earlier docs.
2. **Compare the code to the vision, never the vision to the code.** The project exists because
   the current approach isn't working. The current implementation is *evidence of what exists*,
   never evidence of what was intended — especially where it violates best practices. When code
   and vision disagree, the default is the code is wrong; confirm with Arman only when the
   evidence genuinely cuts both ways.
3. **Decisions are Arman's; asking is your job; burying is a failure.** Product-semantics calls
   (what's free, what a hierarchy means, what enters the vision) go to him DIRECTLY in your
   reply as plain numbered chat text — **never a structured question picker** (Arman ruled
   2026-09-12): numbered, one line of background, ONE direct question, plus the best practice and
   your recommendation, or an explicit "this one is open-ended".
   Never leave a decision as a "flag" inside a document he'd have to dig for. Ask via the
   `grilling` skill.
4. **Every doc is versioned truth.** Each artifact gets a status date, a changelog, and — when
   superseded — a loud pointer to what replaced it. When a decision lands, write it back into
   the doc that raised it (see the education master plan §8: flags become DECISIONS RECORDED).
   Stale docs corrupt every future agent's mental model.
5. **Fleet-aware git hygiene.** Other sessions ARE working on main right now. `git status`
   before every commit; stage only your files by explicit path; expect (and tolerate) your work
   riding in others' commits and vice versa — small commits, never lose work, never stash
   someone else's.
6. **This is an AI-application company.** In every phase, "where do agents plug in" is a
   first-class design question, not an implementation detail — which surfaces get an authored
   agent, what context it receives, what it returns (structured, cited), how it streams.

---

## Phase 0 — Intake

Arman brings ideas: a paragraph, a rant, a competitor screenshot, or a half-written doc.
Extract: the domain, the ambition level, what he believes exists already, and what triggered
this now (the trigger usually reveals what's broken). Classify:

- **Brownfield (usual):** significant parts exist somewhere in the codebase → Phase 1 and
  Phase 2 run in parallel.
- **Greenfield (rare):** nothing exists → Phase 1, then straight to Phase 3.

Ask the scoping questions NOW, in one batch (they shape everything): who is this for, what does
winning look like, what's explicitly out, and — critical for Phase 3 — *what function is this,
really?* (see the benchmark rule below).

## Phase 1 — Vision capture

Draft the VISION document — the single most load-bearing artifact; everything downstream cites
it. Follow the education example's register (`app/(core)/education/VISION-education-hub.md`):
**capability voice, not aspiration voice** — "the platform generates X" not "we hope to build X"
— covering: who it serves (segments table), the core feature set (numbered sections, one per
pillar, dense bullets), platform architecture status table (✅ live / 🔲 roadmap — honest),
coming-soon, competitive landscape table, and "Why We Win" numbered differentiators.

- Write it where the feature lives (e.g. `app/(core)/<area>/VISION-<area>.md`) and register it
  as the source of truth in whatever plan docs follow. Avoid mirrors; if one must exist, note
  the sync obligation in both.
- **Review is progressive, not terminal.** Show Arman the skeleton + pillars early; checkpoint
  again after research changes it (Phase 4). Never let a large vision diverge silently from
  what he'd endorse.

## Phase 2 — Reality audit (brownfield)

Produce the current-status summary that every later claim rests on. Method that worked:

1. Fan out parallel **Explore** agents, one per suspected subsystem, each with a precise
   question sheet ("is X still a stub? which of these six items shipped? what does the
   uncommitted diff in Y do?"). Ask for file paths in every claim.
2. Yourself, in parallel: live DB truth — `information_schema` sweep of the relevant schemas
   with row counts; sample ambiguous tables. **Row counts are gold**: "table exists, 0 rows,
   queried nowhere" is a completely different fact from "table exists."
3. Chase every anomaly to a verdict. A mystery table (education's `quiz_sessions`) gets its
   columns read, its data dated, and its writers grepped — until it's *resolved*, not flagged.
4. Check git motion since any prior audit: `git log --since=<date> -- <paths>`. In-flight work
   by other agents becomes an explicit "owned elsewhere — do not absorb" list.

Output (section in the plan doc, not a separate file): **DONE** (real, verified — the assets to
build on), **IN FLIGHT** (owner named), **MISSING** (what decomposition will cover), plus
resolved-anomalies and open flags. Also fix trivial drift you find (a stale "coming soon" label)
in the same pass — leaving known-wrong metadata is negligence.

## Phase 3 — Competitive research

Full mechanics: [references/research-playbook.md](references/research-playbook.md). The
essentials:

- **Benchmark against the best at the FUNCTION, never against AI-engine peers** — the rule and
  the competitor-selection method are `references/research-playbook.md` step 1; the standing
  champion set is `common-docs/policies/champions.md`. Getting this framing wrong invalidates
  the whole phase.
- **~8–10 parallel deep-research passes, one per competitor/cluster**, each mining real user
  sentiment (Trustpilot, app-store reviews, Reddit, G2, feature boards, news, academic papers,
  regulatory records). What do people LOVE, what do they HATE, what did the company fumble.
  Cited claims only; self-reported marketing numbers flagged as such.
- **Visual capture (was missed on education — do not skip again):** browser-agent passes that
  screenshot each competitor's key flows (onboarding, the hero feature, paywall, empty states)
  into a `research-assets/<competitor>/` folder with an index. These feed the design step.
- **Design pass (also previously missed):** for every surface the plan will build, a design
  direction informed by the screenshots — what the best-in-function get right visually, what we
  adopt/reject — so build-phase agents inherit direction instead of inventing it. Use the
  ui-* / web-design skills.

Synthesize into a `COMPETITIVE_INSIGHTS_AND_REPRIORITIZATION.md` (template in templates.md):
strategic thesis first, ranked market wants with signal counts, per-competitor
nails/hated-for/one-thing-to-take table, cross-cutting themes, then **proposed vision
elevations/additions clearly marked FOR APPROVAL** — research never edits the vision by itself.

## Phase 4 — Vision ratification

Take the proposed elevations/additions to Arman **directly** (law 3) — one question set, clear
options, recommendation marked. On approval, amend the vision **in place, in each item's home
section** (merge, don't append a "research findings" appendix), update mirrors, changelog it.
Deferred items get *documented deferral* — a real brief marked "Wave 2, do not assign" (see
`W2-class-hub.md`) — because "later" without a document means "forgotten."

## Phase 5 — Infrastructure groundwork

Before decomposing, decide the platform layer so N agents don't invent N solutions:

- **Data model:** the canonical content-model pattern per entity family (base columns,
  associations edges, visibility, RLS via the canonical generator, registry entries). New
  tables go through the `db-change` skill family. Name the pattern-reference implementation
  each brief should copy.
- **Server/client split per the data-flow doctrine (CLAUDE.md):** browser ↔ Supabase direct for
  all pure data ops; Python only for real server needs (bytes, signing, heavy compute,
  auth/anon boundaries). Every brief states which side each piece lives on; cross-repo
  (aidream) work is *part of a project*, never a follow-up ticket.
- **Agent integration points (law 6):** enumerate every AI touchpoint; each becomes "author
  agent via agent_author → wire via the launch/streaming pattern" work inside some brief, with
  the agent-spec doc named.
- **Day-1 contracts:** identify every interface where two projects would otherwise block on
  each other (access gates, entitlements, trust envelopes, converters, data contracts). Each
  gets an owner, a typed signature, and the rule: **publish the signature (stub if needed) on
  day 1** so consumers wire call sites immediately. This is what makes full parallelism real
  instead of aspirational.

## Phase 6 — Decomposition into briefs

The milestone deliverable: a briefs folder (`docs/proposals/<area>-projects/`) containing a
MASTER PLAN (README.md), one brief per project, an ASSIGN.md prompt, and F-addenda for agents
already in flight. All templates + the sizing rules: [references/templates.md](references/templates.md).

Sizing rules (Arman's, verbatim in spirit): each project is a **substantial, coherent body of
work** — a full subsystem or vertical slice, never a task list; prefer **fewer, larger**
projects (merge anything knockable-out-quickly into a neighbor); **maximize parallelism** by
pushing every cross-dependency into a Phase-5 contract. Small tasks → one agent overseeing a
group; large tasks → one agent each. Work already owned by a live agent goes in an **F-addendum**
to that agent, with hand-offs in/out stated explicitly. **Split test:** split two pieces into
separate projects only where a reviewer could reject one while approving the other; fold setup,
config, scaffolding, and docs into the project whose deliverable needs them.

A wide refactor (one mechanical change across many callers) is sequenced expand → migrate in
batches → **contract**. The contract project is mandatory, blocked by every migrate batch, and in
the same wave; never "later".

Every brief must pass the blind-handoff test: *could a strong agent with only this brief + the
repo ship the right thing?* If any section makes you think "they'll figure it out," it fails.
The test is **run by a fresh reviewer per brief plus one cross-brief contracts reviewer via
`plan-attack`**, never by the brief's author, before remaining flags go to Arman. A brief
**fails automatically** if it contains TBD/TODO, "handle edge cases", "add appropriate error
handling", "similar to P<n>", or a name or type defined in no brief or contract.

Before assignment, write the collision table into the master plan: one row per pair of briefs that
share a file, table, or interface (what one produces vs. what the other consumes → the Phase-5
contract that settles it), and one row per brief checking it agrees with itself (tests it demands
vs. code it specifies). "No conflicts" without the rows is not a scan you ran.

Map **convergence points** (integration milestones with their own DoD), **fan-out** (what each
convergence unlocks), and **waves** ordered by vision impact. Then surface every remaining flag
to Arman directly (law 3), record his answers back into the docs, and commit.

## Phase 7 — Assignment & fleet operations

- Arman assigns via ASSIGN.md's copy-paste prompt — fresh session per project; F-addenda go to
  the owning agent's existing session. Track assignment state in ASSIGN.md's table.
- While the fleet runs, the master plan is living: decisions recorded, contracts updated when
  an owner ships the real thing, kickoff addenda added when concurrent work lands on a brief's
  turf (see P7's share-links addendum for the shape).
- Your own remaining moves: answer escalations fast with evidence, keep docs truthful, and at
  each convergence run the integration audit its DoD defines.

## Done means

Vision ratified and current · reality audit grounded every claim · research synthesized with
visuals + design direction · infrastructure contracts published · every brief blind-executable ·
flags asked and answers recorded · everything committed · Arman pasting assignment prompts.
