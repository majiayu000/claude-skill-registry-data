---
name: code-review
description: "Architectural code review after each story implementation. Works for both game and product projects. Checks coding standards, architecture, SOLID, testability, and domain-specific concerns."
argument-hint: "[path-to-file-or-directory]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Task, Write, Edit
agent: lead-programmer
---

## Scope, decisions and exact evidence

Read `standards/evidence-lifecycle.md` and `standards/notes-adr-sync.md` from the
project root. Reuse original authorization only for its exact named paths, effects
and limits across roles/retries. Content agreement, writes, independent review,
ADR acceptance and Story/phase completion remain separate. Show a concrete draft
before asking about unresolved material choices or new effects; covered writes
need no repeated per-file or per-role permission.

Read/review-only never invokes a write entrypoint, including in memory. Report-only
may write its assigned new report, not inputs, indexes, session state, logs or T3
pointers. Each other effect needs existing scope or separate changeset authority.
No Memory Bank means the existing Story/review/conversation fallback, not activation.

Invoking a target writer callback is a write entrypoint even when it only appends
to an in-memory list. Review-only and report-only do not authorize non-dry-run
target validation that invokes a writer, or a constructor/factory that enters its
write path. Creating an inert observer or obtaining `calls.append` without calling
it is not a writer invocation. Authorized dry-run checks may use that spy to prove
zero calls; any unexpected callback is still a real scope breach, even without
disk effects. Trace the owning public caller, actual parameters, branch and
callback receiver before diagnostics; a private default does not establish the
public default. Static source ordering can establish write-before-validation
without exercising the writer. A write counterexample needs separately covered
repair/test authority and an isolated copy, not the reviewed original.

Bind claims to original paths, full SHA-256 (64 hex), byte sizes, collection time
with timezone, source commit plus exact uncommitted/ignored/external identities.
Read actual bodies and minimum required direct/indirect evidence closure; retain
recoverable originals and disclose missing inputs. Resolve CDD DocKind/required
owner set and module semantic eight through `design/INSTRUCTIONS.md`, preserving
substantive aliases; headings, counts or existence cannot establish PASS.

Classify each meaningful choice as `covered`, `cdd-layer`, `no-adr`,
`documentation-update`, `adr-required` or `conflict`, with named requirement/owner,
existing TR-ID if assigned, exact Accepted ADR revision/section/scope or justified
no-ADR reason, affected paths/dependencies, evidence and action/owner/due phase.
Trust boundaries, public contracts, durable formats, state ownership and governing
architectural constraints require an Accepted decision or valid scoped exception
under existing governance before affected implementation starts/continues. Continue
independent work. Proposed, implemented, green tests, write approval and director
recommendations do not establish acceptance; historical approval needs exact input
and authority/scope match. Justified `cdd-layer`/`no-adr` waives no other readiness,
manifest or evidence prerequisite. The existing global Technical Setup minimum of
three Foundation ADRs in `workflow/workflow-catalog.yaml` remains a separate gate:
do not bypass it or manufacture ADRs to meet a count.

Absent, conflicting or ambiguous substantive concept/configuration/owner evidence
means Unknown. Apply `standards/technical-preferences.md` before that conclusion;
a missing concept alone does not erase configured legacy Product facts. Continue
domain-independent checks while unresolved domain-specific rules remain pending.

## User Guide

- When to use: Architectural code review after each story implementation. Works for both game and product projects. Checks coding standards, architecture, SOLID, testability, and domain-specific concerns.
- Inputs: Command arguments: `/code-review [path-to-file-or-directory]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: Only when Memory Bank is initialized and each named write effect is covered: `memory_bank/t3_archive/reviews/review-index.md`.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Detection

Resolve the actual domain from substantive concept bodies, configured fields and
explicit project decisions under `standards/technical-preferences.md`:

- **Game**: consistent Game concept/configured legacy Game evidence → use `[Game]` paths below.
- **Product**: consistent Product concept or populated legacy Product configuration,
  including `Language & Framework`, `Platform & Deployment` and `Agent Routing`,
  can establish Product without a concept → use `[Product]` paths below.
- **Unknown**: absent substantive evidence or conflicting/mixed owners; continue
  common read-only checks and resolve the affected route before applying its rules.

Filenames, copied placeholders and the existence of both/neither concept files
alone do not establish a domain or override consistent actual configuration.

---

## Phase 1: Load Target Files

Read the target file(s) in full. Read CLAUDE.md for project coding standards.

---

## Phase 2: Identify Specialists

**[Game]** Read `standards/technical-preferences.md`, section `## Engine Specialists`. Note:

- The **Primary** specialist (used for architecture and broad engine concerns)
- The **Language/Code Specialist** (used when reviewing the project's primary language files)
- The **Shader Specialist** (used when reviewing shader files)
- The **UI Specialist** (used when reviewing UI code)

If the section reads `[TO BE CONFIGURED]`, no engine is pinned — skip engine specialist steps.

**[Product]** Read the actual configured `Product Stack`, `Language & Framework`,
`Language` or `Technology Stack` values in `standards/technical-preferences.md`.
Resolve populated `Agent Routing` and `File Extension Routing` in that Product
context; valid legacy headings do not need renaming. Placeholder values establish
no configured fact, and conflicting values block the affected specialist route.
Identify the primary language and actual configured specialist. The default
language mapping is:

| Language | Specialist Agent |
|----------|-----------------|
| Python | `python-specialist` |
| TypeScript / JavaScript | `typescript-specialist` |
| Rust | `rust-specialist` |
| Go | `go-specialist` |

If no language is configured, skip language specialist steps.

---

## Phase 3: ADR Compliance Check

Read actual code choices, owning Story/relevant Notes, named CDD requirements,
current TR registry/control manifest and governing Accepted decisions. Story/commit/
comment links are discovery aids; no ADR link never skips actual-choice review.

- `covered`: verify retained exact Accepted revision/section/authority/scope and
  actual current code/evidence, not filenames, green tests or implemented status.
- `cdd-layer`: cite substantive CDD-owned detailed contract without new architecture.
- `no-adr`: state the local implementation/testing/process reason and owner.
- `documentation-update`: required facts/links repaired before closure; only
  permitted advisory actions remain with owner/due phase.
- `adr-required`: significant choice lacks Accepted scope; CHANGES REQUIRED,
  route `/architecture-decision` before affected implementation continues.
- `conflict`: contradicts governing CDD/Accepted decision; CHANGES REQUIRED,
  report immediately and resolve through the owner before affected continuation.

Retain applicable deviation severities:
- **ARCHITECTURAL VIOLATION** (BLOCKING): explicitly rejected governing pattern
- **ADR DRIFT** (WARNING): divergence without forbidden pattern; classify materiality
- **MINOR DEVIATION** (INFO): local difference with no architectural impact

Record exact source/Story/Notes/CDD/decision/test identities (full SHA-256/byte size/
original paths, source commit plus changed/ignored inputs), evidence and affected
dependencies. Read complete manifest bytes; date-only identity is LegacyRecheck,
not automatic compliance. No-ADR waives no other required check. Required Proposed/
unknown acceptance cannot become approved through missing links or green tests.
Valid exceptions record authority/risks/exact scope without relabeling findings.
Continue independent review and report incomplete affected checks without code edits.

---

## Phase 4: Standards Compliance

**[通用场景]** Identify the system category and evaluate general standards:

- [ ] Public methods and classes have doc comments
- [ ] Cyclomatic complexity under 10 per method
- [ ] No method exceeds 40 lines (excluding data declarations)
- [ ] Dependencies are injected (no static singletons for core state)
- [ ] Configuration values loaded from config files (not hardcoded)
- [ ] Systems expose interfaces (not concrete class dependencies)

**[Game]** System categories: engine, gameplay, AI, networking, UI, tools
**[Product]** System categories: API, CLI, data, auth, integration, UI, ops, config

---

## Phase 5: Architecture and SOLID

### Architecture

**[Game]**
- [ ] Correct dependency direction (engine <- gameplay, not reverse)
- [ ] No circular dependencies between modules
- [ ] Proper layer separation (UI does not own game state)
- [ ] Events/signals used for cross-system communication
- [ ] Consistent with established patterns in the codebase

**[Product]**
- [ ] Correct dependency direction (infrastructure <- business logic, not reverse)
- [ ] No circular dependencies between modules
- [ ] Proper layer separation (presentation, feature, core, foundation)
- [ ] Events/messages used for cross-module communication (where applicable)
- [ ] Consistent with established patterns in the codebase

### SOLID

**[通用场景]**
- [ ] Single Responsibility: Each class has one reason to change
- [ ] Open/Closed: Extendable without modification
- [ ] Liskov Substitution: Subtypes substitutable for base types
- [ ] Interface Segregation: No fat interfaces
- [ ] Dependency Inversion: Depends on abstractions, not concretions

---

## Phase 6: Domain-Specific Concerns

### [Game] Game-Specific Concerns

- [ ] Frame-rate independence (delta time usage)
- [ ] No allocations in hot paths (update loops)
- [ ] Proper null/empty state handling
- [ ] Thread safety where required
- [ ] Resource cleanup (no leaks)

### [Product] Product-Specific Concerns

- [ ] **API Boundaries**: Input validation present; response shape is consistent; error responses follow project convention; status codes are correct
- [ ] **Schema Safety**: Database queries use parameterization (no string concatenation); migrations are reversible; schema changes have a downgrade path documented
- [ ] **Auth & Permission**: Authorization check on every protected endpoint; no auth logic in presentation layer; token/session handling follows security best practices
- [ ] **Error Handling**: Errors are caught and logged (not swallowed); user-facing error messages don't leak internal state; retry logic for transient failures where appropriate
- [ ] **Observability**: Key operations are logged at appropriate levels; metrics are emitted for critical paths; request IDs / trace context are propagated
- [ ] **Configuration**: No secrets in code; environment-specific config is externalized; feature flags have a removal plan
- [ ] **Migration Safety**: Data migrations are tested against a copy of production schema; rollback is tested; no destructive operations without a confirmation gate

---

## Phase 7: Specialist Reviews (Parallel)

Spawn all applicable specialists simultaneously via Task — do not wait for one before starting the next.

Pass every delegate the original named paths/effects, review-only or report-only
limits, exact inputs and pending decisions. Report-only permits its assigned new
report, not target writer probes; explicitly include the no-write-entrypoint rule
for in-memory callbacks. Inspect actual returned commands and callback receivers
before relying on diagnostic findings. Unchanged files, a delegate's assurance or
a parent's later stop/exclusion do not undo an observed scope breach. Retain and
label the breach; continue only unaffected authorized findings. If the actual
execution trace is unavailable, leave that diagnostic/scope assertion incomplete.

### [Game] Engine Specialists

If an engine is configured, determine which specialist applies to each file and spawn in parallel:

- Primary language files (`.gd`, `.cs`, `.cpp`) → Language/Code Specialist
- Shader files (`.gdshader`, `.hlsl`, shader graph) → Shader Specialist
- UI screen/widget code → UI Specialist
- Cross-cutting or unclear → Primary Specialist

Also spawn the **Primary Specialist** for any file touching engine architecture (scene structure, node hierarchy, lifecycle hooks).

### [Product] Language Specialist

If a language is configured, spawn the language specialist identified in Phase 2 for every target file.

Also spawn `lead-programmer` for any file touching cross-cutting architecture (auth, data access, config, routing, middleware).

### [通用场景] QA Testability Review

**[Game]** For Logic and Integration stories, also spawn `qa-tester` via Task in parallel with the specialists. Pass:
- The implementation files being reviewed
- The story's `## QA Test Cases` section (the pre-written test specs from qa-lead)
- The story's `## Acceptance Criteria`

Ask the qa-tester to evaluate:
- [ ] Are all test hooks and interfaces exposed (not hidden behind private/internal access)?
- [ ] Do the QA test cases from the story's `## QA Test Cases` section map to testable code paths?
- [ ] Are any acceptance criteria untestable as implemented (e.g., hardcoded values, no seam for injection)?
- [ ] Does the implementation introduce any new edge cases not covered by the existing QA test cases?
- [ ] Are there any observable side effects that should have a test but don't?

For Visual/Feel and UI stories: qa-tester reviews whether the manual verification steps in `## QA Test Cases` are achievable with the implementation as written — e.g., "is the state the manual checker needs to reach actually reachable?"

**[Product]** For all story types, also spawn `qa-tester` via Task in parallel with the specialists. Pass the same context. Ask the qa-tester to evaluate:
- [ ] Are test seams exposed (not hidden behind private/internal access)?
- [ ] Do the QA test cases map to testable code paths?
- [ ] Are any acceptance criteria untestable as implemented?
- [ ] Does the implementation introduce new edge cases not covered by existing tests?
- [ ] Are there observable side effects that should have a test but don't?

Collect all specialist findings before producing output.

---

## Phase 8: Output Review

```markdown
## Code Review: [File/System Name]

### [Game] Engine Specialist Findings / [Product] Language Specialist Findings: [N/A — no engine/language configured / CLEAN / ISSUES FOUND]
[Findings from specialist(s), or "No engine/language configured." if skipped]

### Testability: [TESTABLE / GAPS / BLOCKING]
[qa-tester findings: test hooks, coverage gaps, untestable paths, new edge cases]
[If BLOCKING: implementation must expose [X] before tests can run]

### Decision Dispositions and ADR Compliance: [JUSTIFIED / INCOMPLETE / DRIFT / VIOLATION]
[Each actual choice: disposition, named owner/requirement, exact Accepted scope or
no-ADR reason, full input identities, affected dependencies and action/owner]

### Standards Compliance: [X/6 passing]
[List failures with line references]

### Architecture: [CLEAN / MINOR ISSUES / VIOLATIONS FOUND]
[List specific architectural concerns]

### SOLID: [COMPLIANT / ISSUES FOUND]
[List specific violations]

### Domain-Specific Concerns

[Game]: [CLEAN / ISSUES FOUND]
[List game development specific issues, or "No game-specific issues found."]

[Product]: [CLEAN / ISSUES FOUND]
[List product-specific issues by category: API Boundaries, Schema Safety, Auth & Permission, Error Handling, Observability, Configuration, Migration Safety]

### Positive Observations
[What is done well — always include this section]

### Required Changes
[Must-fix items before approval — ARCHITECTURAL VIOLATIONs always appear here]

### Suggestions
[Nice-to-have improvements]

### Verdict: [APPROVED / APPROVED WITH SUGGESTIONS / CHANGES REQUIRED]
```

Default behavior is read-only. After presenting the review, reuse existing
report-only authority for its assigned new artifact. Only when this report effect
is uncovered ask whether the user wants to save it:

> "May I write this code review to `production/code-reviews/code-review-[scope]-[YYYY-MM-DD].md`?"

Within report-only scope write only the assigned new review artifact/readback.
Memory Bank index/pointer updates need separately named effect authority; report
approval does not cover them. Review-only invokes no write entrypoint, including
in memory, and makes no source/session/status edits.

Update the Memory Bank index only after the report is saved and only with authority
for that named index effect. Initialization alone, read-only scope and report-only
scope do not authorize it. If initialization or the intended effect is unresolved,
retain Unknown and leave the index unchanged. Before an authorized update, read
the saved immutable report revision and its exact input/evidence identities;
a proposed report or an INFO result is insufficient. This step does not initialize
Memory Bank.

Review index row:

- Review Type: `code-review`
- Source Artifact: `production/code-reviews/code-review-[scope]-[YYYY-MM-DD].md`
- Verdict: `APPROVED`, `APPROVED WITH SUGGESTIONS`, or `CHANGES REQUIRED`
- Scope: reviewed story, file set, module, or system

Use immutable Source Artifact revision plus exact input manifest identity; retain
older review/approval scope when an authorized current pointer updates. Do not create `memory_bank/` from
`/code-review`; if it does not exist, keep the saved review artifact and tell
the user to run `/constitute` to establish the memory_bank governance control
plane.

---

## Phase 9: Next Steps

- If verdict is APPROVED: run `/story-done [story-path]` to close the story.
- If verdict is CHANGES REQUIRED: fix the issues and re-run `/code-review`.
- If an ARCHITECTURAL VIOLATION is found: run `/architecture-decision` to record the correct approach.

## Exact-byte check availability

Use available read-only tools to collect complete raw-file SHA-256/byte size without
normalizing line endings. If exact bytes/digest or a required dependency cannot be
read, report the affected check incomplete; do not substitute a date, text rendering,
short hash or file existence. Analysis invokes no write entrypoint.
