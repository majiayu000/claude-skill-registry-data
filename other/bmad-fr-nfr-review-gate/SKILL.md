---
name: bmad-fr-nfr-review-gate
description: Run a BMAD spec-driven post-implementation review gate for React/TypeScript frontend work that blocks completion until every requirement row scores 5/5 and the gate reports zero new findings. Use when a GitHub PR, feature, bugfix, or task implemented against BMAD specs needs verification of every FR/NFR, pinned NFR catalog category, expanded quality dimension, system quality attribute, positive/negative/edge test case, the frontend quality surface (coverage, mutation MSI, jscpd duplication, rust-code-analysis metrics, ESLint/TypeScript, dependency-cruiser boundaries), the Lighthouse desktop/mobile performance budgets, the mandatory accessibility gate (WCAG 2.2 AA), visual regression, whole-codebase impact surface, manual test evidence, GitHub review and requested-changes state, and CI check before completion.
---

# BMAD FR/NFR Review Gate

Use this skill after implementation when a PR, feature, bugfix, or task has
BMAD specs under `specs/`. The gate checks whether the React change set
corresponds to every functional and non-functional requirement, verifies the
expanded quality dimensions, every pinned system quality attribute, the
generated positive/negative/edge test cases, automated test and CI coverage,
the frontend quality surface (coverage, mutation MSI, jscpd duplication,
rust-code-analysis metrics, ESLint/TypeScript, dependency-cruiser boundaries),
the Lighthouse desktop/mobile performance budgets, the mandatory accessibility
gate (WCAG 2.2 AA), visual regression, flaky-test risk, and related
whole-codebase impact, then blocks completion until all applicable rows score
5/5 and the gate run reports zero new findings.

## Profile keys consumed

- `make.fr_nfr_gate`
- `make.ci`
- `make.lint_eslint`
- `make.lint_tsc`
- `make.lint_md`
- `make.lint_dup`
- `make.lint_metrics`
- `make.lint_deps`
- `make.test_unit_client`
- `make.test_unit_server`
- `make.test_integration`
- `make.test_e2e`
- `make.test_visual`
- `make.test_mutation`
- `make.merge_mutation_reports`
- `make.test_load`
- `make.lighthouse_desktop`
- `make.lighthouse_mobile`
- `make.a11y`
- `make.pr_comments`
- `make.post_review_findings`
- `quality.coverage_statements`
- `quality.coverage_branches`
- `quality.coverage_functions`
- `quality.coverage_lines`
- `quality.mutation_msi`
- `quality.jscpd_clones`
- `quality.eslint_errors`
- `quality.eslint_warnings`
- `quality.tsc_errors`
- `quality.markdownlint_errors`
- `quality.depcruise_violations`
- `quality.metrics_enforced`
- `quality.visual_diffs`
- `quality.lighthouse_desktop`
- `quality.lighthouse_mobile`
- `capabilities.visual_testing`
- `capabilities.lighthouse`
- `capabilities.mutation_testing`
- `capabilities.load_testing`
- `capabilities.accessibility_audit`
- `capabilities.dynamic_a11y_testing`
- `capabilities.publish_pr_comments`
- `ci.required_checks`
- `review.request_changes_blocking`

Command convention: `make <make.X>` means "run `make` with the target the
profile maps for key `make.X`". A `null` mapping means the capability is absent
in this repository — skip that lane with a capability-absent note instead of
improvising a raw host command. Generic tooling (`bun`/`pnpm`/`npm`, `git`,
`gh`) may be invoked directly when needed.

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

If the resolved runner cannot execute (script missing, `claude`/`gh` not on
PATH, no origin remote), do NOT loop: build the per-requirement matrix manually
from spec reading plus change-set inspection, mark the gate run
`SKIPPED: <reason>`, and derive the new-findings count from the matrix delta
against the prior iteration ledger. The matrix verdict still governs PASS/FAIL;
record the degrade note in the report.

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
being intentionally updated. The frontend quality surface maps onto these
categories rather than replacing them — for example the Lighthouse
desktop/mobile budgets and web-vitals score under Performance, the WCAG 2.2 AA
accessibility gate and the i18n catalogs score under Usability, the bundler /
package-manager / runtime descriptors score under Interoperability, and the
rust-code-analysis, jscpd, and dependency-cruiser gates score under
Maintainability. Each category still needs its own scored row with evidence.

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

The Whole-Codebase Impact Analysis must cover changed and related frontend
surfaces: runtime/render paths and component tree, architecture/module and
import-layer boundaries (the dependency-cruiser graph), the state model
(stores/reactive primitives), routing, the public component API (props +
`UI*` contracts) and any GraphQL queries/schema the change touches, i18n
catalogs, design tokens / theme / styling, config/env, dependencies and the
lockfile, CI/workflows, tests/fixtures and visual snapshots, docs,
operations/observability (web-vitals / RUM), security/privacy, accessibility,
and backward compatibility.

Graph/relationship evidence is required for whole-codebase impact scoring.
Supply it as impact context from the import/layer-dependency graph (the target
mapped by `make.lint_deps`), codebase-memory MCP, CodeQL, SCIP, or similar
tools. If no context is supplied, build a bounded local graph/relationship
context from changed files and direct symbol references; the reviewer still has
to inspect related code rather than relying only on changed files. Every NFR
catalog row, expanded quality row, and system quality attribute row must cite
graph/relationship evidence, or give a concrete source-backed reason why graph
evidence is irrelevant for that row.

## Frontend Quality Dimensions

Each dimension below gets its own scored row. A row reaches 5/5 only when its
mapped gate passes at or above its `quality.*` floor (or at the fixed `0`
ceiling) and the change-set evidence is traced — never asserted. The
`quality.*` values are **raise-only floors / fixed ceilings** over the shipped
defaults: a profile may tighten the bar, never relax it, and the tool config
files (`jest.config.ts`, `stryker.config.mjs`, `.jscpd.json`,
`config/metrics-policy.json`, `lighthouse/lighthouserc.*.js`,
`eslint.config.mjs`, the dependency-cruiser config) are never edited to make a
finding disappear.

| Dimension | Gate (run via) | Profile key / bound | Capability | Fix With |
| --- | --- | --- | --- | --- |
| ESLint errors / warnings | `make.lint_eslint` | `quality.eslint_errors` / `quality.eslint_warnings` (ceiling `0`) | always | [code-organization](../code-organization/SKILL.md), [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md) |
| TypeScript | `make.lint_tsc` | `quality.tsc_errors` (ceiling `0`) | always | [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md) |
| Markdown | `make.lint_md` | `quality.markdownlint_errors` (ceiling `0`) | always | [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md) |
| Duplication (jscpd) | `make.lint_dup` | `quality.jscpd_clones` (ceiling `0`) | always | [complexity-management](../complexity-management/SKILL.md) |
| Metrics (rust-code-analysis) | `make.lint_metrics` | `quality.metrics_enforced` (`true`, hard-fail gate) | always | [complexity-management](../complexity-management/SKILL.md) |
| Dependency boundaries | `make.lint_deps` | `quality.depcruise_violations` (ceiling `0`) | always | [architecture](../architecture/SKILL.md) |
| Jest coverage | `make.test_unit_client` / `make.test_unit_server` / `make.test_integration` | `quality.coverage_statements` / `quality.coverage_branches` / `quality.coverage_functions` / `quality.coverage_lines` (floor `100`) | always | [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md) |
| Mutation (Stryker MSI) | `make.test_mutation` + `make.merge_mutation_reports` | `quality.mutation_msi` (floor = `stryker.config.mjs` `break`, raise-only) | `capabilities.mutation_testing` | [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md) |
| Visual regression | `make.test_visual` | `quality.visual_diffs` (ceiling `0`) | `capabilities.visual_testing` | [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md) |
| Lighthouse desktop | `make.lighthouse_desktop` | `quality.lighthouse_desktop` (floor `95`, i.e. 0.95 minScore) | `capabilities.lighthouse` | [frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md) |
| Lighthouse mobile | `make.lighthouse_mobile` | `quality.lighthouse_mobile` (floor `85`, i.e. 0.85 minScore) | `capabilities.lighthouse` | [frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md) |
| Accessibility (WCAG 2.2 AA) | `make.a11y` | `0` findings | `capabilities.accessibility_audit` / `capabilities.dynamic_a11y_testing` | [accessibility-audit](../accessibility-audit/SKILL.md) |

Lighthouse floors are stored as integer percents (`95` desktop = 0.95 minScore,
`85` mobile = 0.85 minScore); a row passes only when the audited score sits
at or above the floor. The ESLint dimension also enforces the repository's
`no-restricted-syntax` conventions — classes-with-instance-methods (no
`static`, no free functions) outside React components, type-only files, and no
`data-testid` in `src/**`. Jest runs two environments (client `jsdom`, server
`node`) plus an integration project that enforces full coverage over
`architecture.source_root`; MSI is measured only over mutated lines, so it is a
separate, stronger signal that does not by itself guarantee the
`quality.coverage_*` floors. When a capability is false (or its `make.*` target
is `null`), record the row `SKIPPED: <capability>` with a capability-absent
note instead of failing — the bar is not weakened, the lane is declared absent.

## Mandatory Accessibility Gate (WCAG 2.2 AA)

Accessibility is non-negotiable: a PASS for the frontend change set requires the
accessibility row to clear WCAG 2.2 AA. Run the gate via the target mapped by
`make.a11y`; when that key is `null` the plugin substitutes its bundled a11y
lane (axe-core / Playwright a11y probing plus static ARIA/semantic checks). The
row covers the four POUR principles — perceivable (text alternatives, contrast,
non-text content), operable (full keyboard operability, visible focus order,
no traps), understandable (labels, error identification, predictable behavior),
and robust (correct semantic roles, accessible names, valid ARIA). Score it
from the `accessibility-auditor` agent's evidence; route fixes to the component
itself via the [accessibility-audit](../accessibility-audit/SKILL.md) skill and
the `react-implementer` agent — never with a `data-testid` or an `aria-*`
band-aid that hides the defect.

Capability skip path: the **static** a11y lane is gated by
`capabilities.accessibility_audit` and the **dynamic** live-browser probing by
`capabilities.dynamic_a11y_testing`. When `capabilities.accessibility_audit` is
false (or `make.a11y` is `null` with no bundled lane available), record
`SKIPPED: capabilities.accessibility_audit` with a capability-absent note; when
only `capabilities.dynamic_a11y_testing` is false (or `make.start` is `null`),
the dynamic probing degrades to skip-with-note while the static lane still
runs. A skip never lowers the bar — it declares the lane absent and leaves the
row unverified, which fails closed for any requirement that asserts an a11y
behavior.

## Repository Architecture And Design-Smell Review

The review must explicitly apply the sibling
[code-organization](../code-organization/SKILL.md),
[architecture](../architecture/SKILL.md), and
[complexity-management](../complexity-management/SKILL.md) rules before
assigning 5/5 to Maintainability, Maintainability Testability, Modularity,
Simplicity, Testability, Data Quality Integrity, Dependability, or
Architecture and layer-boundary impact rows.

Concrete changed-code blockers include:

- constructor default instantiation of collaborators, nullable service
  collaborators with fallback `new` objects, or manual internal service/repo
  trees that should be injected via tsyringe (`@inject` / `container.resolve`)
  or built by an explicit factory — and, conversely, pulling the DI container
  into a render-path module that the profile keeps container-free;
- `static` class members or standalone (free) functions in non-React
  `src/**/*.ts` (`export function`, default-exported functions, top-level
  arrow/function-expression `const`s) instead of instance methods on an
  injectable class; types declared in a logic file or runtime declared in a
  type-only file; a `data-testid` in `src/**` instead of a semantic query
  (`getByRole`/`getByLabelText`/`getByText`);
- component, hook, store, repository, or service placed outside the
  bulletproof-react module layout, a reusable UI component missing the
  `architecture.component_prefix` (`UI*`) prefix, or cross-feature reach via
  deep relative chains (`../../../X`) instead of a configured path alias;
- render/application code leaking a concrete transport or external SDK (Apollo
  Client, raw `fetch`) through the component instead of going through a typed
  repository/service seam;
- sentinel result states encoded with empty strings, booleans, or nullable
  fields without explicit invariants or named state variants;
- a jscpd clone introduced at or above `minTokens`/`minLines`, or a
  function/closure/component/hook/file over the rust-code-analysis policy bands
  (cyclomatic > 10, cognitive > 15, ABC > 17, args > 3, exit points > 3,
  LLOC/PLOC/SLOC and Halstead ceilings, MI < 20, class WMC/NPM/NPA/COA/CDA
  limits in `config/metrics-policy.json`);
- an unbounded PR performance/load/visual workflow where a bounded smoke/subset
  check is the intended PR gate, or a perf/load job without clear timeout, log,
  and artifact evidence.

If any item applies, the review must fail and include the exact Required Fix.
A generic statement that the module layout or maintainability "looks good" is
not enough for a 5/5 score. Remediation is always root-cause: no suppression
annotations (`eslint-disable`, `@ts-ignore`, `@ts-expect-error`,
`prettier-ignore`, `markdownlint-disable`, jscpd or dependency-cruiser ignore
directives, Stryker disable comments, `/* istanbul ignore */`), never edit the
dependency-cruiser config or `config/metrics-policy.json`, and never lower a
`quality.*` threshold — the coverage floors (`100`), `quality.mutation_msi`,
and the Lighthouse floors are raise-only; the violation-count ceilings stay at
`0`.

## Scoring Contract

| Score | Meaning                                                          |
| ----- | ---------------------------------------------------------------- |
| 1/5   | Requirement not addressed or evidence absent                     |
| 2/5   | Partial implementation with major gaps                           |
| 3/5   | Implemented but missing tests, evidence, or important edge cases |
| 4/5   | Implemented and mostly verified with minor unresolved risk       |
| 5/5   | Fully implemented, verified, traceable, and review-ready         |

PASS requires all applicable FRs, NFRs, NFR catalog categories, expanded
quality dimensions, system quality attributes, frontend quality-dimension rows,
generated test-case matrix rows, automated test and CI coverage rows,
flaky-test risk rows, whole-codebase impact surfaces, the accessibility gate,
the Lighthouse performance budgets, visual regression, manual-test
requirements, QA checkpoints, GitHub completion checks, and CI checks to score
5/5. It also requires review of vulnerabilities, bugs, regressions, defects,
operational problems, and data-loss/privacy/security risks. A not-applicable
row is allowed only with a concrete reason and source evidence. Missing
evidence fails closed.

## Mandatory QA Matrix

The reviewer must generate expected positive, negative, and edge/boundary/
race/timeout/error cases from every FR, NFR, acceptance criterion, story, and
quality requirement. It must map each repeatable case to automated tests and CI
checks:

- component/hook and Apollo-mock unit suites behind `make.test_unit_client` and
  `make.test_unit_server`, plus the interaction suite behind
  `make.test_integration`;
- user-flow E2E behind `make.test_e2e`;
- visual regression behind `make.test_visual` when `capabilities.visual_testing`
  is true (skip with a capability-absent note when false);
- mutation testing behind `make.test_mutation` + `make.merge_mutation_reports`
  when `capabilities.mutation_testing` is true (skip-with-note when false);
- Lighthouse desktop/mobile budgets behind `make.lighthouse_desktop` /
  `make.lighthouse_mobile` when `capabilities.lighthouse` is true
  (skip-with-note when false);
- the accessibility lane behind `make.a11y` when
  `capabilities.accessibility_audit` / `capabilities.dynamic_a11y_testing` is
  true (skip-with-note when false);
- load tests behind `make.test_load` when `capabilities.load_testing` is true
  (skip-with-note when false);
- plus the applicable static checks — ESLint, TypeScript, jscpd,
  rust-code-analysis, dependency-cruiser — and any contract/schema checks.

Manual evidence is supporting evidence only for behavior that cannot be fully
automated. Missing repeatable automated coverage, missing negative or edge
tests, unmitigated flaky-test risk, or unreviewed vulnerability/defect risk
blocks PASS.

## Workflow

1. Read the BMAD spec bundle: PRD, architecture, epics/stories, research, and
   implementation-readiness files when present.
2. Extract every FR, NFR, acceptance criterion, story requirement, and
   readiness requirement with source path evidence.
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
   refactors/fixes (route them to the `react-implementer` agent), rerun
   verification, and start the next gate iteration. A verification failure
   after a passing review is treated as another fix iteration, not completion.
   Bound the loop with an explicit iteration counter, **max 5 iterations**; on
   exhaustion, stop, leave the gate failing, and report the remaining findings
   and the recommended next step instead of iterating further.
7. Fetch and address GitHub comments via the target mapped by
   `make.pr_comments` when a PR exists; when `make.pr_comments` is `null`, use
   `${CLAUDE_PLUGIN_ROOT}/scripts/get-pr-comments.sh`.
8. Do not mark the PR/task complete until the gate exits 0, the target mapped
   by `make.ci` passes (capability-absent note when `null`), the frontend
   quality-dimension rows and the accessibility gate are clear, GitHub comments
   are resolved, every check listed in `ci.required_checks` is green, and —
   when `review.request_changes_blocking` is true — no requested-changes review
   remains. Human approval is not required before the gate runs or posts status
   updates.
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
updates its prior comment, never spams), authorized (writes only to the
resolved repo's own PR), and DEGRADES: `capabilities.publish_pr_comments`
false/absent, `gh` absent, no PR, an empty ledger, a mismatched base repo, or a
`gh` write failure all skip-with-note and exit 0 — publishing NEVER fails this
gate. When the flag is false/absent, skip this step with a note.

## Required PASS Markers

**The reviewing agent authors the review report** that carries these markers —
they are a contract on the report you write, not output emitted by the shipped
`fr-nfr-gate.sh`. The shipped script enforces only the mechanical
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
FRONTEND_QUALITY_DIMENSIONS: PASS
ACCESSIBILITY_GATE: PASS
PERFORMANCE_BUDGET: PASS
VISUAL_REGRESSION: PASS
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
evidence markers. A capability-gated marker (`VISUAL_REGRESSION`,
`PERFORMANCE_BUDGET`, `ACCESSIBILITY_GATE`) may read `N-A (capability absent)`
only with the explicit `SKIPPED: <capability>` note from the matching section —
never silently. The shipped script enforces a mechanical contract on top: the
gate output's mandatory last line is `FR_NFR_NEW_FINDINGS: <n>`, and only
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
