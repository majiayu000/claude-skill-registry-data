---
name: seo-helpful-content
description: >
  Pre-publish (or retroactive) content-quality gate implementing Google's
  official self-assessment questions from the creating-helpful-content doc,
  plus 2024 spam-policy red flags. Verdict: PUBLISH / REVISE / RETHINK.
  Use when user says "helpful content", "people-first", "content
  self-assessment", "is my content helpful", or "content quality gate".
allowed-tools:
  - Read
  - Bash
  - WebFetch
---

# Helpful Content Gate (People-First Self-Assessment)

<!-- Updated: 2026-06-10 -->

Implements Google's own self-assessment from
https://developers.google.com/search/docs/fundamentals/creating-helpful-content.
Walk EVERY question with YES / NO / PARTIAL + one line of evidence from the
content. Google also suggests getting an honest assessment from people
unaffiliated with the site — this skill plays that role.

## Inputs

- **URL** — WebFetch (fallback `curl -sL`), or
- **Local file/draft** — Read tool
- Optional context: site purpose, intended audience, whether AI assisted

## Execution

1. Fetch/read the content; identify topic, format, and apparent audience.
2. Walk **Section A** (content & quality), **Section B** (expertise),
   **Section C** (people-first) — each answer YES/NO/PARTIAL + evidence quote.
3. Walk **Section D** (search-engine-first warning signs) — here YES answers
   are red flags.
4. Run **Section E** spam-policy screen (2024 policies).
5. If AI-assisted, apply the **AI content** rules.
6. Issue verdict with prioritized revision list.

## Section A — Content and Quality Questions (Google's list)

- Does the content provide original information, reporting, research, or
  analysis?
- Does it provide a substantial, complete, or comprehensive description of the
  topic?
- Does it provide insightful analysis or interesting information beyond the
  obvious?
- If drawing on other sources, does it avoid simply copying/rewriting them and
  add substantial value and originality?
- Does the main heading or page title provide a descriptive, helpful summary?
- Does the heading/title avoid exaggerating or being shocking?
- Is this a page you'd bookmark, share with a friend, or recommend?
- Would you expect to see it referenced by a printed magazine, encyclopedia,
  or book?
- Does it provide substantial value compared to other pages in search results?
- Is it free of spelling/stylistic issues?
- Is it produced well — not sloppy or hastily made?
- Is it NOT mass-produced/outsourced across many creators or sites such that
  pages don't get attention or care?

## Section B — Expertise Questions (Google's list)

- Is information presented in a way that makes you want to trust it — clear
  sourcing, evidence of expertise, author/site background (author page, About
  page)?
- Would someone researching the site come away seeing it as well-trusted or
  widely recognized as an authority on its topic?
- Is it written or reviewed by an expert or enthusiast who demonstrably knows
  the topic well?
- Is it free of easily-verified factual errors?

## Section C — People-First Signals (YES = good)

- Existing/intended audience would find it useful coming directly to the site?
- Clearly demonstrates first-hand expertise and depth of knowledge (actually
  used the product/service, visited the place)?
- Does the site have a primary purpose or focus?
- Will readers leave feeling they've learned enough to achieve their goal?
- Will readers leave feeling they've had a satisfying experience?

## Section D — Search-Engine-First Warning Signs (YES = red flag)

- Content primarily made to attract search engine visits?
- Producing lots of content on many topics hoping some performs?
- Using extensive automation to produce content on many topics?
- Mainly summarizing what others say without adding much value?
- Writing about things only because they're trending, not for your audience?
- Will readers need to search again for better information elsewhere?
- Writing to a word count because of a believed Google preference? (Google:
  there is no preferred word count.)
- Entered a niche with no real expertise, mainly for traffic?
- Promising an answer to a question that has no answer (e.g., unconfirmed
  release dates)?
- Changing dates to seem fresh without substantial content changes?
- Adding/removing lots of content mainly to seem "fresh" for rankings?
  (Google: it won't help.)

SEO itself is fine — people-first content plus SEO is Google's recommended
combination; search-engine-first content is the problem.

## Section E — Spam Policy Screen (2024 policies)

From https://developers.google.com/search/docs/essentials/spam-policies:

- **Scaled content abuse:** many pages generated primarily to manipulate
  rankings, not help users — regardless of how made (gen-AI without added
  value; scraped/synonymized/translated feeds; stitched content; multi-site
  networks hiding scale; keyword pages that make little sense to a reader).
- **Site reputation abuse:** third-party content published on a host mainly to
  exploit the host's established ranking signals (sponsored payday-loan
  reviews on an .edu, white-label coupons on a news site). NOT violations:
  wire services, syndicated news, genuine UGC/forums, editorial columns,
  advertorials meant for the publication's own readers, normal affiliate links.
- **Expired domain abuse:** repurposing an expired domain's history to host
  low-value content (casino content on a former school domain).

Any confirmed hit here = automatic RETHINK verdict.

## AI-Generated / AI-Assisted Content

From https://developers.google.com/search/docs/fundamentals/using-gen-ai-content:
automation is acceptable when people-first; using AI primarily to manipulate
rankings violates the scaled content abuse policy. Check:

- Accuracy, quality, relevance — including auto-generated titles, meta
  descriptions, structured data, and alt text
- Context for users: disclose how automation was used where readers would
  reasonably ask "how was this created?" (the "How" from Who/How/Why)
- Ecommerce: Merchant Center requires IPTC `DigitalSourceType`
  `TrainedAlgorithmicMedia` metadata on AI-generated images, and AI-generated
  product data must be labeled

## Output

```
## Helpful Content Gate — <URL or draft>

### A. Content & Quality        (12 questions)
| Question | Answer | Evidence |
|---|---|---|
| Original information/research? | YES/NO/PARTIAL | "..." |
... (every question, all sections)

### D. Search-Engine-First Flags: N raised
### E. Spam Policy Screen: CLEAR / VIOLATION (<policy>)
### AI content: N/A or compliant/issues

### Verdict: PUBLISH | REVISE | RETHINK
- PUBLISH — A/B/C mostly YES, ≤2 PARTIALs, no D flags, E clear
- REVISE  — fixable gaps: list revisions in priority order
- RETHINK — multiple D flags or any E violation; the premise (the "Why")
  is search-first — revision won't fix intent

### Prioritized Revisions
1. ...
```

## Cross-references

- `/seo-eeat-audit` — deep E-E-A-T scoring (trust/author signals)
- `/seo-content` — structural/readability content audit
- `/seo-ai-optimization` — Google AI feature readiness (cites this gate as the
  main content lever)
