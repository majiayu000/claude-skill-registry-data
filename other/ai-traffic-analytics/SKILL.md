---
name: ai-traffic-analytics
description: Measure what AI search really sends the business (visits, signups, revenue) with free tools. Use for "how much traffic do we get from ChatGPT", "track AI referrals in GA4" or "report on our AEO and GEO work". Sets up GA4, Search Console, Bing AI Performance and log tracking, accounts for dark AI traffic, and produces a monthly report.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/ai-traffic-analytics
---

# AI traffic analytics

Set up honest measurement of what AI search sends the business: visits, signups and revenue from ChatGPT, Gemini, Copilot, Perplexity, Claude and Google's AI features, using free tools only. You hand back a checked tracking setup (GA4 channel plus a fallback, reports by landing page and key event, a "how did you hear about us" question), the impression and citation data Google and Bing provide, a log-based leading indicator, and a monthly report that states its own limits.

> **Romeo's rule:** Report the small number accurately, because a dashboard that flatters AI traffic will eventually be used to make an expensive decision.

## Use this when

- Someone asks "how much traffic or revenue do we get from ChatGPT?" and nobody can answer.
- GA4 shows chatgpt.com under Referral or Unassigned and the totals don't agree with each other.
- AEO or GEO work is under way (`ai-search-visibility`) and you need to show what it did beyond citations.
- Leadership wants a monthly AI search report.
- Sales keep hearing "I found you on ChatGPT" but analytics shows almost nothing.

## Don't use this for

- Mention and citation rates per prompt and engine → `ai-search-visibility`, or `dataforseo-ai-tracker` at scale.
- What AI Overviews and AI Mode are doing to Google clicks, page by page, and whether to opt out → `google-ai-overviews-audit`.
- Allowing, blocking or verifying AI crawlers in robots.txt and the CDN → `ai-agent-readiness`.
- A general drop in Search Console clicks → `seo-performance-audit`.

## What you need

### Required
- Analytics access: GA4 Viewer to read reports, Editor to create a channel group (or the same in Plausible, Matomo or similar).
- The site's key events (signup, demo request, purchase) and a rough value for each.
- Search Console access for the site.

### Helpful
- Bing Webmaster Tools with the site verified.
- 30 to 90 days of server, CDN or host logs with timestamp, IP, user agent, URL and status code.
- CRM or signup data that can hold a "how did you hear about us" answer.
- Sales call notes and support tickets.
- Any earlier AI referral numbers, and the date each tracking change was made.

### No tools?
GA4, Search Console and Bing Webmaster Tools are free, and so is a signup-form question. Without GA4, any analytics tool that reports referrer domains works: filter by the AI domains in step 2. Without logs, ask the host for a raw access log export; most shared hosts and CDNs provide one. With nothing at all, start the "how did you hear about us" question today and spot-check a few prompts by hand (`ai-search-visibility`); that is a floor, not a measurement.

## Ground rules

- AI referrals are small. 2026 studies put them at roughly 0.3-1% of site traffic, with ChatGPT sending about three quarters (SE Ranking and Conductor, vendor data). A result far outside that range is possible, but check the setup before anyone celebrates.
- Analytics shows a floor. Apps and in-app browsers strip referrers, people copy a URL or search the brand name later. Say so beside every number.
- Clicks from Google's AI Overviews and AI Mode are Organic Search in GA4 and part of Web in Search Console. They can't be split out, and they never go into GA4's AI Assistant channel or your own AI referral totals.
- Report by landing page and key event. Forty AI visits that produce six demo requests matter more than four thousand sessions that bounce.
- No causal claims. "Citations rose and signups rose" is a pattern; "the AEO work drove signups" needs a controlled test.
- Crawler and fetcher hits are not visits. They live in logs, not GA4, and never get added to traffic.
- Keep definitions fixed. Changing a regex, channel or key event mid-year breaks the trend; write down each change with its date.
- Small numbers swing. Under about 100 AI sessions a month, report counts and 3-month rolling totals, not percentage changes.

## Steps

1. **Check GA4's built-in AI channel.** Since 13 May 2026 GA4 sets medium `ai-assistant` and campaign `(ai-assistant)` on sessions whose referrer matches Google's list of AI assistants, and groups them in an "AI Assistant" channel in the default channel group. Google names ChatGPT, Gemini, DeepSeek, Copilot and Grok as examples but doesn't publish the full list. Check Google's Default channel group help page for the current name and rules.
   - Reports → Acquisition → Traffic acquisition, dimension Session default channel group: is "AI Assistant" listed? Then switch to Session source / medium and search for chatgpt.com, perplexity, gemini.google.com, copilot, claude.ai, deepseek, grok.com, meta.ai and mistral.
   - Any AI source still under Referral, Organic Social or Unassigned (for example `chatgpt.com / (not set)` from a tagged link with no referrer) is a gap. Note the sessions involved; step 2 catches them.
   - Default channel rules can't be edited, and the medium is set as data is processed, so expect sessions from before mid-May 2026 to stay in Referral. Check your data around that date.
   - Google's definitions put AI Overviews and AI Mode in Organic Search. Don't look for them here.

2. **Add a custom channel group as the fallback.** It gives one consistent definition before and after May 2026 and catches what the default list misses. Admin → Data display → Channel groups → Create new channel group, starting from a copy of the default.
   - Add a channel named "AI referrals (custom)", so nobody mistakes it for GA4's built-in "AI Assistant" channel, with the condition Session source matches regex: `.*(chatgpt|openai|perplexity|gemini\.google|copilot|claude\.ai|deepseek|grok\.com|meta\.ai|mistral\.ai).*`
   - Move it above Referral, Organic Social and Unassigned; Google's own help page gives the same instruction for this channel.
   - Custom channel groups apply to past data, so the trend runs back before May 2026. Standard properties get two custom groups; Editor role or above is needed.
   - Avoid patterns that match "ai" anywhere: they swallow mail, email and any other source containing those letters. Test it: Explore → free-form, rows Session source, filter by the new channel, and read every source it catches. Remove false positives and add new assistants as they appear.

3. **Keep ChatGPT's tag intact.** ChatGPT adds `utm_source=chatgpt.com` to the links it shows, which is how app visits with no referrer still get attributed.
   - Request a few URLs that redirect (old slugs, `http://`, the other host variant) with `?utm_source=chatgpt.com` appended and confirm the final URL still carries it. Redirects or middleware that drop query strings before analytics loads lose the attribution: `Fix next`.
   - Canonical tags can keep pointing at the clean URL; that doesn't affect tracking.
   - Never put UTM tags on internal links. GA4 then credits later key events to your own tag instead of the AI source.
   - Look for other `utm_source` values from AI products in the landing-page report and add them to the regex if they appear.

4. **Report by landing page and key event.** Build one Exploration and save it.
   - Free-form; rows Landing page + query string, then Session source; columns Month; values Sessions, Engaged sessions, Key events (each event separately), Session key event rate, Total revenue; filter the AI referrals (custom) channel from step 2.
   - Add a user view: User acquisition report, First user source, for people whose first visit came from an AI source and who converted later through another channel. Report session-based and first-user counts side by side, labelled.
   - The attribution reports in GA4's Advertising section show paths where an AI source was an earlier touch. Use them for context, not as proof.
   - Compare each landing page's AI key event rate with its Organic Search rate. Don't assume AI visitors convert better; measure it.
   - Dozens of AI sessions with near-zero engagement time usually mean bots, prefetching or a regex false positive. Exclude them and note it.

5. **Add Google's impressions.** Search Console → Generative AI performance report. The Search view covers AI Overviews and AI Mode; a separate Discover view covers Discover's generative features. Impressions only, by page, country, device and date: no clicks, no queries.
   - Export monthly and trend AI impressions for the pages that matter. Their clicks are already inside Search Console's Web clicks and GA4's Organic Search.
   - No report usually means too few impressions or a property excluded under Settings → Search generative AI. Say which.
   - Page-level diagnosis and the opt-out question → `google-ai-overviews-audit`.

6. **Add Bing's citations.** Bing Webmaster Tools → AI Performance (public preview since 10 February 2026) covers Microsoft Copilot, AI summaries in Bing and some partner experiences.
   - Read: total citations, average cited pages per day, page-level citations, and grounding queries (a sample of generalised phrases the AI searched with, not users' exact prompts). Since June 2026 the preview adds intents, topics, citation share per grounding query (your citations ÷ all citations shown for it) and a period compare.
   - No clicks, no competitor names, and history only for the dashboard's preset ranges. Export every month (CSV or Excel) and keep the files; that is your trend.
   - Grounding queries are good prompt research material → `ai-prompt-research`.

7. **Use server logs as a leading indicator.** AI systems fetch pages before they cite them, and logs see engines that send no referrer.
   - Split hits by purpose. Search indexing: OAI-SearchBot, Claude-SearchBot, PerplexityBot, bingbot, Googlebot. User-triggered fetches: ChatGPT-User, Claude-User, Perplexity-User. Training: GPTBot, ClaudeBot and similar. Vendors rename and add bots, so check each vendor's crawler page before relying on this list.
   - User-triggered fetches are the closest signal to "someone asked an AI about this page". Count them per page per month.
   - Verify before counting. Match IPs against the ranges vendors publish (OpenAI publishes one list per bot; Google and Bing publish crawler IP lists and support reverse DNS lookups). Hits that only claim a user agent go in a separate "unverified" bucket; user-agent strings are trivial to fake.
   - Googlebot hits can't be split between classic Search and AI features. Report them, don't interpret them as AI.
   - 403, 429 or challenge pages served to verified AI bots are an access problem → `ai-agent-readiness`.
   - One answer can trigger several fetches, or none if the engine uses its cache. Trend fetches; never convert them into visits.

8. **Catch dark AI traffic.** Much AI influence never shows as a referral.
   - Add one question to signup, demo or checkout: "How did you hear about us?" with options including ChatGPT, Google (search), Google AI Overview or AI Mode, Gemini, Perplexity, Copilot, Claude, Other AI assistant, alongside search, social, a friend or colleague, podcast or newsletter, and Other with a text box. Optional is fine; keep the AI options in the middle of the list, not first. Adding the field is a site change: draft it, get approval.
   - Store the answer with the customer record and report counts and share of new customers monthly. Self-reports undercount some channels and overcount others; show them next to GA4 as a range.
   - Branded search: Search Console queries containing the brand name, monthly impressions and clicks, year over year. Branded demand rising along with AI citations is a supporting signal (`inferred`), not proof.
   - Direct sessions landing on deep pages (not the homepage) can include copy-pasted AI links. Trend them, low confidence.
   - Ask sales and support to tag any conversation where the prospect mentions ChatGPT or "AI" and quote two or three examples a month.

9. **Write the monthly report.** Same structure every month, using the template below.
   - Lead with outcomes (key events, revenue), then visits, then visibility (impressions, citations, fetches).
   - Show AI as a share of all sessions and all key events, with the 0.3-1% benchmark as context.
   - Use 3-month rolling totals for small numbers; add year over year once there is a year of data.
   - Name the floor in one line: "Analytics captured N; self-reports say M; the real number is likely higher."
   - List every tracking change made that month, with its date.
   - No causal claims. "After the pricing page update, AI-referred demo requests rose from 3 to 7" is fine; "the update caused it" isn't.

## What to hand back

Hand back the setup checks with priority labels, then the filled-in monthly report. Every fix carries a priority label and an evidence label with confidence.

```markdown
# AI search report: [site], [month year]

**What I found:** [one line, e.g. "The AI referrals (custom) channel had 412 sessions (0.7% of traffic) and 9 signups (2.1% of signups); ChatGPT sent 78% of the sessions."]
**What matters most:** [one line]
**What to do first:** [one line]

## Outcomes
- Key events from AI referrals (custom): [n] ([x]% of all) - by event: [event n, ...] - revenue: [amount]
- Self-reported "heard about us via AI": [n] of [n] answers ([x]%) - by tool: [ChatGPT n, Google AI n, ...]
- Sales and support mentions: [n] - example: "[quote]"

## Visits
- AI sessions: [n] ([x]% of all); 3-month rolling: [n]; same month last year: [n or "no data"]
- By source: chatgpt.com [n] | perplexity [n] | gemini.google.com [n] | copilot [n] | claude.ai [n] | other [n]
- Top landing pages: [URL] - sessions [n] - key events [n] - key event rate [x]% (Organic Search rate [x]%)

## Visibility (no clicks in any of these)
- Google generative AI impressions: Search [n], Discover [n]; top pages: [URLs]
- Bing AI Performance: citations [n]; average cited pages [n]; top grounding queries: [list]; citation share on [query]: [x]%
- Logs, verified only: user-triggered fetches [n] (ChatGPT-User [n], Claude-User [n], Perplexity-User [n]); most-fetched pages: [URLs]; blocked or challenged: [n]

## Supporting signals
- Branded search: impressions [n] ([x]% year over year), clicks [n]

## Caveats and tracking changes
- Analytics captured [n]; self-reports say [n]; the real number is likely higher.
- AI Overview and AI Mode clicks are inside Organic Search, not in the numbers above.
- Changes this month: [what changed, date]

## Fixes, in order
1. [Fix now | Fix next | Worth doing] [what to change] - why: [reason] - evidence: [seen | tool | inferred], [high | medium | low]

## What I could not check
- [data source or page not checked, and what would verify it]
```

## Stop and flag if

- Key events aren't set up, or a consent setup leaves most visitors untracked: say the report shows a fraction of reality and fix tracking before reporting trends.
- The AI share is far above the 0.3-1% range (say 5%+): check the regex for false positives, bot sessions and self-referrals before reporting it.
- You're asked to create channel groups, change forms, redirects or tracking code: draft the change and get permission for that specific change.
- Logs contain IP addresses and other personal data: aggregate them and keep raw lines out of the report.
- Someone wants AI Overview clicks estimated and added to AI totals, or wants causal claims in a board deck: decline and explain why.
- Unacceptable output: unverified bot hits counted as visits, percentage changes on single-digit numbers, AI Overview clicks inside AI referral totals, or a single total with no floor caveat.

## Next step

- `ai-search-visibility` to link the visits to the prompts and citations behind them, using the top AI landing pages as the pages to check.
- `google-ai-overviews-audit` for pages where Google AI impressions rose while clicks fell.
- `ai-prompt-research` with Bing grounding queries and the self-reported answers as input.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
