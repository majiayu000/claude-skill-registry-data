---
name: cms-interaction
description: Configure CMS connections and perform ad-hoc content searches (Sanity, Contentful, WordPress)
---

# CMS Interaction Skill

**Purpose:** Ad-hoc CMS configuration and operations
**Subskills:** onboard, search, publish
**Supported CMSs:** Sanity (full support), Contentful (coming soon), WordPress (coming soon)

---

## Overview

This skill provides ad-hoc CMS operations using `kurt cms` CLI commands:
1. **Configuration**: Set up CMS connections (first-time setup)
2. **Ad-hoc search**: Quick content searches during project planning/research
3. **Publishing**: Push completed drafts back to CMS

**For systematic content mapping and fetching**, use the unified core workflow:
- `kurt map cms --platform sanity --instance prod --cluster-urls` (discovery + clustering)
- `kurt fetch --include "sanity/prod/*"` (download + index)

This workflow integrates CMS content with web content using the same commands. See project-management-skill (gather-sources subskill) for full orchestration.

---

## Architecture

### Pattern: CLI-Wrapper

This skill is a **thin orchestration layer** over kurt CLI commands:

```
User Request → Skill (routing) → kurt cms command → CMS API
```

All CMS logic lives in kurt-core:
- `src/kurt/commands/cms.py` - CLI commands
- `src/kurt/cms/sanity/adapter.py` - Sanity implementation
- `src/kurt/cms/config.py` - Configuration management

This skill focuses on:
- Routing user requests to appropriate commands
- Parsing parameters and options
- Providing context-specific guidance
- Following up after command execution

---

## Usage

### Configuration (First-Time Setup)

```bash
cms-interaction onboard
```

Routes to: `kurt cms onboard --platform sanity`

This guides you through:
- Creating `.kurt/cms-config.json`
- Entering credentials
- Discovering content types
- Mapping custom field names

### Ad-Hoc Search (During Research)

Use during project planning to explore CMS content:

```bash
cms-interaction search --query "tutorial" --limit 10
```

Routes to: `kurt cms search --query "tutorial" --limit 10`

**When to use:**
- Exploring what content exists
- Quick research during project planning
- Finding specific documents by keyword

**For systematic ingestion**, use `kurt map cms` instead (see project-management-skill).

### Publishing Drafts

```bash
cms-interaction publish --file draft.md --id <document-id>
```

Routes to: `kurt cms publish --file draft.md --id <document-id>`

Pushes completed content back to CMS as draft (never auto-publishes).

---

## Getting Started with Sanity

**If you have an existing Sanity account, here's how to get started:**

### Step 1: Get Sanity Credentials

From your Sanity project dashboard:

1. **Project ID**: Found in project settings or URL
2. **Dataset**: Usually `production`
3. **Read Token**: API → Tokens → Add New Token (Viewer role)
4. **Write Token** (optional): Add New Token (Editor role)

### Step 2: Create Initial Config

Create `.kurt/cms-config.json`:

```json
{
  "sanity": {
    "prod": {
      "project_id": "your-project-id",
      "dataset": "production",
      "token": "sk...your-read-token",
      "write_token": "sk...your-write-token",
      "base_url": "https://yoursite.com"
    }
  }
}
```

**Note:**
- The `.kurt/` directory is already gitignored, so your credentials are safe.
- You can configure multiple instances (prod, staging, etc.) per platform.

### Step 3: Run Onboarding

From Claude Code:
```
cms-interaction onboard
```

This discovers your content types and maps your custom field names.

### Step 4: Test Setup

```
cms-interaction search --limit 5
```

---

## Routing Logic

Routes to subskills based on first argument:

- `onboard` → subskills/onboard.md → `kurt cms onboard`
- `search` → subskills/search.md → `kurt cms search`
- `publish` → subskills/publish.md → `kurt cms publish`

Each subskill:
1. Parses user parameters
2. Constructs appropriate `kurt cms` command
3. Executes command
4. Provides follow-up guidance

---

## Integration with Core Workflow

### Ad-hoc use (this skill):
- Quick searches during planning
- Exploring CMS content
- One-off document retrieval
- Publishing completed drafts

### Systematic ingestion (core workflow):
Use the unified map-then-fetch workflow orchestrated by project-management-skill:

```bash
# Discovery + clustering
kurt map cms --platform sanity --instance prod --cluster-urls

# Selective fetching
kurt fetch --include "sanity/prod/*"
kurt fetch --in-cluster "Tutorials"
kurt fetch --with-content-type article
```

**Benefits:**
- Same workflow as web content
- Cross-source clustering (web + CMS)
- Selective fetching by cluster or content type
- Integrated into project sources

See project-management-skill/subskills/gather-sources.md for full orchestration.

---

## Available Commands

All commands route to `kurt cms`:

### Configuration
```bash
cms-interaction onboard
→ kurt cms onboard --platform sanity
```

### Search
```bash
cms-interaction search --query "tutorial" --limit 20
→ kurt cms search --query "tutorial" --limit 20 --platform sanity
```

### Fetch (via CLI directly)
```bash
kurt cms fetch --id <document-id> --output-dir sources/cms/sanity/
```

### Types (via CLI directly)
```bash
kurt cms types --platform sanity
```

### Publish
```bash
cms-interaction publish --file draft.md --id <document-id>
→ kurt cms publish --file draft.md --id <document-id> --platform sanity
```

### Import (via CLI directly)
```bash
kurt cms import --source-dir sources/cms/sanity/
```

---

## Configuration Format

After onboarding, `.kurt/cms-config.json` contains:

```json
{
  "sanity": {
    "prod": {
      "project_id": "abc123",
      "dataset": "production",
      "token": "sk...",
      "write_token": "sk...",
      "base_url": "https://yoursite.com",

      "content_type_mappings": {
        "article": {
          "enabled": true,
          "content_field": "content_body_portable",
          "title_field": "title",
          "slug_field": "slug.current",
          "description_field": "excerpt",
          "inferred_content_type": "article",
          "metadata_fields": {}
        },
        "universeItem": {
          "enabled": true,
          "content_field": "description",
          "title_field": "title",
          "slug_field": "slug.current",
          "description_field": "description",
          "inferred_content_type": "reference",
          "metadata_fields": {}
        }
      }
    }
  }
}
```

**Key fields:**
- `slug_field`: Used in semantic URLs for clustering
- `description_field`: Provides context for topic clustering
- `inferred_content_type`: Auto-assigned from schema name, skips LLM classification

---

## Relationship with Other Skills

### project-management-skill
Orchestrates systematic CMS ingestion:
- Calls `kurt map cms --cluster-urls` for discovery
- Uses `kurt fetch --include "sanity/*"` for bulk download
- Integrates CMS with web content in same workflow

### content-writing-skill
Consumes CMS content:
- References CMS documents in project sources
- Creates drafts for CMS publishing
- Uses `cms-interaction publish` to push back to CMS

### research-skill
Complements CMS search:
- research-skill: External research (Perplexity AI)
- cms-interaction: Internal content search (CMS)

---

## Troubleshooting

### "Platform not configured"
```bash
cms-interaction onboard
```

### "Connection failed"
- Check credentials in `.kurt/cms-config.json`
- Verify tokens in Sanity dashboard
- Test connection: `kurt cms types --platform sanity`

### "No results found"
- Try broader search: `cms-interaction search --limit 20`
- Check enabled content types: `kurt cms types`
- Verify content types configured in onboarding

### "Write permission denied"
- Add `write_token` with Editor role to config
- Regenerate token in Sanity dashboard

---

*For detailed subskill documentation, see subskills/*.md files.*
