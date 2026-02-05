---
name: documentation-asset-manager
description: Manages Tallyfy documentation assets on Cloudflare R2. Uploads images, generates AI captions using Claude Code native vision, maintains CSV inventory with build-time integration. Use when managing docs screenshots or media files.
version: 2.0.0
author: Tallyfy Dev Team
tags: [documentation, assets, r2, cloudflare, inventory, ai-captions, screenshots, vision, build-integration]
dependencies: [pillow, requests]
---

# Documentation Asset Manager

## Purpose

Automates the complete workflow for Tallyfy documentation asset management with Claude Code native vision:

1. **Upload assets** to Cloudflare R2 storage (screenshots bucket)
2. **Generate AI captions** using Claude Code native vision (alt text, descriptive, SEO)
3. **Maintain CSV inventory** at `$GITHUB_ROOT/documentation/documentation_assets.csv`
4. **Build-time integration** - Automatic alt text injection during Starlight builds
5. **Return public URLs** immediately (screenshots.tallyfy.com domain)
6. **Track asset usage** across documentation files

## Recent Updates (v2.0.0)

**✅ Completed:**
- **287 images captioned** with vision-based analysis (100% coverage for native images)
- **Claude Code native** - No external API key needed
- **Build-time integration** - Remark plugin auto-injects alt text from CSV
- **Parallel Task agents** - Batch processing support
- **Path portability** - Auto-detection, works on any developer machine

## Activation Triggers

- "upload documentation asset"
- "upload screenshot to R2"
- "add image to docs"
- "manage documentation media"
- "generate image caption"
- "update documentation screenshot"
- When user provides image/asset path for documentation

## Prerequisites

**Required Credentials** (in parent directory):
- `$GITHUB_ROOT/cloudflare_credentials.json` with fields:
  - `account_id` - Cloudflare account ID
  - `api_token` - Cloudflare API token with R2 access

**Required Packages** (auto-check):
```bash
pip3 install pillow requests
```

**Claude Code Native** (Recommended):
- **No external API key needed** - Uses Claude Code's native vision capabilities
- For batch operations: Use Task agents (see Batch Vision Captioning section)
- For single images: `image_captioner.py` uses subprocess to call claude native

## Instructions

### Step 1: Validate Prerequisites

```bash
# Check credentials exist
test -f $GITHUB_ROOT/cloudflare_credentials.json || echo "❌ Credentials missing"

# Check Anthropic API key
test -f ~/.anthropic/api_key || echo "⚠️ Set ANTHROPIC_API_KEY or create ~/.anthropic/api_key"

# Check Python packages
python3 -c "import anthropic, PIL, requests" 2>/dev/null || echo "⚠️ Run: pip3 install anthropic pillow requests"
```

### Step 2: Upload Asset to R2

Use the R2 uploader script to upload any file:

```bash
# Single file upload
python3 ~/.claude/skills/documentation-asset-manager/scripts/r2_uploader.py \
    --file /path/to/screenshot.png \
    --key "tallyfy/pro/desktop-light-new-feature.png" \
    --credentials $GITHUB_ROOT/cloudflare_credentials.json

# Returns JSON with public URL:
# {
#   "success": true,
#   "url": "https://screenshots.tallyfy.com/tallyfy/pro/desktop-light-new-feature.png",
#   "key": "tallyfy/pro/desktop-light-new-feature.png",
#   "size": "125.4KB"
# }
```

### Step 3: Generate AI Captions

Generate all three caption types using Claude Code native vision:

**For Single Images:**
```bash
# Generate captions using Claude Code native (no API key needed)
python3 ~/.claude/skills/documentation-asset-manager/scripts/image_captioner.py \
    --url "https://screenshots.tallyfy.com/tallyfy/pro/desktop-light-new-feature.png" \
    --output /tmp/captions.json

# Returns:
# {
#   "captions": {
#     "alt_text": "Task assignment interface showing user selection dropdown",
#     "descriptive": "Tallyfy task assignment screen with dropdown menu...",
#     "seo": "Tallyfy task assignment feature showing how to assign tasks..."
#   }
# }
```

**For Batch Operations (Recommended for >10 images):**
```bash
# Use Task agents for parallel processing
# See "Batch Vision Captioning" section below
```

### Step 4: Update CSV Inventory

Add asset to master inventory CSV:

```bash
# Add to inventory
python3 ~/.claude/skills/documentation-asset-manager/scripts/asset_inventory.py \
    --action add \
    --r2-key "tallyfy/pro/desktop-light-new-feature.png" \
    --url "https://screenshots.tallyfy.com/tallyfy/pro/desktop-light-new-feature.png" \
    --captions /tmp/captions.json \
    --article-ids "pro-tasks-assign,pro-getting-started"
```

### Step 5: Complete Workflow (Orchestrator)

For one-command complete workflow:

```bash
# Upload + Caption + Inventory in one go
python3 ~/.claude/skills/documentation-asset-manager/scripts/orchestrator.py \
    --file /path/to/screenshot.png \
    --key "tallyfy/pro/desktop-light-new-feature.png" \
    --article-ids "pro-tasks-assign" \
    --credentials $GITHUB_ROOT/cloudflare_credentials.json

# Complete output:
# ✅ Uploaded: https://screenshots.tallyfy.com/tallyfy/pro/desktop-light-new-feature.png
# ✅ Alt text: "Task assignment interface showing user selection dropdown"
# ✅ Added to inventory: $GITHUB_ROOT/documentation/documentation_assets.csv
```

## Build-Time Integration

**Automatic Alt Text Injection:**

The master CSV is integrated with Starlight documentation builds via a remark plugin:

**Location:** `/support-docs/src/plugins/remark/inject-alt-text.ts`

**How It Works:**
1. During build, remark plugin reads `/documentation/documentation_assets.csv`
2. Matches image URLs in markdown to CSV entries
3. Auto-injects `ai_caption_alt` as alt text
4. Handles URL encoding/decoding automatically
5. Falls back gracefully if CSV unavailable

**Local Development:**
```bash
cd /support-docs
# CSV symlinked to ../documentation/documentation_assets.csv
npm run dev  # Alt text injected automatically
```

**CI/CD (Netlify):**
```bash
# package.json prebuild script copies CSV
npm run prebuild  # Copies CSV before build
npm run build     # Alt text injected during build
```

**Example:**
```markdown
<!-- Before build: -->
![](https://screenshots.tallyfy.com/tallyfy/pro/desktop-light-tasks.png)

<!-- After build: -->
![Task list showing assignees and due dates](https://screenshots.tallyfy.com/tallyfy/pro/desktop-light-tasks.png)
```

## Batch Vision Captioning

**For Large-Scale Caption Regeneration:**

When regenerating captions for many images (>10), use parallel Task agents for efficiency:

**Process:**
1. **Prepare images** - Download and resize to max 1800px (Claude vision constraint)
2. **Launch Task agents** - Process in parallel batches of ~48 images
3. **Consolidate results** - Merge all batch outputs
4. **Update CSV** - Apply new captions to master inventory

**Example (287 images completed in ~60 minutes):**
```bash
# See /temporary/asset-inventory/ for reference implementation:
# - prepare_images_for_vision.py (download + resize)
# - Task agents launched in parallel (6 batches of ~48 images)
# - consolidate_and_update.py (merge results → CSV)
```

**Why Task Agents:**
- Native Claude Code vision (no API keys)
- Parallel processing (6x speedup)
- Automatic retry and error handling
- Real-time progress tracking

## Workflow Patterns

### Pattern 1: Upload New Screenshot

```bash
# User: "Upload this screenshot to docs"
# Skill detects image file path, generates reasonable R2 key from filename
# Executes: upload → generate captions → update inventory → return URL
```

### Pattern 2: Replace Existing Screenshot

```bash
# User: "Replace screenshot at /tallyfy/pro/desktop-light-tasks.png"
# Skill: uploads with same key (overwrites), regenerates captions, updates inventory
```

### Pattern 3: Batch Upload

```bash
# User: "Upload all screenshots in /docs/images/"
# Skill: processes each file sequentially with delays to avoid rate limits
```

### Pattern 4: Generate Caption Only

```bash
# User: "Generate caption for existing image at https://screenshots.tallyfy.com/..."
# Skill: skips upload, generates captions using Claude Code native, updates inventory
```

### Pattern 5: Regenerate All Captions (Completed)

```bash
# All 287 native images now have vision-based captions (completed 2025-11)
# Location: /documentation/documentation_assets.csv (columns: ai_caption_alt, ai_caption_descriptive, ai_caption_seo)
# Build integration: Auto-injected during Starlight builds via remark plugin
```

## Temporary Assets

**Working Directory:** `$GITHUB_ROOT/temporary/asset-manager/`

**Files Created:**
- `upload_result.json` - R2 upload response
- `captions_alt.json` - Alt text caption
- `captions_descriptive.json` - Descriptive caption
- `captions_seo.json` - SEO caption
- `asset_metadata.json` - Combined metadata
- `processing.log` - Processing log

**Cleanup:** Temporary files auto-cleaned after successful completion

## Master Asset Inventory

**Location:** `$GITHUB_ROOT/documentation/documentation_assets.csv`

**CSV Columns:**
- `filename` - Asset filename
- `r2_key` - Full R2 bucket key
- `production_url` - Public URL (screenshots.tallyfy.com)
- `source_type` - native|orphaned|external|missing
- `file_type` - File extension
- `file_size` - Human-readable size
- `file_size_bytes` - Size in bytes
- `url_exists` - Boolean (URL accessible)
- `article_ids` - Comma-separated article IDs
- `article_count` - Number of articles referencing
- `last_modified` - R2 last modified timestamp
- `etag` - R2 ETag
- `ai_caption_alt` - Alt text caption
- `ai_caption_descriptive` - Detailed caption
- `ai_caption_seo` - SEO-optimized caption
- `needs_caption` - yes|no (based on file type)

**Auto-Update:** CSV automatically updated on any upload/delete/caption operation

## Error Handling

### Scenario 1: Credentials Missing

```
ERROR: Credentials file not found
ACTION: Check $GITHUB_ROOT/cloudflare_credentials.json exists
PROMPT: "Cannot find Cloudflare credentials. Ensure file exists with:
         - account_id
         - api_token"
```

### Scenario 2: R2 Upload Fails

```
ERROR: R2 upload failed (API error)
ACTION: Retry once after 5s, then notify user
PROMPT: "Upload to R2 failed: {error_message}
         Retrying once..."
```

### Scenario 3: Caption Generation Fails

```
ERROR: Claude API error (rate limit, network, etc)
ACTION: Complete upload, skip caption, mark for later
PROMPT: "File uploaded successfully to {url}
         Caption generation failed: {error}
         You can generate captions later with:
         python3 scripts/image_captioner.py --url {url}"
```

### Scenario 4: Rate Limit Hit

```
ERROR: Anthropic API rate limit
ACTION: Wait 60s, retry once, then defer
PROMPT: "Rate limit reached. Waiting 60s before retry...
         If persistent, use --skip-captions flag to upload without captions"
```

### Scenario 5: Inventory CSV Locked

```
ERROR: CSV file in use (another process)
ACTION: Wait 2s, retry 3 times, then warn
PROMPT: "Inventory CSV busy. Retried 3 times. Upload succeeded but inventory not updated.
         Run: python3 scripts/asset_inventory.py --sync to update manually"
```

## Advanced Usage

### Skip Caption Generation

```bash
# For quick uploads without AI captions
python3 scripts/orchestrator.py --file screenshot.png --skip-captions
```

### Regenerate Captions for Existing Assets

```bash
# Regenerate all captions for specific asset
python3 scripts/image_captioner.py \
    --url "https://screenshots.tallyfy.com/tallyfy/pro/desktop-light-tasks.png" \
    --update-inventory
```

### Bulk Operations

```bash
# Process all images in directory
for img in /docs/screenshots/*.png; do
    python3 scripts/orchestrator.py --file "$img" --batch-mode
    sleep 3  # Delay between uploads
done
```

### Verify Inventory Integrity

```bash
# Check all URLs in inventory are accessible
python3 scripts/asset_inventory.py --verify-urls
```

### Generate Statistics

```bash
# Get inventory statistics
python3 scripts/asset_inventory.py --stats

# Output:
# Total assets: 812
# Active (used in docs): 290
# Orphaned (not referenced): 499
# Missing (404s): 23
# Images with captions: 288
```

## R2 Bucket Configuration

**Bucket Name:** `screenshots`
**Account ID:** `ac9046789c9ad74c8704a143b442f918`
**Public Domain:** `screenshots.tallyfy.com`
**API Endpoint:** `https://api.cloudflare.com/client/v4/accounts/{account_id}/r2/buckets/screenshots/objects`
**CDN:** Cloudflare global edge cache

## Naming Conventions

**Recommended R2 Key Patterns:**

1. **Structured (Preferred):**
   ```
   tallyfy/pro/desktop-light-{action}-{context}.png
   tallyfy/pro/mobile-dark-{feature}.png
   manufactory/{feature}-{version}.png
   ```

2. **Legacy (Auto-generated):**
   ```
   file-{random_id}.png
   ```

**Examples:**
- `tallyfy/pro/desktop-light-assign-task.png`
- `tallyfy/pro/desktop-light-sidebar-numerated.png`
- `manufactory-triggers-v2.png`

## Security Notes

- Credentials stored in parent directory (not in skill)
- No API keys embedded in skill files
- Anthropic API key from environment or user's ~/.anthropic/
- R2 bucket is private with public domain mapping
- All uploads go through Cloudflare API authentication

## Troubleshooting

**"Module not found" errors:**
```bash
pip3 install pillow requests
```

**"Credentials not found":**
```bash
cat $GITHUB_ROOT/cloudflare_credentials.json
# Should show account_id and api_token
```

**"Claude Code not available":**
```bash
# Ensure Claude Code CLI is installed and accessible
which claude  # Should return path to claude executable
```

**For external API usage (legacy):**
```bash
# Not recommended - use Claude Code native instead
export ANTHROPIC_API_KEY="your-api-key-here"
```

**"R2 upload succeeds but URL 404":**
- Check bucket name is "screenshots"
- Verify custom domain screenshots.tallyfy.com is configured
- Wait 30-60s for CDN cache

**"CSV inventory out of sync":**
```bash
# Rebuild inventory from R2 + documentation
python3 scripts/asset_inventory.py --rebuild
```

## See Also

- `references/r2_api_reference.md` - Complete Cloudflare R2 API docs
- `references/supported_formats.md` - Supported file types and limits
- `references/examples.md` - Usage examples and tutorials
- `$GITHUB_ROOT/documentation/CLAUDE.md` - Documentation repo guidelines

## Maintenance

**Regular Tasks:**
1. Weekly: Verify inventory CSV integrity
2. Monthly: Review orphaned assets (consider cleanup)
3. Quarterly: Check for missing images (404s) and fix
4. As needed: Regenerate captions for improved quality

**Inventory Location:**
- Primary: `$GITHUB_ROOT/documentation/documentation_assets.csv` (version controlled)
- Working Directory: `$GITHUB_ROOT/temporary/asset-inventory/asset_inventory_master.csv` (generated master)
