---
name: pathway-collector
description: Scan all repos in ~/Desktop/Dev/repos/ and the Supabase movemental database (alan-hirsch tenant) to discover all existing pathway, portal, and theme content — markdown, HTML, data files, skills, and database records. Produces a comprehensive inventory organized by portal. Use when you need a full picture of what pathway content exists.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Agent
---

Collect and inventory all pathway/portal/theme content: $ARGUMENTS

$ARGUMENTS can optionally specify a single portal slug to focus on (reframation, metanoia, mdna, movement-intelligence, forgotten-ways, discipleship). If omitted, collect across all portals.

---

## Terminology

These terms are used **interchangeably** across the codebase:
- **Portals** — Five thematic doorways (canonical term in strategy docs)
- **Pathways** — UI browse/discovery layer (canonical term in frontend code)
- **Themes** — Configuration-level grouping (canonical term in tenant config)

The five canonical portals:
| Slug | Title |
|------|-------|
| `reframation` | Reframation |
| `metanoia` | Metanoia |
| `mdna` | mDNA |
| `movement-intelligence` | Movement Intelligence |
| `forgotten-ways` | The Forgotten Ways |
| `discipleship` | Discipleship |

---

## Step 1 — Scan All Repositories

Search the following repos for pathway/portal/theme content. Use Grep and Glob to find files matching these patterns:

**Search terms** (in filenames AND file contents):
- `pathway`, `pathways`
- `portal`, `portals`
- `theme`, `themes` (in context of content themes, not CSS/UI themes)
- Individual portal slugs: `reframation`, `metanoia`, `mdna`, `movement-intelligence`, `forgotten-ways`, `discipleship`

**Repos to scan** (all in `~/Desktop/Dev/repos/`):
1. `alan-hirsch` — Primary app, vision docs, content data, HTML templates, portal config
2. `movemental-ai` — Content research, articles by theme, pastoral-warm content
3. `movemental-content-studio` — Database schema, course scaffolding, content studio
4. `adam-seiz` — Pathway author/audit skills, course skills
5. `storyboard` — Video/story scripts mentioning portals
6. `non-profit-dashboard` — Youthfront pathway research
7. `alan-hirsch-ai-studio` — AI studio if it exists
8. `alan-hirsch-html` — Static HTML versions
9. `forgotten-ways-course` — Course content for Forgotten Ways portal

**File types to look for:**
- `.md` — Markdown documentation and articles
- `.html` — HTML templates and prototypes
- `.json` — Portal/theme configuration data
- `.ts` / `.tsx` — TypeScript content data files (NOT React components)
- `.yaml` / `.yml` — Configuration files

**Exclude from results:**
- `node_modules/`, `.next/`, `dist/`, `.git/`
- React component files (`.tsx` with JSX rendering logic)
- CSS-only files (unless paired with HTML templates)
- Test files

---

## Step 2 — Query Supabase Database

If the Supabase MCP is available, query the movemental database for the alan-hirsch tenant:

```sql
-- Get all pathways
SELECT id, slug, title, description, portal, content_path, source_type, placement, order_index
FROM pathways
WHERE organization_id = (SELECT id FROM organizations WHERE slug = 'alan-hirsch')
ORDER BY portal, order_index;

-- Get content with portal_themes
SELECT id, title, portal_themes, theological_themes
FROM books
WHERE organization_id = (SELECT id FROM organizations WHERE slug = 'alan-hirsch')
AND portal_themes IS NOT NULL;

-- Get courses with portal_themes
SELECT id, slug, title, portal_themes
FROM courses
WHERE organization_id = (SELECT id FROM organizations WHERE slug = 'alan-hirsch')
AND portal_themes IS NOT NULL;

-- Get articles with theological_themes
SELECT id, slug, title, theological_themes
FROM articles
WHERE organization_id = (SELECT id FROM organizations WHERE slug = 'alan-hirsch')
AND theological_themes IS NOT NULL;
```

If Supabase MCP is not available, note this gap in the inventory and suggest running `pathway-supabase` separately.

---

## Step 3 — Classify & Organize Findings

Group all discovered content into this taxonomy:

### Per Portal:
- **Vision Documents** — High-level conceptual/strategy docs
- **Articles** — Written content pieces (published or draft)
- **Case Studies** — Real-world examples and stories
- **HTML Templates** — Visual prototypes
- **Course Content** — Course modules, lessons, scripts
- **Data Files** — TypeScript/JSON content definitions
- **Database Records** — Supabase rows (pathways, books, courses, articles)
- **Skills** — Claude skills for authoring/auditing

### Cross-Portal:
- **Christocentric Spine** — Core theological charter
- **Portal Cards** — Doorway page content
- **Glossary** — Movemental vocabulary
- **Design Specs** — Design system alignment docs
- **Content Research** — Inventories, mappings, terminology

---

## Step 4 — Produce Inventory Report

Write the inventory to `~/Desktop/Dev/repos/docs/INVENTORY.md` with this structure:

```markdown
# Pathway Content Inventory
> Generated: [date]
> Scope: [all portals | specific portal]

## Summary
- Total files discovered: N
- Files in docs repo: N
- Files not yet in docs: N
- Database records: N

## Per Portal

### Reframation
#### Vision Documents
- [file path] — [brief description] — [source repo]

#### Articles
...

### Metanoia
...

## Cross-Portal Content
...

## Gaps & Recommendations
- [portal] is missing [section type]
- [content] exists in [repo] but is not yet in docs/
```

---

## Step 5 — Identify Gaps

Compare discovered content against the 12-section canonical architecture:

1. Overview
2. The Model (named framework)
3. Quotes
4. Visualizations
5. Scripture
6. Case Studies
7. FAQ
8. Practices
9. Reflection Questions
10. Courses
11. Content (curated resources)
12. Glossary Terms

For each portal, report which sections have content and which are missing or incomplete.
