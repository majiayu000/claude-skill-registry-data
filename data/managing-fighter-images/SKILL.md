---
name: managing-fighter-images
description: Use this skill when working with UFC fighter images including downloading from multiple sources (Wikimedia, Sherdog, Bing), detecting and replacing placeholder images, handling duplicates, normalizing image sizes, validating image quality, syncing filesystem to database, or running the complete image pipeline. Handles missing images, batch downloads, and multi-source orchestration.
---

You are an expert at managing the UFC Pokedex fighter image pipeline, which involves downloading, validating, normalizing, and maintaining fighter photos from multiple sources.

# Image Pipeline Overview

The image pipeline supports multiple sources with priority ordering:
```
Wikimedia Commons (legal, ~20% coverage)
    ↓ (if not found)
Sherdog (high UFC coverage, requires mapping)
    ↓ (if not found)
Bing Image Search (fallback)
    ↓
Database update → Normalization → Validation
```

# When to Use This Skill

Invoke this skill when the user wants to:
- Download missing fighter images
- Replace placeholder images from Sherdog
- Detect duplicate fighter photos
- Normalize images to consistent size/format
- Validate image quality
- Sync filesystem images to database
- Run complete image workflow
- Review recently downloaded images

# Image Sources

## 1. Wikimedia Commons (Preferred)
**Coverage:** ~20% of UFC fighters
**Legal Status:** ✅ Public domain / Creative Commons
**Quality:** High (official UFC or press photos)

**Use for:**
- First choice for any fighter
- Legal, high-quality images
- No copyright concerns

## 2. Sherdog
**Coverage:** High for UFC fighters
**Legal Status:** ⚠️ Fair use (third-party site)
**Quality:** Variable, includes placeholders

**Note:** Requires fighter ID mapping in `data/sherdog_id_mapping.json`

**Known issue:** ~266+ placeholder images (generic silhouette)

## 3. Bing Image Search
**Coverage:** Universal fallback
**Legal Status:** ⚠️ Varies by source
**Quality:** Variable

**Use for:**
- Replacing Sherdog placeholders
- Last resort when other sources fail

# Available Operations

## Complete Workflows

### Sherdog Workflow (Multi-step)
Complete workflow for downloading images from Sherdog.

**Command:**
```bash
make sherdog-workflow
```

**Interactive steps:**
1. Export fighters to CSV
2. Search Sherdog for matches
3. Verify matches manually
4. Scrape photos from Sherdog
5. Update database with Sherdog IDs

**Expected duration:** 30-60 minutes (manual review required)

**Output:**
- `data/sherdog_id_mapping.json` - Fighter to Sherdog ID mapping
- `data/images/fighters/*.jpg` - Downloaded images

### Multi-source Orchestrator
Tries multiple sources automatically in priority order.

**Command:**
```bash
make scrape-images-orchestrator
```

**What it does:**
1. Finds fighters without images
2. Tries Wikimedia Commons first
3. Falls back to Sherdog (if mapping exists)
4. Falls back to Bing search
5. Downloads and saves images
6. Updates database

**Best for:** Bulk image acquisition with automatic fallback

## Individual Operations

### 1. Download Missing Images (Wikimedia)

**Command:**
```bash
make scrape-images-wikimedia
```

**What it does:**
- Searches Wikimedia Commons for fighters missing images
- Downloads public domain images
- Updates database with image URLs
- ~20% success rate

**Use when:**
- Prefer legal, high-quality images
- First attempt at filling missing images

### 2. Update Fighter Images (Sherdog)

**Command:**
```bash
make update-fighter-images
```

**What it does:**
- Uses existing Sherdog ID mapping
- Downloads images from Sherdog
- Updates database

**Prerequisite:** Sherdog mapping must exist (`data/sherdog_id_mapping.json`)

### 3. Detect Placeholder Images

Sherdog uses generic placeholder images for some fighters.

**Command:**
```bash
make detect-placeholders
```

**What it does:**
- Uses perceptual hashing to detect Sherdog placeholders
- Marks placeholders in database
- Generates report of affected fighters

**Output:** List of fighter IDs with placeholder images

### 4. Replace Placeholder Images

Replace Sherdog placeholders with Bing image search results.

**Command options:**
```bash
# Replace batch of 50 placeholders
make replace-placeholders

# Replace ALL placeholders (may take 1+ hours)
make replace-placeholders-all
```

**What it does:**
- Searches Bing for fighter images
- Downloads better images
- Replaces placeholder files
- Updates database

**Use when:**
- Detected placeholders exist
- Want higher quality images

### 5. Verify Replacement

After replacing placeholders, verify the new images.

**Command:**
```bash
make verify-replacement
```

**What it does:**
- Shows recently replaced images (last 2 hours)
- Validates new images loaded correctly
- Compares before/after

### 6. Detect Duplicate Photos

Some fighters may have duplicate/similar images.

**Command:**
```bash
make review-duplicates
```

**What it does:**
- Uses perceptual hashing to find similar images
- Opens interactive review with image previews
- Allows manual decision on keeping/removing

**Use when:**
- Cleaning up image library
- Reducing storage usage
- Ensuring unique fighter photos

### 7. Normalize Images

Standardize all images to consistent format and size.

**Command options:**
```bash
# Preview normalization (dry-run)
make normalize-images-dry-run

# Apply normalization
make normalize-images
```

**What it does:**
- Resizes images to 300x300 pixels
- Converts to JPEG format
- Optimizes file size
- Preserves aspect ratio with padding

**Use when:**
- Images have inconsistent sizes
- Need to reduce storage
- Preparing for deployment

### 8. Validate Images

Run quality checks on all fighter images.

**Command:**
```bash
make validate-images
```

**What it does:**
- Checks files exist and are readable
- Validates JPEG format
- Checks minimum resolution
- Detects corrupted files
- Reports issues

**Use when:**
- After bulk downloads
- Before deployment
- Troubleshooting image issues

### 9. Sync Images to Database

Sync filesystem images with database records.

**Command:**
```bash
make sync-images-to-db
```

**What it does:**
- Scans `data/images/fighters/` directory
- Finds images not in database
- Finds database records with missing files
- Updates database to match filesystem
- Reports additions and deletions

**Use when:**
- Manual image additions/removals
- Database and filesystem out of sync
- After external image processing

### 10. Review Recent Images

Preview recently downloaded images.

**Command:**
```bash
make review-recent-images
```

**What it does:**
- Shows images downloaded in last 24 hours
- Opens in image viewer for manual review
- Helps catch bad downloads early

**Use when:**
- After bulk downloads
- Quality assurance check

### 11. Remove Bad Images

Remove specific images and reset database records.

**Command:**
```bash
make remove-bad-images
```

**⚠️ WARNING:** This command requires manual editing of the script first!

**What it does:**
- Removes specified image files
- Clears database image_url for those fighters
- Allows re-download

**Use when:**
- Downloaded wrong images
- Image quality unacceptable
- Need to re-download specific fighters

**Important:** Edit `scripts/remove_bad_images.py` to specify fighter IDs before running!

# Complete Pipeline Workflow

## Workflow: Fill All Missing Images

Use this to maximize image coverage from all sources.

**Steps:**
```bash
# 1. Check current status
PGPASSWORD=ufc_pokedex psql -h localhost -U ufc_pokedex -d ufc_pokedex -c \
  "SELECT
     COUNT(*) FILTER (WHERE image_url IS NOT NULL) as with_images,
     COUNT(*) FILTER (WHERE image_url IS NULL) as without_images,
     COUNT(*) as total
   FROM fighters;"

# 2. Try Wikimedia first (legal, high-quality)
make scrape-images-wikimedia

# 3. Run multi-source orchestrator for remainder
make scrape-images-orchestrator

# 4. If still have gaps, run Sherdog workflow
make sherdog-workflow

# 5. Detect and replace Sherdog placeholders
make detect-placeholders
make replace-placeholders-all

# 6. Normalize all images to consistent format
make normalize-images-dry-run   # Preview first
make normalize-images            # Apply

# 7. Validate everything
make validate-images

# 8. Sync to database
make sync-images-to-db

# 9. Review recent downloads
make review-recent-images

# 10. Check final status
PGPASSWORD=ufc_pokedex psql -h localhost -U ufc_pokedex -d ufc_pokedex -c \
  "SELECT
     COUNT(*) FILTER (WHERE image_url IS NOT NULL) as with_images,
     COUNT(*) FILTER (WHERE image_url IS NULL) as without_images,
     ROUND(100.0 * COUNT(*) FILTER (WHERE image_url IS NOT NULL) / COUNT(*), 1) as coverage_percent
   FROM fighters;"
```

**Expected duration:** 2-4 hours total
**Expected coverage:** 80-95% of fighters

## Workflow: Replace Bad/Placeholder Images

Use this to improve image quality after initial scraping.

**Steps:**
```bash
# 1. Detect Sherdog placeholders
make detect-placeholders

# 2. Review report
cat data/placeholder_report.json   # or wherever report is saved

# 3. Replace placeholders (batch of 50)
make replace-placeholders

# 4. Verify replacements
make verify-replacement

# 5. Repeat until all placeholders replaced
make replace-placeholders-all

# 6. Normalize replaced images
make normalize-images

# 7. Validate quality
make validate-images
```

## Workflow: Clean Up Image Library

Use this for maintenance and quality improvement.

**Steps:**
```bash
# 1. Find and review duplicates
make review-duplicates

# 2. Validate all images
make validate-images

# 3. Normalize inconsistent images
make normalize-images-dry-run   # Check what will change
make normalize-images            # Apply changes

# 4. Sync database to match filesystem
make sync-images-to-db

# 5. Remove any bad images (edit script first!)
# Edit scripts/remove_bad_images.py with fighter IDs
make remove-bad-images

# 6. Re-download removed images
make scrape-images-orchestrator
```

# Image Storage

**Location:** `data/images/fighters/`

**Naming convention:** `{fighter_id}.jpg`

**Format requirements:**
- JPEG format
- 300x300 pixels (after normalization)
- RGB color space
- File size: typically 20-80 KB after optimization

**Database field:** `fighters.image_url` stores relative path (e.g., `/images/fighters/{id}.jpg`)

# Database Queries

### Check image coverage:
```sql
SELECT
  COUNT(*) FILTER (WHERE image_url IS NOT NULL) as with_images,
  COUNT(*) FILTER (WHERE image_url IS NULL) as without_images,
  ROUND(100.0 * COUNT(*) FILTER (WHERE image_url IS NOT NULL) / COUNT(*), 1) as coverage_percent
FROM fighters;
```

### Find fighters missing images:
```sql
SELECT id, name, nickname, division
FROM fighters
WHERE image_url IS NULL
ORDER BY name
LIMIT 20;
```

### Find fighters with images:
```sql
SELECT id, name, image_url
FROM fighters
WHERE image_url IS NOT NULL
ORDER BY created_at DESC
LIMIT 20;
```

### Check for placeholders (if marked in DB):
```sql
SELECT id, name, image_url
FROM fighters
WHERE image_url LIKE '%placeholder%';
```

# Common Issues and Solutions

### Issue: "Sherdog mapping file not found"
**Solution:**
Run the Sherdog workflow first to create the mapping:
```bash
make sherdog-workflow
```

### Issue: Low success rate from Wikimedia
**Expected:** Only ~20% coverage from Wikimedia
**Solution:** This is normal. Use multi-source orchestrator or Sherdog workflow for better coverage.

### Issue: Many placeholder images detected
**Solution:**
Replace placeholders with Bing search:
```bash
make detect-placeholders
make replace-placeholders-all
```

### Issue: Images different sizes causing layout issues
**Solution:**
Normalize all images to 300x300:
```bash
make normalize-images
```

### Issue: Database shows image but file doesn't exist
**Solution:**
Sync database to filesystem:
```bash
make sync-images-to-db
```

### Issue: Downloaded wrong image for fighter
**Solution:**
1. Edit `scripts/remove_bad_images.py` with fighter ID
2. Run `make remove-bad-images`
3. Re-download: `make scrape-images-orchestrator`

### Issue: Duplicate images for same fighter
**Solution:**
```bash
make review-duplicates
# Follow interactive prompts to remove duplicates
```

### Issue: Images failing validation
**Solution:**
```bash
# Check validation report
make validate-images

# Remove invalid images (edit script first)
# Edit scripts/remove_bad_images.py
make remove-bad-images

# Re-download
make scrape-images-orchestrator
```

# Image Quality Guidelines

### Good Images:
✅ Clear face visible
✅ Official UFC photo or press photo
✅ Professional quality
✅ Good lighting
✅ At least 300x300 resolution
✅ JPEG format

### Bad Images:
❌ Blurry or low resolution
❌ Face obscured or cut off
❌ Action shots where face not clear
❌ Wrong person
❌ Generic placeholder
❌ Copyright watermarks
❌ Non-square aspect ratio (before normalization)

# Best Practices

1. **Start with Wikimedia** - Legal and high quality
2. **Use orchestrator for bulk** - Automatic fallback to multiple sources
3. **Detect placeholders early** - Don't let them accumulate
4. **Normalize after downloading** - Consistent sizes for frontend
5. **Validate frequently** - Catch bad downloads early
6. **Review recent downloads** - Manual QA check
7. **Sync regularly** - Keep database and filesystem in sync
8. **Back up before bulk operations** - Can't undo bulk deletions
9. **Use dry-run first** - Preview changes before applying
10. **Handle duplicates proactively** - Saves storage and confusion

# Progress Monitoring

### Monitor downloads:
```bash
# Watch image count grow
watch -n 5 'ls data/images/fighters/*.jpg 2>/dev/null | wc -l'

# Check database count
watch -n 5 'psql -U ufc_pokedex -d ufc_pokedex -tAc "SELECT COUNT(*) FROM fighters WHERE image_url IS NOT NULL;"'
```

### Check script logs:
Most scripts output progress to console. Watch for:
- Success/failure counts
- Error messages
- Warnings about placeholders
- Validation failures

# Limitations

- **Wikimedia coverage limited** - Only ~20% of UFC fighters
- **Sherdog requires mapping** - Manual matching process
- **Bing rate limiting** - Slow for large batches
- **No automatic updates** - Must manually trigger re-downloads
- **Legal uncertainty** - Sherdog/Bing images may have copyright issues
- **Placeholder detection** - Perceptual hashing may have false positives
- **Manual review required** - Some steps need human verification

# Quick Reference

```bash
# Complete image pipeline
make scrape-images-wikimedia && \
make scrape-images-orchestrator && \
make detect-placeholders && \
make replace-placeholders-all && \
make normalize-images && \
make validate-images && \
make sync-images-to-db

# Check coverage
psql -U ufc_pokedex -d ufc_pokedex -c "SELECT COUNT(*) FILTER (WHERE image_url IS NOT NULL) * 100.0 / COUNT(*) as coverage_pct FROM fighters;"

# Quick status
ls data/images/fighters/*.jpg | wc -l   # File count
```

# Related Skills

- See `scraping-data-pipeline` skill for scraping fighter data
- See `managing-dev-environment` skill for database setup
