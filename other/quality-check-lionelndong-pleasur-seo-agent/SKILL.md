---
name: quality-check
description: The publish gate. Runs binary completeness floors, then a publish-BLOCKING uniqueness check (≥1 named information-gain element or hard FAIL — never clone page 1), then a skeptical 3-reviewer panel that decides whether the article beats the live #1 result. Emits PASS/FAIL — there is no score to game. PASS is required to publish; FAIL routes a revision or quarantines.
allowed-tools: Read, Write, Bash, Task
---

# Quality Check — the publish gate

The question is never "does the draft comply with our rules." It is: **a reader opens this
article and the current #1 result side by side — which one do they keep?** A perfectly
"compliant" draft that loses that comparison is a FAIL.

This gate has no 0–100 score, on purpose. A score invites gaming — a model will add numbers,
links, and headers to clear "85" without making the article better (that is exactly how thin
drafts used to pass at 85 while the adversarial read named five real weaknesses). Instead the
gate is three un-gameable parts, and **all must pass**:

1. **FLOORS** — objective completeness you can only satisfy by doing the work.
2. **UNIQUENESS** — a hard, publish-BLOCKING info-gain check: the article must carry ≥ 1 *named*
   information-gain element, or it FAILs outright (STRATEGY §5; Lesson 6 "never clone page 1").
3. **PANEL** — three skeptical reviewers who decide whether this beats what's ranking.

## Input

For slug `{slug}`:
- `content-pipeline/5-drafts/{slug}.md` (the draft; use `6-drafts-cited/{slug}.md` with `--stage cited`)
- `content-pipeline/1-research/{slug}.md` (**the BEAT SPEC + SERP benchmark — required**)
- `content-pipeline/3-outlines/{slug}.md` (coverage map)
- `brand-config.md` (forbidden phrases, audience, products)
- `examples/voice/*.md` (the voice the draft must match)

## Gate 1 — Floors (binary, mechanical)

```bash
python .claude/skills/quality-check/scripts/quality_check.py "{slug}"   # add --stage cited after /verify-claims
```

Writes `quality-checks/{slug}-metrics.md`; exits 0 (FLOORS_OK) or 1 (FLOORS_FAIL). Floors:
SERP benchmark present · depth ≥ 80% of SERP median · item count met · comparison table when
the SERP has one · **every** consensus topic covered · citations resolved (cited stage) · **no
internal tooling in the prose** (Semrush/Ahrefs/Strapi/etc.) · no forbidden phrases.

**Any failed floor → the gate FAILs.** Don't run the panel on a draft that fails a floor —
route the fix first: a missing topic or thin depth goes back to `/outline` or `/research`,
prose problems to `/draft`.

## Gate 1.5 — Uniqueness (the publish-BLOCKING info-gain gate)

**STRATEGY §5 + Lesson 6 "never clone page 1": this is a hard FAIL, not a warning.** Researching
everything on page 1 and squeezing it into one article only produces a *clone*, and a clone
doesn't deserve to outrank the original. Before the panel runs, the reviewer must **name** at
least one genuine **information-gain element** the article carries that the top 10 do **not**.
This also enforces the authors' craft-not-clone / original-only rule (`examples/authors.md`
Hard rule #2; STRATEGY §4).

The element must be **one of these four** (STRATEGY §5), and must actually be *in the draft*:
- **Our own data** — a stat, benchmark, or study we produced (e.g. a `:::methodology` + figures), not a number lifted from a competitor.
- **First-hand product testing** — a hands-on walkthrough/experiment of our own tool (or a tool the post covers), with specifics a reader couldn't get without doing it.
- **A sharper angle** — a genuinely better framing/explanation/synthesis the SERP lacks (not a paraphrase of the consensus take).
- **A 180° challenge to consensus** — a defensible contrarian position, argued with real reasons, against what page 1 agrees on.

**How to judge it (be skeptical, not generous):**
1. Open the draft against the dossier's **BEAT SPEC → "Information gain" / "Our-own-evidence" /
   "Angle"** lines (the uniqueness bundle `/research` step 8a locked) and the top-page summaries
   in `1-research/{slug}.md`.
2. Find the element in the *draft prose* and confirm it is **absent from the page-1 pages** —
   if the top results already have it, it is table-stakes coverage, not info-gain.
3. **Demand a REAL element, not a cosmetic one.** A qualifying element is one of: **our-own-evidence**
   (a cited aggregate PostHog/Stripe usage stat — never PII — or a genuine first-hand product test
   with specifics, or an aggregate-safe user story), **a 180° challenge to the page-1 consensus argued
   with real reasons**, or **a genuinely better explanation/synthesis** the SERP lacks. "We added a
   paragraph / a section / a list the others don't have" is **NOT** info-gain on its own — neither is
   a longer word count, more headers, or a restated take in fresh words. If the named element is just
   *more of the same coverage*, it FAILs.
4. **Name it explicitly** in the verdict block below: which of the four types, the exact section
   it lives in, and one sentence on why the SERP doesn't have it.

**A "unique element" that is really just (a) restated consensus, (b) a generic claim with no
data/test behind it, (c) an own-product price/feature assertion `verify-claims` hasn't confirmed
live, (d) something already present on page 1, or (e) a cosmetic add — an extra paragraph/section,
more words, or reordered consensus with no new data, test, contrarian argument, or better
explanation behind it — does NOT count.** When in doubt, it fails.

Write the result to `quality-checks/{slug}-uniqueness.md`:

```markdown
## Uniqueness: **PASS** | **FAIL**
- Element type: <own-data | first-hand-testing | sharper-angle | 180-challenge>
- Where: <H2/section it lives in>
- Why the SERP lacks it: <one sentence, grounded in the top-page summaries>
- Real, not cosmetic: <one sentence — why this is genuine info-gain and NOT just an extra paragraph/more words/reordered consensus>
- Shareability (Contagious): <which STEPPS principle(s) make it worth sharing/linking — Social currency / Emotion / Practical value / Story — or "none" if it's un-shareable (a weakness to flag)>
- (on FAIL) What's missing: <the named gap; route to /research for data/testing, /outline for angle/coverage>
```

**Gate 1.5 passes iff a reviewer can NAME ≥ 1 qualifying element. Absence = FAIL.** A FAIL here
short-circuits the gate — **do not run the panel** on an article with no information gain; route
the fix first (new data or a hands-on pass → `/research`; a genuinely new angle/section →
`/outline`). Never publish a clone.

## Gate 2 — Reviewer panel (the real signal)

Spawn **three independent `Task` sub-agents**, each a skeptical industry expert who has read
every page-1 result for "{keyword}". Give each the dossier (`1-research/{slug}.md` — note the
BEAT SPEC + top-page summaries), the draft, and 1–2 `examples/voice/` articles. Brand: {brand};
audience: {audience}. Each gets ONE lens:

- **Lens A — Competitiveness:** depth, specificity, usefulness vs the winners.
- **Lens B — Voice, readability & honesty:** does it read like the `examples/voice/` anchors (reader-felt,
  concrete, leads with the real decision) or like generic AI? Would a serious blog run it under
  a byline? **AND is it HONEST about our own product** — does it name real limits/tradeoffs instead of
  over-hyping? A salesy, over-promising, superlative-stacked piece **fails this lens**: it reads like
  marketing, not the trustworthy Ahrefs register, and erodes reader trust (STRATEGY #17). Flag any
  inflated claim, missing tradeoff, or hype word.
- **Lens C — Reader intent, information gain & shareability:** does it satisfy the searcher better
  than the SERP, and carry ≥ 1 genuine thing the top 10 don't have? **Plus a Contagious read
  (Lesson 7; `/contagious-why-things-catch-on`): would anyone actually share or link this, and which
  STEPPS does it hit — Social currency (does sharing it make the reader look smart/in-the-know?),
  Emotion (a surprising, high-arousal finding?), Practical value (a benchmark/yardstick they'd pass
  on?), or Story?** An article that satisfies intent but is forgettably un-shareable — nothing here
  earns a link — is a weakness to name, because un-shareable means no off-page lift (STRATEGY Lesson 7).
  Name the STEPPS principle(s) it hits, or flag that it hits none.

Each sub-agent answers in this exact shape:
> **VERDICT: KEEP_OURS | KEEP_COMPETITOR | TOSS_UP** — default to KEEP_COMPETITOR / TOSS_UP if
> unsure (be skeptical, not polite). Then: 3 sentences on why; the 5 weakest things vs what's
> ranking (specific sentences/sections); 1 thing that genuinely works.

Save all three to `quality-checks/{slug}-panel.md`. Distrust any all-praise verdict shorter
than 200 words — re-run that lens with a sharper brief.

**Gate 2 passes iff ≥ 2 of 3 say KEEP_OURS AND none says KEEP_COMPETITOR.** A single TOSS_UP is
tolerable; any KEEP_COMPETITOR fails the gate.

## Verdict

Write `content-pipeline/quality-checks/{slug}.md` with the verdict line FIRST:

- `## Verdict: **PASS**` — iff FLOORS_OK **and** Gate 1.5 (uniqueness) PASSES **and** Gate 2 passes.
- `## Verdict: **FAIL**` — otherwise (any one of the three failing fails the article).

Then: the floor-table summary, **the named uniqueness element (or the missing-info-gain reason
on FAIL)**, the three panel verdicts, and a **punch list** — specific fixes ordered by severity,
each pointing at a section, each tagged with a **route**: `/draft` for voice/prose, `/outline` or
`/research` for depth/coverage gaps **and for a missing information-gain element** (new data or a
hands-on pass → `/research`; a new angle/section → `/outline`) — never ask `/draft` to fix a
structural deficit or to invent info-gain.

## On FAIL

- **Autonomous mode (`BLOG_AGENT_AUTONOMOUS=1`):** don't stop — emit the verdict + routed punch
  list and return cleanly. The orchestrator owns the retry budget (`BLOG_AGENT_REVISION_BUDGET`,
  now **2**). When the budget is spent, the orchestrator writes `9-needs-review/{slug}.md` and
  moves to the next keyword — **never lower the bar or publish a FAIL.**
- **Interactive mode:** stop and report what failed and where to re-enter the pipeline.

## Why this gate exists

Ryan Law's quality guarantee is a human reading every article before it ships. We auto-publish,
so the panel is that human's stand-in: three skeptics who must agree the piece wins the
side-by-side. The floors guarantee they're judging a complete article, not a stub. The uniqueness
gate (1.5) guarantees they're never asked to bless a *clone* — STRATEGY §5's rule that nothing
ships without a named information-gain element is enforced here as a hard FAIL, so it can't be
voted away by a polite panel. No part emits a number — so there is nothing to optimize toward
except actually being better than, and different from, what's ranking.
