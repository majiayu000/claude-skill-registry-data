---
name: unikit-gd-explore
description: >-
  Research and ideation partner for GAME DESIGN — think through design ideas before writing
  them into the GDD; produces a brief, never edits the GDD itself. Use to assess a genre or
  market for viability, dissect a reference game (mechanics → dynamics → aesthetics), explore
  how to improve or extend an existing system, flow, or content type, research new mechanics
  the design lacks, investigate a part of the GDD in code, or develop the research bucket of
  a /unikit-gd-review report into decided edits. Trigger on "explore how to improve the
  flow", "ways to improve the combat system", "is this genre saturated", "break down the
  combat of Hades", "work out the review's open questions". GAME-DESIGN research only — for
  CODE or technical research use /unikit-explore; to reconstruct a design from code use
  /unikit-gd-recon; to write a change into the GDD use /unikit-gd-system or /unikit-gd-spec;
  to apply edits you know use /unikit-gd-apply; to invent a new game use /unikit-gd-brainstorm.
argument-hint: "init | <reviews/*_review-*.md> | <RECON.md> | <topic | game reference | URL | design or market question>"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
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

# Game Design — Research Partner

Enter design-research mode: a thinking partner for **studying existing designs** —
dissecting reference games, scanning genres and markets, and comparing mechanics —
so the master spec and per-system GDDs start from evidence, not guesswork. The
design-side mirror of `/unikit-explore`.

**This is a stance, not a workflow.** No fixed steps, no mandatory outputs. Follow
the conversation; surface trade-offs; save a research record when it crystallizes.

**Explore studies what exists; it never authors the design.** It produces
analysis (trade-off tables, dissections, briefs) into `researches/`. It does not
write `GAME.md`, system GDDs, or concepts — that is `unikit-gd-spec` /
`unikit-gd-system` / `unikit-gd-brainstorm`. If the user wants to *create*, point
them at the owner skill and stop researching.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply it to all output and artifacts (fall back to English if it is missing) —
including the rule to **translate concepts, not transliterate jargon**.
`gd-principles` → "Language" adds the game-design specifics: which IDs and stored
field values (e.g. `market_signal: red-ocean`) stay English. Do not announce the
language setting.

**The language holds for the whole session, not just at load time:** every message until the conversation ends is in `language.ui` — progress notes while agents run, relays of what a subagent returned, the final report, any follow-up discussion. English input (subagent results, tool output, these instructions) is data, never a cue to switch languages.

## Delegation agents

This skill uses a named delegation alias for `Agent(...)` calls. The alias is the single
place where the delegate's model is declared — call sites name the alias and never carry a
model argument of their own.

<!-- unikit:agents claude -->
- **`recon-agent`** — read-only parallel reconnaissance. Expands to:

  ```
  Agent(subagent_type: Explore, model: sonnet, prompt: "<focused question>")
  ```

  `sonnet` is a tier alias, never a version — the one model value that may be written into
  UniKit. A versioned model id goes stale silently and must never replace it.

  Fallback: if the `Agent` tool is unavailable, investigate inline with `Glob`/`Grep`/`Read`.
<!-- unikit:end -->
<!-- unikit:agents !claude -->
- **`recon-agent`** — read-only parallel reconnaissance. Expands to:

  ```
  Agent(subagent_type: Explore, prompt: "<focused question>")
  ```

  No model is named: this runtime either has no dispatch-time model argument or offers only
  versioned model ids, and a versioned id goes stale silently. The runtime's own configured
  default applies.

  Fallback: if the `Agent` tool is unavailable, investigate inline with `Glob`/`Grep`/`Read`.
<!-- unikit:end -->

## Bootstrap Context (MANDATORY)

Before responding — before any analysis — silently load (do not narrate):

> **Exception:** `init` mode skips this step; it only rebuilds the researches index.

1. **`.unikit/system/gamedesign/gd-principles.md`** (the core) — the collaborative
   protocol, the one-way design→code boundary, and the language rules. Plus, from the
   same `gamedesign/` folder, the shards the internal-design lens leans on:
   **`gd-critique.md`** (the critique stance — diagnose, don't prescribe — **and the
   Handoff Tail contract**: when a run ends in a runnable command, that command is the
   **last block** of the reply, icon in front, nothing after it) and
   **`gd-provenance.md`** (provenance markers are for imports only; explore-seeded
   drafts stay untagged). This skill **applies** it. If missing, warn
   (`unikit-ai update`) and continue with the protocol summarized above.
2. **`.unikit/gamedesign/GD-IDS.yaml`** and **`GAME.md`** (incl. its `## System Map
   [gen]` render) (if they exist) — the current design, so research is grounded in
   this game's pillars and systems rather than generic theory. Absent → this is
   pre-spec research; proceed. **Schema guard:** if `GD-IDS.yaml` is a pre-v2
   `version: 1` registry, do **not** read it for grounding — emit a loud `WARN
   [design] GD-IDS.yaml is version 1 (pre-v2 layout); design grounding skipped` and
   proceed as pre-spec research (the v2 clean break has no automatic migration;
   upgrade via `/unikit-gd-spec`).
3. **`.unikit/memory/gamedesign/RULES_INDEX.md`** — load core domain rules on
   demand by `Load When` for the topic (e.g. `frameworks` for an MDA dissection,
   `economy` for an economy study, `player-motivation` for an audience scan). Obey the
   index's **Rule-Loading Discipline**: load by `Load When`, load a reference only from
   its parent rule's `> **References**:`, and **never glob the memory tree**
   (`.unikit/memory/gamedesign/**`) to discover rules.
4. **`.unikit/DESCRIPTION.md`** / **`.unikit/ROADMAP.md`** (optional) — project
   constraints and milestones; routing context only.
5. **`.unikit/gamedesign/researches/INDEX.md`** (optional) — prior researches;
   check for related work before starting fresh.
6. **`{{skills_dir}}/{{self_name}}/references/market-scan.md`** — the
   market-research engine (the *how* of a scan). Load it **only when the prompt
   carries market intent** — the "Market lens — when it engages" section below
   classifies this. A design-only prompt does **not** load it; this keeps reference
   dissection lean.
7. **`{{skills_dir}}/{{self_name}}/references/internal-design-lens.md`** — the
   own-design research engine (the deep-read protocol, the domain→rules table, the
   options form, the open-questions registry + closure pass, the two brief blocks,
   and the research tags). Load it **only when the prompt carries internal-design
   intent** — improving an existing system or working out a new mechanic for *this*
   game — as the "Internal design lens — when it engages" section below classifies,
   **or when the argument is a `reviews/*_review-*.md` file** (research-bucket mode —
   see "Research-bucket mode" below; each research finding is developed through this
   same engine) **or a `RECON.md` file** (RECON-input mode — the pre-GDD carve-out where
   the reconstruction *is* the candidate design surface; see "RECON-input mode" below).
   When the lens engages, also deep-read the target per that engine
   (GAME.md + its `## System Map [gen]` + GD-IDS + the target `SYS-<slug>.md` A–K + the
   Depends-neighbours' D/F).
8. **`{{skills_dir}}/unikit-gd-recon/references/code-recon.md`** — the shared `code →
   design-fact` engine, **owned by `unikit-gd-recon`** and read here (the same
   provider-owns-spec pattern by which `unikit-gd-brainstorm` reads this skill's
   `delegation-contract.md`). Load it **only when the code-grounded lens engages** (the
   prompt asks how something is built in *this project's code* — see "Code-grounded lens
   — when it engages"). It supplies the extraction heuristics (engine inference, P0
   systems / P1 content, the per-fact `confidence` + source-pointer + `provenance:
   extracted from code` record).

**One-way boundary (with the code-lens exception):** the authoring zones never read
code, but this skill is a **read-only research verb** — its **code-grounded lens**
(below) *does* read project source and asset definitions to ground an in-flight design
slice, the same sanctioned third exception `unikit-gd-recon` uses (`gd-principles` →
One-Way Boundary). Outside that lens, do not read `.unikit/code/` or build artifacts.
Web research **is allowed** here (market and reference scans — `gd-principles`).

### Parallel investigation

For broad topics, launch **inline `recon-agent`** dispatches to
gather reference material in parallel (one per game/genre/angle), then synthesize:

```
recon-agent(prompt:
  "Research <game/genre/mechanic>. Report: core loop, key systems, the standout
   design choices and the trade-offs they make. Cite sources. Be concise — a
   structured summary, not raw dumps.")
```

**Fallback:** if the Agent tool is unavailable, use `WebSearch` / `WebFetch`
directly. Agents and web fetches are read-only advisors — they never write files.
**When this skill is itself running as a spawned subagent** (serving a brainstorm
delegation — see "Serving a brainstorm request"), prefer **direct `WebSearch` /
`WebFetch`** over a nested `recon-agent`: nested spawning from
inside a subagent is unreliable.

## The Stance

- **Analytical, not generative** — explain *why* a design works, name the
  trade-off it makes; ideation belongs to `unikit-gd-brainstorm`.
- **Evidence over opinion** — cite the game, the mechanic, the source; a claim with
  no reference is a hypothesis, mark it as one.
- **Visual** — use ASCII diagrams and comparison tables liberally.
- **Grounded** — anchor every finding to this game's pillars/systems when a design
  exists, or to the stated research question when it does not.

## What You Might Do

**Reference dissection (MDA backwards).** The core technique: take a reference game
and read it **mechanics → dynamics → aesthetics** — from the rules and systems
(mechanics), to the runtime behavior they produce (dynamics), to the felt
experience (aesthetics). This reveals *why* a design feels the way it does and what
is portable versus incidental.

```
MECHANICS            →   DYNAMICS                →   AESTHETICS
(rules, systems)         (emergent behavior)         (the felt experience)
card draft + energy  →   deckbuilding tension    →   Challenge, Expression
permadeath + meta    →   run-to-run escalation   →   Discovery, Submission

  "What to borrow: <portable mechanic>.  What is incidental: <bound to its IP/scope>."
```

**Genre / market scan.** Survey how a genre solves a problem — the spread of
approaches, the conventions players expect, the saturated vs open niches. When the
prompt is **commercial** (viability, audience, competition, demand, platform-fit),
this becomes a full **market scan** — see "Market lens — when it engages" below.

**Mechanics comparison.** Build trade-off tables (each option × axes like depth,
readability, dev-cost, retention, audience). Recommend a path **only if asked**
(`gd-principles` anti-anchoring).

**Surface risks & unknowns.** Name what a design choice would cost, what is unproven,
what needs a prototype.

## Market lens — when it engages

The market lens is **inferred from the prompt, never a flag** — `argument-hint`
stays free-form. Classify the request by its signals:

| Signal class | Triggers (examples) |
|--------------|---------------------|
| **Viability** | "is there a market", "will it sell", "worth making", monetiz* |
| **Discoverability / audience** | discoverability, wishlists, "who buys this", audience, reachable players, TAM |
| **Competition / saturation** | competitors, comparables, "saturated", red ocean, white space, differentiation |
| **Demand** | demand, "do players want this", "are they asking for it" |
| **Platform / store** | Steam tags, store page, genre fit on a platform |

**Decision rule:**

- **Market signals present** → market lens **ON**: load `market-scan.md` and run its
  techniques alongside (or instead of) MDA dissection.
- **Only design signals** (a game name / URL / "break down the combat" / "compare
  mechanics" / pure MDA) → **MDA dissection**; `market-scan.md` is **not** loaded.
- **Both** → run **both** lenses.

**Tie-breaker (genuine ambiguity only).** When the prompt is clearly a decision
question but the *cut* is unclear and the two readings mean materially different
work, ask **one** question — not one per ambiguous prompt:

```
AskUserQuestion: What kind of read do you want?
Options:
1. Design dissection (recommended)
2. Market viability
3. Both
```

"Always run both lenses" is rejected — it breaks the conditional load. This
tie-breaker is **skipped entirely** in subagent mode (next section).

## Internal design lens — when it engages

The third lens points **inward** — at *this* game's own design — rather than at a
reference game (MDA dissection) or the market. It engages when the prompt asks to
improve a system already in the GDD or to work out a new mechanic for the game. Like
the market lens it is **inferred from the prompt, never a flag**. The engine — the
deep-read protocol, the domain→rules table, the options form, the open-questions
registry + closure pass, the two brief blocks — lives in
`references/internal-design-lens.md`; this section is the **switch**.

| Signal class | Triggers (examples) |
|--------------|---------------------|
| **Improve an existing system** | "improve our combat", "доработать баланс боя", "tune our economy design", "rethink the status system", "make X deeper" |
| **New mechanic for this game** | "research a crafting mechanic for us", "проработать новую механику", "what new system could serve PIL-2", "explore a mechanic to add" |
| **Close a design question** | "work through the open question on X", "resolve the trade-off in SYS-y" |
| **Improve an existing flow** | "improve the onboarding", "fix the first-session pacing", "rework this flow's guidance", "доработать прогрессию" |
| **New player-facing flow** | "design the first-session flow", "map a new player sequence for us", "what flow would serve PIL-2" |
| **Improve existing content** | "improve our item catalog", "rework the loot schema", "доработать каталог предметов", "rethink the CT-item fields" |
| **New content area** | "design the item types for us", "what content schema would serve SYS-inventory", "plan a new catalog of enemies", "проработать каталог контента" |

The tell is the **possessive frame** — *our / this game / SYS-id / a pillar* — which
separates this lens from dissecting someone else's game.

**Decision rule:**

- **Internal-design signals present and `GAME.md` exists** → internal lens **ON**:
  load `internal-design-lens.md`, deep-read the target, run the lens flow.
- **Combinable.** The lens runs **alongside** MDA dissection (dissect a reference to
  inform *our* design) and the market lens (is the improvement worth it commercially)
  — load whichever the prompt also triggers.
- **No `GAME.md` yet** → this is **not** internal design but pre-spec research →
  point at `/unikit-gd-brainstorm` (a whole new game) or `/unikit-gd-spec` (start the
  master spec); do not load this engine. **Exception — the RECON carve-out:** when the
  argument resolves to a `RECON.md` file, the reconstruction *is* the candidate design
  surface, so the lens **does** engage even with no `GAME.md` — run "RECON-input mode".
- **No internal signal** (a reference name / "break down X" / a market question with
  no "our/this game" framing) → internal lens **OFF**.

**Read-only — say it on entry.** When the lens engages, state once that this is
research: *"I'll work this through and hand you a brief — I won't edit the GDD; the
change goes through the routed skill."* Repeat the boundary at handoff.

**3-way handoff routing (explore reads the target's state — the user does not pick).**
Read the target's `doc_status` from `GD-IDS.yaml` (the `## System Map [gen]` render
mirrors it), then recommend the **one** command that fits. Each route is a single
recommended command; the routed skill carries its own next hop.

| Target state (`doc_status`) | Recommended route |
|-----------------------------|-------------------|
| no doc / `not-started` | `/unikit-gd-spec` (add-system) — it offers the active seam onward to `/unikit-gd-system` |
| `skeleton` (placeholders) | `/unikit-gd-system` (fill the placeholders) |
| `detailed` | `/unikit-gd-system` (record the delta) |

The brief carries the block the route consumes (see "Saving Research Results" →
mode-aware blocks). For several targets, hand off an **ordered list** of calls,
dependency-sorted (`internal-design-lens.md` → "Multi-target order").

**Flow targets collapse to one route (no add-flow).** A flow **registers itself**, so
its `doc_status` does **not** fork the route the way a system's does — every flow state
(no doc / `not-started` / `skeleton` / `detailed`) routes to
the **same** owner, `/unikit-gd-flow` (it creates, registers, fills, and revises). This
is **not** a 3-way mirror of the system table — there is no `/unikit-gd-spec` add-flow
step:

| Target state (`doc_status`) | Recommended route |
|-----------------------------|-------------------|
| any flow state (no doc … `detailed`) | `/unikit-gd-flow` |

The brief block is `## Flow Feature Plan` (no doc / `not-started` / `skeleton` — needs
seeds) or `## Flow Improvement Plan` (`detailed` — a delta). A
`GOAL` that needs a **missing system** still routes that *system* through
`/unikit-gd-spec` add-system, but the flow itself always goes to `/unikit-gd-flow`.

**Content targets collapse to one route (no add-content).** A content type **registers
itself**, so — like a flow — its `doc_status` does **not** fork the route: every content
state (no doc / `not-started` / `skeleton` / `detailed`) routes
to the **same** owner, `/unikit-gd-content` (it creates, registers, fills, and revises
the schema). There is no `/unikit-gd-spec` add-content step:

| Target state (`doc_status`) | Recommended route |
|-----------------------------|-------------------|
| any content-type state (no doc … `detailed`) | `/unikit-gd-content` |

The brief block is `## Content Feature Plan` (no doc / `not-started` / `skeleton` — needs
seeds) or `## Content Improvement Plan` (`detailed` — a schema
delta). A `belongs_to` that needs a **missing system** still routes that *system* through
`/unikit-gd-spec` add-system, but the content type itself always goes to
`/unikit-gd-content`.

## Code-grounded lens — when it engages

The fourth lens grounds a design slice against **this project's own code** — when the
question is not "how does *another* game do this" (MDA) or "is it worth it" (market) but
**"how is *our* X actually built?"**. It is the **post-GDD, targeted** counterpart to
`unikit-gd-recon`: where recon is a strictly cold-start, whole-project bootstrap (no GDD
yet → one passive `RECON.md`), this lens runs **when a GDD already exists** and reads only
the **slice** the prompt names, to inform an in-flight design decision. Like the other
lenses it is **inferred from the prompt, never a flag**, and it **combines** with the
internal-design lens (read the design intent *and* the code reality together).

| Signal class | Triggers (examples) |
|--------------|---------------------|
| **How is our X built in code** | "how is loot actually wired in the code", "what does our combat system really do", "как в коде устроен инвентарь" |
| **Reconcile design vs implementation** | "does the code match the combat GDD", "what fields does the item asset actually have", "is the economy in code the one we designed" |
| **Ground an improvement in reality** | "improve our loot — but check how it's built first", "before we retune, what's the code actually doing" |

The tell is a **possessive frame pointed at the implementation** — *our code / how it's
built / what the asset actually has* — separating it from MDA's "another game".

**Decision rule:**

- **Code-grounded signal present and `GAME.md` exists** → code lens **ON**: load
  `unikit-gd-recon/references/code-recon.md`, scan **only the named slice** with
  `recon-agent` (fallback: inline `Glob`/`Grep`/`Read`), and fold the
  code findings into the brief.
- **No `GAME.md` yet** → this is the **cold-start** case → **do not** use this lens;
  point at `/unikit-gd-recon` (whole-project reconstruction) instead. Recon owns cold
  start; this lens owns the in-flight slice.
- **No code-grounded signal** → code lens **OFF** (it never reads code uninvited).

**Read-only and code-provenance-tagged.** This lens reads code; it **never** edits the
GDD and **never** writes code. Facts it lifts **directly from code** into the brief carry
`provenance: extracted from code` (review holds them ≥ Major — `gd-provenance`), exactly
as a `RECON.md` would; the designer's own options and reasoning in the same brief stay
**untagged**. This keeps the two read-only research verbs symmetric — code-origin is
tagged identically whether recon or this lens surfaced it. Say it on entry, as the
internal-design lens does: *"I'll read how it's built and hand you a brief — I won't edit
the GDD or the code."* Its routing is the internal-design lens's (the slice's
`doc_status` picks the owner); in **subagent mode** every interactive `AskUserQuestion`
is bypassed, the same as the internal-design lens.

## Input modes — develop a review file or a RECON reconstruction

Two argument shapes put this skill into an **input mode**: it consumes a specific file
the pipeline hands it, develops it through the internal-design lens
(`references/internal-design-lens.md`), and ends with **one** handoff command (the
Handoff Tail contract — `gd-critique`). Both are **read-only on the GDD**; the
subagent-mode bypass applies (no interactive closure-pass questions when spawned). Load
the matching body on demand — do **not** keep both in context:

| Argument resolves to | Mode | Reference body |
|----------------------|------|----------------|
| an existing `reviews/*_review-*.md` file | **Research-bucket mode** — develop a `unikit-gd-review` report's `## Research` bucket **in place** (promote each decided finding into `## Apply-ready`), then recommend `/unikit-gd-apply reviews/<file>.md` | `{{skills_dir}}/{{self_name}}/references/mode-research-bucket.md` |
| a `RECON.md` file | **RECON-input mode** — develop a `unikit-gd-recon` cold-start reconstruction (the pre-GDD carve-out), save the research as usual + a `## Explorations` backlink, then recommend `/unikit-gd-spec <RECON.md>` import | `{{skills_dir}}/{{self_name}}/references/mode-recon-input.md` |

Both write into a file this skill does **not** own (the `reviews/*_review-*.md` report;
`RECON.md`) — the sanctioned cross-skill writes recorded in Ownership below.

## Serving a brainstorm request (subagent mode)

`unikit-gd-brainstorm` delegates market validation to this skill by spawning it as a
subagent. This section is the SKILL-level switch. **Detect delegation by the canonical
marker** — the prompt contains, verbatim, on one line:

> **"Return the brief into this session as text; do not save any files."**

Detection is by this **exact phrase**, not a loose reading. On a match, **load
`references/delegation-contract.md`** (this skill's own spec — provider-owns-spec; the
engine behavior is `references/market-scan.md` → "Subagent mode") and follow it: run
**deterministically**, **bypass every interactive `AskUserQuestion`** (the lens
tie-breaker above, the save-offer under "Saving Research Results", and the
internal-design / code-grounded closure passes — a subagent would hang on any prompt),
run the **market lens** (per-concept `market_signal` + `validation_confidence` +
evidence), and **return the brief into the session as text — save no file** (skip the
save step; the calling session owns persistence). Prefer direct `WebSearch` /
`WebFetch` over a nested `recon-agent` (see "Parallel investigation").

## Saving Research Results

When the conversation crystallizes, **offer** to save (never auto-save) — then **load
`{{skills_dir}}/{{self_name}}/references/save-research.md` and follow it**. That body
holds the artifact templates (`RESEARCH_RESULT.md` with its `Target:` / `Kind:`
discovery tags, `RESEARCH_BRIEF.md`), the **Next Steps routing** table, and the
`researches/INDEX.md` update format. When the research came from the **internal design
lens**, the brief gets the **one** mode-aware block matching the resolved route — the
block field lists live in `references/internal-design-lens.md` → "Mode-aware brief"
(the single source of truth; do not duplicate them).

## Init: Rebuilding the Researches Index

When the argument is exactly `init`, **load
`{{skills_dir}}/{{self_name}}/references/init-index.md` and follow it** — a maintenance
command (no exploration) that syncs `.unikit/gamedesign/researches/INDEX.md` with the
directory (keep / remove / add entries, carry any `Target:` tag), reports
`Kept N · Added N · Removed N`, then **STOPs**.

## Ending

No required ending. It might flow into a saved research, into
`/unikit-gd-spec` / `/unikit-gd-brainstorm`, or just provide clarity. When things
crystallize, you might summarize the findings — but the thinking is often the value.

## Ownership Boundaries

- **Owns:** `.unikit/gamedesign/researches/` — `RESEARCH_RESULT.md`,
  `RESEARCH_BRIEF.md`, and the researches `INDEX.md`.
- **Owns (spec):** `references/delegation-contract.md` — the brainstorm→explore
  contract. This skill is its provider; brainstorm reads it as the interface. Keep its
  canonical marker and brief field-list in sync with `references/market-scan.md`.
- **Internal design lens (read-only).** The lens (`references/internal-design-lens.md`)
  deep-reads `GAME.md` / `GD-IDS.yaml` (+ its `## System Map [gen]` / `## Flow Map [gen]` /
  `## Content Map [gen]` renders) / system docs / flow docs / content-type docs and hands
  off a brief — it **never** writes the GDD, and it **never** writes the `research:`
  pointer into `GD-IDS.yaml`; that pointer is owned by the registering zone
  (`unikit-gd-spec` add-system for a **system**, `unikit-gd-flow` for a **flow**,
  `unikit-gd-content` for a **content type** — there is no add-flow / add-content).
  Explore only **tags** its own research (`Target:` / `Kind:`).
- **Read-only:** `GAME.md`, `GD-IDS.yaml`, systems, flows, content types, concepts —
  route any design change to its owner skill, never edit them here.
- **Research-bucket mode (in-place promotion).** Developing a `unikit-gd-review`
  report's `## Research` bucket turns each open finding into a decided edit and **promotes
  it in place** — moving the line into the report's `## Apply-ready` bucket (reformatted as
  `RF-<date>-n · <target> · Fix (entailed): <edit>`) and appending the worked-out brief —
  then **recommends** the single file command `/unikit-gd-apply reviews/<file>.md`
  (printed, never invoked: there is no `Skill` tool here). This in-place promotion is a
  **sanctioned write into a file this skill does not own**: the `reviews/*_review-*.md`
  report belongs to `unikit-gd-review`. It writes **nothing else** — not the GDD, not
  `researches/` (this review-file mode never opens a `researches/` folder).
- **RECON-input mode (research + backlink).** Developing a `unikit-gd-recon` `RECON.md`
  (the pre-GDD carve-out) saves the research the **normal** way (`researches/<slug>/`)
  and appends a `research:` **backlink** into RECON.md's `## Explorations` section — a
  **sanctioned write into a file this skill does not own** (`RECON.md` belongs to
  `unikit-gd-recon`), limited to that section. It then recommends `/unikit-gd-spec
  <RECON.md>` import. This is the **asymmetry** with review-file mode: a review file is
  mutated in place (no `researches/`); RECON.md is durable, so the research is saved as
  usual and only a pointer is written back.
- **Code-grounded lens (read-only).** When the code lens engages, this skill reads
  project source and asset definitions — the sanctioned third exception to the one-way
  boundary (`gd-principles`), shared with `unikit-gd-recon`. It reads only the **named
  slice** (post-GDD), folds code findings into a brief tagged `provenance: extracted from
  code`, and **never** edits the GDD or the code. Cold-start, whole-project
  reconstruction is `unikit-gd-recon`'s, not this lens's.
- **Not this skill:** generating new concepts → `unikit-gd-brainstorm`; authoring
  the spec/systems/flows/content → `unikit-gd-spec` / `unikit-gd-system` /
  `unikit-gd-flow` / `unikit-gd-content`; cold-start code reconstruction →
  `unikit-gd-recon`.
- **Never:** author or edit a design document; auto-save a research; read the code
  workspace or project source **outside the code-grounded lens** (that lens is the one
  sanctioned read — `gd-principles` third exception).

## Quick Reference

```
/unikit-gd-explore                              → enter design-research mode
/unikit-gd-explore break down the combat of Hades   → reference dissection (MDA backwards)
/unikit-gd-explore roguelike meta-progression       → genre / mechanics scan
/unikit-gd-explore is this roguelike niche saturated?  → market lens (viability / white-space)
/unikit-gd-explore improve our combat balance        → internal design lens (read-only) → routes to system / spec
/unikit-gd-explore how is our loot wired in the code → code-grounded lens (read-only, post-GDD slice) → brief
/unikit-gd-explore reviews/2026-06-25_review-SYS-combat.md → promote ## Research into ## Apply-ready in place → /unikit-gd-apply reviews/X.md
/unikit-gd-explore .unikit/gamedesign/RECON.md      → develop the cold-start reconstruction (pre-GDD) → save research + ## Explorations backlink → /unikit-gd-spec import
/unikit-gd-explore https://…                         → dissect a linked design source
/unikit-gd-explore init                              → rebuild researches/INDEX.md
```
