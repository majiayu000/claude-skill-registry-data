---
name: research
description: Gather keyword metrics, related terms, questions, full SERP benchmark, top-page extractions, and deep web research for a target keyword, then emit a beat spec the outline must satisfy. Triggered by /research <keyword> or as the first content stage of /blog-pipeline.
allowed-tools: Read, Write, WebFetch, mcp__ahrefs__*, Bash
---

# Research Skill

Produce a research dossier that ends in a **beat spec** — a SERP-derived *guideline* for what this article should do to deserve the top of this SERP (what's ranking, how deep, which topics are consensus, where the gaps are). The outline is shaped by it; the completeness floors enforce only the depth + coverage minimums. If the research is thin, everything downstream is thin: this is the most leverage-dense stage of the pipeline.

> Tool calls: read [`references/ahrefs-mcp-cheatsheet.md`](./references/ahrefs-mcp-cheatsheet.md) first — it maps each research task to the real Ahrefs MCP tools and pins the param rules. Two rules that bite: params are comma-separated **strings**, not JSON arrays (`keywords:"ai girlfriend app"`, not `["ai girlfriend app"]`), and `select` + `country` are required on most endpoints. For any tool you haven't used this run, call the `doc` tool first (e.g. `doc {tool:"keywords-explorer-overview"}`) to get its exact input/output schema. Never invent tool names.

## Input

A target keyword as a string. Example: `ai girlfriend app`.

If invoked with no argument, read the most recent context file in `content-pipeline/0-context/` and prompt the user for the keyword.

## Process

1. **Slugify.** `python scripts/slugify.py "<keyword>"`; store the slug.
2. **Read brand context.** `brand-config.md` — audience, products, voice. Research framing should consider what this brand can credibly own.
3. **Pull keyword data via Ahrefs MCP** (cheatsheet "Research workflow"). **Ahrefs is mandatory:** if the MCP is unavailable, use the Ahrefs REST API (same source, lowercase `country=us`) and surface it LOUDLY in your return; if NO Ahrefs at all (MCP + REST both down/exhausted), HARD-FAIL and STOP — never proceed on guessed metrics, never a non-Ahrefs source. See the cheat sheet's "Ahrefs is MANDATORY — outage policy".
   - `keywords-explorer-overview` (`select:"keyword,volume,difficulty,cpc,parent_topic,traffic_potential,global_volume,intents"`) → volume, KD (`difficulty`), CPC, **parent topic** (write to the parent, not the long-tail), traffic potential, intent flags
   - `keywords-explorer-matching-terms` (`match_mode:"phrase"`, limit ~50) + `keywords-explorer-related-terms` ("also rank for" / "also talk about") → variation pool; keep 10–15 same-intent keywords with volumes
   - **Questions → 3–5 FAQ themes (there is NO dedicated questions tool):** pull `keywords-explorer-matching-terms` (`match_mode:"terms"`, limit ~100) and keep keywords starting with what/how/is/are/can/does/do/why/which/who/where, AND read `serp-overview`'s `serp_features` for People-Also-Ask entries. Group into 3–5 themes; drop spam. (Downstream, the FAQ caps at ~5 crisp Q&As — no 12-question dumps, no near-duplicates.)
   - `serp-overview` (`keyword` required) → the ranking URLs, in order, with positions
4. **Build the SERP benchmark (MANDATORY — the heart of this skill).**
   Extract the full content of the top 5–8 ranking pages (skip ads, skip our own domain): for each page, POST to Firecrawl (`https://api.firecrawl.dev/v1/scrape`, body `{"url": <url>, "formats": ["markdown"]}`, header `Authorization: Bearer $FIRECRAWL_API_KEY`); fall back to WebFetch on error. From each extraction record:
   - Word count (of article body, excluding nav/boilerplate — estimate honestly)
   - Title + full H2/H3 list
   - Format (guide / listicle / comparison / how-to / explainer) and **item count** if list-shaped ("9 apps reviewed")
   - Evidence types used: tables (count them), screenshots/images (count), original data, expert quotes, hands-on detail
   - What it does well; where it's thin or generic
   Then compute the benchmark table:
   - Median + max word count of the top 3
   - Modal format and item-count range
   - Table/visual usage across the SERP ("4 of 5 pages have a comparison table")
   - **Consensus topics** — covered by 3+ of the extracted pages (the article MUST cover all of these)
   - **Partial topics** — covered by 1–2 (differentiate with more depth)
   - **Gaps** — asked by searchers (question themes, deep research) but covered by nobody (the information-gain opportunity)
5. **Authority check.** `site-explorer-domain-rating` (or `site-explorer-metrics`) for the top-3 domains, `site-explorer-organic-keywords` (limit 10) for the top-3 URLs → is this SERP beatable, and what secondary keywords do winning pages also rank for (fold the good ones into the outline's subtopics).
6. **First-party fact lock (MANDATORY — added 2026-06-15, PLE-2330).** Before writing any pricing/feature claim into the dossier, fetch the LIVE pages and record exact figures as first-party facts:
   - **Our product (always):** `WebFetch https://pleasur.ai/pricing` and capture every tier name, monthly price, annual-equivalent price, coin/credit allowance, and per-action media metering (image / voice / call costs). Cross-check against the **Canonical pricing** block in `brand-config.md`: if the live page and the block disagree, **trust the live page**, use it in the dossier, and note in the dossier that `brand-config.md` canonical pricing needs a refresh (so the drift gets fixed). If `pleasur.ai/pricing` 404s or the path moved, try `pleasur.ai` nav / `pleasur.ai/plans` and record the working URL.
   - **The competitor (for any comparison/`X vs Y`/alternatives keyword):** fetch the named competitor's live pricing/feature page the same way and record exact tiers/prices/metering. Do not infer competitor prices from reviews or the brief when a live page exists.
   - **Override rule:** any pricing/tier/feature-metering figure supplied by the brief, keyword-queue, memory, or a reviewer is **stale by default**. The live first-party (or live competitor) page wins on conflict. When they conflict, keep BOTH in the dossier WITH their sources and explicitly flag which one is load-bearing (the live one). A dossier that asserts an own-product price/feature with no `pleasur.ai`-live source recorded this run is INCOMPLETE — do not proceed to the beat spec.
   - Record each captured figure inline with `source: <live URL> (fetched <YYYY-MM-DD>)` so `verify-claims` can trace it.
7. **(Optional) Deep web research via OpenRouter (Perplexity).** OFF by default — the SERP top-page
   extraction in step 4 is the primary research, exactly as Ryan does it. Run this extra
   voice-of-customer pass (Reddit, forums, review sites) ONLY when the topic genuinely needs more
   primary signal than the top pages give — opt in with `BLOG_AGENT_DEEP_RESEARCH=1`, or when the
   `--context` explicitly asks for it:

   ```bash
   doppler run -- python .claude/skills/research/scripts/openrouter_research.py \
     --keyword "<keyword>" --slug "<slug>"
   ```

   Output lands at `content-pipeline/1-research/{slug}-deep.md`. When skipped (the default) or if
   `OPENROUTER_API_KEY_BLOG_AGENT` isn't set, note it in the dossier and move on — the master SERP
   benchmark from step 4 is what carries the research.
8. **Recommend an angle.** One-sentence thesis that wins against the current SERP, with justification grounded in the benchmark's gaps + what this brand can credibly demonstrate first-hand. The angle must NOT rest on an own-product pricing/feature claim that step 6 did not confirm live (this is exactly how PLE-2320 built a false "price-concession" + "no credit meter" thesis).
8a. **Lock the UNIQUENESS BUNDLE — proactive, data-backed, shareable (MANDATORY — Lesson 6 "be the journalist / never clone page 1"; STRATEGY §5).** Uniqueness is decided HERE, at research time, not discovered later — and the dossier must lock and name **all three** parts below so `/outline`, `/draft`, and the publish-blocking uniqueness gate (`quality-check` Gate 1.5) all carry the same `[GAIN]` element. The deepest lever is Priceonomics, quoted in Lesson 6: *"Authentic information that your company has access to is the currency of truly valuable content marketing."* Our moat is the information **we** have and the SERP can't clone.

   **(a) OUR-OWN-EVIDENCE — the uncloneable core (≥ 1 REQUIRED).** Lock at least one of these three first-party sources (Priceonomics's three: data we produce, insight from our experience, stories of people we have access to):
   - **An aggregate USAGE-DATA point we can cite** — a count/rate/trend from our **own PostHog or Stripe aggregates** (e.g. "X% of users who create a companion message within the first hour"). **AGGREGATE ONLY — never PII** (mirror `linkable-asset` RULE 1 + the cockpit PII doctrine: no individual, no sub-100 cohort, no free-text). Source it inline.
   - **A FIRST-HAND product test/insight** — we used the specific own-tool capability and observed X (the product-led move already in force). Name the exact capability so `/draft` can show it working.
   - **A real USER STORY** — an aggregate-safe, on-record pattern from our users (never a single re-identifiable person; same PII floor).

     **Honesty is absolute:** use a real/clearly-sourced datum or a genuine first-hand test — **never fabricate a statistic** or a test we didn't run (Data-integrity rules below). If we truly have no first-party datum yet, lean fully on a genuine first-hand product test and say so. This is the always-on PRODUCT-LED authority element; a purely third-party-cited article with no first-hand product demonstration is under-built for our brand. Where it *also* fits, name one credible external expert/study/primary source to cite (the journalist move), sourced inline per step 6 — but never a manufactured expert or an unsourced "studies show."

   **(b) A DELIBERATE ANGLE — decide the unique thesis up front (REQUIRED).** State, in one line, the article's unique thesis and which of the three uniqueness modes it takes (Lesson 6): **new data** (lead with our own-evidence), a **180° contrarian take** on the page-1 consensus (with real arguments, not contrarianism for its own sake), or a **genuinely better explanation** (better proof/examples/synthesis than the SERP). It must be **explicitly NOT the page-1 consensus clone** — name the consensus take from the step-4 benchmark and state how this article departs from it. This is the same angle step 8 recommends; here you commit it as the uniqueness contract.

   **(c) A SHAREABILITY HOOK — engineer it to earn links (Contagious STEPPS, REQUIRED).** Name which **STEPPS** principle(s) make this worth sharing and linking — reference `/contagious-why-things-catch-on` (Jonah Berger): **Social currency** (sharing it makes the reader look smart/in-the-know — our exclusive data is pure social currency), **Emotion** (a surprising/counter-intuitive finding that beats the assumption), **Practical value** ("news you can use" — a benchmark/yardstick readers act on), or **Story** (a Trojan-Horse narrative the data tells). Lesson 7 is explicit that this is what turns an article into something people link to — so the hook is required, not decorative. Prefer a hook that rides on part (a)'s own-evidence (our data IS the social currency / the surprising number / the citable yardstick).

   **Persist all three as the `[GAIN]` element** the BEAT SPEC carries (its `Information gain` + `Authority element` + new `Shareability hook` lines), so `/draft` builds them in and Gate 1.5 can check the *named, real* element — not a cosmetic add. Keep it **product-led** and honest: we demonstrate tools we actually have, cite data we actually hold, and never invent a product we lack (we have no story-generation product, etc.).
9. **Write the beat spec** — the dossier's final section. It is the **SERP summarized as a
   guideline** (what's ranking demands), NOT a rigid numeric contract. Ryan looks at how deep the
   ranking pages go and matches or beats them — he doesn't chase an inflated word target. Shape:

   ```markdown
   ## BEAT SPEC (guides the outline; the floors enforce only the depth + coverage minimums)
   - Target word count: <median word count of the top 3> — the depth bar to MATCH or beat. Not a
     cap, not a quota: win on usefulness, never pad to a number. (The completeness floor only checks
     the draft isn't thin — ≥ 80% of this median.)
   - Format: <modal SERP format>; item count: <the SERP's typical item count> — cover at least that
     many; add more only when each genuinely earns its place.
   - Comparison table: <required iff ≥2 of top 5 have one — list required columns>
   - Must-cover topics (consensus): <bulleted list — every one becomes outline coverage>
   - Differentiation topics: <partial-coverage topics we go deeper on>
   - Information gain — the ANGLE (≥1 REQUIRED — STRATEGY §5, Lesson 6 "never clone page 1"): <the unique thesis nobody on page 1 has, and its mode — NEW DATA / 180° CONTRARIAN (with arguments) / GENUINELY BETTER EXPLANATION. Name the page-1 consensus take and how this departs from it. NOT a clone.>
   - Our-own-evidence — the uncloneable core (≥1 REQUIRED — Priceonomics, Lesson 6, step 8a-a): <≥1 of: an aggregate USAGE-DATA point from our PostHog/Stripe aggregates (AGGREGATE ONLY, never PII), sourced inline; a FIRST-HAND product test of a named own-tool capability; a real (aggregate-safe) USER STORY. Real or genuinely-tested — never fabricated.>
   - Authority element (≥1 REQUIRED — Lesson 6, step 8a-a): <PRIMARILY PRODUCT-LED — the specific own-tool we demonstrate first-hand (overlaps our-own-evidence); PLUS, where it fits, one credible named expert/study/primary source to cite. At least one must be product-led.>
   - Shareability hook — why it earns links (REQUIRED — Contagious STEPPS, step 8a-c): <which STEPPS principle(s) make this worth sharing/linking — Social currency / Emotion / Practical value / Story — per `/contagious-why-things-catch-on`. Prefer a hook riding on the own-evidence above.>
   - Secondary keywords to work in naturally: <from site-explorer-organic-keywords + variations>
   - Beatability: <honest read — authority spread, content quality of incumbents>
   ```
10. **Write the dossier** to `content-pipeline/1-research/{slug}.md` per `templates/research-template.md`. No `{{VAR}}` markers left. Include a "Deep web research findings" summary section (the `-deep.md` file stays available to `/draft`).
11. **Emit chartable data** (unchanged): if the dossier surfaces numeric breakdowns worth charting, write `content-pipeline/1-research/{slug}-data.json` (`{label: number}` dicts, snake_case keys, `_meta.source` for auditability). Don't fabricate; omit if nothing chartable.

## Data-integrity rules (HARD — added 2026-06-15, PLE-2334)

A research dossier nearly published a false own-price claim because it asserted an "authoritative $19/mo" pleasur.ai figure that does not exist and **overrode** the accurate reviewer prices ($12.99 / $27.99) the deep-research step had captured. Never again:

1. **No unsourced figure may override sourced data.** Every number in the dossier carries its source inline. If a figure has no live source, it is a hypothesis, not a fact — label it `[UNVERIFIED]` and never let it displace a figure that *does* have a source. The word "authoritative" is not a source; do not use it to launder a guess.
2. **Conflicting sourced figures both stay.** If deep-research, reviewers, and the brief disagree on a number, surface **all of them with their sources** in the dossier and flag the conflict for downstream resolution (`verify-claims` resolves to the live page). Do not silently pick one and present it as settled.
3. **Own-product facts trace to the first party, live.** Any claim about pleasur.ai's OWN pricing, plan names, tiers, or feature gating (e.g. "no credit metering") must be sourced to the live first-party page (`pleasur.ai/pricing`, product/docs pages) checked during this run — not to the brief, not to memory, not to a reviewer. Brief/keyword-queue figures about our own product are stale by default and must be re-verified live before they enter the dossier. A wrong own-product fact is a trust catastrophe (we are the source of truth for it) and a publish-blocker downstream.

## Output

`content-pipeline/1-research/{slug}.md` — 1,200–2,500 words. Dense, scannable, no fluff. The `outline` skill reads it end-to-end.

## Quality checklist

Before saving, verify:

- [ ] Primary keyword has volume, KD (difficulty), CPC (real Ahrefs numbers, not guesses)
- [ ] 10–15 same-intent related keywords with volumes
- [ ] 10+ questions grouped into 3+ themes
- [ ] **Top 5+ pages extracted with word count, H2 list, format, item count, table/visual counts**
- [ ] **Benchmark table computed (median/max words, modal format, table usage)**
- [ ] **Consensus / partial / gap topics explicitly listed**
- [ ] **BEAT SPEC section present, complete, and numerically specific**
- [ ] **UNIQUENESS BUNDLE locked on the BEAT SPEC (step 8a; STRATEGY §5; Lesson 6/7) — all three present:**
  - [ ] **(a) Our-own-evidence (≥1): an aggregate PostHog/Stripe usage-data point (AGGREGATE ONLY, never PII, sourced inline) OR a named first-hand product test OR an aggregate-safe user story — real/genuinely-tested, never fabricated**
  - [ ] **(b) Angle named: NEW DATA / 180° CONTRARIAN (with arguments) / BETTER EXPLANATION — explicitly NOT the page-1 consensus clone (consensus take named + departure stated)**
  - [ ] **(c) Shareability hook: ≥1 named STEPPS principle (Social currency / Emotion / Practical value / Story) per `/contagious-why-things-catch-on`**
- [ ] **Authority element named (Lesson 6): ≥1 element, at least one PRODUCT-LED (a specific own-tool we demonstrate first-hand), plus a credible named/sourced expert where it fits — no manufactured experts or unsourced "studies show"**
- [ ] One-sentence recommended angle with justification
- [ ] Deep-research section present (or explicit note that OpenRouter wasn't configured)
- [ ] At least 3 verbatim user quotes when deep research ran
- [ ] No raw CSV/JSON dumps; everything synthesized
- [ ] Brand context reflected — the angle is something THIS brand can credibly own
- [ ] **No unsourced figure overrides a sourced one; conflicting sourced figures both surfaced with sources (Data-integrity rule 1–2)**
- [ ] **Step 6 ran: `pleasur.ai/pricing` fetched LIVE this run; every own-product price/tier/coin-metering fact in the dossier carries a `source: <live URL> (fetched <date>)` and matches the live page (not the brief/memory) — Data-integrity rule 3 + step 6**
- [ ] **For a comparison/vs/alternatives keyword: the competitor's pricing/feature page was also fetched live and its figures sourced inline (step 6)**
- [ ] **Any conflict between live figures and brief/queue/`brand-config.md` is surfaced with both sources and the live one flagged load-bearing; `brand-config.md` refresh noted if its canonical block drifted**

## When to re-run

If the SERP shifts (new competitor, format change) or the angle stops holding. Re-running here is cheaper than reworking any later stage.
