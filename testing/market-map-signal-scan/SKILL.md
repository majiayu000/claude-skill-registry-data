---
name: market-map-signal-scan
description: Use when the user needs a consulting-style market analysis, market map, market sizing sanity check, competitive landscape, customer segment analysis, trend scan, opportunity gap assessment, category entry memo, startup idea validation, or strategic market attractiveness diagnosis. Use for turning messy public signals into a decision-ready view of where a market is moving, which segments matter, where competition is crowded, and what white spaces are credible.
---

# Market Map Signal Scan

Use this skill to convert broad market research into a decision-ready market map. The distinctive move is to triangulate market signals before making opportunity claims.

## Reference Loading

Read `references/github-patterns.md` when the user asks why this skill is differentiated from common GitHub agent skills or wants an open-source positioning angle.

Read `references/signal-taxonomy.md` when building a market signal scan, source plan, trend analysis, or uncertainty register.

Read `references/output-templates.md` when producing a full market map, category entry memo, competitor table, opportunity gap matrix, or source confidence register.

## Core Principle

Do not start with TAM. Start with market behavior.

A useful market analysis answers:

1. Who has the problem?
2. What are they already doing about it?
3. Which budgets, workflows, or habits are changing?
4. Which suppliers are gaining attention?
5. Which claims are proven, directional, or speculative?
6. What decision should the reader make next?

## Workflow

1. Define the decision.
   - Clarify whether the user is deciding to enter, invest, build, reposition, partner, price, or monitor.
   - State the geography, customer type, time horizon, and market boundary.
   - Write the 3-5 questions that would change the decision.

2. Draw the first market map.
   - Segment by buyer/job-to-be-done, not only by vendor category.
   - Identify incumbents, challengers, substitutes, complements, channels, and gatekeepers.
   - Mark where money, attention, and switching friction sit.

3. Collect and classify signals.
   - Demand signals: search interest, job posts, community pain, budgets, purchasing cycles, user complaints.
   - Supply signals: new entrants, funding, open-source activity, launches, pricing pages, partnerships.
   - Behavior signals: migration, usage patterns, review themes, workflow changes, willingness to pay.
   - Constraint signals: regulation, data access, integration cost, channel dependency, trust barriers.

4. Triangulate claims.
   - Require at least two independent signal types before treating a trend as credible.
   - Separate hype visibility from adoption evidence.
   - Label every major claim as proven, directional, weak, or unknown.

5. Identify market structure.
   - Determine whether the category is fragmented, consolidating, platform-led, services-led, compliance-led, or community-led.
   - Identify the basis of competition: cost, trust, workflow depth, data advantage, distribution, ecosystem, speed, or brand.
   - Mark bottlenecks that control adoption.

6. Find opportunity gaps.
   - Look for underserved segments, unbundled workflows, distribution gaps, trust gaps, integration gaps, pricing gaps, and compliance gaps.
   - Avoid claiming white space just because few vendors exist; test whether buyers care and can pay.
   - Convert each gap into a testable opportunity thesis.

7. Produce the decision output.
   - Executive answer.
   - Market map.
   - Signal evidence table.
   - Competitor and substitute landscape.
   - Opportunity gap matrix.
   - Recommended next tests.

## Signal Confidence

Use this confidence scale:

| Label | Meaning | What to do |
| --- | --- | --- |
| Proven | Multiple independent signals align and support real behavior | Use in recommendation |
| Directional | Signals point the same way but are incomplete | Use with caveat and next test |
| Weak | Signal is anecdotal, supplier-led, or unverified | Do not anchor the decision |
| Unknown | Evidence is missing or conflicting | Make it a research question |

## Opportunity Gap Tests

Before calling something an opportunity, test:

1. Pain: Is there repeated evidence of buyer pain or workflow friction?
2. Budget: Is there a clear budget owner or substitute spend?
3. Urgency: Why now, not later?
4. Access: Can a new entrant reach buyers through a realistic channel?
5. Defensibility: What improves with scale, data, trust, workflow depth, or ecosystem?
6. Timing: Is the market too early, active now, or already saturated?

## Default Output

```markdown
# Market Map: <Market / Category>

## Decision Context
- Decision:
- Scope:
- Time horizon:
- Key uncertainties:

## Executive Answer
<Recommendation or market read in 3-5 sentences>

## Market Structure
<How the market is segmented and where value/control sits>

## Signal Evidence
| Claim | Signal type | Evidence | Confidence | Implication |
| --- | --- | --- | --- | --- |

## Competitive Landscape
| Player / substitute | Segment | Positioning | Strength | Weakness | Watch item |
| --- | --- | --- | --- | --- | --- |

## Opportunity Gaps
| Gap | Buyer pain | Why now | Evidence strength | Next test |
| --- | --- | --- | --- | --- |

## Recommendation
<Enter / invest / build / partner / monitor / avoid, with rationale>
```

## Guardrails

- Do not present market size estimates without source, scope, and sanity checks.
- Do not confuse search interest, GitHub stars, funding, or media coverage with customer adoption.
- Do not call a segment underserved unless there is evidence of buyer pain and reachable demand.
- Do not overfit to one visible competitor; include substitutes and non-consumption.
- For investment, legal, regulatory, or financial decisions, frame the output as analytical support and state what must be verified by qualified professionals.
