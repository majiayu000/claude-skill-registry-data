---
name: mcp-response-optimization
description: Prevent massive MCP responses from WordPress, Playwright, Notion, and other MCPs that can kill conversations on first call. Sophisticated token management for all MCP tool usage.
---

# MCP Response Optimization

## Core Principle

**REQUEST MINIMAL, DISPLAY NOTHING, SAVE EVERYTHING**

Single MCP calls can kill entire conversations. This skill ensures every MCP call is filtered, limited, silent, extracted, and saved for maximum token efficiency.

## When to Activate

**ALWAYS activate before ANY MCP tool call**, especially:
- WordPress MCP operations (list posts, get pages, media queries)
- Playwright browser automation (DOM queries, screenshots)
- Notion API queries (search, database queries)
- Any search or list operations across MCPs
- Large data retrievals from any source

This skill is **MANDATORY** for all MCP usage in Claude Desktop.

## The Critical Problem

**One MCP call = conversation dead:**
- WordPress query returns 50 full pages → 100,000+ tokens
- Playwright DOM query returns entire page HTML → 80,000+ tokens
- Notion search returns 100 full pages → 120,000+ tokens
- **Result:** Conversation ends on first message

## MCP Integration

This skill optimizes these MCPs:
- **wordpress-mcp**: WordPress content management
- **playwright**: Browser automation and testing
- **notion** / **notionApi**: Notion workspace integration
- **filesystem**: File system operations (for saving large responses)
- **gmail**: Email management
- **supabase**: Database queries
- **firecrawl-mcp**: Web scraping

## WordPress MCP - The Worst Offender

### The Problem
WordPress returns EVERYTHING by default:
- Full post content (50KB per post)
- All metadata, revisions, images (base64)
- Author details, comments, categories
- **One query = conversation killer**

### The Solution: Aggressive Filtering

#### Rule 1: Always Use Field Filters
```javascript
// ❌ NEVER:
wordpress.list_posts({ per_page: 100 })
// Returns: 5MB of data, 1,250,000 tokens

// ✅ ALWAYS:
wordpress.list_posts({
  per_page: 10,
  fields: 'id,title,date,status',
  context: 'view'
})
// Returns: 5KB of data, 1,250 tokens
```

#### Rule 2: Limit Results Aggressively
```javascript
// Default limits:
per_page: 10  // NEVER use 100
page: 1       // Paginate if needed
```

#### Rule 3: Request Specific Fields Only

**For Posts:**
```javascript
// Minimal (when listing):
fields: 'id,title,status,date'

// Add only when needed:
fields: 'id,title,status,date,excerpt'  // For preview
fields: 'id,title,content'  // Only when editing
```

**For Pages:**
```javascript
fields: 'id,title,status,parent'
```

**For Media:**
```javascript
// NEVER load full images
fields: 'id,title,source_url'  // URL only, not base64
```

#### Rule 4: Use Targeted Queries
```javascript
// ❌ BAD:
wordpress.list_posts({ search: 'conference' })

// ✅ GOOD:
wordpress.list_posts({
  search: 'conference',
  per_page: 5,
  fields: 'id,title,date',
  status: 'publish',
  orderby: 'date',
  order: 'desc'
})
```

#### Rule 5: Never Display Full Responses
```javascript
// ❌ DON'T:
console.log(response)

// ✅ DO:
const ids = response.map(post => ({ id: post.id, title: post.title }))
console.log(`Found ${ids.length} posts`)
```

### WordPress Response Patterns

**Pattern: List Posts**
```javascript
const posts = wordpress.list_posts({
  per_page: 10,
  fields: 'id,title,status,date',
  status: 'publish'
})

const post_ids = posts.map(p => p.id)
`Found ${posts.length} posts: ${post_ids.join(', ')}`
```

**Pattern: Get Single Post**
```javascript
const post = wordpress.get_post({
  id: 123,
  fields: 'id,title,content,status'
})

`Retrieved post: ${post.title} (${post.id})`
// Save full content to file if needed
```

**Pattern: Search and Filter**
```javascript
const results = wordpress.list_posts({
  search: 'keyword',
  per_page: 5,
  fields: 'id,title,date'
})

const filtered = results.filter(/* criteria */)
`Found ${filtered.length} matches: [${filtered.map(p => p.id)}]`
```

## Playwright MCP - DOM and Screenshot Killer

### The Problem
- Full page HTML (200KB)
- Complete DOM tree with attributes
- Base64 screenshots (500KB-2MB)
- **One screenshot = conversation over**

### The Solution: Selective Queries

#### Rule 1: Use CSS Selectors, Not Full DOM
```javascript
// ❌ NEVER:
playwright.evaluate("document.documentElement.outerHTML")
// Returns: 50,000+ tokens

// ✅ ALWAYS:
playwright.locator('.product-title').textContent()
// Returns: 10 tokens
```

#### Rule 2: Target Specific Elements
```javascript
const data = {
  title: await page.locator('h1').textContent(),
  price: await page.locator('.price').textContent(),
  available: await page.locator('.stock-status').textContent()
}
// DON'T extract full page content
```

#### Rule 3: Screenshots - Save, Never Display
```javascript
// ❌ NEVER include in response:
const screenshot = await page.screenshot()
// 500KB-2MB base64 = 125,000+ tokens

// ✅ SAVE screenshot:
await page.screenshot({ path: '/outputs/screenshot.png' })
`Screenshot saved: /outputs/screenshot.png`
// 20 tokens vs 125,000 tokens
```

#### Rule 4: Limit Element Extraction
```javascript
const products = await page.locator('.product-card').all()

const product_data = []
for (const product of products.slice(0, 10)) {
  product_data.push({
    name: await product.locator('.name').textContent(),
    price: await product.locator('.price').textContent()
  })
}

fs.writeFileSync('/outputs/products.json', JSON.stringify(product_data))
`Extracted ${product_data.length} products → /outputs/products.json`
```

### Playwright Response Patterns

**Pattern: Page Scraping**
```javascript
await page.goto(url)

const data = {
  title: await page.title(),
  h1: await page.locator('h1').first().textContent(),
  meta: await page.locator('meta[name="description"]').getAttribute('content')
}

fs.writeFileSync('/outputs/page_data.json', JSON.stringify(data))
`Page data saved: /outputs/page_data.json`
```

**Pattern: Element Analysis**
```javascript
const count = await page.locator('.product-item').count()
`Found ${count} products`

const sample = await page.locator('.product-item').first().textContent()
`Sample product: ${sample}`
```

**Pattern: Screenshots for User**
```javascript
await page.screenshot({
  path: '/mnt/user-data/outputs/page.png',
  fullPage: false  // Viewport only
})

`[View screenshot](computer:///mnt/user-data/outputs/page.png)`
```

## Notion MCP - Large Page Objects

### The Problem
Notion returns full page objects with all blocks - can be massive.

### The Solution
```javascript
// ❌ DON'T:
notion.search({ query: 'project' })  // 100 full pages

// ✅ DO:
notion.search({
  query: 'project',
  page_size: 10,
  filter: { property: 'Status', select: { equals: 'Active' } }
})

const page_ids = results.map(r => r.id)
`Found ${page_ids.length} pages: ${page_ids}`
```

## Universal MCP Rules

### Rule 1: Pre-Call Token Budget
Before EVERY MCP call:
- What's minimum data I actually need?
- Can I filter to specific fields?
- Can I limit result count?
- Will response fit in 2,000 tokens?

**If answer to last question is NO → Adjust parameters**

### Rule 2: Pagination Over Bulk
```javascript
// ❌ NEVER:
get_all_items({ limit: 1000 })

// ✅ ALWAYS:
get_items({ limit: 10, page: 1 })
```

### Rule 3: Save Large Responses
```javascript
// Any response >5KB → Save to file

// ❌ DON'T:
console.log(large_response)

// ✅ DO:
fs.writeFileSync('/outputs/response.json', JSON.stringify(large_response))
`Response saved: /outputs/response.json`
```

### Rule 4: ID-Based Workflows
```javascript
// Step 1: Get IDs only
const ids = get_minimal_list()

// Step 2: User picks which ID
`Found ${ids.length} items: ${ids}`

// Step 3: Fetch full details for THAT ONE
const full_item = get_item_by_id(selected_id)
```

### Rule 5: Never Display Raw MCP Responses
```javascript
// ❌ FATAL:
`Here's what I found: ${JSON.stringify(mcp_response)}`

// ✅ CORRECT:
const summary = {
  count: mcp_response.length,
  items: mcp_response.map(i => i.id)
}
`Found ${summary.count} items: ${summary.items.join(', ')}`
```

## Token Estimation Guide

| Operation | Bad Approach | Good Approach |
|-----------|-------------|---------------|
| List 100 WP posts | 1,000,000 tokens | 2,500 tokens |
| Get WP page content | 50,000 tokens | 200 tokens |
| Playwright full DOM | 100,000 tokens | 500 tokens |
| Playwright screenshot | 125,000 tokens | 50 tokens |
| Notion page search | 80,000 tokens | 1,000 tokens |

## Pre-Call Checklist

Before EVERY MCP tool call:

1. ✅ Minimum fields requested?
2. ✅ Result limit set to <20?
3. ✅ Estimated response <2,000 tokens?
4. ✅ Plan to save, not display?
5. ✅ ID-based workflow possible?
6. ✅ Pagination strategy ready?

**If all YES → Proceed**
**If any NO → Adjust parameters**

## Emergency Patterns

### If MCP Response Already Too Large
```javascript
// Response came back huge (>50,000 tokens)

// 1. Save full response to file
fs.writeFileSync('/outputs/large_response.json', JSON.stringify(response))

// 2. Extract minimal summary
const summary = {
  count: response.length,
  first_id: response[0]?.id,
  last_id: response[response.length - 1]?.id
}

// 3. Return summary only
`Response saved to /outputs/large_response.json`
`Summary: ${summary.count} items (${summary.first_id} to ${summary.last_id})`
```

## Success Checklist

This skill is working correctly when:
- ✅ No MCP call exceeds 2,000 tokens in response
- ✅ WordPress queries use field filters 100% of time
- ✅ Playwright saves screenshots, never displays
- ✅ Raw MCP responses NEVER appear in conversation
- ✅ ID-based workflows used consistently
- ✅ Large datasets saved to files automatically

## The Golden Rules

1. **Request minimal fields** - Only what you need
2. **Limit results aggressively** - 10 items max initially
3. **Save, don't display** - Files, not conversation
4. **IDs, not content** - Work with identifiers
5. **Paginate on demand** - Never bulk load
6. **Estimate before call** - Budget tokens first

## Integration with Other Skills

Works with:
- **curv-design-system** - On-brand outputs with token efficiency
- **dashboard-auto-generation** - Data dashboards without token bloat

---

**Deployment:** Import .zip to Claude Desktop → Settings → Skills
**Impact:** Prevents 50,000-100,000+ token MCP disasters
**Result:** Full conversation capacity instead of 1-message death
