---
name: research-repo-technology
description: Research technologies an existing repository should adopt, adapt, build, or reject. Use when assessing architecture or product opportunities, comparing external projects at source level, or producing evidence-backed recommendations and proofs of concept from the live codebase.
---

# Repository Technology Research

Produce decision-grade, repo-specific technology research without turning the result into a generic tool catalogue.

## Adapt to the available runtime

Do not refuse research solely because a preferred model, reasoning level, or subagent type is unavailable. Establish the available capabilities before planning the work, then preserve the evidence standard with the best supported execution shape:

1. Use the current root agent to establish the local baseline and integrate the findings.
2. Use independent research lanes only when subagents are available, permitted, and materially improve coverage. Select only models and reasoning levels explicitly exposed by the runtime.
3. If subagents are unavailable or inappropriate, perform a bounded root-only audit. Reduce the number of gaps or candidates if necessary rather than inventing coverage.
4. State the execution shape, incomplete lanes, and any coverage trade-off in the closeout. A missing capability is a limitation to disclose, not a reason to abandon a well-scoped request.

Never claim that a model identity or capability was verified when it was not. Never fabricate an unsupported model selector.

## Preserve the research boundary

- Treat the task as read-only unless the user explicitly expands the scope.
- Do not edit the repository, install dependencies, update trackers, deploy, or change external state.
- Avoid builds and tests that create artifacts. Inspect existing test code, results, benchmarks, and qualification receipts instead.
- Follow the closest applicable `AGENTS.md` and any repository-specific instructions.
- Preserve dirty worktrees and concurrent work. Record branch, HEAD, and working-tree state at the start and recheck them before closeout.
- Use the live checkout as the source of truth for current implementation. Use explicit product-direction documents as the source of truth for intended direction. Call out disagreements.
- Separate confirmed repository evidence, confirmed external evidence, and inference.
- Browse for current external facts and cite primary sources directly.

## 1. Establish the live repository truth

Start the local audit while independent research lanes run.

1. Inspect repository instructions, Git state, top-level structure, manifests, dependencies, and supported platforms.
2. Locate relevant documents by searching rather than assuming filenames: README, strategy, product direction, architecture, current state, roadmap, ADRs, privacy, security, performance, release, and unfinished-work records.
3. Trace the product's real workflows from source end to end:
   - inputs and acquisition;
   - processing and state transitions;
   - storage, caches, and retention;
   - protocols and external integrations;
   - user-facing presentation and control;
   - error, recovery, and degraded-state behavior.
4. Inspect tests, benchmarks, performance receipts, privacy boundaries, security boundaries, licences, and dependency choices that constrain recommendations.
5. Identify current strengths before gaps. Distinguish verified limitations from hypotheses that still need evidence.
6. Note duplicated machinery, weak ownership boundaries, missing abstractions, performance bottlenecks, stale assumptions, and valuable capabilities the architecture cannot currently provide.

Summarize the baseline as: current strengths, verified limitations, hypotheses, non-negotiable constraints, and the most important evidence gaps.

## 2. Derive research questions from gaps

Frame every lane as:

`observed gap -> user or engineering impact -> decision to inform -> evidence needed`

Do not start with a fashionable technology and search for somewhere to put it.

Before fan-out, set an evidence budget from the user's requested depth: opportunity limit, number of independent lanes, maximum candidates to inspect per gap, wait budget, and a stopping condition. Scale the budget up for an explicitly exhaustive task, but stop once the leading options can be distinguished with primary evidence.

When available and useful, spawn as many independent lanes as the research needs and available slots allow, without an arbitrary minimum or cap. Choose only a model and reasoning level the runtime exposes, keep root ownership of integration, and tell lane agents not to spawn further agents. Give each lane the repository path, non-mutation boundary, one specific question, and the required evidence. Do not leak an intended answer or assign overlapping catalogue searches.

If lanes cannot run, continue root-only with a bounded set of the highest-impact questions. Say which independent checks could not be performed and do not represent the result as exhaustive.

Use a divergent pass to surface non-obvious opportunities, then focus evidence lanes on the strongest clusters. Read [research-lanes.md](references/research-lanes.md) when designing the fan-out.

## 3. Research external technology at source level

Search current primary sources and GitHub only after the local audit has exposed concrete gaps.

For each promising external project or technology:

1. Verify the exact problem it solves and whether that problem matches the repository's gap.
2. Inspect beyond the README:
   - relevant source files and integration boundaries;
   - architecture and algorithms;
   - tests and failure handling;
   - releases, maintenance activity, and issue signals;
   - security posture and dependency surface;
   - licence and source-reuse constraints.
3. Identify the smallest legitimate unit to reuse: component, protocol, data model, algorithm, operational pattern, or design lesson.
4. Name the exact integration point in the target repository.
5. Prefer official documentation, specifications, research papers, release notes, source, tests, and licence files. Use secondary sources only to discover primary evidence.
6. Cite direct pages that support each material claim.

Stop expanding the search when additional projects repeat an already-covered approach without changing the adopt/adapt/build/reject decision.

Do not install, execute, or clone third-party software during a research-only task unless the user explicitly authorizes it. Use read-only web and GitHub access.

## 4. Decide adopt, adapt, build, or reject

Evaluate every candidate against:

- user value and urgency;
- fit with the current architecture and product direction;
- exact integration cost and ownership boundary;
- privacy, security, and data-retention effects;
- latency, throughput, memory, power, and scaling risks where relevant;
- maturity, maintenance, dependencies, and platform support;
- licence compatibility and source-reuse limits;
- reversibility and proof cost;
- genuine differentiation versus commodity reinvention.

Classify the recommendation:

- **Adopt** an existing dependency or standard when it already solves the bounded problem and its operational cost is acceptable.
- **Adapt** a narrow component, protocol, algorithm, or pattern when the whole project is unsuitable but a well-bounded part transfers cleanly.
- **Build** only when existing options do not meet an evidenced need or the repository's combination of constraints creates genuine differentiated value.
- **Reject** attractive but misaligned options explicitly, with the reason.

Reject any opportunity that lacks a verified current limitation, concrete user value, repository integration point, and supporting primary evidence.

## 5. Reconcile and rank

Treat subagent output as leads, not final evidence. Recheck important claims, resolve contradictions, merge duplicates, and discard unsupported recommendations.

Rank opportunities by expected value, evidence confidence, strategic fit, risk, and proof cost. Prefer a short ranked set over false exhaustiveness. Default to no more than eight opportunities unless the user requests another limit.

Before writing the final report, read [report-contract.md](references/report-contract.md) and follow its evidence and proof-of-concept fields.

Select up to three of the strongest qualified opportunities. Use fewer, including none, when the evidence gate above does not justify three, and state why the report stops there. Never add a weak opportunity to meet a quota. For each selected opportunity, propose a bounded proof of concept with:

- one question to answer;
- the smallest representative fixture or workload;
- measurable success thresholds;
- privacy, performance, correctness, and compatibility checks as applicable;
- a stop condition that prevents a prototype from becoming an accidental commitment.

Do not implement the proofs of concept during a research-only task.

## 6. Close out with evidence

Lead with the strategic recommendation, then report the repository baseline, ranked opportunities, adoption decisions, rejected alternatives, and top proofs of concept.

State:

- the exact checkout and evidence inspected;
- what was not verified;
- whether any research lane remained incomplete;
- the final Git/working-tree state;
- that no files, dependencies, tasks, deployments, or external state changed;
- that no build or test was run when that is the case.

Do not claim exhaustive review when source, issue, licence, or maintenance evidence was unavailable.

## Avoid these failure modes

- Recommending from prose while ignoring the live implementation.
- Producing a generic list of tools, models, or frameworks.
- Treating GitHub popularity or a README as production evidence.
- Recommending a whole dependency when only a pattern is transferable.
- Ignoring privacy, licensing, maintenance, or dependency costs.
- Assuming planned work or the current architecture is necessarily correct.
- Rebuilding commodity technology without proving an unmet need.
- Waiting indefinitely for research lanes instead of synthesizing available evidence and disclosing the gap.
