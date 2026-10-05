---
{
  "schema_version": 1,
  "skill_id": "dotnet_change_analysis",
  "xid": "D94E3B3A7C11",
  "aliases": [
    "1F4A6D20B8E1"
  ],
  "summary": "analyze .NET application structure and generate a Markdown change-analysis note for later design or implementation work",
  "applies_when": [
    "user needs repository-based .NET structure analysis, impact investigation, or a Markdown change-analysis note before changing code, especially brownfield code where responsibility separation is not documented and must be read from the code"
  ],
  "exclusions": [
    "Defect-level review belongs to csharp_review",
    "Vulnerability assessment belongs to security_review",
    "Implementation policy is not decided unless explicitly requested"
  ],
  "inputs": [
    "target path, change request or analysis objective, optional scope filters, optional output path"
  ],
  "outputs": [
    "Markdown change-analysis note, scoped target list, impacted boundary list, structure pivot inventory, route/usecase trace matrix, implicit runtime binding inventory, domain-knowledge candidate metadata for later `knowledge_ontology_management` publication, uncertainty list, viewpoint check results, change placement basis, prohibited-changes list derived from extracted local rules, and a handoff list for defect-level or security-scope discoveries"
  ],
  "criteria": [
    {
      "id": "closure_1",
      "statement": "every viewpoint bucket has a recorded state (`done`, `unknown`, or   `not_applicable`)",
      "verification": "Record evidence and apply the existing Workflow verification and closure gates"
    },
    {
      "id": "closure_2",
      "statement": "structure pivots, route/usecase traces, and implicit runtime bindings are   recorded when present, or explicitly marked `not_applicable`",
      "verification": "Record evidence and apply the existing Workflow verification and closure gates"
    },
    {
      "id": "closure_3",
      "statement": "the change placement basis is recorded for the change objective",
      "verification": "Record evidence and apply the existing Workflow verification and closure gates"
    },
    {
      "id": "closure_4",
      "statement": "the prohibited-changes list is recorded and every entry carries its basis,   breakage mode, and evidence (an explicitly empty list with reason is valid)",
      "verification": "Record evidence and apply the existing Workflow verification and closure gates"
    },
    {
      "id": "closure_5",
      "statement": "the change-analysis note exists at the declared output path",
      "verification": "Record evidence and apply the existing Workflow verification and closure gates"
    },
    {
      "id": "closure_6",
      "statement": "every non-trivial conclusion carries its evidence path",
      "verification": "Record evidence and apply the existing Workflow verification and closure gates"
    },
    {
      "id": "closure_7",
      "statement": "impacted targets and unresolved items are listed with reasons",
      "verification": "Record evidence and apply the existing Workflow verification and closure gates"
    },
    {
      "id": "closure_8",
      "statement": "defect-level and security-scope discoveries are on the handoff list, not   silently dropped",
      "verification": "Record evidence and apply the existing Workflow verification and closure gates"
    },
    {
      "id": "closure_9",
      "statement": "the run log passes `python -m xrefkit skill close`",
      "verification": "Record evidence and apply the existing Workflow verification and closure gates"
    }
  ],
  "knowledge_needs": [
    {
      "id": "common_source_analysis_criteria",
      "query": "common source analysis criteria",
      "required_when": "Required by this Skill; resolve applicable material before claiming coverage",
      "seed_xids": [
        "5F21C8A41001"
      ]
    },
    {
      "id": "custom_framework_common_criteria",
      "query": "custom framework common criteria",
      "required_when": "Required by this Skill; resolve applicable material before claiming coverage",
      "seed_xids": [
        "5F21C8A41002"
      ]
    },
    {
      "id": "dotnet_change_analysis_viewpoints",
      "query": "dotnet change analysis viewpoints",
      "required_when": "Required by this Skill; resolve applicable material before claiming coverage",
      "seed_xids": [
        "2E7B5A1FD201"
      ]
    },
    {
      "id": "structure_analysis_determinism_tiers",
      "query": "structure analysis determinism tiers",
      "required_when": "Required by this Skill; resolve applicable material before claiming coverage",
      "seed_xids": [
        "5301B897BA41"
      ]
    },
    {
      "id": "structure_graph_tm_backstop",
      "query": "structure graph tm backstop",
      "required_when": "Required by this Skill; resolve applicable material before claiming coverage",
      "seed_xids": [
        "163AD9936979"
      ]
    }
  ],
  "control_refs": [
    "B7A2C94F0E61",
    "A7F3C92D4E11",
    "6B2D9F4A1C73"
  ]
}
---
<!-- xid: D94E3B3A7C11 -->
<a id="xid-D94E3B3A7C11"></a>

# Skill: dotnet_change_analysis

## Purpose

Analyze an existing .NET application structure and produce a Markdown change-analysis note that can be used as working material before design or implementation changes.

This skill is built for brownfield modification: the responsibility split is
usually not written in any design document and must be derived from code
evidence. When no design record exists, the produced note is the de-facto
design baseline for the subsequent modification.

This skill records structure and change impact. It does not produce defect
findings (that is `csharp_review`) and does not perform vulnerability
assessment (that is `security_review`).

Use the canonical viewpoints in `knowledge/source_analysis/120_dotnet_change_analysis_viewpoints.md#xid-2E7B5A1FD201`.

## Optional References

- [Dotnet change analysis template](references/change_analysis_template.md#xid-6B38F0E4C2A7)

## Inputs

- target path (repository root, solution, or project)
- change request or analysis objective
- optional scope filters (solution, project, directory, feature, file pattern)
- optional output path for the generated Markdown

## Outputs

- Markdown change-analysis note
- impacted boundary list split into review boundary and must-change boundary
- (only when Semantic-Inventory Mode is used) the specific deterministic inventory
  generated for a grep-weak question, recorded as evidence
- structure pivot inventory for non-standard or custom-framework runtime wiring
- route/usecase trace matrix for representative runtime paths
- implicit runtime binding inventory for non-compiler-enforced bindings
- domain-knowledge candidate metadata sufficient for later Skill-side selection
- scoped target list
- uncertainty list
- check results by viewpoint
- change placement basis (de-facto home of the affected logic and the
  responsibility impact of each placement option)
- prohibited-changes list derived from the extracted local rules (changes
  that would break behavior silently, each with basis, breakage mode,
  evidence, and safe alternative)
- handoff list for defect-level or security-scope discoveries

## Startup

- Confirm the target path exists.
- Confirm the change request or analysis objective exists.
- Confirm the review scope is defined when filters are supplied.
- When invoked from `design_flow`, confirm which implementation target lacks
  current source structure findings and treat that target as the analysis scope.
- Load the dotnet change-analysis viewpoints.
- Record `unknown` when project or runtime boundaries cannot be established cleanly.

## Planning

- Define the analysis scope:
  - repository
  - solution
  - project
  - directory or file subset
- Define the output path:
  - user-specified path
  - default working Markdown path when no path is supplied
- Plan the Where path as grep-first; decide which viewpoints (if any) need
  Semantic-Inventory Mode (the grep-weak questions: DI lifetimes, attribute values,
  async-CT, IDisposable ownership, reflection binding, transitive impact) and
  restore the target only if a pack inventory is needed.
- Prepare viewpoint buckets for:
  - structure and responsibility split
  - structure pivots
  - entry points and dependency direction
  - DI registration and lifetimes
  - pipeline structure and order
  - route/usecase trace matrix
  - convention-based discovery
  - implicit runtime binding
  - configuration boundary
  - build-configuration-dependent behavior
  - API, database, and external integration boundary
  - error handling contract
  - security boundary placement
  - logging policy
  - attribute usage
  - concurrency and execution timing
  - performance and resource efficiency
  - test boundary
  - change impact and unresolved items
- If the scope can be separated by solution or project without cross-scope consistency risk, decompose the read-only investigation by scope and execute through subagents.

## Where Impacted-Boundary Analysis (grep-first)

The standard Where path is **grep-first, not pack-first**. An A/B test
([ADR 0001](../../docs/adr/0001-where-step-grep-first.md#xid-F4B92B6AC13E))
showed that for text-greppable impact — type names, method names, construction
sites, references — the deterministic structure pack gives **no token or accuracy
gain** over grep at any codebase scale, because `grep`/`rg` returns the full
reference surface in one pass and an LLM classifies the impact pattern without
reading most files. Do **not** generate the structure pack as a standard Where
backstop.

Standard path for text-greppable impact:

- `grep` / `rg` for the changed entity (type, method, config key) to get the full
  reference surface in a single pass.
- Read a small representative subset (the declaration, a few call sites) — not every
  hit — to read the impact pattern.
- Classify the impact pattern with the LLM (e.g. "object-initializer construction →
  a new required constructor parameter breaks every site"; "additive property →
  read-only consumers do not break").
- Separate the **review boundary** (everything referencing the entity, to check
  whether it must thread the change) from the **must-change boundary** (the sites
  the change actually breaks).

## Semantic-Inventory Mode (deterministic pack — grep-weak questions only)

Invoke the deterministic pack **only** for questions `grep` answers poorly — where
the fact needs constant folding, type/lifetime resolution, or transitive graph
traversal with no textual footprint. Precondition: restore the target
(`dotnet restore <sln-or-csproj>`) so Roslyn resolves symbols; pass the solution or
root project (referenced projects load transitively). Generate only the inventory
the question needs, not the whole pack. See
[Structure-analysis determinism tiers](../../knowledge/source_analysis/121_structure_analysis_determinism_tiers.md#xid-5301B897BA41).

| Grep-weak question | Pack tool |
|------|------|
| custom attribute values (constant-folded ctor/named args) | `tools/structure_graph --attributes` + `tools/attribute_inventory_report.py#xid-86FEF434AF94` |
| DI lifetime graph / captive-dependency | `tools/structure_graph --di` + `tools/di_registration_report.py#xid-66D9070B4548 --graph` |
| async methods lacking CancellationToken | `tools/structure_graph --decl` + `tools/declaration_facts_report.py#xid-4F003AE89B45 --category async --missing-ct` |
| IDisposable / IAsyncDisposable ownership | `implements` edges in `graph.json` + the CA2000 / CA2213 analyzer pipeline |
| reflection / convention-based binding sites | `tools/structure_graph --invocations` + `tools/invocation_facts_report.py#xid-7577F6A5C6AC --category discovery` |
| transitive impact with no textual reference | `tools/where_seed_traversal.py#xid-39959ED2E7EC --seed <s>` (the one impact case grep cannot follow) |

These are candidate facts, not verdicts: confirm activation / consuming mechanism,
curate against the change objective, and record what the pack cannot establish as
`unknown`. Record any generated inventory file as an `evidence` artifact.

## Execution

- For text-greppable viewpoints, run the grep-first Where path; invoke the
  deterministic pack only in Semantic-Inventory Mode for the grep-weak questions
  listed there. The pack is a fallback for specific questions, not a standard pass.
- Identify the solution, projects, startup paths, and major module boundaries.
- Extract the de-facto responsibility split from behavior evidence:
  - derive each component's actual responsibility from what calls it, which
    data it owns or mutates, and which business rules it evaluates — never
    from its name or folder
  - record name-behavior mismatches as findings
  - detect duplicated rule ownership and record every owner of the same rule
  - extract implicit responsibility conventions and record whether they are
    documented or implicit
- Trace the current execution entry points and main dependency directions.
- Identify structure pivots before treating any framework-shaped assumption as true:
  - runtime authorities such as XML command maps, config sections, route tables,
    custom registries, attributes, generated files, database metadata, naming
    conventions, and external framework source
  - the behavior each pivot controls and the code or artifact it activates
  - documented versus implicit status
  - pivot-sensitive tokens that can break silently on rename, move, field-name
    drift, assembly-name drift, missing registration, or order change
- Record DI registrations and lifetimes:
  - registration sites and chosen lifetimes (singleton, scoped, transient)
  - captive-dependency risks where a longer-lived service consumes a
    shorter-lived one
  - hosted services and background registrations
  - components constructed with `new` in layers that otherwise resolve
    through the container
- Record pipeline structure and order by extracting the local rules:
  - enumerate the pipelines that exist here from local evidence (builder
    call sequences, registration order, custom pipeline or handler-chain
    classes, message and batch stage definitions)
  - extract what establishes each pipeline's order (code order,
    configuration, attributes, conventions, a custom registry) and whether
    that rule is documented or only implicit — implicit ordering rules are
    themselves a finding
  - determine what the order controls from local behavior; do not assume
    well-known framework ordering semantics for custom or wrapped pipelines
    without local evidence — mark such assumptions `unknown`
  - record which order-dependent behavior the intended change could disturb
- Record route/usecase traces for representative runtime paths:
  - entry identity: URL, command, message, schedule, screen action, or callback
  - structural authority: route file, XML command, attribute, registry,
    database metadata, convention, or generated mapping
  - binding mechanism: direct call, reflection, string type name, DI, factory,
    convention, request field, model key, or payload field
  - executable owner, result selector, output boundary, model/input binding,
    state boundary, persistence boundary, evidence, and unresolved checks
  - when a route list exists without the cross-file binding path, treat the
    trace as incomplete
- Record convention-based discovery by extracting the local wiring rules:
  - where naming, placement, or assembly scanning decides runtime wiring
  - the matched pattern, scan location, and included assemblies or namespaces
  - which renames or moves would silently break discovery (no compiler error)
- Record implicit runtime bindings as first-class structure facts:
  - XML/config string bindings, reflection type names, assembly-qualified class
    names, controller return strings, view/ref names, request/form field names,
    serialization names, model keys, command names, redirect targets, and
    custom registry keys
  - producer, consumer, token, binding mechanism, evidence, and silent breakage
    mode for each binding
  - do not rely on C# references alone when the runtime binding crosses XML,
    config, ASPX, generated files, database metadata, or framework source
- Record configuration sources, option bindings, environment-dependent
  behavior, and feature-toggle conventions.
- Record build-configuration-dependent behavior:
  - conditional compilation symbols and the behavior they gate
  - multi-target frameworks and per-TFM implementation splits
  - MSBuild conditions that change project content per configuration
  - which configurations the intended change must be verified against
  - rules the compiler enforces within one configuration (nullable,
    warnings-as-errors, analyzer config) are out of scope
- Record API, database, messaging, and external service boundaries, including
  the serialization contract conventions that apply on the wire.
- Record the error handling contract — extraction only, not defect detection:
  - representation convention (exception hierarchy, result types, error codes)
    and which layers use which
  - translation points where infrastructure exceptions are wrapped, and the
    local rule that decides the target type
  - propagation conventions: what crosses each boundary, what is logged
    versus rethrown versus absorbed by design
  - retry and compensation conventions as local rules
- Record security boundary placement:
  - where authentication and authorization are structurally enforced
    (schemes, policies, attributes, endpoint conventions)
  - entry paths without protection and whether that is intentional
  - structural placement only — vulnerability assessment hands off to
    `security_review`
- Record logging policy, sensitive-data handling, and operational monitoring impact.
- Analyze attribute usage with the following rule:
  - extract attribute usage candidates from `[]` syntax
  - exclude numeric tokens and syntax that is not an attribute
  - resolve each candidate as both `Xxx` and `XxxAttribute`
  - confirm namespace and definition origin
  - record usage location, arguments, and target
  - confirm the consuming code and the activation condition
  - mark the attribute as `unknown` when the consuming mechanism cannot be confirmed
- Record concurrency, scheduling, shared state, cancellation, and transactional boundaries.
- Record performance-sensitive paths and resource lifetime/ownership points.
- Record test boundaries and the tests that should detect the intended change.
- Record the change placement basis for the change objective:
  - the de-facto home of the logic the change touches, per the extracted
    responsibility split
  - each realistic placement option with its responsibility impact: does it
    follow the extracted local rules, and would it create a second owner for
    an existing rule
  - facts only — the placement decision belongs to planning or design
- Derive the prohibited-changes list from the extracted local rules:
  - prohibit only changes that would break behavior silently — no compiler
    or analyzer diagnostic; compiler-caught mistakes need no prohibition
  - every prohibition cites the extracted rule it derives from, the silent
    breakage mode, and the evidence; no evidence, no prohibition
  - classify `hard` (breaks in all known cases) or `conditional` (safe only
    with an accompanying step), and state the safe alternative or the
    deviation condition including who decides
  - deliberate design rules (for example a documented fail-fast constructor)
    produce prohibitions against casually removing them, with deviation
    routed to a human
- Generate the Markdown note by using the template structure from `references/change_analysis_template.md` or an equivalent structure.
- Include a domain-knowledge candidate section when the analysis reveals a
  reusable service topology or package/framework behavior. Record only the
  metadata later Skills need for selection and use: framework family, routing
  authority, entry/controller/view/model/state/persistence binding modes,
  change-sensitive tokens, prohibited-change rules, and unresolved verification.
  Do not add redundant `applies_to`; Skill-side selection owns applicability.
  Do not require path when a stable XID/document identity can resolve content.
- The Skill does not publish canonical knowledge directly. When the finding is
  needed as a design basis, hand the domain-knowledge candidate to
  `knowledge_ontology_management` so it can create or refresh a current entry in
  the source-structure findings catalog.
- Keep output roles non-overlapping:
  - `structure pivots` records investigation starting points and the behavior
    each pivot controls
  - `route/usecase trace matrix` records representative cross-file runtime paths
  - `implicit runtime binding` records non-compiler-enforced tokens and their
    producer/consumer relationship
  - `prohibited changes` records only actionable silent-break rules derived
    from extracted local rules
  - `impacted targets` records change-objective-specific review and must-change
    boundaries, not a restatement of all structure-sensitive tokens
  - `domain-knowledge candidate` records compact Skill-selection metadata only
- Do not add a separate change-impact checklist when the same tokens are already
  covered by implicit runtime bindings and prohibited changes.
- Do not present domain-knowledge candidate data twice; use the table form only,
  with at most a short boundary sentence before it.

## Skill-Specific Monitoring and Control

- Treat every viewpoint as recorded only when it has a state:
  - `done`
  - `unknown`
  - `not_applicable`
- Treat unrecorded viewpoints as analysis leaks.
- Separate observed structure, inferred change impact, and missing evidence.
- Preserve the evidence path for every non-trivial conclusion, and when the
  evidence came from a command or search, record the command or pattern so
  the conclusion can be re-verified.
- For each extracted local rule, record whether it is documented (and where)
  or implicit; implicit rules default to unresolved follow-up candidates.
- Route defect-level or security-scope discoveries to the handoff list
  instead of expanding the analysis scope mid-run.

## Skill-Specific Unknowns And Risks

- Mirror every `unknown` viewpoint state that affects this Skill's closure as an
  `unknown` concern, and record unresolved external dependencies as unknowns.
- Record discovered-but-unanalyzed defect or security areas as `risk` concerns
  pointing at the handoff list. The common concern lifecycle and closure checks
  are supplied by the referenced Skill Operating Contract.

## Closure Gate

Closure is allowed only when all of the following hold:

- every viewpoint bucket has a recorded state (`done`, `unknown`, or
  `not_applicable`)
- structure pivots, route/usecase traces, and implicit runtime bindings are
  recorded when present, or explicitly marked `not_applicable`
- the change placement basis is recorded for the change objective
- the prohibited-changes list is recorded and every entry carries its basis,
  breakage mode, and evidence (an explicitly empty list with reason is valid)
- the change-analysis note exists at the declared output path
- every non-trivial conclusion carries its evidence path
- impacted targets and unresolved items are listed with reasons
- defect-level and security-scope discoveries are on the handoff list, not
  silently dropped

## Handoff

- Hand the change-analysis note to the requester and to the next phase —
  typically `planning_flow` (which takes current source structure findings as
  input) or design work.
- When invoked because `design_flow` lacked source analysis for an implementation
  target, hand back the output path as source evidence and the
  domain-knowledge candidate for `knowledge_ontology_management`; design closure
  should use the published canonical finding XID as the source analysis basis
  reference.
- Instruct the receiving phase explicitly: the modification must follow the
  extracted local rules and the change placement basis; any deviation must be
  recorded with its justification, not applied silently.
- The prohibited-changes list is a gate for the receiving phase: a `hard`
  prohibition is violated only with an explicit human decision recorded in
  the receiving run; a `conditional` prohibition requires its accompanying
  step to be part of the same change.
- When the existing structure is itself the problem (broken responsibility
  split, harmful local convention), record it as a `risk` concern and leave
  the decision to expand the fix scope to a human — do not fold structural
  repair into the modification silently.
- Suspected defects discovered during analysis (async hangs, resource leaks,
  synchronization risks) hand off to `skills/csharp_review/meta.md` — record
  them, do not deep-dive them here.
- Suspected security gaps hand off to `skills/security_review/meta.md`.
- Record each handoff as a `handoff` artifact in the run log so the receiving
  run can verify closure of this run before continuing.

## Rules

- Do not decide implementation policy unless the user explicitly asks for it.
- Do not invent a cleaner target architecture without explicit evidence and change intent.
- Derive responsibilities from behavior evidence, never from names or folders.
- Provide placement facts, not placement decisions; the placement choice
  belongs to planning or design.
- Derive prohibitions only from extracted local rules with evidence — never
  from generic best practices, and never for mistakes the compiler or a
  configured analyzer already catches.
- For custom attributes, do not stop at inventory; confirm definition, usage, consuming mechanism, and activation condition.
- For DI analysis, do not stop at the registration list; confirm lifetimes and
  captive-dependency risks.
- For logging analysis, include both emitted information and forbidden information exposure risk.
- For concurrency analysis, include execution timing, shared state, and transaction boundaries.
- For performance analysis, include hot paths, avoidable overhead, and resource lifetime ownership.
- Record structure and change impact only; defect-level findings and
  vulnerability assessment go to the handoff list for `csharp_review` and
  `security_review`.
- Use subagents only when scope boundaries stay explicit and cross-scope reasoning is not required.

