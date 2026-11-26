---
name: devlogMaxxing
description: Write a devlog page on log's site (log.listeningkit.com/devlog/<slug>) that tells the owner's own story about a tool or a competitor, ranks on Google for the keyword people search, and gets cited by ChatGPT, Perplexity and Google's AI answers. The worked example is /devlog/xreacher-alternative. Use when the owner asks for "a devlog", "a page like the Xreacher one", "an <x> alternative page", "a vs page", or to turn something he tried into a page.
---

# devlogMaxxing

A devlog is a blog post in the owner's voice: what he was looking for, what he
tried, what it cost, why it didn't work, and what he built instead. It reads
like a story, not a marketing page. It ranks on one keyword and is shaped so
AI answers can quote it.

The worked example is `/devlog/xreacher-alternative`:
- the page: `site/apps/web/src/landing/devlog/XreacherAlternativePage.tsx`
- its play data: `devlog/xreacherAlternative.ts`
- the shared story parts: `site/apps/web/src/landing/story/StorySections.tsx` and `story.css`
- the list of every devlog: `site/apps/web/src/landing/devlog/articles.json` (`articles.ts` reads it). The `/devlog` page, the share cards and the prerender all come from it
- the research and outline: `~/.buzz/PLANS/LOG_XREACHER_ALTERNATIVE_PAGE_OUTLINE_2026_11_09.md`

## Hard boundaries

- **the owner's story, his facts.** The story comes from what the owner said and from
  evidence: his email, the tool's own pricing page, his account's dashboard.
  Be honest: if it might work now, say so ("it probably works now, but back
  when I used it, it didn't"). Never invent a number, a quote or a result.
- **Never name the account vendors.** Show the research on what accounts cost
  ("public listings put fresh accounts at $5 to $20"), never who sells them.
- **The whop pages' rules, not new looks.** Receipts and comparisons follow
  `~/.buzz/REPOS/whop/pages/src/dataBrokering.html` (`.receipt`, `.rLine`,
  `.cmp`, `.cmpRow`). They're already ported as `Receipt` and `CompareTable`
  (`.lk-story` in `story.css`): plain type on the page, no card, Schoolbell
  lines, dashed dividers, numbers as blue sticker words. Use them. Never
  draw a card of your own.
- **Calm, not noisy.** No hand-drawn arrows. No dashed highlights in
  paragraphs (dashed links are fine). Stickers on one to three words only.
  Punch lines are muted grey.
- **Not on a devlog page:**
  - the "log runs the whole play" box (`HowItWorks`)
  - the Step 1/2/3 cards (`ThreeSteps`)
  - the phone stepper (`PlatformScroll`)
  - the "More plays to run" cards
- **Through log only** for anything sent or read on an account (rule 163).
  Research uses treg's TinyFish (free) and the BHW MCP. Nothing paid
  without the owner (rule 41).

## The page, top to bottom

1. **Hero** (blue, clouds, dither fade). The H1 holds the keyword in a story
   line ("The Xreacher alternative / I built because it didn't work."). Under
   the H1, the byline:
   - the owner's photo (`/images/mattlistening.webp`) in a small circle with a white ring
   - "By Matthew Don"
   - "Published <date>" in a `<time>` tag

   On the right: one handwritten line, one plain line, and the "Set up log" and "Read what happened" buttons.
2. **Kicker**: one handwritten question with a sticker word.
3. **The short version** (`#F3F8FF` box): four bullets. They give the cost of
   theirs, the cost of log, what happened to the owner, and the verdict line ("If
   you want to <job>, log is the <keyword> to try first.").
4. **Story sections** (`StorySection`: a title, a muted punch line, then
   paragraphs): looking for it, trying it (with the screenshot), the price,
   accounts, proxies, building our own, why it's fast, and owning your stuff.
   Put the evidence in the section where it happens:
   - `StoryImage`: a screenshot of the owner's email or dashboard, with a dated caption
   - `Receipt`: their plans, their add-ons, what we pay, speed numbers
   - `CompareTable`: them against log, row by row
5. **A call to action inside the story** (`StoryCta`), at least twice: after
   the "it didn't work" section and at the end. It shows the agent window
   typing the play and a "Set up log, it's free" button.
6. **FAQ** (`StoryFaq`): six or seven questions in the words people type
   into AI tools ("What is the best <x> alternative?", "How much does <x>
   cost?", "Is log free?"). Each is a real H3, answered under it in less than
   300 characters.
7. **The landing's marketing section** (`<Control />`, as on the home page),
   then the copy-the-prompt block (`PromptCta`), then the footer.

## Steps

1. **Find the keyword.**
   - Read the competitor's ranked keywords: `RESEARCH/LOG_COMPETITORS_SITES_*/rankedKeywords/` (`allKeywords.tsv`, `<domain>.json`). If they aren't there, get them from treg (ask the owner before a paid endpoint).
   - Fetch their own pages' titles and headings with treg `tinyfish.web.fetch` (POST, `{"urls":[...]}`, free), and note what they carry that we don't: a FAQ, a comparison table, "best for" lines, their wording.
   - Pick one main keyword ("<x> alternative") and three to five supporting ones from their relevant terms ("automate twitter messages", "best cold DM tools").
2. **Find what gets cited right now.** Ask the BHW MCP (`bhwSearch`, `bhwThread`) for threads from the last three months on AI citations, alternative pages and comparison pages. Keep only what a thread says, with its title, date and link. Write it into the outline.
3. **Collect the evidence.**
   - the owner's emails, found in Gmail through Aside by searching the tool's name, then read and dated.
   - The tool's pricing page.
   - Our own numbers, from rules, docs and RESEARCH.
   - Market prices from a TinyFish search, with no vendor named.

   Screenshot one proof, such as the signup email:
   - Close any open menu first.
   - Use the thread's own URL, not a search, so nothing is highlighted.
   - Crop it with ffmpeg into `site/apps/web/public/images/devlog/<name>.webp`.
4. **Write the outline** to `~/.buzz/PLANS/LOG_<TOPIC>_PAGE_OUTLINE_<date>.md`. It holds the keywords with their volumes, what their pages carry, the BHW list, what the page will have, and what's left.
5. **Build the page.**
   - Add the article to `devlog/articles.json`:
     - `slug`
     - `title` (the keyword and the year)
     - `headline`
     - `description`
     - `summary`
     - `published` and `publishedLabel`
     - `author`
     - `card`: `lead`, `name` (shown in capitals as a white sticker) and `pitch` (HTML, where a span with class `u` draws the dashed underline)
   - Write `devlog/<Name>Page.tsx`, starting from the Xreacher page. Export its story component and its schema (`articleSchema(article, faq)`), and read its title, description and dates from `articleOf(slug)`.
   - Register the story in `BODIES` in `devlog/prerender.tsx`.
   - Add the route `/devlog/<slug>` in `App.tsx` and a line in `public/sitemap.xml`.
   - The `/devlog` list picks the article up by itself.
6. **Make its share card.** Run `C:\Python312\python.exe site/apps/web/scripts/ogCards.py <slug>`. It fills `scripts/ogCard.html` (the member sites' card: blue gradient, hand-drawn frame, the owner's photo, the card text, the byline), renders it in Chrome at 1200×630 and writes `public/og/devlog/<slug>.png`. Look at the PNG before committing it.
7. **Rendered for crawlers and social previews.** The site build (`site/scripts/build-site.mjs`) runs `site/scripts/prerenderPages.mjs` after the web build:
   - It renders every devlog's story to HTML with React on the server.
   - It writes `dist/devlog/<slug>.html` and `dist/devlog.html`, each with its own title, description, canonical link, OG and Twitter tags (the share card as the image), the JSON-LD (`id="devlog-schema"`, so the page doesn't add it twice), and the whole article inside `#root`.
   - `vercel.json` sends `/devlog` and `/devlog/:slug` to those files before the app's catch-all.

   The platform pages (`/twitter`, `/discord`, `/slack`, `/instagram`, `/reddit`) go through the same build, from `landing/useCases/sharePages.json`. Each gets its own title, description and card: the platform's logo on a white tile with no photo, rendered by the same `ogCards.py` into `public/og/pages/<slug>.png`. They carry the tags only, and the app still renders their content. A new platform page is one entry there, plus a rewrite in `vercel.json` (the build refuses a page with no rewrite).

   Check it locally: run `npx vite build` in `site/apps/web`, then `node site/scripts/prerenderPages.mjs`, then read the title, the og tags and the text in `dist/devlog/<slug>.html`.
8. **Link it in.**
   - Link to the platform page (`/twitter` …) where the copy names the platform.
   - Link to the docs (`/docs/<tab>/<page>`, for example `getStarted/mcp`, `howItWorks/liveInbox`, `howItWorks/proxies`, `platforms/x`, `howItWorks/specs/voiceGate`) where the copy names how log does it.
   - Check that every docs link answers 200 on log.listeningkit.com.
9. **Check it.**
   - Run `npx tsc --noEmit --skipLibCheck` in `site/apps/web`.
   - Open it on the local dev server in Aside at 1440 and 390 wide, with nothing scrolling sideways.
   - Read the title and the JSON-LD types from the page.
10. **Ship it.** Commit as the owner (`GIT_CONFIG_COUNT=0`) with the day's log entry (rule 5), push, and add it to the PR or open one (`gh pr create`).

## Done when

- The page is live at `/devlog/<slug>`.
- The keyword is in the title, the H1, the short version, the FAQ and the copy.
- Every number has its source in the outline.
- The byline shows the owner's photo and the date.
- The page is on `/devlog`.
- Its share card is in `public/og/devlog/`.
- The prerendered HTML carries its own tags and the full text.
- The FAQ and the article schema load.
- It reads cleanly at desktop and phone widths.
- The outline lists what's left, above all getting named on the "best <x> alternatives" pages that AI answers already cite. That is the citation tracker's job.
