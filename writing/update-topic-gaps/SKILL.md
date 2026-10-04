---
name: update-topic-gaps
description: Compare an existing article's section coverage to the current SERP (Semrush phrase_organic + Firecrawl page extraction) and to the related-term / question landscape (phrase_related + phrase_questions). Find topics ranking pages cover that the article doesn't, and propose new sections.
allowed-tools: Read, Write, WebFetch, mcp__semrush__*
---

# Update Topic Gaps Skill

> **DATA LAYER RULING (2026-06-12).** Fictional `mcp__semrush__*` kebab-name tools below are overridden by `.claude/skills/keyword-research-pipeline/references/semrush-data-layer.md`. For this skill: current SERP = `keyword_research/phrase_organic`; page content = Firecrawl scrape (`FIRECRAWL_API_KEY`); topic landscape = `phrase_related` + `phrase_questions`. Logic below remains binding.

Articles don't get out-of-date in a vacuum — they get out-of-date because the SERP shifts and because the broader topic landscape grows new clusters around the seed term. New competitors rank with new sections, new angles, new evidence; Semrush Topic Research surfaces idea-clusters real publishers are writing about that may not yet be in the SERP top 5. This skill re-pulls both signals and finds what the existing article is missing.

## Input

`/update-topic-gaps <slug>`

Reads:
- `content-pipeline/updates/1-extracted/{slug}.md` (article H2 list + body)
- `content-pipeline/updates/0-guidance/{slug}.md` (if exists — confirms whether re-pulling SERP is worth it)

## Process

1. **Identify the article's primary keyword.** Often inferable from the H1 / URL slug. If unclear, ask the user.
2. **Re-pull the current SERP for that keyword via `mcp__semrush__serp-results`** (or `mcp__semrush__serp-overview` if your inventory exposes that name — see `../../keyword-research-pipeline/references/semrush-mcp-tool-inventory.md`). Capture the top 10 ranking URLs, AS / Page-AS, traffic, word-count, and the `serp_features` array. **Do not silently fall back to Ahrefs** — Ahrefs is retired.
3. **Pull Semrush Topic Research's idea-cluster tree** via `mcp__semrush__topic-research` with the article's primary keyword as the root. Extract every cluster's name, headlines, questions, and related searches. This is the second gap-source: the topic graph already knows what real publishers are writing about, even when those clusters haven't elbowed into the SERP top 5 yet (see `../../research/references/semrush-mcp-cheatsheet.md` → "Topic Research playbook").
4. **WebFetch the top 5 ranking pages.** Extract each one's H2 list.
5. **Compare H2 lists across both sources:**
   - Topics covered by the article: {list}
   - Topics covered by all top 5 SERP pages: {list}
   - Topics surfaced by Topic Research clusters (cluster name → headlines / questions): {list}
   - Topics covered by the article but NO ONE else (and no Topic Research cluster either): {list — possible differentiator, possible irrelevance}
   - **Topics covered by SERP pages but NOT the article:** {list — SERP-derived gaps}
   - **Topics surfaced by Topic Research clusters but NOT the article AND NOT the SERP top-5:** {list — topic-graph-derived gaps; these are the "covered by no one but the topic graph already knows about it" angles to own}
6. **For each gap, tag the gap-source and priority:**
   - **High priority (SERP)** — topic appears in 4+ of top 5 ranking pages (consensus topic the article needs)
   - **Medium priority (SERP)** — topic appears in 2–3 of top 5 (worth considering)
   - **Low priority (SERP)** — topic appears in 1 ranking page (likely a specific angle, not a must-have)
   - **High priority (topic-graph)** — cluster has high cluster-level volume AND its headlines/questions form a coherent sub-topic the article doesn't address
   - **Medium priority (topic-graph)** — cluster appears in Topic Research but is borderline-related or low-volume
7. **For each high/medium gap, draft a section sketch:**
   - Proposed H2 title
   - 2–3 bullet key points
   - Where to insert in the article's flow (between which existing H2s)
   - **Gap source:** `serp` | `topic-graph` | `both` (if surfaced from both)
   - Evidence / examples needed
8. **Identify obsolete sections.** If the article has H2s that no current ranking page covers AND that don't appear in any Topic Research cluster AND that don't seem essential, flag for possible removal.
9. **Write the audit** to `content-pipeline/updates/4-update-topic-gaps/{slug}.md`:

```markdown
# Topic gaps audit: {slug}

_Gap sources used: SERP top-5 (`mcp__semrush__serp-results`) + Topic Research idea-cluster tree (`mcp__semrush__topic-research`)._

## Current SERP overview
- Pulled: {date}
- Top 10 ranking URLs: {brief list}
- Dominant content type: {guide / listicle / etc.}
- Average word count: {n}
- SERP features present: {ai_overview | featured_snippet | people_also_ask | ...}

## Topic Research overview
- Root keyword: {primary keyword}
- Pulled: {date}
- Cluster tree (top 5 by volume):
  - **{cluster name}** (vol {n}, difficulty {n}) — {1-line summary of what publishers in this cluster are writing about}
  - ...

## Coverage comparison

### Topics in this article
- {h2 list}

### Topics in current top-ranking pages (consensus)
- {topic} — covered by N of top 5

### Topics in Topic Research clusters
- {topic / cluster sub-theme} — surfaced by cluster "{cluster name}"; appears in N of top 5 SERP pages (0 if topic-graph-only)

## Gap sections to add

### High-priority gaps

#### Proposed H2: "..."
- **Gap source:** `serp` | `topic-graph` | `both`
- **Why:** covered by N of top 5 ranking pages / surfaced by Topic Research cluster "{cluster name}" with cluster volume {n}
- **Key points:** ..., ..., ...
- **Insert between:** "{existing H2}" and "{existing H2}"
- **Evidence/examples:** ...

#### Proposed H2: "..."
...

### Medium-priority gaps
...

## Possible removals

- "{existing H2}" — not covered by any current top-ranking page AND absent from Topic Research clusters; consider whether it still earns its place
```

## Output

`content-pipeline/updates/4-update-topic-gaps/{slug}.md`

A list of section additions and possible removals for `update-draft` to apply.

## Quality checklist

- [ ] Re-pulled SERP within the last day (not stale) via `mcp__semrush__serp-results`
- [ ] Topic Research idea-cluster tree pulled in the same run via `mcp__semrush__topic-research`
- [ ] Coverage comparison lists actual topics, not summaries
- [ ] Each gap is tagged with `gap_source: serp | topic-graph | both`
- [ ] Each gap specifies WHERE to insert (which existing sections it sits between)
- [ ] Removals only suggested when truly absent from current SERP AND absent from Topic Research clusters, not just absent from one page
- [ ] If the article looks healthy (no high-priority gaps in either source), state that — don't manufacture gaps
- [ ] No `mcp__ahrefs__*` calls anywhere in the run (Ahrefs is retired; that's a bug, not a fallback)

## When the SERP hasn't shifted

If the article's H2s match the current top-ranking pages well AND no Topic Research cluster surfaces a meaningful uncovered angle, the audit may have nothing to suggest. That's fine — it means the article's structure is still strong. Other audits (claims, product mentions) may still find updates.
