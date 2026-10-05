---
name: creo-seo-content
description: >
  Content-focused SEO audit for Next.js apps. Deep dive into E-E-A-T, AI-generated
  content detection (26 phrases + 24 vague quantifiers), humanity/specificity/structure
  scoring, search intent detection, opportunity scoring, internal linking audit, and
  citability-ready rewrite priorities. Complements creo-seo (which covers technical,
  build, live, schema) by focusing exclusively on content quality. Trigger keywords:
  content audit, E-E-A-T, AI content detection, humanity score, citability, search
  intent, content rewrite, internal linking audit.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Agent
---

# creo-seo-content — Next.js content quality specialist

Content-specific SEO auditor. Runs as standalone or as the Phase 2 delegate of `creo-seo`. Scores each page on 5 content dimensions, detects AI-generated patterns, maps search intent, scores opportunity, and produces rewrite priorities with before/after examples.

## Commands

| Command | Purpose |
|---------|---------|
| `/creo seo-content audit <url>` | Full content audit on a single URL or a list |
| `/creo seo-content humanity <url>` | Humanity score only (AI-pattern detection) |
| `/creo seo-content intent <url or keyword>` | Search intent classification |
| `/creo seo-content linking <url>` | Internal linking audit |
| `/creo seo-content rewrite <url>` | Generate rewrite priorities with before/after |
| `/creo seo-content gate <mdx-path>` | Publish gate — pass/fail score + reasons |

## Scoring

Composite 0–100 per page:

```
Content_Quality =
  (Humanity        × 0.30) +
  (Specificity     × 0.25) +
  (Structure       × 0.20) +
  (SEO_Compliance  × 0.15) +
  (Readability     × 0.10)
```

Publish threshold: ≥ 80 with zero Critical issues.

## Audit flow

1. **Load project profile** from `.claude/skills/creo-seo/creo-seo-{project_id}.md` (shared with creo-seo skill). Fall back to fresh scan if missing.
2. **Fetch page content** — WebFetch for live URLs, Read for local MDX/TSX files.
3. **Normalize text** — strip HTML, extract main content, skip nav/footer.
4. **Score 5 dimensions** per `references/content-quality-rubric.md` (or shared ref in `../creo-seo/references/`).
5. **AI-pattern sweep** per `references/ai-pattern-detection.md` — count phrases, vague words, boosters.
6. **Structure analysis** — H1/H2/H3 hierarchy, paragraph lengths, table/list presence.
7. **Citability check** per `../creo-seo/references/geo-citability.md` — passages in 134–167 word range, 5-dimension scoring.
8. **Intent classification** — informational / navigational / transactional / commercial investigation.
9. **Internal linking audit** per `../creo-seo/references/internal-linking-recipe.md` — count, anchors, cluster fit.
10. **Output** per-page report + rewrite priorities.

## Search intent classification

4-class system:

| Intent | Keyword signals | SERP features |
|--------|-----------------|---------------|
| **Informational** | what, why, how, guide, tutorial, tips, definition | featured snippet, knowledge graph, PAA, video, images |
| **Navigational** | login, sign in, website, dashboard, account, brand names | brand knowledge panel |
| **Transactional** | buy, purchase, pricing, free trial, coupon, order, download | shopping results, local pack, ads |
| **Commercial investigation** | best, review, vs, compare, alternative, similar, top | carousel, comparison tables, lists |

Use intent to route:
- Informational → aim for citability + structured answers
- Commercial investigation → comparison tables, feature matrices
- Transactional → strong CTAs, trust signals, not just SEO
- Navigational → avoid SEO cannibalization of branded queries

## Opportunity scoring (when GSC/keyword data available)

8-factor weighted score 0–100:

```
Opportunity =
  Volume(25%) + Position(20%) + Intent(20%) + Competition(15%)
  + Cluster(10%) + CTR(5%) + Freshness(5%) + Trend(5%)
```

Priority tiers:
- CRITICAL ≥ 80
- HIGH ≥ 65
- MEDIUM ≥ 45
- LOW ≥ 25
- SKIP < 25

Use with `seo-google` extension for live GSC data.

## Writing patterns to enforce

### Direct-answer opening (for AI citability)

Every H2 section must open with a 1–2 sentence direct answer before expanding. Pattern: **"X is Y. It does Z."**

### Key Takeaways block (after intro, before first H2)

3–5 bullets of actual conclusions (not table of contents). AI summaries pull from here.

### Mini-story injection

2–3 per long-form piece. Structure: named person + dates + outcome.

### YouTube embed

≥ 1 relevant video per long-form article for multi-modal signal.

## Content quality gates by page type

| Page type | Min words | Target | Uniqueness |
|-----------|----------:|-------:|-----------:|
| Homepage | 500 | 800–1200 | N/A |
| Service page | 800 | 1200–1800 | 80%+ |
| Blog post | 1500 | 2000–2500 | 60%+ |
| Product page | 300 | 500–800 | Per-SKU |
| Location page | 500 | 600–800 | 60%+ |
| Pricing | 400 | 600–900 | N/A |

## Reference library

Loaded on demand:

| File | Purpose |
|------|---------|
| `references/search-intent.md` | 4-class intent system with signals |
| `references/opportunity-scoring.md` | 8-factor content prioritization |
| `references/content-playbook.md` | Writing patterns (direct-answer, mini-stories, takeaways) |
| `references/rewrite-templates.md` | Before/after examples for common patterns |
| `../creo-seo/references/content-quality-rubric.md` | Shared 5-dim scoring |
| `../creo-seo/references/ai-pattern-detection.md` | Shared AI phrase/vague-word lists |
| `../creo-seo/references/geo-citability.md` | Shared citability rubric |
| `../creo-seo/references/internal-linking-recipe.md` | Shared linking rules |

## Report output

Save to `{reports_path}/seo-content-{YYYYMMDD}-{HHMM}.md`. Format:

```markdown
# Content audit — {url}

**Composite score:** 68/100 (C)
**Publish status:** needs rework
**Intent:** commercial investigation (primary), informational (secondary)
**Opportunity score:** 72/100 (HIGH)

## Dimension breakdown
| Dimension | Score | Notes |
|-----------|------:|-------|
| Humanity | 58 | 12 AI phrases, 18 vague words in 1800w |
| Specificity | 62 | 2 stats only, no sources |
| Structure | 80 | Good H2s, paragraphs slightly long |
| SEO compliance | 75 | Keyword missing from first 100 words |
| Readability | 70 | Flesch 62, avg sentence 24 words |

## AI pattern flags (12 instances)
- "in today's digital world" — line 14
- "leverage" — line 28, 47
- ...

## Rewrite priorities (ranked by impact)
### 1. Opening paragraph — humanity + citability

BEFORE:
> {current opening}

AFTER:
> {rewritten opening with definition, stat, source}

### 2. Section 3 — specificity
...

## Internal linking gaps
- 2 of 3–5 links (below minimum)
- Missing pillar reference to /guide/podcast-hosting
- Orphan: 0 inbound links from other posts

## Next steps
1. Apply top 3 rewrites (est. score 68 → 82)
2. Add 1–2 internal links to pillar + related
3. Add 3 stats with citations to sections 2, 4, 6
```

## Parallel execution

When called by `creo-seo` as part of `/creo seo audit`, run in parallel with Phase 3 + Phase 4. When called standalone, serial execution is fine.

## Quality gates

- Every rewrite priority includes BEFORE + AFTER
- AI phrase flags are line-numbered
- Intent + opportunity scoring only fires when data is available; otherwise skip
- Reports saved to disk
- Scoring must be reproducible from refs (no magic constants in prose)
