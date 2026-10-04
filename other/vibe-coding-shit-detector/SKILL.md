---
name: vibe-coding-shit-detector
description: Detect whether a vibe-coded or AI-generated software project is maintainable engineering or unmaintainable shit. Use for vibe coding audits, vibe code quality, AI codebase health, engineering health, technical debt, architecture drift, maintainability, takeover readiness, production readiness, or Vibe Slop assessments; produces an evidence-based read-only audit, not a style review or automatic remediation.
---

# Vibe Coding Shit Detector

Assess whether a project can be understood, changed, verified, operated, and recovered without relying on chat history or an original author's memory. Treat the repository and executable controls as evidence; do not grade aesthetics or tool choices.

## Operating boundary

Default to `AUDIT_ONLY`.

- Read repository files, local instructions, Git history, tests, CI, and infrastructure configuration.
- Run only safe, read-only discovery. Run existing tests only when they are already within the user's authorization and do not require installing dependencies or changing external state.
- Do not edit source or configuration, add dependencies, refactor, fix findings, change databases or infrastructure, create commits, or alter release state.
- Reports may be written only to the user-requested or clearly designated output location. Never disguise a recommendation as a completed fix.
- Treat unavailable evidence as `UNKNOWN`, never as failure. Do not expose secret values found during inspection; report only location, credential type when identifiable, and remediation urgency.

## Audit workflow

1. **Establish context.** Resolve the repository root, read applicable repository instructions, record the current branch/SHA and dirty state, and note inaccessible evidence domains.
2. **Classify before scoring.** Infer project type, lifecycle stage, criticality, and actual operating responsibility using [project-classification.md](references/project-classification.md). Label each value as user-stated, repository-inferred, or unknown. Ask only when ambiguity would materially change a gate or readiness conclusion.
3. **Discover evidence.** Inventory source, tests, docs, CI, deployment, migrations, and operations material. `scripts/repository_inventory.py` can produce a content-free inventory. Exclude generated dependencies, caches, binaries, and build artifacts.
4. **Map architecture and ownership.** Identify entry points, dependency direction, core entities, state owners, write paths, invariants, and discrepancies between documented and executable behavior. A filename or keyword is only a lead.
5. **Assess change and verification.** Map important invariants to tests or enforcement. When useful and Git history exists, run `scripts/git_change_coupling.py`. Perform both tests below without changing the repository:
   - **Repository Amnesia Test:** determine whether a capable newcomer could understand, run, verify, release, and recover the system using retained project evidence alone.
   - **Controlled Change Test:** simulate one ordinary non-destructive change; report predicted modules, boundaries crossed, unknown dependencies, available verification, and blast radius.
6. **Assess operations only from evidence.** Examine observability, security/configuration, deployment traceability, migrations, backup, rollback, replay, and recovery. Lack of access lowers confidence; it does not prove absence.
7. **Score and apply gates.** Follow [scoring-model.md](references/scoring-model.md), [evidence-model.md](references/evidence-model.md), and [critical-gates.md](references/critical-gates.md). Critical gates override averages. Explain why each maturity rating is not the adjacent rating.
8. **Recommend selectively.** Provide no more than five evidence-linked improvements. Identify one `Next Highest-Leverage Improvement` with impact, effort, and observable acceptance conditions.

## Required conclusions

Keep these conclusions separate:

- `Engineering Health` — weighted capability score from 0 to 100.
- `Vibe Slop Risk` — responsibility-to-governance mismatch from 0 to 100; never derive it as `100 - health`.
- `Evidence Confidence` — support and coverage from 0 to 100.
- `Production Readiness` — `NOT_ASSESSED`, `BLOCKED`, `CONDITIONAL`, or `READY`.

Every material claim must cite a path plus line/range, command result, commit/history observation, or explicitly missing evidence domain. Use the stable finding shape and output contract in [report-schema.md](references/report-schema.md).

## Deliverables

Unless the user asks for a different format, produce both:

- `audit-report.md`, based on [audit-report-template.md](assets/audit-report-template.md)
- `audit-result.json`, validated against [audit-result.schema.json](assets/audit-result.schema.json)

If confidence is below 40, provide findings and limitations but withhold a definitive overall verdict. If production responsibility is unknown or operational evidence is inaccessible, use `NOT_ASSESSED` rather than guessing readiness.
