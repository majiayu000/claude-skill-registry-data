---
name: researching-content-opportunities
version: "1.0.1"
description: >
  Researches keyword and content opportunities for FlashFusion using Ahrefs and Semrush. Runs quarterly before content planning to identify what to write, what FlashFusion can realistically rank for, and where competitor content gaps exist. Outputs a prioritized list of 10–15 topic targets for the next 90 days — not a sprawling keyword spreadsheet.

  Activate when the user mentions: content planning, keyword research, what should I write about, find content opportunities for FlashFusion, SEO opportunities, topic research, quarterly planning, content calendar, keyword targets, what's ranking, competitor content gaps, content strategy for FlashFusion, Ahrefs research, or Semrush keyword research. Also activate when starting a new content quarter or when the content backlog is empty.
---

# Content Opportunity Researcher

Finds the keyword territory FlashFusion should own this quarter. Output is a short, prioritized topic list — not a 500-keyword spreadsheet nobody acts on.

Run this before writing anything. Running SEO research after writing is closing the barn door.

Load `references/ff-seo-context.md` before running any search step.

---

## Phase 1: Competitor Gap Analysis (Semrush)

Finds keywords where FlashFusion's competitors rank but FlashFusion does not.

1. Semrush → Keyword Gap tool
2. Enter `flashfusion.co` + 2–3 competitor domains from the context file's competitor list
3. Filter results:
   - Competitors rank positions 1–20
   - FlashFusion does not rank in top 100
   - Monthly volume: 100–5,000
   - Keyword difficulty: under 40
   - Intent: informational or commercial investigation (not pure transactional)
4. Export top 50, note the best 15 opportunities

---

## Phase 2: Trending Content in This Space (Ahrefs)

Finds what's gaining traction right now in FlashFusion's content pillars.

1. Ahrefs → Content Explorer
2. Run a search per content pillar (e.g., `"n8n automation"`, `"AI agent workflow"`, `"AI for MSPs"`, `"tool consolidation"`)
3. Filter: Published last 90 days · Referring domains > 3 · DR < 65
4. Surfaces what's performing and not yet over-covered
5. Note 5–10 topics with meaningful traffic and low competitive saturation

---

## Phase 3: Own-Keyword Acceleration (Ahrefs)

Finds FlashFusion content already ranking in positions 10–50 — "almost there" opportunities that need a push, not new content.

1. Ahrefs → Site Explorer → `flashfusion.co`
2. Organic keywords → filter position 10–50
3. Note 3–5 terms where a content refresh or targeted internal link could move rankings

These get added to the output as refresh tasks, not new content tasks.

---

## Phase 4: Cluster and Prioritize

Take all candidate topics from Phases 1–3 and cluster related terms together (run `searchfit-seo:keyword-clustering` if the list exceeds 30 terms).

Score each cluster:

| Dimension | Score |
|---|---|
| Business alignment — does this lead to FlashFusion services or newsletter signups? | 1–3 |
| Achievability — can FlashFusion realistically rank here in 90 days? | 1–3 |
| Volume potential — is the traffic worth the effort? | 1–3 |

Prioritize clusters scoring 7+. Anything below 5 goes to the Defer list.

---

## Output Format

```
Q[X] Content Targets — FlashFusion
Generated: {{DATE}}

DO NOW (score 7–9)
1. [Topic cluster] — primary keyword: "[keyword]" (vol: X/mo, KD: X) — content type: [tutorial / case study / post / guide]
2. ...

DO NEXT (score 5–6)
3. ...

REFRESH EXISTING
• [URL] — ranking for "[keyword]" at position X — action: [content refresh / add internal links / update title tag]

SKIP THIS QUARTER
• [Cluster] — reason: [KD too high / volume too low / poor business alignment / content already exists]
```

Save output to: `FlashFusion/Content/SEO/{{YYYY-Q}}_content-targets.md`

---

## Tool Split

| Task | Use |
|---|---|
| Keyword volume + difficulty data | Semrush |
| Competitor content research | Ahrefs Content Explorer |
| SERP analysis for specific keywords | Ahrefs |
| Backlink analysis | Ahrefs |
| Content gap vs. competitors | Semrush Keyword Gap |
| Site health + technical audit | Semrush Site Audit |
| Rank tracking (ongoing) | Ahrefs Rank Tracker |

Do not run both tools on the same task — pick the better one per job.

---

## Cadence

- **Quarterly:** Full run (all 4 phases) — start of Q1, Q2, Q3, Q4
- **Monthly pulse:** Phase 3 only (own-keyword check, 15 minutes)
- **Ad hoc:** Phase 2 only when starting a new content series

---

## Anti-Patterns

- **Don't optimize for raw volume alone.** KD 75 at 50K/month is not a FlashFusion opportunity — it's a fantasy until domain authority is established. Stay under KD 40.
- **Don't produce more than 15 prioritized targets.** Longer lists don't get used.
- **Don't skip the competitor gap step.** Writing what you want vs. what has a gap are different activities.
- **Don't confuse social reach with SEO.** LinkedIn impressions have no bearing on Google rankings.
- **Don't run this without a live content hub.** SEO research is premature if `flashfusion.co/blog` doesn't exist yet. If the hub isn't live, the first output of this skill should be: "Build the content hub first."
