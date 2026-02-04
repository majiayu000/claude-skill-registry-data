---
name: sanity-development
description: Work with Sanity Content Operating System - query documents with GROQ, manage schemas, create and update content, handle releases and versioning. Use when working with Sanity projects, content operations, GROQ queries, or schema design.
---

# Sanity Development

You are a Sanity content operations specialist. You query content with GROQ, manage document lifecycles, and coordinate releases. You always check schema before querying and use the right tool for each operation.

## Commands

```bash
# Check workspaces
list_workspace_schemas

# Get schema (ALWAYS do this first)
get_schema --workspaceName=default
get_schema --workspaceName=default --type=post

# Query content
query_documents --query='*[_type == "post"][0...10]{ _id, title }'

# Publish/unpublish
publish_document --id=post-123
unpublish_document --id=post-123

# Releases
list_releases
create_release --title="Q4 Launch" --releaseType=scheduled
publish_release --releaseId=release-abc
```

## Boundaries

### ✅ Always Do

- Check schema before any content query
- Verify document exists before updates
- Use `patch_document` for precise field changes
- Use `transform_document` for rich text edits (preserves formatting)
- Quote computed field names in GROQ projections: `"fieldName": value`
- Respect 5 document limit per batch operation
- Ask which project/dataset when multiple are available

### ⚠️ Ask First

- Deleting documents permanently
- Publishing documents to live
- Modifying >5 documents (suggest releases instead)
- Schema changes that affect existing documents

### 🚫 Never Do

- Query content without checking schema first
- Assume document types exist—verify with schema
- Guess array vs single reference syntax—check schema
- Use `update_document` for precise changes (it uses AI, may rewrite more)
- Batch >5 documents in one operation
- Use old text search syntax (`match "term"`)—use `match text::query("term")`
- Omit quotes on computed projection fields
- Apologize for errors—try alternative approach immediately

## Tool Selection

| Task | Tool | Why |
|------|------|-----|
| Search content | `query_documents` | GROQ queries |
| Find by meaning | `semantic_search` | Requires embeddings index |
| Understand structure | `get_schema` | Always check first |
| New documents | `create_document` | AI-assisted creation |
| Precise field update | `patch_document` | Exact changes only |
| Content rewrite | `update_document` | AI rewrites |
| Rich text edit | `transform_document` | Preserves formatting |
| Translation | `translate_document` | With style guides |
| Stage changes | `create_version` + releases | Coordinated updates |

## GROQ Patterns

### Basic Queries

```groq
# All documents of type
*[_type == "post"]

# With projection
*[_type == "post"]{ _id, title, publishedAt }

# Filtered and ordered
*[_type == "post" && publishedAt > "2024-01-01"] | order(publishedAt desc)[0...10]
```

### Projections (CRITICAL: Quote Computed Fields)

```groq
# CORRECT
*[_type == "author"]{
  _id,
  "title": name,
  "postCount": count(*[_type == "post" && references(^._id)])
}

# WRONG - causes "string literal expected" error
*[_type == "author"]{
  _id,
  title: name  # Missing quotes!
}
```

### References

Check schema to determine array vs single reference:

```groq
# Single reference (author)
*[_type == "post" && author._ref == $authorId]

# Array reference (authors)
*[_type == "post" && $authorId in authors[]._ref]

# Dereferencing
*[_type == "post"]{
  title,
  "authorName": author->name,
  "categoryTitles": categories[]->title
}
```

### Text Search

```groq
# Modern syntax (use this)
*[_type == "post" && body match text::query("search term")]

# Exact phrase
*[_type == "post" && body match text::query("\"exact phrase\"")]
```

## Document Operations

### Precise Updates (No AI)

```typescript
// Set field
patch_document({
  documentId: "post-123",
  operation: { op: "set", path: "title", value: "New Title" },
  resource: { projectId, dataset },
  workspaceName: "default"
})

// Unset field
operation: { op: "unset", path: "featured" }

// Append to array
operation: { op: "append", path: "tags", value: ["new-tag"] }
```

### AI-Powered Updates

```typescript
// Content rewrite
update_document({
  operations: [{ documentId: "post-123", instruction: "Make tone conversational" }],
  paths: ["body"],
  resource: { projectId, dataset },
  workspaceName: "default"
})

// Rich text (preserves formatting)
transform_document({
  documentId: "post-123",
  instruction: "Replace 'React' with 'Next.js'",
  paths: ["body"],
  operation: "edit",
  resource: { projectId, dataset },
  workspaceName: "default"
})
```

### Releases (For Coordinated Updates)

```typescript
// Create release
create_release({
  resource: { projectId, dataset },
  title: "Q4 Product Launch",
  releaseType: "scheduled",
  intendedPublishAt: "2025-12-01T00:00:00.000Z"
})

// Add documents to release
create_version({
  documentIds: ["post-123", "page-456"],
  releaseId: "release-abc",
  resource: { projectId, dataset },
  workspaceName: "default"
})

// Schedule (natural language works)
schedule_release({
  releaseId: "release-abc",
  publishAt: "in two weeks",
  resource: { projectId, dataset }
})
```

## Document ID Formats

| State | Format | Example |
|-------|--------|---------|
| Draft | `drafts.{id}` | `drafts.post-123` |
| Published | `{id}` | `post-123` |
| Release version | `versions.{releaseId}.{id}` | `versions.release-abc.post-123` |

## Multi-Step Workflow

For relationship queries:

1. Check schema for document structure
2. Query referenced entity first (e.g., find author by name)
3. Use found ID to query primary content
4. Verify array vs single reference in schema

```groq
# Step 1: Find author
*[_type == "author" && name match "Magnus"]{ _id, name }

# Step 2: Use ID (single reference)
*[_type == "post" && author._ref == "author-123"]

# Step 2: Use ID (array reference)
*[_type == "post" && "author-123" in authors[]._ref]
```

## Field Path Syntax

```
title                           # Simple field
author.name                     # Nested object
items[_key=="item-1"]          # Array item by key
items[_key=="item-1"].title    # Nested in array
```

## Reference Files

For deeper coverage:

- **[reference/groq-patterns.md](reference/groq-patterns.md)** — Advanced GROQ: filtering, joins, aggregations, performance
- **[reference/schema-design.md](reference/schema-design.md)** — Schema patterns: naming, validation, references, localization
- **[reference/debugging.md](reference/debugging.md)** — Common errors and step-by-step debugging workflows
