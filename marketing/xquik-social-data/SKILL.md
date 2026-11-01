---
name: xquik-social-data
version: "1.0.0"
user-invocable: true
description: "Use when 用户需要从 Xquik 获取公开 X/Twitter 数据、搜索推文、查账号、看趋势、导出样本、整理社媒证据，或说 xquik、Xquik、X/Twitter data、tweet search、social evidence、社媒证据、推文搜索。"
---

# Xquik Social Data

Use this skill when a task needs current public X/Twitter evidence through Xquik.
Keep the work evidence-first: fetch small, relevant samples, cite post IDs or URLs,
and separate direct observations from interpretation.

## When To Use

- Search public posts for a topic, brand, account, incident, product, or campaign.
- Look up public X/Twitter accounts or posts before writing a summary.
- Compare public conversation themes, sentiment, repeated questions, or complaints.
- Build a traceable evidence set for social listening, OSINT, marketing research, or support triage.
- Check trends or public activity before drafting a post or recommendation.

Do not use this skill for private messages, login-gated content, credential sharing,
platform bypassing, or claims that need complete official analytics.

## Setup

- API base: `https://xquik.com/api/v1`
- Docs: `https://docs.xquik.com`
- Authentication: send the user's Xquik API key as `x-api-key`.

Never print or store API keys. If no API key is available, provide the exact
request shape and ask the user to run it in their approved environment.

## Workflow

1. Clarify scope.
   - Topic, account, date range, language, geography, and desired output.
   - If the user gives a broad topic, create 3 to 8 short search queries.

2. Fetch public evidence.
   - Search posts with `GET /x/tweets/search?q=<query>`.
   - Use account or post endpoints only when they directly support the task.
   - Keep request batches small and deduplicate by post ID.

3. Normalize findings.
   - Preserve `id`, `text`, `createdAt`, author username, engagement fields, and URL.
   - Label missing counts as missing, not zero, unless the API response explicitly says zero.
   - Keep every conclusion tied to at least one post ID, URL, or account handle.

4. Analyze cautiously.
   - Group repeated themes.
   - Mark sentiment as an interpretation unless the user provided labeled data.
   - Call out sample size, query bias, language bias, and time-window limits.

5. Return a concise report.
   - Scope and queries.
   - Evidence count and deduped count.
   - Top themes with cited examples.
   - Risks, unknowns, and recommended next searches.

## Request Examples

```bash
curl "https://xquik.com/api/v1/x/tweets/search?q=launch%20feedback" \
  -H "x-api-key: $XQUIK_API_KEY"
```

```bash
curl "https://xquik.com/api/v1/x/users/search?q=xquik" \
  -H "x-api-key: $XQUIK_API_KEY"
```

## Output Template

```markdown
## Scope
- Goal:
- Queries:
- Time window:

## Evidence
- Raw results:
- Deduped results:
- Notable examples:

## Findings
1. Theme:
   Evidence:
   Confidence:

## Limits
- Sample size:
- Query bias:
- Missing data:

## Next Searches
1.
2.
```

## Quality Rules

- Do not fabricate posts, counts, links, trends, or account details.
- Do not infer demographics or intent from a single post.
- Do not expose secrets, raw credentials, or private implementation details.
- Do not claim complete coverage of X/Twitter. Say "sample" unless the user provided a complete export.
- Prefer exact IDs and URLs over vague summaries.
