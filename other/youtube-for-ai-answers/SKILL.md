---
name: youtube-for-ai-answers
description: Make YouTube videos that Perplexity, Google AI Overviews and AI Mode cite. Use for "get our videos into AI answers", "should we make YouTube videos for AI search" or the video side of an AEO, GEO or LLM SEO plan. Picks the prompts where video helps, then fixes titles, descriptions, chapters, captions and site embeds with VideoObject markup.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/youtube-for-ai-answers
---

# YouTube videos AI engines cite

Find the buyer prompts where AI engines cite YouTube and whose videos they pick, choose the questions where a video genuinely answers better than text, and plan, package and embed videos so engines can find, read and cite them. You hand back a video opportunity list by prompt and engine, a packaging spec per video (title, description, chapters, captions), an embed and markup plan for the site, a list of independent creators to approach with the disclosure rules, and a measurement plan using the same prompt set.

> **Romeo's rule:** Assume the engine reads your video rather than watches it, so the transcript, title and description are the parts it can actually quote.

## Use this when

- The citation-source map from `ai-search-visibility` shows youtube.com cited for money or how-to prompts, especially on Perplexity or in Google AI Overviews and AI Mode.
- Competitors' or independent creators' videos are cited for your prompts and yours aren't, or the brand has no channel.
- The product is easier to show than describe: setup, walkthroughs, side-by-side comparisons, physical products, troubleshooting.
- The brand already has videos that never get cited: vague titles, no chapters, uncorrected auto-captions, not embedded anywhere useful.
- You're planning creator reviews and want them to be honest, disclosed and useful to engines.

## Don't use this for

- Building the prompt set, running the baseline and the full source map → `ai-search-visibility`.
- Cutting pages into Shorts, posts and clips for owned social accounts → `page-to-social-posts`.
- Choosing which third-party platforms deserve effort overall → `parasite-seo-plan`.
- Writing and validating the JSON-LD itself → `schema-markup`.

## What you need

### Required

- Prompt runs with cited URLs and engine names: at least the money and how-to prompts, 2 or 3 runs each on the engines the audience uses.
- Brand, product, audience, country and language.
- The channel URL and YouTube Studio access, or a list of existing video URLs; or confirmation that there's no channel yet.
- The site pages each video should support, by URL.
- A real person who can present or narrate, and real product footage. Without either, stop at step 2.

### Helpful

- YouTube Studio analytics: traffic sources (including external sites), YouTube search terms, audience retention.
- Search Console: the Video indexing report and video appearances in the Performance report.
- Existing scripts, transcripts, sales demos and support recordings worth turning into answers.
- Creator contacts, an affiliate programme if one exists, and any past sponsorship terms.

### No tools?

Run the prompts by hand in a private or logged-out window and open every cited YouTube link. For each, note the channel, length, upload date, title, whether the description has chapter timestamps, and whether captions are manual or "auto-generated" (shown in the captions menu). Search YouTube and Google's Videos tab for the same questions. Check your own pages with view-source and the Rich Results Test, and use the free Video indexing report in Search Console.

## Ground rules

- Make videos where YouTube is already cited. Across 100M+ citations, Otterly (March 2026, vendor data) found Perplexity and Google AI Overviews cite YouTube most, and Gemini and Copilot rarely. Your own runs decide: no YouTube citations for a prompt group means no video project for it.
- Long-form, not Shorts. Long-form videos were about 94% of YouTube citations in the same Otterly study. Shorts can feed discovery on YouTube, but they're rarely the source an engine links.
- Video only where it helps the viewer: steps you need to see, UI walkthroughs, physical tasks, side-by-side tests, troubleshooting. Definitions, pricing and simple lists belong on a text page.
- Put the answer in words. Title, description, chapters and captions are what retrieval systems can read reliably (`inferred` for most engines); Google uses YouTube description timestamps for key moments.
- Captions must be right. Auto-captions mangle product names, numbers and competitor names, and an engine quoting a wrong transcript line is quoting you.
- Real people, real footage, made one at a time. YouTube's monetisation policy (renamed "inauthentic content" in July 2025) excludes mass-produced or repetitive content, including AI-generated videos built from generic templates, and realistic altered or synthetic content must be disclosed. Templated video runs are also spam under Google's policies if they exist to manipulate rankings or AI answers.
- Independent reviews do work your own channel can't: for "best X" and "is X worth it" prompts, engines lean on third-party opinions. Free product, payment or commission is a material connection: under FTC guidance the disclosure goes in the video itself, not just the description, and YouTube's paid promotion setting must be ticked. Never script the verdict.
- Description links are redirected and pass no link value. Success is the video being cited, referral visits and branded search, never links.
- Your page must stand without the video. Google indexes a video only on a watch page, where the video is the main reason for the visit; a video supporting an article is fine there but earns no video features.
- Measure with the same prompt set as rates over repeated runs. One citation in one run is an anecdote.

## Steps

1. **Find where YouTube is cited and whose videos win.** Filter the prompt runs to cited `youtube.com`, `m.youtube.com` and `youtu.be` URLs.
   - Normalise: map `youtu.be/ID` and `/shorts/ID` to the video ID; strip `si=` and tracking parameters. Keep any `t=` value in its own column: it shows which moment the engine pointed to, and that moment deserves its own chapter.
   - Per prompt and engine: YouTube citation rate (runs citing any YouTube video ÷ runs), plus each cited video's channel, owner type (brand, competitor, independent creator, media), length, upload date, title, chapters present, caption type, and whether the description states the answer.
   - Check Google's Videos tab and video results for the same queries; videos that rank there are often the ones AI Overviews pick (`inferred`).
2. **Pick the questions worth a video.** For each prompt group with YouTube citations, answer four questions:
   - Is YouTube cited on an engine this audience uses? Is video genuinely the better format? Can the brand show real footage and real expertise? Are the cited videos beatable: old UI, wrong version, auto-captions, no chapters, no clear answer?
   - Four yeses → `Fix next`. An existing brand video that engines cite with outdated prices or UI → `Fix now`. Video cited but text answers better → `Worth doing` at most. No YouTube citations → `Leave it`.
   - Formats that tend to fit: "how to [job] in [product]", "[product] setup walkthrough", "[A] vs [B] side by side", "[product] review after [n] months of use", "fix [error]", "best [category] for [segment], tested".
   - Pick 3 to 8 videos for the first batch. Fewer, better videos beat a weekly quota.
3. **Plan each video as long-form.**
   - Say the answer or verdict in the first 30 seconds, on camera and in words, then show the proof.
   - One question per video, or chapters that each answer one sub-question; the sub-questions behind a money prompt (→ `query-fan-out-coverage`) make good chapters.
   - Real, current footage with the product version and recording date visible or stated. A named presenter with their role.
   - Say product names, prices, versions and numbers clearly; it's what the captions will carry.
   - Length is whatever the job takes. Cut intros, recaps and filler; never stretch to a target.
   - Shorts only as cut-downs that point to the long video, never as the planned citation target.
4. **Write a title and description that answer in text.**
   - Title (YouTube allows 100 characters; front-load the first 60 or so): the task or question in the buyer's words plus the specific product, version or year. "How to set up two-way calendar sync in Acme (2026 walkthrough)", not "Acme tips #12".
   - Description, first two or three lines: the answer in one or two sentences naming the product and who it's for. Then the key facts (prices and versions with dates), the chapter list, a link to the matching page, sources, and any sponsorship disclosure.
   - Tags matter little: YouTube says title, thumbnail and description matter more, and that excessive tags in a description break its spam policy. No keyword lists.
   - Thumbnail and title must match what the video delivers; misleading ones count as clickbait under YouTube's policies.
5. **Add chapters.** Put timestamps in the description: the first must be `00:00`, there must be at least three in ascending order, and each chapter must be at least 10 seconds long. Write chapter titles as the sub-questions ("03:12 How much does it cost?"). Manual timestamps override YouTube's automatic chapters, and Google can show them as key moments.
6. **Fix captions and the transcript.**
   - Upload a corrected caption file (SRT or VTT) or edit the auto-captions in YouTube Studio → Subtitles; check every product name, number, competitor and technical term.
   - Set the video's language correctly. Add other languages only with reviewed translations for markets you serve.
   - Keep a cleaned, readable transcript (edited for reading, not a raw dump) for the site page.
7. **Get independent creator reviews, honestly.**
   - Start with creators already cited or ranking for your prompts (step 1), then those whose audience matches the segment.
   - Offer product access and facts. The creator keeps editorial control; negative findings stay in. Offer a factual check only (correcting a wrong price), never approval of the verdict.
   - Disclosure: spoken and on screen early in the video, in the description, and with YouTube's paid promotion setting. FTC guidance applies to posts that foreseeably reach US consumers; other markets have their own rules (check local law).
   - Never buy views, likes, comments or subscribers. YouTube's fake engagement policy bans anything that artificially inflates metrics.
8. **Embed each video on its matching page.**
   - One page per video: the page that answers the same question. Place the embed beside the section it supports, with a short text summary of the answer and the steps, plus key points or the cleaned transcript, so the page answers fully without playing anything.
   - Use a standard YouTube `<iframe>` embed. Google finds videos in `<video>`, `<embed>`, `<iframe>` or `<object>` elements; a click-to-load facade that hides the player until clicked can trigger "Cannot determine video position and size" in the Video indexing report. If page speed forces a facade, accept that Google may not index the video for that page.
   - Add `VideoObject` JSON-LD that matches what's visible: required `name`, `thumbnailUrl`, `uploadDate` (ISO 8601 with time zone); recommended `description`, `duration` (ISO 8601, e.g. `PT8M30S`), `embedUrl`, and `contentUrl` if you host the file. Validate with the Rich Results Test (→ `schema-markup`).
   - Check Google's current video indexing requirements: the page is indexed, the video has a valid thumbnail at a stable URL, and the page is a watch page whose main purpose is that one video. A supporting video on an article will show "Video isn't on a watch page"; that's expected, not a defect.
   - For the 1 to 3 most important videos, consider a dedicated watch page: video at the top, a unique title and description, the summary and transcript below, and links to the related article.
9. **Run the channel like a publisher.** A real About section, the same brand name and one-line description used everywhere else, links to the site, consistent upload pacing you can sustain. AI tools can help with scripts, edits and thumbnails; YouTube doesn't require disclosure for that, but realistic synthetic people, voices or events must be disclosed, and no reuploads or stitched clips of other people's work.
10. **Measure with the prompt set.** Monthly, same prompts, same engines, 2 to 3 runs each:
    - YouTube citation rate per prompt group and engine, whose videos are cited, and whether the brand's videos or creator reviews are among them.
    - YouTube Studio: views from external sources and YouTube search terms; Search Console: video appearances and Video indexing report status; site analytics: AI referrals to the pages with embeds.
    - Call a video "cited" only when it appears in two or more monthly runs. Refresh a video when the UI or prices it shows change; old footage gets quoted as current.

## Run it with DataForSEO (optional)

Replaces the manual search for YouTube-cited prompts in step 1 with database results. Connect through the official MCP server (`dataforseo-mcp-server`, calling endpoints through its `api_request` tool) or plain HTTPS with Basic auth.

- **Answers that cite YouTube for a category:** `/v3/ai_optimization/llm_mentions/search_mentions/live`.
  - Two target entities: `target: [{"domain": "youtube.com", "search_filter": "include", "search_scope": ["sources"], "include_subdomains": true}, {"keyword": "project management software", "search_filter": "include", "search_scope": ["question"], "match_type": "partial_match"}]`.
  - Also send `platform` (`google` for AI Overviews, or `chat_gpt`), `location_code: 2840`, `language_code: "en"`, `limit: 40`.
  - Read `question`, `ai_search_volume`, `platform`, `last_response_at` and `sources[]` (`url`, `title`, `domain`, `publication_date`). Keep the YouTube sources to see which videos and channels win each question.
  - The docs don't show this exact two-entity combination, so test it on the sandbox and with a small `limit` first. `youtu.be` is a separate domain; add a second domain entity if short links show up.
- **Limits:** LLM Mentions covers only Google AI Overviews and ChatGPT (US, English), from a pre-collected database with monthly history since August 2025.
  - Perplexity, one of the two engines that cite YouTube most, isn't in it. Run Perplexity by hand, or through `/v3/ai_optimization/perplexity/llm_responses/live`, whose API answers can differ from the app.
  - Database results show the category's pattern; the user's own prompt runs still decide which videos to make.
- **Example cost at published prices** ($0.10 per task + $0.001 per row): 6 category keywords × 2 platforms × `limit: 40` = 12 calls × $0.14 ≈ $1.68.
- **Guardrails:**
  - Estimate the cost and get the user's OK before any paid call; default cap $2 per run.
  - Check `money.balance` with the free `GET /v3/appendix/user_data` first.
  - Always set `limit`; cache results for 30 days; sample live engines at least 3 times per prompt.
  - Test new code on `https://sandbox.dataforseo.com/v3/` first. Never print or save the API password.

## What to hand back

Fill in this template. Every action gets a priority label and an evidence label with confidence.

```markdown
# YouTube for AI answers: [brand], [date]

**What I found:** [one line, e.g. "Perplexity cites YouTube in 11 of 18 how-to runs; all cited videos are creators' 2024 reviews."]
**What matters most:** [one line]
**What to do first:** [one line]

## Method
- Prompts: [N] ([groups]); engines: [list]; runs per prompt: [n]; dates: [x]; country/language: [x]

## Where YouTube is cited
| Prompt group | Engine | YouTube citation rate | Cited videos (channel, length, date) | Ours? |
|---|---|---|---|---|

## Videos to make or fix, in order
1. [Fix now | Fix next | Worth doing] [question] - format: [walkthrough / vs / review]; why video: [reason]; incumbent: [video and its weakness] - evidence: [seen | tool | inferred], [high | medium | low]

## Packaging spec per video
- Title: [text]; first description lines: [text]; chapters: [00:00 ...]; captions: [manual file / corrected auto]; matching page: [URL]

## Embed and markup plan
- [page URL]: embed position, summary/transcript, VideoObject fields, watch page or supporting video

## Creator reviews
- [creator, channel, why]: offer [terms]; disclosure: in video + description + paid promotion setting

## Leave it
- [prompt group or format, and why]

## Re-measure plan
- Next run [date]; success = [metric change]

## What I could not check
- [engine, video or data not checked, and what would verify it]
```

## Stop and flag if

- The plan calls for mass-produced, templated or fully AI-generated videos, reuploads of other people's content, or bought views, likes, comments or subscribers.
- A creator deal requires approval of the verdict, hides payment or free product, or skips YouTube's paid promotion setting.
- Nobody can appear on camera or narrate, and there's no real product footage. Say video isn't the right channel yet.
- The videos would give health, financial, legal or safety advice. Get expert review before publishing.
- Fewer than 10 prompts or one run each: present the opportunity list as provisional.
- Unacceptable output: invented view counts, citation rates or video details, chapter lists for videos you haven't seen, or markup that describes content not on the page.

## Next step

- Run `schema-markup` with the VideoObject plan and the pages that will carry each embed.
- Run `query-fan-out-coverage` on the chosen money prompts to turn sub-questions into chapters and page sections.
- Re-run `ai-search-visibility` monthly with the same prompt set to measure the change.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
