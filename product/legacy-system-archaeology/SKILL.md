---
name: legacy-system-archaeology
description: Use when inheriting an unfamiliar or under-documented implemented system and needing a pure evidence-backed baseline of implemented code, runtime behavior, entry points, state ownership, data lineage facts, identity, permission/approval topology, and current unknowns from current facts only.
---

# Legacy System Archaeology

Use this skill when the user wants more than a repo summary. The default goal is to turn an implemented legacy system into an evidence-backed baseline map. Migration or work-package planning is optional and must be requested explicitly.

## When to Use

- Old monolith, old service, script pile, or half-owned subsystem
- "Analyze this old system", "拆一下旧系统", "看清边界和链路"
- Migration/rewrite/module-split preparation that needs a factual baseline before any plan is written
- Implemented data lineage, duplicate data entry, reconciliation surfaces, approval routing, or permission inconsistencies
- Current analysis is too shallow, too file-oriented, or not actionable

Do not use this for a narrow bug, a single component review, a small feature diff, an audit against "就源输入、多次应用、环环相扣、相互稽核", or a proposed/new requirement review. For implemented-code closed-loop audit, use `implemented-closed-loop-audit` after this baseline. For new requirements or PRDs, use `closed-loop-requirement-drift` after the audit baseline exists.

## Scope Firewall

This skill documents what exists. Do not let future requirements pollute the archaeology.

Allowed evidence:

- implemented source code
- checked-in configuration
- database schema/migrations/mappers
- scripts, timers, queues, workers, routes, tests
- runtime output, logs, screenshots, or command output
- operational docs that describe current production behavior

Do not treat these as implemented facts:

- PRD target behavior
- roadmap items
- backlog tickets
- desired future screens
- stakeholder wishes
- speculative architecture

If the user provides a PRD together with code, use the PRD only to choose where to look. Do not write "missing requirement" findings in this skill's report. If the task is to judge whether a proposed requirement is good or risky, switch to `closed-loop-requirement-drift`.

## Required Outputs

Always produce these sections unless the user narrows scope:

0. `Reader Summary`
1. `System Inventory`
2. `Entry Points and Triggers`
3. `Core Flows`
4. `State and Dependency Map`
5. `Risk Ledger`
6. `Operational Ontology Draft`
7. `Technical Debt and Unknowns`

When the system is data-heavy, audit-like, report-driven, import/export-heavy, or reconciliation-heavy, also produce:

10. `Data Logic Map`

When the system contains movable business objects, re-parenting, archive/reactivate behavior, copy-and-lock migrations, workflow approvals, or data-scope permissions, also produce `Identity and Movement Integrity` and `Authorization and Approval Topology`.

This skill does not produce work-package plans, repair plans, rollout plans, or replacement sequences. If the user asks for those, first finish the pure archaeology baseline, then use a planning workflow outside this skill.

For full reports or handoff artifacts, finish with `Skill Compliance Checklist` so omissions are visible instead of silent.

## Artifact Delivery

For full archaeology reports, gap reviews, or handoff artifacts, write the complete output to a Markdown file in the target project's docs/report area. Do not paste the full report into chat unless the user explicitly asks for inline output.

The report must start with a localized `Reader Summary` before detailed evidence tables. Use the user's current conversation language unless the user explicitly requests another language. Do not default to English just because source code, file names, headings, or templates are English.

The final chat response must use the same language as the user and include only:

- the report file link
- a one-sentence conclusion
- 3 to 5 reader-facing bullets covering what the implemented system is, the strongest proven facts, the most important current risks or unknowns, and where a later audit should focus
- verification performed
- any remaining blocker

Do not make the final response a count of sections, rows, or commands. Counts may appear only as supporting verification after the practical conclusion is clear.

## Reader Summary Standard

For full reports, put `Reader Summary` immediately after scope/evidence metadata if those are legally or operationally required first; otherwise put it at the top of the report.

The summary must be understandable without reading the detailed tables. Include:

- `One-sentence conclusion`: what the implemented system is and how reliable the discovered baseline is
- `What is proven`: the most important implemented facts backed by evidence
- `Main risks / unknowns`: the current facts that create operational, data, identity, permission, approval, or traceability risk
- `What this report does not judge`: explicitly say this archaeology does not evaluate future requirements or score the sixteen-character principle
- `Next recommended review`: usually `implemented-closed-loop-audit` if the user needs principle compliance

Translate section labels into the user's language when helpful, but keep required artifact names such as `Data fact ledger`, `Module I/O matrix`, `Duplicate-entry and drift matrix`, and `Data flow graph` exactly where the skill requires exact names.

## Report Depth Gate

A full archaeology report must be a usable factual baseline for later implemented closed-loop audit or requirement-drift review. Do not stop at a short narrative, module list, or table of contents.

Minimum content for non-trivial systems:

- at least 8 system-inventory rows or every implemented subsystem if fewer exist
- at least 8 entry points/triggers across routes, jobs, scripts, workers, tests, or operational docs where applicable
- at least 5 reconstructed core flows with trigger, handler, state, side effect, and user-visible result
- at least 8 risk-ledger rows with severity, evidence, affected flow/module, and operational/change impact
- when `Data Logic Map` is required: fact ledger, module I/O matrix, duplicate/drift matrix, and Mermaid graph with typed edges
- when identity, movement, permissions, data scope, workflow, or approval are relevant: impact matrix plus authorization/approval topology instead of prose-only treatment
- unresolved unknowns listed explicitly with the command, file, runtime check, or stakeholder answer that would resolve each one

If the repository or evidence set is too small to meet these counts, state `insufficient evidence` in the compliance checklist and explain why. Do not deliver a thin chat answer as a substitute for the Markdown report.

Every non-trivial claim must be tagged as one of:

- `Observed`: directly supported by files, commands, configs, logs, tests, or runtime output
- `Inferred`: likely true from evidence, but not directly proven
- `Unknown`: missing evidence or unresolved contradiction

Do not add a fourth category like `Missing requirement` in this skill. A feature absent from the implementation is only `Unknown` or out of scope unless the current implemented system itself references it.

If the user asks whether implemented code satisfies "就源输入、多次应用、环环相扣、相互稽核", finish this factual baseline first, then run `implemented-closed-loop-audit`. Do not score the principle in this skill.

## Output Hygiene Gate

Before finalizing a full report:
- Include `Scope Firewall` and `Evidence Sources` before the main body so readers know what was inspected and what was excluded.
- Include a localized `Reader Summary` near the top, and make it decision-readable rather than a table-of-contents recap.
- Use contiguous section numbering only for sections that are actually present, or omit numbering entirely.
- Every evidence-bearing Mermaid diagram must use typed edges. Allowed labels include `trigger`, `read`, `write`, `input`, `derive`, `mutate`, `export`, `check`, `approve`, `lock`, `async`, `notify`, `manual`, `Unknown`, or `Inferred <type>`.
- For data-heavy systems, the `Data Logic Map` section must contain exact artifacts named `Data fact ledger`, `Module I/O matrix`, `Duplicate-entry and drift matrix`, and `Data flow graph`. Do not rename them into softer summary headings.
- In pure archaeology, the duplicate/drift matrix describes current duplication, drift risk, existing guards, and missing checks. Do not turn it into a repair plan; use `closed-loop-requirement-drift` for requirement-specific repair design.
- Do not put absent future targets into the fact ledger as if they were business facts. If the user asked about them, record them in `Unknowns That Need Direct Verification` or a direct-answer table tagged `Unknown`.
- The `Skill Compliance Checklist` must be a table with `present`, `partial`, `missing`, or `not applicable`; do not use checkbox bullets for full reports.

## Workflow

### 1. Set the excavation boundary

Start by fixing scope:

- target repo, service, module, or workflow
- user goal: migration, stabilization, rewrite, handover, or cost/risk review
- time horizon: whole system vs one bounded context

If scope is too large, decompose by runtime boundary first: web app, worker, cron/timer, queue consumer, data pipeline, admin/backoffice.

### 2. Build the static map first

Do not start from random files. Identify:

- executable entry points
- framework routes
- CLI commands
- timers / cron / daemons
- queue producers and consumers
- database schemas and migrations
- config roots and env vars
- external services and storage
- identity-bearing fields and code systems
- approval/workflow definitions
- permission and data-scope configuration surfaces
- org/container/user binding surfaces

Prefer fast probes such as `rg`, `rg --files`, `find`, `ls`, `sed`, `git log -- <path>`, and targeted test commands.

If useful, load [probe-queries.md](references/probe-queries.md) and run only the relevant patterns.

### 3. Reconstruct business flows

For each important workflow, trace the chain end to end:

`trigger -> controller/handler -> domain logic -> persistence -> side effects -> downstream jobs -> user-visible result`

Do this for the system's highest-value paths first, not for every file equally.

For each flow, capture:

- trigger surface
- major files and functions
- state written or read
- external calls
- retries, queues, timers, and async hops
- failure handling and silent fallbacks

When the user is worried about "why things break after moving under another parent/team/container/object", trace at least one full mutation flow and one full visibility/approval flow:

- `mutation flow`: move / migrate / clone / lock / deactivate / re-parent
- `visibility flow`: who can still see, edit, approve, or receive tasks afterward

### 4. Map state, ownership, and hidden coupling

Find where state really lives:

- database tables
- files
- caches
- queues
- buckets
- env vars
- generated artifacts
- third-party systems

Then mark hidden coupling:

- shared tables across modules
- implicit contracts through JSON blobs or files
- duplicated business rules
- magic values and feature flags
- cross-module imports that break clean boundaries
- cron jobs or scripts mutating the same entities out of band
- permissions keyed by business codes rather than stable object identity
- workflow routing keyed by parent/container/org bindings that drift after movement
- reports grouped by display code prefixes rather than business-permanent ids

Also identify the factual data chain shape without scoring it: first capture/import surface, canonical store, downstream reuse, mutation/writeback paths, independent checks, and missing traceability evidence.

Also classify identity usage for each core object:

- `business-permanent id`: the identifier that should survive migrations
- `stage/runtime id`: the identifier for the current placement or version
- `display/report code`: the identifier humans group or search by

If these are mixed in queries, permissions, or workflow routing, record that as a first-class risk.

### 4.5 Produce the data logic map

When data entry, reuse, reporting, accounting, audit, or reconciliation matters, do not leave the result as prose. Produce both a table and a graph that make the data logic visible.

The table must show, for each important business fact:

- where it is first entered or imported
- whether that source is canonical, derived, copied, manually corrected, or external
- which modules read it
- which modules write or mutate it
- which downstream tables, reports, exports, workflow tasks, or spreadsheets reuse it
- where the same fact is re-entered, duplicated, transformed, or silently overwritten
- what independent surface cross-checks it
- which source rows or query keys prove traceability

The graph must show:

- source-entry modules
- system-of-record tables
- derived tables or caches
- mutation paths
- report/export paths
- reconciliation or approval gates
- missing or unverified return paths

Use Mermaid when the output medium supports it. Mark each edge as one of:

- `input`: original capture/import
- `derive`: calculated or transformed reuse
- `mutate`: writes back or corrects state
- `export`: file/report/sheet output
- `check`: reconciliation, approval, or audit check
- `manual`: manual re-entry or spreadsheet correction

Every Mermaid edge in this section must include one of these labels. If a diagram edge cannot be backed by artifacts, either omit it or mark the label as `Inferred <edge-type>`.

### 5. Build the risk ledger

Do not stop at structure. Explain why the current shape is dangerous or expensive:

- no single owner
- weak tests around critical flows
- one-way moves/imports with no rollback
- side effects mixed into reads
- manual steps not reflected in code
- dead code that still encodes business assumptions
- credentials or host assumptions embedded in scripts

Each risk should include:

- severity
- evidence
- affected flow or module
- likely operational or change impact

Technical debt is not limited to old frameworks. It includes:

- duplicated source capture
- inconsistent field semantics across modules
- one-way data copies with no reconciliation
- reports that cannot be traced back to a source row
- manual spreadsheet corrections outside the governed chain
- timers or scripts that mutate data without feeding the audit trail
- parallel "temporary" tables that became production state
- object moves that preserve one identifier but break downstream visibility or aggregation
- approval configs keyed to parent/container code or org assignment without a rebinding strategy
- data permissions that still follow old parent codes after a business object moves

### 7. Draft the operational ontology

Translate the excavated system into operating objects, not just tables and modules.

At minimum, identify:

- core objects
- object identifiers
- canonical properties
- key state transitions
- links between objects
- actions that mutate them
- system of record vs derived read model

Good object candidates are domain-specific. Look for durable business objects, source documents/events, workflow tasks, approvals, reports, exports, configuration records, external references, and operational snapshots. Do not import example object names from another project unless they appear in the reviewed system.

The ontology draft must make explicit:

- which object is domain-native vs control/review/reporting-native
- which fields come from original source state vs derived surfaces
- where the same concept is duplicated across modules
- which identifiers are stable across moves vs regenerated per stage
- whether visibility and approval attach to the object, the current container, or both

### 7.5 Audit identity and movement integrity

If the system has objects that can move between parents, containers, tenants, departments, accounts, org trees, stages, or parent records, the archaeology must answer:

- what operation performs the move
- whether the move is `update-in-place`, `clone-and-lock`, `copy-and-archive`, or `soft-link re-parent`
- which identifiers stay stable and which regenerate
- where move history is stored
- which downstream modules read by permanent id vs stage id vs display code
- how to classify downstream state as `migrated`, `not migrated`, `duplicated`, or `lost`

The output must include an `Impact Matrix` when this section is present. If movement is not implemented or not found, still include rows marked `not applicable` or `Unknown`; do not replace the matrix with prose. The matrix must include at least:

- permanent id
- old/new stage ids
- old/new parent/container ids or display codes
- old/new display codes
- downstream domains checked
- status: `migrated`, `not migrated`, `duplicated`, `lost`, `not applicable`, or `Unknown`
- duplicate risk
- loss risk

### 7.6 Audit authorization and approval topology

If the system contains role-based permissions, data-scope permissions, org bindings, approval flows, or workflow task assignment, the archaeology must separate:

- base access control: users, roles, permissions, resources
- data visibility scope: tenant/account/org/container/object-level access
- org routing scope: department, position, authorization position, matrix ownership
- workflow template layer: process definitions, handlers, forms, transitions
- approval configuration layer: reviewers, thresholds, routing rules, overrides, delegation
- runtime evidence layer: current tasks, flow logs, messages, signatures

The output must explicitly ask:

- after an object moves, who can still see it
- who can edit it
- who receives approval tasks
- which config must be copied, rebuilt, or re-bound
- whether historical approvals and new approvals can still be reconciled to one business object

If a layer is absent or enforced outside the reviewed code, include it as `Unknown` instead of omitting it.

### 9. Record traceability facts

For each important business fact, answer:

- where is it first captured
- which object or table is the system of record
- how many downstream modules reuse it
- which reports or workflows re-check it
- where the chain forks
- where the chain loses traceability

If a fact is re-entered manually, transformed silently, exported without a return path, or corrected only in spreadsheets, record the observed gap and evidence. The compliance score belongs in `implemented-closed-loop-audit`.

For movable objects, permissions, and approvals, use factual continuity statuses: `proven`, `partial`, `unknown`, or `contradictory`. Do not use healthy/fragile/broken scoring in this pure archaeology skill.

## Evidence Rules

- Cite real file paths when describing behavior.
- Distinguish file evidence from runtime evidence.
- If a flow is guessed from naming alone, mark it `Inferred`.
- If the code and docs disagree, say so explicitly.
- Prefer "I could not prove X" over smoothing over the gap.
- Avoid architecture diagrams without artifact-backed edges.
- When the user cares about data lineage or auditability, cite the exact artifacts that prove reuse and cross-check, not just the source table names.

## Skill Compliance Checklist

For full reports, add a final checklist with `present`, `partial`, `missing`, or `not applicable` for:

- required base sections 1-7
- localized `Reader Summary` present near the top and reflected in the final chat response
- `Data Logic Map` when data/audit/reporting matters
- data logic artifacts: fact ledger, module I/O matrix, duplicate/drift matrix, Mermaid graph with typed edges
- `Identity and Movement Integrity` when movable or identity-sensitive objects exist, including the downstream impact matrix
- `Authorization and Approval Topology` when permissions, data scope, workflow, or approvals exist
- evidence tags: `Observed`, `Inferred`, `Unknown`
- unresolved unknowns that need direct verification
- report depth gate satisfied or explicit `insufficient evidence` explanation

## Depth Standard

The job is not complete when you can name the modules. It is complete when you can answer:

- what starts the important work
- where state changes happen
- what can run without the user's knowledge
- what breaks if one module is removed
- which parts can be isolated independently
- what boundaries are safe to isolate for later planning

## Common Failure Modes

- describing folders instead of behavior
- listing files without reconstructing flows
- producing work-package, rollout, repair, or replacement planning in a pure archaeology baseline
- assuming ownership boundaries from directory names
- ignoring timers, workers, generated files, and shell scripts
- missing manual operations outside the main app path
- producing a short chat-style summary that has required section names but not enough evidence rows, diagrams, or acceptance detail

## Deliverable Standard

The final artifact should let another engineer:

- understand the real runtime shape of the system
- see which conclusions are proven vs inferred
- support a later planning workflow without redoing the excavation
- identify the first ontology objects to formalize
- see where data lineage is proven, partial, or unknown
- isolate technical debt that breaks traceability or reconciliation
