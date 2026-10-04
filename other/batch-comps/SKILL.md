---
name: batch-comps
description: Batch generation of Hollywood comparable titles using GPT-4o. This skill should be used for generating comps on multiple titles at once, filling gaps in catalog coverage, or running overnight batch processing.
---

# Batch Comps

This skill orchestrates batch generation of Hollywood comparable titles, enabling large-scale comp generation without manual UI interaction.

## When to Use This Skill

- Generating comps for multiple titles at once (20+)
- Filling gaps (titles without comps)
- Genre-specific batch runs (all horror titles, all romance titles)
- New title processing (recently added titles)
- Cost-controlled batch runs with budget limits
- Porting the feature to another app

## What It Does

For each title, the comps generator:
1. Collects title data (synopsis, genre, content analysis)
2. Deconstructs story across 8 dimensions using GPT-4o
3. Generates 5-8 Hollywood comparable titles with scoring
4. Enriches with OMDB data (IMDB IDs, posters)
5. Saves to `comps` and `comps_analysis` columns

**8 Scoring Dimensions**:
- Save the Cat genre
- Tone/atmosphere
- Character archetypes
- Plot structure
- Setting/world
- Themes
- Target audience
- Format/medium

## Commands

```
/batch-comps --missing                    # Titles without comps
/batch-comps --genre=horror               # Specific genre
/batch-comps --limit=50                   # Limit batch size
/batch-comps --min-views=100000           # High-value titles only
/batch-comps --cost-estimate              # Estimate cost before running
/batch-comps --dry-run                    # Preview without executing
/batch-comps --data-complete-only         # Only titles with rich data
/batch-comps --recent=7                   # Titles added in last 7 days
```

## Edge Function Reference

**Location**: `supabase/functions/comps-generator/index.ts`

**Endpoint**: `POST /functions/v1/comps-generator`

**Request Body**:
```typescript
interface CompsRequest {
  title_id: string;
  // Optional: force regeneration even if comps exist
  force?: boolean;
}
```

**Response**:
```typescript
interface CompsResponse {
  success: boolean;
  title_id: string;
  comps: string[];  // Array of comp title names
  comps_analysis: Array<{
    title: string;
    year?: number;
    imdb_id?: string;
    poster_url?: string;
    match_score: number;  // 0-100
    dimension_scores: {
      stc_genre: number;
      tone: number;
      characters: number;
      plot: number;
      setting: number;
      themes: number;
      audience: number;
      format: number;
    };
    explanation: string;
  }>;
  story_deconstruction: {
    stc_genre: string;
    tone: string[];
    character_archetypes: string[];
    plot_structure: string;
    setting: string;
    themes: string[];
    target_audience: string;
    format_notes: string;
  };
  data_completeness: number;  // 0-100
  mode: 'rich' | 'limited';
  processing_time_ms: number;
  cost_estimate: number;
}
```

## Cost Estimation

**Model**: GPT-4o (2 API calls per title)
**Cost**: ~$0.01 per title

| Batch Size | Est. Time | Est. Cost |
|------------|-----------|-----------|
| 10 titles | ~2.5 min | $0.10 |
| 50 titles | ~12 min | $0.50 |
| 100 titles | ~25 min | $1.00 |
| 500 titles | ~2 hours | $5.00 |

### Pre-Run Cost Check

```sql
-- Count titles that need comps
SELECT COUNT(*) as titles_needing_comps
FROM titles
WHERE (comps IS NULL OR array_length(comps, 1) = 0)
  AND views > 100000;  -- High-value only

-- Estimated cost = count * $0.01
```

## Batch Workflow

### Step 1: Identify Titles to Process

```sql
-- Titles without comps (high-value first)
SELECT title_id, title_name_en, views, genre
FROM titles
WHERE comps IS NULL OR array_length(comps, 1) = 0
ORDER BY views DESC NULLS LAST
LIMIT 50;

-- Genre-specific (horror titles)
SELECT title_id, title_name_en
FROM titles
WHERE 'Horror' = ANY(genre)
  AND (comps IS NULL OR array_length(comps, 1) = 0);

-- Recently added titles
SELECT title_id, title_name_en
FROM titles
WHERE created_at > NOW() - INTERVAL '7 days'
  AND (comps IS NULL OR array_length(comps, 1) = 0);

-- Data-complete titles only (better results)
SELECT title_id, title_name_en
FROM titles
WHERE synopsis IS NOT NULL
  AND LENGTH(synopsis) > 100
  AND genre IS NOT NULL
  AND array_length(genre, 1) > 0
  AND (comps IS NULL OR array_length(comps, 1) = 0);
```

### Step 2: Batch Generation

```javascript
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;

async function generateCompsBatch(titleIds, options = {}) {
  const results = { success: [], failed: [], skipped: [] };
  let totalCost = 0;

  // Cost estimation
  if (options.costEstimateOnly) {
    const estimatedCost = titleIds.length * 0.01;
    console.log(`Estimated cost: $${estimatedCost.toFixed(2)} for ${titleIds.length} titles`);
    return { estimatedCost, titleCount: titleIds.length };
  }

  for (const titleId of titleIds) {
    try {
      const response = await fetch(`${SUPABASE_URL}/functions/v1/comps-generator`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title_id: titleId })
      });

      const data = await response.json();

      if (data.success) {
        results.success.push({
          title_id: titleId,
          comps_count: data.comps?.length || 0,
          cost: data.cost_estimate || 0.01,
          mode: data.mode
        });
        totalCost += data.cost_estimate || 0.01;
      } else {
        results.failed.push({
          title_id: titleId,
          error: data.error
        });
      }

      // Rate limiting (respect API limits)
      await delay(2000);

    } catch (error) {
      results.failed.push({
        title_id: titleId,
        error: error.message
      });
    }

    // Budget check
    if (options.maxCost && totalCost >= options.maxCost) {
      console.log(`Budget limit reached: $${totalCost.toFixed(2)}`);
      break;
    }
  }

  return { results, totalCost };
}
```

### Step 3: Verification

```sql
-- Verify comps were generated
SELECT
  title_name_en,
  array_length(comps, 1) as comp_count,
  updated_at
FROM titles
WHERE title_id = ANY($1::uuid[])
ORDER BY updated_at DESC;

-- Check data quality
SELECT
  title_name_en,
  comps_analysis->0->>'match_score' as top_match_score,
  comps_analysis->0->>'title' as top_comp
FROM titles
WHERE title_id = ANY($1::uuid[])
  AND comps_analysis IS NOT NULL;
```

## Console Output

```
Starting batch comps generation...

Configuration:
  Filter: missing comps, high-value (views > 100k)
  Limit: 50
  Budget: $1.00 max

Cost Estimate:
  Titles to process: 50
  Estimated cost: $0.50
  Proceed? (Y/n)

[1/50] Processing "재벌집 막내아들"
       Data completeness: 85% (rich mode)
       ✅ Generated 7 comps
       Top match: "Succession" (92%)
       Cost: $0.012

[2/50] Processing "Solo Leveling"
       Data completeness: 92% (rich mode)
       ✅ Generated 8 comps
       Top match: "Sword Art Online" (88%)
       Cost: $0.011

[3/50] Processing "Unknown Title"
       Data completeness: 23% (limited mode)
       ⚠️ Generated 5 comps (limited data)
       Cost: $0.008

...

Summary:
  ✅ Success: 47 titles (avg 6.8 comps each)
  ⚠️ Limited mode: 8 titles
  ❌ Failed: 3 titles
  💰 Total cost: $0.48

Failed titles:
  - "Title A": Insufficient data (no synopsis)
  - "Title B": API timeout
  - "Title C": Rate limit exceeded
```

## Error Handling

### Common Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `Insufficient data` | Missing synopsis/genre | Collect data first via /batch-intelligence |
| `API timeout` | GPT-4o slow response | Retry with longer timeout |
| `Rate limit` | Too many requests | Increase delay between requests |
| `OMDB enrichment failed` | OMDB API issue | Non-fatal, comps still saved |

### Data Quality Pre-Check

Before running batch, verify data quality:

```sql
-- Check data completeness for target titles
SELECT
  title_name_en,
  CASE
    WHEN synopsis IS NOT NULL AND LENGTH(synopsis) > 100
         AND genre IS NOT NULL AND array_length(genre, 1) > 0
         AND tone IS NOT NULL
    THEN 'rich'
    ELSE 'limited'
  END as expected_mode,
  CASE WHEN synopsis IS NULL THEN 'missing synopsis' END as issue1,
  CASE WHEN genre IS NULL THEN 'missing genre' END as issue2
FROM titles
WHERE comps IS NULL;
```

## Porting Guide

To port this feature to another app (e.g., Creator):

### 1. Service File Template

Create `apps/[app]/src/services/compsGeneratorService.ts`:

```typescript
import { supabase } from '@/integrations/supabase/client';

const FUNCTION_URL = `${import.meta.env.VITE_SUPABASE_URL}/functions/v1/comps-generator`;

export interface SuggestedComp {
  title: string;
  year?: number;
  imdb_id?: string;
  poster_url?: string;
  match_score: number;
  dimension_scores: {
    stc_genre: number;
    tone: number;
    characters: number;
    plot: number;
    setting: number;
    themes: number;
    audience: number;
    format: number;
  };
  explanation: string;
}

export interface CompsResult {
  success: boolean;
  comps: string[];
  comps_analysis: SuggestedComp[];
  data_completeness: number;
  mode: 'rich' | 'limited';
  processing_time_ms: number;
  cost_estimate: number;
  error?: string;
}

export async function generateComps(titleId: string): Promise<CompsResult> {
  const { data: { session } } = await supabase.auth.getSession();

  const response = await fetch(FUNCTION_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${session?.access_token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title_id: titleId })
  });

  return response.json();
}

export function estimateCost(titleCount: number): number {
  return titleCount * 0.01;  // ~$0.01 per title
}
```

### 2. UI Component Template

Create `apps/[app]/src/components/GenerateCompsButton.tsx`:

```typescript
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { generateComps, estimateCost } from '@/services/compsGeneratorService';
import { Sparkles, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

interface Props {
  titleId: string;
  hasExistingComps?: boolean;
  onSuccess?: (comps: string[]) => void;
}

export function GenerateCompsButton({ titleId, hasExistingComps, onSuccess }: Props) {
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const result = await generateComps(titleId);

      if (result.success) {
        toast.success(`Generated ${result.comps.length} comps`, {
          description: `Mode: ${result.mode}, Cost: $${result.cost_estimate.toFixed(3)}`
        });
        onSuccess?.(result.comps);
      } else {
        toast.error(result.error || 'Generation failed');
      }
    } catch (error) {
      toast.error('Failed to generate comps');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Button
      variant={hasExistingComps ? 'outline' : 'default'}
      size="sm"
      onClick={handleGenerate}
      disabled={loading}
      className={hasExistingComps ? 'border-blue-500' : ''}
    >
      {loading ? (
        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
      ) : (
        <Sparkles className="w-4 h-4 mr-2" />
      )}
      {loading ? 'Generating...' : hasExistingComps ? 'Regenerate Comps' : 'Generate Comps'}
    </Button>
  );
}
```

### 3. Results Display Component

```typescript
import { SuggestedComp } from '@/services/compsGeneratorService';

interface Props {
  comps: SuggestedComp[];
}

export function CompsDisplay({ comps }: Props) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {comps.map((comp, index) => (
        <div key={index} className="bg-white rounded-lg border p-4">
          {comp.poster_url && (
            <img
              src={comp.poster_url}
              alt={comp.title}
              className="w-full h-40 object-cover rounded mb-2"
            />
          )}
          <h4 className="font-semibold text-sm">{comp.title}</h4>
          {comp.year && <p className="text-xs text-gray-500">{comp.year}</p>}
          <div className="mt-2">
            <span className="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded">
              {comp.match_score}% match
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
```

### 4. Integration Points

- Add button to title edit page
- Add comps display section
- Wire up data refresh after generation

## Related Skills

- `/batch-intelligence` - Collect data before generating comps for better results
- `/batch-format-fit` - Run format analysis after comps generation
- `/title-pipeline` - Orchestrate full workflow
- `/regenerate-embeddings` - Update embeddings after comps change
