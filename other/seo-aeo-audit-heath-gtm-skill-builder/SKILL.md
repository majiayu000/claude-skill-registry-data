---
name: seo-aeo-audit
description: Audit a page or a site for both classic search and answer-engine visibility, then return prioritized fixes so an AI answer engine will actually quote you. Checks entity clarity, structured answers, schema, internal links, and freshness, and ranks every fix by effort against impact. Trigger on "audit my SEO", "why don't I show up in AI answers", "will ChatGPT cite my page", "check my page for search", "AEO audit", or "how do I rank for this".
---

# SEO and AEO Audit

## What this does
Reads a page (or a set of pages) and scores it two ways at once: can a classic search engine rank it, and can an answer engine lift a clean quote from it. Then it returns a ranked fix list, each fix with the reason it matters and the effort it takes, so you work the cheap high-impact items first. It is written for the world where half your traffic never clicks, because the answer got read aloud.

## What you'll need
You do not need to connect anything to get value today. Paste a URL or the page text and the skill runs now. Connect the tools and it grounds the audit in how the page already performs.

- Works today with: a URL, or the raw page text plus the target question you want to win. Paste it and the skill audits it now.
- More powerful connected to a search console: it sees the queries you already rank near, so the fixes target winnable ground, not fantasy keywords.
- Sharper with a web-analytics tool: it sees which pages earn attention, so you fix the pages that can move the number.
- Sharper with a CMS: it can check schema and internal links across templates, not one page at a time.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the page you give it today and gets sharper as you connect tools. It never claims a ranking it cannot see. An unknown position is labeled unknown, not invented.

- **Bring your data**: paste a URL or the page text plus the question you want to own. The skill returns the full two-track audit today. No connection required.
- **Connect your tools**: the same skill pulls impressions, positions, and traffic automatically and points the fixes at queries you can realistically win.
- **Just exploring**: no page yet? Get the checklist, the exact signals it grades, and a worked example, so you see the shape before you run it.

Every run ends with the one thing that would sharpen the next run, a query source to connect or a page to feed it.

## Customize this for yourself
This was built for a content site that wants to be quoted by answer engines. Set these to your stack:

| Set this | What it is | Example |
|---|---|---|
| TARGET_QUESTION | the query the page should own | "how do I export to CSV" |
| ENTITY | the thing the page is about | your product, a concept, a place |
| SCHEMA types | structured data to check | FAQPage, HowTo, Article, Product |
| SEARCH_CONSOLE | your query-data connector | a search console |
| ANALYTICS | your web-analytics connector | a web-analytics tool |
| CMS | where the page is edited | a CMS |
| FRESHNESS_DAYS | age at which content is stale | 180 (re-tune to your topic) |

Audit against the one question the page should win. A page that answers ten questions ranks for none. Run it again per question.

## The method

### Entity clarity
An answer engine has to know what the page is about in one pass. The skill checks that the ENTITY is named plainly, defined early, and consistent. Vague pages do not get quoted.

### Structured answers
Answer engines lift the cleanest self-contained passage. The skill checks that the TARGET_QUESTION is answered directly, high on the page, in a liftable block: a short definition, a list, or a labeled step sequence. If the answer is buried under a story, it flags it.

### Schema
Checks whether the right SCHEMA type is present and valid for the page's job (an FAQ block, a how-to sequence, an article byline and date). Missing or malformed schema is a named fix, not a vague "add structured data."

### Internal links
Checks that the page is linked to from related pages with descriptive text, and that it links out to its own supporting pages. An orphan page is invisible to both kinds of engine.

### Freshness
Flags content older than FRESHNESS_DAYS with no update, and checks that a real published-or-updated date is visible. Answer engines discount stale pages on time-sensitive topics.

### Prioritized fix list
Every finding is scored effort against impact and sorted. Cheap high-impact fixes go to the top. You get a worklist, not a wall of red.

## Quality gates
- No claimed ranking or position without a connected query source. Unknown stays unknown.
- Every fix names the specific element to change, never "improve your content."
- Illustrative traffic or position numbers are marked as examples, never presented as your real data.

## Output (example)
```
SEO + AEO AUDIT · page: /guide/csv-export · question: "how do I export to CSV"

Classic search:   66 / 100
Answer-engine:    41 / 100   (the gap is why you are not quoted)

Top fixes (effort -> impact):
  1. LOW  -> HIGH   Add a 2-sentence direct answer above the fold.
                    Right now the answer starts in paragraph 5.
  2. LOW  -> HIGH   Add HowTo schema to the numbered steps.
  3. MED  -> HIGH   Link this page from the 3 related feature pages.
                    It is currently an orphan.
  4. LOW  -> MED    Add a visible "updated" date. Last touch: unknown.
  5. MED  -> MED    Break the wall of text into labeled steps.

Next: connect a search console to target queries you already rank near.
```

## Where the inputs come from
The URL or page text and the TARGET_QUESTION come from you. FRESHNESS_DAYS (180) is a default, not a law, tune it to how fast your topic moves. Positions and impressions come from a connected search console, traffic from a connected web-analytics tool, and schema and link checks from the page itself or a connected CMS. The thresholds are yours to move.

## Example chat

**You:** Audit this page for both SEO and AI answer visibility. Here's the URL, target question is "how do I export to CSV."

**Claude:** Audited both tracks. The gap between them is the story.
```
SEO + AEO AUDIT · page: /guide/csv-export · question: "how do I export to CSV"
Classic search:   66 / 100
Answer-engine:    41 / 100   (the gap is why you are not quoted)

Top fixes (effort -> impact):
  1. LOW  -> HIGH   Add a 2-sentence direct answer above the fold.
                    Right now the answer starts in paragraph 5.
  2. LOW  -> HIGH   Add HowTo schema to the numbered steps.
```
The insight worth sitting with: the page ranks fine, 66/100, but scores far lower on answer-engine visibility, 41/100, because the actual answer is buried in paragraph five. Classic search tolerates that. An answer engine won't lift a quote from paragraph five.

**You:** Why is the orphan-page fix ranked medium effort instead of low?

**Claude:** Because fixing it means editing three other pages to add the links, not just this one, that's more surface area than a one-page schema tweak, even though the impact is just as high. Sharpener: connect a search console and I'll target the fixes at queries you're already ranking near instead of the one question you told me to check.

## Go further
The one-page audit proves the gap is real. Here is the version that watches the whole site.

- **Audit the whole site on a schedule.** Run this as a scheduled Claude task across your CMS templates so every page gets re-scored monthly instead of one at a time by request.
- **Target fixes at winnable queries.** Connect Google Search Console so the fix list points at questions you're already close to ranking for, not guesses.
- **Track the AEO score over time.** Log each run's score to a sheet or Amplitude so you can see whether the gap between classic and answer-engine visibility is closing.

The fix list gets sharper every run instead of starting from scratch each time.

## Make it yours
Fork it. Change the schema types, the freshness window, the way fixes are ranked. The point is not to chase a checklist. It is to get the page quoted and clicked for the one question it should own. Built by an operator. Customize it, break it, make it better.
