---
name: opportunity-solution-tree
description: "Builds an Opportunity Solution Tree (OST) - desired outcome at the top, prioritized opportunities, candidate solutions, and assumption tests that connect discovery work to a measurable business outcome. Use when planning continuous product discovery; deciding what to research next; structuring quarterly discovery work; or aligning a product trio (product manager / designer / engineer) on what to test."
---

# Opportunity Solution Tree

> The connective tissue between a business outcome and the experiments that move it.

## What this skill is

A workflow for building an Opportunity Solution Tree (OST) - the discovery framework popularized by Teresa Torres that anchors discovery work to a clear outcome, surfaces opportunities (unmet customer needs, pain points, desires), generates multiple solution candidates, and identifies the assumption tests that need to run before committing. Produces a living artifact a product trio can update weekly.

## What it solves

- Discovery work that wanders without a measurable outcome
- Premature commitment to one solution without exploring alternatives
- Building features before validating the underlying opportunity
- Confusion about which assumption to test next
- Roadmaps that conflate outputs (features shipped) with outcomes (customer behavior changed)

## When to invoke

- Starting a new discovery cycle for a product area
- Restructuring a quarterly plan that's grown feature-heavy
- Deciding what to research next when multiple opportunities compete
- Onboarding a new product trio to a shared discovery model
- Reviewing why a shipped feature didn't move the outcome

## Phase 1: Define the outcome at the top

The root of every tree is a **single, measurable outcome** - a customer behavior the business cares about.

Outcome statement format:
> Increase [metric] from [baseline] to [target] by [date].

Rules for a good outcome:
- It is a behavior, not a feature ("more activations" not "ship onboarding v2")
- It is measurable today (you can see the baseline)
- It has a target - vague aspirations hide trade-offs
- It is owned by the product trio for the cycle

If the outcome is a business Key Performance Indicator (KPI) such as revenue or retention, restate it as the **leading customer behavior** that drives it.

## Phase 2: Map opportunities

Opportunities are customer **needs, pain points, and desires** - never solutions. Source them from:
- Customer interviews (continuous discovery weekly cadence)
- Support tickets, Net Promoter Score (NPS) verbatims
- Sales call recordings
- Behavioral analytics (funnel drop-offs)
- Internal observation (customer success escalations, churn calls)

For each opportunity, write:
- A short title in the **customer's voice**
- Source citations (which interview, which ticket)
- The job stage it sits in (using the job map from the Jobs-to-be-Done (JTBD) skill)

Structure the opportunities into a tree:
- **Parent opportunities** are broad (e.g., "It's hard to know if I'm making progress")
- **Child opportunities** are specific instances (e.g., "I lose track of where I left off when I switch devices")

A tree with only parents is too abstract to act on. A tree with only children misses the synthesis.

## Phase 3: Prioritize opportunities

Score each opportunity on:
- **Reach** - how many target customers experience this?
- **Severity** - how painful when it happens?
- **Strategic alignment** - does solving it support the outcome at the top?
- **Confidence** - how sure are we, based on evidence?

Use a 2-by-2 matrix of **opportunity size × strategic alignment**. Pick **one opportunity** per cycle for the trio to focus on. Multiple parallel opportunities dilute discovery.

## Phase 4: Generate solution candidates

For the chosen opportunity, brainstorm **at least 3-5 solution candidates**. The first solution is almost never the best.

Solution-generation prompts:
- Magic wand: if there were no constraints, what would solve this?
- Borrow from another industry: how does X industry solve a similar pain?
- Inverse: what's the smallest change that could help?
- Service-not-software: what if a human did it?
- Existing-flow: what change to a current flow would do it?

For each candidate, write a 1-paragraph description and a sketch (Loom video, Figma frame, or rough wireframe).

## Phase 5: Identify assumption tests

For each solution candidate, list the assumptions that must be true for it to work. Use the four risk categories described by Marty Cagan:

| Risk | Question |
|------|----------|
| Value | Will customers use it? |
| Usability | Can they figure out how to use it? |
| Feasibility | Can we build it with available technology and time? |
| Business viability | Does it work for legal, sales, support, and finance? |

For each assumption, design the **cheapest possible test**:
- Survey, prototype test, fake-door experiment, concierge Minimum Viable Product (MVP), A/B test, technical spike
- Define the success and kill criteria **before** running the test

Run the test. Update the tree weekly.

## Phase 6: Tree maintenance

The OST is a living artifact, not a one-time deliverable:
- Weekly trio meeting reviews the tree
- New customer signals add or refine opportunities
- Failed assumption tests prune solution branches
- Successful tests advance solutions toward delivery
- Outcome at the top is revisited each cycle

## Output

- One outcome at the root of the tree
- 5-15 opportunities organized parent → child
- One prioritized opportunity for this cycle with reasoning
- 3-5 solution candidates per chosen opportunity
- Assumption-test plan for each candidate with success criteria
- Living artifact (Mural, Miro, FigJam) with edit history

## Operating rules

**Always**
- Anchor the tree on a measurable customer outcome
- Write opportunities in the customer's voice
- Generate at least 3 solution candidates before committing
- Define kill criteria before running an assumption test
- Update the tree weekly with the trio

**Never**
- Put solutions in the opportunity layer
- Pursue more than one opportunity per trio per cycle
- Ship without testing the highest-risk assumption
- Treat the tree as a static deliverable
- Confuse a feature output with a behavior outcome
