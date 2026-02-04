---
name: unbrowser
description: "Intelligent web browsing API that learns from patterns, discovers APIs automatically, and progressively eliminates browser rendering for 10x faster data extraction. Use when you need to extract content from websites, discover APIs, handle authenticated sessions, or automate multi-step browsing workflows."
---

# Unbrowser - Intelligent Web Browsing

Unbrowser (npm: `llm-browser`) is an intelligent web browsing system that **learns from every browse operation** to progressively eliminate the need for slow browser rendering.

## When to Use This Skill

Use Unbrowser when you need to:

- **Extract content from websites** - Articles, product data, structured information
- **Discover and use APIs** - Automatically find and cache API endpoints
- **Handle authenticated sessions** - Login flows, cookies, persistent sessions
- **Learn browsing patterns** - Save and replay multi-step workflows
- **Bypass rendering** - 10x faster than Playwright for repeat visits

## Core Philosophy: "Browser Minimizer"

The goal is to **progressively eliminate browser overhead**:

1. **First visit**: Use content intelligence or lightweight rendering (~200-500ms)
2. **Learning**: Discover APIs, learn patterns, build procedural skills
3. **Future visits**: Direct API calls or cached patterns (~50-200ms, 10x faster)
4. **Collective intelligence**: Patterns learned by all users benefit everyone (cloud API only)

## Quick Start

### Installation

```bash
# For Claude Desktop (MCP)
npm install -g llm-browser

# For Node.js projects
npm install llm-browser
```

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "unbrowser": {
      "command": "npx",
      "args": ["llm-browser"]
    }
  }
}
```

### SDK Usage (Local)

For local SDK usage (all processing runs on your machine):

```typescript
import { createLLMBrowser } from 'llm-browser/sdk';

const browser = await createLLMBrowser();
const result = await browser.browse('https://example.com');

console.log(result.content.markdown);  // Clean markdown content
console.log(result.apis);              // Discovered API endpoints
console.log(result.meta.strategy);     // How content was extracted
```

## Key Capabilities

### 1. Tiered Rendering (Fastest First)

Unbrowser tries **fastest strategies first**, falling back only when needed:

| Tier | Method | Speed | Use Case |
|------|--------|-------|----------|
| 1 | **Content Intelligence** | ~50-200ms | Framework data (__NEXT_DATA__), structured data (JSON-LD), API prediction |
| 2 | **Lightweight Rendering** | ~200-500ms | Simple JavaScript execution without full browser |
| 3 | **Playwright** (optional) | ~2-5s | Complex JavaScript, authentication flows, dynamic content |

**Example:**

```typescript
// First visit: Uses tier 2 (lightweight rendering)
const result1 = await browser.browse('https://news-site.com/article');
// meta.strategy: "lightweight" (~400ms)

// Unbrowser learns the site has __NEXT_DATA__
// Second visit: Uses tier 1 (intelligence)
const result2 = await browser.browse('https://news-site.com/another-article');
// meta.strategy: "framework-extraction" (~80ms) - 5x faster!
```

### 2. API Discovery & Caching

Automatically discovers and uses APIs instead of scraping HTML:

```typescript
// First visit: Scrapes HTML
const product = await browser.browse('https://shop.com/product/123');

// Unbrowser discovers: GET /api/products/123
// Future visits: Direct API call (10x faster, no rendering)

// Access discovered APIs
console.log(result.apis);
// [{
//   url: "https://shop.com/api/products/123",
//   method: "GET",
//   pattern: "rest-resource",
//   confidence: 0.95
// }]
```

**Supported Discovery Methods:**

- **Framework extraction** - Next.js, Nuxt, Gatsby, Remix
- **OpenAPI/Swagger** - Auto-detect and parse specs
- **GraphQL introspection** - Schema discovery via `__schema` query
- **JavaScript analysis** - Extract API calls from bundle code
- **Pattern learning** - Learn from successful API extractions

### 3. Procedural Memory (Skill Learning)

Learns and replays browsing workflows with versioning and rollback:

```typescript
// Teach Unbrowser a skill
await browser.recordSkill('extract-job-posting', async (recorder) => {
  await recorder.navigate('https://jobboard.com/post/123');
  await recorder.click('.view-details');
  await recorder.extract({
    title: '.job-title',
    salary: '.salary-range',
    requirements: '.requirements ul li'
  });
});

// Replay on different job postings
const job1 = await browser.replaySkill('extract-job-posting', 'https://jobboard.com/post/456');
const job2 = await browser.replaySkill('extract-job-posting', 'https://jobboard.com/post/789');
```

Skills include:

- **Version control** - Rollback if new version performs worse
- **Performance tracking** - Success rate, execution time
- **Cross-domain transfer** - Apply patterns to similar sites
- **Auto-adaptation** - Adjusts when selectors change

### 4. Session Management

Persistent authenticated sessions with encryption:

```typescript
// Login once
await browser.browse('https://platform.com/login', {
  session: 'my-platform-session',
  actions: [
    { type: 'fill', selector: '#email', value: 'user@example.com' },
    { type: 'fill', selector: '#password', value: 'password123' },
    { type: 'click', selector: 'button[type="submit"]' }
  ]
});

// Reuse session for authenticated requests
const dashboard = await browser.browse('https://platform.com/dashboard', {
  session: 'my-platform-session'
});

// Sessions persist across restarts (encrypted at rest)
```

### 5. Batch Operations

Process multiple URLs in parallel:

```typescript
const results = await browser.batch([
  'https://company1.com',
  'https://company2.com',
  'https://company3.com'
], {
  parallel: 3,  // Max concurrent requests
  timeout: 10000
});

// Returns array of results
results.forEach(r => console.log(r.content.title));
```

### 6. Stealth Mode

Evade bot detection with fingerprint randomization:

```bash
export LLM_BROWSER_STEALTH=true
```

Features:

- **Fingerprint evasion** - Randomize user agent, screen resolution, fonts
- **Behavioral delays** - Human-like timing between actions
- **WebRTC/Canvas fingerprint masking**
- **Proxy support** - Rotate IPs (Bright Data integration)

## Cloud API (Alternative to Local MCP)

For multi-tenant access or non-Node.js languages:

```bash
# REST API
curl -X POST https://api.unbrowser.ai/v1/browse \
  -H "Authorization: Bearer $UNBROWSER_API_KEY" \
  -d '{"url": "https://example.com"}'

# SDK (thin HTTP wrapper)
npm install @unbrowser/core
```

```typescript
import { createUnbrowser } from '@unbrowser/core';

const client = createUnbrowser({
  apiKey: process.env.UNBROWSER_API_KEY
});

const result = await client.browse('https://example.com');
```

**Cloud API benefits:**

- **Collective learning** - Shared pattern pool across all tenants
- **No local dependencies** - No Playwright, no Node.js required
- **Usage-based billing** - Pay only for what you use
- **Multi-language support** - Python, Ruby, Go, etc.

See [api.unbrowser.ai/docs](https://api.unbrowser.ai/docs) for full API reference.

## Common Patterns

### Extract Article Content

```typescript
const article = await browser.browse('https://blog.com/post');

console.log(article.content.markdown);  // Clean markdown
console.log(article.content.structured?.author);
console.log(article.content.structured?.publishDate);
```

### Monitor Product Prices

```typescript
// First visit: Learns pattern
const product = await browser.browse('https://shop.com/product/123');

// Set up monitoring (checks every hour)
await browser.monitor('https://shop.com/product/123', {
  interval: '1h',
  onChange: (result) => {
    const price = result.content.structured?.price;
    if (price < 100) {
      console.log('Price dropped!', price);
    }
  }
});
```

### Multi-step Workflow

```typescript
// Record workflow
await browser.recordWorkflow('company-research', async (recorder) => {
  const homepage = await recorder.browse('https://company.com');
  const about = await recorder.browse('https://company.com/about');
  const contact = await recorder.browse('https://company.com/contact');

  return {
    name: homepage.content.structured?.companyName,
    description: about.content.text,
    email: contact.content.structured?.email
  };
});

// Replay on different companies
const intel1 = await browser.replayWorkflow('company-research', 'https://company1.com');
const intel2 = await browser.replayWorkflow('company-research', 'https://company2.com');
```

### Discover and Call APIs

```typescript
// Browse once to discover API
const result = await browser.browse('https://api-docs.com/products');

// Discovered APIs are cached
const api = result.apis[0];
console.log(api.url);      // "https://api-docs.com/v1/products"
console.log(api.method);   // "GET"

// Future requests use API directly (10x faster)
const products = await browser.fetch(api.url);
```

## Advanced Options

### Customize Output

```typescript
const result = await browser.browse(url, {
  maxChars: 10000,           // Limit text length
  includeTables: true,       // Extract tables as CSV
  includeNetwork: true,      // Capture network requests
  includeConsole: false,     // Skip console logs
  cleanMarkdown: true        // Remove navigation/ads
});
```

### Proxy Configuration

```typescript
const result = await browser.browse(url, {
  proxy: {
    server: 'http://proxy.example.com:8080',
    username: 'user',
    password: 'pass'
  }
});
```

### Debugging

```typescript
const result = await browser.browse(url, {
  debug: {
    visible: true,        // Show browser window
    slowMotion: 100,      // 100ms delay between actions
    screenshots: true,    // Capture screenshots
    consoleLogs: true     // Collect console output
  }
});

console.log(result.debug.screenshots);  // Array of base64 images
console.log(result.debug.actionTrace);  // Step-by-step actions
```

## Performance Comparison

| Method | First Visit | After Learning | Speedup |
|--------|-------------|----------------|---------|
| **Playwright** | ~2-5s | ~2-5s | 1x |
| **Unbrowser (first)** | ~200-500ms | - | 5-10x |
| **Unbrowser (learned)** | - | ~50-200ms | **20-50x** |

Learning happens automatically - no configuration needed.

## Troubleshooting

### Browser Not Rendering

Unbrowser works **without Playwright** by default. If you need full browser rendering:

```bash
npx playwright install chromium
```

Then Unbrowser will use tier 3 (Playwright) for complex sites.

### API Discovery Not Working

Some sites block API access. Try:

1. **Use session authentication** - Login first, then browse
2. **Enable stealth mode** - `LLM_BROWSER_STEALTH=true`
3. **Use proxy** - Rotate IPs to avoid rate limiting

### Learning Not Persisting

By default, learning is saved to `./procedural-memory.json`. Check:

```bash
ls -la procedural-memory.json
# Should show file with recent timestamp
```

For cloud API, learning is persisted server-side (no local files).

## Environment Variables

```bash
# Local MCP/SDK
LLM_BROWSER_STEALTH=true           # Enable stealth mode
LLM_BROWSER_SESSION_DIR=./sessions # Session storage directory

# Cloud API
UNBROWSER_API_KEY=ub_live_xxxxx    # API key
UNBROWSER_API_URL=https://api.unbrowser.ai  # Override API URL
```

## Resources

- **Documentation**: https://github.com/ogoldberg/ai-first-web-client#readme
- **API Reference**: https://api.unbrowser.ai/docs
- **Examples**: https://github.com/ogoldberg/ai-first-web-client/tree/main/examples
- **NPM Package**: https://www.npmjs.com/package/llm-browser
- **Cloud SDK**: https://www.npmjs.com/package/@unbrowser/core

## License

MIT License - See [LICENSE](https://github.com/ogoldberg/ai-first-web-client/blob/main/LICENSE)

## Support

- **Issues**: https://github.com/ogoldberg/ai-first-web-client/issues
- **Discussions**: https://github.com/ogoldberg/ai-first-web-client/discussions
