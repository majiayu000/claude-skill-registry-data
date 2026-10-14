---
name: spec-index
description: '[General] Use when you need to (re)generate a DERIVED navigation index, cross-capability ERD, or reimplementation guide assembled FROM the canonical Feature Specs under docs/specs/**. Never extracts a separate A-E engineering tree.'
---

> Codex compatibility note:
>
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - User-question prompts mean to ask the user directly in Codex.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, execute each listed child-skill step explicitly and report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.

<!-- CODEX:PROJECT-REFERENCE-LOADING:START -->

## Codex Project-Reference Loading (No Hooks)

Codex uses static project-reference loading instead of runtime-injected project docs.
When coding, planning, debugging, testing, or reviewing, open project docs explicitly using this routing.

**Always read:**

- `docs/project-config.json` (project-specific paths, commands, modules, and workflow/test settings)
- `docs/project-reference/docs-index-reference.md` (routes to the full `docs/project-reference/*` catalog)
- `docs/project-reference/lessons.md` (always-on guardrails and anti-patterns)

**Missing/stale context route:** If `docs/project-config.json`, the docs index, `lessons.md`, `CLAUDE.md`, `AGENTS.md`, or any task-required reference doc is missing or stale, auto-run `$project-init` or the narrow setup route (`$project-config`, `$docs-init`, `$scan-all`, `$scan --target=<key>`, `$claude-md-init`) before ordinary project-specific work. If Codex mirrors or `AGENTS.md` are missing/stale, ask the user to run `$sync-codex`; do not auto-run it.

**Situation-based docs:**

- Project structure/architecture/tech-stack/deployment/setup (any layer — backend, frontend, or infra): `project-structure-reference.md`
- Backend/CQRS/API/domain/entity changes: `backend-patterns-reference.md`, `domain-entities-reference.md`
- Frontend/UI/styling/design-system: `frontend-patterns-reference.md`, `scss-styling-guide.md`, `design-system/README.md`
- Spec authoring, `docs/specs/` pathing, or TC format: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`
- Behavior/public-contract changes or spec-test-code sync: `workflow-spec-test-code-cycle-reference.md` plus the spec docs above
- Derived spec indexes/ERDs/reimplementation guides: `spec-system-reference.md` and source Feature Specs under `docs/specs/`
- Integration test implementation/review: `integration-test-reference.md`
- E2E test implementation/review: `e2e-test-reference.md`
- Code review/audit work: `code-review-rules.md` plus domain docs above based on changed files

Do not read all docs blindly. Start from `docs-index-reference.md`, then open only relevant files for the task.

<!-- CODEX:PROJECT-REFERENCE-LOADING:END -->

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

> **Portability:** `docs/specs/` is the fixed Feature Spec root.

**Goal:** Generate, on demand, a regenerable single-writer navigation layer (catalog + cross-capability ERD + rebuild guide) **assembled FROM** the canonical tech-free 8-section Feature Specs under `docs/specs/{Bucket}/` — so a bucket can be browsed or replatformed without ever forking a second, hand-maintained source of truth. The Feature Specs are the source of truth; this skill only assembles regenerable aids over them.

**Summary:**

- **Purpose:** a DERIVED-aid assembler ONLY — reads §1 Overview, §5 Domain Model Mermaid, §8 TCs from existing Feature Specs to build `INDEX.md` (default) + optional cross-capability `{Bucket}.erd.md` + optional `{Bucket}.reimplementation-guide.md`; it NEVER authors business content. The Feature Spec stays the source of truth.
- **Main steps (run in order):** **Step 0** Scope Gate — ask the user directly (bucket + mode + artifacts), BLOCKING before any read; no `README.*.md` specs → STOP, route to `$spec`. **Step 1** Read source specs — extract capability name+link, §1 summary, §8 feature code/TC count/status, §5 Mermaid entities+relationships. **Step 2** Assemble aids — 2a `INDEX.md` catalog, 2b cross-capability ERD, 2c reimplementation guide. **Step 3** Stamp & Write — DERIVED banner + date, write each artifact immediately (never accumulate in context). **Step 4** Verify — no retired artifacts, every link resolves, banner present, prose tech-free, no canonical claims.
- **Modes:** `index` (default — regenerate derived aids) · `audit` (report which derived aids are stale vs their source specs).
- Hard prohibition is the load-bearing rule: never emit the retired A-E engineering tree, `M##` dirs, `00-module-registry.md`, `01-domain-erd.md`, `06-reimplementation-guide.md`, or `docs/specs/README.md`/`PRIORITY-INDEX.md`. Use the `{Bucket}.*` filenames instead — why: an A-E bundle becomes a second source of truth competing with the Feature Spec.
- Every generated file carries the `> DERIVED — regenerate via $spec-index; do NOT hand-edit` banner, links each row/entity back to its source spec, and keeps INDEX/ERD prose tech-free — only the reimplementation guide may name a target stack.

> **Renamed:** repurposes the former `$spec-discovery` skill (v4.0.0 derived-aid rewrite) — `$spec-discovery` no longer resolves as a slash command; use `$spec-index`.

> **[SCOPE]** This skill assembles a **DERIVED** index / ERD / reimplementation guide over the canonical Feature Specs. It MUST NOT emit a per-module A-E engineering bundle (`A-domain-model`, `B-business-rules`, `C-api-contracts`, `D-events`, `E-user-journeys`), `M##` directories, `00-module-registry.md`, `01-domain-erd.md`, or `06-reimplementation-guide.md` — those are not part of the spec model; their content lives in the Feature Spec (thin-index-only contract: output is DERIVED — never emit A-E bundle files). Authority: [`docs/project-reference/spec-system-reference.md`](../../../docs/project-reference/spec-system-reference.md).

**Inputs:** the canonical 8-section Feature Specs (§1 Overview, §5 Domain Model Mermaid, §8 TCs). Code is the technical source of truth — read it ONLY to resolve cross-spec ERD relationships or a reimplementation build order, never to populate a parallel spec layer.

**Modes:**

| Mode    | Trigger                            | Input                                           | Output                                                                    |
| ------- | ---------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------- |
| `index` | default — refresh derived aids     | Feature Specs in the target bucket(s)           | `INDEX.md` catalog (+ optional ERD / reimplementation guide), all DERIVED |
| `audit` | explicit request — staleness check | Feature Spec mtimes/git vs derived-artifact age | Stale-list report (which derived aids lag their source specs)             |

**Workflow:** `$scout` (locate specs) → `$spec-index` (assemble derived aids) → `$changes-review` → `$watzup`

**Key Rules:**

- **[BLOCKING]** Output is **DERIVED and regenerable** — every generated file carries a `> DERIVED — regenerate via $spec-index; do NOT hand-edit` banner. It is NEVER a second source of truth.
- **[BLOCKING]** MUST NOT emit `M##` dirs, `A-E` files, `00-module-registry.md`, `01-domain-erd.md`, `06-reimplementation-guide.md`, `docs/specs/README.md`, or `docs/specs/PRIORITY-INDEX.md` (all retired). See **Hard Prohibitions**.
- §1-7 of a Feature Spec are tech-free; the derived INDEX/ERD inherit that. The **reimplementation guide is the sole artifact allowed to name a target stack** (it is a rebuild guide — `spec-principles.md` §3 exception).
- Every catalog row / ERD entity links back to the source Feature Spec; mark `[UNVERIFIED]` rather than guessing.
- Read [`docs/project-reference/spec-principles.md`](../../../docs/project-reference/spec-principles.md) §3 (tech-agnostic + banned-token list) before writing any prose.

---

## App Bucket Mapping

Derived aids are organized by **App Bucket** (matches the single-home spec tree). Resolve service→bucket assignments from the canonical table in [`docs/project-reference/spec-system-reference.md`](../../../docs/project-reference/spec-system-reference.md) → **App Bucket Mapping** — do not inline project-specific bucket names in this skill.

---

## Step 0 — Scope Gate (MANDATORY FIRST)

Before reading anything, use ask the user directly. Confirm:

| Dimension      | Question                                                                                                  | Auto-Default    |
| -------------- | --------------------------------------------------------------------------------------------------------- | --------------- |
| **Bucket** ★   | Which App Bucket(s) — one bucket, several, or all of `docs/specs/`?                                       | — must confirm  |
| **Mode** ★     | `index` (regenerate derived aids) OR `audit` (report which derived aids are stale vs their source specs)? | `index`         |
| **Artifacts**  | Which derived aids: bucket `INDEX.md` / cross-capability ERD / reimplementation guide?                    | `INDEX.md` only |
| **Stack note** | (reimplementation guide only) Name a target rebuild stack, or keep stack-neutral build order?             | Stack-neutral   |

> **[BLOCKING]** If the target bucket has **no** Feature Specs matching `docs/specs/{Bucket}/README.*.md`, STOP and route the user to `$spec` — there is nothing to derive from. NEVER fabricate a spec to index.

---

## Step 1 — Read the Source Feature Specs

1. `Glob docs/specs/{Bucket}/README.*.md` → enumerate the canonical specs.
2. For each spec, read and extract ONLY:
    - **Capability name** + file link
    - **Summary** — first sentence of `## 1. Overview`
    - **Feature code** + **TC count** + status mix from `## 8. Test Specifications`
    - **Entities + relationships** from the `## 5. Domain Model` ` ```mermaid ` block (for ERD assembly)
3. Do NOT re-derive business rules, API contracts, or events into new files — those live in the Feature Spec (§1-7) and in code. You are indexing, not extracting.

> **Scale note:** For a bucket with many specs, you MAY spawn parallel reader sub-agents (one per spec) that each return the extracted fields above. This is an optimization, not a gate — there is no per-module A-E extraction to parallelize anymore.

---

## Step 2 — Assemble the Derived Aids

### 2a. Bucket `INDEX.md` (default)

Regenerate `docs/specs/{Bucket}/INDEX.md` as a feature catalog:

```markdown
> **DERIVED — regenerate via `$spec-index`; do NOT hand-edit.** Source of truth: the Feature Specs in `docs/specs/{Bucket}/README.*.md`.

# {Bucket} — Feature Index

| Capability                 | Summary             | Feature Code | TCs | Status         |
| -------------------------- | ------------------- | ------------ | --- | -------------- |
| [{Name}](README.{Name}.md) | {one-line overview} | {FC}         | {n} | {Active/Draft} |
```

> `$spec` owns the canonical Feature Specs only. `$spec-index` owns this derived `INDEX.md` and regenerates it deterministically from the specs, so there is one writer for the derived navigation file.

### 2b. Cross-Capability ERD (on request)

Assemble one Mermaid `erDiagram` from every spec's §5 block in the bucket:

- Merge entities; dedupe by name; keep cross-capability relationships.
- Resolve a relationship only present implicitly in code by reading the code — but the ERD stays tech-free (entity + relationship names only, no class/table identifiers in prose).
- Write to `docs/specs/{Bucket}/{Bucket}.erd.md` with the DERIVED banner. **Do NOT** name it `01-domain-erd.md` (retired).

### 2c. Reimplementation Guide (on explicit request only)

A build-order narrative: capability dependency order, integration touchpoints, suggested rebuild sequence.

- This is the **only** derived artifact permitted to name a target stack (rebuild-guide exception, `spec-principles.md` §3).
- Write to `docs/specs/{Bucket}/{Bucket}.reimplementation-guide.md` with the DERIVED banner. **Do NOT** name it `06-reimplementation-guide.md` (retired).

---

## Step 3 — Stamp & Write

- Every generated file opens with the `> DERIVED — regenerate via $spec-index; do NOT hand-edit` banner + a regenerate date.
- Write each file immediately after assembling it; do NOT accumulate large outputs in context.

---

## Step 4 — Verify (self-check before completing)

- [ ] **No retired artifacts emitted** — grep your own output paths: zero `M[0-9]`, zero `A-domain-model`/`B-business-rules`/`C-api-contracts`/`D-events`/`E-user-journeys`, zero `00-module-registry`/`01-domain-erd`/`06-reimplementation-guide`, zero `docs/specs/README.md`/`PRIORITY-INDEX.md`.
- [ ] **Every catalog row links to an existing Feature Spec** (no dangling links).
- [ ] **DERIVED banner present** on each generated file.
- [ ] **§1-7-derived prose is tech-free** (INDEX/ERD); only the reimplementation guide may name a stack.
- [ ] **No canonical claims** — the derived files never assert they are the source of truth.

---

## Hard Prohibitions (R1 mitigation — NON-NEGOTIABLE)

This skill produces only the DERIVED index / ERD / reimplementation guide. Emitting an A-E engineering tree would create a second source of truth competing with the Feature Spec. Therefore this skill MUST NEVER create:

| Forbidden output                                                                                          | Why                                                                |
| --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `M##` directories (e.g., `M01/`, `M02/`)                                                                  | Retired per-module partition                                       |
| `A-domain-model.md` / `B-business-rules.md` / `C-api-contracts.md` / `D-events.md` / `E-user-journeys.md` | Retired A-E engineering bundle — content lives in the Feature Spec |
| `00-module-registry.md`                                                                                   | Retired registry — bucket `INDEX.md` is the catalog                |
| `01-domain-erd.md`                                                                                        | Retired per-system ERD name — use `{Bucket}.erd.md`                |
| `06-reimplementation-guide.md`                                                                            | Retired per-system name — use `{Bucket}.reimplementation-guide.md` |
| `docs/specs/README.md`, `docs/specs/PRIORITY-INDEX.md`                                                    | Retired QA dashboards — Section 8 is the canonical TC registry     |
| `docs/business-features/**`                                                                               | Not a spec home — all specs live under `docs/specs/`               |

If a user explicitly asks for an A-E bundle, explain it is retired and offer the derived index/ERD instead. The thin-index-only contract applies — output is DERIVED, never an A-E bundle.

---

## Selective Artifact Mode

| User goal                              | Generate                                            |
| -------------------------------------- | --------------------------------------------------- |
| "Refresh the bucket index"             | `INDEX.md` only                                     |
| "I need the data model across the app" | Cross-capability ERD (`{Bucket}.erd.md`)            |
| "Produce a rebuild guide"              | Reimplementation guide (stack-neutral unless named) |
| "Full navigation set"                  | `INDEX.md` + ERD + reimplementation guide           |

---

## Next Steps

**[BLOCKING]** After completing, use ask the user directly — DO NOT skip:

- **"$docs-update (Recommended)"** — sync the Feature Specs + Section 8 if any source content was found stale during indexing
- **"$watzup"** — wrap up if index generation is the final step
- **"Skip, continue manually"** — user decides

---

## Related Skills

| Skill                | Relationship                                                                                                   | When to Call                                               |
| -------------------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `$spec`              | **Source owner** — authors the canonical 8-section Feature Spec and flags when derived refresh may be required | Before spec-index — the specs must exist to index          |
| `$spec [mode=tests]` | **Source owner** — owns Section 8 TCs that this skill counts in the catalog                                    | When TCs change and the index TC counts must refresh       |
| `$docs-update`       | **Orchestrator** — may call spec-index to refresh derived aids after a doc sync                                | After code/spec changes need a full doc sync               |
| `$changes-review`    | **Trigger** — detects spec changes and surfaces stale derived aids                                             | After spec changes; it will suggest regenerating the index |

## What Is Spec Discovery? (v4.0.0)

A **derived-index generator** over the single-home spec tree. The canonical knowledge is the tech-free 8-section Feature Spec; this skill assembles regenerable navigation aids (catalog, cross-capability ERD, rebuild guide) so readers can browse a bucket or plan a replatform without a second hand-maintained layer. It does NOT reverse-engineer code into a parallel spec bundle — that role was retired with the A-E tree.

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
> 4. **Spawn each wave in ONE message** — every `spawn_agent` call in one response, NEVER dripped per turn. Route each task to its specialist (`.claude/skills/shared/sub-agent-selection-guide.md`); NEVER `code-reviewer` as catch-all.
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

- **IMPORTANT MUST ATTENTION Goal:** Give readers a regenerable, single-writer navigation layer (catalog + cross-capability ERD + rebuild guide) assembled FROM the canonical Feature Specs — so a bucket can be browsed or replatformed without ever forking a second, hand-maintained source of truth
- **IMPORTANT MUST ATTENTION Main steps (in order):** Step 0 Scope Gate (ask the user directly bucket+mode+artifacts, BLOCKING) → Step 1 Read source specs (§1 summary, §8 code/TC count/status, §5 Mermaid) → Step 2 Assemble (2a `INDEX.md`, 2b ERD, 2c reimplementation guide) → Step 3 Stamp & Write (DERIVED banner + date, write each immediately) → Step 4 Verify (no retired artifacts, links resolve, banner present, prose tech-free) — why: AI keeps forgetting the skill owns this fixed sequence; NEVER skip or reorder without user approval

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries — MUST ATTENTION each canonical body above):**

- **Cross-Service Check:** scan producers/consumers/sagas/contracts; flag breaking-change risk.
- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.
- **Critical Thinking:** NEVER present a guess as fact; traced proof, confidence >80% to act.

- **IMPORTANT MUST ATTENTION [BLOCKING]** Output is DERIVED — never emit `M##`/A-E/`00-module-registry`/`01-domain-erd`/`06-reimplementation-guide`/QA-dashboard files (see Hard Prohibitions); use `{Bucket}.*` filenames instead — why: an A-E bundle becomes a second source of truth competing with the Feature Spec
- **IMPORTANT MUST ATTENTION [BLOCKING]** The Feature Spec (`docs/specs/{Bucket}/README.{Feature}.md`) is the source of truth — this skill assembles, never authors, business content — why: a derived aid that asserts canonical authority corrupts the single-writer contract
- **IMPORTANT MUST ATTENTION [BLOCKING]** Confirm bucket + mode + artifacts by asking the user directly BEFORE Step 1 — NEVER auto-start; if the bucket has no `README.*.md` specs, STOP and route to `$spec` instead of fabricating a spec to index
- **IMPORTANT MUST ATTENTION [BLOCKING]** Context compaction/session resume → the current task list FIRST; resume existing tasks, never re-run a completed generation pass — why: summaries describe intent, not filesystem state
- **IMPORTANT MUST ATTENTION [BLOCKING]** Stamp the DERIVED banner + regenerate date on every generated file; write after each artifact, never accumulate large outputs in context
- **IMPORTANT MUST ATTENTION [REQUIRED]** INDEX/ERD prose tech-agnostic (read `spec-principles.md` §3 banned-token list FIRST); only a reimplementation guide may name a target stack (rebuild-guide exception)
- **IMPORTANT MUST ATTENTION [REQUIRED]** Every catalog row / ERD entity links to an existing Feature Spec — grep the source path to confirm it resolves; mark `[UNVERIFIED]` rather than guessing — why: dangling links silently rot the navigation layer
- **IMPORTANT MUST ATTENTION** Read code ONLY to resolve a cross-spec ERD relationship or a reimplementation build order — never to populate a parallel spec layer — why: code is the technical source of truth, not a spec substitute
- **IMPORTANT MUST ATTENTION** Cite `file:line` evidence for every extracted field and link (confidence >80% to act, <60% mark `[UNVERIFIED]`) — NEVER fabricate a capability name, feature code, or TC count; grep the source spec to confirm
- **IMPORTANT MUST ATTENTION** Before authoring any new derived format, grep 3+ existing `INDEX.md`/`*.erd.md` siblings and match their structure — verify the new bucket shares the same spec layout before copying a nearby pattern
- **IMPORTANT MUST ATTENTION** Break task scope into small task tracking todos (one per artifact) before acting; mark each `completed` immediately after its file is written; keep exactly one `in_progress`
- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.

**Anti-Rationalization:**

| Evasion                                               | Rebuttal                                                                                                             |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| "User wants full detail — regenerate the A-E bundle"  | A-E is not part of the spec model. Offer the derived index/ERD; the detail already lives in the Feature Spec + code. |
| "I'll write the ERD as `01-domain-erd.md`"            | Wrong filename. Use `{Bucket}.erd.md` with the DERIVED banner.                                                       |
| "The index can be the source of truth, it's complete" | NEVER — it is derived/regenerable. §1-7 + §8 of the Feature Spec are canonical.                                      |
| "No specs in this bucket, I'll extract from code"     | STOP. Route to `$spec`. This skill indexes existing specs; it does not author new ones.                              |
| "Scope is obvious, skip Step 0 ask the user directly" | BLOCKING — NEVER auto-start. Bucket, mode, and artifact set MUST be confirmed first.                                 |
| "I'll just trust the spec link, no need to verify"    | Grep the source path. A dangling link makes the derived navigation layer worse than none.                            |
| "TC count looks about right, skip re-reading §8"      | NEVER guess counts. Re-read `## 8. Test Specifications`; mark `[UNVERIFIED]` if unresolved.                          |

**[TASK-PLANNING]** MUST ATTENTION analyze task scope and break into small todo tasks/sub-tasks via task tracking before acting.

> **[IMPORTANT]** Break into many small todo tasks systematically before starting — this is critical.

**IMPORTANT MUST ATTENTION** Output is DERIVED + regenerable — never a second source of truth; the Feature Spec is canonical.
**IMPORTANT MUST ATTENTION** Confirm bucket + mode + artifacts by asking the user directly BEFORE any read; no specs → STOP, route to `$spec`.
**IMPORTANT MUST ATTENTION** Cite `file:line` for every extracted field; mark `[UNVERIFIED]` rather than guessing; never emit retired A-E/`M##`/QA-dashboard files.

---

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:START -->

## Hookless Prompt Protocol Mirror (Auto-Synced)

Source: `.claude/.ck.json` + `.claude/skills/shared/sync-inline-versions.md` (`:full` blocks) + `.claude/scripts/lib/hookless-prompt-protocol.cjs`

## [WORKFLOW-EXECUTION-PROTOCOL] [BLOCKING] Workflow Execution Protocol — MANDATORY IMPORTANT MUST CRITICAL. Do not skip for any reason.

**Generic portability boundary:** Reusable skills and protocol text stay project-neutral; project-specific conventions are discovered from docs/project-config.json and docs/project-reference/. Apply shared AI-SDD from `shared/sdd-artifact-contract.md`. Read `docs/project-config.json` and `docs/project-reference/docs-index-reference.md`, then open the project reference docs named there. For spec, test-case, behavior-change, public-contract, or `docs/specs/` work, route through the local spec docs named by the docs index: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`, and `workflow-spec-test-code-cycle-reference.md` when specs/tests/code must stay synchronized. If either file or a required reference doc is missing or stale, auto-run `$project-init` (or the narrow lower-level route such as `$project-config`, `$docs-init`, `$scan-all`, or `$scan --target=<key>`) before ordinary project-specific work. Any supported AI tool may execute when this shared context and local docs are available.

1. **DETECT:** If the prompt starts with an explicit slash skill/workflow command, execute it directly. Otherwise match the prompt against the workflow catalog and skill list.
2. **ANALYZE:** Choose the best option: execute directly, invoke a skill, activate a standard workflow, or compose a custom step combination.
3. **AUTO-SELECT:** Pick the best option yourself. Do not ask the user to choose between direct execution, skill, standard workflow, or custom workflow.
4. **ACTIVATE:** For a selected workflow, call `$start-workflow <workflowId>`; for a selected skill, invoke that skill; for a custom workflow, sequence custom steps directly; for direct execution, proceed with the task.
5. **CREATE TASKS:** task tracking for ALL workflow/skill/custom steps before execution when the selected path has multiple steps.
6. **PARALLELIZE:** Before executing the task list, tag each task `PAR` (independent inputs + write set disjoint from every other `PAR` task) or `SEQ` (name the blocking dependency), group `PAR` tasks into waves, declare the wave plan, and spawn each wave's sub-agents in ONE message — all-return barrier per wave, fan-out one level deep unless a sub-agent's own definition authorizes further fan-out. Sequential-by-default is a defect when tasks are independent; do not parallelize shared write targets, output-consuming tasks, trivial single-file work, ordering a skill or workflow explicitly fixes, or user-approval gates.
7. **EXECUTE:** Advance per the **Workflow Step Advancement & Parallel Phases** rule in your context instructions — model-driven; a sub-agent completion advances a step identically to an inline call; a parallel-phase group is an all-return barrier (advance only after ALL members return, never serialize it)

## Shared AI-SDD Protocol Markers

Source: `.claude/skills/shared/sync-inline-versions.md`

## SYNC:ai-sdd-artifact-contract

> **AI-SDD Artifact Contract** — Shared spec-driven development rules stay portable and source-owned.
>
> 1. Keep reusable AI-SDD principles in `.claude`; put repository-specific paths, commands, owners, products, and formats in project config/reference docs.
> 2. Preserve cycle: `spec -> plan -> tasks -> implement -> verify -> update spec/docs`.
> 3. Trace every requirement or invariant through decision, task, TC/test, source evidence, and docs/spec update.
> 4. Treat code-to-spec extraction as reference-only until accepted by the canonical spec owner.
> 5. Any supported AI tool may plan, implement, review, or verify with synced context; using multiple tools is optional.
> 6. Update `.claude` source first, then sync generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`. — why: mirrors are generated artifacts; hand-edits are overwritten on the next sync
> 7. If `docs/project-config.json`, root instruction files, or a required project-reference doc is missing or stale, auto-run `$project-init` or the narrow lower-level route before ordinary project-specific work.
>
> **Active reference:** `shared/sdd-artifact-contract.md` in the active skills root.

---

## SYNC:ai-sdd-artifact-contract:reminder

- **MANDATORY** Apply `shared/sdd-artifact-contract.md`; keep reusable AI-SDD in `.claude` and local rules in project docs.
- **MANDATORY** Code-to-spec extraction is reference-only until canonical acceptance; any supported AI tool may execute with synced context.
- **MANDATORY** Update `.claude` source before syncing generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`.
- **MANDATORY** Missing or stale project config, root instruction files, or required reference docs route project-specific work through `$project-init` or the narrow setup route automatically.
  **[TASK-PLANNING] [MANDATORY]** BEFORE executing any workflow or skill step, create/update task tracking for all planned steps, then keep it synchronized as each step starts/completes.

## [LESSON-LEARNED-REMINDER] [BLOCKING] Task Planning & Continuous Improvement — MANDATORY. Do not skip.

Break work into small tasks (task tracking) before starting. Add final task: "Analyze AI mistakes & lessons learned".

**Extract lessons — ROOT CAUSE ONLY, not symptom fixes:**

1. Name the FAILURE MODE (reasoning/assumption failure), not symptom — "assumed API existed without reading source" not "used wrong enum value".
2. Generality test: does this failure mode apply to ≥3 contexts/codebases? If not, abstract one level up.
3. Write as a universal rule — strip project-specific names/paths/classes. Useful on any codebase.
4. Consolidate: multiple mistakes sharing one failure mode → ONE lesson.
5. **Recurrence gate:** "Would this recur in future session WITHOUT this reminder?" — No → skip `$learn`.
6. **Auto-fix gate:** "Could `$code-review`/`$code-simplifier`/`$security-review`/`$lint` catch this?" — Yes → improve review skill instead.
7. BOTH gates pass → ask user to run `$learn`.
   **[CRITICAL-THINKING-MINDSET]** Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
   **Anti-hallucination principle:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.
   **AI Attention principle (Primacy-Recency):** Put the 3 most critical rules at both top and bottom of long prompts/protocols so instruction adherence survives long context windows.
   **Goal-driven execution:** Define success criteria first, loop until verified, and stop only when observable checks pass.
   **Tests verify intent:** Tests must protect business rules/invariants and fail when the protected intent breaks, not only mirror current behavior.

## Common AI Mistake Prevention (System Lessons)

- **Re-read files after context compaction.** Edit requires prior Read in same context; compaction wipes read state. Re-read before editing.
- **Grep for old terms after bulk replacements.** AI over-trusts find/replace completeness. Grep full repo after bulk edits for missed refs in docs/configs/catalogs.
- **Check downstream references before deleting.** Deletions cascade doc/code staleness. Map referencing files before removal.
- **After memory loss, check existing state before creating new.** Compaction wipes prior-work memory. Query current state to resume — never blindly duplicate.
- **Verify AI-generated content against actual code.** AI hallucinates APIs, class names, method signatures. Grep to confirm existence before documenting/referencing.
- **Trace full dependency chain after edits.** Changing a definition misses downstream consumers. Trace the full chain.
- **When renaming, grep ALL consumer file types.** Some file types silently ignore missing refs (no compile error). Search code, templates, configs, generated files.
- **Trace ALL code paths when verifying correctness.** Code existing ≠ code executing. Trace early exits, error branches, conditional skips — not just happy path.
- **Update docs that embed canonical data when source changes.** Docs inlining derived data (workflows, schemas, configs) go stale silently. Update all embedding docs alongside source.
- **Verify sub-agent results after context recovery.** Background agents may finish while parent compacted — grep-verify output, don't trust assumed completion.
- **Cross-check full target list against sub-agent assignments.** Parallel sub-agents by category miss boundary items. Reconcile union of assignments against target list before proceeding.
- **Sub-agents inherit knowledge only from their agent .md definition — use custom agent types, not built-in Explore.** Tool adoption = permission + knowledge + enforcement (numbered workflow step).
- **Persist sub-agent findings incrementally, not as a final batch.** Long sub-agents hit cutoffs before final write — findings lost. Instruct append-per-section to report file.
- **When debugging, ask "whose responsibility?" before fixing.** Trace caller (wrong data) vs callee (wrong handling). Fix at responsible layer — never patch symptom site.
- **Test failure → record a provisional verdict before trace/edit, then investigate.** Use the full five-way taxonomy: SOURCE-WRONG (production violates intent), TEST-WRONG (assertion/setup is stale), TEST-NOT-OPTIMAL (valid but fragile or low-signal test), ENVIRONMENT-BLOCKED (external state prevents a verdict), or AMBIGUOUS (intent/evidence cannot choose safely). Then trace root cause and triangulate against the governing spec (`docs/specs/**` if one exists) AND source. NEVER weaken an assertion, add a skip, relax a timeout, or change source merely to force green.
- **Grep ALL removed names after extraction/refactoring.** Primary file "done" ≠ secondary files clean. Grep entire scope for every removed symbol before declaring complete.
- **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Pattern-matching as "wrong" skips context. Before changing or reporting any constant/limit/flag/cutoff: read comments, git blame, the CALLER's ordering (the guarantee that makes the value correct usually lives in code running immediately BEFORE the cited line), and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard — and in a validation pass, an accurate `file:line` citation proves the transcription, never the defect.
- **Verify ALL affected outputs, not just the first.** One build green ≠ all green. Multi-stack changes (backend/frontend/tests/docs) require verifying EVERY output.
- **Evaluate fit before copying a nearby pattern.** Closest example ≠ matching preconditions — verify the new context shares the same constraints, base classes, scope, lifetime.
- **Holistic-first debugging — resist nearest-attention trap.** Don't dive into first plausible cause. List EVERY precondition (config, env vars, paths, DB, endpoints, creds, versions, DI, data). Verify each against evidence (grep/query — not reasoning). Ask "what would falsify this?" — if nothing, it's not a hypothesis. Most expensive failure: going deeper in "obvious" layer while bug sits in layer never questioned.
- **Surgical changes — apply the diff test (context-aware).** Two modes: (1) Bug fix → every line traces to the bug; no restyling; orphan cleanup only for imports YOUR changes made unused. (2) Review/enhancement → implement improvements AND announce as "Enhancement beyond main request: [what]". Never silently scope-creep. Diff test: "Would this line exist if I wasn't asked to do X?" — if no, delete or announce.
- **Surface ambiguity before coding — don't pick silently.** Multiple valid interpretations → present each with effort: "[Request] could mean (1) [N h], (2) [N h]. Which matters?" List scope/format/volume/constraints assumptions first. If simpler path exists, say so. Never silently pick.
- **[MANDATORY FIRST ACTION] ALWAYS activate a suitable skill or workflow BEFORE responding.** Match task against workflow catalog + skill list; invoke via skill invocation or `$start-workflow <workflowId>`. NEVER answer or write code before checking. Skip = protocol violation.
- **Why-Review adversarial mindset — apply when reviewing any plan, decision, or design.** Default SKEPTIC not VALIDATOR: steel-man a rejected alternative, invert each stated reason ("what does it sacrifice?"), stress-test top 2-3 assumptions, run pre-mortem ("ships, fails in 3 months — what breaks?"), surface 1-2 alternatives author missed. Section presence ≠ quality; quality = causal reasoning + concrete mitigations + evidence, not "it's better" or "monitor closely".
- **Front-load report-write in sub-agent prompts for large reviews.** Many-file sub-agents hit budget before final write — findings lost. Design prompts so: (1) report-write is first explicit deliverable, (2) append per-file/section (not batched), (3) scope bounded so reads don't exhaust budget. Truncated mid-sentence with no report file → spawn narrower scope, don't retry same prompt.
- **After context compaction, re-verify all prior phase outcomes before continuing.** Summaries describe intent, not environment state (git index, filesystem, processes). On resume, FIRST audit: git status, re-read modified files, verify filesystem. Every "completed" claim is an untested hypothesis until evidence confirms.
- **OOM/memory: check row count before row size.** Triage: (1) Unbounded query — no DB filter for trigger? Push filter to DB; eliminates OOM. (2) Large rows? Projection reduces proportionally. Row reduction > projection in ROI.
- **Assert the outcome your system OWNS, never the intermediate state your INFRASTRUCTURE owns.** When testing anything asynchronous (queue/broker delivery, retries, background jobs, caches, replication), assert the final business/entity state. NEVER assert the delivery bookkeeping — consume/send status, attempt counts, last-error, row existence or counts in a broker, scheduler, or outbox/inbox table. That bookkeeping lives in shared infrastructure that ANY co-running process (a peer worker, a second replica, a leftover local container) can write, usually under a deterministic shared key, so the assertion silently tests the developer's environment instead of the system: green when run alone, flaky the instant anything else shares that broker + database. Gate question for every assertion: "would this hold no matter WHICH process did the work?" — if no, assert the converged data state instead. Corollary: process-local fault injection and in-process telemetry cannot gate work any process may perform — use them as stress amplifiers (arm → bounded window → disarm → assert convergence), never as preconditions.
- **Keep domain concepts out of generic/shared/infrastructure layers.** Reusable layer (shared library, framework, infra module) must reference NO consumer-specific domain concept — tenant/customer/product IDs, business entities, feature rules. Leak compiles + runs → passes review silently while coupling the "reusable" layer to one consumer. Keep shared type domain-free; push domain fields/logic down into the consumer via subclass/composition. — why: a layer coupled to one consumer's domain is no longer reusable.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:END -->
