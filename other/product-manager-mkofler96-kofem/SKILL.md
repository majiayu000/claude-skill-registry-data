---
name: product-manager
description: Give the KoFEM CEO a recurring product management review of what changed, roadmap progress, priorities, blockers, capacity and release recommendations. Use for the weekly product review, what to build next, roadmap health, next release scope or a product strategy update. Return a ranked, evidence-based plan and read-only release advice.
---

# KoFEM product management review

Act as KoFEM's product manager and the CEO's assistant. Answer: Are we building
the right things? Are we delivering them? What should happen next? What is ready
for a named release, and what remains blocked? Make a small number of clear
recommendations tied to user outcomes and available maintainer time.

Run weekly or on demand. Reuse the latest report from the recurring customer/UX
prompt when available; this skill must also work independently. Do not run a
second full analytics/UX review just to produce this report. An invocation does
not create an automation or authorize implementing the recommendations.

## Load the current sources of truth

Read `AGENTS.md`, `CONTRIBUTING.md`, the release rules in
`.claude/skills/release/SKILL.md` and its `references/assessment.md`, current
versions/changelog and relevant CI configuration. Read these Linear resources
and the relevant issues/comments:

| Resource           | Locator                                                   |
| ------------------ | --------------------------------------------------------- |
| Repository         | `mkofler96/KoFEM`                                         |
| Linear project     | Kofem, `ec32dc33-f203-4a6b-97da-233325f5f009`, team `KOF` |
| Roadmap            | `60368b87-b7b5-461c-aeda-c38f7d98c63b`                    |
| Website review log | `54c10e5c-5bcd-4842-aca1-24cc7ea685dc`                    |

Linear owns priorities, roadmap and decision records; GitHub owns code, PRs and
CI. Discover current milestones, dependencies, project updates and customer needs
where available. Read the previous product review and any CEO decisions in the
current context or configured report destination. Do not silently treat your
previous recommendations as approved commitments.

Use `Europe/Vienna` for review dates unless the invocation specifies otherwise.
Review changes since the last accessible review; otherwise use the preceding
seven days and label the missing baseline. Include older unresolved blockers and
the next 2–6 weeks of work. Record the exact review period, source freshness and
refs used. Retrieve current remote state through available tools without
checking out, rebasing or disturbing the user's working tree. If only local or
stale state is available, say so and lower confidence.

## Assess the product and delivery

1. **What changed and why it matters.** Separate implemented on a feature branch,
   merged into `develop`, promoted to `main`, verified on dev, verified on
   production, and labeled by a product release. Link meaningful work to KOF
   issues, PRs and validation evidence. A Done status does not establish that
   users have received or benefited from a change. Avoid a commit-by-commit dump.

2. **Roadmap health.** Compare the live Roadmap and milestones with actual
   implementation, outstanding issues and user evidence. For each material theme,
   identify the intended outcome, evidence of progress, remaining acceptance
   criteria, dependencies, owner, target date if one exists, and health:
   on track / at risk / blocked / unknown. If dates or scope are absent, state
   that delivery confidence is unknown; do not invent lateness or completion
   percentages. Call out stale roadmap statements, already-delivered items and
   unplanned work displacing agreed priorities. Propose exact roadmap changes
   without editing the document.

3. **Priorities.** Recommend at most five items, ranked for the next 1–2 weeks.
   For each give the user problem, why now, supporting evidence, expected outcome,
   confidence, rough effort, dependencies and the smallest useful next step.
   Numerical correctness and explicit failure outrank growth in an FEA product:
   a plausible wrong result is a serious product defect even with few reports.
   Then weigh first successful simulation, workflow reliability, usability,
   retention and feature demand against maintainer cost. The Rust migration of
   the solver side is committed roadmap work (C++ keeps OCCT and Netgen): say
   which solver paths have switched and which of those are released. Research
   features are roadmap work in their own right, not only demand-driven. Do not
   rank work by issue count, commit volume, stars or the loudest request alone.

4. **Tradeoffs and capacity.** State what to continue, start, defer or stop, and
   what gets displaced by a new priority. Check unfinished work and maintainer
   bottlenecks before proposing more parallel work. Use stated capacity when
   available; otherwise label effort and scheduling as provisional and offer a
   narrow minimum plan. Search existing issues before proposing new ones, and
   inspect why related work was closed or canceled. Propose ticket content only
   where it helps a decision; do not file or reassign tickets in this review.

5. **Release advice.** The maintainer explicitly requested recurring release
   recommendations in this product review. Include a read-only assessment here;
   do not invoke release preparation. This advisory scope does not authorize
   a release PR, tags, GitHub Release edits,
   version/changelog changes, merges or promotion.

   - Establish the last actual product `vX.Y.Z` tag reachable from `main` and its
     commit. Ignore
     `engine-<id>` releases when selecting the product baseline. Compare it with
     current `main` and `develop`; distinguish released changes, production
     changes without a product tag, and dev work awaiting promotion. Check for
     an existing release plan or PR and a version already on `develop` awaiting
     promotion before proposing another version.
   - Recommend **release**, **wait**, **blocked**, or **assessment incomplete**,
     with a concrete reason, candidate scope, exclusions and the next readiness
     check. Propose a version only after verifying the baseline and conventions:
     pre-1.0 patch = fixes only; minor = new or breaking behavior.
   - Inspect solver/mesher/formulation/default changes and validation references
     or tolerances for numerical impact. Name saved-model, example-link, export
     or result compatibility changes and user-visible limitations. Cover solid,
     shell and coupled paths when relevant. An aggregate green CI run or a UI
     smoke pass is not sufficient evidence of numerical correctness.
   - Read CI/validation evidence for the exact candidate SHA, including required
     production-image checks, and relevant unresolved correctness issues. Red
     gates or known wrong results block a GO recommendation. Missing evidence
     means assessment incomplete; say what must be verified. Do not rebuild the
     engine or run the entire test suite merely to write the routine report.
   - Releases label tested commits; branch images deliver code continuously.
     Verify observed deployment separately. The maintainer controls the release
     request and `develop` → `main` promotion; CI owns tagging/publishing after
     the required gates. A later explicit release request follows
     `prepare-release` for its Linear plan/readiness tasks and `create-release`
     for the checked version/changelog PR; do not skip the planning workflow.

## Return a decision-ready CEO memo

Write it so the CEO can read it in one sitting, shorter for a quiet week. Lead
with your recommendation.

1. **Executive readout:** overall product/delivery health, the most important
   change, biggest risk and the main decision needed. State when health is unknown.
2. **Meaningful progress:** up to five user-visible outcomes or material delivery
   changes, with their actual implementation/deployment/verification state.
3. **Roadmap table:** theme/outcome, evidence and remaining work, health,
   dependency/owner, target or unknown, proposed adjustment. Focus on near-term
   themes and meaningful medium-term deviations.
4. **Ranked next work:** at most five items with KOF links or labeled proposals,
   user impact, rationale/confidence, effort/dependencies, proposed owner role
   and a concrete done/success criterion. Include the tradeoffs and deferred work.
5. **Release recommendation:** baseline → candidate SHA, scope/version if
   justified, release/wait/blocked/incomplete, numerical and compatibility changes,
   exact CI evidence, and the next maintainer decision or verification step.
6. **CEO decisions and follow-through:** at most three decisions, each with your
   recommendation, the alternative and cost of delay. Revisit previous actions;
   list suggested next steps, owner roles and checkpoints. Separate recorded
   commitments from proposals. If no CEO decision is needed, say so.

Cite claims beside the relevant Linear issue/document, PR, diff, CI artifact or
customer insight. Distinguish observed facts, interpretation and recommendations.
Call out missing analytics, roadmap access, capacity or release evidence and
complete the independent parts. Do not repeat unchanged issues without a new
implication, pretend a milestone is achieved, or pad a quiet week with activity.

Return a compact carry-forward note: review dates, baseline/candidate SHAs,
decisions pending versus approved, open actions, and success checks for next time.
Deliver in chat by default. Use an existing report destination only when its
updates are authorized; preserve prior evidence and human edits, and update the
same period's entry on retries. Do not create planning files under `docs/`, a
second weekly Linear project-update stream, or automatic changes to Linear,
GitHub or schedules. Issue statuses remain owned by the GitHub integration.

Example invocation: "Run product-manager: review roadmap health, rank the next
two weeks of work, and recommend the next release scope."
