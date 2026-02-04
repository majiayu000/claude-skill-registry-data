---
name: playwright-scraper
description: |
  Production-proven Playwright web scraping patterns with selector-first approach and robust error handling.
  Use when users need to build web scrapers, extract data from websites, automate browser interactions,
  or ask about Playwright selectors, text extraction (innerText vs textContent), regex patterns for HTML,
  fallback hierarchies, or scraping best practices.
---

# Playwright Web Scraper

Production-proven web scraping patterns using Playwright with selector-first approach and robust error handling.

---

## Core Principles

### 1. Selector-First Approach

**Always prefer semantic locators over CSS selectors:**

```typescript
// ✅ BEST: Semantic locators (accessible, maintainable)
await page.getByRole('button', { name: 'Submit' })
await page.getByText('Welcome')
await page.getByLabel('Email')

// ⚠️ ACCEPTABLE: Text patterns for dynamic content
await page.locator('text=/\\$\\d+\\.\\d{2}/')

// ❌ AVOID: Brittle CSS selectors
await page.locator('.btn-primary')
await page.locator('#submit-button')
```

### 2. Page Text Extraction

**Critical difference between `textContent` and `innerText`:**

```typescript
// ❌ WRONG: Returns ALL text including hidden elements, scripts, iframes
const pageText = await page.textContent("body");

// ✅ CORRECT: Returns only VISIBLE text (what users see)
const pageText = await page.innerText("body");
```

**Use case for each:**
- `innerText("body")` - Extract visible content for regex matching
- `textContent(selector)` - Get text from specific elements

### 3. Regex Patterns for Extraction

**Handle newlines and whitespace in HTML:**

```typescript
// ❌ FAILS: [^$]* doesn't match across newlines
const match = pageText.match(/ADULT[^$]*(\$\d+\.\d{2})/);

// ✅ WORKS: [\s\S]{0,10} matches any character including newlines
const match = pageText.match(/ADULT[\s\S]{0,10}(\$\d+\.\d{2})/);
```

**Common patterns:**
```typescript
// Price extraction
/\$(\d+\.\d{2})/

// Date/time
/(\d{1,2}\s+[A-Za-z]{3}\s+\d{4},\s+\d{1,2}:\d{2}[ap]m)/i

// Screen number
/Screen\s+(\d+)/i
```

### 4. Fallback Hierarchy

Implement 4-tier fallback for robustness:

```typescript
async function extractField(page: Page, fieldName: string): Promise<string | null> {
  // Tier 1: Primary semantic selector
  try {
    const value = await page.getByLabel(fieldName).textContent();
    if (value) return value.trim();
  } catch {}

  // Tier 2: Alternative selectors
  try {
    const value = await page.locator(`[aria-label="${fieldName}"]`).textContent();
    if (value) return value.trim();
  } catch {}

  // Tier 3: Text pattern matching
  const pageText = await page.innerText("body");
  const pattern = new RegExp(`${fieldName}[\\s\\S]{0,20}([A-Z0-9].+)`, 'i');
  const match = pageText.match(pattern);
  if (match?.[1]) return match[1].trim();

  // Tier 4: Return null (caller handles missing data)
  return null;
}
```

### 5. Error Handling Patterns

```typescript
// ✅ GOOD: Try-catch with specific actions
try {
  await page.goto(url, { waitUntil: 'domcontentloaded' });
} catch (error) {
  throw new Error(`Failed to navigate to ${url}: ${error.message}`);
}

// ✅ GOOD: Timeout with clear error
try {
  await page.waitForSelector('text="Loading complete"', { timeout: 5000 });
} catch {
  // Continue anyway - loading indicator is optional
}
```

### 6. Image Selection Best Practices

```typescript
// ❌ WRONG: Grabs first matching image (could be from carousel/ads)
const poster = await page.locator('img[src*="movies"]').first();

// ✅ CORRECT: Target specific hero/header image
const poster = await page.locator('img[src*="movies/headers"]').first();

// ✅ BETTER: Use semantic structure
const poster = await page.locator('header img, [role="banner"] img').first();
```

### 7. Clean Separation of Concerns

Each scraper method should have a single responsibility:

```typescript
// ✅ GOOD: Each method scrapes ONE resource type
interface ScraperClient {
  scrapeMovies(): Promise<{ movies: Movie[] }>;
  scrapeSession(sessionId: string): Promise<SessionData>;
  scrapePricing(sessionId: string): Promise<PricingData>;
}

// ❌ BAD: Session method returns movie data (violates SRP)
interface ScraperClient {
  scrapeSession(sessionId: string): Promise<{
    session: SessionData;
    movieTitle: string;  // ❌ Cross-concern
    moviePoster: string; // ❌ Cross-concern
  }>;
}
```

**Composition over mixing concerns:**
```typescript
// ✅ Compose data from multiple focused scrapes
const movies = await client.scrapeMovies();
const movie = movies.find(m => m.sessionTimes.includes(sessionId));
const session = await client.scrapeSession(sessionId);
const pricing = await client.scrapePricing(sessionId);

// Build composite response
const ticket = {
  movieTitle: movie.title,        // From movies scrape
  moviePoster: movie.thumbnail,   // From movies scrape
  sessionDateTime: session.dateTime, // From session scrape
  pricing: pricing,               // From pricing scrape
};
```

## Implementation Checklist

When building a scraper, follow this sequence:

### Phase 1: Setup
- [ ] Install Playwright: `bun add playwright`
- [ ] Create browser instance with headless option
- [ ] Set user agent and viewport for realistic browsing

### Phase 2: Navigation
- [ ] Navigate to target URL
- [ ] Wait for page load (`domcontentloaded` or `networkidle`)
- [ ] Handle any cookie banners / popups

### Phase 3: Data Extraction
- [ ] Use `innerText("body")` for visible page text
- [ ] Extract data with semantic selectors first
- [ ] Add fallback selectors for each field
- [ ] Use regex patterns for dynamic content
- [ ] Validate extracted data format

### Phase 4: Robustness
- [ ] Add error handling with clear messages
- [ ] Implement timeout protection
- [ ] Track which selectors worked (`selectorsUsed`)
- [ ] Test against actual page HTML

### Phase 5: Testing
- [ ] Test with valid data
- [ ] Test with missing fields (use fallbacks)
- [ ] Test with network errors
- [ ] Verify no data leaks between scrapes

## Common Patterns

### Browser Setup

```typescript
import { chromium, type Browser, type Page } from 'playwright';

async function createBrowser(): Promise<Browser> {
  return await chromium.launch({
    headless: true, // Set false for debugging
  });
}

async function createPage(browser: Browser): Promise<Page> {
  const page = await browser.newPage({
    viewport: { width: 1280, height: 720 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
  });
  return page;
}
```

### Scraper Client Pattern

```typescript
export async function createScraperClient() {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  return {
    async scrapeData(url: string) {
      await page.goto(url, { waitUntil: 'domcontentloaded' });

      const pageText = await page.innerText("body");
      const selectorsUsed: Record<string, string> = {};

      // Extract fields with fallbacks
      let field1 = null;
      try {
        field1 = await page.getByRole('heading').textContent();
        selectorsUsed.field1 = "getByRole";
      } catch {
        const match = pageText.match(/Title:\s*(.+)/i);
        if (match) {
          field1 = match[1];
          selectorsUsed.field1 = "regex";
        }
      }

      return { field1, selectorsUsed };
    },

    async close() {
      await browser.close();
    },
  };
}
```

### CLI Integration

```typescript
#!/usr/bin/env bun

import { createScraperClient } from './scraper-client.ts';

async function main() {
  const args = process.argv.slice(2);
  const url = args[0];

  if (!url) {
    console.error('Usage: bun run cli.ts <url>');
    process.exit(1);
  }

  const client = await createScraperClient();

  try {
    const result = await client.scrapeData(url);
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(`Scraping failed: ${error.message}`);
    process.exit(1);
  } finally {
    await client.close();
  }
}

main();
```

## Debugging Tips

### Chrome DevTools Integration

Use the Chrome DevTools MCP server to inspect actual page structure:

```typescript
// In your conversation with Claude:
// "Use Chrome DevTools to inspect the pricing page"
// Claude will use: take_snapshot, evaluate_script, etc.
```

### Logging Selectors

Always track which selectors worked:

```typescript
const selectorsUsed: Record<string, string> = {};

// After each extraction
selectorsUsed.fieldName = "getByRole" | "regex" | "fallback-1";

// Return in response for debugging
return { data, selectorsUsed };
```

### Visual Debugging

```typescript
// Take screenshot at key points
await page.screenshot({ path: 'debug-step-1.png' });

// Highlight element before extraction
await page.locator(selector).highlight();
```

## Anti-Patterns to Avoid

### ❌ Using hypothetical attributes

```typescript
// DON'T assume data attributes exist
await page.locator('[data-price]'); // Might not exist!
```

### ❌ Over-relying on CSS classes

```typescript
// DON'T use implementation-specific classes
await page.locator('.MuiButton-root-xyz'); // Will break when CSS changes
```

### ❌ Ignoring visible vs. hidden text

```typescript
// DON'T use textContent for regex extraction
const text = await page.textContent("body"); // Includes hidden iframes!
```

### ❌ Not handling missing data

```typescript
// DON'T assume data exists
const price = await page.locator('.price').textContent(); // Might throw!

// DO use optional chaining and null returns
const price = await page.locator('.price').textContent().catch(() => null);
```

## Production Checklist

Before deploying a scraper:

- [ ] All selectors have fallbacks
- [ ] Error messages are clear and actionable
- [ ] Browser closes properly (use try/finally)
- [ ] No hardcoded delays (use waitForSelector)
- [ ] Respects rate limits / politeness delays
- [ ] Tracks which selectors worked for debugging
- [ ] Tests pass with missing/malformed data
- [ ] No cross-concern data mixing

## Resources

- Playwright Selectors: https://playwright.dev/docs/selectors
- Playwright Best Practices: https://playwright.dev/docs/best-practices
- Chrome DevTools MCP: Use for live page inspection
