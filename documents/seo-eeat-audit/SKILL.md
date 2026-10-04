---
name: seo-eeat-audit
description: >
  Standalone E-E-A-T scoring rubric for a URL or content draft. Scores
  Experience, Expertise, Authoritativeness, and Trust 0-5 each using concrete
  detectable signals, framed per Google's creating-helpful-content doc.
  Use when user says "E-E-A-T", "EEAT", "experience expertise",
  "trust signals", or "author authority".
allowed-tools:
  - Read
  - Bash
  - WebFetch
---

# E-E-A-T Audit & Scoring

<!-- Updated: 2026-06-10 -->

## Framing (state this in every report — from Google's helpful-content doc)

- **E-E-A-T is NOT a specific ranking factor.** Google's systems use a mix of
  factors that can *identify* content with good E-E-A-T.
- **Quality raters** use E-E-A-T to evaluate whether ranking systems are
  working; rater data is not used directly in ranking ("feedback cards from
  diners"). Rater guidelines: https://services.google.com/fh/files/misc/hsw-sqrg.pdf
- **Trust is the most important member.** The others contribute to trust;
  content doesn't have to demonstrate all four.
- **YMYL gets extra weight:** topics affecting health, financial stability,
  safety, or societal welfare are held to stronger E-E-A-T. Detect YMYL and
  raise the pass bar one point per dimension.

## Inputs

- **URL** — fetch with WebFetch (fallback `curl -sL`), or
- **Local draft** — Read tool (markdown/HTML). For drafts, score content-side
  signals only and mark site-level signals (HTTPS, about page) as N/A.

## Execution

1. Fetch the page HTML; also fetch the homepage, `/about`, and `/contact`
   (HEAD or GET) to verify site-level trust pages exist.
2. Detect signals per dimension using the rubric below (HTML parsing
   heuristics: bylines, `rel=author`, Person/ProfilePage JSON-LD, `<time>`
   elements, outbound citation links, first-person experience markers).
3. Score each dimension 0-5 **with a verbatim evidence quote** from the page
   for every point awarded or withheld.
4. Run the "Who, How, Why" questions (below).
5. Recommend the 3 highest-impact improvements (lowest-scoring dimension
   first; Trust outranks ties).

## Scoring Rubric (0-5 per dimension)

### Experience — first-hand use or involvement
Detectable signals:
- First-person evidence markers: "we tested", "I used", "after 6 months of..."
- Original photos/screenshots/video clearly taken by the author (not stock)
- Concrete specifics only a participant would know (test counts, settings,
  prices paid, dates visited)
- Before/after results, process documentation, original data
- For reviews: evidence of the work involved, per Google's product reviews
  guidance (https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews)

Score guide: 0 = pure summary of other sources; 3 = some first-hand detail;
5 = thoroughly documented first-hand experience with evidence.

### Expertise — demonstrable knowledge
Detectable signals:
- Author byline present where readers would expect one
- Byline links to a bio/profile page with relevant credentials, background,
  and areas covered (ProfilePage/Person markup is a plus)
- Expert review attribution ("Medically reviewed by...") on YMYL content
- Technical depth appropriate to audience; claims sourced; no easily-verified
  factual errors

Score guide: 0 = anonymous, unsourced; 3 = named author with bio; 5 = credentialed
expert (or demonstrable enthusiast) with linked, verifiable background.

### Authoritativeness — recognized go-to source
Detectable signals:
- Citations TO authoritative external sources (and being cited — check via
  Ahrefs/`/seo-ahrefs-backlinks` if available)
- Site has a clear primary topic/purpose and topical depth (related content)
- Brand/author presence beyond the site (`sameAs` links, recognized outlets)
- "If someone researched this site, would they find it widely recognized as an
  authority on its topic?" (Google's expertise question)

Score guide: 0 = no sourcing, no topical focus; 3 = well-sourced within a
focused site; 5 = demonstrably recognized authority on the topic.

### Trust — the most important dimension
Detectable signals:
- HTTPS with valid certificate
- About page, contact page with real contact info (address/email/phone)
- Visible `datePublished` / `dateModified` stamps that aren't gamed
- Editorial/review/corrections policy (especially news/YMYL)
- Privacy policy and terms; clear ad/affiliate disclosure
- Headline matches content (no exaggeration or shock framing)
- No spelling/production sloppiness; functioning links

Score guide: 0 = anonymous site, no policies, mismatched claims; 3 = HTTPS +
about/contact + dates; 5 = full transparency stack incl. corrections policy
and disclosures.

## "Who, How, Why" Check (from creating-helpful-content)

- **Who:** Is it self-evident who authored the content? Are there bylines where
  expected? Do bylines lead to author background?
- **How:** Is the production method shown where it builds trust (testing
  methodology, evidence of work)? If automation/AI substantially generated the
  content: is that self-evident through disclosure, with background on how and
  why AI was used?
- **Why:** Created primarily to help people who arrive at the site — or
  primarily to attract search visits? (If the latter, route to
  `/seo-helpful-content` for the full self-assessment.)

## Output

```
## E-E-A-T Audit — <URL or draft>

> Framing: E-E-A-T is not a direct ranking factor; raters use it to validate
> Google's systems. Trust is the most important dimension.
YMYL topic: YES/NO (bar adjusted accordingly)

| Dimension | Score | Key evidence (quoted) |
|---|---|---|
| Experience | X/5 | "..." |
| Expertise | X/5 | "..." |
| Authoritativeness | X/5 | "..." |
| Trust | X/5 | "..." |
| **Overall** | XX/20 | weakest: <dimension> |

### Who / How / Why
- Who: ...
- How: ...
- Why: ...

### Top 3 Highest-Impact Improvements
1. <fix on weakest dimension, Trust prioritized on ties>
2. ...
3. ...
```

## Cross-references

- `/seo-content` — broader content quality audit (readability, structure,
  keyword coverage) that embeds a lighter E-E-A-T pass
- `/seo-helpful-content` — people-first self-assessment gate
- `/seo-rich-results` — ProfilePage/Person markup to reinforce author signals
- Source doc: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
