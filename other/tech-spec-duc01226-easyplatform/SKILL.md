---
name: tech-spec
version: 1.0.0
description: '[Documentation] Use when (re)generating the DERIVED technical spec view over code + tests, or reporting canonical §8 TC/test-code drift. A GENERATOR — it projects code + tests into a regenerable per-component view and NEVER authors business content. Modes generate|audit|sync. Per-mode procedure lives in references/{author,sync}.md.'
triggers: 'tech spec, technical spec, regenerate tech specs, technical spec view, derived technical spec, component technical spec, use case inventory, TC to test map, test coverage map, sync test specs, sync tests, reconcile tests, reverse sync, full sync, harvest invariants, cross-service topology, event consumer inventory'
---

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

> **Portability:** the technical root is read from `docs/project-config.json` → `specRoots.technical.path` (declared `authorship: "derived"`, `m1Policy: "exempt"`). NEVER hardcode a root. `{TechRoot}/{Service}/{Component}.md` is a **pattern** — `{Service}` and `{Component}` are placeholders resolved from the repo, never literal names.

**[IMPORTANT] TaskCreate** — Break ALL work into small tasks BEFORE starting (one task per emitted artifact).

**Goal:** Generate, on demand, a regenerable single-writer **technical view** — per-component derived specs (use-case inventory, TC↔test map, cross-service topology) — **projected FROM** code and test annotations (`TestSpec` for business TC joins, `TechnicalSpec` for technical-only joins when present), so an engineer can read a component's technical surface without ever forking a second, hand-maintained source of truth. **Code and tests are the source of truth; this skill only projects them.**

**Summary:**

- **Purpose:** a DERIVED-view **generator** ONLY — greps handlers/consumers/jobs/producers and test annotations to emit `{TechRoot}/{Service}/{Component}.md`; it **NEVER authors business content**. Code + tests stay the source of truth.
- **Main steps (run in order):** **Step 0** Scope Gate — `AskUserQuestion` (service/component + mode), BLOCKING before any read; no source to derive from → STOP. **Step 1** Derive facts — grep the use-case inventory, the `TestSpec`/`TechnicalSpec` joins, the topology. **Step 2** Instantiate templates — `references/author.md`'s fixed sections in pinned order. **Step 3** Stamp & Write — DERIVED banner + regenerate date, write each artifact immediately (never accumulate in context). **Step 4** Verify — no retired artifacts, banner present, no business artifact types, no canonical claims, no secrets.
- **Modes:** `generate` (default — regenerate the derived view) · `audit` (report which views are stale vs code/tests) · `sync` (report canonical §8 TC ↔ executing test-code drift — `references/sync.md`).
- Hard prohibition is the load-bearing rule: never emit the retired A-E engineering tree, `M##` dirs, `00-module-registry.md`, `01-domain-erd.md`, or `06-reimplementation-guide.md` under the technical root — why: an A-E bundle becomes a second source of truth competing with the Feature Spec, and a generator able to recreate it resurrects the retired tree on its next run (this has occurred once already, via rebase).
- Every generated file carries the `> DERIVED — regenerate with the tech-spec skill; do NOT hand-edit` banner + a regenerate date, anchors each fact back to its source, and makes **no canonical claim**.
- **This skill is M1-EXEMPT** (`specRoots.technical.m1Policy: "exempt"`) — its prose MAY name technology. That exemption is the whole reason this tree exists; it is NOT a licence to carry business content (see **Hard Prohibitions**).

> **[SCOPE]** This skill generates a **DERIVED** technical view over code + tests under `specRoots.technical.path`. It MUST NOT emit a per-module A-E engineering bundle (`A-domain-model`, `B-business-rules`, `C-api-contracts`, `D-events`, `E-user-journeys`), `M##` directories, `00-module-registry.md`, `01-domain-erd.md`, or `06-reimplementation-guide.md` — those are not part of the spec model. It MUST NOT author business content: the Feature Spec under `specRoots.business.path` owns §1–§8, and this skill neither writes nor amends it. Authority: [`docs/project-reference/spec-system-reference.md`](../../../docs/project-reference/spec-system-reference.md), [`.claude/skills/shared/sdd-artifact-contract.md`](../shared/sdd-artifact-contract.md).

**Inputs:** the code tree (command/query handlers, event consumers, background jobs, producers, sagas, outbox) and the test tree (`TestSpec` and `TechnicalSpec` annotations when present). **Code is the technical source of truth** — this skill reads it to **project** a view, never to populate a parallel _canonical_ layer.

**Modes:**

| Mode       | Trigger                                    | Input                                       | Output                                                                                      |
| ---------- | ------------------------------------------ | ------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `generate` | default — refresh the derived view         | code + test annotations                     | `{TechRoot}/{Service}/{Component}.md`, all DERIVED (`references/author.md`)                 |
| `audit`    | explicit request — staleness check         | code/test mtimes or git vs derived-view age | Stale-list report (which views lag their source). Never mutates                             |
| `sync`     | "sync tests" / "reconcile tests" / harvest | canonical §8 TCs + test code                | §8/test drift report + route-only `CoveredBy:`/orphan reconciliation (`references/sync.md`) |

**Tooling:**

- `npm run tech-spec:generate` — regenerate the derived technical views from code/test annotations.
  Equivalent direct invocation, for projects that copy `.claude/` without a `package.json`:
  `node .claude/skills/tech-spec/scripts/generate-tech-specs.mjs`

**Mode resolution (do this before any work):**

1. Parse the mode from the invocation: explicit `[mode=<x>]` arg wins; else infer ("regenerate tech specs", "technical spec for {Component}" → `generate`; "stale", "audit" → `audit`; "sync tests", "reconcile tests", "reverse sync", "harvest" → `sync`).
2. If ambiguous, present the detected mode via `AskUserQuestion` before proceeding — NEVER auto-start a mutating mode.
3. **Read the matching `references/` body** — it is the single source of truth for that mode's procedure, gates, and output contract. Do not run a mode from memory.

**Workflow:** `/scout` (locate the component) → `/tech-spec` (project the view) → `/changes-review` → `/watzup`

---

## The Generator Contract (NON-NEGOTIABLE)

This skill is a **generator**, not an author. Every clause below is structural — none is a preference a future maintainer may relax for convenience.

| #      | Clause                                                                                                                                                                                                                                  | Why                                                                                                                                                                                              |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **C1** | **[BLOCKING]** Output is **DERIVED and regenerable** — every generated file carries a `> DERIVED — regenerate with the tech-spec skill; do NOT hand-edit` banner + a regenerate date. It is **NEVER a second source of truth**.         | A derived view makes no truth claim, so it cannot compete for canonical status. A hand-editable tree makes one — and then "which is right, the doc or the code?" becomes askable.                |
| **C2** | **[BLOCKING]** **Never authors business content.** No user story, no acceptance criterion, no business rule, no §1–§7 prose, no §8 TC is written by this skill — in any mode. The Feature Spec stays the source of truth for all of it. | Carrying the Feature Spec's own artifact types is exactly how a rival tree competes on the Feature Spec's turf.                                                                                  |
| **C3** | **[BLOCKING]** **Never claims to be a source of truth.** The generated files never assert canonical authority. When the view disagrees with code, **code is right by construction and the view is stale — regenerate it.**              | A derived aid that asserts canonical authority corrupts the single-writer contract.                                                                                                              |
| **C4** | **[BLOCKING]** **Write each artifact immediately** after instantiating it; do NOT accumulate large outputs in context.                                                                                                                  | A `{Service}/{Component}` fan-out is exactly the case that exhausts context mid-run and loses every unwritten artifact.                                                                          |
| **C5** | **[BLOCKING]** **Single writer.** This skill is the **sole writer** under `specRoots.technical.path`. Nothing else writes there; it writes nowhere else.                                                                                | Two writers is how a view becomes a sibling.                                                                                                                                                     |
| **C6** | **[BLOCKING]** **Regeneration is idempotent** — regenerating over unchanged source produces an **empty diff**.                                                                                                                          | This is the tree's flagship oracle: it proves the artifact can be thrown away and rebuilt from its source. If it cannot, the tree holds content of its own — it claims truth, and it is a rival. |
| **C7** | **[BLOCKING]** **A-E filenames are never emitted.** See **Hard Prohibitions**.                                                                                                                                                          | An A-E bundle becomes a second source of truth competing with the Feature Spec.                                                                                                                  |

### C8 — Mechanical detect + route · never judge · never write business content

> **A generator MUST NEVER apply RIT — or any judgment test — at generation time.** Judgment produces data; generators consume data.
> Canonical formulation: [`.claude/skills/shared/sdd-artifact-contract.md`](../shared/sdd-artifact-contract.md) (beside RIT). **Cited, not restated.**

|                                                                            | Who                                          | When                                       | Output                                            |
| -------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------ | ------------------------------------------------- |
| **Judgment** (RIT, business-invariant verdicts, visibility classification) | a human, or an AI **outside** this generator | **once**, at authoring/classification time | a **persisted verdict — data**                    |
| **Generation**                                                             | `/tech-spec`                                 | every run                                  | output **mechanically re-derived** from that data |

**Idempotency holds because nothing is re-judged.** The generator reads a verdict it did not make and cannot revise. Same source + same verdicts ⇒ same output, every run. **A generator that judges is not idempotent — it fails C6 against its own tree, permanently, and the failure reports as `hand-edited`, which is the wrong cause and undiagnosable.**

**Two resolutions that are FORBIDDEN, because both look like fixes:**

| Rejected                                              | Why it fails                                                                                                                                                                                                 |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Scope idempotency to only the mechanical sections** | Reintroduces a **per-section carve-out** — an exemption at a new address. A carve-out is this framework's characteristic failure; do not re-mint one inside the oracle.                                      |
| **Cache judgments inside the generator**              | The generator then owns a **staleness problem**: a cached verdict that outlives the code it judged, invisible to review and to `git`. **Persisted verdicts belong in the artifact, not in generator state.** |

### C9 — The harvest detector REPORTS; it never gates

> **A structural proxy for a semantic property REPORTS; it never blocks.**
> Canonical formulation: [`.claude/skills/shared/sdd-artifact-contract.md`](../shared/sdd-artifact-contract.md) (beside RIT). **Cited, not restated.**

Harvest **detection** is a structural signal — _an invariant enforced at ≥2 points with no business rule citing it_ (the countable property `references/sync.md` step 2 already asks for). It is **mechanical**, so this skill may perform it. Its output is a **candidate list** for human or `/spec [mode=update]` adjudication.

- **NEVER an `error`. NEVER a build gate. NEVER a precondition on regeneration. NEVER a fixture that fails CI.**
- The detector is a **structural proxy**: it infers a semantic property from a correlate, and the rule-citation link it reads is **prose, not a key**. It has false positives (a covered invariant can present as uncovered) **and** false negatives (an invariant enforced at one chokepoint is invisible to a ≥2-point counter).
- **Why it may not gate:** a false positive that blocks a build gets suppressed — **and a suppressed detector is a dead detector.** A `report` cannot be suppressed, because it never blocked anything worth suppressing it for.
- **A detection changes the report, never the tree** — so it cannot break C6.

**The boundary — C9 does NOT license softening anything else:**

| Rule                                                | Operationally defined?                       | Severity                 | Why                                                                                    |
| --------------------------------------------------- | -------------------------------------------- | ------------------------ | -------------------------------------------------------------------------------------- |
| **C1** — DERIVED banner                             | **Yes** — a literal string test              | **`error`**              | The banner check **is** the rule                                                       |
| **C6** — regeneration-idempotency                   | **Yes** — regenerate, diff empty             | **`error`**              | **An ORACLE, not a proxy — it re-runs the transform and compares. It does not infer.** |
| **C7** — no A-E resurrection                        | **Yes** — a **closed** filename set          | **`error`**              | The filename list **is** the rule                                                      |
| **C2** — no `US-`/`AC-`/`BR-` in the technical tree | **Yes** — a static prefix denylist           | **`error`**              | The prefix list **is** the rule                                                        |
| **M1 / tech-token bans on the business tree**       | **Yes** — a token denylist                   | **`error`**              | Operationally defined; the spine stands                                                |
| **Harvest detector**                                | **No** — measures a correlate and **infers** | **REPORT — never gates** | The proxy rule                                                                         |

> **Do not misread C6 as a proxy.** C6's rule is _"regeneration over unchanged source produces an empty diff"_ — **and the empty diff IS the rule.** It executes the property rather than reasoning toward it. Demoting C6 would destroy the only real oracle here. **C6 gates at `error`, and nothing stands behind it to be a proxy for.**

---

## Step 0 — Scope Gate (MANDATORY FIRST)

Before reading anything, use `AskUserQuestion`. Confirm:

| Dimension    | Question                                                                                         | Auto-Default   |
| ------------ | ------------------------------------------------------------------------------------------------ | -------------- |
| **Scope** ★  | Which `{Service}` / `{Component}` — one component, one service, or the whole technical root?     | — must confirm |
| **Mode** ★   | `generate` (regenerate the view) OR `audit` (staleness report) OR `sync` (reconcile §8 ↔ tests)? | `generate`     |
| **Sections** | Full view, or a subset (use-case inventory / TC↔test map / topology)?                            | Full view      |

> **[BLOCKING]** Resolve `specRoots.technical.path` from `docs/project-config.json` FIRST. If it is absent, STOP — the technical root is not configured and this skill has no destination. NEVER hardcode a root.
> **[BLOCKING]** If the target `{Service}`/`{Component}` has **no** derivable source (no handlers, consumers, jobs, or annotated tests), STOP — there is nothing to derive from. **NEVER fabricate a component to document.**

---

## Step 1 — Derive the Facts (grep, never recall)

Read `references/author.md` and execute its derivation greps. Extract ONLY mechanically-derivable facts:

1. **Use Case Inventory** — write ops (N), read ops (M), event-driven (K), background jobs (J), and actor roles, per `references/author.md`.
2. **TC↔test map** — the join over existing test annotations (`TestSpec` for business TC coverage, `TechnicalSpec` for technical-only coverage when present), generated from the annotations that already exist in code. **NEVER hand-move this data.**
3. **Cross-service topology** — producers, consumers, sagas, shared contracts, data ownership (the `SYNC:cross-service-check` scan below is the procedure).
4. **Anchors** — every fact carries an abstract `[Source: {namespace}/{service}/{id}]` anchor.

> **Scale note:** for a service with many components, you MAY spawn parallel reader sub-agents (one per component) that each return the extracted fields above. This is an optimization, not a gate.
> **[BLOCKING]** Do NOT interpret, rank, assess business relevance, or judge any derived fact (**C8**). Count it, anchor it, emit it.

---

## Step 2 — Instantiate the Templates

Per `references/author.md`: fixed sections, **declared order**, **pinned table sort keys**, templated prose over grepped values.

> **[BLOCKING]** **A fact that cannot be templated is emitted in a table, never narrated.** Free composition is where non-determinism lives, and it breaks **C6**.

---

## Step 3 — Stamp & Write

- Every generated file opens with the `> DERIVED — regenerate with the tech-spec skill; do NOT hand-edit` banner + a regenerate date.
- Write each file immediately after instantiating it; do NOT accumulate large outputs in context (**C4**).

---

## Step 4 — Verify (self-check before completing)

- [ ] **No retired artifacts emitted** — grep your own output paths: zero `M[0-9]` dirs, zero `A-domain-model`/`B-business-rules`/`C-api-contracts`/`D-events`/`E-user-journeys`, zero `00-module-registry`/`01-domain-erd`/`06-reimplementation-guide`.
- [ ] **DERIVED banner + regenerate date present** on each generated file.
- [ ] **No business artifact types** — zero `US-`, `AC-`, `BR-` identifiers anywhere under the technical root (**C2**).
- [ ] **No canonical claims** — the derived files never assert they are the source of truth (**C3**).
- [ ] **Every anchor resolves** — grep the source path; mark `[UNVERIFIED]` rather than guessing.
- [ ] **No secrets** — zero connection strings, credentials, tokens, internal hostnames, or customer data encountered while reading config/seeders/fixtures.
- [ ] **Idempotency** — re-running over unchanged source produces an empty diff (**C6**).

---

## Hard Prohibitions (NON-NEGOTIABLE)

This skill produces only the DERIVED technical view. Emitting an A-E engineering tree would create a second source of truth competing with the Feature Spec — and a generator still able to recreate A-E would **resurrect the retired tree on its next run**, which is an active hazard rather than a theoretical one: the tree has come back once already through a rebase and had to be re-deleted. Therefore this skill MUST NEVER create:

| Forbidden output                                                                                          | Why                                                                |
| --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `M##` directories (e.g., `M01/`, `M02/`)                                                                  | Retired per-module partition                                       |
| `A-domain-model.md` / `B-business-rules.md` / `C-api-contracts.md` / `D-events.md` / `E-user-journeys.md` | Retired A-E engineering bundle — content lives in the Feature Spec |
| `00-module-registry.md`                                                                                   | Retired registry                                                   |
| `01-domain-erd.md`                                                                                        | Retired per-system ERD name                                        |
| `06-reimplementation-guide.md`                                                                            | Retired per-system name                                            |
| Any `US-` / `AC-` / `BR-` identifier                                                                      | Business artifact types — the Feature Spec owns them (**C2**)      |
| Any file under `specRoots.business.path`                                                                  | This skill never writes the business tree (**C5**)                 |
| A hand-edit invitation, a "maintained by" line, or any canonical claim                                    | The view is regenerable output (**C1**, **C3**)                    |

**Scope:** this prohibition governs the **emit set** under `specRoots.technical.path` — the filenames this skill may create. It does not ban writing those names in prose elsewhere (an ADR recording the retirement must be able to name them as history).

If a user explicitly asks for an A-E bundle, explain it is retired and offer the derived view instead. If a user asks this skill to write a business rule or user story, **route to `/spec`** — this skill has no authoring path.

---

## Related Skills

| Skill                | Relationship                                                                                              | When to Call                                                     |
| -------------------- | --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `/spec`              | **Business owner** — authors the canonical tech-free 8-section Feature Spec. `/tech-spec` never writes it | When a harvested candidate needs a rule authored (`mode=update`) |
| `/spec [mode=tests]` | **Owner of §8 TCs** that this skill's TC↔test map joins against                                           | When a coverage gap needs a canonical TC                         |
| `/spec-index`        | **Sibling derived-aid generator** over the business tree — same contract shape, different source          | For business-tree navigation aids                                |
| `/integration-test`  | **Consumer** — generates the tests whose annotations this skill joins                                     | When `sync` flags a TC with no covering integration test         |
| `/docs-update`       | **Orchestrator** — may call `/tech-spec` to refresh the derived view after code changes                   | After code changes need a full doc sync                          |

## What Is `/tech-spec`?

A **derived-view generator** over code + tests. The canonical technical knowledge is **the code itself**, and a technical-only behavior's guard is **its test**; this skill assembles a regenerable projection (use-case inventory, TC↔test map, topology) so a component's technical surface can be read without a second hand-maintained layer. It does **not** reverse-engineer code into a parallel _canonical_ bundle — that role was retired with the A-E tree, and this skill exists precisely because a projection cannot rival its own source.

---

<!-- SYNC:cross-service-check -->

> **Cross-Service Check** — Microservices/event-driven: MANDATORY before concluding investigation, plan, spec, or feature doc. Missing downstream consumer = silent regression.
>
> | Boundary            | Grep terms                                                                      |
> | ------------------- | ------------------------------------------------------------------------------- |
> | Event producers     | `Publish`, `Dispatch`, `Send`, `emit`, `EventBus`, `outbox`, `IntegrationEvent` |
> | Event consumers     | `Consumer`, `EventHandler`, `Subscribe`, `@EventListener`, `inbox`              |
> | Sagas/orchestration | `Saga`, `ProcessManager`, `Choreography`, `Workflow`, `Orchestrator`            |
> | Sync service calls  | HTTP/gRPC calls to/from other services                                          |
> | Shared contracts    | OpenAPI spec, proto, shared DTO — flag breaking changes                         |
> | Data ownership      | Other service reads/writes same table/collection → Shared-DB anti-pattern       |
>
> **Per touchpoint:** owner service · message name · consumers · risk (NONE / ADDITIVE / BREAKING).
>
> **BLOCKED until:** Producers scanned · Consumers scanned · Sagas checked · Contracts reviewed · Breaking-change risk flagged

<!-- /SYNC:cross-service-check -->

<!-- SYNC:ai-mistake-prevention -->

> **AI Mistake Prevention** — Failure modes to avoid on every task:
>
> **Re-read files after context changes.** Context compaction, resume, or long-running work can make memory stale; verify current files before acting.
> **Verify generated content against source evidence.** AI hallucinates APIs, names, claims, and document facts. Check the relevant source before documenting or referencing.
> **Check downstream references before deleting or renaming.** Removing an artifact can stale docs, generated mirrors, configs, and callers; map references first.
> **Trace the full impact chain after edits.** Changing a definition can miss derived outputs and consumers. Follow the affected chain before declaring done.
> **Verify ALL affected outputs, not just the first.** One green check is not all green checks; validate every output surface the change can affect.
> **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Before changing or reporting a constant, limit, flag, cutoff, wording, or pattern, read nearby context and history, the CALLER's ordering, and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard.
> **Surface ambiguity before acting — don't pick silently.** Multiple valid interpretations require an explicit question or stated assumption with risk.
> **Assert the outcome your system owns, not the intermediate state your infrastructure owns.** When verifying async work, assert the final business state — never the delivery/retry bookkeeping held in shared infrastructure that any co-running process can write. Such a check passes when run alone and flakes the moment anything else shares that infrastructure.
> **Keep shared guidance role-relevant.** Universal guidance must help every receiving skill or agent; code-specific obligations belong only in code-specific protocols.

<!-- /SYNC:ai-mistake-prevention -->

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:cross-service-check:reminder -->

**IMPORTANT MUST ATTENTION** microservices/event-driven: scan producers, consumers, sagas, contracts in task scope. Per touchpoint: owner · message · consumers · risk (NONE/ADDITIVE/BREAKING). Missing consumer = silent regression.

<!-- /SYNC:cross-service-check:reminder -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

**IMPORTANT MUST ATTENTION** follow declared step order for this skill; NEVER skip, reorder, or merge steps without explicit user approval
**IMPORTANT MUST ATTENTION** for every step/sub-skill call: set `in_progress` before execution, set `completed` after execution
**IMPORTANT MUST ATTENTION** every skipped step MUST include explicit reason; every completed step MUST include concise evidence
**IMPORTANT MUST ATTENTION** if Task tools unavailable, maintain an equivalent step-by-step plan tracker with synchronized statuses

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:END -->

<!-- SYNC:parallel-subagent-dispatch -->

> **Parallel Sub-Agent Dispatch** — Plan parallelism the moment a task breakdown exists, BEFORE executing it — running provably independent tasks sequentially wastes wall-clock. Applies to every multi-step job: workflow steps, planning, batch updates, investigation, research, scans, reviews, doc sync. **Plan execution is metadata-gated, NEVER default-parallel** — fan-out follows ONLY what the plan declares (`PAR`/`SEQ` tags + per-phase write set); an untagged plan runs sequentially — why: a derived write set cannot see cascade or generated writes.
>
> 1. **Tag every task `PAR` or `SEQ`.** `PAR` = inputs exclude every pending task's output AND write set disjoint from every other `PAR`. Else `SEQ` — MUST ATTENTION name the dependency forcing it.
> 2. **Group `PAR` into waves.** No edge between members. Two writers of one file NEVER share a wave. Read-only work (search, investigation, review, research) parallelizes freely.
> 3. **Declare before dispatch:** `Parallel plan: wave 1 = [...] · wave 2 = [...] · SEQ = [...] (reason)`.
> 4. **Spawn each wave in ONE message** — every `Agent` call in one response, NEVER dripped per turn. Route each task to its specialist (`.claude/skills/shared/sub-agent-selection-guide.md`); NEVER `code-reviewer` as catch-all.
> 5. **Brief each sub-agent self-contained:** goal · scope + owned files · reference docs · return contract (summary + `Full report:` path, per SYNC:subagent-return-contract) · incremental persistence to `plans/reports/` (per SYNC:incremental-persistence).
> 6. **Barrier per wave.** Advance ONLY after EVERY member returns (a skipped conditional counts as returned). Merge, mark each task completed/skipped, THEN dispatch the next wave. Mutating steps wait for the barrier.
> 7. **One level deep.** A dispatched sub-agent executes its own brief; further fan-out stays the orchestrator's job unless that agent's `.claude/agents/*.md` definition authorizes it.
>
> **NEVER parallelize:** tasks sharing a write target · a task consuming a pending task's output · trivial single-file work (dispatch overhead > gain) · an order a skill or workflow explicitly fixes · gates awaiting user approval.
>
> **Blocked until:** MUST ATTENTION every task tagged PAR/SEQ with a named reason per SEQ · waves declared + write-set disjointness checked · each wave spawned in ONE message · barrier honored before the next wave.

<!-- /SYNC:parallel-subagent-dispatch -->

<!-- SYNC:parallel-subagent-dispatch:reminder -->

- **MANDATORY** After planning tasks, tag each PAR/SEQ and spawn every PAR wave as parallel sub-agents in ONE message — default parallel for workflows, batch updates, investigation, research, reviews; plan execution fans out ONLY on what the plan declares.
- **MANDATORY** Disjoint write sets per wave · all-return barrier before the next wave · specialist routing · sub-agents NEVER fan out further unless their own agent definition authorizes it.

<!-- /SYNC:parallel-subagent-dispatch:reminder -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

- **IMPORTANT MUST ATTENTION Goal:** Project code + tests into a regenerable, single-writer technical view (use-case inventory + TC↔test map + topology) — so a component's technical surface can be read without ever forking a second, hand-maintained source of truth
- **IMPORTANT MUST ATTENTION Main steps (in order):** Step 0 Scope Gate (`AskUserQuestion` scope+mode, BLOCKING; resolve `specRoots.technical.path` FIRST) → Step 1 Derive facts (grep inventory, `TestSpec`/`TechnicalSpec` joins, topology) → Step 2 Instantiate templates (pinned order + sort keys) → Step 3 Stamp & Write (DERIVED banner + date, write each immediately) → Step 4 Verify (no retired artifacts, banner, no `US-`/`AC-`/`BR-`, no canonical claims, no secrets) — why: AI keeps forgetting the skill owns this fixed sequence; NEVER skip or reorder without user approval

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries — MUST ATTENTION each canonical body above):**

- **Cross-Service Check:** scan producers/consumers/sagas/contracts; flag breaking-change risk.
- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.
- **Critical Thinking:** NEVER present a guess as fact; traced proof, confidence >80% to act.

- **IMPORTANT MUST ATTENTION [BLOCKING]** This skill GENERATES; it NEVER authors. No user story, acceptance criterion, business rule, or §8 TC is ever written here — route to `/spec` — why: carrying the Feature Spec's own artifact types is how a rival tree competes on its turf
- **IMPORTANT MUST ATTENTION [BLOCKING]** Output is DERIVED + regenerable — never a second source of truth; when the view disagrees with code, **code is right and the view is stale — regenerate it**
- **IMPORTANT MUST ATTENTION [BLOCKING]** Never emit `M##`/A-E/`00-module-registry`/`01-domain-erd`/`06-reimplementation-guide` under the technical root — why: an A-E bundle becomes a second source of truth, and a generator able to recreate it resurrects the retired tree on its next run
- **IMPORTANT MUST ATTENTION [BLOCKING]** Stamp the DERIVED banner + regenerate date on every generated file; write after each artifact, never accumulate large outputs in context
- **IMPORTANT MUST ATTENTION [BLOCKING]** **Never judge at generation time** (**C8**) — mechanical detect + route only; judgment is not stable across runs, so a judging generator stops being idempotent and fails **C6** against its own tree while reporting the cause as `hand-edited`
- **IMPORTANT MUST ATTENTION [BLOCKING]** The harvest detector **REPORTS, never gates** (**C9**) — never `error`, never a build gate, never a precondition on regeneration — why: a false positive that blocks a build gets suppressed, and a suppressed detector is a dead detector. **This does NOT soften C1/C2/C6/C7 or M1 — all stay at `error`; C6 is an oracle, not a proxy**
- **IMPORTANT MUST ATTENTION [BLOCKING]** Confirm scope + mode via `AskUserQuestion` BEFORE any read; no derivable source → STOP, never fabricate a component to document
- **IMPORTANT MUST ATTENTION [REQUIRED]** Read the root from `specRoots.technical.path`; `{TechRoot}/{Service}/{Component}.md` is a PATTERN — never hardcode a root, a project, a service, or a TC ID
- **IMPORTANT MUST ATTENTION [REQUIRED]** Templated prose over grepped facts ONLY — a fact that cannot be templated goes in a table, never a sentence — why: free composition is where non-determinism lives, and it breaks the idempotency oracle **and** is how a secret gets incidentally pasted
- **IMPORTANT MUST ATTENTION** Cite `[Source:]` anchor evidence for every derived fact (confidence >80% to act, <60% mark `[UNVERIFIED]`) — NEVER fabricate a handler, consumer, job, or TC ID; grep to confirm
- **IMPORTANT MUST ATTENTION** Break task scope into small `TaskCreate` todos (one per emitted artifact) before acting; mark each `completed` immediately after its file is written; keep exactly one `in_progress`
- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.

**Anti-Rationalization:**

| Evasion                                                                            | Rebuttal                                                                                                                                       |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| "I found real insight the grep missed — I'll just add a note"                      | That is authoring. The view holds nothing of its own. Un-greppable nuance belongs in a code comment or an ADR next to the code.                |
| "This component needs a business rule written down"                                | Route to `/spec [mode=update]`. This skill detects and reports; it has no authoring path.                                                      |
| "The regenerate diff is noisy — I'll scope idempotency to the mechanical sections" | That is a per-section carve-out — the exemption disease at a new address. **Shrink the prose surface; NEVER relax the oracle.**                |
| "The harvest detector found a real gap — make it fail the build"                   | NEVER. It is a proxy; a proxy that blocks gets suppressed, and a suppressed detector is dead. Report it.                                       |
| "The tech tree is M1-exempt, so business content is fine too"                      | Two orthogonal properties. `m1Policy` governs tech-agnostic strictness; it says nothing about business content. `US-`/`AC-`/`BR-` stay banned. |
| "Hand-editing this one file is faster than regenerating"                           | A hand-edited derived file is a build failure. Fix the generator or the source, then regenerate.                                               |
| "I'll cache the judgment so the next run is consistent"                            | Generator-owned state is a staleness problem invisible to review and to `git`. Verdicts live in the artifact.                                  |
| "A-E would express this better for engineers"                                      | A-E is retired and has resurrected once already. Emit the derived view.                                                                        |

**[TASK-PLANNING]** MUST ATTENTION analyze task scope and break into small todo tasks/sub-tasks via TaskCreate before acting.

> **[IMPORTANT]** Break into many small todo tasks systematically before starting — this is critical.

**IMPORTANT MUST ATTENTION** GENERATE, never author — output is DERIVED + regenerable; code + tests are the source of truth.
**IMPORTANT MUST ATTENTION** Never judge at generation time; the harvest detector reports and never gates — but C1/C2/C6/C7 stay at `error`.
**IMPORTANT MUST ATTENTION** Root from `specRoots.technical.path`; never emit A-E/`M##`/retired filenames; never write `US-`/`AC-`/`BR-`.

---
