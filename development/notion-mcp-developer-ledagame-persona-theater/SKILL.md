---
name: notion-mcp-developer
description: Develop Notion templates and databases using Notion MCP tools in Claude Code. Orchestrates escape room design skills (narrative-architect, puzzle-designer, formula-master, localizer, playtester) and implements their output via Notion MCP API. Use when creating Notion templates, building databases, implementing game mechanics, or managing complex multi-step Notion development workflows. Handles rate limits, session persistence via Serena MCP, and iterative development cycles.
---

# Notion MCP Developer

## Overview

Transform escape room designs into fully functional Notion templates using Notion MCP tools integrated with Claude Code. This skill orchestrates specialized design skills and implements their output through Notion's API while managing rate limits, session persistence, and iterative development workflows.

## Table of Contents

### Quick Start
- [Core Capabilities](#core-capabilities)
- [Notion MCP Tool Reference](#notion-mcp-tool-reference)

### Best Practices & Patterns
- [Security Best Practices](#security-best-practices)
- [Error Handling Patterns](#error-handling-patterns)

### Workflows & Guides
- [Primary Workflows](#primary-workflows)

### Reference Documentation
Detailed guides for escape room development:
- **[Escape Room Database Architecture](references/escape-room-database-architecture.md)** - Complete 5-database structure (Scenes, Puzzles, Items, PlayerState, Endings) with property schemas and relationships
- **[Game Mechanics Formulas](references/game-mechanics-formulas.md)** - 20+ formula patterns across 5 categories (Unlocking Logic, Progress Tracking, Hint Systems, Timer Systems, Ending Triggers)
- **[Rollup Patterns](references/rollup-patterns.md)** - All 21 Notion rollup functions with escape room examples
- **[Relation Design Patterns](references/relation-design-patterns.md)** - 4 relation types (Single Property, Dual Property, Self-Referencing, Many-to-Many) with implementation guides
- **[Phase-Based Implementation](references/phase-based-implementation.md)** - 5-phase creation strategy optimized from 23 to 11 API calls
- **[Antipatterns & Gotchas](references/antipatterns-and-gotchas.md)** - 6 antipatterns + 6 gotchas with solutions

---

## Core Capabilities

### 1. Template Creation from Scratch
Build complete Notion templates for escape rooms, time tracking, project management, or custom workflows.

### 2. Skill Orchestration
Coordinate existing skills (narrative-architect-korean-style, language-agnostic-puzzle-designer, notion-formula-master, escape-room-localizer, playtesting-orchestrator) and implement their outputs in Notion.

### 3. Database Architecture
Design and implement complex database structures with proper relationships, formulas, rollups, and views using `notion-create-database` and `notion-update-database`.

**Related References**:
- [Escape Room Database Architecture](references/escape-room-database-architecture.md) - Complete database structure patterns
- [Relation Design Patterns](references/relation-design-patterns.md) - How to connect databases
- [Rollup Patterns](references/rollup-patterns.md) - Aggregate data across relations
- [Phase-Based Implementation](references/phase-based-implementation.md) - Optimal creation order

### 4. Content Management
Create, fetch, update, and search Notion content using all Notion MCP tools: `notion-create-pages`, `notion-fetch`, `notion-update-page`, `notion-search`, `notion-move-pages`, `notion-duplicate-page`.

### 5. Rate Limit Management
Intelligently batch operations to respect Notion API limits (180 requests/min general, 30 searches/min).

### 6. Session Persistence
Use Serena MCP to save/load development context for complex multi-step builds spanning multiple sessions.

## Notion MCP Tool Reference

### Essential Tools

**notion-search** (Rate limit: 30/min)
- Search across Notion workspace and connected tools (Slack, Google Drive, Jira)
- Use for finding existing content, templates, or research documents
- Syntax: `query`, optional `teamspace_id`, `page_url`, `data_source_url`, `filters`

**notion-fetch** (Rate limit: 180/min)
- Retrieve complete page or database content by URL/ID
- Returns Notion-flavored Markdown for pages, schema for databases
- Use before modifying content to understand current structure

**notion-create-database** (Rate limit: 180/min)
- Create new database with property schema
- Returns database ID and initial view
- Follow with `notion-update-database` for advanced configuration

**notion-create-pages** (Rate limit: 180/min)
- Bulk create up to 100 pages in single call
- Specify parent (page_id, database_id, or data_source_id)
- Use Notion-flavored Markdown for content

**notion-update-page** (Rate limit: 180/min)
- Update page properties or content
- Commands: `update_properties`, `replace_content`, `replace_content_range`, `insert_content_after`
- Always fetch page first to get current content

**notion-update-database** (Rate limit: 180/min)
- Modify database schema, add/remove/rename properties
- Update title, description, inline display mode
- Cannot delete title properties or create multiple unique_id properties

See [references/notion-mcp-tools.md](references/notion-mcp-tools.md) for complete API reference with examples.

## Security Best Practices

### 1. Prompt Injection Defense

**Threat**: User-provided content in formulas or rich text could inject malicious logic into Notion pages.

#### Validation Rules

**Formula Input Sanitization**:
```javascript
// ❌ Dangerous: Direct formula from user input
const userFormula = userInput; // Could be: if(true, deleteAllPages(), "safe")
notion_create_database({
  properties: {
    "Calculated": {formula: {expression: userFormula}} // INJECTION RISK
  }
});

// ✅ Safe: Whitelist validation
function validateFormula(formula: string): boolean {
  const allowedFunctions = ['if', 'prop', 'and', 'or', 'format', 'round'];
  const forbiddenPatterns = [
    /delete/i,      // No destructive operations
    /fetch/i,       // No external calls
    /eval/i,        // No code execution
    /<script>/i     // No HTML injection
  ];

  // Check allowed functions only
  const functions = formula.match(/\w+\(/g) || [];
  const allAllowed = functions.every(f =>
    allowedFunctions.includes(f.replace('(', ''))
  );

  // Check no forbidden patterns
  const noForbidden = !forbiddenPatterns.some(p => p.test(formula));

  return allAllowed && noForbidden;
}

// Usage
if (validateFormula(userFormula)) {
  notion_create_database({...});
} else {
  throw new Error("Invalid formula: contains disallowed operations");
}
```

**Rich Text Content Sanitization**:
```javascript
// ❌ Dangerous: Direct HTML/Markdown from user
const userContent = userInput; // Could contain: <script>alert('xss')</script>

// ✅ Safe: Strip dangerous tags
function sanitizeContent(content: string): string {
  return content
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '') // Remove <script>
    .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, '') // Remove <iframe>
    .replace(/javascript:/gi, '')  // Remove javascript: URLs
    .replace(/on\w+\s*=/gi, '');   // Remove event handlers (onclick, onerror, etc.)
}

// Usage
notion_create_pages({
  pages: [{
    properties: {title: "User Content"},
    content: sanitizeContent(userContent)
  }]
});
```

#### Formula Validation Checklist

```
Before creating database with formulas:
- [ ] Formulas use only whitelisted functions?
- [ ] No external data fetching (fetch, http)?
- [ ] No user-controllable function names?
- [ ] Validated against forbidden patterns?
- [ ] Tested with malicious inputs?
```

---

### 2. Permission Validation

**Threat**: Operations performed without verifying user has necessary permissions.

#### Pre-Operation Checks

**Verify Bot Permissions**:
```javascript
// Always check bot permissions before operations
async function verifyBotPermissions(): Promise<void> {
  const bot = await notion_get_self();

  if (bot.bot.owner.type !== "workspace") {
    throw new Error("❌ Bot must be workspace-level integration for this operation");
  }

  console.log(`✅ Operating as: ${bot.name} (workspace-level)`);
}

// Usage before critical operations
await verifyBotPermissions();
await notion_create_database({...}); // Now safe
```

**Verify Team Access**:
```javascript
// Check user can access target teamspace
async function verifyTeamAccess(teamName: string): Promise<string> {
  const teams = await notion_get_teams({query: teamName});

  const team = teams.user_teams.find(t => t.name === teamName);

  if (!team) {
    throw new Error(`❌ No access to team: ${teamName}`);
  }

  if (team.role === "guest") {
    throw new Error(`❌ Insufficient permissions (guest only) for: ${teamName}`);
  }

  console.log(`✅ Access confirmed: ${teamName} (role: ${team.role})`);
  return team.id;
}

// Usage
const teamId = await verifyTeamAccess("Game Design Team");
await notion_create_database({
  parent: {teamspace_id: teamId},
  // ...
});
```

**Database Permission Check**:
```javascript
// Verify can modify database before updates
async function verifyDatabaseAccess(databaseId: string): Promise<void> {
  try {
    const db = await notion_fetch({id: databaseId});

    // If fetch succeeds, we have read access
    // Try a harmless update to verify write access
    await notion_update_database({
      database_id: databaseId,
      // No actual changes (empty properties update)
      properties: {}
    });

    console.log(`✅ Write access confirmed for database: ${databaseId}`);
  } catch (error) {
    throw new Error(`❌ Cannot modify database: ${error.message}`);
  }
}
```

#### Permission Checklist

```
Before operations:
- [ ] Verified bot is workspace-level integration?
- [ ] Checked team access if team-specific?
- [ ] Confirmed user has write permissions?
- [ ] Validated operation scope (read vs. write)?
```

---

### 3. Endpoint Validation

**Threat**: Operating on invalid or malicious page/database IDs.

#### ID Validation

**UUID Format Validation**:
```javascript
// Validate Notion UUID format
function isValidNotionId(id: string): boolean {
  // Notion IDs are UUIDv4 (with or without dashes)
  const uuidRegex = /^[0-9a-f]{8}-?[0-9a-f]{4}-?4[0-9a-f]{3}-?[89ab][0-9a-f]{3}-?[0-9a-f]{12}$/i;
  const noDashRegex = /^[0-9a-f]{32}$/i;

  return uuidRegex.test(id) || noDashRegex.test(id);
}

// Usage
if (!isValidNotionId(pageId)) {
  throw new Error(`❌ Invalid Notion ID format: ${pageId}`);
}

await notion_fetch({id: pageId}); // Now safe
```

**Existence Verification**:
```javascript
// Verify page/database exists before operations
async function verifyExists(id: string, type: "page" | "database"): Promise<void> {
  try {
    const entity = await notion_fetch({id});

    if (type === "database" && !entity.properties) {
      throw new Error(`Entity ${id} is not a database`);
    }

    console.log(`✅ ${type} exists: ${id}`);
  } catch (error) {
    throw new Error(`❌ ${type} not found or no access: ${id}`);
  }
}

// Usage
await verifyExists(databaseId, "database");
await notion_update_database({database_id: databaseId, ...}); // Now safe
```

**URL Parsing Validation**:
```javascript
// Extract and validate ID from Notion URL
function extractNotionId(urlOrId: string): string {
  // If already an ID, validate and return
  if (isValidNotionId(urlOrId)) {
    return urlOrId;
  }

  // If URL, extract ID
  const urlMatch = urlOrId.match(/([0-9a-f]{32}|[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})/i);

  if (!urlMatch) {
    throw new Error(`❌ Cannot extract valid ID from: ${urlOrId}`);
  }

  return urlMatch[1];
}

// Usage
const cleanId = extractNotionId(userInput); // Handles URLs or IDs
await notion_fetch({id: cleanId});
```

#### Endpoint Checklist

```
Before operations:
- [ ] Validated ID format (UUID)?
- [ ] Verified entity exists?
- [ ] Confirmed entity type (page vs. database)?
- [ ] Extracted ID from URL correctly?
```

---

### 4. Human Confirmation for Destructive Actions

**Threat**: Accidental data loss from bulk deletes, moves, or irreversible changes.

#### Confirmation Patterns

**Batch Operations (>10 items)**:
```javascript
// Require confirmation for batch operations
async function batchMovePagesWithConfirmation(
  pageIds: string[],
  targetParentId: string
): Promise<void> {
  if (pageIds.length > 10) {
    console.log(`⚠️  About to move ${pageIds.length} pages to ${targetParentId}`);
    console.log(`Pages: ${pageIds.slice(0, 5).join(', ')}...`);

    // ASK USER: "Proceed with moving 50 pages? (yes/no)"
    const userConfirmed = await askUser(`Proceed with moving ${pageIds.length} pages?`);

    if (!userConfirmed) {
      throw new Error("❌ Operation cancelled by user");
    }
  }

  await notion_move_pages({
    page_or_database_ids: pageIds,
    new_parent: {page_id: targetParentId}
  });

  console.log(`✅ Moved ${pageIds.length} pages successfully`);
}
```

**Trash Operations**:
```javascript
// Require explicit confirmation for moving to trash
async function moveDatabaseToTrashWithConfirmation(databaseId: string): Promise<void> {
  const db = await notion_fetch({id: databaseId});

  console.log(`⚠️  WARNING: Moving database to trash`);
  console.log(`Database: ${db.title}`);
  console.log(`This action CANNOT be undone via API`);

  // ASK USER: "Are you SURE? Type database name to confirm:"
  const userInput = await askUser("Type database name to confirm:");

  if (userInput !== db.title) {
    throw new Error("❌ Confirmation failed: name mismatch");
  }

  await notion_update_database({
    database_id: databaseId,
    in_trash: true
  });

  console.log(`✅ Database moved to trash: ${databaseId}`);
}
```

**Destructive Updates**:
```javascript
// Warn before removing database properties
async function removePropertyWithWarning(
  databaseId: string,
  propertyName: string
): Promise<void> {
  console.log(`⚠️  About to remove property: "${propertyName}"`);
  console.log(`This will DELETE all data in this column`);

  const confirmed = await askUser("Confirm removal? (yes/no)");

  if (!confirmed) {
    throw new Error("❌ Operation cancelled");
  }

  await notion_update_database({
    database_id: databaseId,
    properties: {
      [propertyName]: null // Remove property
    }
  });

  console.log(`✅ Property removed: ${propertyName}`);
}
```

#### Confirmation Checklist

```
Require human confirmation for:
- [ ] Batch operations (>10 items)
- [ ] Moving to trash
- [ ] Removing database properties
- [ ] Bulk content replacement
- [ ] Irreversible changes
```

---

## Error Handling Patterns

Comprehensive error handling strategies for robust Notion MCP operations. Covers retry logic, rate limits, timeouts, partial failures, and recovery patterns.

---

### 1. Retry Logic with Exponential Backoff

**Use Case**: Handle transient network errors, temporary Notion API unavailability, or 5xx server errors.

**Pattern**: Exponential backoff with jitter to avoid thundering herd problem.

```javascript
async function retryWithBackoff<T>(
  operation: () => Promise<T>,
  options: {
    maxRetries?: number;
    initialDelayMs?: number;
    maxDelayMs?: number;
    backoffMultiplier?: number;
  } = {}
): Promise<T> {
  const {
    maxRetries = 3,
    initialDelayMs = 1000,
    maxDelayMs = 10000,
    backoffMultiplier = 2
  } = options;

  let lastError: Error;
  let delayMs = initialDelayMs;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error;

      // Don't retry on 4xx errors (client errors)
      if (error.status >= 400 && error.status < 500) {
        throw error;
      }

      // Last attempt, throw error
      if (attempt === maxRetries) {
        throw new Error(
          `❌ Operation failed after ${maxRetries + 1} attempts: ${error.message}`
        );
      }

      // Calculate delay with jitter (±25%)
      const jitter = delayMs * 0.25 * (Math.random() * 2 - 1);
      const actualDelay = Math.min(delayMs + jitter, maxDelayMs);

      console.log(
        `⚠️  Attempt ${attempt + 1}/${maxRetries + 1} failed. Retrying in ${Math.round(actualDelay)}ms...`
      );

      await new Promise(resolve => setTimeout(resolve, actualDelay));

      // Exponential backoff
      delayMs = Math.min(delayMs * backoffMultiplier, maxDelayMs);
    }
  }

  throw lastError!;
}
```

**Usage Example**:
```javascript
// Retry notion-fetch with exponential backoff
const page = await retryWithBackoff(
  () => notion_fetch({id: "page-id"}),
  {maxRetries: 3, initialDelayMs: 1000}
);
```

**Retry Decision Matrix**:
```
Error Type                 | Retry? | Max Attempts | Backoff
---------------------------|--------|--------------|----------
5xx (Server Error)         | ✅ Yes | 3            | Exponential
429 (Rate Limit)           | ✅ Yes | 5            | Use Retry-After header
Network Timeout            | ✅ Yes | 3            | Exponential
Connection Refused         | ✅ Yes | 2            | Linear
400 (Bad Request)          | ❌ No  | 0            | N/A
401 (Unauthorized)         | ❌ No  | 0            | N/A
404 (Not Found)            | ❌ No  | 0            | N/A
409 (Conflict)             | ⚠️  Maybe | 1         | Short delay
```

---

### 2. Timeout Handling

**Use Case**: Prevent hanging operations, especially for long-running API calls like `notion-duplicate-page` or bulk operations.

**Pattern**: Implement configurable timeouts with graceful degradation.

```javascript
async function withTimeout<T>(
  operation: Promise<T>,
  timeoutMs: number,
  operationName: string
): Promise<T> {
  const timeoutPromise = new Promise<never>((_, reject) => {
    setTimeout(() => {
      reject(new Error(`❌ ${operationName} timed out after ${timeoutMs}ms`));
    }, timeoutMs);
  });

  try {
    return await Promise.race([operation, timeoutPromise]);
  } catch (error) {
    if (error.message.includes('timed out')) {
      console.log(`⚠️  Timeout occurred for: ${operationName}`);
      // Log for monitoring/alerting
      // Could also attempt cleanup here
    }
    throw error;
  }
}
```

**Usage Example**:
```javascript
// Set 30-second timeout for duplicate operation
const duplicated = await withTimeout(
  notion_duplicate_page({page_id: "template-id"}),
  30000,
  "notion-duplicate-page"
);
```

**Recommended Timeouts by Operation**:
```javascript
const TIMEOUTS = {
  'notion-search': 10000,           // 10s (search can be slow)
  'notion-fetch': 5000,             // 5s (single page)
  'notion-create-database': 15000,  // 15s (schema creation)
  'notion-create-pages': 20000,     // 20s (batch creation)
  'notion-update-page': 10000,      // 10s (content update)
  'notion-update-database': 15000,  // 15s (schema update)
  'notion-duplicate-page': 30000,   // 30s (async operation)
  'notion-move-pages': 20000,       // 20s (bulk operation)
  'bulk-operations': 60000          // 60s (large batches)
};
```

**Timeout Pattern with Partial Success**:
```javascript
async function batchCreateWithTimeout(
  pages: any[],
  batchSize: number = 100,
  timeoutPerBatchMs: number = 20000
): Promise<{successful: any[], failed: any[]}> {
  const successful: any[] = [];
  const failed: any[] = [];

  for (let i = 0; i < pages.length; i += batchSize) {
    const batch = pages.slice(i, i + batchSize);

    try {
      const result = await withTimeout(
        notion_create_pages({pages: batch}),
        timeoutPerBatchMs,
        `Batch ${Math.floor(i / batchSize) + 1}`
      );

      successful.push(...result.results);
    } catch (error) {
      console.log(`❌ Batch ${Math.floor(i / batchSize) + 1} failed: ${error.message}`);
      failed.push(...batch);
    }
  }

  return {successful, failed};
}
```

---

### 3. Rate Limit Error Recovery

**Use Case**: Handle Notion API rate limits (180 requests/min general, 30 requests/min for searches).

**Pattern**: Respect `Retry-After` header and implement adaptive rate limiting.

```javascript
class RateLimitHandler {
  private requestCount: number = 0;
  private windowStartMs: number = Date.now();
  private readonly windowMs: number = 60000; // 1 minute
  private readonly maxRequests: number = 170; // Leave 10 request buffer

  async throttle(): Promise<void> {
    const now = Date.now();
    const elapsed = now - this.windowStartMs;

    // Reset window if expired
    if (elapsed >= this.windowMs) {
      this.requestCount = 0;
      this.windowStartMs = now;
      return;
    }

    // Check if approaching limit
    if (this.requestCount >= this.maxRequests) {
      const waitMs = this.windowMs - elapsed;
      console.log(`⚠️  Rate limit approaching. Waiting ${waitMs}ms...`);
      await new Promise(resolve => setTimeout(resolve, waitMs));

      // Reset after waiting
      this.requestCount = 0;
      this.windowStartMs = Date.now();
    }

    this.requestCount++;
  }

  async handleRateLimitError(error: any): Promise<void> {
    if (error.status === 429) {
      // Use Retry-After header if available
      const retryAfterSeconds = error.headers?.['retry-after'];
      const waitMs = retryAfterSeconds
        ? parseInt(retryAfterSeconds) * 1000
        : 60000; // Default 60s

      console.log(`⚠️  Rate limit hit (429). Waiting ${waitMs}ms before retry...`);

      await new Promise(resolve => setTimeout(resolve, waitMs));

      // Reset counter after waiting
      this.requestCount = 0;
      this.windowStartMs = Date.now();
    }
  }
}

// Usage
const rateLimiter = new RateLimitHandler();

async function notionApiCall(operation: () => Promise<any>): Promise<any> {
  await rateLimiter.throttle();

  try {
    return await operation();
  } catch (error) {
    if (error.status === 429) {
      await rateLimiter.handleRateLimitError(error);
      // Retry once after rate limit wait
      return await operation();
    }
    throw error;
  }
}
```

**Adaptive Rate Limiting for Search Operations** (30/min limit):
```javascript
class SearchRateLimiter {
  private searchCount: number = 0;
  private searchWindowStart: number = Date.now();
  private readonly searchLimit: number = 25; // Buffer of 5

  async throttleSearch(): Promise<void> {
    const now = Date.now();
    const elapsed = now - this.searchWindowStart;

    if (elapsed >= 60000) {
      this.searchCount = 0;
      this.searchWindowStart = now;
      return;
    }

    if (this.searchCount >= this.searchLimit) {
      const waitMs = 60000 - elapsed;
      console.log(`⚠️  Search rate limit approaching. Waiting ${waitMs}ms...`);
      await new Promise(resolve => setTimeout(resolve, waitMs));

      this.searchCount = 0;
      this.searchWindowStart = Date.now();
    }

    this.searchCount++;
  }
}
```

---

### 4. Partial Failure Handling in Bulk Operations

**Use Case**: Handle scenarios where only some items in a batch operation fail (e.g., creating 100 pages but 5 fail).

**Pattern**: Continue-on-error with detailed failure reporting.

```javascript
interface BatchResult<T> {
  successful: T[];
  failed: Array<{item: any; error: Error}>;
  summary: {
    total: number;
    succeeded: number;
    failed: number;
    successRate: number;
  };
}

async function batchCreatePagesWithPartialFailure(
  pages: any[],
  options: {
    continueOnError?: boolean;
    batchSize?: number;
  } = {}
): Promise<BatchResult<any>> {
  const {continueOnError = true, batchSize = 100} = options;

  const successful: any[] = [];
  const failed: Array<{item: any; error: Error}> = [];

  for (let i = 0; i < pages.length; i += batchSize) {
    const batch = pages.slice(i, i + batchSize);

    try {
      const result = await notion_create_pages({pages: batch});
      successful.push(...result.results);

      console.log(`✅ Batch ${Math.floor(i / batchSize) + 1}: ${result.results.length} pages created`);
    } catch (error) {
      console.log(`❌ Batch ${Math.floor(i / batchSize) + 1} failed: ${error.message}`);

      if (continueOnError) {
        // Record failures and continue
        batch.forEach(item => {
          failed.push({item, error});
        });
      } else {
        // Stop on first error
        throw new Error(
          `Batch operation failed at batch ${Math.floor(i / batchSize) + 1}. ` +
          `Completed: ${successful.length}/${pages.length}. ` +
          `Error: ${error.message}`
        );
      }
    }
  }

  const summary = {
    total: pages.length,
    succeeded: successful.length,
    failed: failed.length,
    successRate: (successful.length / pages.length) * 100
  };

  return {successful, failed, summary};
}
```

**Usage with Retry for Failed Items**:
```javascript
async function createPagesWithRetry(
  pages: any[],
  maxRetries: number = 2
): Promise<BatchResult<any>> {
  let result = await batchCreatePagesWithPartialFailure(pages);

  // Retry failed items
  for (let retry = 0; retry < maxRetries && result.failed.length > 0; retry++) {
    console.log(
      `\n⚠️  Retry ${retry + 1}/${maxRetries}: Retrying ${result.failed.length} failed items...`
    );

    const failedPages = result.failed.map(f => f.item);
    const retryResult = await batchCreatePagesWithPartialFailure(failedPages);

    // Update results
    result.successful.push(...retryResult.successful);
    result.failed = retryResult.failed;

    // Update summary
    result.summary = {
      total: pages.length,
      succeeded: result.successful.length,
      failed: result.failed.length,
      successRate: (result.successful.length / pages.length) * 100
    };
  }

  // Final report
  console.log(`\n📊 Final Results:`);
  console.log(`   Total: ${result.summary.total}`);
  console.log(`   ✅ Succeeded: ${result.summary.succeeded}`);
  console.log(`   ❌ Failed: ${result.summary.failed}`);
  console.log(`   📈 Success Rate: ${result.summary.successRate.toFixed(1)}%`);

  return result;
}
```

**Granular Failure Handling** (Item-by-item):
```javascript
async function createPagesIndividually(
  pages: any[]
): Promise<BatchResult<any>> {
  const successful: any[] = [];
  const failed: Array<{item: any; error: Error}> = [];

  for (let i = 0; i < pages.length; i++) {
    const page = pages[i];

    try {
      const result = await notion_create_pages({pages: [page]});
      successful.push(result.results[0]);

      if ((i + 1) % 10 === 0) {
        console.log(`✅ Progress: ${i + 1}/${pages.length} pages processed`);
      }
    } catch (error) {
      console.log(`❌ Failed to create page ${i + 1}: ${error.message}`);
      failed.push({item: page, error});
    }
  }

  const summary = {
    total: pages.length,
    succeeded: successful.length,
    failed: failed.length,
    successRate: (successful.length / pages.length) * 100
  };

  return {successful, failed, summary};
}
```

---

### 5. Network Error Patterns

**Use Case**: Handle network connectivity issues, DNS failures, connection timeouts, and SSL errors.

**Pattern**: Differentiate between retryable and non-retryable network errors.

```javascript
interface NetworkError extends Error {
  code?: string;
  errno?: number;
}

function isRetryableNetworkError(error: NetworkError): boolean {
  // Retryable network error codes
  const retryableCodes = [
    'ETIMEDOUT',      // Connection timeout
    'ECONNRESET',     // Connection reset by peer
    'ECONNREFUSED',   // Connection refused (server down)
    'EPIPE',          // Broken pipe
    'ENOTFOUND',      // DNS lookup failed (temporary)
    'EAI_AGAIN',      // DNS lookup timeout
    'ENETUNREACH',    // Network unreachable
    'EHOSTUNREACH'    // Host unreachable
  ];

  return retryableCodes.includes(error.code || '');
}

function isNonRetryableNetworkError(error: NetworkError): boolean {
  // Non-retryable errors (configuration/permanent issues)
  const nonRetryableCodes = [
    'ENOTFOUND',      // DNS lookup failed (if persistent)
    'EPROTO',         // Protocol error (SSL/TLS)
    'CERT_HAS_EXPIRED', // SSL certificate expired
    'UNABLE_TO_VERIFY_LEAF_SIGNATURE' // SSL verification failed
  ];

  // If error persists for >3 attempts, consider ENOTFOUND non-retryable
  return nonRetryableCodes.includes(error.code || '');
}

async function handleNetworkError(
  operation: () => Promise<any>,
  maxRetries: number = 3
): Promise<any> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      const networkError = error as NetworkError;

      // Non-retryable errors
      if (isNonRetryableNetworkError(networkError)) {
        console.log(`❌ Non-retryable network error: ${networkError.code}`);
        throw new Error(
          `Network configuration error: ${networkError.code}. ` +
          `Check DNS, SSL certificates, and network connectivity.`
        );
      }

      // Retryable errors
      if (isRetryableNetworkError(networkError)) {
        if (attempt === maxRetries) {
          throw new Error(
            `❌ Network error persisted after ${maxRetries + 1} attempts: ${networkError.code}`
          );
        }

        const delayMs = Math.min(1000 * Math.pow(2, attempt), 10000);
        console.log(
          `⚠️  Network error (${networkError.code}). Retry ${attempt + 1}/${maxRetries} in ${delayMs}ms...`
        );

        await new Promise(resolve => setTimeout(resolve, delayMs));
        continue;
      }

      // Unknown error, rethrow
      throw error;
    }
  }
}
```

**Network Health Check**:
```javascript
async function checkNetworkHealth(): Promise<{
  healthy: boolean;
  latencyMs: number;
  error?: string;
}> {
  const startMs = Date.now();

  try {
    // Ping Notion API with lightweight request
    await notion_get_self();

    const latencyMs = Date.now() - startMs;

    return {
      healthy: true,
      latencyMs
    };
  } catch (error) {
    return {
      healthy: false,
      latencyMs: Date.now() - startMs,
      error: error.message
    };
  }
}

// Usage: Pre-flight check before bulk operations
async function performBulkOperationWithHealthCheck(
  operation: () => Promise<any>
): Promise<any> {
  const health = await checkNetworkHealth();

  if (!health.healthy) {
    throw new Error(
      `❌ Network health check failed: ${health.error}. ` +
      `Cannot proceed with bulk operation.`
    );
  }

  if (health.latencyMs > 5000) {
    console.log(
      `⚠️  High network latency detected (${health.latencyMs}ms). ` +
      `Operation may be slow.`
    );
  }

  return await operation();
}
```

---

### 6. 4xx vs 5xx Error Handling Strategies

**Use Case**: Differentiate between client errors (4xx, user's fault) and server errors (5xx, Notion's fault).

**Pattern**: Log and fix for 4xx, retry for 5xx.

```javascript
interface ApiError extends Error {
  status: number;
  code?: string;
  details?: any;
}

function handleApiError(error: ApiError, context: string): never {
  // 4xx: Client Errors (User/Configuration Issue)
  if (error.status >= 400 && error.status < 500) {
    switch (error.status) {
      case 400:
        throw new Error(
          `❌ Bad Request in ${context}: ${error.message}\n` +
          `Fix: Verify request parameters, property names, and data types.\n` +
          `Details: ${JSON.stringify(error.details, null, 2)}`
        );

      case 401:
        throw new Error(
          `❌ Unauthorized in ${context}: ${error.message}\n` +
          `Fix: Check Notion integration token and permissions.\n` +
          `Run: await verifyBotPermissions()`
        );

      case 403:
        throw new Error(
          `❌ Forbidden in ${context}: ${error.message}\n` +
          `Fix: Bot lacks permission to access this resource.\n` +
          `Check: Team membership and database sharing settings.`
        );

      case 404:
        throw new Error(
          `❌ Not Found in ${context}: ${error.message}\n` +
          `Fix: Verify page/database ID exists and bot has access.\n` +
          `Try: await notion_search({query: "resource name"})`
        );

      case 409:
        throw new Error(
          `❌ Conflict in ${context}: ${error.message}\n` +
          `Fix: Resource was modified concurrently. Retry with latest version.\n` +
          `Strategy: Fetch latest → Merge changes → Retry update`
        );

      case 429:
        throw new Error(
          `❌ Rate Limit Exceeded in ${context}\n` +
          `Fix: Reduce request frequency or wait before retry.\n` +
          `Current Limits: 180 req/min (general), 30 req/min (search)`
        );

      default:
        throw new Error(
          `❌ Client Error ${error.status} in ${context}: ${error.message}`
        );
    }
  }

  // 5xx: Server Errors (Notion API Issue - Retry)
  if (error.status >= 500 && error.status < 600) {
    switch (error.status) {
      case 500:
        console.log(`⚠️  Internal Server Error in ${context}. Retryable.`);
        break;

      case 502:
        console.log(`⚠️  Bad Gateway in ${context}. Retryable.`);
        break;

      case 503:
        console.log(`⚠️  Service Unavailable in ${context}. Retryable.`);
        break;

      case 504:
        console.log(`⚠️  Gateway Timeout in ${context}. Retryable.`);
        break;
    }

    throw error; // Let retry handler catch it
  }

  // Unknown error
  throw error;
}
```

**Comprehensive API Call Wrapper**:
```javascript
async function safeNotionApiCall<T>(
  operation: () => Promise<T>,
  context: string,
  options: {
    maxRetries?: number;
    timeoutMs?: number;
  } = {}
): Promise<T> {
  const {maxRetries = 3, timeoutMs = 10000} = options;

  try {
    // Add timeout
    const result = await withTimeout(operation(), timeoutMs, context);
    return result;
  } catch (error) {
    const apiError = error as ApiError;

    // Handle 4xx (don't retry)
    if (apiError.status >= 400 && apiError.status < 500) {
      handleApiError(apiError, context);
    }

    // Handle 5xx (retry)
    if (apiError.status >= 500 && apiError.status < 600) {
      console.log(`⚠️  Server error in ${context}. Will retry...`);

      return await retryWithBackoff(
        operation,
        {maxRetries, initialDelayMs: 2000}
      );
    }

    // Handle network errors
    if (apiError.code && isRetryableNetworkError(apiError as NetworkError)) {
      console.log(`⚠️  Network error in ${context}. Will retry...`);

      return await handleNetworkError(operation, maxRetries);
    }

    // Unknown error, rethrow
    throw error;
  }
}
```

**Usage Example**:
```javascript
// Wrap all Notion API calls
const scenes = await safeNotionApiCall(
  () => notion_create_database({
    title: [{text: {content: "Scenes"}}],
    properties: {...}
  }),
  "create-scenes-database",
  {maxRetries: 3, timeoutMs: 15000}
);
```

---

### 7. Error Recovery Checklist

Use this checklist before deploying bulk operations or critical workflows:

```
Error Handling Verification:
- [ ] Retry logic implemented for 5xx errors
- [ ] Exponential backoff with jitter configured
- [ ] Timeout configured for each operation type
- [ ] Rate limit handling implemented (180/min general, 30/min search)
- [ ] Partial failure handling for batch operations
- [ ] Network error detection and retry
- [ ] 4xx errors logged with fix instructions
- [ ] Human confirmation for destructive operations
- [ ] Pre-flight network health check
- [ ] Detailed error logging with context
- [ ] Rollback plan for failed operations
- [ ] Monitoring/alerting for repeated failures
```

**Error Handling Test Plan**:
```javascript
// Test error scenarios
async function testErrorHandling() {
  console.log("🧪 Testing Error Handling...\n");

  // Test 1: Invalid page ID (404)
  try {
    await notion_fetch({id: "invalid-id"});
  } catch (error) {
    console.log("✅ Test 1 (404 handling): Passed");
  }

  // Test 2: Rate limit simulation
  // (Make 200 requests rapidly to trigger 429)

  // Test 3: Timeout handling
  try {
    await withTimeout(
      new Promise(resolve => setTimeout(resolve, 10000)),
      1000,
      "test-operation"
    );
  } catch (error) {
    console.log("✅ Test 3 (timeout): Passed");
  }

  // Test 4: Partial batch failure
  const result = await batchCreatePagesWithPartialFailure([
    {properties: {Title: "Valid"}},
    {properties: {}}, // Invalid: missing title
    {properties: {Title: "Valid 2"}}
  ]);

  console.log(`✅ Test 4 (partial failure): ${result.summary.succeeded}/3 succeeded`);
}
```

---

**Summary**: Error handling is critical for production Notion integrations. Always implement:
1. Retry with exponential backoff for transient errors
2. Timeouts to prevent hanging operations
3. Rate limit awareness and adaptive throttling
4. Partial failure handling with detailed reporting
5. Network error differentiation and recovery
6. 4xx logging (fix) vs 5xx retry strategy
7. Pre-deployment error handling verification

---

## Primary Workflows

### Workflow 1: Create Escape Room Template from Design

**Use Case**: "Design and implement a murder mystery escape room in Notion"

**Process**:

Copy this checklist:
```
Notion Escape Room Build:
- [ ] Step 1: Design narrative (narrative-architect-korean-style)
- [ ] Step 2: Create puzzle inventory (language-agnostic-puzzle-designer)
- [ ] Step 3: Plan database architecture (notion-formula-master)
- [ ] Step 4: Save session context (Serena MCP)
- [ ] Step 5: Create databases via Notion MCP
- [ ] Step 6: Implement formulas and relationships
- [ ] Step 7: Create initial content pages
- [ ] Step 8: Add localization (escape-room-localizer)
- [ ] Step 9: Self-test and iterate
- [ ] Step 10: Save final session context
```

**Step 1: Design Narrative**
Invoke `narrative-architect-korean-style` skill to create:
- 3-act story structure
- Character profiles
- Multiple endings
- Emotional beat mapping

**Step 2: Create Puzzle Inventory**
Invoke `language-agnostic-puzzle-designer` skill to create:
- 12-18 puzzles (visual/logic mix)
- Difficulty progression
- Hint system (3 levels per puzzle)

**Step 3: Plan Database Architecture**
Invoke `notion-formula-master` skill to design:
- Scenes database (story progression)
- Items database (inventory)
- Puzzles database (challenges)
- PlayerState database (progress tracking)
- Endings database (multiple conclusions)

**Reference Guides**: Before implementation, review:
- **[Escape Room Database Architecture](references/escape-room-database-architecture.md)** - Complete 5-database structure with all properties
- **[Relation Design Patterns](references/relation-design-patterns.md)** - How to connect databases (Scenes ↔ Puzzles, etc.)
- **[Game Mechanics Formulas](references/game-mechanics-formulas.md)** - Unlocking logic, progress tracking, hint systems
- **[Phase-Based Implementation](references/phase-based-implementation.md)** - Optimal API call order (11 calls vs 23)
- **[Antipatterns & Gotchas](references/antipatterns-and-gotchas.md)** - Common mistakes to avoid

**Step 4: Save Session Context**
```bash
# Use Serena MCP to save design outputs
# Invoke: /sc:save --context "escape-room-design-phase"
```

**Step 5: Create Databases**
Use `mcp__notion__notion-create-database` for each database:

```javascript
// Example: Create Scenes database
{
  "title": [{"text": {"content": "Scenes"}}],
  "properties": {
    "Scene ID": {"title": {}},
    "Description": {"rich_text": {}},
    "Unlocked": {"checkbox": {}},
    "Order": {"number": {"format": "number"}},
    "Act": {"select": {"options": [
      {"name": "Act 1", "color": "blue"},
      {"name": "Act 2", "color": "yellow"},
      {"name": "Act 3", "color": "green"}
    ]}},
    "Previous Scene": {"relation": {"data_source_id": "<scenes-db-id>", "type": "single_property"}}
  }
}
```

**Rate Limit Strategy**: Create databases sequentially (5 databases = 5 requests, well under 180/min limit).

**Step 6: Implement Formulas and Rollups**
Use `mcp__notion__notion-update-database` to add formula properties and rollups:

```javascript
// Example 1: Scene unlock condition formula
{
  "database_id": "<scenes-db-id>",
  "properties": {
    "Unlock Condition": {
      "formula": {
        "expression": "if(prop(\"Scene ID\") == \"S001\", true, prop(\"Previous Scene\").prop(\"Unlocked\"))"
      }
    }
  }
}

// Example 2: Rollup to count solved puzzles
{
  "database_id": "<scenes-db-id>",
  "properties": {
    "Solved Count": {
      "rollup": {
        "relation_property_name": "Required Puzzles",
        "rollup_property_name": "Solved",
        "function": "checked"
      }
    }
  }
}
```

**Reference**: See [Rollup Patterns](references/rollup-patterns.md) for all 21 rollup functions with examples.

**Step 7: Create Initial Content**
Use `mcp__notion__notion-create-pages` to bulk create pages:

```javascript
// Batch create scenes (up to 100 per call)
{
  "parent": {"data_source_id": "<scenes-db-id>"},
  "pages": [
    {
      "properties": {
        "Scene ID": "S001",
        "Description": "You wake up in a dark office...",
        "Order": 1,
        "Act": "Act 1",
        "Unlocked": "__YES__"
      }
    },
    // ... up to 99 more pages
  ]
}
```

**Rate Limit Strategy**: 100 pages = 1 request. For 15 scenes + 8 items + 12 puzzles = 35 pages, use 1 call.

**Step 8: Add Localization**
Invoke `escape-room-localizer` skill, then use `mcp__notion__notion-create-pages` to create language variants.

**Step 9: Self-Test and Iterate**
- Use `mcp__notion__notion-fetch` to retrieve created content
- Test game mechanics manually in Notion
- Use `mcp__notion__notion-update-page` to fix issues
- Repeat until functional

**Step 10: Save Final Context**
```bash
# Save complete build state
# Invoke: /sc:save --context "escape-room-build-complete"
```

### Workflow 2: Modify Existing Template Based on Feedback

**Use Case**: "Update the puzzle difficulty based on playtest feedback"

**Process**:

```
Template Iteration:
- [ ] Step 1: Load session context (Serena MCP)
- [ ] Step 2: Fetch current template structure
- [ ] Step 3: Analyze feedback (playtesting-orchestrator)
- [ ] Step 4: Plan modifications (notion-formula-master)
- [ ] Step 5: Batch update pages/databases
- [ ] Step 6: Validate changes
- [ ] Step 7: Save updated context
```

**Step 1: Load Session Context**
```bash
# Restore previous development state
# Invoke: /sc:load --context "escape-room-build-complete"
```

**Step 2: Fetch Current Structure**
Use `mcp__notion__notion-search` to find template pages, then `mcp__notion__notion-fetch` to retrieve:
```javascript
// Search for template
{"query": "escape room template murder mystery", "query_type": "internal"}

// Fetch main database
{"id": "<database-url-from-search>"}
```

**Step 3: Analyze Feedback**
Invoke `playtesting-orchestrator` skill with feedback data to identify:
- Stuck points (>30% failure rate)
- Puzzles needing more hints
- Formula adjustments needed

**Step 4: Plan Modifications**
Invoke `notion-formula-master` skill to redesign:
- Progressive hint formulas (easier triggers)
- Dynamic difficulty scaling
- Better unlock conditions

**Step 5: Batch Update**
Use `mcp__notion__notion-update-page` to modify multiple pages:

```javascript
// Update puzzle hints (sequential, not parallel to avoid conflicts)
// Puzzle 1
{
  "page_id": "<puzzle-1-id>",
  "command": "update_properties",
  "properties": {
    "Hint 1": "Look at the calendar on the wall",
    "Hint 2": "The important dates are circled in red",
    "Hint 3": "Combine the month and day: 03-15"
  }
}

// Puzzle 2
{
  "page_id": "<puzzle-2-id>",
  "command": "update_properties",
  "properties": {
    "Hint 1": "Check the bookshelf for numbered books",
    "Hint 2": "The numbers on spines form a sequence",
    "Hint 3": "Read them left to right: 4-8-2-9"
  }
}
```

**Rate Limit Strategy**: 12 puzzles × 1 update each = 12 requests, well under limit. Can run sequentially in <1 minute.

**Step 6: Validate Changes**
- Use `mcp__notion__notion-fetch` to verify updates applied
- Compare with expected structure from Step 4

**Step 7: Save Updated Context**
```bash
# Save iteration state
# Invoke: /sc:save --context "escape-room-v2-hints-improved"
```

### Workflow 3: Create Custom Template from Requirements

**Use Case**: "Build a time tracking Notion template with automatic calculations"

**Process**:

```
Custom Template Build:
- [ ] Step 1: Clarify requirements with user
- [ ] Step 2: Design database schema
- [ ] Step 3: Create databases with properties
- [ ] Step 4: Implement calculation formulas
- [ ] Step 5: Create sample data
- [ ] Step 6: Build instructions page
- [ ] Step 7: Package as template
```

**Step 1: Clarify Requirements**
Ask user:
- What entities to track? (Projects, Tasks, Time Entries)
- What metrics to calculate? (Hours per project, billable vs. non-billable)
- What views needed? (Calendar, Kanban, Table)

**Step 2: Design Schema**
Plan databases and relationships:
- Projects (has many Tasks)
- Tasks (has many Time Entries, belongs to Project)
- Time Entries (belongs to Task)
- Summary (rollups from all databases)

**Step 3: Create Databases**
Use `mcp__notion__notion-create-database` sequentially:

```javascript
// Create Projects DB
{
  "title": [{"text": {"content": "Projects"}}],
  "properties": {
    "Project Name": {"title": {}},
    "Client": {"select": {"options": [{"name": "Internal", "color": "blue"}, {"name": "External", "color": "green"}]}},
    "Billable Rate": {"number": {"format": "dollar"}},
    "Total Hours": {"rollup": {/* ... configure after Tasks created ... */}},
    "Total Revenue": {"formula": {"expression": "prop(\"Total Hours\") * prop(\"Billable Rate\")"}}
  }
}

// Create Tasks DB
{
  "title": [{"text": {"content": "Tasks"}}],
  "properties": {
    "Task Name": {"title": {}},
    "Project": {"relation": {"data_source_id": "<projects-db-id>", "type": "single_property"}},
    "Status": {"status": {}},
    "Hours Logged": {"rollup": {/* ... configure after TimeEntries created ... */}}
  }
}

// Create Time Entries DB
{
  "title": [{"text": {"content": "Time Entries"}}],
  "properties": {
    "Description": {"title": {}},
    "Task": {"relation": {"data_source_id": "<tasks-db-id>", "type": "single_property"}},
    "Date": {"date": {}},
    "Start Time": {"date": {}},
    "End Time": {"date": {}},
    "Duration": {"formula": {"expression": "dateBetween(prop(\"End Time\"), prop(\"Start Time\"), \"hours\")"}}
  }
}
```

**Step 4: Implement Rollups**
Use `mcp__notion__notion-update-database` to add rollup properties:

```javascript
// Update Projects DB to rollup hours from Tasks
{
  "database_id": "<projects-db-id>",
  "properties": {
    "Total Hours": {
      "rollup": {
        "relation_property_name": "Tasks Relation",
        "rollup_property_name": "Hours Logged",
        "function": "sum"
      }
    }
  }
}
```

**Step 5: Create Sample Data**
Use `mcp__notion__notion-create-pages` to add examples:

```javascript
{
  "parent": {"data_source_id": "<projects-db-id>"},
  "pages": [
    {
      "properties": {
        "Project Name": "Website Redesign",
        "Client": "External",
        "Billable Rate": 150
      }
    },
    {
      "properties": {
        "Project Name": "Internal Tool Development",
        "Client": "Internal",
        "Billable Rate": 0
      }
    }
  ]
}
```

**Step 6: Build Instructions**
Use `mcp__notion__notion-create-pages` to create guide page:

```javascript
{
  "pages": [{
    "properties": {"title": "How to Use Time Tracker"},
    "content": "# Time Tracker Instructions\n\n## Quick Start\n1. Create a new Project\n2. Add Tasks under that Project\n3. Log Time Entries for each Task\n4. View automatic calculations in Project summary\n\n## Formulas Explained\n- **Duration**: Automatically calculates hours between Start and End Time\n- **Hours Logged**: Rolls up all Duration values from Time Entries\n- **Total Revenue**: Multiplies Total Hours × Billable Rate\n\n..."
  }]
}
```

**Step 7: Package as Template**
- Use `mcp__notion__notion-duplicate-page` to create template copy
- Share URL with user

## Rate Limit Management

### Strategy 1: Sequential Search Operations

**Problem**: Search has strict 30/min limit

**Solution**: Never run searches in parallel, always sequential

```javascript
// ❌ BAD - Parallel searches (will hit rate limit)
// Call notion-search 5 times simultaneously

// ✅ GOOD - Sequential searches
// Call notion-search → wait for result → call again → wait → ...
```

### Strategy 2: Batch Page Creation

**Problem**: Creating many pages individually hits 180/min limit

**Solution**: Use `notion-create-pages` bulk capability (100 pages per call)

```javascript
// ❌ BAD - Individual page creation
// 50 pages × 50 separate calls = 50 requests

// ✅ GOOD - Batch creation
// 50 pages ÷ 1 batch call = 1 request
{
  "pages": [ /* all 50 pages */ ]
}
```

### Strategy 3: Fetch Before Update

**Problem**: Updating without context can cause errors and wasted requests

**Solution**: Always fetch page/database first, then update

```javascript
// ✅ GOOD pattern
// 1. notion-fetch (1 request)
// 2. Analyze content
// 3. notion-update-page (1 request)
// Total: 2 requests with context

// ❌ BAD pattern
// 1. notion-update-page (fails, 1 request)
// 2. notion-fetch to debug (1 request)
// 3. notion-update-page again (1 request)
// Total: 3 requests
```

### Strategy 4: Monitor Request Count

Use `scripts/rate_limit_monitor.py` to track API usage:

```bash
py scripts/rate_limit_monitor.py --window 60
# Output: "Requests in last 60s: 45/180 (25%)"
```

See [references/rate-limit-strategies.md](references/rate-limit-strategies.md) for advanced patterns.

## Session Persistence with Serena MCP

### When to Save Context

**Save after each major phase:**
- Design complete (after skill orchestration)
- Databases created (after database creation)
- Content populated (after page creation)
- Iteration complete (after updates)

### Save Command

```bash
# Invoke slash command
/sc:save --context "descriptive-checkpoint-name"
```

**What gets saved:**
- Notion database IDs
- Page URLs
- Schema designs
- Design outputs from orchestrated skills
- Current development phase

### Load Command

```bash
# Restore previous session
/sc:load --context "descriptive-checkpoint-name"
```

**When to load:**
- Starting new development session
- Resuming after interruption
- Rolling back to previous working state

### Context Naming Convention

Use descriptive names with phase:
- `escape-room-design-v1`
- `time-tracker-databases-created`
- `murder-mystery-localization-complete`

See [references/serena-integration.md](references/serena-integration.md) for detailed Serena MCP usage.

## Integration with Existing Skills

### Orchestration Pattern

When building escape rooms, invoke skills in this order:

1. **narrative-architect-korean-style** → Story, characters, endings
2. **language-agnostic-puzzle-designer** → Puzzle inventory, difficulty curve
3. **notion-formula-master** → Database schema, formulas, rollups
4. **notion-mcp-developer** (this skill) → Implement in Notion
5. **escape-room-localizer** → Add translations
6. **playtesting-orchestrator** → Collect feedback, iterate

### Data Flow Between Skills

**From narrative-architect → notion-mcp-developer:**
- Scene descriptions → Scenes database content
- Character profiles → Characters database
- Endings → Endings database with unlock formulas

**From puzzle-designer → notion-mcp-developer:**
- Puzzle list → Puzzles database content
- Hint progression → Hint formula properties
- Difficulty curve → Order property values

**From formula-master → notion-mcp-developer:**
- Schema designs → `notion-create-database` calls
- Formula expressions → Property definitions
- Rollup configurations → Relation + rollup setup

**From localizer → notion-mcp-developer:**
- Translations → Duplicate pages with translated content
- Cultural adaptations → Modified puzzle descriptions

**From playtester → notion-mcp-developer:**
- Stuck points → Hint improvements via `notion-update-page`
- Completion metrics → Formula adjustments
- Feedback → Content revisions

## Error Handling

### Common Errors and Solutions

**Error**: `Rate limit exceeded`
**Solution**: Wait 60 seconds, then retry. Use `scripts/rate_limit_monitor.py` to check status.

**Error**: `Parent not found`
**Solution**: Verify parent ID exists via `notion-fetch`. Check if using correct ID type (page_id vs data_source_id vs database_id).

**Error**: `Invalid property type`
**Solution**: Fetch database schema first to verify property names and types match exactly.

**Error**: `Relation target database not found`
**Solution**: Create target database first, then create source database with relation.

**Error**: `Formula syntax error`
**Solution**: Validate formula using `scripts/validate_formula.py` before applying.

See [references/error-handling.md](references/error-handling.md) for complete error reference.

## Validation and Testing

### Pre-Creation Validation

Before creating databases, validate schema:

```bash
py scripts/validate_notion_structure.py schema.json
```

### Post-Creation Testing

After building template, run health check:

```bash
py scripts/notion_health_check.py <database-url>
```

Checks:
- All relations resolve correctly
- Formulas compile without errors
- Rollups have valid targets
- Required properties exist

## Resources

### references/
- `notion-mcp-tools.md` - Complete API reference with examples
- `notion-markdown-spec.md` - Notion-flavored Markdown specification
- `rate-limit-strategies.md` - Advanced rate limit patterns
- `database-patterns.md` - Common database architectures for games
- `error-handling.md` - Error codes and solutions
- `serena-integration.md` - Session persistence guide
- `formula-library.md` - Reusable formula patterns

### scripts/
- `rate_limit_monitor.py` - Track API usage in real-time
- `validate_notion_structure.py` - Pre-validate database schemas
- `notion_health_check.py` - Post-creation validation
- `validate_formula.py` - Test formula syntax
- `batch_operations.py` - Helper for batching API calls

### assets/
- `database-templates/` - JSON templates for common structures
- `formula-library/` - Copy-paste formula patterns

## Example Usage

**User**: "Create a murder mystery escape room in Notion with Korean and English versions"

**Assistant**:
1. Invokes `narrative-architect-korean-style` → Receives 3-act murder mystery story
2. Invokes `language-agnostic-puzzle-designer` → Receives 15 visual/logic puzzles
3. Invokes `notion-formula-master` → Receives database schema design
4. Saves context via Serena MCP → `/sc:save --context "murder-mystery-design-complete"`
5. Creates 5 databases via `notion-create-database` (Scenes, Items, Puzzles, PlayerState, Endings)
6. Updates databases with formulas via `notion-update-database`
7. Bulk creates 15 scenes + 8 items + 15 puzzles via `notion-create-pages` (38 pages in 1 request)
8. Invokes `escape-room-localizer` → Receives Korean translations
9. Duplicates pages for Korean version via `notion-duplicate-page`
10. Saves final state → `/sc:save --context "murder-mystery-build-complete"`
11. Returns Notion template URL to user

**Total API Calls**: ~25 requests (well under 180/min limit, 0 searches)

---

**User**: "The puzzle difficulty is too hard, 35% completion rate. Fix it."

**Assistant**:
1. Loads context → `/sc:load --context "murder-mystery-build-complete"`
2. Searches for template → `notion-search` with query
3. Fetches Puzzles database → `notion-fetch`
4. Invokes `playtesting-orchestrator` → Analyzes 35% vs 60-70% target
5. Invokes `notion-formula-master` → Redesigns hint formulas (easier triggers)
6. Updates 15 puzzles via `notion-update-page` (15 sequential requests)
7. Validates changes → `notion-fetch` on sample puzzles
8. Saves iteration → `/sc:save --context "murder-mystery-v2-difficulty-fixed"`
9. Reports changes to user

**Total API Calls**: ~18 requests (1 search + 1 fetch + 15 updates + 1 validation)

## Best Practices

### 1. Always Fetch Before Update
Understand current state before modifying to avoid conflicts and errors.

### 2. Batch Page Creation
Use `notion-create-pages` bulk capability for efficiency.

### 3. Sequential Searches
Never run searches in parallel due to 30/min limit.

### 4. Save Context Frequently
Use Serena MCP after each major phase for easy recovery.

### 5. Validate Before Creating
Run validation scripts to catch schema errors early.

### 6. Test Incrementally
Build databases → test → add content → test → iterate.

### 7. Use Skill Orchestration
Leverage existing design skills before implementation.

### 8. Monitor Rate Limits
Use monitoring script during complex operations.

### 9. Document Template Usage
Create instruction pages for end users.

### 10. Version Control Context
Use descriptive checkpoint names for easy rollback.

---

## Additional Resources

### Reference Documentation
For detailed implementation guides, see:
- **[Escape Room Database Architecture](references/escape-room-database-architecture.md)** - Complete 5-database structure
- **[Game Mechanics Formulas](references/game-mechanics-formulas.md)** - 20+ formula patterns
- **[Rollup Patterns](references/rollup-patterns.md)** - All 21 Notion rollup functions
- **[Relation Design Patterns](references/relation-design-patterns.md)** - 4 relation types with examples
- **[Phase-Based Implementation](references/phase-based-implementation.md)** - Optimized API call order
- **[Antipatterns & Gotchas](references/antipatterns-and-gotchas.md)** - Common mistakes to avoid

### Notion MCP Tool Reference
- **[Notion MCP Tools](references/notion-mcp-tools.md)** - Complete API reference with 14 tools

### Related Skills
Orchestrated by this skill:
- **narrative-architect-korean-style** - 3-act story structure, character profiles, emotional arcs
- **language-agnostic-puzzle-designer** - Visual/logic puzzles, difficulty progression, hint systems
- **notion-formula-master** - Formula 2.0 implementation, database relationships, game mechanics
- **escape-room-localizer** - Korean/English/Japanese localization, cultural adaptation
- **playtesting-orchestrator** - Difficulty analysis, feedback collection, balance adjustment

---

**Version**: 2.0 (Enhanced with Security, Error Handling, and Reference Documentation)
**Last Updated**: 2025-10-30
**Author**: Notion MCP Developer Skill Research Team
**Total Lines**: ~1,900+
**Reference Files**: 7 (6 guides + 1 tool reference)
