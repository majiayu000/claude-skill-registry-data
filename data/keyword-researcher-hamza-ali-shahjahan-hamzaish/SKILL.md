---
name: keyword-researcher
description: Pull real keyword data from GSC (own sites) + Ahrefs Webmaster Tools (own sites) + DataForSEO (competitor/general). Produce a clustered keyword brief.
---

# Keyword Researcher

## When you activate
User asks: "research keywords for X", "what should we rank for?", "what are <competitor> ranking for?", "give me striking-distance keywords for <our site>"

Also invoked by `seo-strategist` for the keyword section of an SEO strategy.

## What you produce
Saved to `products/<name>/launch/keyword-briefs/YYYY-MM-DD-<topic>.md`:

```
## Keyword Brief — <topic / domain>

### Method
- Source: GSC | Ahrefs Webmaster | DataForSEO | combination
- Date range: <if GSC: last 90 days>
- N keywords analyzed: <count>

### Clusters (intent-grouped)

#### Cluster 1: <intent>
- **Primary keyword:** <kw> — volume <N>, difficulty <est>, intent <informational/commercial/transactional>
- **Supporting keywords (5–15):** <list with volume>
- **Search intent summary:** <one sentence>
- **Recommended page:** <new article | optimize existing | landing page | tool page>
- **Page outline:**
  1. <H2>
  2. <H2>
  3. ...

#### Cluster 2: ...

### Striking-distance opportunities (positions 5–15)
| Keyword | Current position | Impressions/mo | Action to climb |
|---|---|---|---|
| <kw> | 7 | 2400 | Add 200 words on <subtopic>, update H1, internal link from <hub> |

### Quick wins (high volume × low competition)
| Keyword | Volume | Difficulty | Why it's a win |
|---|---|---|---|

### Skip these (don't bother)
- <kw> — too competitive, too low intent, or wrong audience
```

## Protocol
1. Identify what data sources apply:
   - Input is *Hamza's domain* → GSC API (last 90d queries) + Ahrefs Webmaster (organic keywords + backlinks)
   - Input is *competitor's domain* → DataForSEO `domain_intersection` or `keywords_for_site`
   - Input is *a topic with no domain* → DataForSEO `keyword_suggestions` + `keyword_for_keywords`
2. Pull data via the API (or ask user to paste if connector not yet wired).
3. Cluster keywords by intent (informational/commercial/transactional) and semantic similarity.
4. For each cluster: pick a primary keyword (best volume × intent fit) and supporting keywords.
5. Recommend a page (new vs optimize existing) — check `products/<name>/` for existing content first.
6. Surface striking-distance and quick wins separately — these are the priorities.
7. Be honest about skip-these. SEO success is as much about choosing what NOT to chase.

## DataForSEO API note
Use sparingly — each call costs fractions of a cent but adds up. Bundle queries when possible. Standard pipeline:
1. One `keyword_suggestions` call (returns ~700 keywords)
2. One `keyword_for_keywords` for the top 50 to get exact volumes
3. Optional: one SERP call per cluster's primary keyword to understand competitive landscape

Per brief: target < $0.50 in API costs.

## Sources
- `stack/analytics-stack.md` (for the SEO data stack rationale)
- `knowledge-base/launch-stage/seo-content-strategy.md`

## What you don't do
- Don't make up search volumes. If no data source is wired yet, say so and propose: get the user to verify GSC + AWT for the site, get DataForSEO credentials.
- Don't recommend a keyword without showing volume and competition.
- Don't ignore the "skip these" section — discipline.
