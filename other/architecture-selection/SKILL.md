---
name: architecture-selection
description: Structured decision framework for choosing a system topology (monolith, modular monolith, microservices), carving module boundaries, classifying subdomains, and assigning an architecture recipe per module; produces or updates the Architecture Profile and a baseline ADR. Use for new projects, new modules, "which architecture should I use", re-architecture discussions, or when profile.yml is missing or in draft.
user-invocable: false
---
# Architecture Selection

Output of this skill: a `profile.yml` (or a diff) + `docs/adr/0001-architecture-baseline.md` (or a new ADR).
It never recommends a style without evidence from the forces below.

## Phase 1 — Interview (ask only what the codebase/user has not answered)
Group questions; ask at most 5 at a time.
1. **Business capabilities**: list the 5–15 things the system does, in business verbs.
2. **Rules**: which capabilities have rules that are regulated, audited, or costly when wrong?
3. **Change**: which parts change most often, and who requests the changes?
4. **Integrations**: external systems, their volatility and failure modes.
5. **Scale & ops**: users, data volume, peak loads, availability target, deployment constraints.
6. **Team**: number of developers now/in 2 years, ownership split, experience with DDD/CQRS.
7. **Lifetime**: prototype, product, or long-lived line-of-business system?
8. **Existing code**: greenfield or brownfield (then also load `architecture-migration`).

## Phase 2 — Topology (A1)
Default: **modular-monolith** for any system with ≥ 3 capabilities; **monolith** for smaller.
Choose **microservices** only if at least two hold, with evidence:
- independent deployment is required by separate teams with separate release cadence
- materially different scaling or availability profiles per capability, measured or contractual
- hard isolation requirements (security, regulatory, tenancy) that process boundaries solve
- the team already operates distributed systems (observability, messaging, CI per service)
Otherwise microservices are recorded as a rejected option with these reasons.

## Phase 3 — Boundaries (A2)
1. Group capabilities by **language** (same term, same meaning) and **change coupling** (change together).
2. Each group owns its data. If two groups must write the same table, the boundary is wrong or one
   is the owner and the other consumes via contract/event.
3. Name modules after capabilities (`Invoicing`), not entities (`InvoiceService`) or layers.
4. Classify each: **core** (differentiating, complex), **supporting** (necessary, specific),
   **generic** (commodity, often integration or off-the-shelf).
5. Check: can each module be described in one sentence without "and"? If not, split or rename.

## Phase 4 — Recipe per module
Apply the scoring in `architecture-composition` §3, then adjust:
- Core subdomain with score < 4 → re-check the rules question; core with no rules is usually misclassified.
- Generic subdomain dominated by an external system → `hexagonal-integration`.
- Reporting / exports / fiscal declarations (e.g. SAF-T) → `pure-slices` with `table-module`, read-only views.
- Team inexperienced with DDD → `sliced-domain` before `clean-sliced`; the migration path is cheap.

## Phase 5 — System-wide conventions
Decide once: endpoint placement, dispatch (default `direct`), error model (default `result`),
validation, write/read data access defaults, migrations tool, test stack. Each non-default needs one
line of reason in the ADR.

## Phase 6 — Record
1. Write `profile.yml` with `status: draft`.
2. Write the baseline ADR (skill `adr`): context = forces; decision = topology, modules table,
   recipes, conventions; consequences; rejected options.
3. List architecture tests to generate (skill `architecture-fitness-tests`).
4. Ask the user to review; set `status: active` only after approval.

## Red flags to call out explicitly
- Same recipe for every module → boundaries or scoring were skipped.
- Every module `core` → classification is aspirational, not real.
- Modules named after tables or layers.
- Microservices chosen for "scalability" without numbers.
- Clean + DDD + CQRS separate-stores on a supporting module.

See `references/decision-record-example.md` for a worked example.
