---
name: notion-operations
description: Use when working with Notion databases, creating/updating pages, querying data, syncing between systems, or building knowledge management workflows
---

# Notion Database Operations

**When to use**: Any Notion integration, database CRUD operations, data synchronization, or knowledge management automation.

## Overview

Production-ready patterns for Notion API integration with comprehensive field type support, error handling, and database synchronization strategies.

## Key Capabilities

- ✅ Complete CRUD operations
- ✅ All Notion field types supported
- ✅ Complex filtering (10+ filter types)
- ✅ Database sync patterns
- ✅ Deduplication strategies
- ✅ Structured data design patterns

## Supported Field Types

```javascript
var notionFields = {
  title: [{text: {content: 'Page Title'}}],
  rich_text: [{text: {content: 'Text content'}}],
  url: 'https://example.com',
  select: {name: 'Option'},
  multi_select: [{name: 'Tag1'}, {name: 'Tag2'}],
  date: {start: '2025-01-01'},
  number: 42,
  checkbox: true,
  email: 'user@example.com',
  phone_number: '+1234567890',
  status: {name: 'In Progress'},
  relation: [{id: 'page-id-123'}]
};
```

## Core Operations

### 1. Create Page

```javascript
var https = require('https');

function createNotionPage(databaseId, properties, apiKey) {
  var body = JSON.stringify({
    parent: {database_id: databaseId},
    properties: properties
  });

  var options = {
    hostname: 'api.notion.com',
    path: '/v1/pages',
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + apiKey,
      'Content-Type': 'application/json',
      'Notion-Version': '2022-06-28',
      'Content-Length': Buffer.byteLength(body)
    }
  };

  return new Promise(function(resolve, reject) {
    var req = https.request(options, function(res) {
      var data = '';
      res.on('data', function(chunk) { data += chunk; });
      res.on('end', function() {
        if (res.statusCode !== 200) {
          reject(new Error('Notion API error: ' + data));
        } else {
          resolve(JSON.parse(data));
        }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}
```

### 2. Query Database

```javascript
function queryNotionDatabase(databaseId, filter, apiKey) {
  var body = JSON.stringify({
    filter: filter,
    page_size: 100
  });

  var options = {
    hostname: 'api.notion.com',
    path: '/v1/databases/' + databaseId + '/query',
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + apiKey,
      'Content-Type': 'application/json',
      'Notion-Version': '2022-06-28'
    }
  };

  return makeRequest(options, body);
}
```

### 3. Update Page

```javascript
function updateNotionPage(pageId, properties, apiKey) {
  var body = JSON.stringify({
    properties: properties
  });

  var options = {
    hostname: 'api.notion.com',
    path: '/v1/pages/' + pageId,
    method: 'PATCH',
    headers: {
      'Authorization': 'Bearer ' + apiKey,
      'Content-Type': 'application/json',
      'Notion-Version': '2022-06-28'
    }
  };

  return makeRequest(options, body);
}
```

## Common Filters

```javascript
// URL equals
var filter = {
  property: 'URL',
  url: {equals: 'https://example.com'}
};

// Text contains
var filter = {
  property: 'Title',
  title: {contains: 'keyword'}
};

// Status equals
var filter = {
  property: 'Status',
  status: {equals: 'Published'}
};

// Checkbox is true
var filter = {
  property: 'Synced',
  checkbox: {equals: true}
};

// Date after
var filter = {
  property: 'Created',
  date: {after: '2025-01-01'}
};

// Multi-select contains
var filter = {
  property: 'Tags',
  multi_select: {contains: 'Important'}
};

// Compound filter (AND/OR)
var filter = {
  and: [
    {property: 'Status', status: {equals: 'Active'}},
    {property: 'Type', select: {equals: 'Video'}}
  ]
};
```

## Database Sync Pattern

Complete workflow for syncing data from source to target database:

```
Step 1: Query Source Database
    ↓
Step 2: Check for Duplicates in Target
    filter: {url: {equals: sourceItem.url}}
    ↓
Step 3: Map Fields
    sourceFields → targetFields
    ↓
Step 4: Create/Update Target
    if exists: update
    else: create
    ↓
Step 5: Mark as Synced in Source
    properties: {Synced: {checkbox: true}}
```

### Implementation

```javascript
// Step 1: Query source
var sourceItems = await queryNotionDatabase(
  sourceDbId,
  {property: 'Synced', checkbox: {equals: false}},
  apiKey
);

// Step 2-4: Process each item
for (var i = 0; i < sourceItems.results.length; i++) {
  var item = sourceItems.results[i];

  // Check duplicate
  var existing = await queryNotionDatabase(
    targetDbId,
    {property: 'URL', url: {equals: item.properties.URL.url}},
    apiKey
  );

  // Map fields
  var targetProps = {
    Title: item.properties.Title,
    URL: item.properties.URL,
    Summary: item.properties.Summary,
    // ... more fields
  };

  // Create or update
  if (existing.results.length > 0) {
    await updateNotionPage(existing.results[0].id, targetProps, apiKey);
  } else {
    await createNotionPage(targetDbId, targetProps, apiKey);
  }

  // Step 5: Mark as synced
  await updateNotionPage(
    item.id,
    {Synced: {checkbox: true}},
    apiKey
  );
}
```

## Structured Data Design

### ❌ Bad: Mixed Storage (3 fields)
```javascript
{
  Title: 'Video title',
  Content: 'Mixed text with timestamps [00:01:23] and quotes...',
  URL: 'https://...'
}
```

**Problems**:
- Cannot query by timestamp
- Cannot filter by quote topic
- Cannot analyze patterns
- Hard to display/organize

### ✅ Good: Structured Storage (14 fields)
```javascript
{
  Title: 'Video title',
  URL: 'https://...',
  Author: 'Channel name',
  Duration: 3600,
  Transcript: 'Full text...',
  Summary: 'AI generated...',
  Tags: ['AI', 'Tech'],
  Quotes: 'Key quotes...',
  Timestamps: '[00:01:23], [00:05:45]',
  Category: 'Tutorial',
  Language: 'English',
  Source: 'YouTube',
  CreatedTime: '2025-01-01',
  Status: 'Processed'
}
```

**Benefits**:
- Queryable by any field
- Filterable and sortable
- Analyzable for patterns
- Better organization

## Best Practices

### 1. Field Naming
- Use PascalCase: `CreatedTime`, `VideoURL`
- Descriptive: `TranscriptText` not `Text`
- Consistent across databases

### 2. URL-Based Deduplication
```javascript
// Always use URL as unique identifier
var filter = {
  property: 'URL',
  url: {equals: item.url}
};
```

### 3. Error Handling
```javascript
try {
  var result = await createNotionPage(dbId, props, apiKey);
  return {success: true, id: result.id};
} catch (error) {
  return {
    success: false,
    error: error.message,
    context: {url: props.URL, title: props.Title}
  };
}
```

### 4. Rate Limiting
```javascript
// Notion API: 3 requests/second
var delay = 350;  // 350ms between requests
await new Promise(function(r) { setTimeout(r, delay); });
```

## Common Patterns

### Pattern 1: Link Collection
```
Webhook (URL) → Fetch Content → AI Analysis → Create Notion Page
```

### Pattern 2: Database Sync
```
Schedule → Query Source → Check Duplicates → Map Fields → Update Target
```

### Pattern 3: Batch Processing
```
Query Database → Split Into Batches → Process Each → Update Status
```

## Troubleshooting

### Invalid properties error
```javascript
// Check field types match database schema
// Use Notion API to get database schema:
GET https://api.notion.com/v1/databases/{id}
```

### Duplicate pages created
```javascript
// Always check for existing pages first
// Use URL or unique identifier for filtering
```

### Rate limit exceeded
```javascript
// Add delays between requests
// Batch operations when possible
// Use page_size parameter for pagination
```

## Integration with Other Skills

- **ai-integration**: Analyze content before saving
- **notion-link-analysis**: URL → AI → Notion automation
- **video-processing**: Save video analysis results
- **notion-database-sync**: Sync between databases

## Full Code and Documentation

Complete implementations:
`/mnt/d/work/n8n_agent/n8n-skills/notion-operations/`

Files:
- `notion-database.js` - Complete CRUD operations
- `notion-sync-patterns.js` - Sync workflows
- `README.md` - Detailed patterns and examples
