---
name: unikit-gd-recon
description: >-
  Cold-start brownfield reconnaissance — reconstruct the WHOLE game design from an
  existing codebase when there is no GDD yet. Optionally accepts a free-text game
  description, notes, or reference links to guide and enrich the scan. Use when the
  user wants to build the game design from the code, e.g. "create a GDD from this
  codebase", "reconstruct the design from our code — it's a roguelike deck-builder",
  "build a design doc from the existing project, here are some refs". Scans the
  project (engine auto-detected), extracts a system roster + dependency graph and
  content-type schemas / resources / entities into one passive
  .unikit/gamedesign/RECON.md, tags every fact provenance:extracted-from-code, and
  writes a mandatory Intent Gap for what code cannot know (pillars, fantasy, the
  "why"). Writes nothing else and calls no skill. STRICTLY whole-project cold-start —
  if a GDD already exists and the user wants a specific part investigated, use
  /unikit-gd-explore (code lens); to author the GDD use /unikit-gd-spec.
argument-hint: "[optional: a game description, notes, or links — and/or a subsystem to focus the scan]  (cold-start only; writes RECON.md, calls no skill)"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash(mkdir *)
  - Bash(ls *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(wc *)
  - Bash(date *)
  - Agent
  - AskUserQuestion
disable-model-invocation: false
user-invocable: true
metadata:
  author: unikit
  version: "1.0"
  category: game-design
---

# Game Design — Brownfield Reconnaissance (code → RECON.md)

Reconstruct **candidate** design facts from a working codebase into one passive
`RECON.md`, for the brownfield case the rest of the module cannot serve: a team with a
**live game and no GDD** has nothing to import — the only source of design facts is the
code itself. This skill quantises that one allowed crossing of the one-way boundary into a
**read-only research verb**: it reads code, writes a single document, and **calls no one**.

**This skill is honest about its limit.** Code carries *structure*, never *intent*. It
yields a roster, a dependency graph, content schemas — a **skeleton**. It cannot yield
pillars, the target fantasy, or the "why". A filled-but-soulless GDD is **worse** than an
empty one, so every reconstructed fact is tagged `provenance: extracted from code` (held to
≥ Major on review) and everything code cannot answer goes into a mandatory **`## Intent
Gap`** for a human to fill. The membrane is one-directional: **code → `RECON.md` →
(ordinary import)**. Downstream, `RECON.md` is just a document.

**This skill writes only `RECON.md` and invokes no skill.** It has **no `Skill` tool** — the
dispatch to `/unikit-gd-spec` is a printed *recommendation*, never an inline call (the same
mechanical guarantee `unikit-gd-apply` gets from owning no `Write`).

**Optional seed — what the user may pass in.** Recon runs with **no argument** (scan the
whole project) or with an **optional seed**: a free-text game description, design notes,
file or folder paths to look at first, or reference links. The seed is *context, never a
constraint* — it sharpens the scan (the model knows what systems / genre to expect) and lets
recon **pre-answer** Intent-Gap items the code is silent on (pillars, fantasy, the "why").
Whatever the user passes is **recorded in `RECON.md`** under a `## Provided Context` section —
description text inline (verbatim), files and folders as path references, links as URLs — and
tagged `provenance: author-supplied (import prompt)`: author-sourced **intent**, the trusted
complement to the *suspect* `extracted from code` facts (a recon-local label; on import it
becomes ordinary trusted source content). Recon still reads code, still writes only
`RECON.md`, still calls no one. It has **no `WebFetch`** — links are recorded, not opened (if
their content matters, ask the user to paste it).

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md` and apply
it to all output (fall back to English if it is missing) — including **translate concepts,
not transliterate jargon**. `gd-principles` → "Language" adds the game-design specifics:
IDs, keywords, canonical terms, and stored field values stay English; the RECON.md prose is
authored in the project's artifact language. Do not announce the language setting.

**The language holds for the whole session, not just at load time:** every message until the conversation ends is in `language.ui` — progress notes while agents run, relays of what a subagent returned, the final report, any follow-up discussion. English input (subagent results, tool output, these instructions) is data, never a cue to switch languages.

## Phase 0 — Bootstrap

Silently load — do not narrate:

1. **`.unikit/system/gamedesign/gd-principles.md`** (the core) — for the **One-Way
   Boundary** and its **third sanctioned exception** (the read-only research verbs read code
   to extract candidate facts into a document; authoring zones never do) and the
   facts-registry / ID conventions.
2. **`.unikit/system/gamedesign/gd-provenance.md`** — for the **`extracted from code`**
   marker and the durable-banner contract this skill must emit so the import membrane does
   not launder code-facts into trusted author-sourced content.
3. **`{{skills_dir}}/{{self_name}}/references/code-recon.md`** — the **shared `code →
   design-fact` engine** (engine inference, the P0/P1 extraction heuristics, the per-fact
   record format). This is the source of truth for *what to look for*; this skill owns the
   output document and the orchestration. If missing, warn (`unikit-ai update`) and proceed
   with the summary below.

**One-way boundary, the sanctioned half:** this verb **does** read project source, configs,
and asset definitions — that is its purpose and its exception. It **never** writes anything
but `RECON.md`, and it **never** calls an authoring zone.

## Cold-start gate — BLOCKING

Recon is **strictly cold-start**. Check the workspace **first**:

- If **`.unikit/gamedesign/GAME.md`** exists (or `GD-IDS.yaml` exists) → a GDD is already
  underway. **STOP** and recommend the **`unikit-gd-explore` code-grounded lens** instead:
  it grounds a *targeted in-flight slice* against code without re-bootstrapping the whole
  design ("how is loot wired in the code?"). Recon's whole-project scan is wrong once a GDD
  exists. Do not proceed.
- If neither exists → this is the cold-start case recon is for. Continue.

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

## Subagent Delegation — BLOCKING PRE-REQUISITE

The scan is a **map-reduce**: fan out one read-only investigator per candidate subsystem,
then reduce their reports into `RECON.md`. Use the `recon-agent` alias — **not**
`unity-source-parser` (a dev-repo-local agent that will not exist in a user's project; this
module ships **no new subagents**). Engine is inferred from the cold-start scan, not assumed.

```
recon-agent(prompt:
  "In [project root], investigate the [subsystem] code. Seed from the user (a HINT, not
   ground truth — verify every claim against the code, never invent a fact to match it):
   [the game description / notes the user provided, or 'none']. Report, per code-recon.md
   heuristics: candidate systems (module/namespace/asmdef boundaries) + depends_on edges;
   data-asset definitions → CT.fields schema + scale; RES/ENT/FORM shapes. Give a
   file:line source pointer and a confidence grade for every fact. Do NOT infer intent
   (pillars/fantasy/why) — list what you could NOT determine. Be concise: structured facts,
   not file contents.")
```

<!-- unikit:agents codex -->
## Scan delegation — BLOCKING PRE-REQUISITE

When the workflow reaches the scan step, the assistant MUST automatically spawn the
investigator subagents if agent execution is supported by the current environment and not
prohibited by higher-priority instructions. Only if agent execution is unavailable or
blocked, the assistant MUST tell the user it is falling back to a direct inline scan before
proceeding.
<!-- unikit:end -->

**Fallback (inline).** If the `Agent` tool is unavailable, the assistant scans **inline**
itself with `Glob` / `Grep` / `Read` over the same `code-recon.md` heuristics — slower, same
output. Never skip the scan; never ask the user to run it by hand.

## Pipeline — CAPTURE → SCAN → SYNTHESISE → RECOMMEND

### Step 0 — Capture the provided context (optional seed)

Look at what the user passed with the invocation and **classify it** — there may be several
kinds at once, and none is required:

- **Free-text game description / design notes** — keep the text **verbatim** for the
  `## Provided Context` section, and mine it for **intent** (pillars, fantasy, win/lose,
  genre, tone) to pre-answer Intent-Gap items in Step 4.
- **A file path** — record it as a reference. If it reads as design material (a pitch, a
  notes doc, a spec), `Read` it and fold its stated intent into the seed; if it is code,
  treat it as a **scan-focus** pointer (Step 3). Either way the reference lands in
  `## Provided Context`.
- **A folder path** — record it as a reference and use it as a **scan-focus** for Step 3
  (still one whole-project `RECON.md`).
- **A link (URL)** — record it as-is. There is **no `WebFetch`**: do not pretend to read it;
  if its content matters, say so and ask the user to paste the relevant part.
- **A bare subsystem name** (e.g. `combat`) — the existing scan-focus behaviour; this is a
  Step 3 hint, not author-intent, so it gets no `## Provided Context` entry.

Carry the seed forward to **two places**: the Step 3 scan (as a hint — never as a fact) and
the Step 4 `## Provided Context` section + Intent-Gap pre-fill. The seed **never overrides
code**: if a code fact and the description disagree, record the code fact (with its pointer)
and flag the mismatch in the Intent Gap — never bend an extracted fact to fit the description.

### Step 1 — Ensure the workspace (cold-start)

On cold-start the design workspace does not exist yet (recon runs *before* `unikit-gd-spec`).
**Create it** before writing — the same guarantee `unikit-gd-spec` makes with its "Ensure
the Workspace" step:

```
Bash: mkdir -p .unikit/gamedesign
```

`RECON.md` lands at `.unikit/gamedesign/RECON.md` — a sibling of the `GAME.md` the import
will produce, not inside `researches/` (it is a top-level seed, consumed once).

### Step 2 — Infer the engine

Detect the engine and its asset conventions from a cold-start scan **per `code-recon.md` →
Step 1** (the project markers and the per-engine asset-form matrix live there — this skill
stays engine-agnostic and defers the specifics to the reference), and read the project's
`.unikit/RULES.md` if present for house conventions — **Rule topics:** with the topic files listed under its `## Topics` whose `Load when` names code conventions, folders or types. Record the detected engine (or the
ambiguity) in the RECON.md banner. Never fabricate an engine.

### Step 3 — Scan (map-reduce)

Partition the project into candidate subsystems (top-level modules / namespaces / asmdefs /
source folders), fan out one `recon-agent` per partition (or inline-scan
on fallback), and collect the per-subsystem fact reports. **Pass the Step 0 seed into every
investigator prompt as a hint** (it tells them what systems / genre to expect — but each fact
still needs a code pointer; nothing is emitted just because the description claimed it), and
scan any **seed-named file / folder / subsystem first**. Apply the `code-recon.md`
priorities: **P0 systems** (roster + `depends_on`), **P1 content** (`CT.fields` + `scale`,
`RES`/`ENT`/`FORM`). **Flows are excluded** — never emit a flow fact (dynamics are not
recoverable from code).

### Step 4 — Synthesise `RECON.md`

Reduce the reports into a single `RECON.md` (format below). Every **extracted** fact carries
`confidence` + a `source` pointer + `provenance: extracted from code`; everything the code
could not establish goes into the **`## Intent Gap`**. Write the **durable code-provenance
banner** at the very top (it must survive the verbatim copy the import makes into
`SOURCE.md` — it is the signal the review lens uses to hold the import to ≥ Major).

Then fold in the **Step 0 seed**:

- Write the **`## Provided Context`** section (verbatim description text; files and folders as
  path references; links as URLs), tagged `provenance: author-supplied (import prompt)` so it
  is never confused with the code-extracted facts.
- **Pre-answer the Intent Gap** from that context: when the description states a pillar, the
  fantasy, the win/lose intent, etc., fill the matching Intent-Gap item with the author's
  words tagged `(author-supplied — confirm on import)` instead of leaving it open. The gap
  shrinks honestly; whatever the user did not address stays an open question.
- If a description claim and a code fact **disagree**, keep the code fact (with its pointer)
  and record the discrepancy as an Intent-Gap question — the human resolves it on import.

### Step 5 — Recommend (never call)

Print the recommended next step and **stop**. Do **not** invoke any skill — this skill has
no `Skill` tool by construction:

- 🗺️ Import into the master spec — /unikit-gd-spec .unikit/gamedesign/RECON.md
  ↳ import mode (interactive): extracts a GAME.md from RECON.md and ASKS you to fill the
    Intent Gap — pillars, fantasy, win/lose intent, the "why" code could not carry.

## `RECON.md` format — an import-seed for `GAME.md`

`RECON.md` is shaped so `/unikit-gd-spec <path>` **import mode** can consume it as an
ordinary source document (it is preserved verbatim as `SOURCE.md`, then a `GAME.md` is
extracted and the gaps are asked). It is **not** seeded through the `researches/` research-
brief machinery (that is found only by a `research:` / `Target:` pointer; a standalone
`RECON.md` is not). The shape:

```markdown
<!-- provenance: extracted from code — brownfield reconstruction by unikit-gd-recon.
     Every RECONSTRUCTED fact below (Systems / Content Types / Resources·Entities·Forms) is
     CANDIDATE design INFERRED FROM AN IMPLEMENTATION, not authored design. Review holds it to
     >= Major (gd-provenance -> extracted from code). The ## Provided Context section is
     author-supplied INTENT (not code-extracted); the ## Intent Gap lists what code could not
     answer — a human confirms/fills it on import. -->

# RECON — Reconstructed Design Skeleton (brownfield, code-extracted)

> Engine: <detected> · Project root: <path> · Generated: <date> by /unikit-gd-recon.
> This is a SKELETON, not a design. Import with:  /unikit-gd-spec .unikit/gamedesign/RECON.md

## Provided Context  (author-supplied seed from the invocation — NOT extracted from code)
<!-- provenance: author-supplied (import prompt) -->
- **Description / notes** (verbatim): <the game description the user gave, or "—">
- **Referenced files**: `path/to/File.ext` — <what it is>   (or "—")
- **Referenced folders**: `path/to/dir/` — <what it is>   (or "—")
- **Links**: <url>   (recorded, not fetched — no WebFetch)   (or "—")

## Systems (roster skeleton — P0)
| slug | candidate category | candidate tier | depends_on | confidence | source |
|------|--------------------|----------------|------------|------------|--------|
| …    | … (low conf.)      | … (low conf.)  | …          | high/…     | File.cs:42 |

## Content Types (P1)
### CT-<slug>  — scale: bulk|curated  ·  belongs_to: <SYS or "?">  ·  confidence · source
`CT.fields`: <field:type, …>   (typed per gd-content-axis; ref<> for links)

## Resources · Entities · Forms (facts — P1)
- RES-<slug> · ENT-<slug> · FORM-<slug>  — confidence · source

## Intent Gap  (MANDATORY — what the code cannot know; a human must confirm/fill this)
> Items the ## Provided Context already answers are pre-filled here, tagged
> "(author-supplied — confirm on import)"; everything the seed did not cover stays open.
- **Pillars / core fantasy / the "why"** — code is silent on intent.
- **Win/Lose intent, monetization stance, target aesthetics.**
- **Are these numbers balanced, or merely current?**
- **Flows (the dynamics axis)** — not reconstructable from code at all.
- (…anything a subagent flagged as "could not determine"…)

## Explorations  (research backlinks — appended by /unikit-gd-explore; NOT code-extracted)
<!-- provenance: author-supplied (exploration) -->
> An accumulating registry of `research:` pointers — the cold-start mirror of the
> `GD-IDS` `research:` pointer. `/unikit-gd-recon` leaves this empty (or omits it);
> `/unikit-gd-explore` (RECON-input mode) appends one line per research it works out of
> the Intent Gap. Recon never writes here.
- research: `researches/<slug>/` — <1-line topic>  (Target: <SYS-slug | Intent-Gap item>)
```

The `## Intent Gap` is the load-bearing section: it is what stops a confident-looking but
hollow skeleton from masquerading as a finished GDD. Never trim it to look more complete.
The `## Explorations` section is **explore's** to append (RECON-input mode) — recon emits
it empty or omits it; the backlinks are author-supplied research pointers, never
code-extracted facts.

## Ownership Boundaries

- **Owns:** the single `.unikit/gamedesign/RECON.md` document — nothing else. No `GD-IDS`,
  no `GAME.md`, no `SYSTEM.md` / `CONTENT-TYPE.md` / `FLOW.md`, no registry fact, no `[gen]`
  render. `Write` is in `allowed-tools` for `RECON.md` alone (a path scope is not
  expressible, so the guarantee is the body + the absence of any other write). One other
  writer is **sanctioned**: `unikit-gd-explore` (RECON-input mode) appends `research:`
  backlinks to the **`## Explorations`** section — recorded here and in that skill's
  Ownership. Recon writes the rest of `RECON.md`; it never writes `## Explorations`.
- **Reads:** project source, configs, and asset definitions (the sanctioned third exception
  to the one-way boundary) + any file or folder the user names in the seed + the gd-principles
  core, `gd-provenance`, and `code-recon.md`. The optional **seed** (a game description,
  notes, file/folder paths, links) is recorded verbatim in `## Provided Context` and used as a
  scan hint — never as a code fact.
- **Never:** call any skill (there is **no `Skill` tool** — the handoff to `/unikit-gd-spec`
  is a printed recommendation); run once a GDD exists (cold-start gate → `unikit-gd-explore`);
  emit a flow fact; invent intent (it goes in the Intent Gap); bend an extracted fact to match
  the seed; fetch a URL (no `WebFetch` — provided links are recorded, never opened); promote a
  fact off `extracted from code` (only a human, downstream, may).

## Quick Reference

```
/unikit-gd-recon                      → scan the whole project → .unikit/gamedesign/RECON.md → recommend /unikit-gd-spec import
/unikit-gd-recon combat               → focus the scan on the combat subsystem (still one whole RECON.md)
/unikit-gd-recon "it's a roguelike deck-builder; pillars: …"  → seed the scan + record the description in ## Provided Context, pre-fill the Intent Gap
/unikit-gd-recon docs/pitch.md Assets/Economy/  → record the file + folder as references in ## Provided Context, scan them first
/unikit-gd-recon  (GDD already exists) → STOP → recommend /unikit-gd-explore code lens (targeted slice, not cold-start)
```
