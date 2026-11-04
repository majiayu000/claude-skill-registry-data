---
name: seo-geo-aeo
description: >
  Ship search visibility that wins Google blue links (SEO), generative citations
  in ChatGPT/Perplexity/Claude/Gemini (GEO), and answer-engine slots in Google
  AI Overviews / AI Mode / featured snippets (AEO). Encodes the production
  playbook proven on the PIRX project: answer-first pages, extraction
  tables, primary-source density, multi-type JSON-LD, AI-crawler allowlists,
  IndexNow for Bing, entity/sameAs, and AI-referral measurement. Use when
  asked about SEO, GEO, AEO, generative engine optimization, answer
  engine optimization, AI Overviews, AI citations, ChatGPT/Perplexity ranking,
  schema/JSON-LD, llms.txt, IndexNow, title tags, content clusters, or
  "get cited by AI". Distinct from a GSC-only audit — this skill designs and
  implements the full stack.
---

# SEO + GEO + AEO Playbook

You are implementing **three surfaces at once**. They share one content system.
They do not share one metric.

| Surface | What wins | Primary index |
|---------|-----------|---------------|
| **SEO** | Rank + CTR in classic SERPs | Google |
| **GEO** | Get quoted in ChatGPT, Perplexity, Claude, Gemini | Bing (ChatGPT) + Google (Perplexity/Gemini) |
| **AEO** | Be the cited source in AI Overviews / AI Mode / snippets | Google |

**Non-negotiable thesis:** GEO is additive to SEO, not a replacement. ~80% of GEO is excellent fundamental SEO. Ranking top-10 no longer *guarantees* an AI citation — you also need extractability. Organic still sends far more raw traffic than all AI engines combined; AI-referred sessions convert much harder. Build both.

**Never fabricate stats, quotes, experts, or studies.** Engines treat that as adversarial. Find real sources or cut the claim. See [content-system.md](content-system.md).

---

## Step 0 — Bind the project

Do not start writing pages until these are named. Infer from the repo; ask only for gaps.

1. **Canonical host** (https, one host; apex 301s to it)
2. **Primary conversion URL** (the tool/signup/demo the content exists to feed)
3. **Entity facts** (legal name, founding, HQ, category, 1-sentence what-it-does) — identical everywhere
4. **Locked terminology** (words that must never appear; canonical names for the product)
5. **Money query** (the one head term) + **cluster queries** (long-tail that feed it)
6. **Author** (real Person with credentials + `sameAs` URLs)

Write them into a short `search-visibility.md` at the project root (or update it). Every later page inherits this.

---

## Step 1 — Pick the job

Infer from the user. If ambiguous, ask once.

| Signal | Job | Read |
|--------|-----|------|
| "audit the site / why aren't we ranking / GSC" | **Audit** | [technical-stack.md](technical-stack.md) then [entity-and-measurement.md](entity-and-measurement.md) |
| "write a post / landing / cluster" | **Content** | [content-system.md](content-system.md) |
| "schema, robots, sitemap, IndexNow, metadata" | **Technical** | [technical-stack.md](technical-stack.md) |
| "Wikidata, Reddit, YouTube, citations, GA4 AI channel" | **Entity + measure** | [entity-and-measurement.md](entity-and-measurement.md) |
| "full program / 90-day plan / playbook" | **Program** | all three, then the 90-day sequence below |

---

## Step 2 — The content law (every public URL)

Every indexable page — blog, tool, landing, comparison — follows this skeleton. Skip a layer and citation rate collapses.

```
1. ANSWER FIRST          Direct answer in the first screenful (≤ first 30% of the page).
                         Bold the verdict. 2–4 sentences. 44% of LLM citations come from here.
2. EXTRACTION TABLE      Exactly one self-contained comparison/data table near the top.
                         An LLM must be able to quote the table with no surrounding prose.
3. PRIMARY CTA           Early, specific, to the conversion URL. Repeat at the close.
4. QUESTION H2s          Each H2 is a real query. First sentence under it is a complete answer.
                         Then elaborate. One idea per section. Sections must stand alone.
5. EVIDENCE DENSITY      ≥1 verifiable number per ~100 words. Inline primary citations.
                         ≥1 attributable expert/source quote on guides.
6. DIFFERENTIATION       Short section: why THIS product, in locked terminology, with operator-locked proof only.
7. FAQ                   3–6 questions people actually type or ask a chatbot. Answers 2–4 sentences, quotable verbatim.
8. SOURCES               Bulleted list of every cited URL with a one-line parenthetical.
```

Title tag: primary query front-loaded, ≤60 characters, hook (number, audience, or concrete outcome) — not the bare keyword.
Meta description: 150–160 characters, query + benefit + CTA.
H1 matches title intent. Canonical is self. OG/Twitter complete (1200×630).

Full rules, anti-patterns, and QA gate: [content-system.md](content-system.md).

---

## Step 3 — Technical foundation (ship once, keep green)

Do these in order. Details and copy-paste artifacts: [technical-stack.md](technical-stack.md).

1. **One canonical host** + HTTPS + trailing-slash policy + `rel=canonical` on every public page
2. **robots.txt** — allow Googlebot, Bingbot, **and** AI retrieval bots (GPTBot, OAI-SearchBot, ChatGPT-User, PerplexityBot, Claude-SearchBot, ClaudeBot, Google-Extended, Applebot-Extended). Disallow app/auth/admin. Block abusive scrapers (Bytespider, CCBot). Sitemap URL declared.
3. **XML sitemap** of public URLs only; submit to Google Search Console **and** Bing Webmaster (ChatGPT reads Bing)
4. **IndexNow** on publish/update — Bing+Yandex instant ping. Google ignores it; do it anyway for GEO
5. **JSON-LD `@graph`** with **≥3 types** per URL. Schema must match visible content. Keep `FAQPage` even after Google killed FAQ rich results — it is now an AI-extraction signal
6. **Person author** on articles/guides (`jobTitle`, `url`, `sameAs`). Organization `sameAs` = Wikidata + LinkedIn + Crunchbase + socials
7. **SSR or prerender** the answer, table, and FAQ. JS-only main content is invisible to many AI crawlers
8. **`llms.txt`** (and optional `llms.txt`) at site root — cheap content map. **Do not invest maintenance** beyond keeping URLs accurate; no major engine uses it for retrieval. `robots.txt` is the file that matters
9. **Core Web Vitals** green on mobile (LCP < 2.5s, INP < 200ms, CLS < 0.1). Title/H1 in first paint
10. **hreflang** only if you truly have translated equivalents

---

## Step 4 — Information architecture

- **Pillar + cluster.** One pillar per money query. Cluster posts answer fan-out questions and link up with descriptive anchors (never "click here").
- **Tool pages are content pages.** ChatGPT over-cites product/tool URLs vs Perplexity. Put the answer, method, table, FAQ, and citations on the tool URL — not only a widget.
- **Predict-X-from-Y / comparison / how-to** pages own the long tail. Each must have non-trivial synthesis (unique table, unique sources, unique advice). Thin programmatic templates get a weakest-link domain penalty.
- **No cannibalization.** One URL owns one primary query. Others 301, canonicalize, or differentiate.
- Internal links: every new page gets 2–3 inbound links from related live pages in the same cluster.

---

## Step 5 — Entity layer (the GEO moat)

On-page extractability is necessary and not sufficient. Engines cite **entities they recognize**.

Priority order (full steps in [entity-and-measurement.md](entity-and-measurement.md)):

1. Identical NAP + one-sentence description on site JSON-LD, Wikidata, LinkedIn, Crunchbase, Product Hunt, G2/Capterra as relevant
2. Wikidata item with `official website` + `sameAs` mirrored in Organization schema
3. Wikipedia only after independent press — do not create a promo stub
4. Genuine Reddit/community answers (no astroturf). Perplexity and AI Overviews overweight Reddit
5. 2–3 YouTube explainers/comparisons (Wikipedia + YouTube + Reddit ≈ a large share of AI-cited media)
6. Digital PR for unlinked brand mentions in trade press

---

## Step 6 — Measure or you are guessing

Only a small minority of teams track AI search. Install this in week 1.

1. **GA4** — native "AI Assistants" channel, or a custom channel above Referral matching `chatgpt.com|chat.openai.com|perplexity.ai|claude.ai|gemini.google.com|copilot.microsoft.com`. Custom groups do not backfill — create immediately. AI Overviews have **no** separate referrer; use GSC.
2. **GSC** — domain property; AI Mode / AI Overview filter when available; question-query regex
3. **Bing Webmaster** — sitemap indexed (ChatGPT path)
4. **Share of voice** — monthly: 20 money prompts across ChatGPT, Perplexity, Gemini, AI Overviews. Record cited / not cited / competitor cited
5. **KPIs:** non-branded clicks + impressions, AI-referral sessions + conversion, citation SoV on the 20 prompts, Bing coverage

---

## 90-day sequence (when building a program)

| Days | Work |
|------|------|
| **1–30** | Canonical + robots AI allowlist + dual sitemaps + IndexNow + GA4 AI channel + GSC/Bing verify. Content-engineer the money URL and top 5 pages (answer-first, table, citations, FAQ, Person author, 3+ schema types). |
| **31–60** | Pillar + first cluster (8–12 URLs). Wikidata + listings `sameAs`. Author bylines. Refresh any page older than 90 days that still ranks. |
| **61–90** | Reddit/YouTube presence. Digital PR. Comparison/alternative pages. Citation SoV baseline → second measurement. Kill or 301 thin URLs. |

---

## Quality gate (nothing ships without this)

- [ ] First 150 words answer the primary query without throat-clearing
- [ ] One extraction table; every cell understandable alone
- [ ] Every H2 is a question; first sentence under it is a complete answer
- [ ] Every load-bearing number has a fetched, clickable primary source
- [ ] Zero fabricated quotes/stats; zero keyword stuffing (target term < 1% of words)
- [ ] FAQ answers are verbatim-quotable and match visible on-page FAQ
- [ ] JSON-LD `@graph` has ≥3 relevant types; URLs absolute; dates ISO-8601; author is Person
- [ ] Canonical, OG, Twitter, sitemap entry, IndexNow ping
- [ ] AI bots allowed; private routes disallowed
- [ ] 2–3 internal links in; 2–3 related links out
- [ ] Product claims use only operator-locked numbers
- [ ] Mobile CWV not regressing

---

## Anti-patterns (hard fails)

- Keyword stuffing, filler intros ("In today's landscape…"), unsourced superlatives
- FAQ schema for questions not visible on the page
- Blocking GPTBot / PerplexityBot / ClaudeBot / Google-Extended
- Thin city/template pages at scale
- Investing weeks in `llms.txt` instead of citability
- Treating AI Overviews as a GA4 "AI Search" channel (they are organic)
- Naming competitor formulas/trademarks the product forbids
- Publishing unverified product stats

---

## Coordination

- Sitewide GSC crawl + striking-distance list: use the project's `seo-analysis` skill if present, then apply **this** playbook to the fixes
- Single URL rewrite: apply [content-system.md](content-system.md) + schema from [technical-stack.md](technical-stack.md)
- Meta-only CTR work: title/description formulas in [content-system.md](content-system.md)
- Do not spawn a separate "GEO voice" that contradicts the product terminology skill
