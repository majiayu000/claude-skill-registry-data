---
name: product-hacking-loop
description: Runs a ChefFlow product hacking loop that dogfoods workflows, attacks assumptions, captures evidence, ranks friction, and converts validated findings into build-queue-ready recommendations. Use when the user asks to hack, stress-test, dogfood, improve, inspect, pressure-test, find hidden product gaps, or make ChefFlow better through internal product testing.
---

# Product Hacking Loop

## Mission

Run an ethical internal product hacking pass on ChefFlow.

The goal is to make the product better by using it like real users, attacking weak assumptions, finding hidden workflow friction, and turning proven findings into queue-ready recommendations. This is not a generic idea dump and not an automatic implementation trigger.

Think like a combined dogfood team, red team, growth team, support analyst, product manager, and chef-operator.

## Guardrails

- Respect ChefFlow's Build Queue First rule. Do not edit application code unless the user explicitly authorizes a queue fire, direct hotfix, or says not to queue.
- Prefer evidence over opinion. Use screenshots, route checks, code references, console/network/runtime observations, support notes, or workflow traces when available.
- Keep the loop scoped. If the user names a route, workflow, persona, or feature, stay there.
- Do not turn every annoyance into a build item. Separate defects, missing controls, confusing UX, business opportunities, and ideas that should not be built yet.
- Do not use dark patterns, deceptive tests, privacy-invasive tactics, or unsafe production mutations.
- For live app or third-party inspection, use `live-browser-experience-audit` when available.
- For missing buttons/actions, use `action-surface-audit` when the core question is actionability.
- For bug-pattern scanning, use `bug-taxonomy-audit` when the core question is defects or regressions.
- For suspected blame-shifting from a downstream feature to an upstream system problem, use `feature-innocence-audit`.
- For queue reconciliation or batching, use `queue-groomer`.

## Routing Gate

Classify the request before doing work:

- **Product hacking report**: User asks to hack, dogfood, stress-test, inspect, pressure-test, or find product gaps. Produce findings and recommendations.
- **Specific workflow pass**: User names a route, feature, persona, or workflow. Test only that surface and its immediate dependencies.
- **Queue shaping**: User asks to queue, save, backlog, batch, or defer. Shape findings into build-queue-ready items and add only when explicitly requested and specified enough.
- **Direct implementation**: User says "fire the queue", "build the queue", "execute this queue item now", "direct hotfix now", or "do not queue this". Follow normal implementation and finish-gate rules.
- **Unclear scope**: Ask the fewest questions needed to know the surface, persona, and evidence depth.

## Product Hacking Loop

1. **Frame the run**
   - Target surface or workflow.
   - Primary persona: chef, client, consumer, admin, staff, partner, or product owner.
   - Job to be done.
   - Success criteria.
   - Evidence sources allowed.
   - Privacy/action boundaries.

2. **Dogfood the workflow**
   - Walk through the real task from start to finish.
   - Note where the user must leave context, guess, copy data, wait, repeat work, or manually reconcile information.
   - Check first-use, repeat-use, empty, loading, error, stale, partial, permission-blocked, and success states when relevant.

3. **Attack assumptions**
   - What happens with missing, duplicated, stale, contradictory, or low-confidence data?
   - What happens under mobile constraints, slow network, short time, client pressure, or last-minute event change?
   - What would a confused user click?
   - What would a power user expect to do faster?
   - What would a malicious or unauthorized user try?
   - What operational failure would make this workflow embarrassing in real chef work?

4. **Mine friction**
   - Dead ends, missing next actions, weak labels, hidden controls, slow paths, unclear ownership, missing proof, no recovery path.
   - Signals with no action.
   - Actions with no confidence, urgency, state, history, or destination.
   - Repeated manual work that should become automation or a reusable command.
   - Support questions that should become product surfaces.

5. **Sort findings**
   - **Defect**: Something is broken, insecure, misleading, inaccessible, or regressively worse.
   - **Workflow gap**: A real task cannot be completed cleanly.
   - **Action gap**: The user can see something but cannot act in context.
   - **Trust gap**: The user cannot tell source, freshness, confidence, owner, or consequence.
   - **Growth gap**: The product loses activation, retention, conversion, or expansion opportunity.
   - **Operational gap**: ChefFlow fails a realistic chef/client/business scenario.
   - **Do not build yet**: Interesting, but unproven, low leverage, too broad, or better handled manually.

6. **Convert only validated work**
   - Preserve the raw observation.
   - State the user pain and business impact.
   - Define smallest useful scope.
   - Write acceptance criteria and verification steps.
   - Name dependencies, risks, route/auth/tenant implications, and proof needed.
   - Recommend queue item priority and batch only after the finding is specific enough.

## Evidence Checklist

Use the smallest evidence set that proves the point:

- Route/page inspected and URL.
- Screenshot, recording, or explicit visual observation for UI findings.
- Console, network, or server log notes for runtime issues.
- Code references for implementation or wiring claims.
- User-flow transcript for workflow findings.
- Data-state examples for stale, empty, duplicate, or partial-state findings.
- Before/after expectation for proposed fixes.

## Scoring

Score each finding:

- **Impact**: user/business value if fixed.
- **Urgency**: how soon it damages trust, conversion, retention, workflow completion, or safety.
- **Confidence**: strength of evidence.
- **Effort**: expected implementation size.
- **Blast radius**: affected routes, roles, data, and systems.

Recommended priority:

- **P0**: Security, tenant isolation, data loss, unusable core workflow, severe regression.
- **P1**: High-value workflow blocked or major trust/action gap.
- **P2**: Important polish, discoverability, speed, or conversion improvement.
- **P3**: Nice-to-have, speculative, or better saved for later.

## Output Format

Use this structure unless the user requests a different format:

```md
## Product Hacking Run

- Target:
- Persona:
- Job to be done:
- Evidence used:
- Boundaries:

## Findings

### 1. [Finding title]

- Type:
- Priority:
- Evidence:
- What failed:
- Why it matters:
- Recommended response:
- Queue-ready scope:
- Acceptance criteria:
- Verification:
- Risks/dependencies:

## Quick Wins

[Smallest high-confidence improvements, if any.]

## Do Not Build Yet

[Ideas rejected or deferred, with reason.]

## Recommended Batch

[Smallest set of queue candidates that creates the broadest product lift.]
```

## ChefFlow Closeout

If the user wants findings saved, add them to the build queue only when they are specified enough to be useful. If they are still broad, ask concise spec questions first.

If the user authorizes implementation, follow ChefFlow firing rules, dirty workspace protection, canonical dev server policy, security/auth invariants, proof-pack expectations, and finish-check requirements.
