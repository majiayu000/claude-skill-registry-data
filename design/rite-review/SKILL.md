---
name: rite-review
description: Review polished feature diff for correctness, readability, architecture, security, tests proving acceptance, Critical/Important findings, and quality dimensions before seal.
argument-hint: "[scope: slice N | feature] [--full]"
user-invocable: true
---

<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/standards/code-navigation.md","devrites-lib/reference/standards/code-index.md","devrites-lib/reference/candidate-integrity.md","devrites-lib/reference/orchestration-profiles.md","devrites-lib/reference/parallel-dispatch.md","devrites-lib/reference/standards/agents.md","devrites-lib/reference/standards/tooling.md","rite-review/reference/feature-scoped-review.md","rite-review/reference/five-axis-review.md","rite-review/reference/anti-patterns.md"],"triggers":{"applicability":["devrites-lib/reference/standards/repository-topology.md","devrites-lib/reference/standards/data-integrity.md","devrites-lib/reference/standards/integration-reliability.md"],"code-review":["devrites-lib/reference/standards/code-review.md","devrites-lib/reference/standards/review-checklist.md","devrites-lib/reference/standards/review/README.md","devrites-lib/reference/standards/duplicate-code.md"],"performance":["devrites-lib/reference/standards/performance.md","rite-review/reference/performance-review.md","rite-review/reference/performance-checklist.md"],"principles":["devrites-lib/reference/standards/principles.md"],"security":["devrites-lib/reference/standards/security.md","devrites-lib/reference/standards/security-checklist.md","rite-review/reference/security-review.md"],"testing":["devrites-lib/reference/standards/testing.md"],"ui":["rite-review/reference/nielsen-heuristics.md","rite-review/reference/cognitive-load.md","rite-review/reference/performance-checklist.md"],"workflow-artifacts":["devrites-lib/reference/workspace-artifact-schema.md"]},"workspace":["brief.md","spec.md","state.md","decisions.md","assumptions.md","questions.md","decision-coverage.md","architecture.md","plan.md","tasks.md","traceability.md","eng-review.md","test-plan.md","gates.md","evidence.md","touched-files.md","design-brief.md","browser-evidence.md"],"workspaceByRole":{"code-reviewer":["spec.md","plan.md","tasks.md","test-plan.md","architecture.md","decisions.md","state.md","evidence.md","touched-files.md"],"devex-reviewer":["spec.md","plan.md","tasks.md","state.md","touched-files.md","evidence.md"],"doubt-reviewer":["spec.md","plan.md","tasks.md","state.md","decisions.md"],"frontend-reviewer":["spec.md","plan.md","tasks.md","state.md","touched-files.md","evidence.md","design-brief.md"],"performance-reviewer":["spec.md","plan.md","tasks.md","state.md","touched-files.md","evidence.md"],"plan-reviewer":["spec.md","plan.md","tasks.md","test-plan.md","decision-coverage.md","architecture.md","state.md"],"security-auditor":["spec.md","plan.md","tasks.md","state.md","touched-files.md","evidence.md"],"simplifier-reviewer":["spec.md","plan.md","tasks.md","state.md","touched-files.md"],"spec-reviewer":["brief.md","spec.md","decision-coverage.md","questions.md","decisions.md","assumptions.md","state.md"],"test-analyst":["spec.md","tasks.md","test-plan.md","state.md","evidence.md"]},"rootOnly":["devrites-lib/reference/standards/code-index.md","devrites-lib/reference/standards/tooling.md","devrites-lib/reference/orchestration-profiles.md","devrites-lib/reference/parallel-dispatch.md"]} -->
> Read-set manifest: `devrites-engine context <slug> --phase review` bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.


# /rite-review: feature-scoped review

Review the **active feature scope only**. **Read the active workspace first**; if none,
tell the user to run `/rite-spec <feature>`.

> **Scope:** `/code-review` is a generic diff review with no workspace context.
> `/rite-review` reads
> `.devrites/work/<slug>/spec.md` first, runs Spec ↔ Code-review axes as
> parallel fresh-context reviewers (see [`parallel-dispatch.md`](../devrites-lib/reference/parallel-dispatch.md)), and gates feeding
> into `/rite-seal`. Use `/code-review` for a one-off diff; use
> `/rite-review` for a DevRites feature where the spec is the contract. Use the shared depth rules in
[`devrites-lib/reference/orchestration-profiles.md`](../devrites-lib/reference/orchestration-profiles.md);
all workflow-named roles remain mandatory at every depth.

## Rules consulted (read on demand from `.claude/skills/devrites-lib/reference/standards/`)

Pull these via `Read` when the diff demands them:

- [`code-review.md`](../devrites-lib/reference/standards/code-review.md): small PRs, severity labels, tests-first review focus.
- [`review-checklist.md`](../devrites-lib/reference/standards/review-checklist.md): compact pass/fail sweep before reporting the verdict.
- [`principles.md`](../devrites-lib/reference/standards/principles.md): declared project invariants (`.devrites/principles.md`); a diff that violates one with no recorded exception is a Critical, blocking finding.
- [`testing.md`](../devrites-lib/reference/standards/testing.md): confirm that passing tests actually prove the spec.
- [`agents.md`](../devrites-lib/reference/standards/agents.md): when to fan out to which review subagent.
- [`security.md`](../devrites-lib/reference/standards/security.md): when input / auth / data / integrations / secrets are in scope.
- [`security-checklist.md`](../devrites-lib/reference/standards/security-checklist.md): for the same security-sensitive scope, the compact trust-boundary sweep.
- [`repository-topology.md`](../devrites-lib/reference/standards/repository-topology.md), [`data-integrity.md`](../devrites-lib/reference/standards/data-integrity.md), [`integration-reliability.md`](../devrites-lib/reference/standards/integration-reliability.md): only
  when the spec applicability map or final diff triggers their ownership/failure/proof checks.
- [`performance.md`](../devrites-lib/reference/standards/performance.md): only when perf is relevant or a regression risk is visible.

## Operating rules

- **Feature scope only** — see
  [feature-scoped-review](reference/feature-scoped-review.md). Spec Drift Guard applies.
- **Silent-failure hunt:** when the suite is green, require proof that error paths and
  partial-success branches would fail tests if broken. **Failing case:** tests pass but
  handler returns success on internal error → Critical until an asserting test exists.
- **Review the finished product.** `/rite-polish` has already simplified code and
  normalized or polished UI. If review finds a remaining complexity issue, record it as
  a finding rather than rerunning a simplification pass.
- Follow the shared
  [`candidate-integrity.md`](../devrites-lib/reference/candidate-integrity.md).
  Review starts only from the digest Polish closed.
- Findings are labeled (below). Re-prove after any accepted correction.
- **Reviewers judge; root reconciles; wright fixes.** Per
  [`agents.md`](../devrites-lib/reference/standards/agents.md), root directly
  reconciles verdicts/writes artifacts; engines do not. Accepted corrections
  route to `devrites-slice-wright`.

## Workflow

0. Read `.claude/skills/devrites-lib/reference/standards/core.md` first (the always-on operating rules); pull the
   on-demand rules above as the diff demands them.
1. Read `spec.md`, `tasks.md`, `state.md`, `decisions.md`,
   `touched-files.md`, `.devrites/principles.md` (if present: the binding invariants to score
   the diff against), and the `git diff`. For "what would this change break"
   questions, apply `.claude/skills/devrites-lib/reference/standards/code-navigation.md`:
   `detect_changes` (explicit `base_branch`, `scope: "impact"`), then `trace_path` on the
   symbols that matter, before falling back to LSP/file search. When a finding hinges on an external library's
   current API, context7 if available can confirm the signature. Run
   `devrites-engine check candidate <slug>` and require its digest to match the
   single `evidence.md` binding and the `browser-evidence.md` binding when that
   file exists. Read those ledgers via the bounded advisory read
   ([`workspace-artifact-schema.md`](../devrites-lib/reference/workspace-artifact-schema.md) § Read next by phase; trigger `workflow-artifacts`): binding line, `EVID-###`
   index, then bodies for this candidate's AC/slice IDs only. A missing,
   malformed, or open candidate returns to Polish/Prove.
   Read `touched-files.md` `## Review trail` and `eng-review.md` `## Deferred findings`:
   every deferred row is an input finding for the step-3 cohort (quoted in the owning
   reviewer's brief without severity) and ends in `review.md` with its own label and
   action tag — never silently dropped. Hand each lane reviewer the
   `devrites-engine recall --paths <its touched paths>` pointers as prior context, not findings.
2. **Review tests first** while the step-3 cohort runs — launch it first; this
   root pass needs none of its output: do they prove the acceptance criteria? Missing,
   weak, or wrong tests are the first findings.
   **Completion:** every acceptance criterion maps to a proven test or a labeled finding.
3. **Review spec and code separately in parallel.** A change can pass
   one axis and fail the other: code that follows every project standard but
   implements the wrong thing (Code-review pass, Spec fail), or code that does exactly
   what the spec asked but breaks project conventions (Spec pass, Code-review fail).
   Separate contexts prevent one axis from masking the other. This is the initial
   full pass; a correction uses step 7's bounded recheck:
   - Freeze that closed digest: write the candidate diff (feature base to HEAD, plus any
     uncommitted candidate change) to `packets/<wave>.diff` and name that file in the
     packet. `dispatch open` refuses a Review or Seal reviewer wave whose packet names
     no existing diff, or whose manifest omits a path the feature's `WIP(<slug>):`
     checkpoints changed.
     Give the same digest and diff to the **two** axis reviewers (three when
     [engineering lanes](../devrites-lib/reference/parallel-dispatch.md) split the code axis) in
     parallel, each with its own narrow brief and no
     cross-pollination — and evaluate the frontend (step 4), security (step 5),
     and performance (step 6) dispatch conditions from this same diff now,
     joining the cohort when applicable rather than dispatching later waves:
     - **Spec axis** → `devrites-spec-reviewer`: "Apply your documented discipline on
       the active feature workspace + diff. Report (a) criteria the spec asked for that
       are missing or partial, (b) behaviour in the diff the spec did not ask for
       (scope creep / drift), (c) criteria implemented incorrectly. Quote the spec
       line per finding. If the spec is missing or unreadable, report `Review gap:
       missing spec` and do not infer requirements from the diff."
     - **Seal roles** → `devrites-test-analyst`, plus `devrites-doubt-reviewer` per
       stood decision and `devrites-devex-reviewer` when triggered, join this cohort on
       the same digest. Their findings join step 7's single correction, and Seal cites
       their unchanged same-candidate accounts instead of re-dispatching them.
     - **Code-review axis** → `devrites-code-reviewer`: "Apply your full documented
       discipline (tests-first, correctness, readability, architecture, maintainability,
       standards) on the feature workspace + diff. Cite file:line; skip tooling-enforced
       checks. Apply canonical anti-slop and silent-failure lenses; inspect each hunk
       for unrequested deletion. Unexcepted `.devrites/principles.md` violations are
       Critical. Distinguish binding standards from judgment-only baseline smells."
       Route it through [parallel-dispatch.md § Engineering lanes](../devrites-lib/reference/parallel-dispatch.md#engineering-lanes):
       a frontend+backend diff gets two lane reviewers in this cohort.
   - **Do NOT merge or re-rank** their findings. Present them under separate
     `## Spec` and `## Code review` sub-sections in `review.md`. Surface contradictions
     between the axes explicitly (e.g. "Spec axis says complete, Code-review axis says
     untestable"): `/rite-seal` decides what blocks. Preserve each reviewer's
     `Outcome:` and admit its account through
     [[`agents.md`](../devrites-lib/reference/standards/agents.md) § Result admission](../devrites-lib/reference/standards/agents.md#result-admission).
     Either `Outcome: gap` stops Review; silence, failure, or malformed output never
     becomes an empty findings list.
4. **Reconcile, don't re-review.** With the two parallel reports in hand, the inline
   lead reconciles. It does **not** re-run the code-review axes over correctness /
   readability / architecture / maintainability that `devrites-code-reviewer` already
   covered. Stay in scope ([feature-scoped-review](reference/feature-scoped-review.md)).
   Add only what the dispatched agents could not, then resolve overlaps and
   contradictions before labeling. ([five-axis-review.md](reference/five-axis-review.md)
   documents the axes the code-review agent applies.)
   - **UI feature?** `devrites-frontend-reviewer` joins the step-3 cohort; apply the **UX rubric**
     ([nielsen-heuristics](reference/nielsen-heuristics.md)) and the
     **cognitive-load lens** ([cognitive-load](reference/cognitive-load.md),
     [performance-checklist](reference/performance-checklist.md)). No UI/route/style
     paths: record `Not-applicable: no relevant paths in diff`.
5. **Security:** `devrites-security-auditor`
   ([security-review](reference/security-review.md)) joins the step-3 cohort when
   input, auth, data,
   secrets, or permissions are in the diff; else `Not-applicable: no relevant paths in diff`.
6. **Performance:** `devrites-performance-reviewer`
   ([performance-review](reference/performance-review.md),
   [performance-checklist](reference/performance-checklist.md)) joins the step-3 cohort
   only on a budget or
   hot path; else `Not-applicable: no relevant paths in diff`.
7. Reconcile and accept only in-scope fixes. Consolidate them into one bounded
   wright correction; never edit source in the reviewing context. Any correction
   updates the candidate manifest, returns through affected Prove, and then starts
   a fresh Review binding on the new digest. Dispatch affected exact reviewers on
   all their open findings and the dependency/regression closure under
   [evidence validity](../devrites-lib/reference/candidate-integrity.md#evidence-validity).
   Cite unchanged sub-scope coverage only with its original identity and explicit
   justification; never relabel old accounts. Changed contracts or uncertain impact
   require the full applicable pass.
8. The root updates `review.md` and `state.md`, writing exactly one candidate
   binding in `review.md` for the current digest, distinguishing fresh accounts from
   cited unchanged sub-scope evidence and reconciling complete coverage.
   **Completion:** the records name the reviewed candidate identity and every accepted
   correction has affected proof plus a fresh Review. Then checkpoint remaining
   candidate diffs per [`checkpoint.md`](../rite-build/reference/checkpoint.md);
   a wright correction does not commit on control until that Review is green.

## Finding labels

- **Critical:** must fix before seal (correctness/security/data loss).
- **Important:** should fix before seal (likely bug, real maintainability risk).
- **Suggestion:** worth doing, not blocking.
- **Nit:** trivial/style.
- **FYI:** context, no action implied.

**Action tag (separate from severity).** Tag each finding with how to act on it:
`blocking` (fix before seal), `non-blocking` (fix when convenient), or `if-minor` (fix only if the
change is already small: a pure noise-economics lever). Every Critical is `blocking` and gates the
seal; `non-blocking` / `if-minor` findings are recorded, not a stop.

## Confidence and severity

Apply [[`agents.md`](../devrites-lib/reference/standards/agents.md) § Result admission](../devrites-lib/reference/standards/agents.md#result-admission).
Roll trivia into one line. `/rite-seal` gates on `Critical == 0`,
`Important == 0` (y/N override), acceptance, and drift. No composite score.

> **Mid-flight discipline.** When tempted to demote a Critical, hide a finding, fix without re-verification, or wander out of scope: see [`anti-patterns`](reference/anti-patterns.md). Load it the moment you reach for the excuse.

## Output → `review.md`

Write the detailed review to `review.md`.
