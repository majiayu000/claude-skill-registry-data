---
name: ai-stakeholder-translator
description: "Translates one product update, decision, or launch plan into five audience-tailored communications - engineering update, executive summary, board narrative, customer changelog, and sales enablement brief - with the same core facts and sensitivity-checked content in each. Use when announcing a launch or major release to several audiences; communicating a roadmap change, delay, or descoping decision; preparing board and executive updates from the same source material; or turning an internal decision into customer-facing and sales-ready messaging."
---

# AI Stakeholder Translator

> One input, five outputs: the same facts, framed for the people who need to act on them.

## What this skill is

A communication multiplexer for product managers. It takes a single piece of product information, extracts the core facts once, classifies what each audience is allowed to see, and then generates five versions tuned to each audience's priorities, vocabulary, preferred metrics, and attention span. Because every version is derived from one fact base, the story stays consistent no matter who forwards what to whom.

## What it solves

- Five separately written updates that drift apart and contradict each other on dates, scope, or numbers
- Engineering detail leaking into executive or board updates that need outcomes, not implementation
- Internal timelines, revenue figures, or unreleased roadmap items leaking into customer or sales material
- Customer changelogs written in internal jargon that customers cannot parse
- Sales teams learning about a launch from the changelog, with no talking points or objection handling
- Board narratives that report activity instead of connecting to a strategic theme

## When to invoke

- A feature, release, or launch needs to be announced to engineering, leadership, the board, customers, and sales
- A roadmap change, delay, or descoping decision has to be communicated without spin or inconsistency
- A quarterly or monthly update must be cut for both the executive team and the board
- An internal decision record needs to become customer-facing release notes and a sales brief
- A product manager wants a consistency check on messaging before sending anything

## Phase 1: Intake and core message extraction

Before writing anything, reduce the input to a fact base that every output will draw from.

| Element | What to capture |
|---------|-----------------|
| Core fact | One sentence: what happened or what was decided |
| Impact magnitude | Who is affected, how many, how much it matters |
| Timeline | Dates for availability, rollout stages, or decision effective date |
| Business metrics | Revenue, retention, conversion, adoption, or cost effects |
| Technical metrics | Latency, reliability, performance, scope of change |
| Open risks | Known issues, dependencies, or things that could still slip |

If any element is missing, ask for it or mark it explicitly as unknown. Never invent a metric to fill a gap.

## Phase 2: Sensitivity classification

Tag every fact in the fact base with one of three levels before it is allowed into any output.

| Level | Typical content | Allowed audiences |
|-------|-----------------|-------------------|
| All audiences | Shipped features, public benchmarks, general availability dates already announced | All five |
| Internal only | Internal timelines, resource constraints, internal metrics, known bugs | Engineering, executive, board, sales (with care) |
| Restricted | Unreleased roadmap dates, revenue numbers, pricing not yet public, customer names under Non-Disclosure Agreement (NDA) | Executive and board only |

When the level is unclear, default to the more restrictive one and flag it for the owner.

## Phase 3: Audience profiles

Each output is shaped by what its audience cares about and how they consume information.

| Audience | Channel | Length | Leads with | Vocabulary |
|----------|---------|--------|------------|------------|
| Engineering team | Team chat or email | 5-10 bullets | What changed, why, what it touches | Technical, direct |
| Executive team | Email or direct message | 3-5 sentences, under 150 words | Outcome and business impact | Outcome-oriented |
| Board | One slide plus speaker notes | Slide under 30 words; notes under 100 words | Strategic thesis | Strategic, metric-anchored |
| Customers | Changelog or release notes | One paragraph | User benefit | Plain language, zero jargon |
| Sales | Enablement brief | One page | Why it wins deals | Benefit and competitive framing |

## Phase 4: Generate the five outputs

Produce all five from the classified fact base:

1. **Engineering team update** - what shipped or changed, the reasoning, affected systems, follow-up work, and owners
2. **Executive summary** - the outcome, the business impact, the key risk, and any decision or support needed
3. **Board narrative** - a slide headline tied to a strategic theme, plus speaker notes that explain why it matters for the company's trajectory
4. **Customer changelog** - what the customer can now do, framed as a benefit, with any action they need to take
5. **Sales enablement brief** - an elevator pitch, 3-5 talking points, at least two objection-and-response pairs, and competitive positioning

## Phase 5: Consistency and leak check

Run every output against the fact base before handing it over.

| Check | Pass condition |
|-------|----------------|
| Fact consistency | All five outputs state the same dates, scope, and numbers |
| Sensitivity | No restricted content in customer or sales outputs; no internal-only content in the customer output |
| Length limits | Executive summary under 150 words; board slide under 30 words |
| Strategic link | Board narrative names the strategic theme it advances |
| Jargon | Customer changelog contains no internal terms, code names, or acronyms without explanation |
| Sales readiness | Sales brief has at least two objection-and-response pairs |

Report any check that fails and the fix applied.

## Output

- Fact base with sensitivity level tagged on each item
- Engineering team update
- Executive summary
- Board slide and speaker notes
- Customer-facing changelog entry
- Sales enablement brief with talking points, objection handling, and competitive positioning
- Consistency and leak check results

## Operating rules

**Always**
- Extract and classify the fact base before writing any output
- Derive every output from the same facts so numbers and dates match
- Lead each output with what that audience cares about most
- Default to the more restrictive sensitivity level when in doubt
- Flag missing facts as unknown instead of filling them in

**Never**
- Put restricted content in customer or sales material
- Invent metrics, dates, or customer quotes to make a version more compelling
- Let the customer changelog carry internal jargon or code names
- Soften bad news in one version while stating it plainly in another
- Skip the consistency check because the outputs "look right"
