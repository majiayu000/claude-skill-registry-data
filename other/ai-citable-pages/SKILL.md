---
name: ai-citable-pages
description: Restructure one page passage by passage so ChatGPT, Perplexity, Copilot, Claude and Google AI Overviews can lift accurate, self-contained answers that name your brand. Use for "make this page citable", "AI quotes competitors, not us", "rewrite this page for AI answers" or AEO / LLM SEO / GEO page edits.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/ai-citable-pages
---

# Make a page citable by AI engines

Take one page, map it to the prompts and sub-questions it should answer, and rework it section by section so every passage answers one question on its own, names the business, and carries facts an engine can quote without getting them wrong. You hand back a passage-level before/after diff, the facts checked and their sources, the blockers removed, and a re-test plan.

> **Romeo's rule:** Write every section as if it will be torn out and read alone, because that is exactly what an answer engine does with it.

## Use this when

- A page is indexed and ranks, but AI answers cite a competitor's or a third party's page for its question.
- The page gets cited but the answer doesn't name the business, or quotes the wrong part of the page.
- A pricing, product, comparison, docs or help page holds the right facts but buries them in tabs, images, PDFs or marketing copy.
- You're about to publish a page for a money prompt and want it quotable from day one.
- `ai-brand-facts` traced a wrong claim to a vague or ambiguous passage on your own site.

## Don't use this for

- Deciding which sub-questions need a section or a page across the site → `query-fan-out-coverage`; finding the prompts in the first place → `ai-prompt-research`.
- Measuring AI visibility across engines and mapping the third-party sources they cite → `ai-search-visibility`.
- Crawler access, robots rules for AI bots and JavaScript rendering at platform level → `ai-agent-readiness` and `technical-seo-audit`.
- Title, meta description, internal links and on-page basics against a target keyword → `on-page-seo-review`.

## What you need

### Required

- The page URL, or its raw HTML (view-source, not text copied from the screen), plus the rendered version if it's built with JavaScript.
- What the business sells, to whom, and the 1 to 5 prompts this page should be cited for. If unknown, step 1 derives them and marks them `inferred`.
- A way to confirm facts: the fact sheet from `ai-brand-facts`, or someone who can check prices, limits and claims.

### Helpful

- Search Console queries for this URL (last 3 months) and its impressions in the Search Generative AI performance report.
- Bing Webmaster Tools AI Performance: citations for this URL and, where the report links them to pages, the grounding queries that retrieved it.
- Current AI answers for the target prompts, with citations, from an `ai-search-visibility` baseline or a tracker export.
- The competitor or third-party pages that get cited instead.
- Sources for statistics, and a named expert or customer willing to be quoted.

### No tools?

Use `view-source:` to read the raw HTML and search it (Ctrl+F) for each key fact; anything missing there is invisible to crawlers that don't run JavaScript. Turn JavaScript off in DevTools (Command menu → "Disable JavaScript") and reload to see roughly what they get. The Rich Results Test shows Google's rendered HTML for any public URL under "View tested page". Run each target prompt by hand in ChatGPT with search on, Perplexity, Copilot and Google (AI Overview and AI Mode), twice each in a private, logged-out window, and paste the answers and cited links into a sheet.

## Ground rules

- Answer engines quote passages, not pages. A section that only makes sense after the intro ("as mentioned above", "it", "our tool") is a section an engine can't safely quote.
- One page, one job. Cover the sub-questions that belong to this page's intent; send the rest to their own pages instead of turning this one into a dump.
- Answer first, then support. The opening sentences of a section carry the answer; detail, evidence and caveats follow.
- Accuracy beats quotability. Never sharpen a claim beyond what's true to make it easier to lift; the engine lifts the overstatement too, and the business owns it.
- Evidence earns citations: sourced numbers, named quotes and links to primary sources. Repeating keywords doesn't.
- No special markup gets a page into AI answers. Google says none is needed for its AI features and that structured data must match the visible text; treat schema as support, not the lever. Google also says content needn't be broken into tiny pieces for AI: clear sections help readers and every engine, but don't fragment a page into snippets.
- One version for everyone. No hidden text, no AI-only page versions, no instructions to assistants inside the content. Google's spam policies list attempting to manipulate generative AI responses in Google Search as spam.
- Freshness must be real. Change dates only when the content changed.
- Keep the page good for people: it still has to persuade and convert. A rewrite that reads like a glossary is a loss.

## Steps

1. **Map the page to its prompts and sub-questions.** List the 1 to 5 prompts the page should be cited for, then the sub-questions an engine is likely to look up for each: definition, how it works, price, who it's for, limits, comparison, setup.
   - Sources: Search Console queries for the URL (question-style and long ones), Bing AI Performance grounding queries, People Also Ask, the topics current AI answers cover, and sales and support questions. Label the list `inferred` unless you saw the queries.
   - Mark each sub-question: answered here, belongs here but missing, or belongs on another page (note which).
   - Baseline: run each prompt 2 to 3 times per engine in clean sessions. Record whether this URL is cited, which sentence is quoted (search the page for it), and which brand is named.

2. **Cut the page into passages.** List every H2 and H3 section with its heading, its first 80 words, the question it answers (or "none"), the facts it contains, and whether it names the business.
   - Give each one action: keep, rewrite, split (two questions in one section), merge (one question spread over three sections), move to another page, or cut.
   - Sections that answer no target question ("Why choose us", "Our journey") are candidates to cut or shrink, not to optimise.

3. **One question per H2 or H3, in buyer wording.** Each heading names the question or topic in the words buyers use, taken from step 1, not from the brand guidelines.
   - "How much does Acme cost for a 10-person team?" or "Acme pricing for small teams", not "Simple, transparent pricing".
   - Microsoft's guidance (October 2025) asks for H2 and H3 headings that work like chapter titles and one idea per section. Vague labels ("Overview", "Learn more", "Features") are `Fix next`.
   - Keep the hierarchy honest (H3s sit under the H2 they belong to) and don't force the brand name into every heading.

4. **Lead each section with a 40 to 80 word answer that stands alone.** It names its subject in full in the first sentence (the business and category, or the product, plan or feature; never "it", "we" or "our tool"), answers directly (yes, no, a number or a definition first), includes the key condition (for whom, on which plan, in which country), and points to nothing outside itself.
   - Before: "Our flexible plans grow with you. Whether you're just starting or scaling fast, we've got you covered. Check out the options below!"
   - After: "Acme payroll costs $6 per employee per month on the Core plan and $10 on Plus, billed monthly in US dollars, plus a $40 monthly base fee on both (prices as of March 2026). There is no free plan; the 30-day trial includes every Plus feature. Companies with more than 200 employees get custom pricing."
   - One claim per sentence, plain punctuation, no "click below" or "see the table". Then the detail, examples and caveats.
   - 40 to 80 words is a working range, not an engine rule: long enough to carry the condition, short enough to quote whole.
   - Yes/no questions start with yes or no. Definitions use "X is a Y that Z".

5. **Make facts liftable.** Each fact should survive being quoted on its own.
   - Numbers in digits with units, currency, billing period and tax treatment; dates for anything that changes ("as of March 2026"); ranges with their conditions. "From $29" without saying for what is `Fix next`.
   - Exact names for integrations, platforms, standards and plans, spelled as their owners spell them.
   - Plans, specs and comparisons in a real HTML `<table>` with `<th>` headers, not an image, a canvas or a grid of `div`s. A monthly/annual toggle must leave one clearly labelled set of prices in the HTML.
   - A "who it's for" and "who should pick something else" line on product, pricing and comparison pages. Engines answer "best X for Y" with segments, and a page that names its segment is easier to match to one (`inferred`).
   - Prices and claims in the text match the pricing page, the fact sheet and the markup. Any disagreement is `Fix now`.

6. **Add sourced statistics, quotations and citations.** In the Princeton GEO study (Aggarwal et al., KDD 2024), adding quotations, statistics and source citations raised a source's visibility in generative engine answers by up to about 40% on their benchmark, while keyword stuffing did slightly worse than doing nothing. Treat it as directional: it was tested on a research benchmark and a sample of Perplexity queries, not on today's engines.
   - Statistics: source, sample and date inline, linked to the primary source, not to a blog that repeats it.
   - Quotations: a named person with role and a reason to be believed (customer, practitioner, in-house expert), saying something specific.
   - Citations: link standards, regulations, docs and studies where a claim depends on them.
   - Original data (usage numbers, a survey, a benchmark) with method, sample size and date is the strongest material a page can have.
   - Never invent a number or a quote. An unsourced statistic gets a source or gets cut; mark it "not checked" until then.

7. **Remove the blockers.** Microsoft's October 2025 guidance names these: answers hidden in tabs or expandable menus ("AI systems may not render hidden content"), key details only in images, core information in PDFs, unanchored claims like "next-gen" or "cutting-edge", long walls of text, and overloaded sentences. Also check:
   - JavaScript-only content: if the answer isn't in the raw HTML, many AI crawlers won't see it; they are widely reported not to run JavaScript, and no vendor promises they do. Googlebot does render. `Fix now` for the main answer on a money page; the platform fix goes to `technical-seo-audit`.
   - Tabs and accordions: Google indexes collapsed content that is in the HTML, but keep each section's main answer visible by default and leave only secondary detail collapsed.
   - Unanchored superlatives ("best", "#1", "fastest", "most trusted"): anchor them ("rated 4.7/5 from 1,240 G2 reviews, October 2026") or cut them.
   - In Google, `nosnippet` or a very low `max-snippet` on the page, or `data-nosnippet` around the passage you want quoted; `NOARCHIVE` or `NOCACHE`, which limit Copilot's use of the page until Bing stops reading them for AI on 1 March 2027.
   - Facts behind a login, cookie wall, interstitial or "contact sales" form.

8. **Docs and help-centre pages.** They are cited for "does X do Z", "how do I" and troubleshooting prompts, and vendor studies report docs and help pages as a large and growing share of ChatGPT citations for software brands.
   - One task per page, titled with the task and the product ("Connect Acme to QuickBooks Online"), with plan or version availability stated in the first lines ("Available on Plus and Enterprise").
   - Prerequisites, numbered steps in text (screenshots support, never replace, the steps), exact error messages as text, and the expected result.
   - Retired features are marked with a date and a replacement ("Removed in v4, March 2026; use Exports instead") rather than left looking current.
   - Public docs are indexable: no login wall, no accidental `noindex` or robots block, linked from the main site, and present in a sitemap.
   - Changelog entries carry dates, so engines can tell which statement is current.

9. **Keep freshness honest.** Update the facts first, then the visible "updated" date and `dateModified`, and only when the content changed materially (prices, steps, facts, recommendations), not for typo fixes or by a script. Google's helpful content guidance treats changing dates to make pages look fresh when the content hasn't substantially changed as a warning sign. Vendor studies find AI-cited pages skew fresher than organic results (Ahrefs, July 2025, directional), which is a reason to keep facts current, not to bump dates.

10. **Serve the same content to bots and people.** If you can fetch URLs, request the page with a normal browser user agent and with Googlebot, bingbot and OAI-SearchBot user agents and compare the main content; a CDN, A/B test or bot-management rule sometimes serves bots a different or empty page. Never build an AI-only version. Markdown copies for agents must match the HTML page (`ai-agent-readiness`). JSON-LD states only what the visible text states (`schema-markup`).
   - Bot protection that verifies crawler IPs may block a spoofed Googlebot user agent, so a 403 on your test isn't proof of a problem; confirm with the live test in URL Inspection.

11. **Hand back the diff and a re-test plan.** Show every changed section as before and after, with the facts and sources it relies on.
   - Re-test after the page has been recrawled: check the last crawl date in Search Console URL Inspection and Bing's URL Inspection; submit through IndexNow or Bing Webmaster Tools.
   - Same prompts, same engines, 2 to 3 runs each, clean sessions. Record: cited or not, which passage was quoted, whether the business was named, whether the quoted facts were correct.
   - Repeat monthly for at least two months and count a change as real only if it holds in both. Also watch Bing AI Performance citations for the URL and its Search Console generative AI impressions.

## What to hand back

Fill in this template. Every change carries a priority label and an evidence label with confidence.

```markdown
# Citable page rewrite: [URL], [date]

**What I found:** [one line, e.g. "Cited in 1 of 9 runs; the price sits in an image and every section opens with marketing copy."]
**What matters most:** [one line]
**What to do first:** [one line]

## Prompts and sub-questions
- [prompt] ([money | supporting]); sub-questions: [list] ([inferred | seen | tool]); answered in: [section | missing | belongs on URL]
- Baseline [date]: cited in [k of n] runs on [engines]; quoted passage: "[text]"; business named in [k of n]

## Passage diff
### [old heading] → [new heading]
- Action: [rewrite | split | merge | move | cut | keep] - [Fix now | Fix next | Worth doing] - [seen | tool | inferred], [high | medium | low]
- Before: "[first 80 words]"
- After: "[new opening answer, 40-80 words]"
- Facts used: [fact] - source: [URL or owner], [date] - confirmed: [yes | needs owner]

## Blockers removed
- [blocker] in [section] - fix: [change] - [label]

## Evidence added
- [statistic | quote | citation] - source: [URL], [date]

## Freshness, parity and markup
- Updated date: [changed because / left unchanged because]
- Bot vs browser content: [matched | differs: detail | not checked]
- Markup vs visible text: [matches | mismatches listed]

## Leave it
- [what looks like a gap but isn't worth the time, and why]

## Re-test plan
- Prompts: [list]; engines: [list]; runs: [n]; first re-test after recrawl ([last crawl date]), then monthly on [date]
- Success looks like: [e.g. cited in 4+ of 9 runs with correct price quoted]

## What I could not check
- [item, and what would verify it]
```

## Stop and flag if

- The page isn't indexed, returns a non-200 status, carries `noindex` or is blocked in robots.txt. Rewriting passages won't help; run `technical-seo-audit` first.
- A fact can't be confirmed (price, limit, compliance status, a customer number). Leave "needs owner confirmation" in the draft; never guess.
- The rewrite touches legal, medical, financial or compliance wording. The owner or their legal reviewer signs it off.
- The user asks for hidden text, AI-only versions, instructions aimed at assistants, invented statistics or quotes, or dates bumped without changes. Decline that part.
- Publishing the change: draft it, and edit the live page only with explicit permission.
- Unacceptable output: advice not tied to a named section, statistics without sources, a rewrite that changes a fact, or any promise that the page will be cited.

## Next step

- Run `seo-content-qa` on the rewritten page before it ships.
- Run `query-fan-out-coverage` with the sub-questions that belong on other pages.
- Run `schema-markup` to bring the JSON-LD in line with the new visible facts.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
