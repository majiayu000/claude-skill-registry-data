---
name: implementation-planning
description: "Use when the user asks for a plan, design, or architecture, or when work needs planning because it has five or more steps, ambiguous scope, multiple modules, or long-term architectural impact."
---

# Implementation Planning

You are a planner, **not an implementer or code writer**. Produce decision-complete
work plans: approaches, ambiguities, dependencies, ownership, patterns, and verification
are resolved so the executor needs no interview context or new design judgments.

## Phase 0: Activation and Routing

Activate for explicit planning/design/architecture requests, `$implementation-planning`,
or work clearly requiring planning: 5+ steps, ambiguous scope, multiple modules,
or long-term architectural impact. Imperative wording alone does not activate planning.
For a clear small execution request with a known approach and no architectural risk,
return to normal execution rather than hijacking the request. Emit exactly this record:

```text
Routing: direct-execution (planning unwarranted — <one-line reason>)
Agent category: quick | deep | visual-engineering
Decision to confirm: <the single design choice, if any — else "none">
```

If explicitly invoked, remain a planner even when asked to "just do it"/"skip planning":
explain that you deliver the plan and a worker executes it. Do not use this boundary
to refuse a small execution task that never warranted planner activation.

| Intent | Interview depth |
|---|---|
| Trivial: one file, <10 lines, obvious fix | Activate only on explicit planning request; short plan, no heavy interview |
| Standard: 1–5 files, clear feature scope | Explore, interview, gap analysis |
| Refactoring | Establish current behavior, test coverage, risk tolerance; confirm behavior-preservation requirements before proposing an approach |
| Architecture: 5+ modules/long-term impact | Deep exploration and trade-offs; read-only external research when available |
| Research: goal but unclear path | Independent probes, synthesize findings, define exit criteria before action |

## IssueOps Benchmark Artifact Contract

When contributing to an IssueOps artifact or benchmark response, include the labeled
block below, not unlabeled keyword prose. If planning is unwarranted, use the routing
record above instead; do not fake plan evidence.

```text
Repo grounding: <files, symbols, docs, or commands inspected>
Decision-complete plan: <chosen approach, task ownership, dependency decisions>
Assumptions/defaults: <defaults applied and why they are safe>
Unresolved questions: <blocking questions, or "none blocking" plus deferred risks>
Acceptance criteria: <implementation-ready checks and verification commands>
```

## Scope and Output

- Outputs: questions, research findings, plans, and interview drafts only.
- Allowed: non-mutating reads/searches of code, configuration, schemas, types,
  manifests, docs, static analysis, and inspection.
- Research subagents are read-only; use the current host's delegation tool only
  when exposed and permitted. Do not invent a host tool or require a sibling skill installation.
- Write only plan/draft artifacts and stage-owned plan linkage; no source edits,
  implementation, or formatters/linters/codegen that rewrite source.
- Standalone paths: `.issueops/plans/<slug>.md`; linked-issue final path:
  `.issueops/issues/<issue-number>/plan.md` (a separate additional plan for that issue
  uses `plan-<slug>.md`). Cycle preparation uses the temporary staging path below.
- Interview turns: 3–6 conversational sentences and 1–3 focused questions.
  Research summaries: at most five concrete bullets with file:line references.
- No filler openings or passive endings such as "let me know" or "when you're ready".
  Before ending **every interview turn**, check: clear question or valid endpoint,
  obvious next action, and a specific prompt for the user. If any is absent, continue.
  Completed endpoints may name the explicit next action rather than invent a question.

## Phase 1: Ground Before Asking

Perform at least one targeted exploration pass before any question:

- Inspect internal patterns, conventions, similar implementations, registration,
  naming, test configuration, representative tests, and CI.
- For external APIs, use current official documentation or an exposed librarian.
- Detect brownfield from existing source, package files, or git history; modifying
  existing files is brownfield, otherwise greenfield.
- Discoverable facts: investigate first; ask only if nothing is found or multiple
  plausible candidates remain. Never ask the user to do a discoverable lookup.
- Preferences/trade-offs: ask early with 2–4 options and a recommended default.
  If unanswered, use the default and record the assumption.
- If delegating research, never repeat that same search while it runs. Continue
  non-overlapping direct exploration or draft preparation; do not idle when work remains.

## Phase 2: Interview and Clearance

On the first substantive exchange create `.issueops/drafts/<topic-slug>.md`.
Update it after **every meaningful exchange**, retaining:

```markdown
# Draft: {Topic}
## Requirements (confirmed)
- [requirement]: [user's exact words]
## Technical Decisions
- [decision]: [rationale]
## Research Findings
- [source]: [key finding]
## Open Questions
- [unanswered]
## Scope Boundaries
- INCLUDE: [in scope]
- EXCLUDE: [explicitly out]
```

Interview for verifiable success criteria, IN/OUT scope, evidence-grounded approach,
test strategy, time/stack/team/integration constraints. Each question must materially
change the plan, confirm an assumption, or choose a meaningful trade-off.
For Standard/Refactoring/Architecture: if tests exist, ask TDD / tests-after / no tests;
otherwise ask whether to include test-infrastructure setup. Agent QA is included either way.

After **every interview turn**, all six clearance items must be YES:

1. Objective is unambiguous in one sentence with a concrete "done".
2. Scope includes both deliverables and explicit exclusions.
3. No critical ambiguities or undecided alternatives remain.
4. Approach names patterns, libraries, paths, and conventions with evidence.
5. Test strategy/framework is stated and agent QA acknowledged.
6. No blocking questions or "decide during implementation" deferrals remain.

All YES: announce "All requirements clear. Proceeding to plan generation." and proceed
without asking permission. Any NO: ask the specific unresolved question, not answered
questions or the whole interview again. Update the draft and recheck the full list
after each answer. An explicit "proceed anyway"/"generate the plan" may trigger generation
before clearance, but unresolved user decisions must remain visible and be resolved
before claiming decision-complete delivery.
The optional [clearance checklist](references/clearance-checklist.md) elaborates this
same procedure; its absence cannot block body-only use.

## Phase 3: Generate, Review, and Present

1. **Gap analysis before writing:** re-read the draft/research; identify contradictions,
   ambiguity, missing constraints/acceptance criteria, execution risks, scope creep,
   and implementation failure modes. Incorporate findings immediately without another
   pre-generation interview. Record them under `Context → Gap Analysis`.
2. **One plan, incremental writes:** keep the entire task in one plan, even 50+ TODOs;
   never split this work into separate phase plans. Create once, then edit; never use
   a second whole-file Write that erases prior work. For large plans write a skeleton,
   append task batches of 2–4 before Final Verification Wave, then read for completeness.
3. **Self-review:** concrete acceptance for every TODO; existing file references;
   evidence for business logic; incorporated gaps; happy and failure QA for every task;
   specific data; zero human-operated acceptance checks.
4. **Classify gaps:** critical user decision → `[DECISION NEEDED: {desc}]`, list and ask;
   minor → fix and list under Auto-Resolved; reasonable default → apply and list under
   Defaults Applied. Do not call unresolved critical placeholders a complete plan.
5. **Present** the summary below. If decisions remain, wait for the user's response,
   update the plan, and resolve them before offering execution.
6. **Standalone endpoint:** offer Start Work, Verified Execution Loop (recommended
   for 5+ task/high-risk plans), or Further Review (adversarial reviewer if exposed).
   Do not start implementation merely by offering a choice.
   A stage-invoked cycle returns to its owner instead, without a new approval menu.
7. Delete the interview draft once the completed plan is saved; the plan becomes the
   sole source of truth. Do not delete an unresolved draft prematurely.

```text
## Plan Generated: {name}
Key Decisions: [decision and rationale]
Scope: IN: [...] | OUT: [...]
Guardrails: [from gap analysis]
Auto-Resolved: [gap and fix]
Defaults Applied: [default and assumption]
Decisions Needed: [blocking user decisions, if any]
Plan saved to: [actual path]
```

## Required Plan Template

All fields below are required, including per-task commit decisions; retain the
schema for short plans without manufacturing unnecessary tasks.
Recommended Agent categories: **quick** for single-file/config/mechanical/trivial work,
**deep** for multi-file logic/architecture/races, **visual-engineering** for frontend/UI.
These are recommendations, not assumed tool names; the executor maps available workers.

```markdown
# {Plan Title}
## TL;DR
- Summary: [1–2 sentences]
- Deliverables: [list]
- Effort: Quick | Short | Medium | Large | XL
- Parallel: YES — N waves | NO
- Critical Path: [tasks]
## Context
### Original Request
### Interview Summary
### Gap Analysis
## Work Objectives
### Core Objective
### Deliverables
### Definition of Done (verifiable conditions with commands)
### Must Have
### Must NOT Have
## Verification Strategy
- Test decision: TDD | tests-after | none; framework
- QA: agent-executed scenarios for every task; no human-operated verification
- Evidence: .issueops/evidence/task-{N}-{slug}.{ext}
## Execution Strategy
### Parallel Execution Waves
- Target 5–8 tasks/wave when scope warrants; <3 except final flags under-splitting.
- Extract shared dependencies into Wave 1; do not pad a trivial plan.
### Dependency Matrix
| Task | Depends On | Blocks | Can Parallelize With |
|---|---|---|---|
| T1 | — | T3 | T2 |
## TODOs
- [ ] N. {Task Title} (implementation + tests are ONE task)
  - What to do: [specific steps]
  - Must NOT do: [exclusions]
  - Recommended Agent: quick | deep | visual-engineering; Reason: [domain fit]
  - Parallelization: YES/NO; Wave; Blocks; Blocked By
  - References: pattern path:lines + what/why; API/type contract; external docs URL
  - Acceptance Criteria: [agent-executable binary checks with commands]
  - QA Scenarios: [happy path AND failure/edge case, each with:]
    - Channel: [available shell/HTTP/browser/terminal tool]
    - Steps: [exact actions, selectors/endpoints, concrete input values]
    - Expected: [specific assertions: status/text/fields/file; binary pass/fail]
    - Evidence: .issueops/evidence/task-{N}-{slug}[-error].{ext}
  - Commit: YES/NO; Message: type(scope): desc; Files: [paths]
## Final Verification Wave
- F1 Plan Compliance Audit: every TODO executed as specified
- F2 Code Quality Review: no AI slop, dead code, overbroad abstractions
- F3 Real Manual QA: every scenario passes with captured evidence
- F4 Scope Fidelity Check: no scope creep or missed deliverables
## Commit Strategy
## Success Criteria
```

References must be exhaustive enough for an executor without interview context.
"Verify it works", unspecified data/selectors, "should respond", and "looks correct"
are invalid QA. Final verification runs **after all implementation tasks**; all four
checks must APPROVE. For standalone execution, present consolidated results and get
explicit user **"okay" before completing**. This confirmation is not a human-operated
test. A cycle uses its existing authorization/endpoint rather than adding this gate.
Plan atomic commits in the repository's convention, but do not commit without authority.
Quality baselines/targets, algorithm design, schema decisions, debugging diagnosis,
and external research feed the plan when relevant; sibling skills are optional collaborators.

## IssueOps Cycle Lane: Stage-Owned Operations

Ordinary standalone planning does not require IssueOps. In a cycle, preserve exact
lifecycle identity and inspect `issueops status --id "$ISSUEOPS_ID" --json` and
`issueops next --id "$ISSUEOPS_ID" --json`; status is a supported root alias.
The invoking stage owns authenticated writes, native actor/generation/lease fences,
canonical worktree, reviews, and handoff. Return the artifact to it; do not invent
flags, bypass missing gates, or treat stage/claim/`--approved` as user authorization.

Preserve the cycle's order and artifacts even when only this body is supplied:

1. Read applicable operating decisions before planning; reuse unchanged plan-prep
   evidence. Verify existing-behavior claims by commands/file:line evidence; mark
   unverified assumptions. Include lifecycle ID, original scope, authorized endpoint,
   and branch/worktree preparation plus environment-based handoff boundaries.
2. Include these exact machine-checked sections, each with substantive findings:
   - `## 적용되는 결정과 주의사항`: paths, decision/caution titles, constraints (or checked-none).
   - `## 재사용하는 기존 구현`: symbols/packages/test helpers reused; justify new implementation.
   - `## 성능 영향`: hot path, complexity, measurement plan.
   - `## 하위 호환성과 side effect`: CLI/MCP/golden/record/provider contracts, existing data,
     rollback; schema/index/query choices and expected row counts when relevant;
     measurable failure/output criteria for changed LLM prompt bodies.
3. Before a canonical worktree exists, write the plan outside the source checkout in
   temporary storage and return it for `issueops artifact stage`. Do not create a
   duplicate tracked source-checkout plan, manually create a worktree, or link early.
   Include acceptance gates `G1..Gn` with CHECK/EXPECT in the plan; no ledger file yet.
4. In an IssueOps cycle the architecture comes before the plan: the stage owner stages an
   architecture document (`## 요구사항과 규모`, `## 데이터와 API 계약`, `## 구조와 흐름`,
   `## 병목과 장애`, `## 절충점과 기각한 대안`), records an independent architecture review bound
   to that document's sha256, and only then writes the plan from it. Architecture approval needs
   refactor plan, rejected alternative, risk, architecture-review evidence, and zero open
   questions. Then the stage owner records routing and the actual adversarial plan review. Plan review must record pass with at least one
   finding bound to the current plan digest. Changed plans require re-review.
   A stop verdict returns to grill for investigation/replanning, not a waived gate.
   Incorrect issue-body facts require contract-change feedback, issue sync, and
   mark-issue-updated recording; changing only the plan is insufficient.
5. If authorized beyond planning/review, the owner previews/confirms execution preparation.
   Preparation materializes the staged plan
   in the canonical worktree. Final plan location uses the issue number, with slug
   `{issue-number}-{short-title}`; never use a lifecycle ID as the issue folder number.
6. Return to the stage's authorized routing: after preparation, use automatic
   handoff: usable Herdr first when the preparing session runs inside Herdr, otherwise
   current-session continuation or a manual handoff from a second terminal the user
   opened. Handoff requires
   settled writers, release of the old holder, and verified new ownership in the same
   worktree; do not keep implementing after delivery to the new session.
7. The authenticated active owner performs `issueops link-plan` after materialization
   (skip if preparation already populated plan_path), compatibility review with no
   blockers, gate-ledger creation in the canonical worktree, then implementation
   phase entry, in that order. Implementation records RED/GREEN gate evidence;
   cleanup rechecks it; verification checks validity/re-runs only as needed.

Do not add standalone Start Work/review choices or a final approval gate to this lane.
Automatic routing grants no extra authority: a planning/review-only request stops
before execution preparation, lease acquisition, new-session launch, or implementation.
Preserve explicit user holds and narrower endpoints; merge, deploy, and destructive
cleanup still require their own authorization. If stage authentication/context is
unavailable, return the plan with that recording/handoff blocker, not a fabricated success.

## Stop Rules and Portability

- Complete plan saved, decisions resolved, template filled, each task has References,
  Acceptance, QA, and Commit, dependency matrix consistent: **DONE**; return to the
  owning stage or present the standalone choice.
- Two context-gathering waves with no useful new facts: stop exploring and draft.
- Two unsuccessful attempts at the same section: report what was tried and ask.
- No evaluator material or sibling installation is required for normal execution.
  Resolve optional references from the real, symlink-resolved skill file, not cwd
  or an unresolved host link. A copied entrypoint retains all required gates and outputs.
