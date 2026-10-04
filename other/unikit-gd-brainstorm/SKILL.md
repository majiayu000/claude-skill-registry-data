---
name: unikit-gd-brainstorm
description: >-
  Ideate a brand-new game concept with the user, from a blank page or a one-line hint to
  a finished CONCEPT card. Use it whenever the user wants to come up with a new game —
  whether the project has no design document yet, or already has one and they're exploring
  a fresh idea. Through a structured divergence/convergence dialogue it explores ideas,
  frames the hook, generates and scores concepts (market validation delegated to
  /unikit-gd-explore), and settles pillars, loops, motivation, and a pre-mortem. Trigger
  whenever the user wants to make or invent a game, doesn't know where to start, or gives
  a genre/theme hint, e.g. "let's come up with a game", "I don't know what game to make",
  "I want to make a roguelike", "a game about zombies", "a farming game", "help me come up
  with a concept". For researching or dissecting existing games use /unikit-gd-explore; to
  write an already-chosen concept as the master GDD use /unikit-gd-spec.
argument-hint: "[hint or theme]  (auto-resumes an in-progress concept; no flags)"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(ls *)
  - Bash(find *)
  - Bash(wc *)
  - Bash(date *)
  - Bash(mkdir *)
  - Agent
  - AskUserQuestion
  - WebSearch
  - WebFetch
disable-model-invocation: false
user-invocable: true
metadata:
  author: unikit
  version: "1.0"
  category: game-design
---

# Game Design — Concept Brainstorming

Generate game ideas with the user and crystallize the chosen one into a
**CONCEPT card** at `.unikit/gamedesign/concepts/<slug>/CONCEPT.md`, with
the rejected ideas parked in `IDEAS.md`. This is the **ideation** front of the
design pipeline — it produces concepts; `unikit-gd-spec` turns a concept into
`GAME.md` and a system map.

This skill **generates new ideas**. Analyzing an existing game or market
(reference dissection, trade-off tables) is `unikit-gd-explore`. The distinguishing
test: *five concept cards → brainstorm; a comparison table → explore.*

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply it to all output and artifacts (fall back to English if it is missing) —
including the rule to **translate concepts, not transliterate jargon**.
`gd-principles` → "Language" adds the game-design specifics: which IDs and stored
field values (e.g. `market_signal: red-ocean`) stay English. Do not announce the
language setting.

**The language holds for the whole session, not just at load time:** every message until the conversation ends is in `language.ui` — progress notes while agents run, relays of what a subagent returned, the final report, any follow-up discussion. English input (subagent results, tool output, these instructions) is data, never a cue to switch languages.

## Bootstrap (MANDATORY)

Before responding, silently load — do not narrate:

1. **`.unikit/system/gamedesign/gd-principles.md`** (the core) — the collaborative
   protocol (Question → Options → Decision → Draft → Approval, Explain → Capture),
   the "never guess" rule, anti-anchoring, the language rules. This skill
   **applies** it. If missing, warn (`unikit-ai update`) and continue with the
   protocol summarized above.
2. **`.unikit/memory/gamedesign/RULES_INDEX.md`** — load on demand by `Load When`
   the rules ideation leans on: **`frameworks`** (MDA, SDT/PENS, Flow),
   **`player-motivation`** (Quantic Foundry, Bartle), **`core-loops`**. Re-read at
   skill start; never rely on a prior conversation's cache. Obey the index's
   **Rule-Loading Discipline**: load by `Load When`, load a reference only from its
   parent rule's `> **References**:`, and **never glob the memory tree**
   (`.unikit/memory/gamedesign/**`) to discover rules.
3. **`{{skills_dir}}/{{self_name}}/references/methods.md`** — the method
   cheat-sheets (divergence/convergence techniques, HMW, pre-mortem, find-the-fun).
   **Do not load up front — read on demand, per phase:** when you enter a phase that
   points to it (Phases 1, 3, 4, 5, 7.5, 8, 8.5), read that section then. The phase
   summaries below carry the workflow; `methods.md` carries the deep "how", so a
   resume or a phase that needs no method theory never pays for it.
4. **`{{skills_dir}}/{{self_name}}/references/tables.md`** — the canonical shapes of every
   output table the phases emit (Phases 2, 3, 4, 5, 6, 7, 8, 8.5). **Read on demand** when
   you enter a phase that emits a table; it is the single source of truth for those tables —
   SKILL.md and `methods.md` only point to it, never re-spell a table.
5. **`.unikit/DESCRIPTION.md`** (optional) — existing project constraints, if this
   is ideation inside an established project.
6. **`.unikit/RULES.md`** (if present) — project overrides, highest priority. **Rule topics:** load the topic files listed under its `## Topics` whose `Load when` matches the design work at hand — the concept, system, flow or content type; when unsure, load.

**Market validation is delegated, not ad-hoc.** This skill does **not** research the
market inline or early — early data anchors timid ideas (anti-anchoring,
`gd-principles`). Market evidence enters at **Phase 3.5**, where brainstorm spawns
`unikit-gd-explore` as a subagent to scan the shortlist and **return a brief into
this session**. The delegation **interface** — the brief's fields, the canonical
marker, the four-verdict gate — is the contract at
`{{skills_dir}}/unikit-gd-explore/references/delegation-contract.md`, **loaded on
entering Phase 3.5** (per-phase, like `methods.md`), not up front; brainstorm reads
that *interface*, never explore's engine (`market-scan.md`). General `WebSearch` /
`WebFetch` lookups remain available as read-only advisors — they never write and
never substitute for the Phase 3.5 scan.

## Phase 0 — Auto-Resume (no flags)

*Brainstorming runs across many turns, so this step looks in the concepts index for
an unfinished concept that matches the hint and offers to continue it — a session
interrupted by a `/clear` or a closed terminal is never lost.*

Read `.unikit/gamedesign/concepts/INDEX.md` (if it exists). Each row carries a
slug, title, keywords, **status** (`in-progress | complete | promoted | abandoned`),
and the last phase reached. Semantically match the user's hint against the rows:

- A live `in-progress` concept matches the hint →

  ```
  AskUserQuestion: Found "<title>" — you left off at phase <N>. What now?
  Options:
  1. Continue "<title>" from phase <N> (recommended)
  2. Start a fresh concept
  3. List all concepts
  ```

- No match → start a new concept at `concepts/<slug>/`.
- A match exists but the user chooses to start fresh → **ask for a different slug**, then
  create `concepts/<new-slug>/` and print `INFO [concept] creating <new-slug>`.

`promoted` and `abandoned` concepts are **never offered for resume**, but their
`IDEAS.md` is read so the session does not re-pitch a killed idea. Repeated
brainstorms need a **different** slug — the user is asked for one; the date no longer
supplies the difference. **Appending an automatic suffix is forbidden**: the slug is
derived from the topic, so a second run at one topic produces the same name, and a
silently suffixed folder is one the auto-resume above will never offer again.

On resume, jump to the saved phase — including the **fractional phases 3.5, 7.5, and
8.5** (a session interrupted mid-scan, mid-flow-seeds, or mid-validation resumes there,
not back at 3, 7, or 8); on a fresh start, begin at Phase 1.

## Phases 1–9

Run the phases in order. Each phase below is the **workflow**; its deep method detail
lives in `references/methods.md` — read that section when you reach the phase, not up
front. Diverge and converge as **separate** moves — never score an idea as you
generate it.

### How to respond in each phase

- **Go deep, not terse.** Each phase is a consultation, not a form to fill in. When
  you present options, loops, pillars, or risks, explain the *reasoning* in a few
  sentences — the framework it draws on, the comparable game that proves it, the
  trade-off it carries — not a bare one-line bullet. The user is making a creative
  decision and needs the *why*, not just the *what*. A phase answered in a single line
  is almost always too thin; spend the words.
- **Open every phase with its purpose.** The italic line under each heading below says
  what the phase is and why it exists — orient the user the same way in your own words
  before you dive into the questions, so no phase arrives unexplained.
- **Readable plain markdown only.** Number options and concepts with plain `1.` / `2.`
  and label variants `A)` / `B)`. Never use circled or enclosed glyphs (①②③, 🅰🅱, Ⓐ)
  or other decorative unicode — they render as boxes or unreadable smudges in most
  terminals. Bold, short tables, and plain headings carry all the structure you need.

### Phase 1 — Creative Discovery (+ commercial frame)

*Find the seed before generating anything: who you are designing for, the feeling you
are chasing, and what "success" means commercially. This is what makes every idea that
follows aimed and yours, instead of generic.*

Ask about the **person**, not the game: emotional anchors, three games they love
and what those left them wanting, plus constraints (solo/team, deadline, engine,
experience). Synthesize a **Creative Brief** (3–5 sentences) and confirm it.

Then capture a **commercial frame** (one screen, kept separate from the person
questions):

- **Target outcome tier** — hobby / recoup / commercial.
- **Target platform** — ask explicitly, **never default to Steam** (the four options
  below). Platform is a market-shaping decision, not a deployment detail.
- **Budget / team size** — solo / small team / funded. A **reachability** constraint:
  a clone-dense mobile market is unreachable without a UA budget, however good the
  concept. Phase 3.5 reads demand as *reachable* vs *someone else's* against it, and
  passes it to the delegated scan as the `budget/team` input.
- **Target session length** — shapes platform fit (web rewards short instant loops;
  premium PC tolerates long sessions); sets the card's platform-fit sanity line (field 8).
- **Monetization intent** — premium / F2P-IAP / ads / portal rev-share / none. Feeds
  the T8 `monetization_fit` read in Phase 3.5 (`monetization_intent` in the scan).
- **Scan mode** — `quick` / `standard` / `deep` for the Phase 3.5 delegation;
  `standard` is the default, `quick` for an early red-ocean sweep of 3–4 concepts.
- **Kill-readiness** — drop on bad data, or passion-project regardless?

Platform options (name a *lead* even for cross/console):

1. **PC / Steam** — wishlist-driven, long tail, premium or early-access pricing.
2. **Mobile** — store-feed and UA-driven, F2P norms, short sessions, clone-dense.
3. **Web / instant** — portal- and embed-driven (itch, CrazyGames, Poki): instant
   play, near-zero install friction, ad/portal economics.
4. **Cross / console** — still name a *lead* platform; one store shapes every later
   signal.

The platform **steers the Phase 3.5 scan** (each platform has its own demand signals,
sources, and clone-density; the cross-market rule turns a mobile/web target into a
Steam demand-check plus a target-store clone-check — full per-platform table and the
cross-market rule in `references/methods.md` § Phase 1).

**Anti-anchoring boundary (explicit).** Structural *platform* facts (mobile is
clone-dense; web rewards an instant hook; Steam is wishlist-driven) may inform this
frame now — they are not about any specific concept and do not anchor divergence.
**Concept-specific demand data** (does *this* idea sell, how many clones of *this*
concept exist) is withheld until Phase 3.5, after divergence.

The frame **scopes Phase 3.5; it does not censor divergence.** A user with no
commercial intent leaves it **empty** — that is valid and **skips Phase 3.5**
(`market-signal` then stays an ordinary Pugh judgment, not a delegated scan).

### Phase 2 — How-Might-We Framing

*Recast the brief as open "How might we…" questions that invite many answers instead
of smuggling in one solution. Good framing is what keeps the next step — divergence —
genuinely wide.*

Reframe the brief as **3–5 "How might we…"** questions (positively framed, no
baked-in solution). **Present them as a table** so the user can weigh the framings side
by side instead of reading a flat list, and mark the strongest **(Recommended)** with a
one-line WHY; the user picks one to diverge on. The table's columns and a worked example
live in `references/tables.md` § Phase 2 (the single source of truth for this table).

### Phase 3 — Divergence

*Generate breadth on purpose: five concepts from five different idea-generators, so
the field is genuinely varied and not five repaints of the first thought. Hold all
judgment for later — quantity now, scoring in Phase 4.*

Generate **five concepts using five different methods** (verb-first, genre mashup
with the intersection-audience caveat, experience-first/MDA-backward, world-first,
constraint-first — each method's prompt and source in `references/methods.md`
§ Phase 3). Render **each** concept as its own **nine-field card** — a `Field | Value`
table so the fields stay aligned and scannable instead of buried in prose. Then, after
the five cards, present one **comparison table** across all of them: the shortlist
decision is a side-by-side judgment ("which two hooks are strongest?") that five separate
cards cannot support at a glance. The nine fields, the comparison columns, and worked
examples of both live in `references/tables.md` § Phase 3 (the single source of truth for
these tables).

Once the five are on the table, ask the user how to proceed — and offer three
distinct moves, not just "pick some":

1. **Shortlist 2–4** to carry forward into validation / scoring.
2. **Five more** — *extend* the field with a stimulus method (random input / SCAMPER /
   Lotus Blossom) built on the current favorite; keeps what is working and pushes for
   adjacent variety.
3. **Regenerate from scratch** — *discard this whole batch* and generate five **new**
   concepts from different methods or a different How-Might-We angle. This is the right
   call when none of the five land or they all feel like one idea wearing five hats.
   The discarded batch still goes to `IDEAS.md` (with its revival condition) so nothing
   is silently lost or re-pitched later.

### Phase 3.5 — Market validation (delegated to explore) — **gated**

*Pressure-test the shortlist against the real market — does a reachable audience
exist, and is there unmet room for it — delegated to explore so brainstorm never
grades a market from memory. It runs after divergence, on purpose: early data anchors
timid ideas.*

**Gate:** run this phase **only if Phase 1 produced a non-empty commercial frame.**
Empty frame → **skip**; `market-signal` stays an ordinary Phase 4 judgment, no
subagent.

Run **after** divergence, on the user's **shortlist (2–4 concepts)** — never earlier
(early data anchors timid ideas; `gd-principles`). brainstorm does **not** research
the market itself — it **delegates** to `unikit-gd-explore` and consumes the evidence.

**Load the contract first.** On entering this phase, read
`{{skills_dir}}/unikit-gd-explore/references/delegation-contract.md` — the interface
this delegation follows: the brief's fields, the canonical marker, and the
four-verdict gate. brainstorm reads that *interface*, never explore's engine
(`market-scan.md`). (Hard-code the `unikit-gd-explore` path — it is **not**
`{{self_name}}`.)

**Delegate** — spawn explore as a subagent and **wait for the return**. Expands to:

```
Agent(
  subagent_type: "general-purpose",
  prompt: "/unikit-gd-explore <commercial frame incl. target platform + budget/team + shortlist>. scan_mode: <quick|standard|default standard>. Validate cross-market per the platform rule. Return the brief into this session as text; do not save any files.",
  description: "Market-validate the shortlist",
  skills: ["unikit-gd-explore"]
)
```

Pass **`scan_mode`** explicitly: `standard` is the default; use `quick` for an early
3–4 concept red-ocean sweep (it returns C-capped signals — enough to flag, not to
commit on). Carry the **budget/team** slot from the commercial frame as a reachability
input; until Phase 1 captures it, it arrives `unknown` and the scan degrades
gracefully (never fabricates a budget read). Substitute the real frame values into the
`<…>` placeholders.

**Fallback (no Agent tool).** If the `Agent` tool is unavailable in this environment,
do **not** print the delegation as a recommendation — that is a known failure mode
where the model renders the call instead of running it. Instead, invoke
`/unikit-gd-explore` **inline** as a real skill call, passing the same commercial
frame + shortlist and the canonical marker verbatim, and wait for its brief. If skill
invocation is *also* unavailable, run the scan yourself inline with `WebSearch` /
`WebFetch` against the technique catalogue in
`unikit-gd-explore/references/market-scan.md` (comparable mapping, demand
classification, review mining, and the cross-market rule above), and label every
finding with the same `market_signal` + `validation_confidence` fields so the rest of
the flow is unchanged.

The prompt MUST carry the **canonical marker** verbatim, on one line:

> *"Return the brief into this session as text; do not save any files."*

so explore runs its market lens deterministically and persists nothing (the
contract). The subagent returns, per concept, `market_signal` +
`validation_confidence` + a short evidence brief **into this session**.

**Carry the platform — the cross-market rule.** A market is platform-specific (a genre
that thrives on Steam can be a clone-saturated graveyard on mobile, and the reverse
happens too), so the delegation prompt names the **target platform from Phase 1** and,
for a non-PC target, asks explore to validate *across* markets: prove the genre on Steam
(the clearest *demand* signal even when you ship elsewhere), then scan the *target* store
for clones, then read the gap — Steam-proven + no strong clone on the target store is the
prize; Steam-proven **but** the target store already clone-dense is a red ocean on the
platform that actually matters. The mechanics of that rule live in
`references/methods.md` § Phase 1, and the scan engine that runs it in
`unikit-gd-explore/references/market-scan.md`. Report the read **per platform** in the
brief; it feeds the kill gate below.

**Consume — the calling session owns persistence:**
- Lift the **six machine fields** (`market_signal`, `validation_confidence`,
  `clone_density`, `trend_fit`, `monetization_fit`, `recommendation`) **verbatim** into
  the **CONCEPT card** header machine-block, **outside the nine-field table** (the card
  stays "nine fields, no more").
- Distil `key_evidence` and `go_to_market_risk` (comparables, the unmet need, the reach
  risk) into the card's **`## Notes`** — not just the machine fields.
- **Write no `researches/` file** — that directory is explore's; a delegated scan is
  evidence for *this* concept, carried in the card.

**Decision gate — four verdicts, not a binary.** Consume the brief's `recommendation`
per concept and surface it **before** Phase 4 scoring (the contract's gate table):

| Verdict | Meaning | Action |
|---------|---------|--------|
| **proceed** | white-space, confidence ≥ B | carry into Phase 4 as a strong candidate |
| **proceed-with-differentiation** | contested, conf ≥ B, a clear twist exists | carry forward; sharpen the hook |
| **validate-later** | white-space/contested at conf C, or `unknown` | carry forward but route the open risk to the Phase 8.5 validation plan |
| **pivot** | red-ocean **but** an adjacent white-space exists | cross-pollinate (below): graft the under-competed angle onto a stronger concept; render the hybrid as a full nine-field card |
| **kill** | red-ocean, no adjacent white-space, unreachable at scope | park in `IDEAS.md` with a revival condition |

Never silently carry a `kill`/`pivot` concept forward, and never `proceed` or `kill`
on `unknown` — `unknown` always routes to `validate-later`. The gate informs; the
user decides.

**Cross-pollinate before you cut (the `pivot` verdict).** A red-ocean concept is not
only a kill candidate — it is also raw material, and the gate's **`pivot`** verdict
routes here rather than to `kill`. When one shortlisted concept reads **red-ocean**
while another reads **white-space / contested**, do not just drop the crowded one:
proactively offer
a **genre mash-up** that grafts the under-competed concept's angle onto the stronger
one (the genre-mashup divergence method, with its intersection-audience caveat — the
hybrid must please *both* audiences, not merely exist). A saturated genre often hides a
strong twist the moment it is crossed with a fresher one. The hybrid is a **new candidate
concept**, so present it as a full **nine-field concept card** — the same `Field | Value`
table as Phase 3 (`references/tables.md` § Phase 3), not a loose prose pitch — so it is
directly comparable to the shortlist; route it to Phase 4 / Phase 8.5. Recommend it when
the evidence supports it, but never impose it — the user decides.

### Phase 4 — Convergence (two-pass Pugh) → **incremental write**

*Now judge. A two-pass Pugh matrix scores the survivors on locked creative criteria
first, then on the market evidence — keeping the two apart so optimism can never
out-vote data. Pugh scoring just compares each option against criteria to rank them
transparently.*

Score the surviving concepts with a **two-pass Pugh matrix** (full method, the hard
rule, and the `market-signal` vs `market_signal` terminology in `references/methods.md`
§ Phase 4 + § Content velocity):
- **Pass 1 — creative** (lock *before* the scan): hook / scope-fit / team-fit /
  personal-fire / **content-velocity** — can the design *feed itself* cheaply
  (procedural / systemic / competitive / UGC), or does every play-hour cost
  author-hours of hand-made content? A low-velocity model is a hidden scope and
  live-game risk, scored here as a real feasibility axis, not a footnote.
- **Pass 2 — evidence** (from the Phase 3.5 brief, only if it ran): market-signal +
  validation-confidence.

**Hard rule:** the **market-signal** score may **not exceed what
validation-confidence allows** — an unproven market read cannot win on optimism.
Show the two passes as **two separate tables** (columns and a worked matrix in
`references/tables.md` § Phase 4) — kept apart so locked creative scores and market
evidence never share a column; the user weights, arithmetic transparent. If
Phase 3.5 was skipped, `market-signal` is scored as an ordinary Pass-1 judgment. Use
**How-Now-Wow** if "I like all of them". Do **not** approve a hybrid whose winning
bet rests on a low-confidence market assumption — route it to Phase 8.5 instead.
Select or hybridize. Rejected concepts go to **`IDEAS.md`** (idea, essence, reason,
revival condition). **Persist now** — write the chosen card draft and `IDEAS.md`; an
interruption after this loses nothing.

### Phase 5 — Loop Stack

*Map the nested gameplay loops — from the 30-second core action up to the meta-game —
plus the discoverability loops that decide whether anyone starts and comes back. This
is the spine of moment-to-moment fun and the first read on whether the game retains.*

Define the nested loops (30 s / 5 min / session / meta) plus the **discoverability
loops** (first-session → retention, the 6-second trailer moment, the "one more run"
retention hook — full detail in `references/methods.md` § Phase 5). Then audit **SDT**
(Autonomy / Competence / Relatedness — flag if only 1 of 3 is served) and **game feel**
(does the core verb get ≤100 ms, multi-channel feedback? — Swink). Present all three as
tables — the loop stack, the SDT audit, the game-feel check — so a gap (an unserved need,
a flat verb) is visible at a glance rather than lost in prose. Columns and worked examples
are in `references/tables.md` § Phase 5 (the single source of truth).

### Phase 6 — Pillars & Anti-Pillars → **incremental write**

*Pillars are the 3–5 load-bearing design values every later decision gets tested
against ("does this serve a pillar?"). Anti-pillars name what the game deliberately
refuses to be — together they keep scope honest and decisions consistent.*

Derive **3–5 pillars**: active, each serving ≥1 emotion, each with a **design test**
and mutual tension; reject empty pillars and task-pillars. For each pillar add
**Evidence** (the data / comparable that justifies it — ideally the Phase 3.5 brief's
review-mining) and a **Cut rule** (what is cut first under scope pressure); a pillar
with no evidence is a slogan — flag it. Add **≥3 anti-pillars** ("We will NOT <X>
because PIL-n"); the brief's review-mining (love / hate / wish) feeds these. Present the
pillars and anti-pillars as **two tables** — a pillar carries five columns (emotion,
design test, evidence, cut rule) that only line up under scrutiny in a grid, and the
table makes a sloganeering pillar (empty evidence cell) impossible to hide. Columns and
worked examples are in `references/tables.md` § Phase 6. Run a Lock / Rename / Swap cycle.
**Persist now.**

### Phase 7 — Player Motivation (player + buyer)

*Pin who this is for psychologically (what drives them to play) and commercially (what
makes them buy or wishlist) — and, just as sharply, who it is NOT for. A concept that
serves everyone usually moves no one.*

**Quantic Foundry:** the user ranks the **top 3 of 12** motivations; the skill
checks them against the pillars and loops. Set MDA primary/secondary and a one-line
Bartle read. Then separate **player from buyer**: the **buying trigger** and the
**quitting / refund trigger** (from the Phase 3.5 brief when it ran), plus an
explicit **anti-persona** — "who this is NOT for". Capture the whole read as one table
(player psychology → buyer triggers → anti-persona) — columns and a worked example in
`references/tables.md` § Phase 7.

### Phase 7.5 — Scenario / Flow seeds

*Turn the loops (Phase 5) and pillars (Phase 6) into the **dynamics seeds** the Flow
axis picks up downstream — this does not author flows, it seeds them (as Phase 6 seeds
the pillars the spec later formalizes).*

Draft **3–5 scenario prompts** (the concrete player situations the game must deliver,
each anchored to a pillar), a **candidate wiring mode** per scenario (`linear` /
`conditional` / `emergent` — a candidate only; `/unikit-gd-flow` confirms it), and
**flow seeds** (1–3 draft `GOAL`-shaped objectives + the systems each would exercise,
`GOAL → SYS`). Drafts, not registered ids — full method in `references/methods.md`
§ Phase 7.5. The seeds ride into Phase 9's Open Questions / Next Steps for the Flow
axis (`/unikit-gd-explore` flow lens → `/unikit-gd-flow`); brainstorm never writes a
`FLOW.md` or `GD-IDS`.

### Phase 8 — Pre-mortem & Scope → **incremental write**

*Klein's pre-mortem: imagine it is six months out and the project already failed —
treat that as a fact — and list why. The certainty framing surfaces the doubts
optimism normally hides, so you can cut scope down to the part that proves the fun.*

Run **Klein's pre-mortem verbatim** ("six months from now the project failed — that is
a fact — why?" — the certainty framing *is* the technique; `references/methods.md`
§ Phase 8): 8–12 reasons across fun / scope / market / tech / team / **content** (ran
out of content, or it got too slow/expensive to make — the content-velocity risk as a
failure mode). Present the 8–12 reasons as a table (reason · category · real? ·
mitigation — `references/tables.md` § Phase 8); the user marks the real ones; mitigate
only those. Then settle the platform, the **MVP cut** — does the chosen scope match how fast you can actually ship
content? — and the **find-the-fun test** (Cerny: the smallest prototype that proves or
kills the core; `references/methods.md` § Phase 8). **Persist now.**

### Phase 8.5 — Validation Plan & Kill Criteria

*Turn each real risk the pre-mortem found into the cheapest test that proves or kills
it before full production — every test with a pass threshold, a deadline, and explicit
kill-criteria numbers. The goal: spend the least to retire the biggest risk.*

For each **Critical** risk the pre-mortem marked real, design the **cheapest test
that proves or kills it** before building the full game (the test catalogue — fake-door
Steam page / prototype / Discord poll / capsule A/B, each with its typical signal — in
`references/methods.md` § Phase 8.5). Each test names a **pass threshold + deadline +
the risk it retires**. State **2–4 explicit kill criteria with numbers** (reuse the
Phase 3.5 brief's benchmarks, e.g. genre wishlist medians). Present both as tables — the
validation tests and the kill criteria — per `references/tables.md` § Phase 8.5. This is where a
low-confidence market bet from Phase 4 gets a cheap real-world check instead of a
taste call. Record the tests and kill criteria in the card's **`## Notes`** — **no
separate file** (brainstorm owns one card, not a research bundle).

### Phase 9 — Record & Handoff

*Lock the finished concept into one approved CONCEPT card and hand off to the next
step. The card is the only artifact that survives the session, so it must carry the
reasoning and the market evidence, not just the verdict.*

Present the **complete CONCEPT card** for **one approval** ("not yet" → edit
sections, do not split the approval). When Phase 3.5 ran, the card must carry the
**market evidence** so it is traceable: the **six machine fields** (`market_signal`,
`validation_confidence`, `clone_density`, `trend_fit`, `monetization_fit`,
`recommendation`) in the header block **and** the distilled argument in `## Notes` (no
`researches/` file was written — the card *is* the citation). Set the card header
(`> Status: drafted · Version: 1 · Created: <date>`).

Also set the **descriptive `genre:` hint** in the header — a human genre name
inferred from the concept (the elevator-pitch *[genre]* slot, e.g. «симулятор
ломбарда», «match-3 головоломка»). It is an **intent, not a catalog id**: write
what the game *is*, even if no genre-profile is named that. `unikit-gd-spec`
resolves this hint best-fit to a bundled profile and installs it downstream.
**Brainstorm stays CLI-free here** — it never runs `unikit-ai genres list` /
`genres install` and never recommends or installs a profile; the genre catalog is
consumed at spec, not here (this avoids the chicken-and-egg of an empty profile
before install). Leave `genre:` empty/soft when no clear genre — `unikit-gd-spec`'s
universal baseline covers it.

Set the INDEX row status to `complete`. Then recommend the follow-up (do not auto-invoke).

## Writing the Artifacts

```bash
mkdir -p .unikit/gamedesign/concepts/<slug>
```

- **`CONCEPT.md`** — the nine-field card with a `## Notes` section for the reasoning
  the table cannot hold (rejected alternatives, inspirations, the Phase 3.5 market
  argument, the Phase 8.5 validation tests). When Phase 3.5 ran, the header carries a
  **machine block** with the six machine fields (`market_signal`,
  `validation_confidence`, `clone_density`, `trend_fit`, `monetization_fit`,
  `recommendation`) **outside** the nine-field table (the table stays "nine fields, no
  more"). These underscore fields are *evidence* — distinct from the hyphenated
  `market-signal` Pugh *criterion*.
  Header: `> Status: <exploring|drafted|approved> · Version: 1 · Created: <date>`.
  Also a `> genre: "<descriptive hint>"` header field — the human genre name
  (intent, not a catalog id; Phase 9). CLI-free: brainstorm writes the hint only;
  `unikit-gd-spec` resolves it to a profile and installs it.
- **`IDEAS.md`** — the rejected-idea backlog: each entry is *idea · essence ·
  reason (scope / not-fun / off-theme / duplicate) · revival condition*.
- **`concepts/INDEX.md`** — prepend (newest first) a row:
  `slug · title · keywords · status · last phase · market_signal` (the last column
  blank when Phase 3.5 was skipped). Create with a
  `> Auto-maintained by /unikit-gd-brainstorm. Do not edit manually.` header if
  absent. Update the existing row's status/phase on resume.

## Final: Compact Report & Next Steps

The terminal plaque (TIER A — `gd-principles` → Language: names lead, status is a plain
phrase; the pillar ids live in GAME.md / GD-IDS):

```
Concept: <title>  (.unikit/gamedesign/concepts/<slug>/)
Status: <still a draft | approved>  ·  reached phase 9
Pillars: <name>, <name>, …   Anti: <n>   MDA: <primary>/<secondary>
Find-the-fun: <the prototype that proves the core>
Rejected → IDEAS.md: <n>
```

**Next steps** (do not auto-invoke):

- 🗺️ Build the master spec — /unikit-gd-spec <slug>
- 🔬 Research a reference or the market — /unikit-gd-explore <topic>

Prototype-first is also valid — validate the find-the-fun before specing.

No summary document, no report file.

## Ownership Boundaries

- **Owns:** `.unikit/gamedesign/concepts/` — `CONCEPT.md`, `IDEAS.md`, and the
  concepts `INDEX.md`.
- **Not this skill:** `GAME.md` + the system map → `unikit-gd-spec`; analyzing an
  existing game/market → `unikit-gd-explore`; per-system GDDs →
  `unikit-gd-system`.
- **Never:** write a concept without approval; offer `promoted`/`abandoned`
  concepts for resume; read the code workspace or project source.

## Quick Reference

```
/unikit-gd-brainstorm                         → blank-page ideation (or resume from index)
/unikit-gd-brainstorm cozy farming roguelike  → seed divergence with a hint
/unikit-gd-brainstorm                         → auto-resumes a matching in-progress concept
```
