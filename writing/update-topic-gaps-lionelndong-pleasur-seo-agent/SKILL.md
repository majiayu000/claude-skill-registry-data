---
name: update-topic-gaps
description: Compare an existing article's section coverage to the current SERP (Ahrefs serp-overview + Firecrawl page extraction) and to the related-term / question landscape (keywords-explorer-related-terms + keywords-explorer-matching-terms). Find topics ranking pages cover that the article doesn't, and propose new sections.
allowed-tools: Read, Write, WebFetch, mcp__ahrefs__*
---

# Update Topic Gaps Skill

> **Data layer: Ahrefs MCP** (`mcp__ahrefs__*`): current SERP = `serp-overview`; page content = Firecrawl (`FIRECRAWL_API_KEY`, WebFetch fallback); topic landscape = `keywords-explorer-related-terms`/`-matching-terms` by `parent_topic`. Read [`../research/references/ahrefs-mcp-cheatsheet.md`](../research/references/ahrefs-mcp-cheatsheet.md) first — string params, `select`+`country` required. Logic below is binding.

Articles don't get out-of-date in a vacuum — they get out-of-date because the SERP shifts and because the broader topic landscape grows new clusters around the seed term. New competitors rank with new sections, new angles, new evidence; the Ahrefs related-term / question landscape surfaces sub-topics real publishers are writing about that may not yet be in the SERP top 5. This skill re-pulls both signals and finds what the existing article is missing.

## Input

`/update-topic-gaps <slug>`

Reads:
- `content-pipeline/updates/1-extracted/{slug}.md` (article H2 list + body)
- `content-pipeline/updates/0-guidance/{slug}.md` (if exists — confirms whether re-pulling SERP is worth it)

## Process

1. **Identify the article's primary keyword.** Often inferable from the H1 / URL slug. If unclear, ask the user.
2. **Re-pull the current SERP for that keyword via `serp-overview`** (`{keyword:"<kw>", country:"US", select:"url,title,position,domain_rating,url_rating"}`; see `../../research/references/ahrefs-mcp-cheatsheet.md` section 4). Capture the top 10 ranking URLs, position order, and DR/UR. ⚠️ For the SERP-features array (incl. `ai_overview`, `question`/PAA), call `keywords-explorer-overview` (`{keywords:"<kw>", country:"US", select:"keyword,serp_features"}`) instead — `serp-overview` has no `serp_features` column (verified PLE-3063).
3. **Pull the Ahrefs related-term / question landscape** as the topic-cluster source. Call `keywords-explorer-related-terms` (`{keywords:"<primary kw>", country:"US", view_for:"also_talk_about", select:"keyword,volume,difficulty,parent_topic,intents", limit:"100"}`) and `keywords-explorer-matching-terms` (`{keywords:"<primary kw>", match_mode:"terms", country:"US", select:"keyword,volume,difficulty,parent_topic", limit:"100"}`); **group the combined rows by `parent_topic`** to form clusters (each cluster = a parent_topic with its member keywords and question-form members). This is the second gap-source: the topic landscape already knows what real publishers are writing about, even when those clusters haven't elbowed into the SERP top 5 yet (see the cheatsheet section 2 "Related / long-tail ideas").
4. **WebFetch the top 5 ranking pages.** Extract each one's H2 list. (The MCP returns SERP metadata, not full page text — WebFetch, or Firecrawl when a page bot-walls, gives the H2 list — cheatsheet section 7.)
5. **Compare H2 lists across both sources:**
   - Topics covered by the article: {list}
   - Topics covered by all top 5 SERP pages: {list}
   - Topics surfaced by the related-term clusters (cluster parent_topic → member keywords / question members): {list}
   - Topics covered by the article but NO ONE else (and no related-term cluster either): {list — possible differentiator, possible irrelevance}
   - **Topics covered by SERP pages but NOT the article:** {list — SERP-derived gaps}
   - **Topics surfaced by related-term clusters but NOT the article AND NOT the SERP top-5:** {list — topic-landscape-derived gaps; these are the "covered by no one but the topic landscape already knows about it" angles to own}
6. **For each gap, tag the gap-source and priority:**
   - **High priority (SERP)** — topic appears in 4+ of top 5 ranking pages (consensus topic the article needs)
   - **Medium priority (SERP)** — topic appears in 2–3 of top 5 (worth considering)
   - **Low priority (SERP)** — topic appears in 1 ranking page (likely a specific angle, not a must-have)
   - **High priority (topic-graph)** — cluster has high aggregated cluster volume AND its member keywords / question members form a coherent sub-topic the article doesn't address
   - **Medium priority (topic-graph)** — cluster appears in the related-term landscape but is borderline-related or low-volume
7. **For each high/medium gap, draft a section sketch:**
   - Proposed H2 title
   - 2–3 bullet key points
   - Where to insert in the article's flow (between which existing H2s)
   - **Gap source:** `serp` | `topic-graph` | `both` (if surfaced from both)
   - Evidence / examples needed
8. **Identify obsolete sections.** If the article has H2s that no current ranking page covers AND that don't appear in any related-term cluster AND that don't seem essential, flag for possible removal.
9. **Write the audit** to `content-pipeline/updates/4-update-topic-gaps/{slug}.md`:

```markdown
# Topic gaps audit: {slug}

_Gap sources used: SERP top-5 (`serp-overview`) + Ahrefs related-term / question landscape (`keywords-explorer-related-terms` + `keywords-explorer-matching-terms`, grouped by parent_topic)._

## Current SERP overview
- Pulled: {date}
- Top 10 ranking URLs: {brief list}
- Dominant content type: {guide / listicle / etc.}
- Average word count: {n}
- SERP features present: {ai_overview | featured_snippet | people_also_ask | ...}

## Topic landscape overview
- Root keyword: {primary keyword}
- Pulled: {date}
- Cluster tree (top 5 by aggregated volume):
  - **{parent_topic}** (vol {n}, difficulty {n}) — {1-line summary of what publishers in this cluster are writing about}
  - ...

## Coverage comparison

### Topics in this article
- {h2 list}

### Topics in current top-ranking pages (consensus)
- {topic} — covered by N of top 5

### Topics in related-term clusters
- {topic / cluster sub-theme} — surfaced by cluster "{parent_topic}"; appears in N of top 5 SERP pages (0 if topic-graph-only)

## Gap sections to add

### High-priority gaps

#### Proposed H2: "..."
- **Gap source:** `serp` | `topic-graph` | `both`
- **Why:** covered by N of top 5 ranking pages / surfaced by related-term cluster "{parent_topic}" with cluster volume {n}
- **Key points:** ..., ..., ...
- **Insert between:** "{existing H2}" and "{existing H2}"
- **Evidence/examples:** ...

#### Proposed H2: "..."
...

### Medium-priority gaps
...

## Possible removals

- "{existing H2}" — not covered by any current top-ranking page AND absent from the related-term clusters; consider whether it still earns its place
```

## Output

`content-pipeline/updates/4-update-topic-gaps/{slug}.md`

A list of section additions and possible removals for `update-draft` to apply.

## Quality checklist

- [ ] Re-pulled SERP within the last day (not stale) via `serp-overview`
- [ ] Related-term / question landscape pulled in the same run via `keywords-explorer-related-terms` + `keywords-explorer-matching-terms` (grouped by parent_topic)
- [ ] Coverage comparison lists actual topics, not summaries
- [ ] Each gap is tagged with `gap_source: serp | topic-graph | both`
- [ ] Each gap specifies WHERE to insert (which existing sections it sits between)
- [ ] Removals only suggested when truly absent from current SERP AND absent from the related-term clusters, not just absent from one page
- [ ] If the article looks healthy (no high-priority gaps in either source), state that — don't manufacture gaps
- [ ] All data calls are `mcp__ahrefs__*`

## When the SERP hasn't shifted

If the article's H2s match the current top-ranking pages well AND no related-term cluster surfaces a meaningful uncovered angle, the audit may have nothing to suggest. That's fine — it means the article's structure is still strong. Other audits (claims, product mentions) may still find updates.
