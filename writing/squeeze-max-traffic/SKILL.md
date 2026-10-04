---
name: squeeze-max-traffic
description: Post-draft pass that expands a drafted article to capture the FULL keyword family — keywords the page already or could rank for, plus the Ahrefs Content Gap (keywords competitors rank for but we don't) — by weaving the worthwhile ones in as natural added paragraphs/sections. NOT keyword stuffing. Triggered after /draft, before /quality-check.
allowed-tools: Read, Write, Edit, mcp__ahrefs__*, Bash
---

# Squeeze Max Traffic Skill

> **Strategy anchor: STRATEGY.md §3 (full traffic potential of the top page, not a single keyword's volume) + the Lesson 5 row ("squeeze max traffic; wide kw family") + Lesson 3 (one strong page ranks for ~1,000 related keywords).** A page that nails its parent topic should pull traffic from the whole *family* of related queries, not just its head term. This step makes sure the drafted article actually reaches for that family — **without** ever crossing into the keyword-stuffing line (anti-pattern #10) or padding (the empty-paragraph test in `/draft`).

This is **Lesson 5, part 3** of the Ahrefs method, operationalized as a discrete pipeline step: after the article is drafted, audit it against (a) the keywords this page can realistically rank for, and (b) the **Content Gap** — keywords competitors rank for that we don't — and weave the *worthwhile* ones in as genuine added value. Coverage we add must read like the writer always meant to cover it; if a keyword can't be served with a real paragraph a reader benefits from, it doesn't go in.

## Where this sits in the pipeline

```
/research → /outline → /product-mentions → /draft → [ /squeeze-max-traffic ] → /quality-check → /verify-claims → /generate-visuals → /format-for-publish
```

**After `/draft`, before `/quality-check`.** It reads the drafted body at `content-pipeline/5-drafts/{slug}.md`, expands it in place, and re-saves to the same path so the quality gate judges the squeezed article (including the uniqueness gate — added paragraphs must still be original, never page-1 clones). Run it once per article; re-run only if `/research` is re-run and the keyword family shifts.

> Tool calls: this step reuses the **Ahrefs MCP** exactly as `/research` and `/content-gap-analysis` do. Read [`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) first — params are comma-separated **strings**, not JSON arrays (`keywords:"ai girlfriend app"`, not `["ai girlfriend app"]`); `select` + `country` are required on most endpoints; call `doc {tool:"..."}` for any tool you haven't used this run; never invent tool names. **Ahrefs outage policy is the same as `/research`:** MCP first, REST fallback (surface it loudly), and if both are down, do the keyword-family expansion from the data already in `1-research/{slug}.md` rather than blocking the pipeline — note the degradation in the report.

## Input

For slug `{slug}`:
- `content-pipeline/5-drafts/{slug}.md` (required — the drafted body this step expands; byline comment stays the first line, untouched)
- `content-pipeline/1-research/{slug}.md` (the dossier — primary keyword, **parent topic**, the BEAT SPEC's "Secondary keywords" + consensus/partial/gap topics; the matching/related-terms pool already lives here)
- `content-pipeline/3-outlines/{slug}.md` (coverage map — what the article already deliberately covers)
- `content-pipeline/0-keywords/keyword-ideas.csv` + `cache/competitors.json` (if present — the resolved competitor set and the gap pool from `/content-gap-analysis`)
- `brand-config.md` (audience, products, **forbidden phrases** — added prose obeys the same voice/forbidden rules as `/draft`)

## Process

1. **Map what the page already covers.** Read the draft and the outline's coverage map; list the H2/H3 topics and the head + secondary keywords already worked in. This is the baseline — we expand the family, we don't re-add what's there.

2. **Pull the full keyword family for THIS page (Lesson 3 — the page ranks for ~1,000 related keywords, not one).** From the dossier's primary keyword and **parent topic**:
   - `keywords-explorer-related-terms` ("also rank for" / "also talk about") and `keywords-explorer-matching-terms` (`match_mode:"phrase"`, then `match_mode:"terms"` for multi-word) → the variation pool for the parent topic. `select` to carry `keyword,volume,difficulty,traffic_potential,parent_topic,intents`.
   - `site-explorer-organic-keywords` on the **top-ranking page in this SERP** (limit ~30, `order_by traffic_potential:desc`) → the secondary keywords the *winning* page already earns traffic from. These are the proven sub-queries a strong page on this topic captures (the dossier's step-5 authority check already started this; go wider here).
   - Keep only **same-intent, same-parent** keywords — a query that needs a *different* article shape is a separate cluster member for the queue (route it to `/keyword-prioritization`, do NOT bolt it on here; mismatched intent never ranks — STRATEGY §6, anti-pattern #9).

3. **Pull the Content Gap (Lesson 5 part 3 — keywords competitors rank for but we don't).** Reuse [`/content-gap-analysis`](../content-gap-analysis/SKILL.md): if `content-pipeline/0-keywords/keyword-ideas.csv` already holds a fresh gap (`gap_mode=missing`) from a recent keyword-research run, filter it to rows whose **parent topic / cluster matches this article** and use those. If there's no fresh gap for this topic, derive a quick page-level gap directly: take the resolved competitors (`cache/competitors.json`, or auto-discover via `site-explorer-organic-competitors`), pull each competitor's `site-explorer-organic-keywords` for terms in this parent topic, and keep the ones **they rank for and our drafted article doesn't cover**. Tag these `source=content_gap`.

4. **Merge, dedupe, and TRIAGE — keep only the worthwhile.** Combine the family pool (step 2) + the gap pool (step 3); drop anything already covered (step 1). Then triage each remaining keyword — **most candidates do NOT make it in.** A keyword earns a place only if **all** hold:
   - **Same searcher intent** as the article (no intent mismatch — STRATEGY §6).
   - **On-topic for the parent** — a reader of this article would genuinely expect it covered (not a tangent that belongs to another cluster member).
   - **Servable with real value** — you can add a true paragraph/sub-section a reader benefits from (a specific, a step, a comparison, an answer), not a sentence whose only job is to contain the phrase.
   - **Worth the words** — meaningful volume/traffic_potential, or it closes a consensus/gap a competitor covers and we don't. Trivial near-duplicates of a phrase already present get **merged into existing prose**, not added as new sections.
   Output a short **squeeze plan**: each kept keyword → the section it strengthens (or the new sub-section it justifies) → the value the added prose delivers.

5. **Weave it in as natural prose — never stuff (anti-pattern #10; the `/draft` empty-paragraph test).** Apply the plan:
   - **Add real paragraphs / sub-sections** where a kept keyword justifies genuinely new coverage — written in the article's persona/voice (the byline persona already chosen in `/draft`; keep its craft) and to the same specificity bar as `/draft` (named things, numbers cited with `[link]` for verify-claims, steps, first-hand product detail). A new sub-section gets a real H3 and earns its length.
   - **Fold near-variants into existing sentences** where a separate section would be redundant — phrase the existing point using the searcher's actual language so the page is matchable for that variant without a new block.
   - **Keep the authority + uniqueness intact:** added coverage must preserve the dossier's product-led authority element and must not turn a unique angle into a page-1 clone (the quality gate's Gate 1.5 still has to pass). New paragraphs are original — never lifted/paraphrased from a competitor we found in the gap step.
   - **Respect the existing structure and components:** don't bloat the article past what its content earns; don't duplicate a native `:::` component; don't stack or duplicate visuals. If a kept keyword maps to a comparison/FAQ the article should have, extend the existing table/`:::faq` rather than starting a parallel one.
   - **Give a genuinely new section its visual (the squeeze→visuals seam — DON'T leave squeezed content visual-less).** The outline planned visuals BEFORE this expansion, and `/generate-visuals` runs AFTER it — so a brand-new H3/sub-section you add here would otherwise ship with no visual. If a new section would genuinely benefit from one, add **ONE** typed `[VISUAL:...]` placeholder inside it per `templates/visual-strategy.md` — value-first (a real screenshot, a chart from resolvable `research.<key>` data, a diagram, or an external competitor/SERP shot), and **never** a PNG of a stat/quote/table/callout a native `:::` component already renders. **PRESERVE every existing `[VISUAL:]` marker untouched** — only ADD, never edit or delete the ones `/draft` and `/outline` already placed. (Externals you add resolve via `/generate-visuals` → `/capture-visuals` automatically.)
   - **Stay light on on-page SEO (Lesson 5 part 2):** intent-match and useful coverage, NOT keyword density. No exact-match repetition for its own sake; if a sentence only exists to hold a phrase, cut it.

6. **Depth + forbidden-phrase re-check.** Re-read top to bottom: every added paragraph passes the empty-paragraph test (a concrete noun/number/step/example), no forbidden phrase entered, no crutch word now used 3+ times because of the additions, rhythm still varied. The article total may grow, but only by content that earns its place — never pad to a number.

7. **Save** the expanded body back to `content-pipeline/5-drafts/{slug}.md` (overwrite; byline comment still the first line). Write the squeeze plan + the kept/rejected keyword lists to `content-pipeline/5-drafts/{slug}-squeeze.md` for the audit trail and so `/quality-check` (and a human) can see what was added and why.

## Output

- `content-pipeline/5-drafts/{slug}.md` — the drafted article, expanded to capture the worthwhile keyword family + content gap, woven in as natural prose. Same byline, same persona voice, same structure where possible.
- `content-pipeline/5-drafts/{slug}-squeeze.md` — the squeeze plan: kept keywords (→ section → value added) and rejected keywords (→ reason), plus a note on any Ahrefs degradation.

## Quality checklist

Before saving, confirm:
- [ ] Pulled the page's keyword family (related/matching terms on the **parent topic** + the winning page's organic keywords) — same-intent, same-parent only
- [ ] Pulled the **Content Gap** (reused `/content-gap-analysis`'s `missing` rows for this topic, or derived a page-level gap from competitors) — keywords competitors rank for that the draft didn't cover
- [ ] Triaged: every kept keyword is same-intent, on-topic, servable with **real** value, and worth the words; off-cluster / intent-mismatch keywords routed to `/keyword-prioritization`, not bolted on
- [ ] Added coverage is **natural prose** — real paragraphs/sub-sections (or folded variants), to the `/draft` specificity bar; **zero keyword stuffing** (anti-pattern #10), no sentence that exists only to hold a phrase
- [ ] Persona voice preserved (byline unchanged, first line intact); structure/components not bloated or duplicated; no stacked visuals
- [ ] Every existing `[VISUAL:]` marker left untouched; any genuinely-new section that warrants one got exactly ONE value-first `[VISUAL:]` added (no native-component duplication) so squeezed content isn't visual-less
- [ ] **Uniqueness + authority preserved** — additions stay original (no page-1/competitor clone; Gate 1.5 still passes) and the dossier's product-led authority element survives
- [ ] Empty-paragraph test passes on every addition; no new forbidden phrase; no crutch word now ≥3×; rhythm still varied
- [ ] `{slug}-squeeze.md` written (kept → section → value; rejected → reason; any Ahrefs-outage degradation noted)

## When to skip / when it's a no-op

- **Skip** if the article already covers the full same-intent family and there's no matching content gap (a tight, narrow topic). Write a one-line `{slug}-squeeze.md` saying "no worthwhile family/gap expansion — already complete" and pass through. A no-op is a valid, honest outcome; **never invent thin sections to look busy.**
- **Don't** use this step to chase a higher-volume but different-intent keyword (that's anti-pattern #9) or to push the article above its winnable scope — those are queue decisions for `/keyword-prioritization`, not draft-time additions.
