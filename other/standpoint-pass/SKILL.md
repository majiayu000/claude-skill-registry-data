---
name: standpoint-pass
description: >-
  "Who is most affected here, and what did the text do to them?" - Re-read
  primary material from the position of the most-affected, least-powerful
  party, and re-rank what matters by harm-to-the-many instead of
  offense-to-the-powerful. Use when (1) analyzing a speech, document, policy,
  or transcript whose salience was inherited from coverage (famous lines,
  viral clips), (2) a report ranks findings by scandal value, (3) closing any
  investigation whose subjects hold more power than the people affected,
  (4) an external correction showed the importance-ranking was tilted. Does
  NOT trigger for: technical/product analysis with no affected-party
  dimension, or pure verification of quotes and facts (use
  iterative-verification).
---

# Standpoint Pass

**Seed question:** *Who is most affected here, and what did the text do to them?*

> *Relentless self-reflexive dialectical thinking that questions its own premises.*

## Core Principle

Salience is inherited before reading begins: coverage, clipping, and quotation
have already decided which lines are "important". Importance under the question
actually asked — especially harm-to-the-many — has to be re-derived from the
primary text. The worst line by that measure is often phrased as kindness, which
is exactly why it survives passes tuned to offense. (Principle P3 (inherited-salience-is-not-importance); the standpoint injection is also the outside-control Principle P7 (blindness-is-not-independence) calls for.)

**The anti-pattern this counters:**
```
❌ Ranking findings by what made headlines
❌ "Nothing else stands out" after N passes that all started from the famous line
❌ A harm-detector tuned to offense-against-power, blind to harm-to-the-powerless
```

**The pattern this enforces:**
```
✅ Name the most-affected, least-powerful party BEFORE re-reading
✅ Re-rank every substantive line by harm-to-the-many, with the mechanism stated
✅ Check the kindness-phrased claims explicitly — that's where the worst line hides
```

## When This Applies

**TRIGGER:**
- Analyzing a speech, document, policy, or transcript whose importance was set
  by coverage — the famous lines, the viral clip, the quote everyone reacted to
- A report or draft ranks its findings by scandal value or headline potential
  rather than by who is harmed
- Closing an investigation whose subjects hold more power than the people the
  material actually affects
- An external correction or objection revealed the importance-ranking was tilted
  (pairs with iterative-verification's "external correction ⇒ regenerate")
- After several passes over a text that all still start from the same famous
  line and end at "nothing else stands out"
- A harm-detector that keeps surfacing offense-against-power while never
  surfacing harm-to-the-powerless
- The harm-standpoint reading points toward a conclusion favorable to a
  disfavored party (an adversary state, an accused figure) — the valence
  reflex suppresses exactly this reading before it forms; co-fire
  engage-the-disfavored

**DO NOT TRIGGER:**
- Technical, product, or engineering analysis with no affected-party dimension
- Pure verification of whether quotes and facts are accurate — that is
  iterative-verification's job (run it first; this pass re-reads what it confirmed)
- A text with no power asymmetry between its subjects and the people it affects

## The Pass

1. **Name the standpoint.** Identify the most-affected, least-powerful party in
   the material — a concrete group, not an abstraction. State why they qualify
   on both axes (most affected; least powerful).
2. **Re-read the primary text from that position.** Not coverage of it — the
   text itself.
3. **Re-rank.** List the substantive lines ranked by harm-to-the-many, each with
   its harm mechanism spelled out.
4. **Ask the kindness question.** "What claim does the text make about those at
   the bottom, phrased as kindness?" Quote the candidate passages; benevolent
   phrasing is a place to look, not a verdict.
5. **State what would move the ranking.** A falsifiable slot: what evidence or
   reading would change the order?

## Mandatory Output Slots

| Slot | Contents | Invalid when |
|------|----------|--------------|
| **Named standpoint** | The most-affected, least-powerful party, named concretely, with why they qualify on both axes | Names a powerful stakeholder; or an abstraction ("society", "the public"); or omits the why |
| **Re-ranked lines** | Substantive lines ranked by harm-to-the-many, each with its harm mechanism | Reproduces the coverage ranking; or asserts harm with no mechanism |
| **The kindness question** | "What claim does the text make about those at the bottom, phrased as kindness?" — answered with quoted text | Answered "none" without quoting the passages that were checked |
| **What would move the ranking** | Falsifiable: evidence or reading that would change the order | Empty, or "nothing" |

An output missing any slot, or with any slot in its invalid state, is not a
completed standpoint pass — say so rather than presenting it as one.

## Worked Example (fictionalized)

A finance minister of the invented state of Varenia gives a budget speech.
Coverage headlines a gaffe about the cost of her official car. The standpoint
pass names seasonal agricultural workers (most affected: the budget cuts their
injury insurance; least powerful: non-citizens, non-unionized). Re-ranked, the
worst line is phrased as kindness: *"we are freeing seasonal workers from
one-size-fits-all contracts"* — the mechanism being that "freeing" removes the
insurance mandate. The gaffe ranks last. What would move the ranking: evidence
that the insurance mandate is preserved in secondary legislation.

## Honest Limits

- The pass injects ONE standpoint; it does not enumerate all affected parties.
  Choosing the most-affected/least-powerful is itself a judgment — name the
  runner-up standpoints considered.
- A standpoint re-read is evidence about salience, not a verdict on the text.

## Cross-References

- **cui-bono** — the standpoint method here is the "Standpoint" contradiction
  method applied to *salience* instead of claims
- **iterative-verification** — run verification first; this pass re-reads what
  verification confirmed (verified ≠ understood)
- **source-omission-analysis** — omissions BY sources; this skill is about
  omissions BY the reader's attention
- **frame-rotation** — rotates grammar/language; this rotates the reader's
  position
- **engage-the-disfavored** — clears the valence gate beneath this pass: when
  the harm-reading lands adversary-favorable, the reflex that pre-discounts
  disfavored-side conclusions buries it; that skill forces the engagement
  this one re-ranks. In geopolitical cases, co-fire.

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.
