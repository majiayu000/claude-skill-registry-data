---
name: bmad-fr-nfr-review-gate
description: Run a BMAD spec-driven post-implementation review gate that blocks completion until every requirement row scores 5/5 and the gate reports zero new findings. Use when a GitHub PR, feature, bugfix, or task implemented against BMAD specs needs verification of every FR/NFR, pinned NFR catalog category, expanded quality dimension, system quality attribute, positive/negative/edge test case, automated test and CI coverage expectation, flaky-test risk, whole-codebase impact surface, manual test expectation, QA best practice, GitHub review and requested-changes state, and CI check before completion.
---

# BMAD FR/NFR Review Gate

Use this skill after implementation when a PR, feature, bugfix, or task has
BMAD specs under `specs/`. The gate checks whether the implementation
corresponds to every functional and non-functional requirement, verifies
expanded quality dimensions, every pinned system quality attribute, generated
positive/negative/edge test cases, automated test and CI coverage, flaky-test
risk, and related whole-codebase impact, then blocks completion until all
applicable rows score 5/5 and the gate run reports zero new findings.

## Profile keys consumed

- `make.fr_nfr_gate`
- `make.ci`
- `make.tests`
- `make.e2e`
- `make.infection`
- `make.load_tests`
- `make.deptrac`
- `make.pr_comments`
- `make.post_review_findings`
- `quality.phpinsights.complexity`
- `quality.infection_msi`
- `capabilities.load_testing`
- `capabilities.publish_pr_comments`
- `ci.required_checks`
- `review.request_changes_blocking`

## Gate runner resolution

The gate invocation is resolved from the profile `make` map:

- `make.fr_nfr_gate` non-null: run the mapped target — the repository ships
  its own gate wrapper, which may accept richer toggles (publishing
  suppression, autonomous commit-and-push remediation, iteration caps).
- `make.fr_nfr_gate: null` (the shipped default): use the plugin script.
  Never assume a repo-local make target exists:

  ```bash
  "${CLAUDE_PLUGIN_ROOT}/scripts/fr-nfr-gate.sh" --spec-path "specs/<slug>" --impact-context "<one-line change summary>"
  ```

## Inputs

- BMAD spec bundle or file: `--spec-path specs/<slug>` (default `specs/`).
- Impact context: `--impact-context` carries a one-line change summary plus
  graph/relationship conclusions (see below) and, when manual testing was
  performed, a pointer to the manual-evidence file.
- Manual evidence: a markdown file the reviewer writes and cites in scorecard
  rows. The shipped script does not ingest it directly — summarize its
  conclusions in `--impact-context` and cite the file path in the report.
- Publishing behavior (shipped script): always posts the
  `BMAD FR/NFR Review Gate` commit status for the PR HEAD; posts a PR comment
  carrying the findings only when the finding count is above zero — success
  stays comment-quiet, the status check is the durable signal. Exit 0 means
  zero new findings; findings, malformed output, or transport failure after
  one retry exit 1 with a failure status.
- A repo wrapper mapped via `make.fr_nfr_gate` may expose extra inputs:

```bash # profile-example
# Upstream reference wrapper invocation with its env-var contract:
BMAD_REVIEW_SPEC_PATH=specs/my-bundle \
BMAD_REVIEW_MANUAL_EVIDENCE=var/manual-test-evidence/<task>.md \
BMAD_REVIEW_AUTO_PUSH=true \
make bmad-fr-nfr-review-gate
```

## Pinned NFR Catalog

The gate uses these NonFunctionals.com catalog categories:

- Performance
- Usability
- Maintainability
- Availability
- Interoperability
- Security
- Manageability
- Automatability
- Dependability

Do not add, remove, or rename categories during a review unless the skill is
being intentionally updated.

## Expanded Quality And Impact

The gate also requires an Expanded Quality Scorecard covering:

- Functional Suitability
- Performance Resource Sustainability
- Compatibility Coexistence
- Interaction Capability Accessibility
- Reliability Resilience
- Security Privacy Accountability
- Maintainability Testability
- Flexibility Portability
- Safety Harm Prevention
- Data Quality Integrity
- Operational Excellence Releaseability
- Observability Diagnosability
- Supply-Chain Integrity
- Compliance Governance
- Sustainability Resource Impact
- AI Automation Governance

It also requires a System Quality Attributes Scorecard covering every current
attribute from
<https://en.wikipedia.org/wiki/List_of_system_quality_attributes>.
Each attribute must have a scored row with evidence, source, status, and an
improvement recommendation. If an improvement, metric, guardrail, test, CI
check, or operational control is missing, the row fails and the report must
include a Required Fix.

The Whole-Codebase Impact Analysis must cover changed and related surfaces:
runtime paths, architecture/layer boundaries, domain model, persistence,
public API/schema, async events/queues, config/env, dependencies/lockfiles,
CI/workflows, tests/fixtures, docs, operations/observability,
security/privacy, and backward compatibility.

Graph/relationship evidence is required for whole-codebase impact scoring.
Supply it as impact context from the layer-dependency graph (the target mapped
by `make.deptrac`), codebase-memory MCP, CodeQL, SCIP, or similar tools. If no
context is supplied, build a bounded local graph/relationship context from
changed files and direct symbol references; the reviewer still has to inspect
related code rather than relying only on changed files. Every NFR catalog row,
expanded quality row, and system quality attribute row must cite
graph/relationship evidence, or give a concrete source-backed reason why graph
evidence is irrelevant for that row.

## Repository Architecture And Design-Smell Gate

The gate must explicitly apply the sibling
[code-organization](../code-organization/SKILL.md),
[implementing-ddd-architecture](../implementing-ddd-architecture/SKILL.md),
[deptrac-fixer](../deptrac-fixer/SKILL.md), and
[complexity-management](../complexity-management/SKILL.md) rules before
assigning 5/5 to Maintainability, Maintainability Testability, Modularity,
Simplicity, Testability, Data Quality Integrity, Dependability, or
Architecture and layer-boundary impact rows.

Concrete changed-code blockers include:

- constructor default instantiation of collaborators, nullable service
  collaborators with fallback `new` objects, optional `NullLogger` fallbacks,
  and manual internal resolver/service trees that should be injected or built by
  an explicit factory;
- class placement that violates the class-type directory model, including new
  or expanded `Service/`, `Helper/`, `Util/`, or `Manager` buckets, resolvers in
  `EventListener/`, normalizers in `Validator/`, and DTOs that own validators,
  normalizers, or environment policy;
- Application code that leaks concrete external SDK/framework construction or
  raw vendor objects through use-case ports instead of Infrastructure adapters
  behind typed Application interfaces;
- sentinel result states encoded with empty strings, booleans, or nullable
  fields without explicit invariants or named state variants;
- factories or transformers that hide persistence, event publication, I/O, or
  broad orchestration;
- callback-by-reference control flow or `assert()` used to prove business
  success state;
- widening dedicated domain collections to bare `array`, `iterable`, or
  unstructured payloads in production APIs;
- multi-aggregate persistence across separate flushes without a transaction
  boundary, durable compensation/reconciliation design, or source-backed reason
  that best-effort rollback satisfies the stated FR/NFR;
- unbounded PR load-test workflows where a bounded smoke/subset check is the
  intended PR gate, or load-test jobs without clear timeout, log, and artifact
  evidence.

If any item applies, the gate must fail and include the exact Required Fix.
A generic statement that DDD layout or maintainability "looks good" is not
enough for a 5/5 score. Remediation is always root-cause: no suppression
annotations, never edit `deptrac.yaml`, and never lower `quality.*`
thresholds — `quality.phpinsights.complexity` (canonical floor 94) and
`quality.infection_msi` (canonical floor 100) are raise-only.

## Scoring Contract

| Score | Meaning                                                          |
| ----- | ---------------------------------------------------------------- |
| 1/5   | Requirement not addressed or evidence absent                     |
| 2/5   | Partial implementation with major gaps                           |
| 3/5   | Implemented but missing tests, evidence, or important edge cases |
| 4/5   | Implemented and mostly verified with minor unresolved risk       |
| 5/5   | Fully implemented, verified, traceable, and review-ready         |

PASS requires all applicable FRs, NFRs, NFR catalog categories, expanded
quality dimensions, system quality attributes, generated test-case matrix rows,
automated test and CI coverage rows, flaky-test risk rows, whole-codebase impact
surfaces, manual-test requirements, QA checkpoints, GitHub completion checks,
and CI checks to score 5/5. It also requires review of vulnerabilities, bugs,
regressions, defects, operational problems, and data-loss/privacy/security
risks. A not-applicable row is allowed only with a concrete reason and source
evidence. Missing evidence fails closed.

## Mandatory QA Matrix

The reviewer must generate expected positive, negative, and edge/boundary/
race/timeout/error cases from every FR, NFR, acceptance criterion, story, and
quality requirement. It must map each repeatable case to automated tests and CI
checks: the suites behind `make.tests` and `make.e2e`, mutation testing behind
`make.infection`, load tests behind `make.load_tests` when
`capabilities.load_testing` is true (skip with a capability-absent note when
false), plus applicable static-analysis, security-scan, and contract/schema
checks. Manual evidence is supporting evidence only for behavior that cannot
be fully automated. Missing repeatable automated coverage, missing negative or
edge tests, unmitigated flaky-test risk, or unreviewed vulnerability/defect
risk blocks PASS.

## Workflow

1. Read the BMAD spec bundle: PRD, architecture, epics/stories, research, and
   implementation-readiness files when present.
2. Extract every FR, NFR, acceptance criterion, story requirement, and readiness
   requirement with source path evidence.
3. Confirm expected positive, negative, and edge test classes from the spec so
   missing automated coverage can be treated as a blocker.
4. Run the gate via the resolved runner (see Gate runner resolution). With the
   shipped script:

   ```bash
   "${CLAUDE_PLUGIN_ROOT}/scripts/fr-nfr-gate.sh" --spec-path "specs/<slug>" --impact-context "<one-line change summary>"
   ```

5. If manual testing is required, record evidence in a markdown file (format
   below), cite it in the scorecard rows, summarize its conclusions in the
   impact context, and rerun the gate.
6. If the gate exits non-zero (new findings), apply PR-scoped root-cause
   refactors/fixes, rerun verification, and start the next gate iteration. A
   verification failure after a passing review is treated as another fix
   iteration, not completion. Bound the loop with an explicit iteration
   counter; an unbounded loop is acceptable only when intentionally chosen.
7. Fetch and address GitHub comments via the target mapped by
   `make.pr_comments` when a PR exists; when `make.pr_comments` is `null`, use
   `${CLAUDE_PLUGIN_ROOT}/scripts/get-pr-comments.sh`.
8. Do not mark the PR/task complete until the gate exits 0, the target mapped
   by `make.ci` passes (capability-absent note when `null`), GitHub comments
   are resolved, every check listed in `ci.required_checks` is green, and —
   when `review.request_changes_blocking` is true — no requested-changes
   review remains. Human approval is not required before the gate runs or
   posts status updates.
9. For PR work, leave the final result visible on the PR through the
   `BMAD FR/NFR Review Gate` commit status (and the findings comment on FAIL).

## Publish (gated)

The gate's `BMAD FR/NFR Review Gate` commit status remains the durable success
signal; this Publish step is an additional consolidated view and does not
replace it. When `capabilities.publish_pr_comments` is `true`, project the gate
findings / per-requirement matrix to the canonical ledger JSON (schema in the
poster header) at `${SDLC_LEDGER_DIR:-.sdlc/review-ledgers}/fr-nfr.json`, then
publish ONE consolidated, idempotent PR comment via the target mapped by
`make.post_review_findings`; when that key is `null` (the shipped default), the
plugin substitutes its script:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/post-review-findings.sh" fr-nfr \
  --file "${SDLC_LEDGER_DIR:-.sdlc/review-ledgers}/fr-nfr.json" --pr "$PR"
```

The poster is idempotent (hidden `<!-- sdlc-review:fr-nfr -->` marker — it
updates its prior comment, never spams), authorized (writes only to the resolved
repo's own PR), and DEGRADES (NFR-3): `capabilities.publish_pr_comments`
false/absent, `gh` absent, no PR, an empty ledger, a mismatched base repo, or a
`gh` write failure all skip-with-note and exit 0 — publishing NEVER fails this
gate. When the flag is false/absent, skip this step with a note.

## Required PASS Markers

**The reviewing agent authors the review report** that carries these markers
— they are a contract on the report you write, not output emitted by the
shipped `fr-nfr-gate.sh`. The shipped script enforces only the mechanical
`FR_NFR_NEW_FINDINGS: <n>` contract (see the note after the marker list); it
never emits or validates any `*_SCORECARD`, `*_MIN_SCORE`, or `STATUS:` line.
So produce the marker-bearing scorecard report yourself from the scoring work
above; do not expect the script's stdout or its commit status to contain them.
(A repo wrapper mapped via `make.fr_nfr_gate` may additionally enforce these
markers on reviewer output — when one is mapped, follow its contract too.)

The review report produced for the gate must include:

```text
FR_NFR_SCORECARD: PASS
NFR_CATALOG_SCORECARD: PASS
EXPANDED_QUALITY_SCORECARD: PASS
SYSTEM_QUALITY_ATTRIBUTES_SCORECARD: PASS
WHOLE_CODEBASE_IMPACT: PASS
GRAPH_IMPACT_CONTEXT: PASS
TEST_CASE_MATRIX: PASS
AUTO_TEST_COVERAGE: PASS
FLAKY_TEST_RISK: PASS
MANUAL_TEST_EVIDENCE: PASS
QA_BEST_PRACTICES: PASS
GITHUB_COMPLETION_GATE: PASS
CI_GATE: PASS
```

A `STATUS: PASS` without these markers is a failure, and PASS also requires
`EXPANDED_QUALITY_MIN_SCORE: 5/5`, `IMPACT_ANALYSIS_MIN_SCORE: 5/5`,
`SYSTEM_QUALITY_ATTRIBUTES_MIN_SCORE: 5/5`, `TEST_CASE_COVERAGE_MIN_SCORE: 5/5`,
`AUTO_TEST_COVERAGE_MIN_SCORE: 5/5`, and `FLAKY_TEST_RISK_MIN_SCORE: 5/5`
evidence markers. The shipped script enforces a mechanical contract on top:
the gate output's mandatory last line is `FR_NFR_NEW_FINDINGS: <n>`, and only
`n = 0` exits 0 — a missing or malformed line fails closed with a failure
commit status.

## Manual Evidence Format

Manual evidence must include:

- tester
- date
- scenario
- steps
- observed result
- linked artifacts or command output when available
- related FR/NFR IDs or NFR catalog categories

Do not fabricate manual evidence. If evidence is absent, leave the gate failing
and report the exact manual action required.

## Verification

Run focused checks for this skill change:

```bash
bash -n "${CLAUDE_PLUGIN_ROOT}/scripts/fr-nfr-gate.sh"
```

For production code changes, also run the target mapped by `make.ci`.
