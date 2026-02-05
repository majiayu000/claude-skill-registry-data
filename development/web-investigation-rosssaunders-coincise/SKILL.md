---
name: web-investigation
description:
  Investigate website structure and debug web scraping using Chrome DevTools
  MCP. Use when analyzing documentation frameworks, debugging extraction issues,
  understanding HTML structure, investigating why web content isn't being
  captured correctly, or exploring API documentation sites. Covers Redocly,
  Swagger UI, and other modern documentation frameworks.
allowed-tools:
  mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__take_snapshot,
  mcp__chrome-devtools__evaluate_script, Read, Grep, Glob
---

# Web Investigation with Chrome DevTools MCP

This skill provides workflows for investigating website structure, debugging web
scraping issues, and understanding documentation frameworks using Chrome
DevTools MCP.

## When to Use This Skill

Activate this skill when you need to:

- **Understand website structure** - Analyze how content is organized and
  rendered
- **Debug extraction issues** - Investigate why content isn't being captured
- **Identify documentation frameworks** - Determine if site uses Redocly,
  Swagger UI, etc.
- **Check authentication patterns** - Find how endpoints indicate authentication
  requirements
- **Verify HTML structure** - Confirm selectors and element attributes before
  extraction
- **Investigate dynamic content** - Check if content requires interaction
  (clicks, waits, etc.)

## Core Investigation Workflow

### 1. Navigate to the Target URL

```javascript
mcp__chrome - devtools__navigate_page({ url: "https://docs.example.com" })
```

### 2. Take Initial Snapshot (for simple checks)

For quick structure overview:

```javascript
mcp__chrome - devtools__take_snapshot()
```

**Note**: Snapshots can be very large (>25,000 tokens). Only use when you need
full accessibility tree. For targeted investigation, use `evaluate_script`
instead.

### 3. Targeted Investigation with evaluate_script

This is the primary investigation method - faster and more focused than
snapshots:

```javascript
mcp__chrome -
  devtools__evaluate_script({
    function: `() => {
    // Your investigation code here
    return {
      // Return structured data about what you found
    };
  }`
  })
```

## Common Investigation Patterns

### Pattern 1: Identify Documentation Framework

```javascript
mcp__chrome -
  devtools__evaluate_script({
    function: `() => {
    const body = document.body.innerHTML;

    // Check for Redocly
    const hasRedocly = document.querySelector('[data-section-id]') !== null;

    // Check for Swagger UI
    const hasSwagger = document.querySelector('.swagger-ui') !== null;

    // Check for custom framework indicators
    const hasCustom = document.querySelector('[data-api-explorer]') !== null;

    return {
      framework: hasRedocly ? 'Redocly' : hasSwagger ? 'Swagger UI' : 'Unknown',
      hasDataSectionIds: hasRedocly,
      hasSwaggerUI: hasSwagger,
      bodyClassList: document.body.className
    };
  }`
  })
```

### Pattern 2: Check Authentication Header Patterns

**Example from Backpack Integration:**

```javascript
mcp__chrome -
  devtools__evaluate_script({
    function: `() => {
    // Check both public and private endpoints
    const publicSection = document.querySelector('[data-section-id="tag/Markets/operation/get_markets"]');
    const privateSection = document.querySelector('[data-section-id="tag/Account/operation/get_account"]');

    const publicHtml = publicSection ? publicSection.innerHTML : '';
    const privateHtml = privateSection ? privateSection.innerHTML : '';

    return {
      public: {
        hasXApiKey: publicHtml.includes('X-API-KEY'),
        hasXSignature: publicHtml.includes('X-SIGNATURE'),
        hasXTimestamp: publicHtml.includes('X-TIMESTAMP'),
        hasAuthHeaders: publicHtml.toLowerCase().includes('header parameters')
      },
      private: {
        hasXApiKey: privateHtml.includes('X-API-KEY'),
        hasXSignature: privateHtml.includes('X-SIGNATURE'),
        hasXTimestamp: privateHtml.includes('X-TIMESTAMP'),
        hasAuthHeaders: privateHtml.toLowerCase().includes('header parameters')
      }
    };
  }`
  })
```

**Use this to**:

- Determine how to classify endpoints (public vs private)
- Identify which headers indicate authentication
- Understand exchange-specific patterns

### Pattern 3: Check for Expandable/Hidden Content

**Example from Backpack Integration (Response Buttons):**

```javascript
mcp__chrome -
  devtools__evaluate_script({
    function: `() => {
    // Find expandable buttons (200, 400, 500 response codes)
    const buttons = Array.from(document.querySelectorAll('button'));
    const responseButtons = buttons.filter(btn => {
      const text = btn.textContent;
      return /^\s*\d{3}\s/.test(text);
    });

    return {
      totalButtons: buttons.length,
      responseButtons: responseButtons.length,
      buttonTexts: responseButtons.slice(0, 5).map(b => b.textContent),
      hasExpandableContent: responseButtons.length > 0,
      ariaExpandedStates: responseButtons.map(b => b.getAttribute('aria-expanded'))
    };
  }`
  })
```

**Use this to**:

- Detect if response schemas are hidden
- Determine if buttons need to be clicked
- Understand interaction requirements

### Pattern 4: Analyze Section Structure

```javascript
mcp__chrome -
  devtools__evaluate_script({
    function: `() => {
    // Find all sections with IDs or data attributes
    const sections = document.querySelectorAll('[data-section-id], [id]');

    // Get first 10 sections with their attributes
    const sectionInfo = Array.from(sections).slice(0, 10).map(section => ({
      id: section.id || section.getAttribute('data-section-id'),
      tag: section.tagName,
      hasHeading: !!section.querySelector('h1, h2, h3'),
      headingText: section.querySelector('h1, h2, h3')?.textContent?.substring(0, 50)
    }));

    return {
      totalSections: sections.length,
      sections: sectionInfo
    };
  }`
  })
```

**Use this to**:

- Understand content organization
- Identify section boundaries
- Plan extraction selectors

### Pattern 5: Find Operation/Endpoint Sections

**Example from Backpack Integration:**

```javascript
mcp__chrome -
  devtools__evaluate_script({
    function: `() => {
    // Find sections that are operations (endpoints)
    const operations = document.querySelectorAll('[data-section-id]');

    const operationInfo = Array.from(operations)
      .filter(op => {
        const id = op.getAttribute('data-section-id');
        return id && id.includes('operation');
      })
      .slice(0, 5)
      .map(op => {
        const id = op.getAttribute('data-section-id');
        const methodEl = op.querySelector('[data-role="method"], .http-verb, .method');
        const pathEl = op.querySelector('[data-role="path"], .path, .endpoint-path');
        const heading = op.querySelector('h2, h3');
        const link = heading?.querySelector('a[href]');

        return {
          dataSectionId: id,
          method: methodEl?.textContent?.trim() || 'NOT_FOUND',
          path: pathEl?.textContent?.trim() || 'NOT_FOUND',
          headingText: heading?.textContent?.substring(0, 50),
          linkHref: link?.getAttribute('href')
        };
      });

    return {
      totalOperations: operations.length,
      operationEndpoints: operationInfo.length,
      examples: operationInfo
    };
  }`
  })
```

**Use this to**:

- Verify extraction selectors work
- Understand endpoint structure
- Test source URL extraction logic

### Pattern 6: Extract Table Structure

```javascript
mcp__chrome -
  devtools__evaluate_script({
    function: `() => {
    const tables = document.querySelectorAll('table');
    const firstTable = tables[0];

    if (!firstTable) return { error: 'No tables found' };

    // Analyze table structure
    const rows = firstTable.querySelectorAll('tr');
    const firstRow = rows[0];
    const cells = firstRow?.querySelectorAll('td, th');

    return {
      totalTables: tables.length,
      firstTableRows: rows.length,
      firstRowCells: cells?.length,
      hasProperTheadTbody: {
        thead: !!firstTable.querySelector('thead'),
        tbody: !!firstTable.querySelector('tbody')
      },
      firstRowHTML: firstRow?.outerHTML?.substring(0, 200)
    };
  }`
  })
```

**Use this to**:

- Check if tables need cleaning before extraction
- Understand table structure
- Verify GFM conversion will work

## Documentation Framework Specifics

### Redocly Framework

**Identifying characteristics**:

- Uses `data-section-id` attributes
- Expandable response sections (buttons with status codes)
- Operations have `tag/.../operation/...` patterns

**Key patterns**:

```javascript
// Check if Redocly
const isRedocly = !!document.querySelector("[data-section-id]")

// Find endpoint sections
const endpoints = document.querySelectorAll('[data-section-id*="operation"]')

// Check for expandable buttons
const hasExpandableResponses = !!document.querySelector("button[aria-expanded]")
```

**Common issues**:

- Response schemas hidden behind buttons → Need to click to expand
- DOM updates are async → Must wait after clicking
- Nested section structure → Need proper selectors

### Swagger UI Framework

**Identifying characteristics**:

- Contains `.swagger-ui` class
- Uses `.opblock` for operations
- Interactive try-it-out features

**Key patterns**:

```javascript
// Check if Swagger UI
const isSwagger = !!document.querySelector(".swagger-ui")

// Find operations
const operations = document.querySelectorAll(".opblock")
```

## Debugging Checklist

When extraction isn't working correctly, investigate in this order:

1. **Verify framework identification**
   - Run Pattern 1 to identify the framework
   - Confirm selectors match framework patterns

2. **Check for dynamic/hidden content**
   - Run Pattern 3 to find expandable elements
   - Determine if interaction is needed

3. **Analyze authentication patterns**
   - Run Pattern 2 on sample endpoints
   - Identify headers that indicate authentication

4. **Verify section structure**
   - Run Pattern 4 to understand organization
   - Check for proper boundary detection

5. **Test endpoint detection**
   - Run Pattern 5 to verify operation selectors
   - Confirm method/path extraction works

6. **Inspect table rendering**
   - Run Pattern 6 if tables are involved
   - Determine if cleanup is needed

## Example: Investigating Backpack Exchange

This is a real example of how this skill was used:

**Problem**: All 42 endpoints classified as private, 0 as public

**Investigation**:

```javascript
// 1. Navigate to docs
mcp__chrome - devtools__navigate_page({ url: "https://docs.backpack.exchange" })

// 2. Check a known public endpoint
mcp__chrome -
  devtools__evaluate_script({
    function: `() => {
    const section = document.querySelector('[data-section-id="tag/Markets/operation/get_markets"]');
    const html = section?.innerHTML || '';
    return {
      hasXApiKey: html.includes('X-API-KEY'),
      hasXSignature: html.includes('X-SIGNATURE'),
      hasXTimestamp: html.includes('X-TIMESTAMP')
    };
  }`
  })
// Result: All false → Public endpoint has NO auth headers

// 3. Check a known private endpoint
mcp__chrome -
  devtools__evaluate_script({
    function: `() => {
    const section = document.querySelector('[data-section-id="tag/Account/operation/get_account"]');
    const html = section?.innerHTML || '';
    return {
      hasXApiKey: html.includes('X-API-KEY'),
      hasXSignature: html.includes('X-SIGNATURE'),
      hasXTimestamp: html.includes('X-TIMESTAMP')
    };
  }`
  })
// Result: All true → Private endpoint HAS auth headers
```

**Solution**: Classification logic should check for auth headers, not text
searches.

## Best Practices

1. **Use evaluate_script over snapshots** - More efficient, faster, targeted
2. **Return structured data** - Makes results easier to analyze
3. **Check multiple examples** - Test both public/private, different sections
4. **Look at actual HTML** - Don't assume structure, verify it
5. **Test incrementally** - Start with simple checks, then go deeper
6. **Document findings** - Record patterns for future reference

## Version History

- **v1.0** (2025-01-02): Initial version based on Backpack Exchange integration
  learnings
