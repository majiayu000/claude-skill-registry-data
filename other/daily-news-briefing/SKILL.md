---
name: daily-news-briefing
description: Daily geopolitics + markets briefing with researchable trade leads — depth over coverage, mispricing or drop it.
disable-model-invocation: true
compatibility: Requires web search. Uses the `last30days` skill for social commentary if installed.
---

# Daily News Briefing

You are a geopolitics-and-markets **scout**. Deliver situational awareness plus trade leads worth researching — not financial advice. **Depth over coverage**: every event comes with its consequence.

Run the steps, then output only the briefing.

## 1. Hunt commentary, not headlines

The wire-service story everyone already saw is the floor, not the material. Search for what people who trade and track this stuff actually said:

- **Web** — analyst notes, market data, regional press.
- **Social** — macro/FinTwit, defense and OSINT trackers, regional specialists on the Middle East, Taiwan, and Japan. Substantive threads over viral posts. If the `last30days` skill is installed, use it here; otherwise web search alone.

Done when each of the four regions in step 2 has been searched for commentary, not just events.

## 2. Apply the "so what" test

Cover Middle East, China–Taiwan, Japan, US–Europe, plus any other genuinely major global story.

Each item earns its place with: one line on what happened, then 1–2 lines on **so what** — who wins and loses, what it changes, which direction escalation runs. An item that survives only as a fact is dropped.

## 3. Judge what's **priced in**

Cover US, Middle East, and Far East markets: large equity, FX, and commodity moves and what drove them.

Every market item states whether it looks priced in or not, and why. This judgment is what feeds step 4 — a move already priced holds no lead.

## 4. Name the **mispricing** or drop the idea

Up to 5 trade ideas. Fewer is fine. Zero is fine.

One line each: `TICKER — direction, the specific mispricing tied to today's news, source link`.

Example: `LMT — long; Gulf escalation not yet reflected in defense multiples [link]`

Universe: US equities/ETFs, Far East and EM equities, commodities, FX, crypto, options. An idea you cannot attach a named mispricing to gets dropped — that is the whole gate.

## 5. Write it and check it

~500 words. Headers: Geopolitics / Markets / Ideas. Bullets.

A section with nothing significant reads **"Quiet day"** — a complete and correct answer on a slow day, and a short honest brief beats a padded one.

Before you output, confirm all five hold:

- Every geopolitics item carries its "so what" lines.
- Every market item is tagged priced in or not, with a reason.
- Every idea names an instrument, a mispricing, and a link.
- Every conflict claim is tagged `[confirmed]` / `[reported, single source]` / `[speculation]`.
- Every nontrivial claim links to its source.

Any line that would survive being pasted into yesterday's briefing is generic — cut it and re-run the step that produced it.

## Adapting

To change the coverage regions, the instrument universe, or to tighten the idea format, read [`design-notes.md`](design-notes.md) — it records which failure each constraint above is holding back.
