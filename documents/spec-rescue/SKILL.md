---
name: spec-rescue
description: Rescue or rebuild a corrupted, contradictory, or drifted specification using a structured workflow instead of prose-first rewriting. Use whenever a spec has conflicting sections, hidden duplicates, ambiguous authority, smeared process/design content, repeated failed rewrite attempts, or the user wants to consolidate decisions before writing final prose. Strongly use this when the user wants to inventory a spec, preserve approved wording, build a schema/ledger source of truth, detect duplicate/overlap/conflict by intent, or generate final spec text only after decisions are stabilized.
---

# Spec Rescue

This skill exists for situations where raw Markdown spec writing has become unreliable.

Use it when:

- the spec has been rewritten multiple times and trust is gone;
- approved decisions exist, but are scattered through chat, handoffs, and draft prose;
- the same design idea appears in multiple sections with different wording;
- process guidance, design rules, implementation notes, and sign-off claims are mixed together;
- the user wants a spec rebuilt from known decisions rather than repaired by paragraph editing;
- you need a workflow that is traceable, reversible, and less vulnerable to LLM drift.

The core idea is simple:

- **do not treat long-form Markdown as the primary source of truth**
- **capture decisions atomically first**
- **inventory existing prose separately**
- **reconcile duplicates/conflicts before writing final spec prose**

## Workflow Source

This skill is a summary layer, not the authority on the workflow by itself.

The operational workflow for this process lives at:

- `docs/specs/spec-workflow.md`

If there is any tension between this skill and the workflow file, follow the workflow file.

`docs/specs/spec-session-status.md` is the current-state artifact. Do not treat it as the source of workflow rules.

The core workflow artifacts this skill expects are:

- `docs/specs/spec-chunk.md`
- `docs/specs/spec-inventory.md`
- `docs/specs/spec-ledger.yaml`
- `docs/specs/spec-conflicts.yaml`
- `docs/specs/spec-evidence.md` or `docs/specs/spec-evidence.yaml`
- `docs/specs/spec-session-status.md`

At session start, do not infer the workflow state from prose alone.

Read in this order:

1. `AGENTS.md`
2. `docs/specs/spec-workflow.md`
3. `docs/specs/spec-session-status.md`
4. use CORE exactly as CORE requires for this workflow
5. `docs/specs/spec-chunk.md`
6. `docs/specs/spec-inventory.md`

Then take:

- current phase from `docs/specs/spec-session-status.md`
- workflow rules from `docs/specs/spec-workflow.md`
- protected decision record from `docs/specs/spec-chunk.md`
- inventory-only snapshot from `docs/specs/spec-inventory.md`

Do not guess the phase. Do not substitute another memory source for CORE.

For this workflow, the CORE protocol is exact:

### RULE: APPROVAL REQUIRED BEFORE ANY WRITE TO CORE

Before calling ANY tool that writes data into or through CORE, you MUST
present what you intend to do and get explicit approval.

Tools that require approval before use:
- `memory_ingest` - show the full ingestion text first
- `add_reminder` - show the reminder text and schedule first
- `update_reminder` - show what will change first
- `execute_integration_action` - show the action and parameters first

Present the exact content, not a summary of it. Max must see the actual text
that will be stored. Then wait for approval before calling the tool.

This is not optional. A single incorrect write to CORE can propagate bad data
into every future session.

### RULE: ALL DATA MUST HAVE COMPLETE ENTITY CONNECTIONS

Every piece of data that enters CORE must contain everything CORE needs to
build correct graph connections. CORE extracts entities by name from the text
it receives. If a name is missing, abbreviated, or vague, the entity either
doesn't get created or doesn't connect to existing entities in the graph.

For every write to CORE:
- Repos: Owner and name - "Maxcogar/syndicatecnc-weekly-web-brief", never
  "the repo" or "the project"
- Files: Full paths from repo root - "src/api/handlers/auth.ts", never
  "the auth file" or "that handler"
- Packages/Dependencies: Full name and version when relevant -
  "python-fastmcp 2.0", never "the MCP library"
- APIs/Services: Proper name and endpoint when relevant -
  "ERPNext REST API /api/resource/Sales Order", never "the ERP endpoint"
- MCP Servers: Full name - "Engineering Design Navigator MCP server", never
  "the MCP server" or "the navigator"
- Infrastructure: Named - "Google Cloud Run", "Firebase Hosting",
  "HP t740 Docker host", never "the server" or "the cloud"
- Skills/Configs: With identifiers - "integration-builder skill at
  /mnt/skills/user/integration-builder/SKILL.md", never "that skill"
- People: Full name - "Max Cogar", never just "Max" or "the user"
- Organizations: Proper name - "CNC Syndicate", "Anthropic", never
  "the company"

Never use: "the repo", "the project", "the file", "that function", "the bug",
"the thing we fixed"

### START OF EVERY SESSION

**Step 1:** Call `initialize_conversation_session` (`new: true`). Store the
`sessionId` for the entire session.

**Step 2:** Identify the repo and work context. Determine:
- Which repository is being worked on (owner/name)
- What feature, bug, or task is the focus

**Step 3:** Call `memory_search` with a complete semantic question about the
repo or work being done.

CORE classifies every query into one of 5 types (aspect, entity lookup,
temporal, exploratory, relationship) and routes to the optimal search
strategy. The query must be a full natural-language question so CORE can
determine intent.

**Step 4:** If the session involves external services or integrations, call
`get_integrations` to verify connection status.

### END OF EVERY SESSION

**Step 1:** Write the full ingestion message.

**Step 2:** Present the ingestion message to Max for review. Do not call
`memory_ingest` until Max approves the content.

**Step 3:** Once approved, call `get_labels`, select the appropriate
label(s), and call `memory_ingest` with the approved text, `sessionId`, and
label ID(s).

If no label fits, ingest without a label. Do NOT guess.

### HOW TO WRITE THE INGESTION MESSAGE

Write as if the next Claude Code session has zero context and needs to pick
up exactly where this session left off. If a detail would be needed to
continue the work - find the right file, understand why a decision was made,
reproduce a bug, or know what's left to do - it must be in the message.

Format:

```text
<user>Max Cogar is working on {repo} - {what the session goal was, with enough context to understand why}</user>
<assistant>{What was done, decided, built, fixed, and what state the work is in}</assistant>
```

## Non-negotiable rules

1. Do not silently rewrite the final spec from memory.
2. Do not treat handoffs or prior drafts as authority once the user has clarified otherwise.
3. Do not smooth over contradictions in prose before making them explicit.
4. Do not let a paragraph carry multiple independent decisions if those decisions could be separated.
5. Do not start implementation work from unresolved or contradictory design prose.

## Artifact model

This workflow uses distinct artifacts with distinct roles.

### 1. `spec-chunk.md`

Protected human record.

Use for:

- owner decisions as primary chunks;
- approved section text as amendments;
- preserving exact wording and traceability;
- maintaining a reversible history.

Do not use it for:

- freeform reconciliation;
- speculative rewrites;
- automatic replacement of older text.

### 2. `spec-inventory.md`

Current-spec snapshot.

Use for:

- exact breakdown of the real spec as written now;
- sections, DDs, ACs, scope claims, and sign-off claims;
- descriptive inventory only.

Do not use it for:

- approval;
- correction;
- merge decisions.

### 3. `spec-ledger.yaml`

Atomic source of truth.

Use for:

- one record per real decision or rule;
- owner decisions, surviving invariants, and explicitly marked new synthesis;
- later deterministic comparison against the codebase and draft prose.

### 4. `spec-conflicts.yaml`

Conflict register.

Use for:

- duplicate intent;
- overlapping intent;
- conflicting intent;
- unresolved ambiguity.

### 5. `spec-evidence.md` or `spec-evidence.yaml`

Evidence log.

Use for:

- repo findings gathered from direct reads, search, RAG, and deterministic extraction;
- proving where the codebase or docs mention a concept;
- backing claims without promoting evidence into authority.

### 6. Final spec Markdown

Derived artifact only.

Write it only after the decision set is stable enough to support prose safely.

### 7. Session handoff record

Durable session-close state.

For this workflow, use:

- `docs/specs/spec-session-status.md`

## Authority model

Always distinguish three things:

### A. Candidate authority

The final spec being stabilized.

### B. Verification basis

The owner decisions, approved wording, and other explicitly accepted constraints that the spec must faithfully encode during review.

### C. Evidence/context

Repo files, handoffs, prior drafts, plans, contracts, profiles, hooks, search results, and RAG findings.

Critical rule:

- evidence and context may justify review conclusions;
- they do not automatically become governing authority inside the spec.

## Statement classification

When reviewing any spec material, classify each questionable statement as one of:

1. `clear_and_acceptable`
2. `unclear_requires_owner_clarification`
3. `contradictory_or_nonfunctional_cannot_stay`

Do not preserve a statement just because you can imagine an interpretation that makes it work.

## Review posture

When fixing source text, prefer the smallest safe correction:

1. delete unsafe statement
2. narrow unsafe statement
3. split overloaded statement
4. only then rewrite larger passages

Avoid broad rewrites when the actual problem is an overloaded sentence or false attribution.

## Workflow

### Phase 1 — Capture known decisions

Goal:

- move known decisions out of unstable prose and into a protected record.

Process:

1. create or update `spec-chunk.md`;
2. record owner decisions as primary chunks;
3. attach approved section text as amendments without overwriting the primary chunks;
4. keep exact approved wording when it exists.

Exit:

- the known decisions are captured in chunk form.

### Phase 2 — Inventory the real spec

Goal:

- document exactly what the current spec says before trying to fix it.

Process:

1. create or update `spec-inventory.md`;
2. inventory all top-level sections;
3. inventory all explicit DDs, ACs, scope claims, and sign-off claims;
4. break large sections into meaningful decision-bearing units when useful.

Exit:

- the current spec is fully mapped.

### Phase 3 — Build the atomic ledger

Goal:

- create the machine-readable source of truth.

Process:

1. create `spec-ledger.yaml`;
2. create one ledger item per real decision or rule;
3. mark each item as:
   - `owner_decision`
   - `surviving_invariant`
   - `new_synthesis`
4. attach traceability to chunk IDs, approved section text, or explicit owner statements.

Critical rule:

- if something is new synthesis, label it honestly;
- do not attribute it to the owner or a standard unless that is explicitly true.

### Phase 4 — Register duplicates, overlaps, conflicts

Goal:

- make structural problems explicit before prose reconciliation.

Process:

1. create `spec-conflicts.yaml`;
2. record:
   - duplicate intent
   - overlapping intent
   - conflicting intent
   - unresolved ambiguity
3. give every issue an ID and status.

Definitions:

- **duplicate**: different text, same intent
- **overlap**: shared intent plus extra distinct material
- **conflict**: incompatible or competing intent

### Phase 5 — Gather evidence

Goal:

- collect repo reality and references.

Process:

1. read relevant plans, contracts, commands, profiles, hooks, tests, and prior specs;
2. use search and RAG to find all references to the concept under review;
3. record them in `spec-evidence.md` or `spec-evidence.yaml`.

Critical rule:

- RAG is for retrieval and discovery, not authority.

### Phase 6 — Deterministic conformance extraction

Goal:

- compare codebase facts to ledger truth where possible.

Process:

1. write small deterministic scripts for mechanically checkable facts;
2. extract actual values and declarations from the codebase;
3. compare them to the ledger;
4. record mismatches as evidence.

Good deterministic targets:

- declared inputs
- parameter names
- artifact names
- retry cap values
- route enums
- revision-mode sections present or absent
- direct `spec_path` mutation

### Phase 7 — Reconcile the ledger

Goal:

- resolve duplicates, overlaps, and conflicts before prose generation.

Process:

1. review `spec-conflicts.yaml`;
2. merge duplicates;
3. split or consolidate overlaps;
4. resolve conflicts explicitly;
5. leave unresolved ambiguity visible until answered.

### Phase 8 — Write final prose

Goal:

- generate stable Markdown from stable decisions.

Process:

1. map ledger items to target sections;
2. write section prose from the ledger, not from memory;
3. keep traceability from prose to ledger items;
4. avoid introducing fresh synthesis without explicit labeling and approval.

### Phase 9 — Final verification

Goal:

- confirm that the prose matches the ledger and does not carry hidden decisions.

Process:

1. compare each section to its ledger basis;
2. rerun deterministic checks where relevant;
3. reject any section that introduces hidden authority or unsupported glue text;
4. only then present for sign-off.

## Suggested ledger shape

Use fields like:

```yaml
- id: CL-001
  title: Retry cap
  status: approved
  type: process
  statement: The correction loop has a finite retry cap of 3 on the same card.
  rationale: Repeated failures beyond 3 indicate a deeper issue requiring separate investigation.
  source_basis:
    - owner_decision_2026_05_20
  scope: correction_loop
  constraints:
    retry_cap: 3
  related:
    overlaps_with: []
    conflicts_with: []
  notes: []
```

## Suggested conflict shape

Use fields like:

```yaml
- id: CF-001
  kind: overlap
  left: CL-003
  right: CL-014
  description: Both records govern correction-mode behavior, but one adds route-specific constraints.
  status: open
  resolution: null
  notes: []
```

## How to use this skill

When this skill triggers:

1. read `AGENTS.md`;
2. read `docs/specs/spec-workflow.md`;
3. read `docs/specs/spec-session-status.md`;
4. use CORE exactly as CORE requires for this workflow;
5. read `docs/specs/spec-chunk.md`;
6. read `docs/specs/spec-inventory.md`;
7. take the current phase from `docs/specs/spec-session-status.md`;
8. identify the authoritative artifact for that phase using `docs/specs/spec-workflow.md`;
9. do not skip earlier phases just because prose exists;
10. keep source-of-truth work separate from prose work;
11. explicitly say when a file is protected, inventory-only, working, frozen, or derived;
12. keep the user informed about what artifact is being changed and why;
13. close the session by updating `docs/specs/spec-session-status.md` if work stops midstream;
14. use CORE exactly as CORE requires before considering the session correctly closed;
15. for this workflow, that means completing the exact
    session-start / approval-before-write / session-end protocol from
    `C:\Users\maxco\.claude\CLAUDE.md` rather than improvising a local
    variant.

Do not create extra workflow/process files unless the owner explicitly asks for them. Use the existing workflow and status artifacts.

## Failure signs

This skill is failing if:

- you keep restating the same decision in multiple DDs without collapsing it;
- you cannot say whether a statement is authority, verification basis, or evidence;
- you are “fixing” prose while conflicts remain unresolved in the underlying decision set;
- you are using RAG results as if they are approval;
- you are writing new explanatory glue into the final spec that does not trace back to a ledger item.
