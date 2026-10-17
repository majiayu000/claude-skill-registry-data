---
name: positioning-doc
description: >-
  Write a product positioning document. Use when the user says "write a positioning doc",
  "positioning statement", "how should we position this product", "positioning for [product]",
  "we need to differentiate from competitors", "product positioning and messaging",
  "positioning workshop", "help me define our position in the market", or wants to establish
  how a product should be perceived relative to competitors.
  For customer-facing message wording, see messaging-framework. For the competitive research behind it, see competitor-analyst. For storing it in the knowledge base, see brand-context.
metadata:
  grounded_in:
    - "Positioning - Ries & Trout"
    - "Obviously Awesome - April Dunford"
  reads:
    - knowledge/icp/personas.md
    - knowledge/markets/competitors.md
  writes:
    - knowledge/markets/positioning.md
    - output/positioning-doc/
---

## Overview

This skill produces a positioning document that anchors all downstream messaging: the messaging
framework, the landing page, the ads, the sales deck. It is upstream of all of them, so a vague
positioning doc does not fail here, it fails four skills later.

## Where this method comes from

The five-step sequence below is **April Dunford's, from *Obviously Awesome* (2019)**. Dunford's
argument is that positioning is a set of five interlocking components, not a sentence, and that the
sentence is only the last thing you write. Run the components in order, because each one constrains
the next, and jumping straight to the market category is exactly how positioning statements end up
interchangeable between four competitors.

| Dunford component | The question it answers | Where it is worked below |
|---|---|---|
| Competitive alternatives | What would they use if we did not exist? | Step 1 |
| Unique attributes | What do we have that those alternatives do not? | Step 2 |
| Value | What can the customer do because of those attributes? | Step 3 |
| Customers who care most | Who finds that value urgent rather than nice? | Step 4 |
| Market category | What context makes the value obvious? | Step 5 |

The rule that the statement must not be claimable by a competitor without changing their product is
Dunford's falsification test, and it is the only hard gate in this skill.

**"Positioning: The Battle for Your Mind"** by Al Ries and Jack Trout (1981) supplies the older
discipline underneath it. Positioning is not what you do to a product, it is what you do to the mind
of the prospect. Three of their rules bind the steps below:

| Ries and Trout rule | Consequence in this skill |
|---|---|
| The first brand to own a concept in the mind wins | If a competitor already owns the attribute, you cannot take it by claiming it. Pick another, or reframe the category (Step 5) |
| You cannot be all things to all people | The doc is written for one primary segment only (Step 4) |
| Attacking the leader by name reinforces the leader | The leader is never named in the statement (Anti-pattern 1) |

## Before you write: is the input strong enough?

Positioning built on nothing propagates into every downstream asset, so check the input first.

| Signal | Threshold | If below |
|---|---|---|
| Named competitive alternatives, including non-product ones | 2 minimum | Stop. Ask the user, or run `/competitor-analyst`. A statement with one alternative is a feature claim |
| Differentiators that survive the "would they need a different product?" test | 1 minimum | Stop and say so plainly. Zero surviving differentiators is the finding, and it is more useful than a doc |
| Customers or prospects the segment claim is based on | 5 minimum | Proceed, but mark Step 4 `[ASSUMED: segment not validated against N customers]` |
| Sourced proof points for the owned attributes | 1 per attribute | Ship the attribute with the proofs you have. Never pad to three with invented ones |

Warning signs that the positioning is not real yet, in priority order:

1. Every differentiator in Step 2 also appears on a competitor's homepage. The doc is describing the category, not the product.
2. The user cannot name what a lost deal chose instead. Step 1 is guesswork, so Steps 2 to 5 inherit it.
3. The target segment is defined by company size alone with no trigger. That is a list, not a segment.
4. The statement still reads true if you swap in a competitor's name. It has failed the falsification test.

## Workflow

### Step 1: Define the competitive alternatives

Before writing anything, answer: what would your customer use if your product did not exist? This is not your competitor list - it is the actual behavior they would fall back to. Spreadsheets, a competitor's tool, doing nothing, hiring someone. List 2-4 concrete alternatives.

This matters because positioning is always relative. You cannot claim an attribute without implying "unlike [alternative]."

### Step 2: Identify your differentiated capabilities

List the specific features, behaviors, or properties your product has that the alternatives do not. Be ruthlessly specific. "Easier to use" is not a capability. "Runs in under 30 seconds without setup" is.

For each capability, ask: would a competitor have to make a different product to copy this? If yes, it is a real differentiator. If no, cut it.

### Step 3: Map capabilities to customer value

For each differentiator, state the concrete customer value it creates. Use this format:

| Capability | Customer Value |
|---|---|
| [specific product capability] | [measurable or tangible outcome for the customer] |

Aim for 3-5 rows. More than 5 means you have not prioritized.

### Step 4: Define the target customer segment

Ries and Trout: you cannot be everything to everyone. A narrow target is a strength, not a weakness. Define the segment by:
- Role or job title
- Company size or context (if B2B)
- Specific situation or trigger that makes them need this product
- What they are trying to accomplish (the job, not the persona)

If you have multiple segments, rank them. Write the positioning doc for the primary segment only.

### Step 5: Write the positioning statement

Use this template exactly:

> For [target customer] who [specific situation or need], [your product] is the [category] that [primary differentiator and value]. Unlike [primary alternative], [your product] [key point of difference].

Rules:
- One sentence per blank. No run-ons.
- The category must be recognizable - do not invent one unless you are deliberately creating a new market.
- The differentiator must be singular, not a list.

### Step 6: Define owned attributes and proof points

Pick 2-3 attributes your brand should own in the customer's mind. For each:

```
Attribute: [single phrase, e.g. "fastest time to first result"]
Proof points:
- [stat or fact]
- [customer quote or case study result]
- [product behavior or benchmark]
```

## Anti-Patterns

**1. Positioning against the market leader by name**
Bad: "Unlike [Market Leader], we actually have good customer support."
Good: "Unlike tools built for enterprise, [your product] is configured in a single afternoon - no implementation team required."
Naming the leader reinforces their position. The challenger wins by creating a new frame, not attacking head-on.

**2. Feature list as positioning**
Bad: "We have AI, integrations, real-time collaboration, and an API."
Good: "The only [category] built for [specific workflow] - so [target customer] stops switching between 4 tools."
Features are evidence. They are not the position.

**3. Positioning to everyone**
Bad: "Works great for teams of any size, in any industry."
Good: "Built for [specific role] at [specific company stage or type]."
Broad positioning is invisible positioning.

**4. Skipping the competitive alternatives step**
Bad: Positioning statement written without naming what the customer would actually use otherwise.
Good: Alternatives identified first - every claim is implicitly a claim against those alternatives.

## Self-check

Every item is checkable by reading the finished document, not by asserting it was done. Where an
item names a count, count it in the artifact.

- [ ] Step 1 lists 2 or more alternatives, and at least one is a non-product behaviour (spreadsheet, manual process, doing nothing, hiring someone)
- [ ] Every row in the Step 3 table has a filled Capability cell and a filled Customer Value cell, and the table has 3 to 5 rows
- [ ] Each Step 2 differentiator carries a one-line answer to "what would a competitor have to change to copy this?" written in the doc
- [ ] Step 4 names exactly one primary segment, with a role, a context and a trigger. If secondary segments are listed, they are under a heading marked "not the subject of this doc"
- [ ] The positioning statement contains all five template blanks filled, is one sentence per blank, and names one differentiator, not a list separated by "and"
- [ ] Falsification test recorded in the doc: paste the statement with a named competitor substituted, and a one-line verdict on whether it still reads true
- [ ] No competitor brand name appears anywhere in the statement itself
- [ ] Every proof point is quoted from a named source with its origin cited inline, or written as `[PROOF NEEDED: <what evidence would establish this>]`. An attribute with one sourced proof point ships with one, never with an invented second
- [ ] Count the `[ASSUMED]` and `[PROOF NEEDED]` markers and state the count at the top of the doc. If it is above 5, the doc is a draft and must be labelled one

## What this skill cannot know

These are the limitations that bite in practice. Where one applies to the artifact, write it into the document as an open question rather than leaving the reader to assume it was verified.

1. **Whether the customer's mind already has the position filled.** Ries and Trout's claim is about the prospect's head, and this skill only sees your side of it. Only unaided-awareness or win/loss research tells you whether an attribute is already occupied by someone else.
2. **Whether a differentiator is durable.** The falsification test asks whether a competitor would need a different product today. It cannot see their roadmap, an unannounced acquisition, or a feature shipping next quarter.
3. **Whether the category name is one buyers actually search and budget for.** A category is only useful if a buyer recognises it. Confirm against real search terms, analyst category names, or the words in sales call recordings before committing.
4. **Whether the proof points are true.** This skill can require a source and refuse to invent one. It cannot verify that a stat the user supplied is current, correctly measured, or legally safe to publish.

## Context and output

**Before you start.** Read `knowledge/icp/personas.md` for who the value is urgent to, and `knowledge/markets/competitors.md` for the alternatives. If either is missing, run `/brand-context` first or proceed and mark the affected sections `[ASSUMED]`.

**When you finish.** Save to `output/positioning-doc/<DD-MM-YYYY>-<company-slug>.md` with YAML frontmatter carrying the date, the skill name, and the key decisions made.

## Shared file ownership: knowledge/markets/positioning.md

**This skill owns `knowledge/markets/positioning.md`.** It owns the file's structure, section order,
and the positioning statement itself. `/messaging-framework` also writes to this file but is an
appender only, restricted to a `## Message hierarchy` section it may not extend beyond.

What this skill may do:

| Section | Allowed | Not allowed |
|---|---|---|
| Positioning statement, the five Dunford components, owned attributes, proof points | Replace in full | |
| `## Message hierarchy` (owned by `/messaging-framework`) | | Never edit or delete. Leave it in place and re-attach it below your sections |

The write gate, which is not optional:

1. Show the user a diff of the exact lines you would change in `knowledge/markets/positioning.md` before writing a single byte, and wait for an explicit yes. Six other marketing skills read this file as truth, so an ungated write turns one thin session into canon nobody can trace back.
2. If the `[ASSUMED]` and `[PROOF NEEDED]` count is 5 or higher, or fewer than 2 competitive alternatives were sourced, do not offer the write at all. Save to `output/` only and say plainly that the positioning is not yet canon.
3. Never invent a differentiator, a competitor capability, a market size, or a proof point to fill a gap in the file. An empty section with `[NEEDS INPUT: <what would fill it>]` is correct output.

## Related skills

- `/brand-context` for creating the persona and competitor files this skill reads, when the knowledge base is empty
- `/competitor-analyst` for when Step 1 has fewer than 2 sourced alternatives, or the differentiators need an ERRC grid and strategy canvas behind them
- `/customer-research` for when Step 4's segment claim is not backed by real customer conversations
- `/messaging-framework` for turning the finished statement into the customer-facing words, run after this skill, never before
- `/landing-page-writer` for putting the positioning on a page once the statement passes the falsification test
- `/copy-review` for checking whether live copy still carries this position after a repositioning
