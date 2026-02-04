---
name: supabase-operations
description: This skill should be used when the user asks to "list posters", "get poster info", "fetch context document", "get latest poster", "check poster count", "show poster details", "get context for poster", "show enrichment quality", "diagnose enrichment", "show pulse script", "get all poster data", "check what data we have", or mentions Supabase, posters, context documents, enrichment, or database queries. Provides commands and scripts for querying Local Pulse poster data from Supabase.
version: 2.0.0
---

# Supabase Operations for Local Pulse

## Overview

Local Pulse uses Supabase PostgreSQL for data storage with two environments:
- **Staging**: `SUPABASE_DATABASE_URL` - for development/testing
- **Production**: `SUPABASE_DATABASE_URL_PROD` - for live data

All scripts are **read-only** and located in `scripts/supabase/`.

---

## Quick Reference

| What you want | Command |
|---------------|---------|
| List all posters | `poetry run python scripts/supabase/list_posters.py --prod` |
| Get latest poster summary | `poetry run python scripts/supabase/get_latest_poster.py --prod` |
| Get ALL data for latest poster | `poetry run python scripts/supabase/show_all_poster_data.py --latest --prod` |
| Get context document | `poetry run python scripts/supabase/get_context_document.py --latest --prod` |
| Diagnose enrichment quality | `poetry run python scripts/supabase/show_enrichment_quality.py --latest --prod` |
| Show compiled Pulse Script | `poetry run python scripts/supabase/show_pulse_script.py --latest --prod` |
| Get specific poster by ID | `poetry run python scripts/supabase/get_poster.py <poster_id> --prod` |

---

## Available Scripts

### 1. `list_posters.py` - List All Posters

Lists all posters with count, status, and summary stats.

```bash
poetry run python scripts/supabase/list_posters.py --prod
poetry run python scripts/supabase/list_posters.py --prod --limit 10
```

**Output**: Table with poster IDs, status, creation date, uploader + status breakdown.

---

### 2. `get_latest_poster.py` - Latest Poster Summary

Quick overview of the most recent poster.

```bash
poetry run python scripts/supabase/get_latest_poster.py --prod
poetry run python scripts/supabase/get_latest_poster.py --prod --full  # includes context doc
```

**Output**: Poster metadata, user inputs, event info, user-provided URLs.

---

### 3. `show_all_poster_data.py` - ALL Database Fields ⭐

**The comprehensive script** - shows EVERY field from ALL related tables.

```bash
poetry run python scripts/supabase/show_all_poster_data.py --latest --prod
poetry run python scripts/supabase/show_all_poster_data.py <poster_id> --prod
```

**Output includes ALL fields from**:
- `posters` table (status, vision, OCR, website, costs, editing)
- `vision_analysis` table (context document, extracted entities/events)
- `events` table (all event details, pricing, schedule)
- `entities` table (all entities with Spotify, Google Places, social media data)
- Compiled Pulse Script

---

### 4. `get_context_document.py` - Context Document

Fetches the enriched context document.

```bash
poetry run python scripts/supabase/get_context_document.py --latest --prod
poetry run python scripts/supabase/get_context_document.py <poster_id> --prod
```

**Output**: Full context document content + OCR poster text.

---

### 5. `show_enrichment_quality.py` - Quality Diagnosis ⭐

**Diagnose enrichment quality** - shows what was found vs. what's missing.

```bash
poetry run python scripts/supabase/show_enrichment_quality.py --latest --prod
poetry run python scripts/supabase/show_enrichment_quality.py <poster_id> --prod
```

**Output includes**:
- User inputs quality score
- Vision analysis quality score
- Context document sections check
- Event completeness per event
- Entity enrichment coverage (Spotify, Google Places, etc.)
- Pulse Script analysis
- Cost summary

---

### 6. `show_pulse_script.py` - Compiled Pulse Script

Shows the LLM-generated markdown for the event page.

```bash
poetry run python scripts/supabase/show_pulse_script.py --latest --prod
poetry run python scripts/supabase/show_pulse_script.py <poster_id> --prod
```

**Output**: Full Pulse Script + analysis (entity refs, sections present).

---

### 7. `get_poster.py` - Poster Details by ID

Basic poster info with events and entities summary.

```bash
poetry run python scripts/supabase/get_poster.py <poster_id> --prod
```

---

## Common Workflows

### "I just enriched a poster, show me everything"

```bash
# Full data dump
poetry run python scripts/supabase/show_all_poster_data.py --latest --prod

# Or quality focused
poetry run python scripts/supabase/show_enrichment_quality.py --latest --prod
```

### "What's in production?"

```bash
poetry run python scripts/supabase/list_posters.py --prod
```

### "Check if enrichment worked properly"

```bash
poetry run python scripts/supabase/show_enrichment_quality.py --latest --prod
```

### "Show me the context document"

```bash
poetry run python scripts/supabase/get_context_document.py --latest --prod
```

### "Show me the Pulse Script"

```bash
poetry run python scripts/supabase/show_pulse_script.py --latest --prod
```

### "Get all data for a specific poster"

```bash
POSTER_ID="31ad6cba-1dec-4789-8ecc-57b1ee35422f"
poetry run python scripts/supabase/show_all_poster_data.py $POSTER_ID --prod
```

---

## Database Schema Reference

### `posters` Table
Core poster data including:
- **Identity**: poster_id, file_path, status, owner_id
- **User Inputs**: user_provided_urls, location_hint, extra_context, ticketing_url
- **Vision**: vision_status, overall_theme, visual_style, atmosphere_tags, audience_tags
- **OCR**: poster_text, word_count, ocr_confidence, ocr_strategy
- **Website**: website_url, website_source, website_content
- **Processing**: enrichment_providers, cost_summary, processing_date
- **Output**: compiled_pulse_script, compiled_at
- **Editing**: uploaded_by, last_edited_by, last_edited_at

### `vision_analysis` Table
- context_document (the big enriched document)
- extracted_entities, extracted_events (JSON)
- vision_model, prompt_version
- is_safe, rejection_reason

### `events` Table
- title, description, location
- event_datetime, event_end_datetime, door_time
- performers, pricing (JSON)
- status, age_restriction
- is_recurring, is_multi_day, is_cancelled, is_sold_out

### `entities` Table
- name, entity_type, confidence, event_role
- spotify (JSON with followers, popularity, genres, top tracks)
- google_places (JSON with rating, address, phone)
- social_media (JSON with Instagram, Facebook, etc.)
- google_kg, tavily, google_cse (additional enrichment)

---

## Environment Setup

Add to `.env`:

```bash
# Staging (default)
SUPABASE_DATABASE_URL=postgresql://...

# Production (use --prod flag)
SUPABASE_DATABASE_URL_PROD=postgresql://...
```

---

## Flags Reference

| Flag | Description |
|------|-------------|
| `--prod` | Use production database (SUPABASE_DATABASE_URL_PROD) |
| `--latest` | Use the most recently created poster |
| `--full` | Show extended details (context doc, etc.) |
| `--limit N` | Limit number of results |

---

## Troubleshooting

### "No context document yet"
The poster hasn't been enriched. Check `status` field - should be `enriched` or `compiled`.

### "Connection failed"
Check that `SUPABASE_DATABASE_URL_PROD` is set in `.env`.

### "Missing enrichment data"
Run `show_enrichment_quality.py` to diagnose what's missing and why.

---

## CRITICAL: Local Supabase Migration Safety

### NEVER Do These (Data Loss Risk)

| Action | Result |
|--------|--------|
| Rename an applied migration file | Forces `db reset` = **ALL DATA LOST** |
| Delete an applied migration file | Inconsistent state, likely requires reset |
| Edit an applied migration file | Changes won't apply, schema drift |
| Run `supabase db reset` without asking | **ALL DATA LOST** |

### Migration File Rules

```bash
# FORBIDDEN - renaming existing migration:
mv supabase/migrations/20241228000000_foo.sql supabase/migrations/20241228010000_foo.sql

# CORRECT - create NEW migration for changes:
supabase migration new my_changes
# Then edit the new file
```

### Safe vs Destructive Commands

**Safe (no confirmation needed):**
```bash
supabase start
supabase stop
supabase status
supabase migration new <name>
supabase migration list
supabase db diff
```

**DESTRUCTIVE (MUST ask user first):**
```bash
supabase db reset        # Wipes ALL data
supabase stop --no-backup
supabase db push --force
```

### Before ANY Migration Work

1. Check current state: `supabase migration list`
2. Never rename/delete existing migration files
3. Always create NEW migrations for schema changes
4. If timestamp conflicts: use a different timestamp, don't rename

### If Migrations Get Out of Sync

Ask user: **"This will DELETE ALL DATA in local Supabase. Continue?"**

```bash
# Only after explicit user approval:
supabase db reset
```

---

## Local Development Quick Reference

### Start Local Supabase
```bash
./scripts/local/start.sh
# Or manually:
supabase start
```

### Check Status
```bash
supabase status
psql "postgresql://postgres:postgres@127.0.0.1:54322/postgres" -c "SELECT COUNT(*) FROM posters;"
```

### Local vs Production URLs
```
Local:      postgresql://postgres:postgres@127.0.0.1:54322/postgres
Production: postgresql://postgres.[project-id]:[pass]@aws-0-[region].pooler.supabase.com:6543/postgres
```

### Storage Buckets
Local Supabase needs buckets created manually. Check `supabase/config.toml` or create via SQL:
```sql
INSERT INTO storage.buckets (id, name, public) 
VALUES ('drafts', 'drafts', true) ON CONFLICT DO NOTHING;
```
