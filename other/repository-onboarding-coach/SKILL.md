---
name: repository-onboarding-coach
description: Analyze unfamiliar repositories and turn code evidence into durable human maintenance confidence. Use when onboarding a developer, taking over a repository, creating or refreshing a project atlas, tracing a business flow, preparing a change-impact brief, teaching someone to maintain a codebase, assessing maintenance readiness, reducing uncertainty before AI-assisted changes, or adding confidence alongside normal development without changing the existing workflow.
---

# Repository Onboarding Coach

Build a durable mental model and evidence-backed maintenance system for the current repository. Optimize for human understanding, safe change ownership, and calibrated confidence—not maximum document volume.

## Match the user's language

Write explanations and generated artifacts in the user's language. When the user
writes Chinese, default to Simplified Chinese. Keep code symbols, paths, API
names and commands unchanged. Render evidence labels as `已验证（Verified）`,
`推断（Inferred）` and `未知（Unknown）` when using Chinese.

## Select a mode

Choose the smallest mode that satisfies the request:

| Mode | Use when | Primary output |
|---|---|---|
| `ambient` | Normal AI-assisted work should continue without a new process | Concise impact, risk and verification context |
| `bootstrap` | The repository or team is unfamiliar | Project Atlas |
| `learn` | The user wants to understand a domain or flow | Flow Card + teach-back |
| `change-prep` | A requirement may lead to code changes | Change Brief |
| `refresh` | An Atlas already exists and code changed | Incremental evidence refresh |
| `readiness` | The user wants to know what they can safely maintain | Competency assessment |

Default to `ambient` for ordinary requirements. Use `bootstrap`, `learn`, `refresh`, or `readiness` when the user explicitly asks for those outcomes or the repository is the task itself. Combine modes only when the user clearly needs them. Do not generate a full Atlas for a narrow code question.

## Work alongside the existing workflow

In `ambient` mode:

1. Analyze only the requirement's likely path and adjacent risks.
2. Do not create Atlas files, install hooks, change CI, or introduce forms unless the user asks.
3. Before editing, share at most a compact summary of affected flow, state/cache impact, risk and intended verification when it materially helps.
4. Continue low-risk and reversible work without pausing for teach-back or document approval.
5. Pause only when a missing decision changes security, billing, destructive data behavior, compatibility, or another high-impact invariant.
6. After editing, compare predicted and actual impact, run proportional checks, and report unexpected scope or unresolved risk.
7. Do not quiz the user unless they explicitly request learning or readiness coaching.

Treat confidence as a sidecar to delivery, not a replacement workflow.

## Start with repository evidence

1. Read all applicable repository instructions such as `AGENTS.md`, `CONTRIBUTING.md`, and local policy files.
2. Inspect Git status, current branch, HEAD, repository root, and recent history. Preserve user changes.
3. Run `scripts/repo_inventory.py <repo> --summary` for a deterministic, context-bounded structural inventory when Python 3 is available. Request the full lists only when a summary category needs deeper inspection.
4. For repository onboarding or flow discovery, run `scripts/evidence_manifest.py <repo> --summary`. Use its registrations and relations as investigation candidates, never as a verified runtime call graph.
5. If `.codegraph/` exists, use CodeGraph before grep or manual file reading to locate symbols and critical paths.
6. Inspect actual entrypoints, routing or job registration, persistence models, migrations, caches, external clients, configuration, and tests.
7. Prefer current code and executable tests over stale documentation. Use Git history to explain non-obvious decisions when necessary.
8. Never expose credentials, private customer data, production secrets, or sensitive repository content in generated artifacts.

## Apply the evidence model

Classify important claims:

- `Verified`: directly supported by current code, tests, schema, configuration, or observed output.
- `Inferred`: plausible from available evidence but not completely proven.
- `Unknown`: evidence is absent, conflicting, inaccessible, or requires runtime confirmation.

For every high-impact claim, record:

- the claim;
- status;
- source symbols or files;
- supporting tests or migrations when available;
- the verified Git commit;
- risk if stale or wrong.

Do not hide uncertainty behind fluent prose. Convert uncertainty into an explicit known-unknown item.

Read `references/evidence-manifest.md` before treating generated flow candidates as evidence. Read `references/atlas-schema.md` when creating or refreshing an Atlas. Read `references/change-brief.md` before analyzing a concrete change. Read `references/competency-rubric.md` before coaching or assessing a developer.

## Bootstrap a Project Atlas

### 1. Establish the project passport

Identify:

- purpose and users;
- languages, frameworks, build tools, and deployment shape;
- executable entrypoints and background workers;
- primary data stores, caches, queues, and external services;
- build, test, lint, and run commands;
- repository policies and operational constraints.

### 2. Build the domain map

Identify the smallest stable vocabulary that explains the system:

- core business entities;
- ownership boundaries between modules;
- source of truth for each entity;
- public and internal interfaces;
- lifecycle and state transitions.

Do not create a file-by-file summary. Group code by responsibility and business capability.

### 3. Select critical flows

Start from explicit registrations in the Evidence Manifest, then verify candidates
with CodeGraph, implementation, callers or consumers, tests, and runtime evidence.
Do not confuse the manifest's discovery score with business criticality.

Rank flow candidates using:

- business centrality;
- request or event frequency;
- state mutation;
- security or financial impact;
- operational incident likelihood;
- cross-module complexity.

Document five to eight flows first. Expand only after the core mental model is stable.

For each flow, cover:

- trigger and entrypoint;
- authentication and validation;
- orchestration and dependencies;
- reads, writes, transactions, and cache behavior;
- external calls;
- failures, retries, fallbacks, compensation, and idempotency;
- authorization, billing, audit, and observability impact;
- invariants, tests, change hotspots, and known unknowns.

### 4. Create risk and state maps

Explicitly map:

- database tables and migrations;
- cache keys, TTLs, warmup, and invalidation;
- queues, events, locks, and async settlement;
- external provider credentials and reload behavior;
- security, privacy, billing, concurrency, compatibility, and migration risks.

### 5. Write the Atlas

Use the templates in `assets/project-atlas-template/`. Copy only the sections needed by the repository. Default to `docs/project-atlas/` when the user authorizes documentation writes and the repository has no preferred location.

Record repository-relative `Evidence paths` metadata on critical pages so freshness checks can map Git changes without guessing dependencies.

Keep the index concise. Use progressive disclosure: overview first, detailed flow and entity pages second, exact code retrieval on demand.

## Teach a domain or flow

### Explain

Start with a one-screen mental model, then show the normal path, failure path, and state changes. Explain why the design exists, not just which functions call each other.

### Verify

Cross-check the flow against tests, migrations, configuration, and at least one caller or consumer. Mark gaps explicitly.

### Teach back

When the user asks for learning or coaching, ask them to explain the flow without looking at the source. Focus on causal questions:

- What triggers the flow?
- Which state is authoritative?
- What is cached and how does it become stale?
- What can fail, retry, compensate, or partially succeed?
- Which invariant would be most dangerous to break?
- How would you prove a change is safe?

Correct misconceptions with concrete evidence. Avoid trivia about line numbers or private helper names.

### Simulate

Give one realistic requirement and one failure scenario. Ask the learner to predict affected modules, state changes, tests, observability, and rollback. Compare the prediction with repository evidence.

## Prepare a change

Use the template in `references/change-brief.md`.

Before editing, determine:

- user intent and acceptance criteria;
- explicit assumptions;
- entrypoints and affected call paths;
- data model, migration, cache, queue, and external-service impact;
- authentication, authorization, billing, privacy, concurrency, and compatibility impact;
- normal, failure, retry, fallback, and rollback behavior;
- narrow and broad validation commands;
- observability and rollout plan;
- unresolved questions and risk rating.

In normal delivery mode, share a concise impact summary and continue implementing within scope. In explicitly requested learning mode, pause after the Change Brief so the learner can predict the implementation before code changes begin.

After implementation:

1. Compare the actual diff with the predicted impact.
2. Explain unexpected files or behaviors.
3. Run proportional tests and inspect the resulting state.
4. Update only Atlas pages whose stable knowledge changed.
5. Add newly discovered unknowns or invariants.

## Refresh an existing Atlas

1. Run `scripts/atlas_freshness.py <repo> --atlas <atlas-path> --format json` for a deterministic candidate report.
2. Read the Atlas verification commit and declared evidence paths.
3. Compare candidate pages with current HEAD using Git diff, CodeGraph when available, and history.
4. Map changed files and symbols to affected flows, entities, state maps, and invariants.
5. Re-verify affected claims against current code and tests.
6. Leave unaffected pages unchanged.
7. Update verification metadata only after evidence is checked.
8. Report pages that may be stale but cannot be verified.

Treat the script's `review` status as a prompt for human/AI verification, not proof that a page is wrong. Do not rewrite the whole Atlas for cosmetic consistency.

## Assess maintenance readiness

Use `references/competency-rubric.md` and evaluate observable behavior rather than confidence statements.

Assess whether the developer can:

- explain the project and its boundaries;
- trace a core flow;
- identify sources of truth and cache behavior;
- predict change impact;
- recognize high-risk invariants;
- design tests, rollout observation, and rollback;
- complete and explain a real scoped change.

Report:

- current level by domain;
- verified strengths;
- unsafe or unverified areas;
- the next smallest real task that would produce evidence of growth.

Do not claim a developer is ready for high-risk maintenance based only on reading or quiz performance.

## Keep human agency in the loop

Use AI for discovery, cross-referencing, drafting, and implementation. Require human understanding at decision boundaries:

- accepting a high-impact assumption;
- changing an invariant;
- approving a migration or compatibility break;
- changing authentication, billing, permissions, or destructive behavior;
- selecting rollout and rollback strategies.

The goal is not for the human to match AI retrieval speed. The goal is for the human to understand the system well enough to judge, verify, and own the outcome.

## Avoid these failure modes

- Do not generate an exhaustive file-by-file encyclopedia.
- Do not treat a call graph as a complete business explanation.
- Do not mark inferred behavior as verified.
- Do not produce hundreds of pages before validating the top flows.
- Do not quiz learners on names instead of causal reasoning.
- Do not let documentation block urgent safe delivery unless the user enabled training mode.
- Do not let Atlas generation modify application code.
- Do not expose secrets in inventory output or documentation.
- Do not promise complete understanding; bound and track uncertainty.

## Resource routing

- Run `scripts/repo_inventory.py` for a read-only structural snapshot.
- Run `scripts/evidence_manifest.py` to connect source candidates with static registrations, nearby tests, migrations, and ranked investigation starting points.
- Run `scripts/atlas_freshness.py` to compare Atlas verification commits and declared evidence paths with current Git HEAD.
- Read `references/evidence-manifest.md` for the manifest schema and confidence boundaries.
- Read `references/atlas-schema.md` for Atlas structure, evidence headers, and flow selection.
- Read `references/change-brief.md` for change-impact analysis.
- Read `references/competency-rubric.md` for teach-back and readiness assessment.
- Copy from `assets/project-atlas-template/` when creating repository documentation.
