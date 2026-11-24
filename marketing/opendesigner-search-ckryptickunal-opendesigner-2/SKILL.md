---
name: opendesigner-search
description: SEO, AEO and GEO. Gets a site found by Google and AI answer engines. Checks crawling, robots, sitemap, llms.txt, titles and markup, asks ChatGPT and Perplexity by hand, proposes fixes.
license: MIT
compatibility: Python 3.10+ (standard library, no network) for the checks. A browser the agent can drive, for the answer-engine probe.
metadata:
  version: "0.3.1"
  homepage: "https://github.com/ckryptickunal/OpenDesigner"
---

# OpenDesigner: search

Search engines rank pages. Answer engines, such as ChatGPT search, Perplexity and Google's AI Overviews, read a few pages and write an answer that cites them. Both start from the same thing: pages a crawler can read, that say plainly what they are about, in the words people ask with. This skill checks that, asks the engines what they see, and proposes fixes. It never changes the person's site, and never posts anywhere for them, without their yes.

## Words
- **SEO** (search engine optimisation): getting pages crawled, indexed and chosen in search results.
- **AEO** (answer engine optimisation): being the page an engine quotes when it answers a question directly.
- **GEO** (generative engine optimisation): being read and cited by AI answer engines.

The three share most of their work. Say one plain sentence, then the term.

## Start here
1. **Read what exists.** `opendesigner/PRODUCT.md` has a Site brief for a site that persuades (issue 48): Q-site-04 holds how people find it, the languages and the questions it should answer; Q-site-05 holds its page families. These are the targets. When they are missing, ask for the three or four questions customers ask before buying, once.
2. **Find the served pages.** Check what the server sends, not the source. Use a local production build (`dist/`, `out/`, `public/`, `_site/`, or whatever the build command writes) and the deployed site. A source file can look right while the served page is wrong.

## The order (most costly first)
1. **Can a stranger read it?** Open the deployed pages logged out. Is the text in the HTML, or does it only appear after JavaScript runs? Is a public page stuck behind a sign-in? Nothing below matters until this passes.
2. **Rule checks:** `python3 <skill>/scripts/search.py audit <build-folder> --base https://<site>`, read-only. It checks:
   - robots.txt for each search, user and training bot;
   - the sitemap, canonicals and `noindex` conflicts;
   - titles, descriptions and the h1;
   - text in the served HTML;
   - JSON-LD (it parses, and FAQ questions match the visible page);
   - llms.txt against the pages (lines no page states, new sections it leaves out, links to pages that are gone), orphan pages, and images without alt or size.

   Every finding carries its evidence. `search.py robots <file>` prints which bots a robots.txt lets in.
3. **Ask the answer engines:** a handful of questions, by hand, logged out, in a browser the person can see. `references/probe.md` covers what each engine shows and how to read it. Ask:
   - the brand question ("What is <name>?");
   - two or three category questions, in the customers' words from Q-site-04;
   - one how-to question.
4. **Turn what they searched and cited into page fixes:** `references/fixes.md`. Engines quote pages that answer the question directly in the asker's words, give something to copy (a file tree, a rule file, a prompt), and state each capability in one plain sentence. A page that only describes the product wins "which tool" questions and loses "how do I" questions.
5. **List off-site places** where the engines found the category answers: directories, awesome-lists, comparison roundups. These are proposals only: each submission or post needs the owner's yes.
6. **Report:** `references/report.md`.

## After every content change
A new headline, section, claim or picture makes the files around it stale. After each change:
1. Run `search.py audit` on the new build. It names llms.txt lines no page states any more, new sections it leaves out, and links to pages that are gone.
2. Propose updates to llms.txt, the share title and description, the share image (rebuilt from the page as it is now) and, when pages came or went, the sitemap. `review.py check` names share text the h1 no longer says; `engine.py review` names a share image older than the headline, hero, logo or brand colour.
3. Check that robots.txt still says what the owner decided, including about AI-training crawlers.

Each update waits for the owner's yes, like every fix.

## Rules and judgment
- **The script checks** what a rule can settle: a bot blocked, a missing canonical, a title past 60 characters.
- **The agent judges** everything else: what the engines' searches mean, which page answers which question, the wording, which listings matter.
- Never present a judgment as a measurement.

## Hard boundaries
- **Engines:** a handful of questions, typed by hand. Read what the engine's own page loads in the person's browser, as DevTools shows it: its answer, its sources, and the searches it reports.
  - Never call an engine's endpoints yourself.
  - Never script or repeat queries in bulk.
  - Never sign in, solve a CAPTCHA or create an account.
- **Off-site:** submissions, posts, listings and emails each need the owner's yes, item by item.
- **Never invent** statistics, quotes, reviews or sources. GEO (KDD 2024) found that quotes and statistics raise an engine's use of a page, but only real ones may be used: the owner's proof from Q-site-03, with its qualifiers.
- **No keyword stuffing, and no pages made at scale to rank.** Google's spam policies name both, and GEO measured stuffing at −8%.
- **Training crawlers** (GPTBot, ClaudeBot, Google-Extended) are the owner's choice. Blocking them does not remove a site from search; never report it as an error.
- **FAQPage and HowTo markup that matches the page** is reported as info ("no Google rich result"). Never suggest removing it: answer engines may still read it.
- **Checks report.** A fix to the site waits for the person's yes (AGENTS.md).
- **Live fetching:** `search.py audit --live` is off until the owner approves it. Until then, check the deployed site in a browser.

## What it cannot do
Say these plainly, with the next step for each:
- backlinks: outreach and listings, with the owner;
- keyword volumes: they need the owner's Search Console or a paid tool;
- Search Console and Bing Webmaster data: ask the owner for the reports;
- field Core Web Vitals: ask for a PageSpeed Insights run.

If the site has five pages, the limit is content and links, not technical fixes. Say so.

## References
- `references/probe.md`: what ChatGPT, Perplexity and Claude show, how to read it, and a worked example.
- `references/fixes.md`: from the engines' searches and citations to page fixes.
- `references/practices.md`: each practice with its source and how strong it is: platform docs, studies, practice.
- `references/report.md`: the report's shape.

If something in OpenDesigner itself was missing, wrong or confusing, record it with `engine.py feedback "..." --kind gap|bug|confusing|idea` (`references/improve.md` in the opendesigner skill). Nothing is posted without the person's OK.
