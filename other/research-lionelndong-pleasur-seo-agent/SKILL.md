---
name: research
description: Gather keyword metrics, related terms, questions, full SERP benchmark, top-page extractions, and deep web research for a target keyword, then emit a beat spec the outline must satisfy. Triggered by /research <keyword> or as the first content stage of /blog-pipeline.
allowed-tools: Read, Write, WebFetch, mcp__semrush__*, Bash
---

# Research Skill

Produce a research dossier that ends in a **beat spec** — a quantified statement of what this article must do to deserve the top of this SERP. The outline is bound by the beat spec; the quality gate scores against it. If the research is thin, everything downstream is thin: this is the most leverage-dense stage of the pipeline.

> Tool calls: read [`references/semrush-mcp-cheatsheet.md`](./references/semrush-mcp-cheatsheet.md) first — it pins the REAL tool/report names and parameter shapes (the only pattern is `get_report_schema` → `execute_report`). Never call `mcp__semrush__keyword-overview`, `topic-research`, `serp-results` or other invented names; they don't exist.

## Input

A target keyword as a string. Example: `ai girlfriend app`.

If invoked with no argument, read the most recent context file in `content-pipeline/0-context/` and prompt the user for the keyword.

## Process

1. **Slugify.** `python scripts/slugify.py "<keyword>"`; store the slug.
2. **Read brand context.** `brand-config.md` — audience, products, voice. Research framing should consider what this brand can credibly own.
3. **Pull keyword data via Semrush MCP** (cheatsheet steps 1–4):
   - `phrase_this` + `phrase_kdi` → volume, CPC, competition, KD%
   - `phrase_fullsearch` + `phrase_related` (limit 40–50) → variation pool; keep 10–15 same-intent keywords with volumes
   - `phrase_questions` (limit 30–40) → group into 3–5 question themes; drop spam
   - `phrase_organic` (limit 10–20) → the ranking URLs, in order
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
5. **Authority check.** `domain_ranks` for the top-3 domains, `url_organic` (limit 10) for the top-3 URLs → is this SERP beatable, and what secondary keywords do winning pages also rank for (fold the good ones into the outline's subtopics).
6. **Deep web research via OpenRouter (Perplexity).** Voice-of-customer + community signals (Reddit, forums, review sites):

   ```bash
   doppler run -- python .claude/skills/research/scripts/openrouter_research.py \
     --keyword "<keyword>" --slug "<slug>"
   ```

   Output lands at `content-pipeline/1-research/{slug}-deep.md`. If `OPENROUTER_API_KEY_BLOG_AGENT` isn't set, skip and note it in the dossier — don't fail the pipeline.
7. **Recommend an angle.** One-sentence thesis that wins against the current SERP, with justification grounded in the benchmark's gaps + what this brand can credibly demonstrate first-hand.
8. **Write the beat spec** — the dossier's final section, in exactly this shape:

   ```markdown
   ## BEAT SPEC (binding on outline + quality gate)
   - Target word count: <max(1.1 × median of top 3, 1800)> (±20%)
   - Format: <modal SERP format>; item count: <max items on SERP + 1, if list-shaped>
   - Comparison table: <required iff ≥2 of top 5 have one — list required columns>
   - Must-cover topics (consensus): <bulleted list — every one becomes outline coverage>
   - Differentiation topics: <partial-coverage topics we go deeper on>
   - Information gain (≥1 REQUIRED): <the thing nobody on page 1 has — original comparison, first-hand product walkthrough, fresh data, better explanation>
   - Secondary keywords to work in naturally: <from url_organic + variations>
   - Beatability: <honest read — authority spread, content quality of incumbents>
   ```
9. **Write the dossier** to `content-pipeline/1-research/{slug}.md` per `templates/research-template.md`. No `{{VAR}}` markers left. Include a "Deep web research findings" summary section (the `-deep.md` file stays available to `/draft`).
10. **Emit chartable data** (unchanged): if the dossier surfaces numeric breakdowns worth charting, write `content-pipeline/1-research/{slug}-data.json` (`{label: number}` dicts, snake_case keys, `_meta.source` for auditability). Don't fabricate; omit if nothing chartable.

## Output

`content-pipeline/1-research/{slug}.md` — 1,200–2,500 words. Dense, scannable, no fluff. The `outline` skill reads it end-to-end.

## Quality checklist

Before saving, verify:

- [ ] Primary keyword has volume, KD%, CPC (real Semrush numbers, not guesses)
- [ ] 10–15 same-intent related keywords with volumes
- [ ] 10+ questions grouped into 3+ themes
- [ ] **Top 5+ pages extracted with word count, H2 list, format, item count, table/visual counts**
- [ ] **Benchmark table computed (median/max words, modal format, table usage)**
- [ ] **Consensus / partial / gap topics explicitly listed**
- [ ] **BEAT SPEC section present, complete, and numerically specific**
- [ ] One-sentence recommended angle with justification
- [ ] Deep-research section present (or explicit note that OpenRouter wasn't configured)
- [ ] At least 3 verbatim user quotes when deep research ran
- [ ] No raw CSV/JSON dumps; everything synthesized
- [ ] Brand context reflected — the angle is something THIS brand can credibly own

## When to re-run

If the SERP shifts (new competitor, format change) or the angle stops holding. Re-running here is cheaper than reworking any later stage.
