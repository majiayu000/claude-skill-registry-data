---
name: vibe-coding
description: "Use this when an approved Spec that passes the installed authoritative spec-intake validator must be turned into stable code, or when an existing AI-built project must be initialized, repaired, tested, evaluated, reviewed, pushed, or prepared for deployment. This company orchestration skill automatically applies repository inspection, risk-adaptive architecture and technical-debt controls, planning, subagent development, TDD, business-scenario traceability, loop engineering, independent review, Git delivery, and optional SRE deployment while pausing for user choices only when product, business, architecture, data, permission, risk, or plan scope would change."
---

# Vibe Coding

Convert an approved business Spec into stable, observable, maintainable, and transferable software. The user should not need to know which engineering sub-skill to call. Orchestrate the development system automatically and expose only decisions that require product or business authority.

## Non-negotiable contract

Formal coding starts only when the input Spec passes the installed authoritative `spec-intake` schema and validator and contains:

- `stage_gate.readiness_label = engineering_ready`;
- `stage_gate.decision = ready_for_engineering`;
- business-owner-confirmed `business_success_scenarios` for the current scope;
- QA-approved `validation_plan.scenario_coverage` for every critical in-scope scenario;
- a confirmed `delivery_risk_profile`.

If this contract is missing, invoke `spec-intake` and return to product definition. Do not invent missing business outcomes in engineering. The only exception is an explicitly user-authorized R0 prototype: it must remain isolated, synthetic-data-only, visibly marked non-production, and cannot count as progress toward formal delivery. Never downgrade into that path automatically.

Use three sources of truth together:

1. The Spec defines what and why.
2. The checked-in repository, runtime contract, and agent rules define how the change fits.
3. Fresh tests, Evals, E2E evidence, and business-observable signals define whether it works.

Self-confidence, code inspection alone, a screenshot, or "tests should pass" is never completion evidence.

## Responsibility model

The responsibility chain is fixed:

```text
Business defines the successful end-to-end flow
  -> Skill structures it and enforces gates
  -> QA expands professional coverage
  -> Engineering automates execution and evidence
```

Business owns the intended outcome and observable success. Product or this Skill may structure and replay it for confirmation. QA adds boundary, negative, permission, repeat, dependency-failure, and recovery coverage. Engineering selects fixtures, frameworks, environments, commands, telemetry, and evidence paths. QA and engineering may not silently rewrite the business outcome.

Read `references/spec-input-contract.md` whenever accepting or rejecting a Spec.

## Start protocol

At the beginning of every formal run:

1. Show a concise stage tracker using the runtime plan tool when available.
2. Resolve and record the remote repository URL before implementation. If no approved accessible Remote exists, perform only safe read-only inspection and pause with choices to provide an existing URL or explicitly authorize creation in a named organization; never invent or silently create one.
3. Inspect the nearest applicable `AGENTS.md` or equivalent agent rules, then the actual README, project manifest, source, tests, architecture, runtime, Git status, remote, and recent history.
4. Locate the approved Spec and validate it.
5. Classify the work and delivery path from facts, not the user's job title or the agent's confidence.
6. Preserve unrelated user changes.

Never require Graphify as a company-level gate. A repository may use it only when that repository's own instructions require it.

## Ten-stage orchestration

Run these stages in order. A stage may be revisited when new evidence invalidates an earlier assumption.

### 1. Accept the engineering contract

- Validate the Spec with `spec-intake/scripts/validate_spec.py`.
- Extract scope, exclusions, business rules, success scenarios, delivery risk, owners, runtime constraints, and open decisions.
- Refuse formal implementation when the stage gate is not engineering-ready.
- Create an explicit requirement/scenario inventory for later traceability.

### 2. Inspect the real repository

- Confirm `origin` or the approved remote URL before writing code.
- Read applicable agent rules and identify every enforceable development requirement.
- Discover the actual install, build, start, stop, test, Eval, health, and release commands.
- Identify architecture boundaries, ownership, dependencies, data paths, observability, last green commit, and current working-tree changes.
- Do not create parallel infrastructure when the repository already provides a supported path.

Read `references/agent-rules-compliance-standard.md` and `references/repository-template-standard.md`.

### 3. Initialize, choose the repository organization, and choose the debt strategy

New projects must establish the standard project contract before feature work. Existing projects must first discover and assess the actual README, `PROJECT.yaml`, Spec, architecture, plan, business goal/metrics, runtime constraints, test plan, traceability, Eval plan, runbook, rule audit, and technical-debt register. The contract requires complete content and navigability, not one mandatory detailed-document directory tree.

When an existing repository does not use the recommended layout, present exactly two organization choices before moving or creating documents:

- **A. Convert to the standard structure:** move or consolidate the applicable documents into the recommended paths, update all links and tooling, and verify no references break.
- **B. Adapt in place:** preserve the repository's coherent existing structure, map each required document responsibility—including QA normalized Spec, test design, and test cases—to normalized project-relative paths in `PROJECT.yaml`, and add the exact responsibility-to-path map to the root README. Fill missing content in the most appropriate existing location; do not create duplicate sources of truth merely to imitate the template.

The organization choice does not waive any content, evidence, ownership, test, Eval, runtime, or recovery requirement. Record the choice. For a new repository with no established structure to preserve, use the standard structure unless the user identifies an approved organization convention.

Do not infer completeness from filename, file length, or confident prose. After documents are mapped and gaps are filled, dispatch a genuinely independent review execution and retain its orchestration trace. Its review artifact binds every mapped file's SHA-256 and each required semantic topic to a unique full-line locator plus a nontrivial section hash. Missing topics, stale hashes, reused/nonexistent locators, incomplete sections, or a trace showing self-review block initialization. The JSON identity fields are audit declarations; the actual Agent/tool trace proves independence.

Technical debt means a verified gap between the current repository and an approved requirement that increases change risk, failure likelihood, verification cost, operational risk, or future maintenance cost. It includes violations of applicable agent rules, broken or absent architecture boundaries, missing deterministic tests/Evals, undocumented runtime behavior, unsafe dependencies, missing observability, and unowned or unrecoverable delivery paths. A stylistic preference without an approved requirement or measurable risk is not debt.

When debt affects the current work, present exactly two decision paths:

- **A. Full remediation:** fix all identified debt, verify the repaired baseline, update documents, and then implement the feature.
- **B. Minimum safe remediation:** repair the minimum architecture and verification boundary required for a safe baseline; explicitly exclude all remaining debt and all code paths it affects from the current feature. Do not patch new behavior onto the defective path.

No third path allows continuing on a known-bad architecture. Record the user's choice and evidence. Read `references/project-initialization-standard.md`, `references/documentation-content-standard.md`, and `references/technical-debt-standard.md`.

### 4. Design and plan

- Use `brainstorming` when implementation discovery reveals a material design decision not already settled by the Spec.
- Select or preserve an approved architecture; do not freely invent a new system boundary.
- Maintain system architecture and, when relevant, algorithm design, UI states, authorization, data lifecycle, integrations, runtime constraints, business metrics, rollback, and observability.
- Use `writing-plans` to produce bite-sized tasks with exact files, tests, commands, and commit boundaries.
- Use `using-git-worktrees` when isolation is appropriate and safe.

Pause for user choice before changing product behavior, business goals or metrics, business rules, architecture boundaries, data or permission models, risk level, runtime commitments, cost commitments, or plan scope. Provide two or three concrete options, recommend one, and explain impact in business language.

Read `references/architecture-and-ui-standard.md` and `references/interaction-and-change-control-standard.md`.

### 5. Define the feedback contract

Before each implementation slice, record:

- target behavior and linked requirement/scenario IDs;
- observable signals and baseline;
- objective pass/fail rules;
- exact verification command arrays;
- evidence paths;
- rollback method.

The feedback contract turns implementation into a closed loop. If no reliable signal can distinguish success from failure, do not code yet; improve observability or return to the business/product gate.

Read `references/loop-engineering-standard.md`.

### 6. Implement small slices

- Prefer `subagent-driven-development` for complex work with separable components; give every subagent a bounded contract and independent verification target.
- If subagents are unavailable, execute sequentially without dropping independent spec, code, and test review.
- Use `test-driven-development`: create the failing test first, observe the intended failure, implement the smallest coherent change, rerun relevant checks, and commit a green slice.
- Use `systematic-debugging` for unexpected failures; trace the root cause before changing code.
- Plan-external refactoring discovered during coding is allowed only after explaining why the current design is invalid or risky, giving scoped options, receiving user confirmation, and updating Spec/design/plan/tests before code.
- Do not combine a bug fix with unrelated framework changes, dependency upgrades, or broad cleanup.

Read `references/subagent-and-review-standard.md`.

### 7. Prove business behavior

- Invoke `qa-generated-test-case` to turn the current Spec and business success scenarios into executable QA coverage.
- Maintain traceability from each in-scope requirement and critical business scenario to QA cases, automated verification, observable signals, and fresh evidence.
- Run unit, integration, E2E, permission-negative, recovery, UI/accessibility, performance, and Eval checks according to risk and relevance.
- An E2E is a product/business success flow first and a technical automation second. Business owns the flow; QA professionalizes coverage; engineering automates it.
- Run checks repeatedly during implementation, not only at the end. Compare actual signals to the baseline and pass/fail rules, diagnose deltas, make the smallest justified correction, and rerun until the feedback contract passes or a decision gate is reached.

Read `references/testing-standard.md`, `references/eval-standard.md`, and `references/loop-engineering-standard.md`.

### 8. Review independently

- Use `requesting-code-review` after each substantial slice and before delivery.
- Use an independent testing/review agent to inspect Spec compliance, tests, Evals, architecture, security, maintainability, and evidence.
- Use `receiving-code-review` to verify findings against the repository before changing code.
- Automated agent review and test are mandatory for a PR. Human review requirements belong to the repository or engineering team; do not invent a universal human-approval gate.
- The authoring agent must not be the only source of approval evidence.

### 9. Deliver through Git

- Automatic local commits are allowed after relevant checks pass.
- The repository must have an approved remote URL from the start.
- The versioned pre-commit hook must run the repository-owned `commands.pre_commit_full` aggregate before every local commit; it covers the risk-tier-required format, static, type, unit, integration, and build checks.
- After complete tests and Evals pass, push the branch or create/update a PR; do not leave a completed feature only in a local worktree.
- Direct push/merge is allowed only when the project is single-owner **or** the change is small, repository permissions allow it, risk is R0/R1, and no independent PR trigger applies. PR triggers include a large change in a multi-person project, R2/R3 risk, architecture/API/data/permission/integration/migration or technical-debt repair, a protected branch, or explicit repository policy. Multi-person ownership alone does not force a PR for a small change when the contributor has push permission.
- Use `finishing-a-development-branch` for final integration choices.

Read `references/git-delivery-standard.md` and `references/pull-request-standard.md`.

### 10. Deploy only when requested or required

Deployment is optional. If deployment is in scope, invoke `production-devops-sre` and let that Skill determine whether staging, production controls, migration handling, change tickets, observability, and rollback validation are required. Do not hard-code a universal staging requirement here.

Read `references/deployment-adapter-standard.md`, `references/runtime-standard.md`, and `references/incident-and-rescue-standard.md`.

## Risk-adaptive minimums

Use the confirmed `delivery_risk_profile`; never lower its tier silently.

| Tier | Typical scope | Minimum delivery controls |
| --- | --- | --- |
| R0 | isolated prototype, synthetic data | runnable demo, smoke check, explicit non-production label, no live integration |
| R1 | low-risk internal tool or reversible small feature | initialized project contract, business-rule tests, critical E2E, UAT/equivalent owner evidence, full checks, rollback |
| R2 | important workflow, integration, sensitive data, important writes | architecture/data/security review agents, integration and permission-negative tests, recovery verification, PR, operational evidence |
| R3 | external users, finance/HR/legal/payment, critical infrastructure or irreversible impact | engineering-led delivery, complete security/reliability controls, PR, human approvals as required by governing policy, release rehearsal and recovery evidence |

Read `references/risk-adaptive-controls.md` for dimension-specific escalation.

## Required project artifacts

The root contains `README.md` and JSON-compatible `PROJECT.yaml`. The current Spec, Design, and Plan continue to use the Superpowers convention:

```text
docs/superpowers/specs/YYYY-MM-DD-<topic>-spec.json
docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md
docs/superpowers/plans/YYYY-MM-DD-<topic>.md
```

Other documents may use the standard paths or a coherent existing repository layout. `PROJECT.yaml.documentation` maps every responsibility to its real path, and adapted repositories repeat that navigation in README. At minimum maintain:

- approved Spec and business success scenarios;
- business goal and measurable business metrics;
- system architecture and conditional algorithm design;
- runtime constraints and observable signals;
- implementation plan;
- test plan, scenario/requirement traceability, and Eval plan;
- QA normalized Spec, test design, and test cases;
- agent-rules audit and technical-debt register;
- independent documentation content review bound to mapped-file hashes and topic locators;
- task feedback contracts and fresh evidence manifests;
- runbook and rollback;
- PR/delivery record when applicable.

Use `assets/templates/` as content contracts and recommended organization, not as a mandatory tree for existing repositories. Validate the repository contract with `scripts/validate_project.py`, every task feedback contract and its measured signals with `scripts/validate_feedback.py`, and business scenario coverage/evidence with `scripts/validate_traceability.py`. Pass the actual project root and environment; declarations, missing README mappings, or nonexistent evidence paths do not satisfy these gates.

## Completion gate

Before any completion claim:

1. Use `verification-before-completion`.
2. Run the configured full test and full Eval commands from a clean, current checkout.
3. Validate the evidence manifest and traceability.
4. Confirm every critical in-scope business success scenario has fresh executable evidence and its business-observable success signals match the pass rule.
5. Confirm the remote delivery action required by policy succeeded.
6. Report exact status using `references/completion-status-standard.md`.

Use the exact status vocabulary from the completion standard: `development_complete_not_deployed`, `pushed`, `pr_open_waiting`, `merged`, `non_production_deployed`, `production_rollout`, `production_deployed`, `blocked`, or `rolled_back`. A local-only implementation cannot be reported as development complete because successful remote delivery is a completion gate. Never collapse states into "done".

## Failure and rescue

There is no arbitrary "AI failed twice" completion logic. Loop engineering should expose drift during each slice. Stop immediately when evidence indicates data corruption, security or permission bypass, secret exposure, production impact, or an unrecoverable migration risk. For other failures:

1. freeze scope and preserve the last green commit;
2. reproduce with a deterministic failing check;
3. collect logs, environment, Spec version, commit, attempts, and impact;
4. classify the failed contract layer;
5. apply the smallest root-cause fix;
6. rerun the complete affected feedback loop;
7. hand off a reproducible package when required expertise or authority is missing.

Read `references/incident-and-rescue-standard.md`.

## Reference loading map

Load only the documents needed for the current stage:

- Intake: `spec-input-contract.md`, `risk-adaptive-controls.md`.
- Initialization: `repository-template-standard.md`, `project-initialization-standard.md`, `documentation-content-standard.md`, `technical-debt-standard.md`, `agent-rules-compliance-standard.md`.
- Design/change: `architecture-and-ui-standard.md`, `interaction-and-change-control-standard.md`.
- Build/verify: `loop-engineering-standard.md`, `testing-standard.md`, `eval-standard.md`, `subagent-and-review-standard.md`.
- Git: `git-delivery-standard.md`, `pull-request-standard.md`, `completion-status-standard.md`.
- Runtime/deploy/rescue: `runtime-standard.md`, `deployment-adapter-standard.md`, `incident-and-rescue-standard.md`.
