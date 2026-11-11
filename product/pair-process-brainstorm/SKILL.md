---
name: pair-process-brainstorm
description: "Runs discovery in three fixed phases — grill interview, domain integration, backlog tree triage — on a free theme or an existing `$root` issue, landing an integrated Draft epic/story tree while leaving the PRD untouched. Invoke to open a new feature area or to deepen an existing epic/story ('brainstorm the notifications area', 'explore what is missing under #205'); level (broad/punctual) and orientation (functional/technical) are deduced from the root's type and tags, or asked as the first interview question when no root is given (or its type label is unrecognized). Composes /pair-capability-grill, /pair-capability-map-subdomains, /pair-capability-map-contexts, /pair-process-plan-epics, /pair-process-plan-stories."
version: 0.3.0
author: Foomakers
---

# /pair-process-brainstorm — Structured Discovery (3 phases)

Turn a rough theme — or an existing epic/story — into an **integrated Draft tree** in the backlog, through three phases: **interview → domain → triage**. **Phase order is fixed**, and each phase's output feeds the next: the interview's raw requirements blob is what the domain phase places, and the placed result is what the triage phase slices into issues. The **PRD is never modified** — discovery lands in the backlog and in domain context files, not in the product vision.

Discovery is **parametrized**, not a fixed script: with `$root` the level, orientation and phase-3 writer are deduced from the root's type and tags (or asked, on the fallback row); without it, the level is the first question — [parametrization.md](./parametrization.md). **Per-phase idempotency** ([convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md), itemized list in [resume.md](./resume.md)): each phase checks its own output first, so a re-run resumes at the first unfinished phase instead of re-interviewing, re-placing or re-triaging.

Discovery is also the **only** new process skill (D24): every phase delegates to existing capabilities — brainstorm owns the phase order, the parametrization, and nothing else.

## Process Profile

<!-- process-step: id=brainstorm -->

Executable form of the **`brainstorm`** step. Gate and composer rule: [degradation.md](./degradation.md).

## Composed Skills

| Skill             | Type       | Required                                                                                                                                                          |
| ----------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `/pair-capability-grill`          | Capability | Yes † — phase 1 interview (raw requirements blob). If not installed, warn and run the interview inline: one question per turn, each with a recommendation.           |
| `/pair-capability-map-subdomains` | Capability | Optional — phase 2 placement for a **broad** discovery: functional, and alongside `/pair-capability-map-contexts` when technical. Scoped. If not installed, warn and skip domain placement. |
| `/pair-capability-map-contexts`   | Capability | Optional — phase 2 placement for a **punctual or technical** discovery, scoped. If not installed, warn and skip context mapping.                                    |
| `/pair-process-plan-epics`     | Process    | Conditional — phase 3 writer when the root is an **initiative** (epics under it), an **untyped** root whose parent is an **initiative** (sibling epics under that initiative), or absent and the level is broad. If not installed, present the confirmed tree for manual entry. |
| `/pair-process-plan-stories`   | Process    | Conditional — phase 3 writer when the root is an **epic** (stories under it), a **story** or an **untyped** root **with an epic parent** (sibling stories under that parent epic), or absent and the level is punctual. If not installed, present the confirmed tree for manual entry. |
| `/pair-capability-record-decision`| Capability | Optional — phase 2, when a flagged domain conflict needs a DDR (`$type: domain`). If not installed, warn and record the conflict in the tree's rationale instead.   |

† **Required _when installed_.** `/pair-capability-grill` carries Required = Yes because phase 1 composes it **by default** — but it **degrades gracefully**: brainstorm warns and runs the interview inline (Phase 1 item 5, and under Graceful Degradation) when grill is absent, never HALTing on it. "Required" here means _composed by default_, not _a hard prerequisite_, so the flag never contradicts the degrade-inline step.

## Arguments

| Argument        | Required | Description                                                                                                                                       |
| --------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$root`         | No       | Existing issue the discovery hangs from (e.g. `#205`). Its type and tags deduce level + orientation, and phase 3 integrates the tree under it (a story root: under its parent epic). A root whose type label is absent or unrecognized resolves on the matrix's **fallback row**. Omitted → free-theme discovery, level asked first. |
| `$theme`        | No       | Free theme text to explore. **Precedence with `$root`**: given together, `$theme` **narrows the topic inside `$root`** — it becomes the interview's `$topic` (winning over the root's subject), while the root still deduces level, orientation, and the phase-3 writer; it never re-parents the tree. Given alone, it is the whole topic. If both are omitted, phase 1's opening questions ask for the level and then the theme (items 3 and 4). |
| `$level`        | No       | `broad` (feature/initiative) or `punctual` (single story) — overrides the deduced level.                                                           |
| `$orientation`  | No       | `functional` or `technical` — overrides the deduced orientation.                                                                                   |

## Parametrization (level · orientation · writer)

Deduction inputs, in precedence order: **argument > tags > issue type**. Every invocation matches **exactly one base row**, so the triple is never left unresolved, and it is always **stated up-front** as a proposal the developer can override.

> **The matrix is normative and lives in [parametrization.md](./parametrization.md)** — one row per `$root` signal, with the phase-2 capability, the phase-3 writer and the parent it receives, plus the rationale for the fallback row and for keying the writer on type rather than level. **Step 0 item 4 reads it on every run**; never resolve the triple from memory.

## Algorithm

### Step 0: Resolve Root, Level, and Orientation

1. **Check**: Is `$root` provided?
2. **Skip**: If absent, level stays unresolved — phase 1 asks it as its FIRST question — and orientation resolves from that answer (or from `$orientation`). On this path the **writer** resolves once the level is answered and the **parent** only once phase 2's placement is confirmed (Phase 3 item 6), so neither is resolved here: this step never invents one. Proceed to Phase 1.
3. **Act**: Load `$root` from the PM tool — resolution: see [way-of-working / PM-tool resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/way-of-working-pm-resolution.md). Unresolvable id → **HALT** (`$root <id> not found`); never guess a root.
4. **Act**: Apply the [Orientation Matrix](./parametrization.md) to the loaded issue's type and tags — no recognized type label resolves on the matrix's **fallback row** (level asked in phase 1, writer `/pair-process-plan-stories` under the root's parent epic, or `/pair-process-plan-epics` when that parent is an initiative), never on no row at all — then state the deduction up-front as a proposal:

   > Root `#[ID]: [Title]` (type: [type | **none recognized — fallback row**], tags: [tags]) → level: **[broad | punctual | asked as phase 1's first question]** · orientation: **[functional | technical]**.
   > Phase 2 will run [`/pair-capability-map-subdomains` | `/pair-capability-map-contexts` | both | resolved once the level is answered]; phase 3 will write with [`/pair-process-plan-epics` | `/pair-process-plan-stories`] under `#[parent ID]` ([the root | the root's parent epic | the root's parent initiative | the initiative the placement points to]).
   > [Fallback row with an **initiative** parent only: the level answer **sizes the interview only** — the tree is epics because the parent is an initiative, and the writer is not overridable. If `#[ID]` is really a story, label it and re-run.]
   > Proceed, override level/orientation, or label `#[ID]` and re-run?

5. **Verify**: Either `$root` is loaded with level, orientation **and** the phase-3 writer + parent resolved (deduced or overridden), or the level is queued as phase 1's first question — no `$root`, or the fallback row — with its row identified all the same. On the **no-`$root`** path the row resolves the rest later by construction (writer once the level is answered, parent once phase 2's placement is confirmed), so this beat requires only that the row is identified, never that a parent is invented. No input leaves the triple unresolved.

### Phase 1: Interview — Raw Requirements Blob

1. **Check**: Does a blob for this theme/root already exist in this session, or a prior handoff **for this same root/theme** at `.pair/working/brainstorm-<root-id | theme-slug>.md` (item 6 names it)? The root/theme qualifier binds **both** clauses: a handoff keyed to another discovery is not a match and is left alone.
2. **Skip**: A `partial` handoff is loaded and the interview resumes from its first open item — answered items are never re-asked. A `complete` blob is **not** carried in silently: it is offered — _"resume the finished interview from [date], or start a fresh one?"_ — because a completed discovery whose tree was already written, or whose tree the developer rejected, must not skip a legitimate new interview on the same root. A handoff marked `consumed` (item 9 retires it) counts as **absent**.
3. **Act**: When no `$root` was given — **or** the root matched the matrix's fallback row (no recognized type) — the **FIRST question** asks the level, before any content question:

   > Is this a **broad** exploration (a feature/initiative, several capabilities) or a **punctual** one (a single story)?
   > **Recommendation**: [broad | punctual] — [why, from the theme's wording, the root's body when there is one, and the current backlog].

   Record the answer as the level, then resolve orientation from the [Orientation Matrix](./parametrization.md).
4. **Act**: When **neither `$root` nor `$theme`** was given, the **second question** asks the theme, still before any content question — `/pair-capability-grill`'s `$topic` has no value without it, so this question is not optional:

   > What should this discovery explore? Name the area, the problem, or the idea.
   > **Recommendation**: [candidate theme] — [why, from the backlog's thinnest area or the last discovery's open items].

   Record the answer as `$theme`.
5. **Act**: Compose `/pair-capability-grill` with `$mode` omitted (interview), `$topic`: **`$theme` when it was given** (it wins over the root's subject and narrows the discovery inside `$root` — Arguments table), otherwise the root issue's subject — and `$context`: the loaded `$root` plus the resolved level/orientation, so grill explores before asking instead of re-fetching. Grill returns the **raw requirements blob** (R3.7) — findings per sub-question, open items, flagged assumptions.
6. **Act**: Persist a handoff **whenever the run ends before phase 3 completes** — `partial` when the interview stopped before explicit shared understanding, `complete` when it finished but the run stops or HALTs later. Write it to `.pair/working/brainstorm-<root-id | theme-slug>.md`: **one file per discovery**, so it can never be carried into an unrelated root. Take grill's offer when there is one; **brainstorm is the writer whenever grill made none** — inline interview, an interview that ended with grill's explicit yes, or a stop at a later HALT. The file records the blob's state (`partial` | `complete` | `consumed`) and the **resolved parametrization**: level, orientation, `$theme`/root subject, and writer + parent **when already resolved** (on the no-PM-tool path the parent is not, by construction — item 4 records blob, parametrization and placement). Rationale for the trigger and for the shared HALT obligation: [resume.md](./resume.md).
7. **Verify**: A raw requirements blob is available for Phase 2, with level, orientation, and a non-empty `$topic` (theme or root subject) resolved — and, if the run ends before phase 3 completes, that blob (`partial` or `complete`) is on disk at this discovery's own handoff path with whatever parametrization was resolvable.

### Phase 2: Domain Integration

Places the blob in the domain and reconciles it with what the project has already registered. Runs the Load / Check / Flag / Update-inline sequence of the [Context Map Maintenance](../../../.pair/knowledge/guidelines/architecture/design-patterns/context-map-maintenance.md) guideline.

1. **Check**: Has this blob's placement already run — do the subdomain/context rows and the glossary/entity/rule entries the blob implies already sit in `context-map.md` (or the owning `subdomain/<slug>.context.md`), attributed to this discovery?
2. **Skip**: If the placement is already recorded, confirm it and carry it into Phase 3 — do not re-compose the `/map-*` capability and do not re-walk the map. Partial placement resumes at the first unrecorded area only.
3. **Act — Load**: Read `context-map.md` (in `.pair/adoption/product/`) if it exists, plus the `subdomain/<slug>.context.md` sibling of every subdomain the blob touches whose index row shows an own context file.
4. **Act**: Compose the placement capability the [Orientation Matrix](./parametrization.md) selects, always **scoped to the areas the blob touches, never `$scope: all`** (that is `/pair-process-bootstrap`-only):
   - Broad/functional → Compose `/pair-capability-map-subdomains` with `$scope: [the capability areas the blob touches]` — core/supporting/generic + Volatility for each.
   - Punctual/technical → Compose `/pair-capability-map-contexts` with `$scope: [the contexts/services the blob touches]` — boundaries plus the per-relationship strength/distance/volatility verdict.
   - Broad + technical → both, in that order, on the same scope: placement first, then the integrations it implies.
5. **Act — Check + Flag**: Compare every feature, term, and rule in the blob against the loaded Glossary, Entities, and Common Rules and Invariants. On **conflict** with a registered rule (or a redefined term), stop and surface it explicitly — citing the conflicting rule and the DDR that formalizes it, when one exists — and resolve it with the developer before proceeding. A conflict resolved by changing the registered rule is recorded by composing `/pair-capability-record-decision` with `$type: domain`; never override a registered rule silently.
6. **Act — Update inline**: Write approved new or sharpened terms, entities, and rules back into `context-map.md` (or the owning subdomain's context file) using the guideline's Inline-Maintenance Method — a normal step of this phase, not a separate invocation. Cite the deciding source for each entry.
7. **Act**: If `context-map.md` does not exist, skip items 1, 3, 5 and 6 with a note and keep the placement from item 4 — its absence is the expected steady state, not an error.
8. **Verify**: The blob's areas are placed (or the placement is confirmed as already recorded, or the skip is noted), every conflict is either resolved or recorded, and the map reflects the approved terms. Phase 3 receives the placed blob plus the flagged/unresolved items.

### Phase 3: Tree Triage — Draft Items

**Adoption Context Read** — performed **at item 5**, after the Skip (item 2) and HALT (item 4) checks, before anything is assembled (a re-run that skips or halts never pays for it): read the recorded decisions and the domain map per [adoption-informed-generation.md](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/adoption-informed-generation.md): **read-only**, never a write. **This skill's subject**: the placed blob, scoped to what phase 2 placed and reusing the map it **already loaded**. No adoption history ⇒ a noted skip, no citations.

1. **Check**: Was a tree already proposed for this discovery — a confirmed proposal list in this session (evaluated **here**, it needs no backlog read), or items under the resolved parent whose idempotency keys already match the tree's candidates (that half needs the tree of item 5 and the parent of item 6, so it is evaluated **once item 6 has resolved the parent**, before the writer is composed in item 7)?
2. **Skip**: If so, re-present that outcome instead of re-triaging; a re-run is a no-op because the composed writer re-checks each key and proposes `ALREADY EXISTS #ID` (skip) for it.
3. **Check**: Is a PM tool configured and reachable ([way-of-working / PM-tool resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/way-of-working-pm-resolution.md))?
4. **Act**: No PM tool → **HALT** here with the setup pointer (`/pair-capability-setup-pm`); phases 1–2 keep their output (blob handoff + updated domain files), so re-running after setup starts at this phase. **Before halting, write phase 1's handoff if it is not already on disk** — the completed blob, its resolved parametrization (no parent on this path — see Phase 1 item 6), and phase 2's placement. Phase 1 item 6 is the writer; every HALT past phase 1 shares this obligation ([resume.md](./resume.md)).
5. **Act**: Assemble the **candidate tree** from the placed blob — each candidate a **vertical slice** carrying user value, **one level deep**, sitting one level under the parent Step 0 announced (epics under an initiative parent, stories under an epic one), each with its one-line rationale, the domain placement it came from, and what the adoption read applies (reshaped or dropped with the record named, a **citation**, or a `Revisits <id>: <why>` label). **The item type follows the resolved parent, not the answered level** — the level sizes the interview, never what the tree contains ([Level sizes, parent types](./parametrization.md#level-sizes-parent-types)). The tree never carries two levels: an initiative-root discovery produces epics **only**, no story slices beneath them (see item 7).
6. **Act**: Resolve the parent — **compound insertion** (R3.1) — from the [Orientation Matrix](./parametrization.md)'s writer column, which keys on the **root's type**, not on the level:
   The row gives parent, writer and tree level for every signal — **container roots** (`initiative`, `epic`) parent the tree on themselves; **leaf roots** (`story`, and the untyped fallback) parent it on the root's parent epic and enter the writer's registry as an **EXTEND target**, never as a candidate; **no `$root`** parents it on the initiative (broad) or epic (punctual) the placement points to, confirmed with the developer. Read the row rather than re-deriving it here.

   **Discovery never invents a parent**: when the row's parent does not exist, HALT with its remedy named — see [HALT Conditions](#halt-conditions), _No parent to hang the tree from_, which carries all of them (including the untyped root's labelling remedy, and the one case that looks like this HALT and is not).
7. **Act**: Triage the candidate tree against the **existing** backlog under that parent scope, per the shared [to-issues-triage.md](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/to-issues-triage.md) convention — extend-vs-create is decided against the existing tree, so discovery merges into the backlog instead of duplicating it. Compose **exactly one** writer — the one resolved in item 6 — passing **both** the parent and the tree:
   - `/pair-process-plan-epics` with `$initiative: [the resolved initiative]`, `$candidates: [the candidate tree]` and `$domain-placed: [the areas phase 2 placed or confirmed **in the subdomain catalog**]` — **omitted entirely** when phase 2 composed `/pair-capability-map-contexts` only, since nothing reached that catalog and Step 3.5 must then run `/pair-capability-map-subdomains` as normal.
   - `/pair-process-plan-stories` with `$epic: [the resolved epic]`, `$candidates: [the candidate tree]` and `$adoption-read: [this phase's read plus the effect applied to each candidate]` — inherited, not re-read.

   **One writer per run, one level written**: an initiative-root (or free-theme broad) discovery stops at the confirmed epics — it does **not** cascade into `/pair-process-plan-stories`, because the tree of item 5 carries no story slices to hand over and inventing them here is exactly how phase 3 would flood the backlog. Slicing a new epic is the next, separately confirmed step: `/pair-process-plan-stories` with `$epic: [the new epic]`, or `/pair-process-brainstorm` with `$root: [the new epic]` for another interview-driven pass.

   `$candidates` stops the tree from being discarded: given it, both writers triage the **supplied** candidates instead of re-deriving their own (their Step 3 Check). `$domain-placed` carries phase 2's placement **in-band**, so the writer's domain step is a confirm-only pass and the developer approves **one** subdomain-catalog delta per run — scope and omission rule in [parametrization.md](./parametrization.md). Each writer still runs its own registry query and presents the **dry-run** list — `ALREADY EXISTS #ID` | `EXTEND #ID` | `CREATE`, one per candidate with its rationale, its citation and any `Revisits <id>` flag — for confirmation **before any write**. Brainstorm writes no issue itself.
8. **Act**: Items land as **Draft**: discovery produces planning units, and `/pair-process-refine-story` is the single Draft→Ready path (**D24**); `/pair-next` picks the tree up from there. Report a discovery that changes the product vision as a recommendation to run `/pair-process-specify-prd` — the PRD is never modified here.
9. **Verify**: Every candidate carries exactly one confirmed proposal; created/extended items are Draft, linked under the resolved parent (and to `$root` when given); `.pair/adoption/product/PRD.md` is unchanged. **Then retire this discovery's handoff** — remove it, or mark it `consumed` — so a finished discovery never lingers to skip a later interview on the same root (the rule `/pair-capability-checkpoint` already applies to finished stories). This is the handoff's terminal state: without it a `complete` blob would be consumed forever by Phase 1 item 1.

## Output Format

```text
BRAINSTORM COMPLETE:
├── Scope:       [free theme: "<theme>" | root #ID: Title]
├── Level:       [broad | punctual] ([deduced from type/tags | asked — no root | asked — root has no recognized type | argument override])
├── Orientation: [functional | technical] ([deduced | override])
├── Phase 1:     [blob: N findings, M open items, K assumptions]
├── Phase 2:     [placement: subdomains/contexts touched | skipped — no map, no artifacts] · [conflicts: N flagged, N resolved]
├── Writer:      [/plan-epics | /plan-stories] — one writer, one level — under [#parent ID: Title] ([root | root's parent epic | root's parent initiative | placement])
├── Phase 3:     [Created: X · Extended: Y · Skipped: Z — all Draft] · [N cited · M revisits]
├── PRD:         untouched
└── Next:        [/refine-story on the first Draft story | /plan-stories on the first Draft epic (initiative-root discovery stops at epics)]
```

The `Next:` line names only steps enabled by the project's [process profile](../../../.pair/knowledge/guidelines/technical-standards/ai-development/process-profiles.md): a disabled one is dropped, and when none is left the line names no skill.

## HALT Conditions

- **`$root` not found** (Step 0) — the id does not resolve to an issue; report it and stop, never guess a root.
- **No PM tool configured** (Phase 3) — phases 1–2 complete and keep their output: the completed blob plus its parametrization is written as a `.pair/working/` handoff **before** halting (Phase 3 item 4), so the re-run after `/pair-capability-setup-pm` starts at phase 3 instead of re-interviewing; HALT with the `/pair-capability-setup-pm` pointer.
- **No parent to hang the tree from** (Phase 3, **any** root or none) — no initiative exists for a broad free-theme tree, no epic for a punctual one, **or** the `$root` story / untyped root has no parent at all to hang siblings from (an orphan is a normal PM-tool state — sub-issue links are optional); HALT with the `/pair-process-plan-initiatives` / `/pair-process-plan-epics` pointer — and, for an **untyped** root, with the labelling remedy alongside it (label `#[ID]` with its real type and re-run) — rather than writing beneath an unrelated parent. An untyped root whose parent is an **initiative** never reaches this HALT: it resolves to `/pair-process-plan-epics` under that initiative (Phase 3 item 6).
- **Unresolved domain conflict** (Phase 2) — a flagged conflict with a registered rule or DDR that the developer has not resolved; discovery never overrides a registered rule.
- **Developer rejects the tree** (Phase 3) — resolve the triage proposal before any write.

## Idempotent Re-invocation

See [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md) — brainstorm is one of the four orchestrators that resume **per-phase**. Re-invoking it on a partially completed discovery is safe and expected: each phase checks its own output before acting, so the run resumes at the first unfinished phase and never re-does a completed one.

> **The itemized per-phase resume list is in [resume.md](./resume.md)** — what each phase detects, what it confirms, and the one path that re-asks (the level, when it was asked rather than deduced and no `.pair/working/` handoff survives). Read it whenever a re-invocation lands mid-discovery.

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) for the standard scenarios (optional skill not installed → skip that step and note it; PM tool unreachable → ask the developer directly). **No missing composition fails a discovery** — grill, `/map-*`, `/pair-capability-record-decision`, the plan-\* writers, a missing `context-map.md` and absent/unreadable adoption history (adoption-informed triage) each degrade to a noted skip or an inline substitute; the only hard stops are the HALT Conditions above.

> **The per-composition fallback for each one is in [degradation.md](./degradation.md)** — read it when a composition brainstorm expects is missing, not on a normal run.

## Notes

- **Composes, never re-derives**: the interview is `/pair-capability-grill`'s, the domain placement `/map-*`'s, the writes `/pair-process-plan-epics`/`/pair-process-plan-stories`' (which own the to-issues triage). Brainstorm owns the phase order and the level/orientation parametrization only (D24).
- **The PRD is never modified** — R3.4: discovery writes to the backlog and to domain context files; product-vision changes are surfaced as a `/pair-process-specify-prd` recommendation.
- **Modifies PM tool state** (phase 3, via the composed plan-* skills) **and adoption files** (phase 2, context map + domain catalogs).
