---
name: data-to-kinds
description: "The staged pipeline that turns any API, provider payload, scrape, or computed result into registered, rendered platform kinds. Use on 'create kinds for X', 'distill X into kinds', 'point yourself at API X', or as a stage (A/B/V/D/C) of a running data-to-kinds run. NOT for consuming existing kinds (use aidream's workflow-io-kinds / matrx-frontend's shape-system)."
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/data-to-kinds/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# data-to-kinds — point an agent at a data source; get a fully-rendered platform kind family

**Entry point.** Someone names a source — an API, a provider, a graph action family, a system
aspect — and this skill carries it the whole way: distill shapes with Arman via tables → `@kind`
pydantic models → publish to the registry → generate TS types → canonical components by
converging the displays we already built → a live demo calling the real server → verification →
cutover of the nodes/tools that emit it. **No step needs an explanation from anyone.** If you hit
one that does, that is a defect in THIS skill: fix it here in the same session (canonical copy
`common-docs/skills/data-to-kinds/SKILL.md`, then `python3 common-docs/meta/scripts/sync_skills.py`;
never edit a repo mirror — the sync erases it). Run-specific decisions go in the run's ledger,
not here. Arman's instructions that generalize beyond your family ("always X", "never Y") become
standing law here the day he says them.

## Route by stage — a run is ONE stage

Read, in order: this whole file (vocabulary, pipeline, standing laws, chip prompts, runs); your stage's file; ALL of open-gaps.md; **and every skill or document your stage file tells you to run or read — those pointers bind exactly like the stage steps** (Stage D: run the `safe-cutover` skill FIRST, before step 0; Stage A step 0: `operations/kind-conversion-board.md` § four consumer surfaces). This route names every companion file of this skill; it never forbids what a stage file requires:

- **Stage A only → read [stage-a.md](stage-a.md).**
- **Stage B only → read [stage-b.md](stage-b.md).**
- **Stage V only → read [stage-v.md](stage-v.md).**
- **Stage D only → read [stage-d.md](stage-d.md).**
- **Stage C** — inline below, in this file.
- **Every stage (C included), before its first step → read ALL of [open-gaps.md](open-gaps.md)** — its numbered items carry rules that correct the stage steps, and most never name the stage they bind, so reading only the items that name your stage misses them. Append new friction there.

## Why (Arman, 2026-08-20/21, condensed)

Content IR is the one language every part of the system speaks. When our own code derives data,
emitting a kind is the easiest thing in the world — the function spits out the object in exactly
the shape we want — and then every surface (web, mobile, desktop, extension), every workflow node,
and every agent can count on that shape: no type errors, universal rendering, no custom code. The
search pilot was *"the most incredible proof we could ever have"*: two providers with different
raw shapes became ONE kind family with nested kinds and primitives, rendered by ONE set of
components from a real server call. The bar now: *"skills that teach agents how to do this end
to end — point them at an API or some aspect of our system and ensure all of this gets done."*

## Vocabulary you must hold

- **Data kinds** (`category: data`) — pure portable shapes, no runtime/provider mess. **Runtime
  wrapper kinds** (`category: runtime`: `node_outcome`, `run_result`, `agent_result`,
  `tool_result`) carry instance context with the data kind NESTED as a typed payload. A wrapper
  never absorbs payload fields; a payload never carries runtime fields. You build DATA kinds.
- **Family** — one source's kind set: a collection kind + item kinds + the system-wide
  primitives they hold (search: `web_search_results` → `web_result`, `news_result`, … →
  `rating`, `postal_address`, …). **Sectioned, never flattened**: heterogeneous sections stay
  typed arrays of typed item kinds; a collection is never a bag of loose keys.
- **Maturity** (`kind_definition.metadata.maturity`, machine-readable, never a vibe):
  `placeholder` (outer structure honest, data NOT studied — the fast-fire tier and the `@kind`
  default) → `distilled` (real data studied, shape designed — what Stage A produces) →
  `verified` (distilled AND proven end-to-end: registered → typed → rendered → exercised —
  awarded ONLY by the verification pass; `@kind` refuses to declare it). Registering a basic
  FE route promotes nothing. Over-engineering guard: a boring flat result whose placeholder
  shape already tells the truth is promoted `simple-is-correct` as-is — richness in the DATA
  (arrays of structures, recurring sub-objects, heterogeneous sections) earns the full treatment.

> 🚨 **UNRESOLVED CONFLICT — `CFL-054`. Do not build against this section until Arman rules.**
> **This document says:** a result's second view is the raw provider payload, returned only when a caller asks for it (`include_raw=`), off by default.
> **[`open-gaps.md`](/skills/data-to-kinds/open-gaps.md) (the item on the second projection) says:** the second view should be what the current live path produces from the same input, shown beside the kind on every demo, going quiet once the cutover lands.
> **Why it matters:** it decides what every demo's second tab shows and what Stage D's repointed emitters must serve — the untouched provider data for inspection, or the old output for comparison that disappears after cutover.
> **Your move:** bring Arman these two readings and the consequence, get his ruling, then build.
> Register: [`/operations/conflicts.md`](/operations/conflicts.md) · `CFL-054`

- **The three projections of one result**: (1) the KIND — canonical, what travels/persists/
  renders; (2) the RAW payload — on demand (`include_raw=`), off by default; (3) the AI VIEW —
  **DECLARED ON THE KIND** as `@kind(..., ai_view=(...))`, naming which of its own fields a model
  receives. Published to `kind_definition.metadata.ai_view` and applied at the ONE prompt door
  (`matrx_ai.config.prompt_values`), which recurses into collections. Omit it and the whole
  payload travels, as before. One core engine per source; the engine's result gets its kind at
  that boundary.
  **Why it is on the kind and not at the tool boundary** (Arman, 2026-08-24 — this SUPERSEDES the
  earlier "never in the kind" rule): a workflow step emits a kind and the author binds it to an
  agent variable, and no tool is involved at all. *"If you overdo it, then you're killing the
  model's context window."* A second kind per family doubles the vocabulary and makes every author
  learn a conversion; the kind naming its own fields costs one line and needs nobody to remember.
  **What to put in it:** the markdown/body plus the provenance a model cannot infer from the body.
  Arman: *"as long as you include those [links and media] in your markdown inline, that's the best
  way to include them… the agent sees what's a header tag, sees what's an image, sees what's a
  link just because it's built into the markdown. And then you don't have to add them as extras."*
  So a field already inline in the body is a DUPLICATE, not an addition. Measured on one real
  page: 235,442 chars → 288.

## The pipeline at a glance

| Stage | Repo | Produces | Gate (Arman) | Then |
|---|---|---|---|---|
| **A Distill** | aidream | shapes distilled → `@kind` models + adapters + tests → published (inactive) → demo endpoint → ledger | **none — do NOT stop for a table approval** (gap #14 of 2026-08-24) | fire B |
| **B Render** | matrx-frontend | `kind_component` rows → activation → `pnpm shape:types` → compiled mirrors → one canonical component per kind → live demo | **THE gate: approves the rendering on the demo** | fire V+D (or C if this is a pilot) |
| **V Verify** | either | four legs per kind; stamps `verified` | — (report) | — |
| **D Cutover** | aidream (+FE consumers) | emitters repointed to the family, collection schema superseded, legacy displays converged | approves cutover on the STAGED proof — no merge, registry publish, or deploy before it ([stage-d.md](stage-d.md) step 6) | — |
| **C Review** | common-docs (owns this skill) | skill rewrite + replication run | — | — |

Every run has ONE ledger: `common-docs/operations/<family>-kinds-run.md` (type `Register`; the
search pilot's is `operations/search-kinds-pilot.md` — copy its section layout: material · chain
table · decisions (append-only, Arman's) · per-stage build records · artifacts). The ledger row
is the durable completion signal the orchestrator watches; it is only true once pushed.

---

## Stage A — Distill (aidream)

**Stage A only → read [stage-a.md](stage-a.md).** Blast radius across five surfaces, real captures, shape tables, `@kind` models, translation adapters, publish, demo endpoint.

## Stage B — Render (matrx-frontend)

**Stage B only → read [stage-b.md](stage-b.md).** Component sweep, types, compiled mirrors, copy controls, canonical components, `kind_component` rows, activation, live demo.

## Stage V — Verify (the four legs; stamps `verified`)

**Stage V only → read [stage-v.md](stage-v.md).** The four legs per kind (registered · typed · rendered · exercised) and the `verified` stamp.

## Stage D — Cutover (convert what emits and consumes the family)

**Stage D only → read [stage-d.md](stage-d.md).** Field-read proof, emitter repoint, hidden consumers, history plan, legacy convergence, committed guard — on top of the `safe-cutover` skill.

## Stage C — Review and generalize (owns this skill)

Review the whole run — skill-said vs happened, every missing instruction, every ruling — rewrite
THIS skill (tight: instructions, not a memoir), fix the ledger, then **fire the replication run**
from the queue as a Stage A chip that references ONLY this skill (no outside explanation — the
skills and documents its stage files name still bind, per § Route by stage). The replication's friction is
the failure list: the replication agent appends it to [open-gaps.md](open-gaps.md) and its ledger links it.

---

## Standing rules (all stages)

- **Every keep/drop/merge/require decision is Arman's — but you arrive with the answer.**
  *"if I was gonna fucking do it myself, what do I need you guys for?"* (2026-08-23). A table of
  bare verdicts is a menu, and a menu is a defect. **Every row carries your recommendation and its
  one-line reason; he confirms or corrects.** Two mechanics that follow: *"it depends"* is a
  first-class answer — capture the CONDITION he then names verbatim, because it is usually the most
  valuable sentence of the session, and it becomes a rule on the kind. And **plumbing never enters
  his table** — a missing credential, a codegen failure, a 403 endpoint goes in a developer list at
  the bottom of your report. Routing agent-doable work to him is itself a defect.
- **Content IR alignment binds you** (`systems/architecture/content-ir/FEATURE.md`): one system;
  XML/markdown/fence arrival surfaces stay first-class; frozen block-type values never change;
  kinds-as-JSON is the internal form, never a forced wire format. Names per `NOMENCLATURE.md` +
  lexicon (short snake_case noun, no provider prefix, no hashes, no node names).
- **Provenance survives merging.** A shared kind keeps source identity as a `source` field (or
  source-specific companion kinds); merge shapes, never origins.
- **Specific kinds without going overboard.** A repeated reusable structure gets a kind; a one-off
  blob does not. Layer where identification helps (collection, item, primitive); never a wrapper
  whose only content is its payload — self-identifying items are already portable.
- **Reuse before minting; parallel path until approval**; live nodes/services/routes repointed
  only in Stage D after approval.
- **Completion signaling**: each stage ends by updating the ledger row + artifacts AND firing the
  next stage's chip with a standalone prompt. **Commit and push as you go** — a ledger row is only
  true once on origin/main.
- **Ask Arman with the page, the action, the question** — and never hand him the design problem.

## Distillation laws (Arman, 2026-08-20, ratified during the first run)

- **A drop is a loss of data we paid for.** Never inherit a drop from existing code — past code
  dropping a field may be the mistake this pipeline fixes. Every drop is justified on its own
  merits. Drop freely ONLY provider plumbing: request echoes, tracking/redirect links, pagination
  endpoints, the provider's own UI chrome. Real-world data defaults to KEPT, as structure.
- **Provider asymmetry is never a drop reason.** One provider carrying a field the other lacks →
  optional field on the shared kind; map both providers' variants onto the same field wherever the
  data is the same thing.
- **Known string formats become structured data.** Parse hours, dates, ratings, addresses into
  typed structure. Keep the original string alongside only when the parse is lossy or relative
  ("2 weeks ago"); never synthesize precision the source didn't give. Datetimes/URLs stay scalar
  JSON-Schema formats, not kinds.
- **Recurring small structures are core-primitive candidates** (rating, opening hours, postal
  address, geo coordinates): propose system-wide primitive kinds held by bigger kinds; check the
  registry first; never mint a primitive that exists.
- **Embedded HTML is judged by what's inside.** Pre-rendered UI with no unique data → discard.
  Unique data wearing HTML → convert to structure (text + extracted links); never store raw HTML.
- **One copy of everything.** Kinds reference canonical entities rather than duplicating them.

## Arman's rulings from the Kind Directives session (2026-08-23/25 — standing law)

- **THE STRICTNESS LAW — no escape hatches, ever.** *"everywhere we leave a little bit of
  breathing room for exceptions of a very specific type, coding agents abuse it and suddenly make
  it their default route… if something comes down to making things strict or not, you need to make
  them strict."* You may not ship a same-line opt-out comment, a new baseline entry (baselines
  shrink only), a grandfather set, a dual registration, or a "try the new shape, fall back to the
  old" branch. **A fallback branch is a defect the moment it is written.** Strict for anything an
  author or an agent controls; loud-and-recorded ONLY where a genuine platform outage would
  otherwise punish a user — and that path must be unreachable by writing bad code. Full text:
  [`/policies/strictness-law.md`](/policies/strictness-law.md).
- **Enrichment is an optional field, not a variant.** When a kind will later be enriched by
  another system (a search result gaining the scraped page behind it), declare it now as an
  OPTIONAL nested kind on the existing shape — *"That's how schemas work."* Do not mint a second
  "enriched" kind and do not flatten the enrichment in.
- **Heavy nested content renders collapsed, with a window-panel escape.** The enriched/nested kind
  is a collapsible section, expandable IN PLACE, plus an icon that opens the full nested kind in a
  **window panel** — our movable, non-blocking, minimize/maximize panels, *not* a modal. State this
  in the component's brief so Stage B does not invent a third pattern.
- **A schema always yields a form — and that is only the default.** The generic auto-form built
  from a kind's schema is an acceptable input surface and should exist for everything (ideally from
  a reusable package installable in any JS environment). **The moment a kind is used as a DECLARED
  input anywhere we recognize — a workflow node, a manifest, a mandate — the rule flips and a
  custom input component becomes REQUIRED.** Auto-form is the floor, never the finish.
- **The kind NAME is a routing language.** Reserved prefixes resolve to a generic component when no
  custom one exists, so an enrolled family gets a view for free and a custom component overrides it.
  Resolution order is exact (kind, platform, role) → db override → compiled → **prefix rule** →
  generic floor. Never hand-register N near-identical components where one prefix rule serves them.
- **A final live check is required before anything is called done.** Ruled 2026-08-23 (*"Yes! I
  agree with you that a final live check is required to consider it done"*) — Stage V is not a
  someday sweep, it is the last step of every run. Nothing reaches G5 without it.
- **Naming is the agent's call, judged by what a coding agent understands naturally** — bring the
  proposal, not the question, and prefer short and specific over ceremonious.

## THE MERGE + TRANSLATION LAW (Arman, 2026-08-20 — platform-level, unbreakable)

- **Provider-named kinds are BANNED.** `brave_search_results` next to `google_search_results` is
  the death of the kind system — 100 kinds is the same as no kinds. Same kind/type/purpose → ONE
  merged kind; the provider is a `source` field. Adding a provider = one adapter, never a kind.
- **Every provider gets a TRANSLATION ADAPTER, modeled on the AI request system's configuration
  equivalence**: value vocabularies map ("US" ↔ "United States"); equivalent concepts land in one
  field however each provider spells them; a field one provider lacks is DERIVED when an honest
  derivation exists (rank from array order, `published_at` parsed, an approximation when the
  source is relative). The fewer optional fields, the more every downstream can count on.
- **Never lossy by accident.** An adapter declares every raw key in exactly one set: MAPPED (raw
  path → field) or DROPPED (named key + reason, Arman-approved, visible in code). Anything else is
  UNKNOWN and screams (log + ops record) — that is how a provider adding a field gets noticed.

## Earned traps (still true — each cost a run-day)

- `KindModel` needs BOTH `populate_by_name` (in) and `serialize_by_alias` (out): a kind nested in
  a plain model otherwise serializes as `kind_` and its own `additionalProperties:false` schema
  rejects it (pinned by `packages/matrx-graph/tests/test_content_ir_model.py`).
- `_touch_row` bumps `kind_definition.version` on every update — re-read before pinning
  `kind_example.kind_version`. `kind_example.source` is CHECK-constrained to
  `authored|captured|migrated|synthetic`; real-payload examples are `captured`.
- Changing an ACTIVE kind's schema changes live node verification on the next run — hence the
  cutover gate (Stage D.1). Use `--evolve` for additive drift; never a publisher overwrite.
- pydantic leaves defaulted fields (incl. `__kind`) out of `required`, so they generate as
  optional in TS — the type tells the truth about validation, the serializer always emits them.
- Brave returns empty-string location fields; Google News dates are relative; a token-only
  `ai_overview` means "no answer" — read the family FEATURE.md's earned traps before touching it.

## Open gaps (SDK wishlist + replication friction logs)

**Every stage, before its first step, reads ALL of [open-gaps.md](open-gaps.md)** (SDK wishlist items 1–5 + every replication run's friction log, numbered items with the rule each earned) — the same rule as § Route by stage. Hit friction (replication agents included) → append it there; the SDK build consumes it.

## Chip prompts (standalone — paste as the chip body, fill the ⟨⟩)

**Stage A:** "You are STAGE A of the data-to-kinds run for ⟨family⟩. Read these three files in
`common-docs/skills/data-to-kinds/` (mirrored at `.claude/skills/data-to-kinds/`): `SKILL.md`, `stage-a.md`,
and ALL of `open-gaps.md` — plus every skill or document `stage-a.md` tells you to read — and follow them verbatim. Source: ⟨engine/client path, nodes, provider(s)⟩. Existing placeholders:
⟨`aidream/kinds/<domain>.py` slugs or none⟩. Create the ledger `common-docs/operations/⟨family⟩-
kinds-run.md` from the search pilot's layout. Bring Arman your tables, each row with your recommendation, but do NOT
stop for a table approval (gap #14 of 2026-08-24: the one approval gate is Stage B's rendered demo); publish inactive; ship
the demo endpoint; mark Stage A DONE and fire Stage B. Every instruction the skill
failed to give you goes into its `open-gaps.md` in the same session."

**Stage B:** "You are STAGE B of the data-to-kinds run for ⟨family⟩. Read these three files in
`common-docs/skills/data-to-kinds/` (mirrored at `.claude/skills/data-to-kinds/`): `SKILL.md`, `stage-b.md`, and ALL of
`open-gaps.md` — plus every skill or document `stage-b.md` tells you to read — plus the ledger `common-docs/operations/⟨family⟩-kinds-run.md`. Kinds: ⟨slugs⟩. Endpoint:
⟨POST /api/…⟩. Build per Stage B, demo at `/demos/⟨family⟩`, verify in-browser, get Arman's
render approval, mark DONE, fire V + D."

**Stage V / D / C:** same shape — name the family, the ledger, the slugs, the stage, and the files to read: `SKILL.md`,
that stage's file (`stage-v.md` / `stage-d.md`; Stage C is inline in `SKILL.md`), ALL of `open-gaps.md`, and every skill
or document that stage's file tells you to run or read — never "only" (Stage D: the `safe-cutover` skill first).

## Runs

| Run | Ledger | State |
|---|---|---|
| Search results (Brave + SerpAPI Google) — the pilot | `common-docs/operations/search-kinds-pilot.md` | A+B approved; C done 2026-08-23; V + D pending (cutover gated) |
| Scraper / crawl results (`scraper.*`) — replication run 1 | `common-docs/operations/scraper-kinds-run.md` | Stage A fired 2026-08-23 |
| SEO rank tracking + SERP landscape — queue row 2 | `common-docs/operations/rank-kinds-run.md` | A+B approved; **V done 2026-08-26** (`serp_placement` + `provider_run_receipt` verified); D.0 field-read proof clean; D remainder open |
| RAG retrieval + citations — queue row 3 | `common-docs/operations/rag-kinds-run.md` | A+B approved; **V done 2026-08-26** (`source_ref` + `retrieved_chunk` + `rag_synthesize_result` verified); D.0 4/4 SAFE; D remainder open |
| Tabular results (`data_table`) — queue row 4 / replication run 4 | `common-docs/operations/table-kinds-run.md` | A+B approved; **V done 2026-08-26** (`data_table` verified); D.0 clean (1 passthrough human-judged); D remainder open |

**Campaign doctrine (platform law, applies beyond kinds):** `common-docs/policies/conversion-campaigns.md` — the four consumer surfaces, demo-is-not-a-conversion, a campaign ends in a committed guard, consumer lists are computed not hand-written.

**Tracking spine:** `common-docs/operations/kind-conversion-board.md` — every family in flight, its gate (G1 enlisted → G2 blast radius → G3 shaped → G4 cut over → G5 guarded), and who holds it. A family is DONE only at G5; a demo is not a conversion. Update your row every gate.

**What to run next:** `common-docs/operations/data-to-kinds-queue.md` — the ranked inventory of every remaining candidate, each with a filled-in chip prompt. Fire one at a time; queue rows 1 and 4 mint primitives that later rows nest.
