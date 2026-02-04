---
name: rss-fetch
description: Fetch and parse RSS feeds from provided URLs. Use this skill when the user wants to gather news articles for content creation.
---

# RSS Feed Fetcher

This skill fetches and parses RSS feeds from provided URLs, extracting article titles, descriptions, links, and publication dates.

## When to Use

Use this skill when:
- Starting the content creation workflow
- Need to gather recent news articles on a topic
- Want to find trending stories for blog inspiration

## Default RSS Sources

When no specific sources are provided, use these default feeds:

```
https://hnrss.org/frontpage
https://techcrunch.com/feed/
https://www.wired.com/feed/rss
https://feeds.arstechnica.com/arstechnica/technology-lab
https://www.theverge.com/rss/index.xml
```

## How to Use

Execute the script with RSS feed URLs as arguments:

```bash
rss-fetch.sh "url1" "url2" "url3" ...
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| urls | Yes | One or more RSS feed URLs to fetch |

### Example with All Default Sources

```bash
/home/user/.claude/skills/rss-fetch/scripts/rss-fetch.sh \
  "https://hnrss.org/frontpage" \
  "https://techcrunch.com/feed/" \
  "https://www.wired.com/feed/rss" \
  "https://feeds.arstechnica.com/arstechnica/technology-lab" \
  "https://www.theverge.com/rss/index.xml"
```

## Output

Results are saved to `/tmp/rss/feeds.json` with this structure:

```json
{
  "fetched_at": "2024-01-15T10:30:00Z",
  "sources": ["hnrss.org", "techcrunch.com", ...],
  "articles": [
    {
      "title": "Article Title",
      "description": "Article summary...",
      "link": "https://...",
      "pubDate": "2024-01-15T09:00:00Z",
      "source": "techcrunch.com"
    }
  ]
}
```

After fetching, read `/tmp/rss/feeds.json` to see all available articles.

## Guidelines

1. Run this skill at the beginning of the content creation workflow
2. Pass all RSS URLs as arguments to fetch from multiple sources
3. After fetching, analyze the articles to find relevant topics
4. Use the article links as sources for your generated content
5. Filter articles based on the user's specified topic/keywords
