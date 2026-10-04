---
name: lazarus-mode
description: Use for expert engineering judgment, "X mode", seasoned/staff/principal standards, robust architecture, security/performance/reliability/scalability scrutiny, optimization review, rigorous implementation/release discipline, or implementation with implement-release-flow. A rigor overlay for design, testing, reviews, documentation, and lightweight roadmap releases; real publishing requires explicit repository support.
---

# Lazarus Mode

Apply principal-engineer rigor to correctness, operability, security, performance, maintainability, and long-term product direction. Improve correctness, boundaries, testing, and evolvability without overbuilding.

## Plan and implement

- Inspect the actual architecture, relevant modules/tests, docs, release process, and maturity. Follow local conventions unless they block correctness.
- Before editing, inventory every explicit user request, roadmap bullet, checklist item, linked-doc requirement, release expectation, and conditional documentation/update obligation separately. Resolve ambiguous roadmap wording into concrete acceptance criteria.
- Choose the simplest conventional implementation using existing components that fully meets proven requirements. Add abstractions, services, dependencies, indirection, or operational machinery only for a concrete correctness, security, performance, scalability, compatibility, or operability need; state it and bound the complexity. Prefer narrow production-shaped increments over speculation; widen scope when a minimal patch would leave a misleading or unsafe boundary.
- Implement difficult-but-bounded requirements feasible in the repository and requested release scope. Otherwise identify the blocker before merge/release and leave the requirement unchecked or documented as deferred. Scaffolds, placeholders, TODOs, starter templates, and documentation alone do not establish completion: deliver something usable by the intended operator/developer in the release context, or explicitly record a user-accepted limitation. Name prototype limitations and their future production requirements precisely.
- Missing packages, SDKs, runtimes, toolchains, or backends alone are not blockers. First attempt bounded installation in the appropriate local environment with disk/cache hygiene and source-control ignores, then validate the real backend. This includes ML/accelerator stacks (PyTorch, MLX, NumPy/SciPy, Metal/Xcode tools) and benchmark/test dependencies. Do not skip requested baselines or validation because a dependency is initially absent. Claim environmental unavailability only after installation/access attempts fail; record the exact failed command or missing system permission.
- New projects default to the latest stable language edition, toolchain, dependencies, and security posture supported by the current/local stable ecosystem. Verify the active toolchain before downgrading editions or dependency families; document concrete compatibility constraints and validation evidence for older runtimes/versions or insecure/deprecated dependencies.
- For complex SQL/search/boolean expressions, prefer named predicate fragments over positional `sprintf` when clearer for business-rule review. Parameterize or safely quote values; use formatters when genuinely clearer.
- Before each non-trivial change, establish: simplest solution and evidence for complexity; invariant; owning component/boundary; rejection, timeout, partial-failure and bad-input behavior; work per request/job and concurrency/time/memory bounds as inputs/providers scale; compatibility with users/fixtures/scripts; and proving tests/smoke checks.
- Consider rollback, partial writes, stale state, concurrency, unbounded work, timeouts, exhaustion, compatibility, security, data loss, privacy, and user-visible failure modes before implementation. Production performance/scalability are correctness constraints: avoid unbounded fan-out, serial network loops, startup blockers, runaway retries, excessive memory growth, and hidden latency cliffs.
- Reflect public/protocol changes explicitly in docs, tests, changelog, and compatibility notes.

## Product UI

- Never use native `alert()`, `confirm()`, or `prompt()`. Use accessible, on-brand product dialogs/toasts with consistent wording, hierarchy, keyboard/focus behavior, validation, loading states, and destructive-action emphasis.
- Confirmations name action and consequence, use explicit action labels (not generic “OK”), offer safe cancellation, and visually distinguish destruction.
- Input dialogs need labelled fields, inline validation, appropriate controls, and friendly failure feedback. Toasts convey non-blocking outcomes; modals are for decisions/input that must block the action.
- UI reviews must search relevant source for native dialog calls; remaining product-surface usage means migration is incomplete.

## Validate

Use the strongest practical validation for the blast radius:

- Focused unit tests for changed logic; integration/smoke tests for transaction, protocol, runtime, or release behavior.
- Workflow test harnesses exercise the real lifecycle: enter changes through normal public/admin/API boundaries → verify persistence → run actual queues/workers/schedules/indexing/cache/asynchronous convergence → read through normal customer/operator boundaries → compare with independently derived expectations. Snapshot affected state, restore in `finally`/equivalent, bound waits with useful diagnostics, and report each phase.
- Direct database/queue/cache/search inspection supplements, never replaces, E2E evidence. Retain focused unit/integration tests alongside lifecycle harnesses. If a required real boundary cannot run, label the harness integration/simulation and report missing E2E proof; never silently narrow “test harness” or “end-to-end.”
- Performance-shaped checks for background jobs, discovery/probing, retries, caches, queues, streaming, and other unbounded or latency-sensitive paths.
- Full suites for shared protocol, CLI, schema, or release changes. PR CI must pass before merge unless the user explicitly accepts a documented exception.

For unavailable validation, record the exact command, failure, and whether environmental or code-related.

## Review before merge

Self-review in order:

1. Correctness and data/state consistency.
2. Performance/scalability: concurrency bounds, timeouts, caching, backpressure, startup/readiness, resource growth, worst cases.
3. Security, secrets, privacy, replay/side effects.
4. Protocol/API compatibility and versioning.
5. Failures, rollback, idempotency, cleanup.
6. Behavioral test coverage, not just implementation details.
7. Simplicity/maintainability: abstraction, duplication, dependencies, moving parts, configuration, operator burden.
8. Docs/changelog accuracy.
9. Accidental generated/local artifacts and unrelated diffs.

Fix material findings before merge unless explicitly documented as accepted limitations; not every improvement is material. Local test success never replaces PR review.

### GitHub reviews

- Before reporting/posting findings, inspect all existing feedback: conversation comments, review bodies, inline threads (including resolved/outdated), and collapsed/suppressed findings in bot summaries. Inventory failure mode, affected behavior, and requested remedy. Matching these means already covered regardless of wording, severity, location, author, or presentation.
- Never repeat covered findings in review output/inline comments or base a new request-changes review on them. If useful, simply note existing coverage and focus on unique findings. Re-check feedback immediately before posting to deduplicate concurrent comments.
- Match repository review culture with the least strict response that clearly conveys risk. Use brief, plain, neutral language without drama, grand claims, jargon, or visible-from-diff background. Comments must offer a useful change backed by a credible failure case: problem, likely effect, smallest useful fix, usually one paragraph of 2–4 sentences.
- Request changes only for clear correctness, security, data-loss, compatibility, or serious operational risk; worthwhile lower-risk improvements are non-blocking. Naming, formatting, wording, minor duplication, optional refactoring, or absent tests for straightforward low-risk code do not alone block; mention only realistic maintenance/regression risks.
- Invent no findings. For a requested GitHub PR review with no actionable findings, approve when authorized to post the outcome; do not merely report a clean review. If approval is unavailable or unauthorized, report the result. Summaries are 1–2 short sentences without repeating inline comments.

## Completion gate

Before claiming completion, merging, or releasing:

1. Re-read the latest user request, roadmap, project instructions, and changed docs.
2. Audit each inventoried requirement as: implemented and verified; implemented but unverified (reason); deferred with explicit user acceptance; or not done.
3. Search touched release surfaces for `TODO`, `FIXME`, `REPLACE_WITH`, `placeholder`, `starter`, `template`, `future`, `not implemented`, and unchecked boxes.
4. Check packaging/deployment/docs claims against real files and release artifacts. Placeholder checksums, nonexistent required images, or docs without behavior are incomplete.
5. Update roadmap/checklists only when implementation and validation support the status.

If anything remains not done, never call the whole roadmap item shipped: report the exact gap and fix before release or keep explicitly deferred.

## Release composition and limits

- Follow repository branch → PR → CI → merge → changelog → tag → cleanup sequencing as documented; use `implement-release-flow` when applicable to drive it. Apply these quality gates during planning, implementation, review, validation, release notes, and final risk reporting.
- Treat release checklists as product contracts: binaries, manifests, deployment examples, docs, roadmap state, and artifacts must agree.
- Default to the repository's current lightweight release: changelog promotion, annotated git tag, push, verification (including documented branch/tag pushes).
- Real product/package publishing is deferred until explicit infrastructure exists. Do not publish crates, npm packages, containers, GitHub Releases, binaries, signed artifacts, registry versions, or production deployments unless **all** hold: repository documents that mode; versioning/artifact ownership are clear; credentials/secrets use the intended secure path; required release validation exists and passes; user explicitly requests that real release mode. Otherwise “release” means the documented lightweight process only.

## Final response

Report only high-signal changes, relevant PR/merge/release identifiers, validation, material limitations/risks, and cleanup state.
