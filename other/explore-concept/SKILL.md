---
name: explore-concept
status: provisional
description: "PROVISIONAL / EXPERIMENTAL — committed for the record, not a blessed workflow (its first run produced the shelved quaternion 'Belt' artifact). Explore a mathematical concept by convening the people and things that understand it — originators, near-misses, practitioners, and the concept's embodied instantiations in the universe — in a carried-out dialogue where they ask each other questions, then read the friction out of the transcript and hand it to an artifact-building stage. Invoke before designing a new app, when the user or an agent asks to explore/scope a concept (e.g. /explore-concept quaternions) — do not auto-invoke spontaneously."
argument-hint: "<a math concept to explore — e.g. quaternions>"
---

# Explore a Concept

> [!CAUTION]
> **Provisional / experimental skill.** Kept for the record, not endorsed. Its first
> real run (quaternions → "The Belt") produced a *plausible, well-documented, hollow*
> artifact that passed its own review — see the hard-fail reflection under
> `docs/sessions/progress/quaternion-exploration-app-ig4jmy/`. The diagnosis there
> (a natural-language pipeline is blind to a kinesthetic payoff and manufactures false
> confidence) is a caution about this very skill. Use only with that warning in mind.

The **divergent gathering phase** that comes *before* designing a new animath app.
Given a mathematical concept, this skill does **not** collect parallel essays and
average them. It convenes the holders of *orthogonal, embodied* understandings of
the concept in **one room** and makes them **teach each other** — and then reads
the design-relevant friction out of what they actually said. The pipeline:

> **Stage 1 — Foundation** (cited research) → **Stage 2 — The Room** (a
> carried-out dialogue) → **Stage 3 — The Friction Atlas** (read the crossings out
> of the transcript) → **Stage 4 — Building the artifact** (the design team turns
> crossings into 2–4 candidate apps + a draft plan) → **/three-hats** → **BUILDING_AN_APP.md**.

## Why a dialogue, not parallel lenses

This skill used to fan out ten independent "lens" essays and let a narrator
synthesize them. That **flattens the very thing that is generative.** A synthesis
can only surface what each lens already brought; a *dialogue* surfaces what **no
single voice held** — the content that exists only in the translation between two
of them. (In the quaternion trial run, "why can't we do it in three numbers?"
produced nothing useful until Hamilton was allowed to *refuse* Frobenius's
one-line "the wall is a wall" and keep asking — at which point the room had to
manufacture the concrete answer *15 is not a sum of three squares*, aimed straight
into Hamilton's own failing `ij` term. That fact was not retrieved. The friction
made it.) The whole skill is therefore organized around **keeping the voices
orthogonal and in genuine dialogue**, and only culling *after the fact, from the
words*.

The animath-specific question the whole thing serves is unchanged: *what is the
single best first visualization to build here?* — but we now answer it by first
finding **where the learning actually crosses difficult terrain**, and only then
asking what is buildable.

## Input

`$ARGUMENTS` — the concept to explore (e.g. `quaternions`, `the Fourier
transform`, `Gaussian curvature`). A bare concept name is fine; this skill's job is
to widen it. If the argument is empty, ask the user for the concept in one line.

## Output Files

Resolve the **branch slug** first: `git branch --show-current`, strip a leading
`claude/`, replace `/` with `-`. All outputs go in that branch's progress folder.
Get the `YYYY-MM-DD-SNN` identifier from the most recent file in
`docs/sessions/progress/<branch-slug>/` (use the current session's; if there is no
progress report yet, use today's date with `S01`). Write these files (`{id}` = that
identifier):

- `docs/sessions/progress/<branch-slug>/{id}-concept-foundation.md` — Stage 1 research base (`kind: research`)
- `docs/sessions/progress/<branch-slug>/{id}-room-transcript.md` — Stage 2 the carried-out dialogue (`kind: dialogue`)
- `docs/sessions/progress/<branch-slug>/{id}-friction-atlas.md` — Stage 3 crossings read out of the transcript (`kind: atlas`)
- `docs/sessions/progress/<branch-slug>/{id}-concept-plan.md` — Stage 4 candidates + draft build plan (`kind: plan`, `status: proposed`)

Each file is **Markdown + YAML frontmatter** per `docs/sessions/REPORT_STYLE.md`
(`kind`, `session`, `date`, `title`, `branch`, `slug`, `status`, `build`), then
`##` sections, GitHub-alert callouts and Markdown tables. `npm run sessions`
renders them to the rich HTML view. (Stage 4 may *optionally* spawn the design-team
roles as separate `kind: lens` files — see Stage 4 — but the four files above are
the required spine.)

## Stage 1 — Foundation (deep research)

Build a cited, fact-checked evidence base **first**, so the room argues from shared
facts rather than model memory, and so the transcript is **auditable** (every claim
a voice makes should trace to this document). Invoke the **`deep-research` skill**
with a prompt assembled from the concept and the angles below, scoped tightly
enough that it does not need to ask clarifying questions — something like:

> Research **<concept>** for the purpose of designing an educational, interactive
> visualization. Cover, with sources: (1) **history & originator** — who introduced
> it, when, what problem they were actually trying to solve, the key insight, **and
> the near-misses** (who reached it and didn't publish, who hit the wall and
> failed, who saw a piece without recognizing it); (2) **genetic origin** — how it
> emerges from simpler, well-understood ideas, and *why the obvious simpler version
> is impossible* if it is; (3) **natural & applied appearances** — where it shows
> up in physics, engineering, computer graphics, biology, nature, other math, and
> **where it is physically *felt*** (demonstrations a body can do); (4) the standard
> **visual representations** used to teach it, and which reveal vs. obscure the
> structure; (5) **canonical learner confusions / pitfalls**. Prefer authoritative
> sources.

Capture the result into `{id}-concept-foundation.md`. If `deep-research` is
unavailable, do a lighter targeted WebSearch + WebFetch pass over the same points.

> [!IMPORTANT]
> **Quarantine the candidate visuals.** Put area (4) — "the standard visual
> representations" — in its own `## Prior-art visualizations (quarantined — do not
> lead the room)` section. The room is seeded with the *facts* (history,
> near-misses, genetic origin, applications, felt demonstrations, pitfalls) but is
> told to let the picture **emerge from the dialogue**, treating the quarantined
> section as prior art to *differentiate from or earn*, never a menu to adopt. Only
> the Stage 4 design team and the synthesis may lean on it freely.

Also do a quick **codebase prior-art scan** (for Stage 4): note what already exists
that a new app could lean on — e.g. `src/math/quat4.ts`, `src/controls/QuarterTurnControls`,
the `src/lib/particles/` engine + `ParticleViewerShell`, the 4D projection modes,
`lib/colormaps.ts`, the CSS/DOM app pattern — and skim `docs/BUILDING_AN_APP.md`
and the closed archetype vocabulary (`src/chrome/workspace/archetypes.ts`).

## Stage 2 — The Room (the carried-out dialogue)

**Convene a cast of orthogonal, embodied understandings and write the dialogue out
in full as text.** This is authored as **one sustained transcript by a single
writer holding every voice** — not as parallel agents. The friction is *relational*
(it lives between voices) and cannot be produced by isolated agents writing in
separate contexts; that is precisely the failure mode of the old parallel-lens
approach. Seed strictly from the Stage-1 foundation.

### Casting — span the trajectory `no-knowledge → all-we-know → how-we-use-it`

Draw the cast from the foundation's facts. Aim to fill each band; some concepts
won't populate all of them, and that is itself a finding.

- **Originators & near-misses** — the historical lineage, *including* those who
  reached it and didn't publish, who hit the wall and failed, or who saw a piece
  without recognizing it. (For quaternions: Hamilton, Rodrigues, Gauss-in-a-drawer,
  Cayley.)
- **The impossibility / structure voices** — whoever can answer "**why can't we**
  do the obvious simpler thing?" *concretely*, not by assertion. The wall must have
  a keeper who can hand a learner a fact they can check. (Frobenius, Hurwitz.)
- **Practitioners** — the people who *use* it, who carry the "why care" and the
  "how we use it" end. (The animator, aerospace attitude control, the graphics
  engineer; Shoemake.)
- **Embodied & natural instantiations** — where the concept is *felt* in the
  universe, especially **felt-but-unformalized**: a body, an organism, a physical
  phenomenon that "knows" the concept without symbols. (The Dirac belt / spinning
  plate, the spin-½ electron, the falling cat, the brain's head-direction code / a
  navigating bee or bat.) These are the most valuable voices for animath's
  *manipulate-to-learn* ethos — they are pure felt.
- **The naive learner** — meets the concept for the first time, bounces honestly,
  says the wrong guess out loud.
- **The skeptic** — resists the obvious app; keeps the room honest.

### Register — how they speak (this is load-bearing)

- **Questions, not declamations.** No speeches, no "I, Hamilton, declare…". The
  room runs on genuine questions across the gaps: **"How do you…", "What about…",
  "Why can't we…", "Is *that* your…?"**
- **Press.** When a voice hits a hard question, do not let the room drop it with a
  one-line answer everyone nods at. Make the asker *refuse to leave it alone* until
  the room manufactures an answer a learner could actually hold. (The richest
  content in the trial run came entirely from this rule.)
- **Carry it out fully as text.** Do not summarize "they discussed X." Write the
  exchange. Some voices speak a lot; some barely; some choose not to speak (a
  near-miss who "put it in a drawer" can embody that silence). Everyone gets the
  chance.
- **Felt before formal.** Let the embodied voices *show* (a belt, a turning object)
  rather than state. Where the felt and the formal land on the same spot, let the
  room notice it *in dialogue* — do not annotate it from outside.
- **Do not pre-cull.** The transcript is not pre-filtered for "useful" moments. The
  words do the culling; Stage 3 reads it out. Resist the urge to append "here are
  the takeaways" — that is Stage 3's job, and doing it here destroys the evidence.
- **The transcript is spoken dialogue only.** No margin commentary, no inline "what
  just happened here" notes, no `>` annotations wedged between lines. If you can see
  the friction, *leave it* for the reader and the atlas — narrating it inside the
  room is the same contamination, merely relocated.

Write the full transcript to `{id}-room-transcript.md`, opening with a short
**"Seeded from"** note linking the foundation (for auditability) and a **Cast**
list grouped by the bands above, then the dialogue.

### Two ways to run the room

The room can be **authored** or **live**; both are legitimate, with different
guarantees.

- **The authored room** — one writer holds every voice and writes the whole
  transcript. Fast, coherent, the default. Its risk is *self-collusion*: a single
  author can unconsciously have one voice ask the question whose answer it already
  knows, *staging* the reveal rather than earning it.
- **The live room** — the cast is split across **multiple model-diverse agents**
  (Agent tool, each with a different `model`), each a *troupe* of personas, **routed
  turn-by-turn by you as director**. No agent holds both sides of a friction, so no
  single context authors both a question and its answer. This is the collusion-proof
  mode — use it to *test* whether the surfacing is real, or for a high-stakes
  concept. It is slower and token-heavy.

Live-room discipline (each rule was learned by violating it; breaking any one
reintroduces the contamination the mode exists to remove):

1. **Split antagonists across troupes.** The presser (naive learner, skeptic) and
   the voice that must answer them belong to *different* agents on *different*
   models. Put the impossibility-keeper in the same troupe as the skeptic and you
   are back to self-collusion.
2. **The director relays verbatim and adds nothing.** Route each line into the next
   agent's prompt exactly as spoken. Paraphrasing while relaying *is* co-authoring.
3. **Never seed the payload.** Withhold from every brief the things you want to see
   *emerge* (the concrete counterexample, the key reframe). Give a voice the
   *principle* it would plausibly hold, never the punchline. If you catch yourself
   leaking an answer into a brief, **discard that line and re-run from a clean
   brief** (in the quaternion live run this caught a seeded "15" and the clean
   re-run produced a different, hand-built counterexample — `3·21 = 63`).
4. **Pressers get a no-jargon clause.** A naive learner / skeptic who reaches for
   textbook words ("fiber bundle", "topological charge") has broken character. Brief
   them to demand, and speak in, plain checkable terms only.
5. **Stateless is fine — and is a feature.** If no agent-to-agent message tool
   exists, spawn a fresh agent of the troupe each turn with its brief + the public
   transcript, directed to speak as one persona. A context with no persistent self
   cannot plan a reveal ahead.
6. **Record the audit.** The transcript header carries a model→persona table and a
   provenance note flagging any beat re-run for contamination.

Honest limit: even done perfectly, the director still chooses turn order and when
to press — residual influence the live room reduces but does not erase. The
quaternion runs are on the branch: `…-room-transcript.md` (authored) and
`…-live-room-transcript.md` (live, model-diverse).

## Stage 3 — The Friction Atlas (read the crossings out of the transcript)

Now, and only now, cull — *from the words*. Read the transcript and extract the
**atlas of crossings**: the places of **friction, interest, and explanatory load**
strung along the trajectory `no-knowledge → all-we-know → how-we-use-it`. For each
crossing record: the gap (from → to), who stood on each side, **what the friction
was**, why it is interesting, whether/how it is **felt**, and — flagged as a Stage-4
seed, not a design — the *shared handle the dialogue kept reaching for* (the
concrete object two voices were forced to meet on).

Then surface the **emergent invariants**: the motifs that showed up at *multiple
independent crossings without being put there* (in quaternions: the half-angle
reappearing at three unrelated crossings; the twin walls bookending the path; the
felt anchors clustering exactly at the hardest formal crossing). These recurrences
are **the pattern of learning the concept itself dictates** — they, not the topic
name, are the real spine. Every atlas entry must cite the transcript moment it came
from. Write to `{id}-friction-atlas.md`.

## Stage 4 — Building the artifact (the design team + draft plan)

Only here does design begin. Hand the artifact-building roles **everything the
prior stages produced** — the full Stage-1 foundation (now including the
quarantined prior-art, usable here), the complete Stage-2 transcript, and the
Stage-3 atlas — not the atlas alone. The atlas is the *spine* (it says which
crossings matter), but the transcript's exact phrasings, the originator's framing,
and the foundation's formulas and citations are the raw material the explainer, the
on-ramp, and the panels are built from. Either reason through the roles inline, or
spawn them as parallel agents writing `kind: lens` files
(`{id}-design-builder.md`, `-educator.md`, `-game-designer.md`, `-illustrator.md`,
`-visual-designer.md`):

- **The Builder** — what animath can render well and cheaply vs. what fights the
  framework; concrete prior art to reuse (the `lib/particles` engine,
  `QuarterTurnControls`, 2D shader viewers, CSS/DOM); realistic build cost.
- **The Educator** — the learning arc that walks the atlas's crossings in order;
  progressive disclosure; how a learner checks their own understanding.
- **The Game Designer** — the core interaction loop; the smallest satisfying
  action→feedback cycle built on a crossing; honest-to-the-math play.
- **The Illustrator & Visual Designer** — the look, the legibility, what the
  *shared handle* from each crossing actually looks like on screen.

Then write `{id}-concept-plan.md` (`kind: plan`, `status: proposed`):

1. **From atlas to app** — which crossing(s) the app is built on, and why (favor
   the ones where *felt and formal coincide* and the emergent invariants concentrate).
2. **Candidate app concepts** — **2–4** distinct concepts, each a short pitch (what
   you see, what you do, what it teaches) scored in a table on **framework fit ·
   pedagogical payoff · visual appeal** (Low/Med/High, one-line justification each).
3. **Recommendation** — the single best first course of action, and why.
4. **Draft build plan** — concrete enough for `BUILDING_AN_APP.md`: engine to build
   on; **`SectionDef[]` panels** (each tagged with a closed-vocabulary archetype);
   **`ViewDef[]` view(s)**; the **on-ramp view** (most illuminating first frame);
   the **explainer angle** (use the originator's framing from the transcript); the
   route/registry edits (`index.tsx`, `apps.ts`, `catalog.ts`); honest caveats (what
   the picture distorts).
5. **Next steps** — recommend `/three-hats <path to this plan>` before building.

End the plan with the **Self-Reflection Protocol** (`.claude/prompts/self-reflection.md`)
as a `## Self-reflection` section.

## After Stage 4

Present a condensed summary in the conversation: the crossing(s) the app is built
on, the recommended concept and runner-up, the scoring at a glance, and the
one-paragraph build plan — with pointers to the full files. Then **stop and let the
user choose** before any implementation; offer `/three-hats` as the next step.

## Rules

- This is **exploration and planning only** — do **not** write app code or edit the
  registry during this skill. The deliverable is the plan.
- **Keep the voices orthogonal in the room; reconcile only in the atlas.** A voice
  that already agrees with another is a wasted seat — recast it.
- **The room is authored, not parallelized.** Stage 4's design roles may be
  parallel agents; the dialogue itself never is.
- **Cull from the words, never ahead of them.** The transcript stays un-pre-filtered;
  the atlas cites it.
- Update the session progress report after each stage transition per the
  progress-report rule.
- Commit and push the new report files when the skill completes.
