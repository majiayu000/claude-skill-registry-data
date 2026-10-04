---
name: pathway-supabase
description: Pull pathway, portal, and theme content from the Supabase movemental database for the alan-hirsch tenant. Queries pathways, books, courses, articles, and content_items tables for portal-tagged records. Exports results as organized markdown into the docs repo.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Agent
---

Pull pathway content from Supabase: $ARGUMENTS

$ARGUMENTS can specify:
- A portal slug to focus on (reframation, metanoia, mdna, movement-intelligence, forgotten-ways, discipleship)
- A content type to focus on (pathways, books, courses, articles)
- "all" to pull everything

If no arguments, pull all pathway-related content for the alan-hirsch tenant.

---

## Prerequisites

This skill requires either:
1. **Supabase MCP** — Connected to the movemental database
2. **Supabase CLI** — `supabase` CLI configured for the project
3. **Direct connection** — Via `psql` or a database client

If none are available, print instructions for the user to connect.

---

## Database Schema Reference

Source: `movemental-content-studio/shared/alan-hirsch/database/schema.ts`

### Key Tables

**`pathways`** — Learning path sequences
```
id, slug, title, description, portal, content_path, inventory_id,
source_type, placement, order_index, organization_id, created_at, updated_at
```

**`books`** — Books with portal associations
```
id, title, subtitle, author, portal_themes (JSONB), description,
cover_image_url, publication_year, organization_id
```

**`courses`** — Courses with portal associations
```
id, slug, title, description, portal_themes (JSONB), instructor,
duration_weeks, organization_id
```

**`articles`** — Articles with theological themes
```
id, slug, title, body, theological_themes (JSONB), author,
status, organization_id
```

**`contentItems`** — Generic content with theological themes
```
id, title, type, theological_themes (JSONB), organization_id
```

---

## Step 1 — Identify the Organization

Query for the alan-hirsch organization ID:

```sql
SELECT id, slug, name FROM organizations WHERE slug = 'alan-hirsch';
```

Store this ID for all subsequent queries.

---

## Step 2 — Pull Pathways

```sql
SELECT id, slug, title, description, portal, content_path, source_type, placement, order_index
FROM pathways
WHERE organization_id = '{org_id}'
ORDER BY portal, order_index;
```

---

## Step 3 — Pull Portal-Tagged Content

### Books
```sql
SELECT id, title, subtitle, author, portal_themes, description, publication_year
FROM books
WHERE organization_id = '{org_id}'
  AND portal_themes IS NOT NULL
ORDER BY title;
```

### Courses
```sql
SELECT id, slug, title, description, portal_themes, instructor, duration_weeks
FROM courses
WHERE organization_id = '{org_id}'
  AND portal_themes IS NOT NULL
ORDER BY slug;
```

### Articles
```sql
SELECT id, slug, title, theological_themes, author, status
FROM articles
WHERE organization_id = '{org_id}'
  AND theological_themes IS NOT NULL
ORDER BY slug;
```

### Content Items
```sql
SELECT id, title, type, theological_themes
FROM "contentItems"
WHERE organization_id = '{org_id}'
  AND theological_themes IS NOT NULL
ORDER BY type, title;
```

---

## Step 4 — Organize by Portal

Group all results by portal/theme association. A single record may appear under multiple portals if its `portal_themes` array contains multiple values.

---

## Step 5 — Export to Docs Repo

Write results to `~/Desktop/Dev/repos/docs/knowledge/supabase-export/`:

### File: `pathways-export.md`
```markdown
# Pathways — Supabase Export
> Exported: [date]
> Tenant: alan-hirsch

## By Portal

### Reframation
| ID | Slug | Title | Source Type | Order |
|----|------|-------|-------------|-------|
| ... | ... | ... | ... | ... |

### Metanoia
...
```

### File: `books-by-portal.md`
```markdown
# Books Tagged by Portal
> Exported: [date]

## Reframation
- **{title}** by {author} ({year}) — {description}

## Metanoia
...
```

### File: `courses-by-portal.md`
(Same format as books)

### File: `articles-by-portal.md`
(Same format, grouped by theological theme to portal mapping)

---

## Step 6 — Cross-Reference with Docs

Compare the Supabase export against what's already in the docs repo:

1. Are there pathways in the DB that have no corresponding vision doc?
2. Are there courses tagged to a portal that have no course content in docs?
3. Are there articles in the DB that aren't represented in `pathways/{slug}/articles/`?

Write discrepancies to `~/Desktop/Dev/repos/docs/knowledge/supabase-export/DISCREPANCIES.md`.

---

## Step 7 — Report

Print a summary:
- Total pathways found
- Total content records by type
- Content distribution across portals
- Key discrepancies between DB and docs repo
