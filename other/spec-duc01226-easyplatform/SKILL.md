---
name: spec
version: 5.0.0
description: '[Documentation] Use to author, audit, amend, or test-spec a business Feature Spec. The single spec skill — modes draft|init|update|audit|amend create/maintain the tech-free 8-section Feature Spec; draft authors a provisional spec from an idea/requirement (no code yet, Evidence: TBD); tests generates Section 8 TC-{FEATURE}-{NNN} test specifications; sync reconciles §8 TCs ↔ executing test code. Per-mode procedure lives in references/{author,tests,sync}.md.'
triggers: 'feature spec, feature documentation, create feature doc, update feature doc, business feature documentation, audit feature spec, amend feature spec, spec from idea, generate spec from requirements, draft feature spec from prompt, idea to spec, requirements to spec, tdd spec, tdd test, test driven, write test specs, create test cases, update test specs, test specifications for feature, test spec for feature, sync test specs, generate test specs from code, update test specs after changes, test specs from PR, test specs from pull request, code to test specs, sync tests, reconcile tests with code, sync test specs to integration tests'
---

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

> **Portability:** `docs/specs/` is the fixed Feature Spec root. `docs/templates/detailed-feature-spec-template.md` remains the default template unless `workflowPatterns.featureDocTemplate` points to another template.

**[IMPORTANT] TaskCreate** — Break ALL work into small tasks BEFORE starting. For simple tasks, ask user whether to skip.

**Goal:** Own the entire Feature Spec lifecycle in one skill — author/maintain tech-free 8-section business Feature Specs (code evidence carried only in Section 8 test-case anchors, never prose), generate Section 8 test specifications, and reconcile those TCs with executing test code — producing a tech-free, AI-implementable Feature Spec whose Section 8 TC registry stays the single source of truth, traceable to test code, so any team can rebuild the feature on any stack from the spec alone. The mode you run determines which `references/` body drives work; the shared §8 contract, M1-M7 mandates, and quality philosophy below apply every mode.

**Summary:**

- **Purpose:** one skill owns the whole Feature Spec lifecycle across 7 modes — `draft | init | update | audit | amend | tests | sync` — producing/maintaining a tech-free 8-section business Feature Spec whose §8 TC registry is the single source of truth, traceable to executing test code, so any team can rebuild the feature on any stack from the spec alone.
- **Main steps (every run):** (1) resolve mode FIRST — explicit `[mode=<x>]` wins, else infer from request + repo state, ambiguous → `AskUserQuestion` before any mutating mode; (2) read the matching `references/{author,tests,sync}.md` body — NEVER run a mode from memory; (3) `TaskCreate`-break the work (one task per file read) before starting; (4) execute the mode's procedure/gates from its body; (5) cross-service check before concluding.
- **§1-7 prose STRICTLY tech-free** — no framework/product/language/persistence/messaging/auth names (banned tokens → `spec-principles.md` §3.2); technical identifiers live ONLY in evidence carriers, frontmatter, and mermaid blocks. — why: M1/M5 require rebuild-on-any-stack from prose alone.
- **Section 8 is the canonical TC registry for business TCs** (`TC-{FEATURE}-{NNN}`) — every TC carries verifiable `[Source: namespace/service/id]` evidence (sole exception `mode=draft` → `Evidence: TBD` + provisional flag, upgraded to a real anchor on the first code-sourced run); NEVER overwrite existing TCs during `update` — `tests` owns generation, `sync` reconciles drift.
- **Honor the M1-M7 mandates** (`sdd-artifact-contract.md`) + canonical TC format (`shared/tc-format.md`) — any **M1-M5 or M7** violation FAILS the artifact (M6 binds the REVIEWER, not the artifact); `INDEX.md`/ERD are DERIVED — flag refresh need in `update`, NEVER trigger `/spec-index` here. — why: separation of concerns keeps the canonical spec the only source of truth.

> **Renamed:** formerly `/feature-spec` (and earlier `/feature-docs`); the former `/spec-tests` skill is now folded in as `mode=tests` / `mode=sync`. Those names no longer resolve as slash commands — use `/spec` with the matching mode.

### Modes (resolve mode FIRST — BLOCKING)

| Mode     | Use when…                                                                                                                                     | Body                   |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| `draft`  | Author a provisional spec from an idea/requirement/prompt — **no code yet** (TDD-first, §8 `Evidence: TBD`, provisional marker)               | `references/author.md` |
| `init`   | No `docs/specs/{Bucket}/` exists — author a full 8-section spec from source                                                                   | `references/author.md` |
| `update` | Docs exist + code changed — section-impact-mapped updates                                                                                     | `references/author.md` |
| `audit`  | `--audit` flag or user asks — staleness report per section (never mutates docs)                                                               | `references/author.md` |
| `amend`  | `[mode=amend]` from the bugfix workflow — minimal regression-scoped §3/§4/§8 touch only                                                       | `references/author.md` |
| `tests`  | Generate or update Section 8 `TC-{FEATURE}-{NNN}` test specifications                                                                         | `references/tests.md`  |
| `sync`   | Reconcile §8 TCs ↔ executing test code (forward/reverse/harvest, orphan, staleness); `harvest` captures a SPEC-SILENT invariant into §4/§5/§8 | `references/sync.md`   |

**Mode resolution (do this before any work):**

1. Parse the mode from the invocation: explicit `[mode=<x>]` arg wins; else infer from request + repo state ("from idea/requirements/prompt", "draft spec", "no code yet" → `draft`; no `docs/specs/{Bucket}/` AND code exists to source from → `init`; docs exist + diff → `update`; "audit/stale" → `audit`; bugfix caller → `amend`; "write/update test specs", "TCs" → `tests`; "sync tests", "reconcile §8 with tests" → `sync`). **`draft` vs `init`:** both author a new spec, but `draft` sources from idea/requirement text (no code → `Evidence: TBD`, provisional) while `init` sources from existing code (real `[Source:]` evidence). "No docs" alone does NOT imply `init` — check whether code exists to source from. `draft` never auto-overwrites existing §8 TCs.
2. If ambiguous, present the detected mode via `AskUserQuestion` before proceeding — NEVER auto-start a mutating mode.
3. **Read the matching `references/` body** — it is the single source of truth for that mode's procedure, gates, and output contract. Do not run a mode from memory.

**Key Rules (all modes):**

- **[BLOCKING]** Read `docs/project-reference/spec-principles.md` — repo-local prose/evidence rules (§3 prose scope + §3.2 banned prose-token list). For the AI-implementability criteria + tech-agnostic mandates, read `.claude/skills/shared/sdd-artifact-contract.md` ("AI-Implementability Gate" + mandates M1-M7) — those are the canonical authority, not the local stub.
- **[BLOCKING]** EVERY test case MUST carry verifiable code evidence as a `[Source: namespace/service/id]` abstract anchor in its Section 8 hidden carrier — physical `file:line` lives only in the provenance sidecar.
    > **Exception (`mode=draft`):** an idea-sourced spec has no code yet — its §8 TCs carry `Evidence: TBD` (reference-only) and the spec is flagged provisional (`provisional: true` frontmatter + a "DRAFT — unverified until code lands" header banner). The first `update`/`init` run against real code MUST upgrade every `TBD` to a real `[Source:]` anchor and clear the provisional flag. This mirrors existing TDD-first handling — it relaxes evidence ONLY for draft, never for code-sourced modes.
- **[BLOCKING]** Section 8 is the canonical TC registry for business TCs — §8 business TCs are the source of truth; test code implements them. The `tests` mode owns generation; `sync` mode reconciles drift; the author modes (`draft`/`init`) populate §8 at authoring time (`draft` with `Evidence: TBD`, `init` with real `[Source:]`) and MUST NOT overwrite existing TCs during UPDATE.
- Authored docs MUST match the master template's **8 tech-free sections** (Overview, Glossary, User Stories & AC, Business Rules, Domain Model, Process Flows & Interaction Surface, Permissions & Roles, Test Specifications) + YAML frontmatter — zero technical terms in prose, size caps enforced.
- **[BLOCKING] Canonical TC format authority:** `.claude/skills/shared/tc-format.md` (GWT template, Evidence carrier, decade-numbering, Preservation Tests). **M1-M7 mandates:** `.claude/skills/shared/sdd-artifact-contract.md` — any **M1-M5 or M7** violation FAILS the artifact (M6 binds the REVIEWER, not the artifact).

> `docs/project-reference/feature-spec-reference.md` — project-specific Feature Spec patterns (read directly when relevant). `docs/project-reference/domain-entities-reference.md` — domain entity catalog, relationships, cross-service sync.

### 8-Section Feature Spec Rules (canonical reference)

> Canonical home for the Feature Spec rules; applies to any edit under the Feature Spec docs root.

**Format:** Tech-free 8-section Feature Spec. Activate the `/spec` skill before editing.

**Read first:** `docs/project-reference/feature-spec-reference.md`, `docs/project-reference/spec-system-reference.md`, and `docs/project-reference/spec-principles.md`. For behavior/public-contract changes, also read `docs/project-reference/workflow-spec-test-code-cycle-reference.md`.

**8 sections (exact order):** 1. Overview · 2. Glossary · 3. User Stories & Acceptance Criteria · 4. Business Rules · 5. Domain Model · 6. Process Flows & Interaction Surface · 7. Permissions & Roles · 8. Test Specifications. No technical sections (Commands/Events/API/Cross-Service/Performance/Troubleshooting) — code is the technical source of truth.

> §6 carries a tech-agnostic interaction surface (views/nav/observable states/per-story click-paths) per the `SYNC:ui-intent-layer` block this skill carries; backend-only specs state the skip reason explicitly. This does NOT contradict "No technical sections" — the interaction surface is tech-agnostic INTENT (UX roles, information, states, flows), not a technical "UI Pages" section; M1-clean keeps it free of framework/route/CSS/component-class names.

**Mandatory:**

- §1-7 prose is STRICTLY tech-free — no framework/product/language/persistence/messaging/auth names (banned tokens → `spec-principles.md` §3.2). Technical identifiers live ONLY in evidence carriers.
- Section 5 (Domain Model): Mermaid ERD + `[Source: component/{service}/{id}]` abstract anchor per entity (cannot be omitted)
- Section 4 (Business Rules): `[Source: rule/{service}/{id}]` abstract anchor per rule group
- Section 8 (Test Specifications): canonical business TC source — TC-{FEATURE}-{NNN} IDs, each carrying a hidden `[Source: namespace/service/id]` carrier + a `CoveredBy:` field. Legacy `IntegrationTest:` fields are accepted only as migration input.

**Rules:**

- TC IDs live in Section 8 only — never authored in `docs/specs/` directly
- Section 8 authored via `/spec [mode=tests]`; `/spec [mode=init]` populates it only during initial authoring
- No line-count cap applies to Feature Specs. Split the capability only when TCs>40 or distinct module-level capabilities emerge.

### M1-M5 + M7 Compliance (BLOCKING — applies to every authored spec and every TC)

See `.claude/skills/shared/sdd-artifact-contract.md` → "AI-SDD Mandates (M1-M7)" for the full BLOCKING criteria. In brief: **M1** tech-agnostic prose; **M2** no source code in prose; **M3** logical-IDs-first traceability with a SEPARATE `[Source:]` carrier; **M4** AI-implementability (one interpretation, named success/failure); **M5** rebuild-from-scratch on any stack from §1-8 prose alone. Tech terms are allowed ONLY inside evidence carriers (`**Evidence**`, `CoveredBy`, legacy `IntegrationTest`, `[Source:]`), YAML frontmatter, and ` ```mermaid ``` ` blocks.

**M7 — Business-visibility.** Apply the demo test to the case BODY: _"what would a stakeholder SEE change?"_ — no answer → FAIL as TECHNICAL-ONLY. A `When` that is an invocation (a handler runs, a consumer receives, a job fires, data syncs) or a `Then` asserting schema/type/nullability/call-count FAILS. Judge the BODY, never the title or ID.

> **M1 governs vocabulary; M7 governs subject matter.** A technical case in impeccably tech-free prose satisfies M1 while violating M7.
>
> M6 is absent from this list by design: it binds the REVIEWER (a review that passes an M1-M5/M7 violation is itself defective), never the artifact. The artifact-facing set reads **M1-M5 and M7**.

---

## Derived-Index Delegation

This skill owns the **canonical** Feature Spec (§1-8) and its §8 TC registry. The bucket `INDEX.md` and cross-capability ERD are **derived** artifacts regenerated by `/spec-index` FROM these specs — never a source of truth, and never authored here. In `update` mode, flag "derived spec artifact refresh may be required" but do NOT trigger `/spec-index` directly (separation of concerns).

---

## Workflow Recommendation

> **MANDATORY IMPORTANT MUST ATTENTION — NO EXCEPTIONS:** If you are NOT already in a workflow, you MUST ATTENTION use `AskUserQuestion` to ask the user. Do NOT judge task complexity or decide this is "simple enough to skip" — the user decides whether to use a workflow, not you:
>
> 1. **Activate `workflow-feature` workflow** (Recommended) — spec-driven with tests by default: scout → investigate → spec-discovery → domain-analysis → why-review → spec → spec-clarify → plan → plan-review → plan-validate → why-review → spec [mode=tests] → why-review → artifact-review --type=spec-tests → plan → plan-review → feature-implement → domain-entities-review → spec [mode=tests] → why-review → artifact-review --type=spec-tests → spec [mode=sync] → integration-test → integration-test-review → integration-test-verify → workflow-review-changes → production-readiness-review → security-review → changelog → test → docs-update → workflow-end → watzup
> 2. **Execute `/spec` directly** — run this skill standalone in the resolved mode

---

## Next Steps

**[BLOCKING]** After completing, use `AskUserQuestion` to present options. Do NOT skip — user decides:

- **"/spec [mode=tests] (Recommended)"** — Generate/update Section 8 test specs for the documented features (if you just authored/updated a spec)
- **"/spec [mode=sync]"** — Reconcile Section 8 TCs ↔ executing test code
- **"/artifact-review --type=spec-tests"** — Audit TC coverage + GIVEN/WHEN/THEN quality
- **"Skip, continue manually"** — user decides

---

## Related Skills

| Skill                                | Relationship                                                                                                           | When to Call                                                                                           |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `/spec-index`                        | **Derived consumer** — assembles a regenerable navigation index/ERD FROM these Feature Specs (never a source of truth) | AFTER specs exist — (re)generate the bucket `INDEX.md` / cross-capability ERD over the canonical specs |
| `/artifact-review --type=spec-tests` | **Reviewer** — audits TC coverage in Section 8                                                                         | After `spec [mode=tests]`, to validate TC completeness and GIVEN/WHEN/THEN quality                     |
| `/integration-test`                  | **End consumer** — generates test code from TCs in Section 8                                                           | After `spec [mode=tests]`, to produce actual integration test files                                    |
| `/docs-update`                       | **Orchestrator** — calls this skill as Phase 2                                                                         | Run `/docs-update` for full chain sync; it calls `/spec` internally                                    |
| `/changes-review`                    | **Trigger** — detects feature doc staleness                                                                            | Calls `/docs-update` when a business doc is stale relative to code changes                             |

---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.

<!-- SYNC:ui-intent-layer -->

> **[BLOCKING] Capture a tech-agnostic UI/UX intent layer in every UI-bearing spec — a reader must be able to visualize how the feature works without naming any technology.** When the feature has a user interface, the spec MUST ATTENTION carry an interaction-surface section so the application — not just its API — can be rebuilt on any stack:
>
> 1. **View Inventory** — list each view/screen by its UX ROLE and purpose (e.g. "list of items", "item editor", "confirmation step") and what information it presents. Describe by role, never by an implementation name.
> 2. **Navigation Map** — how a user moves between views: entry points, transitions, and exits. Trace how this surface connects to neighboring features already in the system.
> 3. **Key observable UI States** — the distinct states a user can observe per view (empty, loading, populated, error, success, permission-denied, etc.) — described as what the user perceives, not how it is rendered.
> 4. **Per-story interaction flow** — for each user story, the step-by-step click/action path from intent to outcome, cross-referenced to the logical IDs the spec already owns (`US-`/`OP-`/`BR-`).
> 5. **Couple to the companion design artifact** — keep deep visual fidelity (layout, tokens, pixel detail) OUT of the spec; it lives in the linked `design-spec`/mockup. Record that companion's path in the spec frontmatter so the spec stays the navigable hub.
>
> **M1-clean (NON-NEGOTIABLE):** the prose names ZERO frameworks, routes/URLs, CSS, or component-class names — only roles, information, states, and flows. Technology detail belongs in the companion design artifact, never here.
>
> **Skip ONLY** when the feature is backend-only (no UI) — state that reason explicitly in the section.

<!-- /SYNC:ui-intent-layer -->

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

<!-- SYNC:evidence-based-reasoning -->

> **Evidence-Based Reasoning** — Speculation is FORBIDDEN. Every claim needs proof.
>
> 1. Cite `file:line`, grep results, or framework docs for EVERY claim
> 2. Declare confidence: >80% act freely, 60-80% verify first, <60% DO NOT recommend
> 3. Cross-service validation required for architectural changes
> 4. "I don't have enough evidence" is valid and expected output
>
> **BLOCKED until:** `- [ ]` Evidence file path (`file:line`) `- [ ]` Grep search performed `- [ ]` 3+ similar patterns found `- [ ]` Confidence level stated
>
> **Forbidden without proof:** "obviously", "I think", "should be", "probably", "this is because"
> **If incomplete →** output: `"Insufficient evidence. Verified: [...]. Not verified: [...]."`

<!-- /SYNC:evidence-based-reasoning -->

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:spec-tests-code-triangulation -->

> **Spec ↔ Tests ↔ Code Triangulation** — The unit of review is the WHOLE PACKAGE (spec + tests + code), not the diff alone. Load all three faces together and reason mutual-consistency FIRST, before any isolated per-file check.
>
> 1. **Locate all three faces** for the changed behavior: the governing Feature Spec section(s) (§3 ACs / §4 BRs / §8 TCs), the tests that guard it, and the production code. A missing face is a finding (SPEC-GAP / TEST-GAP / DEAD-SPEC).
> 2. **Triangulate pairwise** — classify which face is wrong on every disagreement:
>     - code vs spec → CODE-EXTRA / SPEC-STALE / CODE-WRONG (a [HARD] §4 rule or §5 invariant with no enforcing path is CODE-WRONG).
>     - tests vs spec → TEST-GAP / SPEC-SILENT.
>     - tests vs code → TEST-GAP / WEAK-TEST (a test that survives a deliberately broken invariant).
> 3. **Capture hidden rules** — an invariant the code enforces but the spec never states (SPEC-SILENT) is surfaced as a finding, added into §3/§4/§8, and guarded with a test: the enrichment loop, never a silent pass.
> 4. **Re-review after enrichment** — when triangulation adds spec content or a test, re-review the package against the enriched spec; converge only when a full pass surfaces no new disagreement.
>
> NEVER mark PASS while any face disagrees without a logged finding. The diff is the entry point; the package is the unit of judgment.

<!-- /SYNC:spec-tests-code-triangulation -->

<!-- SYNC:spec-drift-adjudication -->

> **Spec drift adjudication (code-wrong vs spec-stale).** Whenever changed behavior diverges from a canonical Feature Spec (business rule, acceptance criterion, flow, state transition, or §8 TC under `docs/specs/`), you MUST NOT silently pick a side. Adjudicate per `shared/sdd-artifact-contract.md` → **Drift Gates**:
>
> 1. **Detect** — compare the change against the spec's documented intent. No divergence → record `Spec in sync` and move on.
> 2. **Classify** the divergence:
>     - **CODE-WRONG** — the spec correctly states intended behavior and the change violates it → BLOCKING finding; fix the code/test against intended behavior (write/adjust a regression TC first).
>     - **SPEC-STALE** — the change is the new intended behavior and the spec now documents the old/wrong behavior → update the spec FIRST via `/spec [mode=update]`, then sync `/spec [mode=tests]` + `/spec [mode=sync]`.
>     - **AMBIGUOUS** — intended behavior is unclear → `AskUserQuestion` (or the canonical spec owner) before editing either side.
>     - **SPEC-SILENT** — the code correctly enforces an invariant/behavior that NO canonical spec artifact (§3 AC, §4 BR, §5 invariant, §8 TC) states → not drift but an UNWRITTEN rule discovered by review. ENRICH the spec via the **Invariant Harvest** pass (`/spec [mode=sync] direction=harvest` → `spec/references/sync.md`): prove it is always-true (≥2 enforcement points or a rejecting guard), express it as a universally-quantified property, then add the rule to §4 (or §3/§5) AND a §8 TC via `/spec [update]` + `/spec [mode=tests]` and add the guarding test. A discovered invariant left only in code (or only in tests) is INCOMPLETE — this is the highest-value capture (the rule nobody wrote down).
> 3. **Never normalize drift just because code/tests are green** — green can encode the drift itself. Reconcile to canonical intent, never to whichever side currently passes.
>
> A behavior-changing review/implementation that leaves a spec divergence unadjudicated is INCOMPLETE; an unwritten-but-enforced invariant left uncaptured (no §4/§8 entry) is equally INCOMPLETE.

<!-- /SYNC:spec-drift-adjudication -->

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

<!-- SYNC:evidence-based-reasoning:reminder -->

**IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim. Confidence >80% to act, <60% = do NOT recommend.

<!-- /SYNC:evidence-based-reasoning:reminder -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

<!-- SYNC:ui-intent-layer:reminder -->

- **MANDATORY** For UI-bearing specs, author/maintain the tech-agnostic interaction-surface layer (View Inventory + Navigation Map + observable UI States + per-story `US-/OP-/BR-`-traced flow); keep deep visual fidelity in the linked `design-spec`/mockup recorded in frontmatter; name ZERO frameworks/routes/CSS/component classes; skip ONLY for backend-only features with a stated reason.

<!-- /SYNC:ui-intent-layer:reminder -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

- **IMPORTANT MUST ATTENTION Goal:** Produce a tech-free, AI-implementable Feature Spec whose Section 8 TC registry stays the single source of truth, traceable to executing test code — so any team can rebuild the feature on any stack from the spec alone

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries — MUST ATTENTION honor each canonical body):**

- **Cross-Service Check:** ALWAYS scan producers, consumers, sagas, contracts before concluding; missing consumer = silent regression.
- **Evidence:** cite `file:line` for every claim; confidence >80% to act, <60% NEVER recommend.
- **Critical Thinking:** apply critical + sequential thinking; NEVER present a guess as fact.
- **Spec↔Tests↔Code Triangulation:** the unit of judgment is the WHOLE PACKAGE (spec §3/§4/§8 + tests + code) — reason mutual-consistency first; a disagreeing or missing face is a logged finding, NEVER a silent pass.
- **Spec Drift Adjudication:** on behavior divergence from a canonical spec, classify CODE-WRONG / SPEC-STALE / AMBIGUOUS / SPEC-SILENT and harvest unwritten invariants into §4/§8 + a guarding test — NEVER normalize drift to whichever side is green.
- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.

- **IMPORTANT MUST ATTENTION [BLOCKING]** Resolve the mode FIRST and read its `references/{author,tests,sync}.md` body — NEVER run `draft`/`init`/`update`/`audit`/`amend`/`tests`/`sync` from memory; ambiguous → `AskUserQuestion` before any mutating mode — why: each mode's gates + output contract live in its body, not in this entry skill
- **IMPORTANT MUST ATTENTION [BLOCKING]** EVERY test case MUST carry verifiable code evidence as a `[Source: namespace/service/id]` abstract anchor in its Section 8 hidden carrier — physical `file:line` → provenance sidecar only; sole exception `mode=draft` (`Evidence: TBD` + provisional flag, upgraded to real anchor on first code-sourced run) — why: a TC without evidence is unverifiable and silently rots
- **IMPORTANT MUST ATTENTION [BLOCKING]** Section 8 is the canonical TC registry for business TCs — existing TCs MUST NOT be overwritten during `update`; `tests` mode owns generation, `sync` mode reconciles drift — why: test code implements §8, so overwriting it orphans real tests
- **IMPORTANT MUST ATTENTION [BLOCKING]** §1-7 prose is STRICTLY tech-free — no framework/product/language/persistence/messaging/auth names (banned tokens → `spec-principles.md` §3.2); technical identifiers live ONLY in evidence carriers, frontmatter, and mermaid blocks — why: M1/M5 require rebuild-from-scratch on any stack
- **IMPORTANT MUST ATTENTION [BLOCKING]** Honor the M1-M7 mandates (`.claude/skills/shared/sdd-artifact-contract.md`) + canonical TC format (`.claude/skills/shared/tc-format.md`) — any **M1-M5 or M7** violation FAILS the artifact (M6 binds the REVIEWER, not the artifact); M7: judge the case BODY by the demo test — an invocation-shaped `When` is TECHNICAL-ONLY however tech-free its wording; no line-count cap applies, split only for TC volume or distinct capabilities
- **IMPORTANT MUST ATTENTION** `INDEX.md`/ERD are DERIVED — flag refresh need in `update`, NEVER trigger `/spec-index` here — why: separation of concerns keeps the canonical spec the only source of truth
- **IMPORTANT MUST ATTENTION** evidence gate — cite `file:line`/grep for every claim, confidence >80% to act, <60% do NOT recommend; verify AI-generated TC/source anchors against ACTUAL code (grep to confirm) before authoring — why: hallucinated `[Source:]` anchors break traceability
- **IMPORTANT MUST ATTENTION** cross-service check before concluding any spec/§8 work — scan producers, consumers, sagas, contracts; per touchpoint owner · message · risk (NONE/ADDITIVE/BREAKING) — why: a missing downstream consumer is a silent regression
- **IMPORTANT MUST ATTENTION [BLOCKING]** Break work into small `TaskCreate` tasks BEFORE starting (one per file read) + a final review task; on context loss `TaskList` first, never duplicate — why: long spec files exhaust context and lose un-tracked progress
- **IMPORTANT MUST ATTENTION** Search codebase for 3+ similar patterns and read existing spec siblings before authoring new content — match local conventions over generic defaults

**Anti-Rationalization:**

| Evasion                                          | Rebuttal                                                                                     |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------- |
| "Mode is obvious, skip the `references/` body"   | The body owns gates + output contract — running from memory drifts. Read it every time.      |
| "This TC's source is clear, skip the anchor"     | No `[Source:]` carrier (or `Evidence: TBD` for non-draft) = unverifiable TC. Add the anchor. |
| "`update` — just regenerate Section 8"           | §8 is canonical; integration tests implement it. NEVER overwrite — `sync` reconciles drift.  |
| "One tech name in prose is harmless"             | One banned token fails M1 and breaks rebuild-on-any-stack. Move it to an evidence carrier.   |
| "Small spec, skip task tracking"                 | Skip depth, NEVER skip tracking — context loss wipes un-tracked progress.                    |
| "Index looks stale, I'll just run `/spec-index`" | Not this skill's job — flag the refresh need; derived artifacts regenerate separately.       |

**[TASK-PLANNING]** MUST ATTENTION analyze task scope and break into small todo tasks/sub-tasks via TaskCreate before acting.

**IMPORTANT MUST ATTENTION** Resolve the mode FIRST + read its `references/` body · EVERY §8 TC carries a `[Source:]` evidence anchor (except `mode=draft`) · §1-7 prose STRICTLY tech-free — the three rules this skill must never skip.

---
