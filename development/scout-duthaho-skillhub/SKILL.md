---
name: scout
description: >-
  Competitive reconnaissance for your project — what do the repos solving
  this same problem do better, and what's worth adopting? Finds peer repos
  (ranked by activity, downloads, dependents — never raw stars), mines what
  their users beg for — issue reactions, releases, docs claims, every
  finding with a locator — and verdicts each candidate feature
  ADOPT/ADAPT/SKIP/WATCH, where SKIP is the default and "a competitor has
  it" is never a reason. ADOPT items become ready seeds for feature or
  autopilot; verdicts persist in out/scout/tracker.md so repeat runs open
  with what changed. Keyless. Use for "what are similar projects doing",
  "compare us to X", "what are we missing" — e.g. "/scout",
  "/scout <owner/repo>", "/scout deep <repo>". For X-vs-Y tech choices use
  verdict; for community buzz use pulse.
---

# scout — know the neighbors before building blind

`/scout` — find peer projects, then reconnoiter them
`/scout <owner/repo> [...]` — reconnoiter exactly these peers
`/scout deep <owner/repo>` — one peer, source-level (clone + file:line evidence)

Answer one question: **what have the projects solving this same problem
learned that we haven't — and which of those lessons deserves to exist
here?** Both halves matter: a scout that only returns "features to copy" is
just an automated parity trap. The deliverable is judgment: adopt this,
skip that, and the evidence either way.

## Step 0 — Know thyself first

Recon of others starts with a fix on your own position:

- Read this repo's `AGENTS.md` (the map skill writes it), `README`, and its
  own issue tracker's top-reacted open requests. Distill: **the project's
  job in one sentence**, and its **differentiation axis** — the thing it
  does that peers don't, which every later verdict is judged against.
- Read `out/scout/tracker.md` if it exists: peers already scouted, verdicts
  already made. A feature SKIPped with a reason isn't re-litigated unless
  the evidence changed; repeat runs open with **"Since last scout"** — new
  releases, new high-reaction requests, verdicts due for revisit.
- "Similar" means **same problem, not same tech stack** — a peer in another
  language that owns your problem space teaches more than a same-framework
  neighbor that doesn't.

## Step 1 — Find the peers (skip when the user names them)

Discover candidates keyless, then rank by signals that resist gaming:

- **GitHub topics overlap** (`/repos/{o}/{r}/topics`, then
  `/search/repositories?q=topic:X`) and README/description keyword search.
- **Registry keyword co-occurrence** — npm `/-/v1/search?text=keywords:...`,
  PyPI JSON — projects sharing your package keywords.
- Awesome lists and "alternatives to X" directories for the long tail.

Rank by **recent push cadence, download counts (api.npmjs.org /
pypistats.org), and dependents (deps.dev)** — never by raw stars; star
counts are purchasable and four-figure HN threads document the fake-star
economy. Present the candidates with one line each on why they qualify;
settle on **3–6 peers**. Fewer, studied properly, beats a survey.

## Step 2 — Reconnoiter each peer

One sub-agent per peer, in parallel. Budget first: keyless GitHub allows
**60 core req/hr and 10 search req/min shared across all sub-agents** —
allocate calls per peer up front, and on a 403 mark the signal unknown
rather than retrying in a loop. Each agent mines three signal layers:

1. **What their users beg for** — open issues sorted by 👍 reactions
   (`/search/issues?q=repo:X+is:issue+is:open&sort=reactions-%2B1`).
   Enhancement requests draw ~4× the reactions bugs do; this is raw market
   demand. A high-reaction request a peer *hasn't* built is as valuable as
   a shipped feature — it's an open lane, not a gap to close.
2. **What they shipped, and when** — the releases API: feature inventory
   from release notes, plus shipping cadence (a peer releasing weekly
   pressures differently than an annual one).
3. **What they claim** — README/docs feature inventory, marked as claims,
   not verified behavior.

**Every finding carries a locator** — issue URL with reaction count,
release tag, doc anchor. AI summaries of unfamiliar repos are exactly where
confident hallucination lives; a claim without a pointer is discarded, not
softened. Each agent writes full findings to `out/scout/.work/<peer>.md`
and returns a summary; synthesize from the files.

**Deep mode** (`/scout deep <repo>`, or offered when a verdict needs it):
clone the peer locally and read the implementation — architecture choices,
the tricky parts of a feature you're weighing. Evidence tightens to
**file:line**. This is the expensive tier; use it on the one or two peers
that earned it, never the whole field.

## Step 3 — The gap, both ways

Lay the feature inventories side by side against your project's job:

- **They have, we lack** — the adoption candidates, each with its demand
  evidence attached.
- **We have, they lack** — the moat. Knowing what not to break or dilute
  is half the value of the exercise; these feed the differentiation axis,
  not the backlog.
- **Nobody has, their users want** — open lanes from layer-1 signals; often
  the best entries on the list.

## Step 4 — Verdicts, with the parity gate

For each candidate: **ADOPT / ADAPT / SKIP / WATCH**. The gate:

- **SKIP is the default.** "A peer has it" removes a reason to say no and
  supplies none to say yes; parity-chasing is the documented failure mode
  of this whole exercise. Promotion out of SKIP needs positive evidence:
  demand in *your* tracker or stated goals, fit with *your*
  differentiation axis, and a cost that fits the value.
- **ADOPT** — wanted here, fits the axis: one-paragraph implementation
  sketch shaped to this codebase + effort estimate. **ADAPT** — the idea
  transfers, their shape doesn't; name what changes. **WATCH** — promising
  but unproven; note the revisit trigger (adoption numbers, a stable
  release).
- **License check before any ADAPT that borrows shape:** ideas are free,
  code is licensed — flag the peer's license (a GPL peer next to your MIT
  project means re-implement from the idea, never from the source).

## Step 5 — Brief, memory, handoff

- Render the brief **in chat** per `references/brief-template.md` (read it
  when you reach this step), then save to `out/scout/<slug>-<YYYY-MM-DD>.md`
  (date via `date +%F` — never guessed; create the folder if needed;
  committing the brief is the user's call).
- Update `out/scout/tracker.md`: one row per peer (last release seen, last
  scout date) and one per verdict (feature · verdict · reason · date) — the
  memory that makes the next run a delta instead of a redo.
- Offer the handoff, never perform it: each ADOPT item is phrased as a
  ready `/feature <item>` or `/autopilot <item>` invocation, with the
  brief's sketch as the spec seed.

## Guardrails

- **"A competitor has it" is never a reason.** Every ADOPT cites demand or
  goal-fit from *this* project's side. The skill exists to prevent the
  parity trap, not to automate it.
- **Evidence is a locator.** Issue URL, reaction count, release tag,
  file:line in deep mode. No locator, no finding.
- **Stars are noise.** Rank and argue from cadence, downloads, dependents,
  and reaction counts — the signals that resist buying.
- **Respect the budget.** 60 req/hr shared; allocate up front, degrade
  honestly ("signal unknown") instead of retry-looping.
- **The moat is output too.** A brief that only lists what to copy failed;
  what to protect and what lanes are open carry equal weight.
- **Advisory, not authoritative.** It recommends with evidence; the human
  decides what enters the backlog. Nothing is implemented, filed, or
  committed by this skill.
