---
name: repo-foundation
description: Build software products on a clean, minimal foundation, develop new features or bug fixes, and adapt architecture as requirements evolve. Use when initializing a new codebase, adding features to an existing repository, or refactoring architectural boundaries and contracts.
---

# Repo Foundation

Build software products with an explicit, just-enough foundation, develop features on top of that foundation, and adapt it when requirements change.

Optimize for total effort: achieve changes that are correct, testable, and maintainable with minimal rework, review overhead, and coordination cost. Prompt length is only one factor.

## Core Principles (Apply Across All Modes)

- **No universal dogma:** Do not enforce a single architecture, language, error-handling pattern, directory structure, or style. Match complexity to current requirements and system boundaries, not to an enterprise ideal.
- **Scope, baseline, and user work:**
  - Establish a baseline before mutating code: use the pre-existing revision/commit when Git exists; use a file inventory or snapshot when uninitialized or greenfield.
  - In a dirty workspace, protect pre-existing uncommitted user modifications. You may edit distinct, relevant parts of the same file as long as user work is preserved. Only stop and ask if there is an actual collision or ambiguous intent.
  - Never create commits or force Git initialization solely for handoff or tracking.
- **Conventions and precedents:** Reuse conventions only with healthy repository precedent. Do not treat weak or accidental patterns as precedent, and do not expand tasks into out-of-scope cleanup.
- **Prose, naming, and restraint:**
  - Names reflect business domain concepts and ownership.
  - Add comments only for information code cannot express: grounded rationale, non-obvious invariants, units, rounding, ordering, protocol quirks, or compatibility.
  - Do not narrate syntax; do not invent tickets, incidents, owners, or production histories; do not delete useful comments to "look less AI"; do not enforce word blacklists or comment ratios.
  - Do not add abstractions, wrappers, or factory layers without concrete ownership, contract, or test seam needs.
- **Verification rigor:**
  - Record baseline failures and distinguish: (1) pre-existing failures outside scope, (2) in-scope failures to fix (e.g., a bugfix starting with a failing test), (3) regressions from current changes, and (4) environment errors.
  - Do not require all pre-existing checks to pass before starting work; do not fix out-of-scope errors to make the baseline green.
  - Verify the final code state; never use pre-cleanup test results to certify modified code.
- **No speculative authority:** Do not assume permission to push, publish, deploy, modify branch protection, install system-wide hooks, or purchase external services.

## Mode Selection

| Mode | Trigger | Core Actions | Exit Criteria |
|---|---|---|---|
| **Bootstrap** | New repository from scratch or an area lacking minimal foundation (no build/test/run commands, conventions, or boundaries). | Elicit critical constraints, choose just-enough design, set up minimal tooling/checks, implement and verify the first representative slice. Read [bootstrap](references/bootstrap.md). | Representative slice works and is verified; run/build commands are documented; repo is stable for subsequent work. |
| **Continue** | Adding a feature, bugfix, or improvement on an existing, fitting foundation. | Determine owning domain and boundary, implement changes, run proportionate checks, and review diff. Executable directly from core. | Task requirements are met; diff is reviewed; intentional contract changes are verified (or existing contracts preserved); remaining limitations are stated. |
| **Evolve** | New requirements alter core contracts, ownership, boundaries, or architecture; or adopting a repo with conflicting conventions. | Assess blast radius, execute controlled migration, update evidence, tests, and documentation. Read [evolution](references/evolution.md). | Transition is verified; new contracts are operational; instructions and documentation align with code. |

Adopting an existing repository begins with mode selection; do not default to re-bootstrapping. If the repository already has working instructions, tooling, and conventions, reuse them. If a specific subsystem lacks a foundation, establish only what that subsystem requires.

---

## Continue Workflow (Core)

Execute routine feature development and bug fixes on an existing foundation directly from core instructions:

### 1. Scope and Baseline
Confirm the user's objective, observable consequences, affected boundaries, baseline revision/inventory, and any uncommitted user changes to preserve.

### 2. Implement Just Enough
- **Assumptions vs. product decisions:** Choose conventional, reversible defaults (directory layout, helper naming, standard library choices) autonomously. Bundle and ask product/architectural decisions (external dependencies, data schema changes, new auth schemes) before making breaking changes.
- **Intentional contract changes:** When a task explicitly requires changing a contract, verify that callers and tests reflect the new contract rather than forcing deprecated behavior.

### 3. Verify Proportionately
- **Lightweight path (Low risk):** For routine bug fixes, typos, formatting, or localized edits within established boundaries, keep scope tight, run relevant mechanical checks (syntax, linter, affected unit tests), and skip secondary review passes.
- **High-risk vigilance:** Single-line changes to authorization, permissions, data migrations, cryptography, persistence lifecycles, or concurrency carry critical risk. Read [verification](references/verification.md) when designing checks for critical boundaries.

### 4. Continuity and State
- **Implementation vs. requirements:** Existing code shows current behavior, not proof of meeting requirements. Passing tests do not guarantee completeness if acceptance requirements were omitted.
- **Reconciliation:** When task notes and code conflict, cross-check requirements and tests; do not default to editing notes to rubber-stamp code. If resuming across sessions or taking over a repo, read [continuity](references/continuity.md).
- **Tracking:** Reuse existing repository mechanisms (issue trackers, project notes). Do not create dedicated handoff files for routine features.

---

## Companion Coordination (`repo-native-refactor`)

- **Complementary roles:** Foundation builds, implements, and adapts; Refactor audits, tightens prose, removes residue, and aligns conventions within scope. Foundation does not reimplement refactor's taxonomy or risk bands; Refactor does not revert intentional, requested behavioral changes.
- **Discovery and fallback:** Locate companion through host-supported discovery only; do not hardcode paths, download, or assume mentioning the name triggers execution. Foundation operates fully without companion (report companion not used). Same-agent self-review is not independent review.
- **Invocation timing:** Invoke refactor at meaningful checkpoints (completed feature, bootstrap slice, architectural evolution, or explicit audit request). Do not invoke after minor edits or lightweight fixes.
- **Minimal handoff contract:** Transfer objective/scope/intentional changes, baseline & user changes, contracts & precedents, check status & limitations from existing context without creating handoff files.
- **Post-cleanup and loop limits:** Rerun affected checks on final code state after refactor edits. Perform at most one refactor pass per checkpoint by default; iterate only on concrete findings or failing checks. If a product decision is missing, ask the user; do not guess or unilaterally redesign.

---

## Reference Routing

Read supporting references only when the corresponding trigger occurs:

- **[references/bootstrap.md](references/bootstrap.md):** Read in **Bootstrap mode** to establish a new repository, set up minimal tooling, and build the first representative slice.
- **[references/evolution.md](references/evolution.md):** Read in **Evolve mode** to assess blast radius, handle breaking contract changes, or reconcile conflicting conventions.
- **[references/continuity.md](references/continuity.md):** Read when resuming work across sessions, taking over a repository, or reconciling stale notes with code reality.
- **[references/verification.md](references/verification.md):** Read when designing checks for greenfield code, high-risk boundaries (auth, data loss, concurrency), or weak test suites.
