---
name: tubelab-mcp
description: Use when a TubeLab tool call fails or returns nothing, when unsure which search tool or filter to use, or when the user asks how TubeLab tools, credits or the REST API work. Holds the costs, rules and quirks every workflow skill assumes.
license: MIT
metadata:
  author: tubelab
  version: "3.1"
  kind: data-layer
---

# TubeLab MCP: the data layer

TubeLab is a read-only index of public YouTube data. It holds breakout channels, outlier videos and trending title formulas, refreshed daily, plus live reads of channels, videos, transcripts and comments. This skill is not a workflow. It holds what we learned by running the workflow skills: costs, craft rules and quirks. Open it when a tool call fails or returns nothing, or when you are unsure which tool or filter to use.

The full parameter and REST reference is not repeated here. See "Full reference" at the end.

## Connect and check

- The MCP endpoint is `https://public-api.tubelab.net/mcp`. Most clients connect with OAuth. Cursor and other IDE agents send an API key as `Authorization: Bearer <key>`, which needs a Pro or Team plan. Setup for each client: https://tubelab.net/docs/api/mcp-server
- When unsure, call `get_credits_balance` first. It is free.
- The MCP is included from the Starter plan. Monetization, revenue, RPM and audience fields can be empty on Starter accounts. Plans: https://tubelab.net/pricing

## Tool map

The MCP tool names differ from the REST paths, and the tool schemas do not show costs.

| Tool | Cost | Use it for |
|---|---|---|
| `search_channels` | 5 credits | Channels by topic, with many filters. The niche-finding tool. |
| `search_related_channels` | 5 credits | Channels similar to one or more channel IDs. Competitor sets. |
| `search_outliers` | 2 credits | Videos that beat their own channel's average. What is working now. |
| `search_related_outliers` | 2 credits | Outliers similar to a title, a video, a thumbnail (`thumbnailVideoId`, by image) or a channel's videos (`relatedChannelId`). |
| `search_trending_formats` | 1 credit | Title formulas with usage stats and example videos. English only. Pass no `language`. |
| `get_channel`, `get_channel_videos` | free | The same payload: channel stats plus up to 120 long-form videos, newest first, with outlier flags. One call is enough. |
| `get_channel_shorts` | free | A sample of Shorts with outlier flags. |
| `get_video` | free | Title, description, tags, publish date, views, likes and comment count. |
| `get_video_transcript` | free | Transcript text plus timed `events[]`. |
| `get_video_comments` | free | Up to 100 top comments. |
| `get_credits_balance` | free | Remaining credits. |

Each call costs the same whatever its `size`. Repeating an identical request within a short window is not charged again. Changing one filter is a new charge.

## What only TubeLab returns

Use this when a user asks to run a skill without TubeLab. Say what is lost before you start. Claim no more than this table: channel, video and comment reads can be done with other tools.

| What TubeLab returns | What plain YouTube gives instead | What the alternative costs |
|---|---|---|
| Outlier videos across the whole index in one search, each with its ratio to the channel's average and a z-score | A search ranked by relevance, views or date. No baseline per channel. | Reading each channel's video list to work out its average: several calls per channel, hundreds for one page of results. You can only test channels you already found. |
| Breakouts on small or new channels: outliers filtered by the channel's subscribers, average views, views per subscriber and video count | No filter by channel size. Big channels fill the results. | The same reads, then most results are thrown away. |
| Outlier search by meaning or exact words, by title pattern with wildcards, and by exact length | Keyword search and three fixed length buckets | No way to ask for titles shaped like "Why * Failed". |
| Channel search by creation date, subscribers, average and median views, views per subscriber, steadiness of views, views per hour and video count | Channel search by keyword only | One read per candidate, and no way to ask for channels created this year that beat their size. |
| Audience estimates per channel: age band, gender, income tier and region | Not public. Only the channel's owner sees them. | Cannot be rebuilt. The only route is asking each creator. |
| Monetization per channel: ads on or off, the date that changed, detected income methods (sponsors, affiliate links, products, courses, newsletter, community, services, donations), revenue and RPM bands | Not public | Income methods mean opening each channel's descriptions by hand. Ad status, lost-ads dates and RPM cannot be rebuilt. |
| Classification per channel: Content Authenticity, made with AI, faceless, on camera, made for kids | Only a made-for-kids flag | Judging every channel by eye. |
| Terminated channels, searchable | A terminated channel returns nothing. | Cannot be rebuilt after the fact. |
| Similar channels by content, and the outliers of those channels. A terminated channel can be the seed. | The related-videos endpoint was removed in 2023. There was never one for channels. | Guessing neighbours from keyword searches. |
| Trending title formulas: the template with its slots, example videos, video count, average ratio and click triggers, filtered by growth | Nothing | Collecting thousands of titles and grouping them by hand, with no growth history. |
| Volume | The Data API's default quota is 10,000 units a day and a search costs 100, so about 100 searches a day. | A deep niche sample does not fit in a day. |

What stays replaceable: reads of a channel, a video and its comments. Transcripts need the video owner's permission on the official API. The TubeLab channel read still adds each video's ratio, z-score and outlier flag.

## Identifiers and links

- Channel tools accept a channel ID (`UC...`), a URL or a handle (`@name`). Prefer the ID when a search hit already gave it.
- Video tools need the bare 11-character video ID. Take it from `watch?v=ID`, `youtu.be/ID`, `shorts/ID` or `embed/ID`, and strip `&t=` and other parameters.
- Search hits carry `id` (the video) and `snippet.channelId`. Use those. Never guess an ID.
- Build report links only from tool data. Video: `https://www.youtube.com/watch?v=<id>`. Moment: the same plus `&t=<seconds>s`, where seconds are `startMs` divided by 1000. Channel: `https://www.youtube.com/@<handle>`, or `https://www.youtube.com/channel/<channelId>` when there is no handle. Brands, products and offers: the URL as read in a description, or the video moment where they were only heard.

## Craft rules

1. **Broad, then narrow.** Start with one wide search and read what comes back. Then add filters. Six filters on the first call often return nothing, and they cost the same.
2. **Recency first.** Always set `publishedAtFrom` with a token: `month`, `trimester`, `semester` or `year`, never a date. If results are thin, widen one step at a time and say so in the report. A lookup by handle is the exception: pass only the handle as `query`.
3. **Content Authenticity stays on.** `classificationQuality: "neutral"` means General and above, because the server includes `positive`. Use `neutral` for niche, outlier, idea and title work. Use `positive` (High) for anything about thumbnails. Never drop it to widen a thin result. Widen recency or remove another filter instead. `negative` is only for auditing low-effort content. `niche-watchlist`, `audit-channel-risk` and `reverse-engineer-niche` are the exceptions: the watchlist's saved search, the audit's similar channel searches and reverse-engineer-niche's two risk searches leave the filter out.
4. **Ratio over raw views.** `averageViewsRatio` is views divided by the channel's average. It and `zScore` say whether a format worked. Raw views only say the channel is big. Rank by ratio, show both, and keep the channel's subscriber count next to every ratio.
5. **Semantic by default.** `by: "semantic"` understands topics. `by: "lexical"` matches exact words. `query` takes 1 to 3 phrasings of one topic, not a list of topics.
6. **Stable paging.** Page with `from`, a 0-based result offset, so page 2 is `from: size`. Keep the same `seed` and filters on every page of one search. With no `sortBy`, results come in seeded-random order, which is what the app shows on first load. Each page is a new charge. Two pages is the ceiling unless the user asks or the skill says so. `niche-finder` pages its two channel searches 3 to 4 pages deep.
7. **Exclude low-effort niches.** Pair the quality floor with `excludeNiche` on channel searches or `excludeKeyword` on outlier searches. Start from this list, drop what belongs to the user's niche, and add the user's own: `music, song, lofi, movies, trailer, compilation, kids, nursery, news, politics, lingerie, haul, asmr, reaction, live stream`.
8. **Estimates are estimates.** Revenue, RPM and audience fields are model outputs. Use them to order results and show them as bands. Never quote them as facts, and do not filter on them unless asked.
9. **Thin signal.** Fewer than 5 hits is not a trend. Say so and widen once. If it is still thin, report "no signal" instead of inventing one.
10. **Proof line.** Every claim about a channel or video carries channel (handle) · video title verbatim · views · ratio · publish date. Link everything you cite, with a URL from tool data. A sponsor that was only heard links to its video moment. Label estimates. If you did not fetch it, you do not know it.

## Reading results

- **What to trust on a channel hit.** Cluster channels on `semantic.niches[]`. Median views show demand; the average is pulled up by outliers. A views-to-subscribers ratio above 1 means the algorithm shows the channel beyond its subscribers. A variation coefficient under 1 means steady views, and above 1.5 means a few hits carry the channel. Outlier counts cannot be filtered on, so read `positiveOutliersCount` on each hit.
- **Index values against live reads.** A search hit's statistics come from the index. A `get_channel` read is live. The two can differ a lot on small or young channels. When you read a channel, use the live value and say which one you used.
- **App default views.** The Niche Finder opens with `subscribersFrom: 1`, `medianViewsFrom: 1000`, `videosCountFrom: 2` and no sort. The Outliers Finder opens with `viewCountFrom: 5000`, `type: "video"` and no sort. Use these settings to get the same unbiased sample the user sees in the app.
- **Dates on channels.** `joinedDateFrom` is when the channel was created. `sortBy: "foundAt"` orders by when TubeLab first found the channel.
- **Faceless flags** are predictions. Check them on the thumbnails when it matters.
- **Sponsors.** The public API strips the `sponsored` flag inside `monetization`. Read `detections.sponsored.detected` instead.
- **First-world audiences.** RPM estimates are most reliable for these. Filter on `audienceRegion` `021` (Northern America), `154` (Northern Europe), `155` (Western Europe) and `053` (Australia and New Zealand), with income `upper_middle` or `high`. Prefer this to filtering on RPM.
- **Shorts.** For Shorts channels, pair `contentKind: "short-form"` with `filterBy: "short"`, so range filters read the Shorts statistics. Monetization data is less accurate on Shorts-only channels.
- **Trending formats.** `framework` is the template with `[X]` slots. `pattern` is the value to pass as `titlePattern` to `search_outliers`, unchanged. `overall_stats.doc_count` is the number of videos using it. The hit carries click triggers and overall stats, but no growth numbers. Growth is a filter and a sort key. Call a formula rising only when a search with `lastVideosCountChangePercentageFrom` returned it, and state the floor.
- **Niche Analyzer scores.** The app scores a sample of a niche's channels from 0 to 100, each capped at 100. Leave channels under 1,000 subscribers out, because their ratios mean nothing. Market Size is the average of each channel's most-viewed video ÷ 1,000,000 × 100. Unsaturated is the average of (average views ÷ subscribers) ÷ 1.1 × 100. Profitable is the average low RPM estimate ÷ 7 × 100. Under 50 is weak, 50 to 70 is fair, and 71 and above is strong.
- **Thumbnails.** A video hit carries `thumbnails.high.url`; on a channel hit that field is the avatar. Any video ID also works with `https://i.ytimg.com/vi/<id>/hqdefault.jpg`. In a report, show the 320-pixel `https://i.ytimg.com/vi/<id>/mqdefault.jpg`. It exists for every video and keeps reports compact; `maxresdefault.jpg` has returned 404. A terminated channel's videos return a grey placeholder there, so use `https://cdn.tubelab.net/vi/<id>.jpeg` for those. The tools return a link, not the picture, so always download and open the thumbnail of every video you analyze. If an image truly cannot be fetched, say it was not viewed, and never describe it unseen.
- **Transcripts.** A 30-minute video returns over 100KB. For a hook, read `events[]` until `startMs` passes 45000, then stop. Transcripts keep the spoken language.
- **Large responses.** Channel reads and transcripts run 75K characters and up. Extract what you need and never echo them. Some clients save oversized responses to a file named by timestamp, and reads fired in parallel have overwritten each other's file. Fetch large reads one at a time and parse the saved file.

## Quirks and errors

- `search_trending_formats` rejects `language` with "Expected string, received array". The MCP schema lists `language` as an array for every search tool, but this backend wants a string. Leave it out; the default is English.
- When left out, `search_trending_formats` defaults to English, `quality: "positive"`, `videosCountFrom: 18`, sorting by `lastVideosCountChangePercentage`, `size: 12`, and formulas found in the last 4 months.
- `search_related_channels` ranks by similarity, not size. A large seed channel returns small lookalikes unless you add `subscribersFrom`. Its hits are mostly small, recently found channels: with no floor, 12 of 20 hits for a 108K seed had under 100 subscribers. A floor at about a tenth of the seed's subscribers fixed the size but let in off-topic channels (13 of 20 on topic), and `subscribersFrom: 300000` has returned off-topic channels. Keep only on-topic hits. Several seeds blur into one generic set (31 of 40 hits shared between two different three-seed searches), and the seeds themselves do not come back. Use one seed per search.
- High `viewCountFrom` floors on `search_outliers` surface paid brand campaigns, with ratios of 50 and more. Add `channelMonetizationAdsense: true` or remove them by hand.
- `search_outliers` returns nothing with `averageViewsRatioTo` at 0.5: the index holds videos that beat their channel, not flops. Find flops in free channel reads.
- On `search_channels`, adding `contentKind: "long-form"` has let channels with a views-to-subscribers ratio near 0 through an `avgViewsToSubscribersRatioFrom: 1` filter. Leave `contentKind` out and drop Shorts-only channels by hand.
- `search_related_outliers` with a `title` anchor has returned off-topic hits and ignored `publishedAtFrom` and `classificationQuality`. The `videoId`, `thumbnailVideoId` and `relatedChannelId` anchors behave. `search_outliers` with `by: "lexical"` has ignored the query. In both cases, check the hits are on topic before spending more.
- `language` on outlier searches matches the indexed title language, not the audio. English-tagged titles can be Hindi, Urdu or Tamil videos. The title script and thumbnail text usually reveal it. Check `defaultAudioLanguage` from `get_video` when it matters.
- `channelVideoCountTo` caps at 120, because channels are sampled to 120 videos. `titlePattern` must contain `*` and at least two letters. Every range needs from below to.
- Channel sample dates (`publishedAtEstimate`) are rough: about a month off within the last year, and only the year before that. The list's order is reliable, newest first, and `get_video` gives the exact date. View counts in the list are rounded. Comment dates are only accurate to the month, and comment like counts are often null.
- `get_video_comments` returns "Failed Dependency" or "No comments found" when comments are disabled. Treat that as no data, not a failure. Its `comments[]` can repeat entries, so dedupe on author plus text. `authorIsChannelOwner` has come back null on every row, even on the creator's pinned comments. Spot the creator's replies by matching the author handle to the channel's.
- Empty `hits` with `pagination.total: 0`: widen recency, drop one filter or rephrase `query`. Keep the quality floor.
- `pagination.total` has come back as exactly twice `size`. Do not use it to measure how crowded a niche is.
- `get_channel` has no audience, monetization, revenue or RPM fields. Those appear only on search hits. To get them for one channel, call `search_channels` with `query: ["@handle"]` and no other filter. With `publishedAtFrom` or `classificationQuality` set, the channel often does not come back. A similar-channels search seeded with the channel does not return it.
- `monetization.adsense: false` means a channel lost AdSense only on a hit that also has a `monetizationChangedAt` date, which is what the `monetizationChanged` filter returns. Without that date, false only means the channel is not monetized.
- HTTP 429 is the rate limit, about 30 calls per window on the MCP, shared across sessions. Wait for the reset and retry. Pace reads rather than firing them all at once.

## Spending credits

Spend paid searches on finding candidates and free reads on understanding them. Two to six searches per job is a sane norm, and a paid search is not paged in a loop. Two skills go deeper, because the sample is the product: `niche-finder` pages two channel searches 3 to 4 pages deep, and `reverse-engineer-niche` uses up to 15 searches without paging. If a search errors, call `get_credits_balance`, then retry once with fewer filters. Keep budgets and credit counts out of the report; give them if the user asks.

## Full reference

- When connected to the MCP, the tool schemas list every parameter name and allowed value. Read them before guessing a filter.
- For the full parameter list, response shapes, REST endpoints, authentication, pagination and error codes, fetch https://tubelab.net/docs/skill.md. It is generated from the API spec, so it stays current.
- Fetch it when you need a parameter the schema does not explain, when you work without the MCP over REST, or when the user asks how the API works. Over REST, the parameter names are the same, and channel endpoints take a channel ID, not a handle.
