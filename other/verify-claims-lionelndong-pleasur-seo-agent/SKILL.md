---
name: verify-claims
description: Find sources for every numerical claim in the draft, add inline hyperlinks, and add internal links to brand-reference articles. Triggered after /draft.
allowed-tools: Read, Write, Edit, WebFetch, WebSearch
---

# Verify Claims Skill

Made-up stats are the most reliable way to mark a draft as AI-generated. This skill ensures every numerical claim has a real, citable source — and that internal-linking opportunities from brand-reference are wired in.

## Input

For slug `{slug}`:
- `content-pipeline/5-drafts/{slug}.md` (the draft to verify)
- `content-pipeline/2-reference/{slug}.md` (internal-linking opportunities)
- `content-pipeline/brand-articles.json` (Strapi inventory cache — defensive backstop when `2-reference/` is empty)

## Process

1. **Read the draft.**
2. **Extract every claim that needs a source:**
   - Numerical claims ("90% of pages get no traffic")
   - Specific assertions about how things work ("Google's PageRank algorithm uses...")
   - Quoted figures from people or studies
   - Industry "research shows" claims
   - Anything with a `[link]` placeholder from drafting
3. **For each claim, verify or replace:**
   - Use **WebSearch** + **WebFetch** to find a primary source. Prefer original studies, official documentation, or first-hand brand publications over second-hand citations.
   - If the source confirms the claim → replace `[link]` with the real URL using descriptive anchor text. Use markdown link syntax inline.
   - If the source contradicts the claim → either correct the number (using the real source) or remove the claim if it can't be supported.
   - If you can't find a source within 2–3 search attempts → flag the claim with `[CITATION NEEDED]` rather than fabricating one.
4. **Add internal links from brand-reference.** Walk through the draft section by section. Wherever a phrase matches an internal-linking opportunity from `2-reference/`, link it. Use anchor text that matches the linked article's H1 when possible.

   **Defensive backstop:** if `2-reference/{slug}.md` lists zero internal-linking opportunities AND `content-pipeline/brand-articles.json` exists with `count > 0`, do NOT skip internal linking. Instead, score the inventory's articles for relevance to this draft (title/H2 keyword overlap) and weave in 2–3 of the best matches with descriptive anchor text. This catches the common failure mode where `/brand-reference` ran before the Strapi inventory was populated, or against a stale cache.
5. **Anchor text rules:**
   - Descriptive — matches what the linked page is about
   - Not naked URLs ("https://...")
   - Not "click here" or "read more"
   - Not over-optimized — don't force exact-match keyword anchors for every internal link
6. **Verify the verification.** After all edits, scan once more — confirm no `[link]` or `[CITATION NEEDED]` placeholders remain (or if they do, they're flagged for human review).
7. **Citation-density check (two tiers).** Use the same heuristic as `quality_check.py` (so the two stay aligned). Two tiers, treated very differently:

   - **Must-cite claims** — numbers, percentages, named studies, year-anchored facts, "according to X" assertions. Ryan's "cite everything" rule applies here. If coverage is below **60%**, emit `## Editor notes / Citation gaps` listing every unlinked must-cite claim by line number. The editor cuts, accepts, or asks for a broader search.
   - **Voice-flagged statements** — population quantifiers ("most platforms"), superlatives ("the only platform that..."), comparative absolutes ("every X is Y"), and named-brand mentions without links. These are usually **opinionated voice**, not citation-needing claims. Over-citing them damages the conversational tone the whole pipeline is built around. Emit `## Editor notes / Voice-flagged statements (review)` listing them — editor decides per case. **Never auto-link these** — they are flagged for human judgment, not pipeline action.

   The tier distinction is the load-bearing rule. Force a citation onto a sentence like "Most platforms claim 'uncensored' but few are" and the article reads like a footnoted academic paper instead of an Ahrefs blog post.
8. **Save** to `content-pipeline/6-drafts-cited/{slug}.md`. The file structure is identical to the draft — just with real links substituted in.

## Output

`content-pipeline/6-drafts-cited/{slug}.md`

The draft, with every numerical claim citing a real source and every appropriate internal-linking opportunity wired in.

## Quality checklist

- [ ] Every numerical claim has a `[descriptive anchor](real-url)` link
- [ ] No remaining `[link]` placeholders from drafting
- [ ] No fabricated sources (sources that don't exist or don't say what's claimed)
- [ ] Internal links from `2-reference/` wired in with descriptive anchor text — and at least 1 internal link present whenever the brand-articles inventory has relevant entries
- [ ] No naked URLs in the body
- [ ] Any unverifiable claims marked `[CITATION NEEDED]` rather than left unsourced
- [ ] Must-cite citation density ≥ 60% (numbers, studies, year-anchored facts only); otherwise `## Editor notes / Citation gaps` block emitted
- [ ] Voice-flagged statements (population claims, superlatives, brand mentions) listed in `## Editor notes / Voice-flagged statements (review)` for editorial decision — NEVER auto-linked

## When verification reveals a problem

If a stat in the draft is **wrong** (no source supports it), don't paper over it. Either:
- Replace the number with the actual one and adjust the surrounding sentence
- Cut the claim and rewrite the sentence to make the same argument without the disputed number

The draft was wrong before; making it look correct without fixing it is worse.

## Common source patterns to prefer

- **Direct sources** — for a third-party-tool claim, link to the tool's official docs or a primary-source publication like Search Engine Land; for a Google claim, link to Google's official docs or a Search Central blog post
- **Primary research** — academic papers, industry surveys with stated methodology
- **Recent over old** — within 2 years preferred for changing fields like SEO
- **Authoritative over popular** — DR/UR matters less than whether the source is the actual originator of the data

## Flag before save

If the draft makes claims that even with effort you can't verify, write a `## Editor notes` section at the bottom of the cited file listing:
- Each `[CITATION NEEDED]` location
- Brief note on what you tried and why it's unverified

The human editor decides whether to cut the claim or accept the risk.
