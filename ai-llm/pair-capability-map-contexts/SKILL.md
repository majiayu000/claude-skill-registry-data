---
name: pair-capability-map-contexts
description: "Maps subdomains to DDD bounded contexts and derives the integration pattern between them (integration strength, socio-technical distance, volatility), scoped to items just touched. Composed by /pair-process-refine-story, /pair-process-plan-tasks, /pair-process-brainstorm; full-scope re-mapping only via /pair-process-bootstrap."
version: 0.6.0
author: Foomakers
---

# /pair-capability-map-contexts — Bounded Context Placement (Capability)

Map subdomains to bounded context boundaries and assess each relationship between contexts on three dimensions — integration strength, socio-technical distance, volatility — to derive the integration pattern. A **capability**, not a standalone lifecycle step: always invoked scoped to the contexts/services the caller just touched, never as a full re-mapping outside `/pair-process-bootstrap`.

## Process Profile

<!-- process-step: id=define-bounded-contexts -->

Executable form of the **`define-bounded-contexts`** step. A **direct** invocation while a step is disabled by the project's profile warns and asks for confirmation; under `$approval: auto` there is nobody to answer, so the run **HALTs**. <!-- approval-round: kind=gate; auto=halt -->

A **composed** invocation never prompts — it degrades exactly as a step that is not installed. No section ⇒ no-op. See [process-profile gate](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/process-profile-gate.md).

## Arguments

| Argument | Required | Description                                                                                                                                 |
| -------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `$scope` | Yes      | Contexts/services touched by the caller (e.g. a context name, a service, the contexts implicated by a task). `all` — full re-mapping, allowed only when composed by `/pair-process-bootstrap`. |
| `$approval` | No    | Approval-round mode: `interactive` (default — the Step 4 round runs as written) or `auto` (ask nothing: the proposed delta is accepted as-is, a **conflict** keeps the existing entry, both reported). **`auto` does not lift the Step 3 gate** — an unbalanced + volatile relationship with neither mitigation nor acceptance still HALTs. See [approval rounds](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/approval-rounds.md). |

## Composed Skills

| Caller          | When                                                                       |
| ---------------- | --------------------------------------------------------------------------- |
| `/pair-process-refine-story`  | Technical analysis phase — identifies touched contexts/services.          |
| `/pair-process-plan-tasks`    | Identifies touched contexts/services for the task breakdown.              |
| `/pair-process-brainstorm`    | Punctual/technical discovery (phase 2) touching one or a few contexts. |
| `/pair-process-bootstrap`     | Initial full-catalog mapping — the only caller allowed `$scope: all`.     |

Invocable independently with an explicit `$scope` for ad hoc placement.

## Algorithm

### Step 0: Resolve Scope and DDD Adoption State

1. **Check**: Does [`adoption/tech/boundedcontext/`](../../../.pair/adoption/tech/boundedcontext) contain `.md` files beyond README.md (DDD already adopted)?
2. **Check**: If not adopted, are subdomains defined ([`adoption/product/subdomain/`](../../../.pair/adoption/product/subdomain) has `.md` files beyond README.md)?
3. **Act**: Resolve the working mode:
   - **DDD mode** — bounded context catalog exists, or a subdomain catalog is available to map from.
   - **System-areas fallback** — no context catalog AND no subdomain catalog. No DDD prerequisite is enforced; do not HALT. Proceed to Step 1 in fallback mode, treating existing services/modules as the context boundary.
4. **Check**: Does `$scope` resolve to any context/service in the current codebase or catalog?
5. **Skip**: If `$scope` resolves to nothing → report "no domain impact" and return control to the caller. No file changes.
6. **Verify**: Mode and non-empty scope determined. When in DDD mode, also load (best-effort, warn if missing): [architecture.md](../../../.pair/adoption/tech/architecture.md), [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md), [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md).

### Step 1: Detect Existing Bounded Contexts

1. **Check**: Scan [`adoption/tech/boundedcontext/`](../../../.pair/adoption/tech/boundedcontext) for existing `.md` files (excluding README.md).
2. **Act**: Build a registry of existing contexts:

   ```text
   EXISTING CONTEXTS:
   ├── [filename.md]: [Title] (Type: [Core/Supporting/Infrastructure])
   └── ...
   ```

3. **Verify**: Registry built. Only entries touched by `$scope` are candidates for creation/update.

### Step 2: Context Boundary Analysis (DDD mode)

_Skip if in system-areas fallback — go to Step 2b._

1. **Act**: Synthesize context boundaries for the in-scope items from multiple inputs:
   - **Subdomains**: group related in-scope subdomains based on business cohesion, and read their `Volatility` rating.
   - **Architecture**: service decomposition patterns, consistency requirements.
   - **Tech stack**: database choices, communication protocols.
   - **Way of working**: team structure, ownership model.
2. **Act**: For each in-scope context, determine Type — Core (high autonomy), Supporting (medium autonomy), Infrastructure (shared services) — and subdomain grouping rationale.
3. **Verify**: In-scope context boundaries identified.

### Step 2b: System-Areas Fallback (no-DDD projects)

1. **Act**: Treat each existing service/module touched by `$scope` as a provisional context boundary — Type inferred from its role (an entry point/API service reads as Core or Supporting; a shared library reads as Infrastructure).
2. **Act**: Relationship assessment (Step 3) still applies between system areas — the three dimensions do not require a DDD catalog to be meaningful.
3. **Verify**: Placement resolved to system area(s). Note in output that this is a fallback, not a DDD classification.

### Step 3: Relationship Assessment (3 Dimensions)

For each relationship between an in-scope context and another context it touches:

1. **Act**: Assess **integration strength** — how tightly coupled the two contexts are at the code/data level:
   - `intrusive` — shared database/schema or direct internal access.
   - `functional` — synchronous call dependency (must respond to operate).
   - `model` — shared domain model/types without a formal contract.
   - `contract` — explicit interface (API/event schema) between independently deployable contexts.
2. **Act**: Assess **socio-technical distance** — team/organizational distance between the owning teams (same team = low; different team, same org = medium; different org/vendor = high).
3. **Act**: Assess **volatility** — read from the subdomain(s) underlying each side of the relationship (`Volatility` field from [subdomain-template.md](../../../.pair/knowledge/guidelines/collaboration/templates/subdomain-template.md)); for generic subdomains, factor in the recorded implementation volatility.
4. **Act**: Derive the **balanced/unbalanced outcome**:
   - High socio-technical distance ⇒ pattern should be `contract` (or an anti-corruption layer). If the current/proposed strength is `intrusive`/`functional`/`model` despite high distance → **unbalanced**.
   - High integration strength with low distance ⇒ co-location in the same context is appropriate; keeping them as separate contexts despite high strength → **unbalanced**.
   - Otherwise → **balanced**.
5. **Act**: Annotate contract-coupled relationships (`contract` strength) as **"contract tests expected"** — downstream story validation strategies touching this relationship inherit the contract/boundary test categories (coupling-balance guideline, see Notes).
6. **Check**: Is the relationship **unbalanced AND volatile** (either side rated `Volatility: High`)?
7. **Act**: If unbalanced + volatile → **gate at approval**: proceed only once one of the following is recorded:
   - A mitigation (e.g. introduce an ACL, renegotiate the pattern toward `contract`), or
   - An explicit developer acceptance of the risk (recorded in the context file).

   **This gate is not an approval round and `$approval: auto` does not lift it** — it is the judgement kind ([approval rounds](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/approval-rounds.md)): with neither a mitigation nor an acceptance on the table there is no proposal to auto-accept, and Step 5 would write a domain model recording a coupling risk nobody judged. So it **HALTs under every value of `$approval`**, and it is the one place a non-interactive run of this skill can still stop for a human. <!-- approval-round: kind=gate; auto=halt -->
8. **Verify**: Every in-scope relationship has strength, distance, volatility, outcome, and (if gated) a mitigation/acceptance recorded.

### Step 4: Context Catalog Delta Proposal

1. **Check**: Does an in-scope context already exist in the registry with a different Type/relationship set (catalog conflict)?
2. **Act**: If a conflict exists → propose the delta only (not a full re-map). Under `$approval: auto` a conflicting delta is **not applied**: the existing entry is kept and the delta is reported unapplied, since overwriting a recorded placement nobody was asked about is the one outcome `auto` must not produce.
3. **Act**: Present the scoped catalog delta to the developer (`$approval: interactive`; under `auto` it is reported in the Output Format instead of asked):

   > Proposed bounded context placement (scope: [$scope]):
   > **[Type]**: [Name] — subdomains: [list]
   >
   > Relationships:
   > - [Context A] ↔ [Context B]: strength=[intrusive/functional/model/contract], distance=[low/medium/high], volatility=[from subdomains], outcome=[balanced/unbalanced]
   >   [if gated] ⚠ unbalanced + volatile — mitigation: [...] or accepted: [...]
   >
   > Approve or adjust? <!-- approval-round: kind=confirm; auto=accept -->

4. **Verify** (`$approval: interactive`): Developer approves the delta, including any gated relationships' resolution. Under `auto` the delta is accepted as-is (already reported in item 3) — but a **gated** relationship is never auto-resolved: Step 3 item 7 has already HALTed unless a mitigation or an acceptance was recorded. <!-- approval-round: kind=confirm; auto=accept -->

### Step 5: Context Specification

For each approved context in scope:

1. **Check**: Does this context already exist as a file?
2. **Act**: If exists and no conflict was raised → leave untouched; pre-existing relationships without the 3-dimension assessment remain valid as-is (no forced migration — assessed the next time that relationship falls inside a `$scope`).
3. **Act**: If new, or an approved delta applies → create/update the context file following [bounded-context-template.md](../../../.pair/knowledge/guidelines/collaboration/templates/bounded-context-template.md) (resolve override-first — [template resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/template-resolution.md)):
   - Fill all template sections: Type, Subdomains Covered, Business Scope, Relationships (with the 3-dimension assessment per relationship), Integration Patterns, Data Ownership, Team Alignment, Ubiquitous Language, Quality Attributes, Encapsulated Knowledge, Change Vectors.
   - File path: `adoption/tech/boundedcontext/[kebab-case-name].md`
4. **Verify**: File created/updated and parseable. Entries outside `$scope` are untouched.

### Step 6: Update Catalog README

1. **Act**: Update [`adoption/tech/boundedcontext/README.md`](../../../.pair/adoption/tech/boundedcontext/README.md) for the entries touched by this run:
   - List all contexts with subdomain mappings.
   - Include integration overview, flagging gated (unbalanced + volatile) relationships.
   - Link to individual context files.
2. **Verify**: README reflects the current catalog.

## Output Format

```text
CONTEXT PLACEMENT COMPLETE:
├── Scope:        [$scope]
├── Mode:         [DDD | System-areas fallback]
├── Touched:      [N contexts]
├── Created:      [X new files]
├── Updated:      [Y existing files]
├── Relationships: [balanced: A, unbalanced: B, gated: C]
├── Approval:     [interactive — approved | auto — accepted as-is, D conflict(s) kept unapplied]
├── Location:     adoption/tech/boundedcontext/
└── Next:         /plan-epics (scoped) or back to the calling process skill
```

The `Next:` line names only steps enabled by the project's [process profile](../../../.pair/knowledge/guidelines/technical-standards/ai-development/process-profiles.md): a disabled one is dropped, and when none is left the line names no skill.

## Edge Cases and Error Handling

- **Scope resolves to nothing** — report "no domain impact", caller proceeds without HALT.
- **Existing catalog conflicts with scoped update** — always propose the delta and require human approval before writing (idempotent behavior preserved). Under `$approval: auto` the write does not happen either: the existing entry is kept and the delta is reported unapplied (Step 4 item 2). <!-- approval-round: kind=keep-or-redo; auto=keep -->
- **Pre-existing relationships without the 3-dimension assessment** — treated as valid; assessed only when that relationship falls inside a future `$scope`.
- **No `subdomain/` or `boundedcontext/` artifacts at all** — system-areas fallback (Step 2b); no error, no DDD prerequisite.
- **Unbalanced + volatile relationship, no mitigation/acceptance offered** — HALT at **Step 3 item 7**, where the gate is raised (before Step 4's delta round, which never sees the relationship). This is the one case where the capability blocks, **under every value of `$approval`**: a judgement gate is not suppressible by a non-interactive signal.
- **`$scope: all` requested by a caller other than `/pair-process-bootstrap`** — warn and downgrade to the caller's actual touched items; full re-mapping stays bootstrap-only.

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) (adoption files missing → warn, proceed with what's available rather than halting) for the standard scenarios. Additional cases:

- If architecture or tech-stack adoption files are missing, warn and infer boundaries from subdomains alone.
- If subdomains have no `Volatility` field yet, treat volatility as unknown/Medium for the assessment and note it as provisional.
- If neither a subdomain nor a bounded-context catalog exists, use the system-areas fallback (Step 2b) rather than halting.
- If the adoption directory doesn't exist, create it.
- If README.md doesn't exist, create it from scratch.

## Notes

- This skill **creates/updates adoption files** — not PM tool issues. Bounded contexts are design artifacts.
- **Idempotent** — see [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md). This skill's check: detects existing files by filename; only entries inside `$scope` are evaluated for changes.
- The 3-dimension relationship assessment (strength, distance, volatility) is the input to the coupling-balance guideline — see `.pair/knowledge/guidelines/architecture/design-patterns/coupling-balance.md` (introduced by #209); until that guideline lands, apply the heuristics in Step 3 directly.
- Contract-coupled (`contract` strength) relationships are annotated "contract tests expected" — `/pair-capability-design-manual-tests` and story-level validation strategies should pick up the contract/boundary test category for that relationship.
- Migration: this skill was reclassified from a process skill (`process/map-contexts`) to a capability (`capability/map-contexts`) — see [skills-guide.md](../../../.pair/knowledge/skills-guide.md#migration-notes) for the rename and new invocation paths.
