---
name: news-feed-quality
description: Run the news-card iteration loop — capture fixtures, run the live cycle, show every card whole, fix what blocks the target card, merge, repeat. Invoke when the operator says "run the news loop", names an iteration number or budget, or asks to improve what news.html's cards say.
---

# news-feed-quality — the news card, and the loop that gets it there

news.html ingests public articles, synthesises facts from them, and enriches the graph from
supplemental sources so more of each article can ground — the grounding then enriching the
article. This skill is the loop that improves what those cards actually say, measured against
one hand-written target card (§2) rather than against a score.

> **Invoke it by telling a session:** *"Follow the `news-feed-quality` skill"*, optionally naming
> an iteration number or budget ("run iterations 14 to 18").

## What this skill is for

One iteration is: run the cycle, show every card whole, read the worst gap against the target,
fix its cause, merge, repeat. Minutes per pass. Use it for routine improvement of the news
feed's output quality — the words on the card, not the throughput.

Depth comes from repeating the same loop against fresh live data, not from breadth across
sources. The measuring stick never changes.

## 0. Ground rules

- **Coordinator model, unlike the playtest loop.** The run and the reading happen on the main
  thread; fixes go to background sub-agents with disjoint file ownership, as many at once as
  have genuinely separate files. This is CLAUDE.md's standard model — the loop is not serial,
  because a run scores everything merged since the last one.
- **Show every card, verbatim and complete.** No selection, the worst included. A loop that
  reports a summary instead of the cards has stopped being this loop.
- **The next run is the measurement.** Never ask a change agent for a before/after benchmark —
  the following cycle scores everything merged. Change agents measure their own specimens, not
  the feed.
- **Never wait on a pipeline or a deploy.** CI and deploys are shipping, not gates.
- **A lookup miss is a miss.** Enrichment writes facts and never invents them. An item with no
  claim in it produces no fact: the honest miss applies to news exactly as it does to chat.
- **Regression floors ride the test suite** so a landed win cannot silently unwind.

## 1. The loop

Repeat until a stop condition (§7) fires:

1. **Run.** `node scripts/news-bench/capture-fixtures.mjs` when fresh articles are wanted, then
   `node scripts/news-bench/run-live-cycle.mjs` (§3).
2. **Show.** Every card into chat, whole, in the four-part form, plus the scores (§4). This is
   the step the loop exists for; it is not a formality.
3. **Read the worst gap** against the target card (§2). One gap, named at its cause, not a list
   of symptoms.
4. **Fix it** (§5) — main thread if small, sub-agents if the tracks have disjoint files.
5. **Merge** as each track lands, and update `NEXT.md` in the same breath (§6).
6. Go to 1. The next run scores what just merged.

## 2. The target card — the measuring stick

Hand-written against a real article from the 2026-08-12 fixtures. Every sentence is one the
templates can genuinely build; nothing here is aspirational prose.

> ### nigel farage
>
> **Nigel Farage forced a new election in Clacton.** Farage came under pressure over
> his finances. His main challenger is Count Binface, a novelty candidate.
>
> *what the graph already knew:* Nigel Farage is a British politician. He leads
> Reform UK. Clacton is a town in Essex, England. Clacton is a parliamentary
> constituency of the United Kingdom.
>
> **the report as filed:**
> > **How Nigel Farage Ended Up Running Against Count Binface in Clacton**
> > Nigel Farage forced a new election in his parliamentary seat after coming under
> > pressure over his finances. His main challenger is Count Binface, a novelty
> > candidate.
> > — NYT World News, 2026-08-12

Where each part comes from:

| part | source | step |
| --- | --- | --- |
| "Nigel Farage forced a new election in Clacton." | synthesised fact, place attached | ingest |
| "Farage came under pressure…" / "His main challenger is…" | further facts from the description's own sentences | synthesise |
| "Nigel Farage is a British politician. He leads Reform UK." | reference lookup on the whole name **nigel farage** | enrich |
| "Clacton is a town in Essex…" | reference lookup on **clacton** | enrich |
| the report block | the article itself | ingest |

Read every run against this card. "Better than last time" is not the bar; "closer to this" is.

## 3. Running a cycle

```bash
node scripts/news-bench/capture-fixtures.mjs     # fresh articles, when wanted
node scripts/news-bench/run-live-cycle.mjs       # poll → synthesise → enrich live → build cards
```

- `capture-fixtures.mjs` refetches the live sources and **moves the ground under any before/after
  comparison** — never run it in the middle of one. A change agent measuring its own specimen
  must not run it at all.
- `run-live-cycle.mjs` starts fresh state each run, so the negative cache resets and the same
  misses re-burn lookup slots every time. The deployed worker persists state and does not — a
  miss repeating across runs here is not evidence it repeats in production.
- `iterate.mjs --label=<x>` is the separate metrics/report lane, not this loop.
- `ensure-bench-inputs.mjs --from <checkout>` builds a fresh worktree's seed and packs in
  seconds. A sub-agent whose worktree is missing `public/chat-seed.json` needs this before the
  cycle will run at all.
- Tee any run you intend to filter: `... 2>&1 | tee /tmp/iterN.log | tail -40`.

## 4. What "show every card" means

Each card, verbatim, in the four-part form:

- **OUR PARAGRAPH** — the card's own prose
- **FACTS LEARNED** — the triples this article produced
- **RELATED FACTS ALREADY HELD** — with each fact's source labeled
- **ORIGINAL TEXT** — headline, description, source, date

Then the scores that matter, which are about admission rather than volume:

- terms defined by enrichment, out of terms looked up
- article facts grounded because of that enrichment
- cards with real background, and cards that are thin
- **admission per source** — items polled, grounded, carded, and how many of those cards have
  something to say

A thin card is one whose only claim restates its own headline. Thin cards are ranked last and
counted, never dropped: dropping them hides a miss instead of fixing it.

## 5. Choosing the fix

Fix the first thing that blocks the target card, **at its cause**. The recurring lesson from
this loop is that the visible symptom is usually downstream of the real defect:

| symptom on the card | where the cause usually is |
|---|---|
| a hub that is an adjective or a torn headline fragment | the entity/name reader in `src/services/extract-facts.mjs` |
| one sentence where the description holds three | the closed sentence-shape taxonomy, same file |
| a definition fetched but the card unchanged | the anchor band, or the re-grounding path in `src/services/news.mjs` |
| background full of unrelated senses | neighbourhood selection in `src/domain/news-feed.mjs` / `sense-scope.mjs` |
| filler sentences no sense gate refuses | often a FALSE FACT the graph believes — check what the article's own extraction minted before touching the gate |
| a false row in the research block | the definition-body reader in `src/services/news.mjs` |
| an event stated twice | paragraph assembly, where the whole row set is in view — not extraction, which sees one row |

**The rule that keeps costing time when ignored:** a gate cannot refuse a fact the graph
believes. If a stray keeps arriving, check whether extraction minted something false upstream
before making the selector cleverer.

**Prefer closed sets to general rules.** A named, curated table of shapes beats a widened regex;
a false positive on an unrelated phrasing is worse than an honest miss.

**Dispatching fixes:** brief each sub-agent with its own files, the specimens it must move, the
deliberate misses it must not resurrect, and `test:fast` plus its blast radius — never the full
suite. The coordinator runs the full suite once, at the push.

## 6. Keeping the record

- Update `NEXT.md` as each track lands — in the same commit as the fix, not at the end.
- A bug found while fixing an item is that item's remainder, not a new item, unless it is
  genuinely a different subsystem — and say so explicitly when you promote one.
- When a run measures something the list gets wrong, correct the list. An item that claims ten
  sites when a search finds a hundred is worse than no item.

## 7. Stop conditions

The loop ends when the FIRST of these fires:

- **Budget.** The iteration count or range named at invocation is reached.
- **Two no-change iterations in a row.** A run whose cards are byte-identical to the previous
  run's, with no track merged between them, means the loop has stopped finding gaps at this
  source mix — say so rather than re-running.
- **The gap left is not in this loop's reach.** When the worst remaining gap needs a design
  decision, a data load, or work in a subsystem this loop does not own, stop and name it. Write
  it into `NEXT.md` with what the run measured, and hand the decision over.

On stop, report: iterations run, what each moved on the cards, the current scores against the
target card (§2), and anything the runs measured that changes what should be done next.

## Constraints that are not negotiable

- No LLM in the product path, and none anywhere in this loop's measurement.
- Fixture captures keep the minimum the fetchers read, with origin and licence noted — never
  full article bodies.
- Every read-time resolver stays a pure function of the fact set: no wall clock, no counter, no
  reliance on arrival order. Feed the same facts in two orders and demand the same answer.
