---
name: scraping-data-pipeline
description: Use this skill when scraping UFC fighter data from UFCStats.com, validating scraped data, loading data into the database, or running the complete scraping pipeline. Handles fighters list, fighter details, events, and fight history. Includes data validation, error recovery, cache invalidation, and progress reporting.
---

You are an expert at orchestrating the UFC Pokedex scraping pipeline, which involves multiple steps from data collection to database loading.

# Pipeline Overview

The scraping pipeline follows this flow:
```
UFCStats.com → Scrapy Spiders → JSON/JSONL files → Validation → Database → Cache Invalidation
```

# When to Use This Skill

Invoke this skill when the user wants to:
- Scrape fighter data (list or details)
- Load scraped data into the database
- Validate scraped JSON/JSONL files
- Run the complete scraping pipeline
- Handle missing or failed scrapes
- Update fighter data from UFC Stats

# Available Operations

## 1. Scraping Operations

### Scrape Fighter List
Scrapes all fighter URLs from UFCStats.com alphabetical listing.

**Command:**
```bash
make scraper
```

**Output:** `data/processed/fighters_list.jsonl`

**What it does:**
- Crawls http://ufcstats.com/statistics/fighters alphabetically
- Extracts fighter IDs and basic info
- Saves to JSONL format (one fighter per line)
- Takes ~5-10 minutes for full list

### Scrape Fighter Details
Scrapes detailed information for specific fighters.

**Command options:**
```bash
# Sample scrape (single fighter for testing)
make scrape-sample

# All fighters from list
make scraper-details

# Specific fighters by ID
.venv/bin/scrapy crawl fighter_detail -a fighter_ids=id1,id2,id3

# Specific fighters by URL
.venv/bin/scrapy crawl fighter_detail -a fighter_urls=url1,url2
```

**Output:** `data/processed/fighters/{id}.json` (individual files)

**What it scrapes:**
- Personal info (name, nickname, DOB, height, weight, reach, stance)
- Complete fight history with results
- Career statistics
- Current record (W-L-D)

## 2. Data Loading Operations

### Load Sample Data (SQLite-safe)
Loads first 8 fighters from fixtures for quick testing.

**Command:**
```bash
make api:seed
```

**Use when:**
- Testing on SQLite
- Need quick test data
- Developing new features

### Load All Scraped Data
Loads complete scraped dataset into database.

**Command:**
```bash
make load-data
```

**Use when:**
- Have full scraped dataset
- Running PostgreSQL
- Need production data

**Safety note:** Blocked on SQLite by default (10K+ fighters). Override with:
```bash
ALLOW_SQLITE_PROD_SEED=1 make api:seed-full
```

### Load Sample of Scraped Data
Loads only first N fighters for testing.

**Command:**
```bash
make load-data-sample
```

**Use when:**
- Testing with realistic data
- Need more than 8 fighters but not full dataset
- Validating data loading logic

## 3. Data Validation

Before loading, validate the scraped data:

**Steps:**
1. Check files exist:
   ```bash
   ls -lh data/processed/fighters_list.jsonl
   ls -lh data/processed/fighters/*.json | wc -l
   ```

2. Validate JSONL structure:
   ```bash
   head -5 data/processed/fighters_list.jsonl | jq '.'
   ```

3. Check for parsing errors:
   ```bash
   grep -i "error\|exception" data/processed/fighters_list.jsonl
   ```

4. Count records:
   ```bash
   wc -l data/processed/fighters_list.jsonl
   ```

# Complete Pipeline Workflows

## Workflow 1: Full Scrape and Load (PostgreSQL)

Use this for complete data refresh on PostgreSQL.

**Steps:**
```bash
# 1. Ensure PostgreSQL is running
docker-compose up -d

# 2. Scrape fighter list (~5-10 min)
make scraper

# 3. Validate fighter list
wc -l data/processed/fighters_list.jsonl
head -3 data/processed/fighters_list.jsonl | jq '.'

# 4. Scrape fighter details (~30-60 min for all)
make scraper-details

# 5. Validate detail files
ls data/processed/fighters/*.json | wc -l

# 6. Load into database
make load-data

# 7. Verify in database
PGPASSWORD=ufc_pokedex psql -h localhost -p 5432 -U ufc_pokedex -d ufc_pokedex -c "SELECT COUNT(*) FROM fighters;"

# 8. Restart backend to invalidate cache
pkill -f uvicorn
make api
```

**Expected duration:** 40-90 minutes total

## Workflow 2: Sample Scrape and Load (Quick Test)

Use this for quick testing or development.

**Steps:**
```bash
# 1. Start with SQLite (no Docker needed)
USE_SQLITE=1

# 2. Scrape sample fighter
make scrape-sample

# 3. Seed with fixtures
make api:seed

# 4. Start backend
make api:dev

# 5. Verify
curl http://localhost:8000/fighters/ | jq '.fighters | length'
```

**Expected duration:** 2-3 minutes total

## Workflow 3: Update Specific Fighters

Use this to refresh data for specific fighters.

**Steps:**
```bash
# 1. Get fighter IDs that need updating
# (from database or fighters_list.jsonl)

# 2. Scrape specific fighters
.venv/bin/scrapy crawl fighter_detail -a fighter_ids=id1,id2,id3

# 3. Reload just those fighters
# (Currently requires full reload - see limitations below)
make load-data

# 4. Restart backend
pkill -f uvicorn && make api
```

## Workflow 4: Handle Missing/Failed Scrapes

If some fighters failed to scrape:

**Steps:**
```bash
# 1. Find fighters with missing detail files
# Compare fighters_list.jsonl count vs. fighters/*.json count
TOTAL=$(wc -l < data/processed/fighters_list.jsonl)
SCRAPED=$(ls data/processed/fighters/*.json 2>/dev/null | wc -l)
echo "Total: $TOTAL, Scraped: $SCRAPED, Missing: $((TOTAL - SCRAPED))"

# 2. Identify missing IDs
# (You may need to write a quick script)

# 3. Re-scrape missing fighters
.venv/bin/scrapy crawl fighter_detail -a fighter_ids=missing_id1,missing_id2

# 4. Reload data
make load-data
```

# Cache Management

After loading data, invalidate Redis cache (if using Redis):

**Commands:**
```bash
# Check Redis connection
redis-cli ping

# Clear all fighter-related cache
redis-cli KEYS "fighters:*" | xargs redis-cli DEL

# Or clear entire cache
redis-cli FLUSHDB
```

**Note:** Backend gracefully degrades if Redis is unavailable, so cache clearing is optional.

# Error Handling

## Common Issues and Solutions

### Issue: "No such file or directory: data/processed/fighters_list.jsonl"
**Solution:** Run `make scraper` first to create the fighter list.

### Issue: Scraper fails with connection errors
**Solution:**
- Check internet connection
- Verify UFCStats.com is accessible
- Reduce concurrent requests in `scraper/settings.py`
- Add delays: `SCRAPER_DELAY_SECONDS=2.0`

### Issue: Database constraint violations during load
**Solution:**
- Drop and recreate database: `make db-reset`
- Check for duplicate IDs in scraped data
- Validate JSON structure

### Issue: "Blocked on SQLite" when loading full dataset
**Solution:**
- Use PostgreSQL for production data: `docker-compose up -d`
- Or override safety check: `ALLOW_SQLITE_PROD_SEED=1 make api:seed-full`

### Issue: Partial scrapes (some fighters missing)
**Solution:**
- Use Workflow 4 above to identify and re-scrape missing fighters
- Check scraper logs for errors
- Verify HTML structure hasn't changed on UFCStats.com

# Data Validation Checklist

Before loading, verify:

- [ ] `fighters_list.jsonl` exists and has expected count (~1000-2000 fighters)
- [ ] Each line in JSONL is valid JSON
- [ ] Fighter detail JSON files exist in `data/processed/fighters/`
- [ ] Sample fighter JSON has required fields: `id`, `name`, `record`
- [ ] No parsing errors in JSON files
- [ ] Database is running (PostgreSQL) or SQLite mode enabled
- [ ] Database schema is up to date: `make db-upgrade`

# Progress Monitoring

### Monitor scraping progress:
```bash
# Watch fighter details being created
watch -n 5 'ls data/processed/fighters/*.json | wc -l'

# Check scrapy logs
tail -f scrapy.log
```

### Monitor database loading:
```bash
# Check fighter count in database
PGPASSWORD=ufc_pokedex psql -h localhost -p 5432 -U ufc_pokedex -d ufc_pokedex -c "SELECT COUNT(*) FROM fighters;"

# Check recent inserts
PGPASSWORD=ufc_pokedex psql -h localhost -p 5432 -U ufc_pokedex -d ufc_pokedex -c "SELECT name, record, created_at FROM fighters ORDER BY created_at DESC LIMIT 10;"
```

# Best Practices

1. **Always validate before loading** - Check JSONL structure and counts
2. **Use sample loads for testing** - Don't load 10K fighters into SQLite
3. **Monitor scraping progress** - Scrapy can fail silently on some fighters
4. **Respect rate limits** - UFCStats.com should not be hammered
5. **Clear cache after loading** - Ensure API serves fresh data
6. **Back up before full reload** - Database drops and recreates tables
7. **Test with sample first** - Validate pipeline with `make scrape-sample`

# Limitations

- **Incremental updates not supported** - Must reload all data (no upsert logic yet)
- **No automatic scheduling** - Must trigger scrapes manually
- **No fighter image scraping** - Images handled separately (see `managing-fighter-images` skill)
- **SQLite safety checks** - Full dataset blocked on SQLite (design choice)
- **No event scraping yet** - Events spider exists but not integrated

# Quick Reference

```bash
# Full pipeline (PostgreSQL)
make scraper && make scraper-details && make load-data

# Quick test (SQLite)
make scrape-sample && make api:seed && make api:dev

# Validate data
wc -l data/processed/fighters_list.jsonl
ls data/processed/fighters/*.json | wc -l

# Clear cache
redis-cli FLUSHDB

# Check database
PGPASSWORD=ufc_pokedex psql -h localhost -U ufc_pokedex -d ufc_pokedex -c "SELECT COUNT(*) FROM fighters;"
```
