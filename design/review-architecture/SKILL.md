---
name: review-architecture
description: Review system architecture — layering, module boundaries, coupling/cohesion, pattern fit, quality attributes (scalability, resilience, evolvability), and architectural smells. Triggers "review architecture", "architecture review", "system design review", "check architecture".
argument-hint: '[--staged | --unpushed | --changed | --all | --multi]'
effort: xhigh
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Review Architecture

Macro-level review of system structure: how modules, layers, and components fit together. Complements `review-cleancode` (micro/code smells) and `review-interfaces` (single-interface design).

## Usage

```
/review-architecture                  # Review context-related code
/review-architecture --staged         # Review staged changes against the surrounding architecture
/review-architecture --unpushed       # Review all unpushed commits against the surrounding architecture
/review-architecture --changed        # Review unstaged changes against the surrounding architecture
/review-architecture --all            # Full system audit (parallel agents per category)
/review-architecture --multi          # Also get external advisor opinions
```

## Scope

| Flag | Scope | Method |
|------|-------|--------|
| (none) | Context-related code | Files from the current conversation context. If no context, ask the user to specify a target or use `--staged`/`--changed`/`--all`. |
| `--staged` | Staged changes + their architectural context | `git diff --cached --name-only`, then read each file's surrounding module/layer to judge fit |
| `--unpushed` | Unpushed commits + their architectural context | `git diff --name-only $(git rev-list HEAD --not --remotes \| tail -1)^..HEAD`, then read each file's surrounding module/layer to judge fit |
| `--changed` | Unstaged changes + their architectural context | `git diff --name-only`, then read each file's surrounding module/layer to judge fit |
| `--all` | Full system | Map directory/module structure, then parallel agents per category |
| `--multi` | Add external opinions | Combines with any scope; invokes `second-opinion --quick` |

`--unpushed` derives its range from `git rev-list HEAD --not --remotes` (oldest unpushed commit's parent → HEAD). If nothing is unpushed, or there is no remote/upstream (or the range walks back to the root commit) so it can't be determined reliably, stop and ask the user to pick another scope.

## Gotchas
- Architecture issues are **structural** — a small staged diff can introduce a major architectural problem (e.g., a UI file importing from the database layer). Always read the surrounding module, not only the diff.
- "Looks modular" ≠ "is modular". A folder split with shared mutable state, or many files all importing one "manager", is the **modular mirage** — flag it.
- Project-specific architecture (documented in `CLAUDE.md`, `docs/`, ADRs) overrides generic best practice. Read those first; do not flag a deliberate deviation as a violation.
- Don't re-litigate `review-cleancode` (SOLID at class level) or `review-interfaces` (single-function/class design). Architecture is about **between** modules, not within one.
- Single-file or single-module changes rarely have architectural impact. If `--staged` only touches isolated leaf code, say so and stop — do not invent issues.

## Workflow

1. **Read project conventions first** — `CLAUDE.md` (root + relevant subdirs), `docs/architecture/`, `docs/adr/`, any ADR-style markdown. These define the intended architecture; the review checks alignment to it, not to a generic ideal.
2. **Determine scope** based on flags (see Scope table).
3. **Map the structure**:
   - For `--staged` or `--changed`: identify which modules/layers the changed files belong to and what they import from.
   - For `--all`: build a quick mental map of top-level modules, their dependencies, and the dominant pattern (layered, hexagonal, event-driven, modular monolith, microservices).
4. **Review against the 6 categories** in the Architecture Checklist below.
5. **Parallelize** if `--all` or the diff scope spans >5 modules: spawn one sub-agent per category, each scanning across the scope. Merge and deduplicate findings.

   Dispatch workers that return findings without editing files. Disable delegation tools where supported; read-only access alone does not prevent delegation. Any coordinating role needs explicit subtasks, a descendant limit, and a stopping condition in its brief.
6. **External opinions** (if `--multi`): invoke `second-opinion --quick`, which queries every advisor it has configured, in parallel (the roster lives in the `second-opinion` skill). Phrase the diff source according to the resolved scope (`git diff --cached` for `--staged`, `git diff` for `--changed`, the whole repository for `--all`):

```
Read-only architecture review. Review the architecture of the <diff source> and their surrounding modules in this repository. Focus on: module boundaries and coupling, layering violations, pattern consistency, support for stated quality attributes (scalability, resilience, evolvability), and architectural smells (god modules, circular deps, leaky abstractions, manager classes, modular mirage). Provide a focused review in 300 words or less.
```

Wait for all external results before proceeding to step 7.

7. **Classify severity** for each finding:
   - **Critical**: Structural defect that will cause cascading bugs, block scaling, or make a class of changes dangerous (e.g., circular module dependency, layer inversion, broken bounded context).
   - **High**: Significant maintainability or evolvability problem (e.g., god module, leaky abstraction across a major boundary, missing seam where one is needed for the stated quality attribute).
   - **Medium**: Pattern inconsistency or coupling smell that increases cognitive load (e.g., one feature using a different communication pattern than the rest, mild abstraction leak).
   - **Suggestion**: Improvement opportunity with marginal current impact (e.g., extract a shared kernel, rename a module to match its responsibility).
8. **Report findings** grouped by severity using the Output Format below.

## Architecture Checklist

### 1. Layering & Boundaries

- **Layer respect**: Does each file import only from layers it is allowed to depend on? (e.g., domain → no infrastructure imports; UI → no direct DB imports.)
- **Bounded contexts**: Are domain boundaries clear, and does data cross them through explicit contracts (DTOs, events, ports) rather than shared mutable models?
- **Leaky abstractions**: Does an abstraction expose details of its implementation (e.g., a "Repository" returning ORM-specific types, a "transport-agnostic" interface that takes HTTP headers)?
- **Public vs internal**: Are module exports curated, or is everything public by default?
- **Dependency direction**: Does the dependency graph point inward (toward stable, abstract code) or is it tangled?

### 2. Module Structure & Coupling

- **Circular dependencies**: Module A imports from B which (transitively) imports from A. Always Critical at the module level.
- **God module**: A module that everyone imports from and that imports from everyone (high fan-in *and* fan-out).
- **Modular Mirage**: Folders look modular but share global state, a singleton "manager", or a fat utility module — structural split without semantic cohesion.
- **Manager / orchestrator centralization**: One module containing all the orchestration logic that other modules merely defer to. Often emerges from AI-generated code; redistribute behavior to the modules that own the data.
- **Shotgun coupling**: A single conceptual change requires edits across many modules — boundaries are drawn on the wrong axis.
- **Cohesion**: Are the things in a module actually about the same concept, or just colocated?

### 3. Pattern Fit & Consistency

- **Right pattern for the problem**: Layered, hexagonal/ports-and-adapters, event-driven, modular monolith, microservices — does the chosen pattern match the system's scale, team structure, and change rate?
- **Consistency**: Is the dominant pattern applied consistently, or do some features bypass it (one feature talking to the DB directly while everything else goes through a repository)?
- **Communication patterns**: Sync vs async, request/response vs events — used consistently and for the right reasons?
- **Data ownership**: Each piece of data has exactly one writing module; others read via API/event.
- **Anti-patterns**: Distributed monolith (microservices that must deploy together), anemic domain (logic lives in services, models are bags of fields), big ball of mud (no discernible structure).

### 4. Quality Attributes

For each attribute the project cares about, check whether the architecture actively supports it. Don't grade attributes the project doesn't claim.

- **Scalability**: Stateless vs stateful boundaries; horizontal scale points; cache layers; data partitioning; single points of contention.
- **Resilience**: Failure isolation between modules; timeouts, retries, circuit breakers at integration points; graceful degradation paths.
- **Evolvability**: Seams for change at the points the project says will change. Are the modules likely to change together actually together?
- **Observability**: Consistent logging, tracing, metrics — established at module boundaries, not bolted on per-call.
- **Security boundaries**: Trust zones (untrusted input vs internal); auth checks at the edge; sensitive data minimized in transit between modules.
- **Performance architecture**: Hot paths identified; expensive work on async boundaries; N+1 risks at module integration points.

(Specific deep dives belong to `review-security` and `review-perf` — here, look for **structural support or lack of support**, not specific bugs.)

### 5. Cross-Cutting Concerns

- **Auth/authz**: Enforced at one consistent layer, not duplicated/skipped per feature.
- **Error handling**: A coherent strategy across modules (e.g., domain errors → application layer translates → transport layer serializes), not ad-hoc per file.
- **Configuration**: Centralized loading and typing; not scattered `process.env` reads.
- **Logging/tracing**: Established once, used uniformly; correlation IDs flow across module boundaries.
- **Validation**: At trust boundaries, not sprinkled throughout the domain.

### 6. Conventions, Decisions & Debt

- **Alignment with documented architecture**: `CLAUDE.md`, `docs/`, ADRs. Flag deviations *and* note when documentation is stale relative to the code.
- **Decisions without rationale**: A surprising structural choice with no ADR or comment explaining why — flag for documentation, not necessarily for change.
- **Architectural debt**: Workarounds, "temporary" shims, suppressed lint at module boundaries, comments like "TODO: split this module".
- **Evolution path**: Is there a credible way to grow this architecture for the next 6-12 months without a rewrite? If the answer requires "and then we rewrite X", flag it.

## Architectural Smells (quick reference)

| Smell | Signal | Severity heuristic |
|-------|--------|--------------------|
| Circular module dependency | A → B → A | Critical |
| Layer inversion | Lower layer imports from higher | Critical |
| God module | Imported by ~everything, imports ~everything | High |
| Modular mirage | Split folders + shared mutable state / singleton manager | High |
| Leaky abstraction | Interface exposes implementation type | High |
| Anemic domain | Logic in services, models are data bags | High (depending on stated style) |
| Distributed monolith | Services must deploy together | Critical (if microservices claimed) |
| Shotgun surgery axis | One change touches many modules | High |
| Manager centralization | One module orchestrates, others are passive | Medium-High |
| Hidden coupling | Modules sync via shared DB table / global state instead of API | High |

## Output Format

```markdown
## Architecture Review: {scope}

### Summary
{1-3 sentences: dominant pattern, biggest risk, overall health}

### Critical (structural defects, scaling/safety blockers)
- {module or file:line} - {category}: {description}
  **Impact:** {what breaks or becomes risky}
  **Fix:** {direction — not necessarily a full design}

### High Priority (maintainability / evolvability)
- {module} - {category}: {description}
  **Fix:** {direction}

### Medium Priority (consistency / cognitive load)
- {module} - {description}

### Suggestions
- {improvement opportunity}

### Documentation Gaps
- {decisions that lack an ADR or comment explaining why}
```

If `--multi` was used, append:

```markdown
### External Opinions

Add one subsection per advisor that responded, titled with the advisor's name as reported by `second-opinion`:

#### {advisor name}
{that advisor's review}

#### Cross-Model Agreement
{areas where the external advisors agree/disagree with the Claude review — consensus issues (flagged by multiple models) get higher confidence}
```

## Examples

**Staged change introduces a layering violation:**
> /review-architecture --staged

A new file in `src/ui/` directly imports `db/connection.ts`. The review reads the surrounding module, sees that all other UI code goes through `services/`, and reports a Critical layer-inversion issue with the fix to route the call through the existing service.

**Full audit finds a god module:**
> /review-architecture --all

Parallel agents per category. Finds `lib/utils.ts` imported by 80+ files and itself importing from auth, db, and HTTP layers. Reports as High with a split plan along the axes that callers actually use.

**Cross-model architecture review on a contested refactor:**
> /review-architecture --multi --staged

Runs the 6-category review plus the external advisors. Cross-model agreement highlights that multiple reviewers flag the same circular dependency between `orders` and `billing`, raising confidence.

## Troubleshooting

### Review reports "no architectural impact" on a real change
**Solution:** The diff may be leaf-level but introduce a coupling not visible from the file alone. Re-run with a wider lens — read the parent module's imports and exports, and ask whether this change shifts where data flows or who owns what.

### Findings overlap with `review-cleancode` or `review-interfaces`
**Solution:** Architecture findings should be about **relationships between modules**. If a finding is fully describable inside a single class or function, it belongs in `review-cleancode`. If it's about a single interface's signature, it belongs in `review-interfaces`. Drop the overlap.

### Disagreement on the "right" pattern
**Solution:** Pattern choice is a project decision, not a universal one. If `CLAUDE.md`/`docs/` document the intended pattern, judge against that. If not, flag the absence of a documented decision rather than imposing one.

### `--all` is too slow on a large codebase
**Solution:** Restrict scope to a top-level module: `/review-architecture src/orders/` or similar. Architecture review is most valuable per bounded context, not whole-repo at once.

## Notes

- Always read project documentation (`CLAUDE.md`, `docs/`, ADRs) before flagging deviations as violations.
- Prefer **describing the structure first**, then judging it. A finding without a stated structural fact is hand-waving.
- Architectural fixes are usually larger than code-review fixes. The output should give a *direction*, not a fully-designed solution.
- For `--all`, parallelize one agent per category (6 agents).
- A single change rarely warrants full architectural rework; recommend the smallest fix that restores the property, plus a follow-up if needed.
