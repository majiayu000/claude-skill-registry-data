---
name: regenerate-embeddings
description: Manages OpenAI embeddings for title vector search, including batch regeneration, single title updates, verification, and cost estimation. This skill should be used when regenerating embeddings for new titles, fixing missing embeddings, or updating embeddings after content changes.
---

# Regenerate Embeddings

This skill orchestrates the regeneration of OpenAI embeddings for titles, enabling vector similarity search for the AI chatbot and mandate matcher features.

## When to Use This Skill

- New titles added without embeddings
- Title content updated (synopsis, description, genre)
- Batch regeneration for improved search quality
- Verifying embedding coverage
- Debugging search issues for specific titles

## Background

**What are embeddings?**
- 1536-dimensional vectors from OpenAI's `text-embedding-ada-002` model
- Enable semantic similarity search
- Stored in `titles.combined_embedding` column
- Used by: chat-orchestrator, mandate-matcher, vector-search

**Cost**: ~$0.0001 per title ($0.10 per 1000 titles)

## Commands

```
/regenerate-embeddings --new              # Titles without embeddings
/regenerate-embeddings --batch=50         # Top 50 by views
/regenerate-embeddings --title="Name"     # Specific title by name
/regenerate-embeddings --id=abc123        # Specific title by ID
/regenerate-embeddings --verify           # Check coverage stats
/regenerate-embeddings --cost             # Estimate cost only
```

## Existing Scripts

This skill wraps existing scripts in `/scripts/`:

| Script | Purpose |
|--------|---------|
| `run-regeneration.js` | Batch regenerate by views |
| `regenerate-specific-title.js` | Single title regeneration |
| `count-valid-embeddings.js` | Count titles with embeddings |
| `verify-regeneration-success.js` | Verify regeneration worked |

## Workflows

### Batch Regeneration (Most Common)

Regenerate embeddings for top titles by view count:

```bash
# Set OpenAI API key
export OPENAI_API_KEY="sk-..."

# Run regeneration for top 50 titles
node scripts/run-regeneration.js 50

# Or with start index for pagination
node scripts/run-regeneration.js 50 100  # Start at index 100
```

**Output**:
```
🚀 Starting regeneration for 50 titles (starting at index 0)...

✅ Regeneration complete!

Results:
  ✅ Success:  48 titles
  ❌ Failed:   1 titles
  ⏭️  Skipped:  1 titles
  ⏱️  Duration: 45.2s
  💰 Cost:     $0.0048
```

### Single Title Regeneration

For a specific title that needs updating:

```bash
# Via edge function
curl -X POST "$SUPABASE_URL/functions/v1/regenerate-embeddings" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title_id": "abc123"}'
```

Or modify `regenerate-specific-title.js` with the title name and run:

```bash
node scripts/regenerate-specific-title.js
```

### Find Titles Without Embeddings

Query titles missing embeddings:

```sql
-- Count titles without embeddings
SELECT COUNT(*) as missing_embeddings
FROM titles
WHERE combined_embedding IS NULL;

-- List titles without embeddings (by views)
SELECT title_id, title_name_en, views
FROM titles
WHERE combined_embedding IS NULL
ORDER BY views DESC NULLS LAST
LIMIT 20;
```

Or run the verification script:

```bash
node scripts/count-valid-embeddings.js
```

### Verify Embedding Quality

Check if embeddings are valid (1536 dimensions):

```sql
-- Check embedding dimensions
SELECT
  title_id,
  title_name_en,
  array_length(combined_embedding, 1) as dimensions
FROM titles
WHERE combined_embedding IS NOT NULL
LIMIT 10;

-- Find invalid embeddings
SELECT title_id, title_name_en
FROM titles
WHERE combined_embedding IS NOT NULL
  AND array_length(combined_embedding, 1) != 1536;
```

## Edge Function Details

**Function**: `supabase/functions/regenerate-embeddings/`

**Request Body**:
```json
{
  "limit": 50,           // Number of titles to process
  "start_index": 0,      // Pagination offset
  "title_id": "abc123"   // OR specific title ID
}
```

**Response**:
```json
{
  "results": {
    "success": 48,
    "failed": 1,
    "skipped": 1,
    "errors": ["Title xyz: API error"]
  },
  "estimated_cost": 0.0048
}
```

## Cost Estimation

Before running regeneration, estimate costs:

```bash
# Count titles needing embeddings
psql "$DATABASE_URL" -c "
  SELECT COUNT(*) as count
  FROM titles
  WHERE combined_embedding IS NULL;
"
```

**Cost calculation**:
- Model: text-embedding-ada-002
- Cost: $0.0001 per 1K tokens
- Average title: ~500 tokens
- **Per title**: ~$0.00005
- **Per 1000 titles**: ~$0.05

## Embedding Content

Embeddings are generated from combined text:

```javascript
const embeddingParts = [
  title.title_name_en || '',
  title.title_name_kr || '',
  title.synopsis || '',
  title.description_kr || '',
  (title.genre || []).join(' '),
  title.tone || ''
].filter(Boolean);

const embeddingText = embeddingParts.join(' ').trim();
// Truncated to 8000 characters for API limit
```

**Important**: If any of these fields change, consider regenerating the embedding.

## Database Schema

```sql
-- Embedding columns in titles table
combined_embedding    vector(1536)   -- The embedding vector
embedding_model       text           -- 'text-embedding-ada-002'
embedding_updated_at  timestamptz    -- Last update time
```

## Progress Tracking

For large batch operations, track progress:

```bash
# Terminal 1: Run regeneration
node scripts/run-regeneration.js 500

# Terminal 2: Monitor progress
watch -n 5 'psql "$DATABASE_URL" -c "
  SELECT
    COUNT(*) FILTER (WHERE combined_embedding IS NOT NULL) as with_embedding,
    COUNT(*) FILTER (WHERE combined_embedding IS NULL) as without_embedding,
    COUNT(*) as total
  FROM titles;
"'
```

## Troubleshooting

### "Rate limit exceeded"

OpenAI has rate limits. Solutions:
- Reduce batch size (`limit` parameter)
- Add delay between requests
- Use tier upgrade on OpenAI

### "Title not appearing in search"

1. Check if embedding exists:
   ```sql
   SELECT combined_embedding IS NOT NULL as has_embedding
   FROM titles WHERE title_name_en = 'Title Name';
   ```

2. Check embedding dimensions:
   ```sql
   SELECT array_length(combined_embedding, 1)
   FROM titles WHERE title_name_en = 'Title Name';
   ```

3. Regenerate if needed:
   ```bash
   # Modify and run
   node scripts/regenerate-specific-title.js
   ```

### "Embedding generation failed"

Check the title has sufficient content:
```sql
SELECT
  title_name_en,
  LENGTH(COALESCE(synopsis, '')) as synopsis_len,
  LENGTH(COALESCE(description_kr, '')) as desc_len
FROM titles
WHERE title_name_en = 'Title Name';
```

Titles need at least some text content for meaningful embeddings.

## Notifications

### Console Output

```
Regenerating embeddings...

[1/4] Checking coverage
      Total titles: 1,234
      With embeddings: 1,180 (95.6%)
      Without embeddings: 54

[2/4] Estimating cost
      Titles to process: 54
      Estimated cost: $0.0027

[3/4] Regenerating
      Processing title 1/54: "Title Name"...
      Processing title 2/54: "Another Title"...
      ...

[4/4] Summary
      Success: 52
      Failed: 2
      Cost: $0.0026
      Duration: 1m 23s
```

### Slack Notification

```json
{
  "text": "Embedding Regeneration Complete",
  "attachments": [{
    "color": "good",
    "fields": [
      {"title": "Processed", "value": "54 titles", "short": true},
      {"title": "Success", "value": "52", "short": true},
      {"title": "Failed", "value": "2", "short": true},
      {"title": "Cost", "value": "$0.0026", "short": true}
    ]
  }]
}
```

## Best Practices

1. **Run during low-traffic hours** - Reduces load on OpenAI
2. **Start with small batches** - Test with 10-20 titles first
3. **Monitor costs** - Track OpenAI spending
4. **Verify after regeneration** - Run verification script
5. **Document changes** - Note when embeddings were last updated

## Related Skills

- `/title-intelligence` - Collect title data before regeneration
- `/cost-report` - Track embedding regeneration costs
- `/health-check` - Verify vector search is working
