---
name: verify-impl
description: "Forensic audit of an implementation against its authoritative specification. Use whenever a specification document and an implementation are both in scope and the user asks any conformance question - even when not phrased explicitly: 'does this code match the spec', 'verify this implementation', 'check spec conformance', 'audit compliance between design and code', 'is the implementation faithful', 'verify spec coverage', 'audit against requirements', 'spec-vs-code'. Also triggers when a file path under `.specs/` is mentioned alongside an implementation. Do NOT use for general code review, specification design review before implementation begins, security review, or architecture review without a spec document. Pass both the spec and the implementation scope as arguments; the skill does not infer them from the conversation."
metadata:
  author: Serghei Iakovlev
  version: "3.1"
  category: review
---

# Spec-vs-Implementation Verification

You are conducting a forensic verification - a systematic, evidence-based comparison of implemented code against its authoritative technical specification. You answer one question: **does the implementation faithfully realize every requirement, constraint, design decision, interface contract, algorithm, and invariant defined in the specification?**

The specification is the product of deliberate architectural work. Every footnote, every constraint, every edge-case note exists because an architect determined it was necessary. A missed requirement is a latent defect; a diverged algorithm is a behavioral bug; a weakened invariant is a potential security boundary violation.

## Input

The user provides a path to a specification file (markdown). Read the spec in its entirety before classifying anything. The spec is the authoritative source of truth: if the code does not meet it, that is a failure of the implementation, not of the spec.

## Workflow

The verification proceeds in seven phases. Each phase has a documented gate that prevents a specific failure mode (false positives, recency bias, severity inflation, missed cross-cutting concerns). Do not skip, merge, or abbreviate any phase.

Copy this checklist into your response and mark items as you complete them:

- [ ] Phase 1 - Build project context
- [ ] Phase 2 - Extract every verifiable requirement
- [ ] Phase 3 - Discover the implementation surface
- [ ] Phase 4 - Verify each requirement
- [ ] Phase 5 - Cross-cutting verification
- [ ] Phase 6 - Self-verification
- [ ] Phase 7 - Verdict and remediation

### Phase 1 - Build project context

Before verifying anything, understand the system the spec lives within.

**Project documentation.** Search and read:

- Context files: `AGENTS.md`
- Project docs: `README.md`, `CONTRIBUTING.md`, plus `docs/` or `doc/` directories - especially design and ADR sets
- Build manifests: `package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`, etc. - to understand the tech stack
- Runtime model: `.env.example`, `docker-compose.yml`, `compose.yml`, `Makefile`

**Codebase structure.** List the project root and key subdirectories. Identify module boundaries, layering, dependency direction, naming conventions, package organization, and test structure.

**Review standards.** Search for project-defined review instructions (`.claude/rules/`, `REVIEW.md`, `.github/instructions/`). If found, adopt their severity classification and review dimensions over the defaults in this skill.

### Phase 2 - Extract every verifiable requirement

**Objective:** complete, numbered inventory of every obligation the spec imposes on the implementation.

Read the specification *in its entirety*, from the first line to the last. Do not skim. Do not summarize sections as "standard boilerplate" - the spec has no filler; every sentence potentially encodes a requirement.

For each requirement, record:

| Field | Content |
|---|---|
| **ID** | `R-{section}-{seq}` (e.g. `R-3.2-04`) |
| **Spec quote** | The exact text from the specification (verbatim, in quotes) |
| **Spec location** | Section number and/or line range in the spec file |
| **Category** | One of eleven - see [references/requirement-taxonomy.md](references/requirement-taxonomy.md) |
| **Criticality** | `must` (violation = defect), `should` (violation = concern), `note` (informational intent) |

For the exhaustive list of what counts as a requirement, the eleven category definitions, and edge cases that look like filler but encode requirements, read [references/requirement-taxonomy.md](references/requirement-taxonomy.md) before extracting.

**Completeness check.** After extraction, count the requirements. For a 400-line spec, expect 30–60; for an 800-line spec, 60–120. If significantly below this range, you missed requirements - re-read the spec.

Output the requirements table before proceeding to Phase 3.

### Phase 3 - Discover the implementation surface

**Objective:** identify every source file that constitutes the implementation of this specification.

1. Use the spec's file-structure section (if present) plus your own analysis to enumerate files the spec says should be created or modified.
2. Search the codebase for these files. Read each completely.
3. If the spec references interfaces or types from other modules, read those too - contract conformance requires it.
4. If a file the spec mandates does not exist, record this as a `MISSING` finding immediately.

Build a file inventory:

| File | Exists | Lines | Layer/Module | Role per spec |
|---|---|---|---|---|

### Phase 4 - Verify each requirement

**Objective:** for every requirement from Phase 2, determine whether the implementation satisfies it.

For **every single requirement** (no batching, no "the rest are fine"):

1. **Locate** the corresponding code. Quote the lines (`file:line_range`).
2. **Compare** the spec requirement against the actual implementation behavior.
3. **Classify** the result:

| Status | Meaning |
|---|---|
| `PASS` | Implementation matches the requirement |
| `DRIFT` | Implementation works but deviates in a way that changes behavior |
| `PARTIAL` | Some aspects present, others missing |
| `MISSING` | No corresponding implementation found |
| `CONFLICT` | Implementation contradicts the requirement |

4. **For non-PASS findings**, provide:
   - The exact spec quote (what was required)
   - The exact code quote (what was implemented, or "not found")
   - A precise explanation of the discrepancy
   - Severity classification per [references/severity-rubric.md](references/severity-rubric.md)

**Anti-bias protocol.** Do not rationalize discrepancies. If the spec says X and the code does Y, that is a finding - even if Y seems reasonable. The spec is the authority. If the spec is itself wrong, raise that as a separate flag - but it does not excuse the implementation divergence.

**Attention discipline.** After completing the verification pass, explicitly re-read the last 20% of the spec to counter recency bias. Check whether requirements from the middle sections were evaluated too leniently.

Output a detailed findings table with evidence.

### Phase 5 - Cross-cutting verification

**Objective:** check properties that span multiple requirements and are easy to miss in line-by-line review.

Based on the project's architecture documentation (from Phase 1), verify the cross-cutting dimensions enumerated in [references/cross-cutting-checks.md](references/cross-cutting-checks.md). The reference defines eight dimensions (dependency direction, naming consistency, lifecycle management, error handling, concurrency safety, interface compliance, security boundaries, data safety) and the conditions under which each may be skipped. Skip explicitly - silently dropping a dimension is the failure mode this phase exists to prevent.

### Phase 6 - Self-verification

**Objective:** reduce false positives by independently verifying each non-PASS finding.

For each finding from Phases 4 and 5:

1. Re-read the relevant spec section. Is your interpretation correct?
2. Re-read the relevant code. Did you miss a code path that addresses the requirement?
3. Check if the requirement is satisfied through a different file or mechanism than expected.
4. Assign a confidence score: `high` (≥ 0.9), `medium` (0.7–0.9). Drop findings below 0.7.

This phase is mandatory. Initial review findings have a 15–30% false-positive rate; self-verification cuts this significantly.

### Phase 7 - Verdict and remediation

**Review summary.** Populate the template at [assets/review-summary-template.md](assets/review-summary-template.md) with metrics, the verdict, and the key findings.

**Remediation plan.** Generate **only if** there are critical or major findings. Use the template at [assets/remediation-plan-template.md](assets/remediation-plan-template.md). Each fix must be:

- **Self-contained** - an implementer should not need to re-read the full spec to apply the fix.
- **Precise** - exact files and line numbers.
- **Ordered** - dependency order; fix type definitions before functions that use them.
- **Verifiable** - each fix has a clear "done when" condition.

## Critical reminders

- **The spec has no filler.** Every section, note, risk mitigation, and diagram encodes requirements. Treat the entire document as load-bearing.
- **Quote before judging.** Extract the exact spec text before evaluating code. Prevents drift between what you think the spec says and what it actually says.
- **Absence is a finding.** Behavior defined in the spec but not implemented is `MISSING`, not "probably handled elsewhere".
- **The spec is the authority.** A divergent implementation that "seems better" is still a defect.
- **No severity inflation.** See [references/severity-rubric.md](references/severity-rubric.md) for the rubric and worked examples.

## Output

Write the full review to a markdown file under `.reviews/`, creating the directory if it does not exist. The filename is decided in this order:

1. **Invoker-provided path.** If the invocation specifies an explicit output path (e.g. `.reviews/Review-ISSUE-42-r2.md`), use that path verbatim. Invokers carry task-specific identifiers, iteration suffixes (`-r2`, `-r3`), and ticketing conventions this skill has no visibility into. Do not second-guess.
2. **Default (no path provided).** Derive the filename from the spec path using `Review-{spec-name}.md`. If the spec filename starts with `Spec-`, strip that prefix:
   - `.specs/Spec-6.4-Worker-Attempt-Function.md` → `.reviews/Review-6.4-Worker-Attempt-Function.md`
   - `.specs/Spec-BP-138.md` → `.reviews/Review-BP-138.md`
   - `.specs/auth-service.md` → `.reviews/Review-auth-service.md`

   If the derived file already exists, append a numeric index: `.reviews/<name>-2.md`, `.reviews/<name>-3.md`, etc. Use the next available number.

After writing, print the path to the created file.
