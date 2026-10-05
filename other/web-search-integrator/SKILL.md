---
name: web-search-integrator
description: Integrate Tavily for real-time web search and content extraction. Use this skill when the application needs web search capabilities, content extraction from URLs, website crawling, or AI-powered research. Triggers on requests for web search, URL content extraction, site crawling, or real-time information retrieval.
_meta_type: sdk
---

# Tavily Web Search SDK Integration

## Scenarios

- **Real-time Search**: Web search capabilities for LLM and AI Agent workflows
- **AI Chatbots**: Real-time information retrieval for conversational AI
- **Content Extraction**: Extract and analyze content from URLs
- **Website Crawling**: Crawl and map website structures
- **Deep Research**: Generate comprehensive research reports

**Not recommended for:**
- Offline-only applications
- Large-scale scraping without rate limiting
- Applications requiring search result caching (results are real-time)

## Setup

### 1. Install Dependencies

```bash
npm install @tavily/core
```

### 2. Copy SDK Wrapper

Read `lib/web-search.ts` from this skill and copy it to the project, then use it directly.

## Configuration

### Zero Configuration (Default)

Genie provides default zero-configuration support using `tavily.auth-proxy.local` as the endpoint. **No environment variables are required** - Genie has integrated authentication in the proxy gateway by default.

Simply use:

```typescript
import { createClient } from './lib/web-search';
const client = createClient();
```

### Custom Configuration (Optional)

Users can optionally configure environment variables. When configured, Genie will use user-provided credentials instead of the default proxy:

```env
# Optional - Only configure if you want to use your own credentials
TAVILY_WEB_SEARCH_API_KEY=tvly-your-api-key-here
```

**Obtaining Credentials** (if needed):
1. Visit [Tavily Platform](https://app.tavily.com/)
2. Sign in or create an account
3. Copy your API Key from the Dashboard

## Quick Start

### Basic Search

```typescript
import { createClient } from './lib/web-search';

const client = createClient();

// Basic search
const response = await client.search('Latest AI developments');
console.log(response.answer);
console.log(response.results);
```

### Advanced Search

```typescript
const response = await client.search('What is quantum computing?', {
  searchDepth: 'advanced',      // 'basic' | 'advanced'
  topic: 'general',             // 'general' | 'news' | 'finance'
  maxResults: 10,               // 0-20
  includeAnswer: true,          // Get AI-generated answer
  includeRawContent: 'markdown' // Include full page content
});
```

### Content Extraction

```typescript
// Extract content from URLs (max 20 URLs per request)
const response = await client.extract([
  'https://example.com/article1',
  'https://example.com/article2'
], {
  format: 'markdown',
  extractDepth: 'basic'
});
```

### Website Crawling

```typescript
const response = await client.crawl('https://docs.example.com', {
  maxDepth: 3,
  limit: 50,
  instructions: 'Find all API documentation pages'
});
```

### Website Mapping

```typescript
// Get all URLs from a website
const response = await client.map('https://example.com', {
  maxDepth: 2,
  limit: 100
});
// Returns array of discovered URLs
```

### Deep Research

```typescript
// Create research task
const task = await client.research('AI trends in 2025', {
  model: 'pro',
  citationFormat: 'apa'
});

// Get research report
const report = await client.getResearch(task.requestId);
```

## Response Structure

```typescript
// Search Response
{
  answer?: string;        // AI-generated answer (if includeAnswer: true)
  results: Array<{
    title: string;
    url: string;
    content: string;      // Snippet or full content
    score: number;        // Relevance score
    publishedDate?: string;
  }>;
  query: string;
  responseTime: number;
}
```

## Architecture Integration

### Service Layer Pattern (Recommended)

```typescript
// src/services/search.service.ts
import { createClient } from '../lib/web-search';

export class SearchService {
  private client = createClient();

  async search(query: string) {
    return this.client.search(query, {
      searchDepth: 'advanced',
      includeAnswer: true,
      maxResults: 5
    });
  }

  async getLatestNews(topic: string) {
    return this.client.search(topic, {
      topic: 'news',
      timeRange: 'week',
      maxResults: 10
    });
  }

  async extractArticle(url: string) {
    const result = await this.client.extract([url], {
      format: 'markdown'
    });
    return result.results[0];
  }
}
```

### Express Route Example

```typescript
// src/routes/search.routes.ts
import { Router } from 'express';
import { SearchService } from '../services/search.service';

const router = Router();
const searchService = new SearchService();

router.get('/search', async (req, res) => {
  const { q } = req.query;
  const results = await searchService.search(q as string);
  res.json(results);
});

router.get('/news', async (req, res) => {
  const { topic } = req.query;
  const results = await searchService.getLatestNews(topic as string);
  res.json(results);
});
```

## Search Options

| Option | Values | Description |
|--------|--------|-------------|
| searchDepth | 'basic', 'advanced' | Search depth level |
| topic | 'general', 'news', 'finance' | Search topic category |
| maxResults | 0-20 | Maximum results to return |
| includeAnswer | boolean, 'basic', 'advanced' | Include AI answer |
| includeRawContent | false, 'markdown', 'text' | Include full page content |
| timeRange | 'day', 'week', 'month', 'year' | Time filter for results |
| includeDomains | string[] | Only include these domains |
| excludeDomains | string[] | Exclude these domains |

## Security Best Practices

1. **Never expose API Key in frontend**: Always call search from backend
2. **Use environment variables**: Store API key in `.env`
3. **Implement rate limiting**: Prevent excessive API usage
4. **Validate user input**: Sanitize search queries

## Troubleshooting

**Authentication Errors**
- Verify `TAVILY_WEB_SEARCH_API_KEY` environment variable is set if using custom configuration
- Check API Key format starts with `tvly-`

**Empty Results**
- Try using `searchDepth: 'advanced'`
- Remove overly restrictive domain filters
- Check if query is too specific

**Rate Limiting**
- Implement request throttling
- Cache frequently requested searches

## Resources

- **SDK Wrapper Source**: `lib/web-search.ts`
- **Official Documentation**: [docs.tavily.com](https://docs.tavily.com)
- **API Console**: [app.tavily.com](https://app.tavily.com)
