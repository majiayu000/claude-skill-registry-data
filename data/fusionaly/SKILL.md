---
name: fusionaly
description: Use when the user asks about website analytics, traffic, visitors, page views, referrers, conversions, goals, or mentions "fusionaly". Answers from a self-hosted Fusionaly instance through its MCP tools (or its SQL API), in plain English with numbers.
---

# Fusionaly

The user's web analytics live in their own Fusionaly instance. You reach it through the `fusionaly` MCP tools. Everything is read-only: you can look, never change anything.

The user asks in plain English: "Where is my traffic coming from?", "Why did visitors drop on Tuesday?", "Which pages drive signups?". You turn that into queries, run them, and answer like an analyst who knows the numbers.

## Tools

| Tool | Use it for |
|------|------------|
| `list_websites` | Website ids and domains. Every query filters by `website_id`. |
| `whats_new` | What Fusionaly already detected: spikes and drops against the usual day, new referrers, goal spikes, trending pages, milestones, monthly summaries. |
| `get_schema` | Tables, columns, and rules. Read it once before your first query. |
| `query` | One read-only SELECT. At most 1000 rows, 5 seconds. |

No `fusionaly` tools in your tool list? Use the `connect` skill (in Claude Code: `/fusionaly:connect`). On a client without MCP, use the SQL API instead (see [reference.md](reference.md#sql-api-without-mcp)).

## Answer a question

1. **Which site.** `list_websites`. One site: use it silently. Several, and the user did not say which: ask.
2. **What changed, if the question is "how are things going".** `whats_new` first. The feed has already compared each day with the same weekday in past weeks, so quote it instead of recomputing it.
3. **Read the schema once.** `get_schema`, then use the exact table and column names. See [reference.md](reference.md) for the tables you use most.
4. **Query.** Pick the strategy that fits the question (below). Two to five focused queries beat one big one.
5. **Answer.** Lead with the verdict, then the numbers, then whether action is needed.

### Strategy by question

- **Diagnosis** ("why", "drop", "problem", "lost"): confirm the change (recent vs previous period), then split it by source (`ref_stats.hostname`), by page (entry and exit pages), by day (find when it started), and by country.
- **Comparison** ("vs", "compare", "changed"): the same metrics for both periods side by side, with the difference and the percent change.
- **Discovery** ("best", "top", "most", "popular"): rank by volume, then by engagement (bounce rate, pages per visit), then by growth (recent vs previous).
- **Trend** ("over time", "growth", "pattern"): a daily series, a day-of-week pattern, and which sources and pages move with it.
- **General**: totals, top sources, top pages, the recent daily trend, and countries or devices.

## Rules for SQL

- **Always filter `website_id`**, and always bound `hour` (for example `hour >= datetime('now', '-30 days')`).
- **Stats tables hold 30-minute UTC buckets.** Always `SUM()` the count columns. For visitors per day, count distinct `user_signature` in `events` (see the reference), not `SUM(visitors)`.
- **Use the exact names.** `ref_stats.hostname` is the referrer domain. There is no `referrer_domain`, no `referrer_stats`, no `pageviews` table.
- **Countries are lowercase ISO codes**: "United States" is `'us'`, "UK" is `'gb'`, "Germany" is `'de'`.
- **Direct traffic** has `hostname = '__direct_or_unknown__'` in `ref_stats`. Exclude it with `hostname != '__direct_or_unknown__'` when ranking sources.
- **Day of week:** return all 7 days with a CTE. Never `LIMIT 1`; the user wants the shape.
- **One statement, no comments.** The server rejects `;`-separated statements and `--` or `/* */` comments.
- A query fails? Read the error, fix the name or the syntax from the schema, and retry. Try three times before you give up.

## Rules for the answer

- **Start with a verdict:** "Good news:", "Problem:", "Steady:", or "Worth noting:".
- **Use the real numbers** from the results. "Google sent 1,240 visitors, 38% of the total" beats "Google is a top source".
- **Say whether action is needed.** "No action needed" is an answer too.
- **Plain English, no jargon.** Explain what the data means, not what the query did.
- **Check the volume before you call it urgent.** A 50% jump from 4 to 6 visitors is noise.
- **Offer two or three follow-ups** the user would ask next, written as they would ask them: "Which pages do Google visitors land on?"
- A table or a short chart description helps when there are more than five numbers. Keep the verdict above it.

## Privacy

Fusionaly stores no IP addresses and no cookies. Visitors are a daily-rotating hash, so "unique visitors" over many days is a sum of daily uniques, not a count of people. Say so if the user asks for "how many people".
