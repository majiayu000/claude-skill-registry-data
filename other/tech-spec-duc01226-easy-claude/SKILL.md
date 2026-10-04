---
name: tech-spec
version: 1.0.0
description: '[Documentation] Use when generating the DERIVED technical spec view over code and tests, or reporting §8 TC drift. Generator only, never authors business content. generate|audit|sync.'
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

**Goal:** For annotation-compatible projects, project code and configured test annotations into a regenerable technical view without creating a second source of truth; route native-case reconciliation to its canonical owner and never report unsupported generation as empty success.

**Summary:**

- **Purpose:** a DERIVED-view annotation generator ONLY — it reads code plus the configured `TestSpec` / `TechnicalSpec` contract and never authors business content. It has no native-case carrier adapter.
- **Profile gate:** resolve `specArtifacts` and `specRoots` first. A valid native profile routes `sync` through `/spec [mode=sync]`; `generate` is `UNSUPPORTED` until a compatible generator exists. If no native profile applies, keep the strict §8/TC default. Missing or invalid required contracts remain `NOT CONFIGURED` / blocked; never fall back or claim empty success.
- **Main steps (run in order):** **Step 0** Resolve config/profile/root and scope/mode; ask only for ambiguous scope or mode. Native generation → report `UNSUPPORTED` and stop before the generator; absent `techSpecScan` → `NOT CONFIGURED`. **Step 1** Derive supported annotation facts — use-case inventory, annotation joins, topology. **Step 2** Instantiate the fixed templates. **Step 3** Stamp & write each artifact immediately. **Step 4** Verify no retired artifacts, banners, business content, canonical claims, or secrets.
- **Modes:** `generate` only when the annotation generator contract applies · `audit` reports freshness only for a configured derived view · `sync` routes native profiles to `/spec [mode=sync]`, or reports canonical §8 TC ↔ test-code drift under the strict default (`references/sync.md`).
- Hard prohibition is the load-bearing rule: never emit the retired A-E engineering tree, `M##` dirs, `00-module-registry.md`, `01-domain-erd.md`, or `06-reimplementation-guide.md` under the technical root — why: an A-E bundle becomes a second source of truth competing with the Feature Spec, and a generator able to recreate it resurrects the retired tree on its next run (this has occurred once already, via rebase).
- Every generated file carries the `> DERIVED — regenerate with the tech-spec skill; do NOT hand-edit` banner + a regenerate date, anchors each fact back to its source, and makes **no canonical claim**.
- **This skill is M1-EXEMPT** (`specRoots.technical.m1Policy: "exempt"`) — its prose MAY name technology. That exemption is the whole reason this tree exists; it is NOT a licence to carry business content (see **Hard Prohibitions**).

> **[SCOPE]** This skill generates a **DERIVED** technical view over code + tests under `specRoots.technical.path`. It MUST NOT emit a per-module A-E engineering bundle (`A-domain-model`, `B-business-rules`, `C-api-contracts`, `D-events`, `E-user-journeys`), `M##` directories, `00-module-registry.md`, `01-domain-erd.md`, or `06-reimplementation-guide.md` — those are not part of the spec model. It MUST NOT author business content: the Feature Spec under `specRoots.business.path` owns §1–§8, and this skill neither writes nor amends it. Authority: [`docs/project-reference/spec-system-reference.md`](../../../docs/project-reference/spec-system-reference.md) — project-reference docs root default `docs/project-reference`; a `docsRoots.projectReference.path` entry in `docs/project-config.json` overrides the path — and [`.claude/skills/shared/sdd-artifact-contract.md`](../shared/sdd-artifact-contract.md).

**Inputs:** supported annotation mode reads the code tree (command/query handlers, event consumers, background jobs, producers, sagas, outbox) and configured test annotations (`TestSpec` / `TechnicalSpec`). **Code is the technical source of truth** — this skill projects a view and never populates a parallel canonical layer. A native profile is not an input to this annotation generator.

**Modes:**

| Mode       | Trigger                                    | Input                                          | Output                                                                       |
| ---------- | ------------------------------------------ | ---------------------------------------------- | ---------------------------------------------------------------------------- |
| `generate` | default — only when the annotation generator contract applies | code + configured test annotations | `{TechRoot}/{Service}/{Component}.md`, all DERIVED (`references/author.md`); native profiles are unsupported |
| `audit`    | explicit request — staleness check          | code/test mtimes or git vs an existing derived view | Stale-list report when configured; otherwise `NOT CONFIGURED`. Never mutates |
| `sync`     | "sync tests" / "reconcile tests" / harvest  | native profile, or §8 TCs under strict default | Native: `/spec [mode=sync]` report. Default: §8/test drift and route-only `CoveredBy:` / orphan report (`references/sync.md`) |

**Tooling:**

These are the ONLY invocations. `.claude/` is portable and self-running — never route this tooling
through a host `package.json` script, which does not exist in a project that copied only the bundle.
Before an interactive generation, resolve the profile and require the supported annotation contract. An absent `techSpecScan` is `NOT CONFIGURED`; do not invoke `--optional` and present its successful skip as coverage.

- `node .claude/skills/tech-spec/scripts/generate-tech-specs.mjs` — regenerate the derived technical
  views from code/test annotations.
- `node .claude/skills/tech-spec/scripts/generate-tech-specs.mjs --check` — read-only freshness and
  annotation-occurrence completeness gate. It is fail-closed when a project contract is absent or
  malformed; add `--optional` only for an orchestration entry point that should record an absent
  `techSpecScan` contract as a skip (the sync runner's `tech-spec-freshness` stage does exactly this).

**Mode resolution (do this before any work):**

1. Read `docs/project-config.json`; resolve `specArtifacts`, `specRoots.technical.path`, and `techSpecScan` before selecting a procedure. A malformed declared profile blocks; it never falls back to TC.
2. Parse the mode from the invocation: explicit `[mode=<x>]` wins; otherwise infer from the request.
3. A native profile routes `sync` to `/spec [mode=sync]`; its `generate` view is `UNSUPPORTED` and must stop before the annotation generator. Without a native profile, strict §8/TC sync remains the default; generation still requires the configured annotation contract.
4. If scope/mode remains ambiguous, ask via `AskUserQuestion` before mutation.
5. **Read the matching `references/` body** — it owns that mode's procedure and output contract. Do not run a mode from memory.

**Workflow:** `/investigate` (locate the component) → `/tech-spec` (project the view) → `/changes-review` → `/watzup`

**Key Rules:**

- **MUST ATTENTION** resolve `specArtifacts`, `techSpecScan`, `specRoots.technical.path`, and mode before generation; never hardcode roots or component names.
- **MUST ATTENTION** route native-profile reconciliation through `/spec [mode=sync]`; keep strict §8/TC behavior only when no native profile applies.
- **MUST ATTENTION** require `/spec [mode=sync]` to return its configured native reconciliation report; **NEVER** treat a missing report as a successful sync.
- **MUST ATTENTION** map each selected owner/case/variant through the actual executor, assertion, and run evidence; **NEVER** infer coverage from title or identity alone.
- **MUST ATTENTION** report native generation as `UNSUPPORTED` and absent annotation configuration as `NOT CONFIGURED` before invoking the generator; never emit or accept an empty success.
- **NEVER** author business content or emit retired A-E artifacts; code/tests remain the source of truth.
- **MUST ATTENTION** derive facts mechanically, anchor them to sources, write each artifact immediately, and verify regeneration is idempotent.
- **NEVER** let the harvest detector gate generation; it reports candidates while C1/C2/C6/C7 remain hard errors.

---

## The Generator Contract (NON-NEGOTIABLE)

This skill is a **generator**, not an author. Every clause below is structural — none is a preference a future maintainer may relax for convenience.

| # | Clause | Why |
| --- | --- | --- |
| **C1** | **[BLOCKING]** Output is **DERIVED and regenerable** — every generated file carries a `> DERIVED — regenerate with the tech-spec skill; do NOT hand-edit` banner + a regenerate date. It is **NEVER a second source of truth**. | A derived view makes no truth claim, so it cannot compete for canonical status. A hand-editable tree makes one — and then "which is right, the doc or the code?" becomes askable. |
| **C2** | **[BLOCKING]** **Never authors business content.** No user story, no acceptance criterion, no business rule, no §1–§7 prose, no §8 TC is written by this skill — in any mode. The Feature Spec stays the source of truth for all of it. | Carrying the Feature Spec's own artifact types is exactly how a rival tree competes on the Feature Spec's turf. |
| **C3** | **[BLOCKING]** **Never claims to be a source of truth.** The generated files never assert canonical authority. When the view disagrees with code, **code is right by construction and the view is stale — regenerate it.** | A derived aid that asserts canonical authority corrupts the single-writer contract. |
| **C4** | **[BLOCKING]** **Write each artifact immediately** after instantiating it; do NOT accumulate large outputs in context. | A `{Service}/{Component}` fan-out is exactly the case that exhausts context mid-run and loses every unwritten artifact. |
| **C5** | **[BLOCKING]** **Single writer.** This skill is the **sole writer** under `specRoots.technical.path`. Nothing else writes there; it writes nowhere else. | Two writers is how a view becomes a sibling. |
| **C6** | **[BLOCKING]** **Regeneration is idempotent** — regenerating over unchanged source produces an **empty diff**. | This is the tree's flagship oracle: it proves the artifact can be thrown away and rebuilt from its source. If it cannot, the tree holds content of its own — it claims truth, and it is a rival. |
| **C7** | **[BLOCKING]** **A-E filenames are never emitted.** See **Hard Prohibitions**. | An A-E bundle becomes a second source of truth competing with the Feature Spec. |

### C8 — Mechanical detect + route · never judge · never write business content

> **A generator MUST NEVER apply RIT — or any judgment test — at generation time.** Judgment produces data; generators consume data.
> Canonical formulation: [`.claude/skills/shared/sdd-artifact-contract.md`](../shared/sdd-artifact-contract.md) (beside RIT). **Cited, not restated.**

| | Who | When | Output |
| --- | --- | --- | --- |
| **Judgment** (RIT, business-invariant verdicts, visibility classification) | a human, or an AI **outside** this generator | **once**, at authoring/classification time | a **persisted verdict — data** |
| **Generation** | `/tech-spec` | every run | output **mechanically re-derived** from that data |

**Idempotency holds because nothing is re-judged.** The generator reads a verdict it did not make and cannot revise. Same source + same verdicts ⇒ same output, every run. **A generator that judges is not idempotent — it fails C6 against its own tree, permanently, and the failure reports as `hand-edited`, which is the wrong cause and undiagnosable.**

**Two resolutions that are FORBIDDEN, because both look like fixes:**

| Rejected | Why it fails |
| --- | --- |
| **Scope idempotency to only the mechanical sections** | Reintroduces a **per-section carve-out** — an exemption at a new address. A carve-out is this framework's characteristic failure; do not re-mint one inside the oracle. |
| **Cache judgments inside the generator** | The generator then owns a **staleness problem**: a cached verdict that outlives the code it judged, invisible to review and to `git`. **Persisted verdicts belong in the artifact, not in generator state.** |

### C9 — The harvest detector REPORTS; it never gates

> **A structural proxy for a semantic property REPORTS; it never blocks.**
> Canonical formulation: [`.claude/skills/shared/sdd-artifact-contract.md`](../shared/sdd-artifact-contract.md) (beside RIT). **Cited, not restated.**

Harvest **detection** is a structural signal — *an invariant enforced at ≥2 points with no business rule citing it* (the countable property `references/sync.md` step 2 already asks for). It is **mechanical**, so this skill may perform it. Its output is a **candidate list** for human or `/spec [mode=update]` adjudication.

- **NEVER an `error`. NEVER a build gate. NEVER a precondition on regeneration. NEVER a fixture that fails CI.**
- The detector is a **structural proxy**: it infers a semantic property from a correlate, and the rule-citation link it reads is **prose, not a key**. It has false positives (a covered invariant can present as uncovered) **and** false negatives (an invariant enforced at one chokepoint is invisible to a ≥2-point counter).
- **Why it may not gate:** a false positive that blocks a build gets suppressed — **and a suppressed detector is a dead detector.** A `report` cannot be suppressed, because it never blocked anything worth suppressing it for.
- **A detection changes the report, never the tree** — so it cannot break C6.

**The boundary — C9 does NOT license softening anything else:**

| Rule | Operationally defined? | Severity | Why |
| --- | --- | --- | --- |
| **C1** — DERIVED banner | **Yes** — a literal string test | **`error`** | The banner check **is** the rule |
| **C6** — regeneration-idempotency | **Yes** — regenerate, diff empty | **`error`** | **An ORACLE, not a proxy — it re-runs the transform and compares. It does not infer.** |
| **C7** — no A-E resurrection | **Yes** — a **closed** filename set | **`error`** | The filename list **is** the rule |
| **C2** — no `US-`/`AC-`/`BR-` in the technical tree | **Yes** — a static prefix denylist | **`error`** | The prefix list **is** the rule |
| **M1 / tech-token bans on the business tree** | **Yes** — a token denylist | **`error`** | Operationally defined; the spine stands |
| **Harvest detector** | **No** — measures a correlate and **infers** | **REPORT — never gates** | The proxy rule |

> **Do not misread C6 as a proxy.** C6's rule is *"regeneration over unchanged source produces an empty diff"* — **and the empty diff IS the rule.** It executes the property rather than reasoning toward it. Demoting C6 would destroy the only real oracle here. **C6 gates at `error`, and nothing stands behind it to be a proxy for.**

---

## Step 0 — Scope Gate (MANDATORY FIRST)

Before deriving facts or invoking a generator, read the project config and resolve the profile and technical root. Use `AskUserQuestion` only if scope or mode remains ambiguous. A native-profile generation request returns `UNSUPPORTED` here; do not continue to the annotation generator.

| Dimension       | Question                                                                                          | Auto-Default          |
| --------------- | ------------------------------------------------------------------------------------------------- | --------------------- |
| **Scope** ★     | Which `{Service}` / `{Component}` — one component, one service, or the whole technical root?      | — must confirm        |
| **Mode** ★      | `generate` (supported annotation view only) OR `audit` OR `sync` (native `/spec` report, or strict-default §8 ↔ tests)? | `generate` |
| **Sections**    | Full view, or a subset (use-case inventory / TC↔test map / topology)?                             | Full view             |

> **[BLOCKING]** Resolve `specArtifacts`, `techSpecScan`, and `specRoots.technical.path` from `docs/project-config.json` FIRST. If the technical root is absent, STOP. A native profile does not authorize annotation generation; absent/unsupported generator configuration is `NOT CONFIGURED` / `UNSUPPORTED`, never an empty successful view.
> **[BLOCKING]** If the target `{Service}`/`{Component}` has **no** derivable source (no handlers, consumers, jobs, or annotated tests), STOP — there is nothing to derive from. **NEVER fabricate a component to document.**

---

## Step 1 — Derive the Facts (grep, never recall)

Read `references/author.md` and execute its derivation greps. Extract ONLY mechanically-derivable facts:

1. **Use Case Inventory** — write ops (N), read ops (M), event-driven (K), background jobs (J), and actor roles, per `references/author.md`.
2. **TC↔test map (strict default only)** — join existing configured `TestSpec` annotations for business TC coverage and `TechnicalSpec` for technical-only coverage. Do not apply this map when a native profile is selected; native reconciliation belongs to `/spec [mode=sync]`. **NEVER hand-move annotation data.**
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

| Skill                | Relationship                                                                                                    | When to Call                                                  |
| -------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| `/spec`              | **Business owner** — authors the canonical tech-free 8-section Feature Spec. `/tech-spec` never writes it        | When a harvested candidate needs a rule authored (`mode=update`) |
| `/spec [mode=tests]` | **Owner of strict-default §8 TCs** joined by the annotation view                                                   | When the no-native-profile default needs a canonical TC       |
| `/spec [mode=sync]`  | **Owner of native-profile reconciliation** — consumes the configured owner/case/variant and evidence contract     | When a native profile applies                                 |
| `/spec [mode=index]`        | **Sibling derived-aid generator** over the business tree — same contract shape, different source                | For business-tree navigation aids                             |
| `/integration-test`  | **Consumer** — generates the tests whose annotations this skill joins                                           | When `sync` flags a TC with no covering integration test      |
| `/docs-manager --mode=update`       | **Orchestrator** — may call `/tech-spec` to refresh the derived view after code changes                         | After code changes need a full doc sync                       |

## What Is `/tech-spec`?

A **derived-view generator** over code + configured annotations, not a native-case adapter. For supported annotation projects it assembles a regenerable projection without creating a second source of truth. Native profile reconciliation belongs to `/spec [mode=sync]`; native technical-view generation stays explicitly unsupported until a compatible generator contract is declared. When no native profile applies, this skill retains the strict §8/TC default.

---

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `cross-service-check` — Scan producers, consumers, sagas and shared contracts for cross-service impact; concluding an investigation, plan or spec in a service-based system → .claude/skills/shared/protocols/cross-service-check.md

<!-- PROTOCOL-GUIDES:END -->

<!-- SYNC:cross-service-check:reminder -->

**IMPORTANT MUST ATTENTION** microservices/event-driven: scan producers, consumers, sagas, contracts in task scope. Per touchpoint: owner · message · consumers · risk (NONE/ADDITIVE/BREAKING). Missing consumer = silent regression.

<!-- /SYNC:cross-service-check:reminder -->

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

**IMPORTANT MUST ATTENTION** follow declared step order for this skill; NEVER skip, reorder, or merge steps without explicit user approval
**IMPORTANT MUST ATTENTION** for every step/sub-skill call: set `in_progress` before execution, set `completed` after execution
**IMPORTANT MUST ATTENTION** every skipped step MUST include explicit reason; every completed step MUST include concise evidence
**IMPORTANT MUST ATTENTION** if Task tools unavailable, maintain an equivalent step-by-step plan tracker with synchronized statuses

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:END -->


## Closing Reminders

- **IMPORTANT MUST ATTENTION Goal:** For compatible annotation projects, produce a regenerable technical view without a second source of truth; route native reconciliation to `/spec [mode=sync]` and never treat unsupported generation as empty success.
- **IMPORTANT MUST ATTENTION Main steps (in order):** resolve `specArtifacts`, `techSpecScan`, and roots → native `sync` to `/spec [mode=sync]` or strict-default §8/TC sync; native generation `UNSUPPORTED`, absent generator config `NOT CONFIGURED` → for supported annotation generation derive facts → instantiate fixed templates → stamp/write immediately → verify outputs. Ask only for unresolved scope/mode; do not fall back or skip the explicit unsupported result.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries — MUST ATTENTION each canonical body above):**

- **Cross-Service Check:** scan producers/consumers/sagas/contracts; flag breaking-change risk.

- **IMPORTANT MUST ATTENTION [BLOCKING]** This skill GENERATES; it NEVER authors. No user story, acceptance criterion, business rule, or §8 TC is ever written here — route to `/spec` — why: carrying the Feature Spec's own artifact types is how a rival tree competes on its turf
- **IMPORTANT MUST ATTENTION [BLOCKING]** Output is DERIVED + regenerable — never a second source of truth; when the view disagrees with code, **code is right and the view is stale — regenerate it**
- **IMPORTANT MUST ATTENTION [BLOCKING]** Never emit `M##`/A-E/`00-module-registry`/`01-domain-erd`/`06-reimplementation-guide` under the technical root — why: an A-E bundle becomes a second source of truth, and a generator able to recreate it resurrects the retired tree on its next run
- **IMPORTANT MUST ATTENTION [BLOCKING]** Stamp the DERIVED banner + regenerate date on every generated file; write after each artifact, never accumulate large outputs in context
- **IMPORTANT MUST ATTENTION [BLOCKING]** **Never judge at generation time** (**C8**) — mechanical detect + route only; judgment is not stable across runs, so a judging generator stops being idempotent and fails **C6** against its own tree while reporting the cause as `hand-edited`
- **IMPORTANT MUST ATTENTION [BLOCKING]** The harvest detector **REPORTS, never gates** (**C9**) — never `error`, never a build gate, never a precondition on regeneration — why: a false positive that blocks a build gets suppressed, and a suppressed detector is a dead detector. **This does NOT soften C1/C2/C6/C7 or M1 — all stay at `error`; C6 is an oracle, not a proxy**
- **IMPORTANT MUST ATTENTION [BLOCKING]** Resolve config/profile before work; ask only for ambiguity. Native generation → `UNSUPPORTED`, absent `techSpecScan` → `NOT CONFIGURED`, invalid profile → blocked; never claim empty success
- **IMPORTANT MUST ATTENTION [REQUIRED]** Read `specArtifacts`, `techSpecScan`, and `specRoots.technical.path`; `{TechRoot}/{Service}/{Component}.md` is a PATTERN — never hardcode a root, project, service, native case, or TC ID
- **IMPORTANT MUST ATTENTION [REQUIRED]** Templated prose over grepped facts ONLY — a fact that cannot be templated goes in a table, never a sentence — why: free composition is where non-determinism lives, and it breaks the idempotency oracle **and** is how a secret gets incidentally pasted
- **IMPORTANT MUST ATTENTION** Cite `[Source:]` anchor evidence for every derived fact (confidence >80% to act, <60% mark `[UNVERIFIED]`) — NEVER fabricate a handler, consumer, job, native case, or TC ID; grep to confirm
- **IMPORTANT MUST ATTENTION** Break task scope into small `TaskCreate` todos (one per emitted artifact) before acting; mark each `completed` immediately after its file is written; keep exactly one `in_progress`
- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.

**Anti-Rationalization:**

| Evasion                                                       | Rebuttal                                                                                                          |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| "I found real insight the grep missed — I'll just add a note" | That is authoring. The view holds nothing of its own. Un-greppable nuance belongs in a code comment or an ADR next to the code. |
| "This component needs a business rule written down"           | Route to `/spec [mode=update]`. This skill detects and reports; it has no authoring path.                          |
| "The regenerate diff is noisy — I'll scope idempotency to the mechanical sections" | That is a per-section carve-out — the exemption disease at a new address. **Shrink the prose surface; NEVER relax the oracle.** |
| "The harvest detector found a real gap — make it fail the build" | NEVER. It is a proxy; a proxy that blocks gets suppressed, and a suppressed detector is dead. Report it.          |
| "The tech tree is M1-exempt, so business content is fine too" | Two orthogonal properties. `m1Policy` governs tech-agnostic strictness; it says nothing about business content. `US-`/`AC-`/`BR-` stay banned. |
| "Hand-editing this one file is faster than regenerating"      | A hand-edited derived file is a build failure. Fix the generator or the source, then regenerate.                   |
| "I'll cache the judgment so the next run is consistent"       | Generator-owned state is a staleness problem invisible to review and to `git`. Verdicts live in the artifact.      |
| "A-E would express this better for engineers"                 | A-E is retired and has resurrected once already. Emit the derived view.                                            |

**[TASK-PLANNING]** MUST ATTENTION analyze task scope and break into small todo tasks/sub-tasks via TaskCreate before acting.

> **[IMPORTANT]** Break into many small todo tasks systematically before starting — this is critical.

**IMPORTANT MUST ATTENTION** GENERATE, never author — output is DERIVED + regenerable; code + tests are the source of truth.
**IMPORTANT MUST ATTENTION** Never judge at generation time; the harvest detector reports and never gates — but C1/C2/C6/C7 stay at `error`.
**IMPORTANT MUST ATTENTION** Resolve profile and root first; native `sync` goes to `/spec [mode=sync]`, strict TC remains only the absent-profile default, and native generation is explicitly unsupported until a compatible generator exists. Never emit A-E/`M##`/retired filenames or business content.

---
