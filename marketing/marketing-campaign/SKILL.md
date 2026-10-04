---
name: marketing-campaign
description: End-to-end marketing campaign planning and execution — audience research, positioning, campaign angle, landing page copy, email sequences, social posts, ad copy, video scripts, and content calendars. Use when orchestrating a multi-channel product launch from one brief. Do NOT use for a single asset (content-engine for a post, article-writing for a piece, crosspost for distribution only) or for the underlying market study (market-research).
origin: ECC
---

# Marketing Campaign

Plan and execute launch campaigns that convert — not just campaigns that ship.

## When to use

- planning a product, collection, or feature launch
- building a full content suite from a single product brief
- defining positioning and campaign angle before any copy is written
- orchestrating multiple content types across channels
- reviewing an existing copy set for conversion quality and brand consistency

**When NOT to use:**

- the ask is one post, one thread, or one article — use `content-engine` / `article-writing`
- the ask is publishing already-written copy — use `crosspost`
- positioning is not settled and the user will not settle it. Copy written before the angle is
  approved gets thrown away; that is the most expensive failure in this skill

## Inputs

Required before Phase 3 — **absent input = stop, never assume**:

1. **Product truth.** For SkyyRose: SKU, name, price, and availability come from
   `wordpress-theme/skyyrose-flagship/data/skyyrose-catalog.csv`; imagery resolves only via
   `data/sot-images.json` / `skyyrose.core.sot_images` (filenames are not identity); collection
   language only from `docs/brand/collection-stories.md`. Never a product fact from memory.
2. **Audience research** — from `market-research`: jobs-to-be-done, fears, language, alternatives.
3. **Approved positioning and angle** (Phase 2 output). No approval → no copy.
4. **Voice profile** — from `brand-voice`, so every channel sounds like one author.
5. **A real deadline** if urgency will be used. Fake urgency is banned; without a real date the
   urgency beat is cut, not invented.

## Procedure

### Phase 1 — Research

Use `market-research` to profile the audience (jobs-to-be-done, fears, language, alternatives),
map 3+ direct or adjacent competitors (positioning, gaps, messaging weaknesses), and identify
1–3 insights the angle will exploit.
**Deliverable:** a research brief — audience profile + competitive summary + key insights.

### Phase 2 — Positioning

Produce: core benefit statement (one sentence, no feature list, no jargon) · positioning formula
`[Product] helps [audience] [achieve outcome] by [mechanism]` · campaign angle (the specific
tension, insight, or moment the campaign lives in) · tone profile (delegate to `brand-voice`).
**Do not write any copy until positioning and angle are approved.**

### Phase 3 — Content production

In this order — each layer informs the next:

1. **Landing page copy** — hero, problem, solution, features, how it works, proof, CTA
2. **Email sequence** — one purpose per email; arc: problem → education → agitation → solution →
   proof → urgency → final CTA
3. **Social posts** — platform-native via `content-engine` (LinkedIn and X are different formats,
   not the same copy resized)
4. **Short-form video scripts** — timestamp-blocked, written for screen and ear
5. **Ad copy variants** — 3–4 testing different angles or audience segments
6. **Content calendar** — day-by-day: channel, type, timing, dependencies

Write each deliverable to its own file so the Verification checks have real targets.

### Phase 4 — Review, then hand off

Gate every deliverable: 5-second test on all hero / above-fold copy · CTA audit (one per piece,
specific, earned) · tone consistency across channels · claim audit (every claim specific and
supportable) · cross-channel consistency (ad claims match landing page; email body matches
subject). Anything paid, published, or written to production goes through the owning skill's
STOP-AND-SHOW gate — this skill produces copy, it does not spend money or publish.

## Output contract

1. Positioning brief — angle, core benefit statement, tone profile
2. Landing page copy — all sections
3. Email sequence — subject + preview + body + CTA per email, labelled by day and purpose
4. LinkedIn posts — 3+ platform-native, distinct angles
5. X posts — 5+ standalone + 1 thread
6. Short-form video scripts — 2+ timestamp-blocked with visual direction
7. Ad copy variants — short headline / long headline / body per variant
8. Content calendar — day-by-day with channel, type, timing, dependencies
9. Copy review summary — flagged issues and open questions before anything goes live

# Verification

Run across the whole deliverable set, not one file. A check that errors on a missing file exits
2 — a dead gate, not a pass (bug-230).

1. **No verbatim reuse across channels** — the consistency rule made falsifiable:

```bash
sort landing-hero.md email-01.md x.txt linkedin.txt | uniq -d | grep -v '^[[:space:]]*$'
```

   **PASS:** no output (final grep exits 1). Any returned line is copy-pasted between two
   channels; rewrite one. `[repro]`

2. **Hard-banned language is absent everywhere**:

```bash
grep -rnEi 'game.chang|revolutionar|world.class|cutting.edge|competitive landscape|learn more|click here|thousands (of )?(people |customers )?trust' ./campaign/
```

   **PASS:** exit 1, zero matches across the whole campaign directory. Every hit is deleted and
   rewritten, not softened. `[repro]`

3. **Every claimed number is sourced** — stops invented traction and invented pricing:

```bash
grep -rnE '[0-9]+(\.[0-9]+)?%|\$[0-9]' ./campaign/ | grep -v 'Source:'
```

   **PASS:** exit 1, no lines returned. `(Source: catalog CSV)` or
   `(Source: operator-supplied; unverified)` are acceptable labels; silence is not. `[repro]`

4. **Price/SKU claims match the catalog** — the SOT, not memory:

```bash
grep -n '<sku>' wordpress-theme/skyyrose-flagship/data/skyyrose-catalog.csv
```

   **PASS:** the row exists and its name/price match every mention in the campaign copy. No row
   → the product claim is deleted, not approximated. `[repo]`

Prove check 1 can fail before trusting it (rule 3): copy one hero line verbatim into an email,
confirm `uniq -d` returns it, restore. Observed in the worked example.

**A SKIP is not a PASS.** The 5-second test and tone-consistency read are human judgments — no
command grades them. State explicitly that they are open and name the reviewer who closes them,
rather than letting the mechanical greens imply the whole gate passed.

## Worked example

Real run, 2026-07-28, a Black Rose one-run drop campaign. Two deliverables written to the session
scratchpad: `landing-hero.md` ("Armor for the people the concrete raised. / Black Rose. One run.
No restock.") and `email-01.md` ("You stood up first. The coat is the receipt. / Black Rose goes
live tonight at 7pm PT."). The hero line is derived from Black Rose canon in
`docs/brand/collection-stories.md` `[repo]`.

```bash
$ sort landing-hero.md email-01.md | uniq -d | grep -v '^[[:space:]]*$'; echo "exit=$?"
exit=1
```

Zero verbatim overlap `[repro]` — same angle, different sentences, which is the contract.

The number-sourcing gate was proven red first in the same run, on a sibling research file:

```bash
$ grep -nE '[0-9]+(\.[0-9]+)?%|\$[0-9]' research-brief.md | grep -v 'Source:'
3:- Average luxury-streetwear AOV is $240
```

After labelling that line `(Source: operator-supplied; unverified)`, the same command exits 1
`[repro]`. Open items from this run: the 5-second test and tone read on the hero are unclosed and
owned by the requester — mechanical greens do not close them.

## Failure modes

| Failure | What it looks like | Rule |
|---|---|---|
| Copy before approved positioning | drafts written, angle changes, everything rewritten | Phase 2 gates Phase 3. Do not start copy until the angle is approved |
| Invented product facts | price, drop date, or SKU stated from memory | bug-096 shape. Catalog CSV is the only manifest; `data/sot-images.json` the only imagery source — filenames are not identity |
| Mixed collection canon | Love Hurts "bloodline" language on a Black Rose asset | Each collection has its own locked canon; Black Rose = armor / "the concrete answering back" |
| Verbatim reuse across channels | the ad headline is also the email subject and the hero | Check 1. Same voice, different sentences |
| Fake urgency | a countdown with no real deadline | Banned. No real date → cut the urgency beat |
| Hollow proof | "thousands trust us" | Check 2 catches it. Specific and supportable or gone |
| Generic CTA | "learn more", "click here" | Check 2 catches it. Every CTA is specific and earned |
| Interchangeable copy | the campaign would work for a competitor unchanged | Rewrite. Specificity beats adjectives on every channel |
| Mechanical greens read as full pass | "campaign verified" with no human tone read | A SKIP is not a PASS — name the open judgments and their owner |

## Related skills

`brand-voice` (run before content production) · `content-engine` (platform-native production) ·
`crosspost` (distribution) · `market-research` (audience + competitive intelligence) ·
`seo` (landing page on-page optimisation)
