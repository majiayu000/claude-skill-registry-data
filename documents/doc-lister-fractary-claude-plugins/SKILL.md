---
name: doc-lister
description: Lists and filters documentation files by type, status, tags, and date range with frontmatter parsing
model: claude-haiku-4-5
---

# doc-lister

<CONTEXT>
**Purpose**: List and filter documentation files.

**Architecture**: Operation-specific skill (Layer 3)
</CONTEXT>

<CRITICAL_RULES>
- ALWAYS scan specified directory
- ALWAYS parse frontmatter for filtering
- NEVER modify files
- ALWAYS return structured list
</CRITICAL_RULES>

<INPUTS>
Required:
- `path` - Directory to scan (default: docs/)

Optional filters:
- `doc_type` - Filter by fractary_doc_type
- `status` - Filter by status (draft, published, deprecated)
- `tags` - Filter by tags (array)
- `date_range` - Filter by created/updated dates
</INPUTS>

<WORKFLOW>
1. **Scan Directory**
   - Find all README.md files recursively
   - Exclude node_modules, .git, etc.

2. **Parse Frontmatter**
   - Extract YAML frontmatter from each file
   - Build document list with metadata

3. **Apply Filters**
   - Filter by doc_type if specified
   - Filter by status if specified
   - Filter by tags if specified
   - Filter by date range if specified

4. **Return List**
```json
{
  "total": 42,
  "filtered": 15,
  "documents": [
    {
      "path": "docs/api/auth/login/README.md",
      "title": "Login Endpoint",
      "doc_type": "api",
      "status": "published",
      "version": "1.2.0",
      "updated": "2025-01-15"
    }
  ]
}
```
</WORKFLOW>
