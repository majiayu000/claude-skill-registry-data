---
name: batch-format-fit
description: Batch format suitability analysis using GPT-4o across 5 content formats (Film, TV Series, Animation, Microdrama, Audio Drama). This skill should be used for analyzing format fit on multiple titles, generating catalog reports, or running overnight batch processing.
---

# Batch Format Fit

This skill orchestrates batch format suitability analysis, enabling large-scale format scoring without manual UI interaction.

## When to Use This Skill

- Analyzing format fit for multiple titles at once (20+)
- Filling gaps (titles without format analysis)
- Format-specific discovery (finding all titles good for microdrama)
- Catalog reports (format distribution across catalog)
- New title processing (recently added titles)
- Porting the feature to another app

## What It Does

For each title, the format fit analyzer:
1. Collects title data (synopsis, genre, content analysis)
2. Deconstructs story with format-specific attributes using GPT-4o
3. Scores suitability across 5 content formats
4. Provides 7-dimension analysis per format
5. Saves to `title_format_fit` table

**5 Content Formats**:
| Format | Description | Key Factors |
|--------|-------------|-------------|
| Film | 90-150 min feature | Self-contained story, production scale |
| TV Series | 8-16 episodes | Character depth, arc potential |
| Animation | Animated adaptation | Visual complexity, world-building |
| Microdrama | 60-120s vertical video | Cliffhangers, trope alignment |
| Audio Drama | Podcast/audio fiction | Dialogue-driven, voice potential |

**7 Scoring Dimensions per Format**:
- Narrative structure
- Character suitability
- Visual requirements
- Pacing fit
- Production feasibility
- Audience alignment
- Genre fit

## Commands

```
/batch-format-fit --missing                     # Titles without analysis
/batch-format-fit --format=microdrama           # Focus on specific format
/batch-format-fit --limit=50                    # Limit batch size
/batch-format-fit --min-score=80                # Re-analyze low scores
/batch-format-fit --cost-estimate               # Estimate cost before running
/batch-format-fit --dry-run                     # Preview without executing
/batch-format-fit --report                      # Generate format distribution report
/batch-format-fit --recent=7                    # Titles added in last 7 days
```

## Edge Function Reference

**Location**: `supabase/functions/format-fit-engine/index.ts`

**Endpoint**: `POST /functions/v1/format-fit-engine`

**Request Body**:
```typescript
interface FormatFitRequest {
  title_id: string;
  // Optional: force regeneration even if analysis exists
  force?: boolean;
}
```

**Response**:
```typescript
interface FormatFitResponse {
  success: boolean;
  title_id: string;
  scores: {
    film: number;          // 0-100
    tv_series: number;
    animation: number;
    microdrama: number;
    audio_drama: number;
  };
  analyses: {
    film: FormatAnalysis;
    tv_series: FormatAnalysis;
    animation: FormatAnalysis;
    microdrama: MicrodramaAnalysis;
    audio_drama: FormatAnalysis;
  };
  story_deconstruction: {
    narrative_complexity: string;
    character_count: number;
    visual_intensity: string;
    pacing_type: string;
    setting_production_cost: string;
  };
  data_completeness: number;
  mode: 'rich' | 'limited';
  processing_time_ms: number;
  cost_estimate: number;
}

interface FormatAnalysis {
  score: number;
  dimensions: {
    narrative_structure: number;
    character_suitability: number;
    visual_requirements: number;
    pacing_fit: number;
    production_feasibility: number;
    audience_alignment: number;
    genre_fit: number;
  };
  strengths: string[];
  challenges: string[];
  recommendation: string;
}

interface MicrodramaAnalysis extends FormatAnalysis {
  cliffhanger_potential: number;
  trope_alignment: string[];
  episode_structure_fit: number;
  vertical_filming_compatibility: number;
  target_platform_fit: string;  // ReelShort, DramaBox, etc.
}
```

## Cost Estimation

**Model**: GPT-4o (2 API calls per title)
**Cost**: ~$0.01-0.015 per title

| Batch Size | Est. Time | Est. Cost |
|------------|-----------|-----------|
| 10 titles | ~3 min | $0.12 |
| 50 titles | ~15 min | $0.60 |
| 100 titles | ~30 min | $1.20 |
| 500 titles | ~2.5 hours | $6.00 |

## Batch Workflow

### Step 1: Identify Titles to Process

```sql
-- Titles without format analysis
SELECT t.title_id, t.title_name_en, t.views
FROM titles t
LEFT JOIN title_format_fit f ON t.title_id = f.title_id
WHERE f.id IS NULL
ORDER BY t.views DESC NULLS LAST
LIMIT 50;

-- Titles good for specific format (discovery)
SELECT t.title_name_en, f.microdrama_score
FROM titles t
JOIN title_format_fit f ON t.title_id = f.title_id
WHERE f.microdrama_score >= 80
ORDER BY f.microdrama_score DESC;

-- Recently added titles
SELECT title_id, title_name_en
FROM titles
WHERE created_at > NOW() - INTERVAL '7 days';
```

### Step 2: Batch Analysis

```javascript
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;

async function analyzeFormatFitBatch(titleIds, options = {}) {
  const results = { success: [], failed: [], skipped: [] };
  let totalCost = 0;

  // Cost estimation
  if (options.costEstimateOnly) {
    const estimatedCost = titleIds.length * 0.012;
    console.log(`Estimated cost: $${estimatedCost.toFixed(2)} for ${titleIds.length} titles`);
    return { estimatedCost, titleCount: titleIds.length };
  }

  for (const titleId of titleIds) {
    try {
      const response = await fetch(`${SUPABASE_URL}/functions/v1/format-fit-engine`, {
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
          scores: data.scores,
          best_format: getBestFormat(data.scores),
          cost: data.cost_estimate || 0.012
        });
        totalCost += data.cost_estimate || 0.012;
      } else {
        results.failed.push({
          title_id: titleId,
          error: data.error
        });
      }

      // Rate limiting
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

function getBestFormat(scores) {
  const formats = ['film', 'tv_series', 'animation', 'microdrama', 'audio_drama'];
  return formats.reduce((best, format) =>
    scores[format] > scores[best] ? format : best
  , formats[0]);
}
```

### Step 3: Generate Format Distribution Report

```sql
-- Format distribution across catalog
SELECT
  CASE
    WHEN f.film_score = GREATEST(f.film_score, f.tv_series_score, f.animation_score, f.microdrama_score, f.audio_drama_score)
    THEN 'Film'
    WHEN f.tv_series_score = GREATEST(f.film_score, f.tv_series_score, f.animation_score, f.microdrama_score, f.audio_drama_score)
    THEN 'TV Series'
    WHEN f.animation_score = GREATEST(f.film_score, f.tv_series_score, f.animation_score, f.microdrama_score, f.audio_drama_score)
    THEN 'Animation'
    WHEN f.microdrama_score = GREATEST(f.film_score, f.tv_series_score, f.animation_score, f.microdrama_score, f.audio_drama_score)
    THEN 'Microdrama'
    ELSE 'Audio Drama'
  END as best_format,
  COUNT(*) as title_count,
  ROUND(AVG(GREATEST(f.film_score, f.tv_series_score, f.animation_score, f.microdrama_score, f.audio_drama_score)), 1) as avg_best_score
FROM title_format_fit f
GROUP BY 1
ORDER BY title_count DESC;

-- Microdrama-ready titles (score >= 80)
SELECT
  t.title_name_en,
  f.microdrama_score,
  f.microdrama_analysis->>'target_platform_fit' as target_platform,
  f.microdrama_analysis->>'cliffhanger_potential' as cliffhanger_score
FROM titles t
JOIN title_format_fit f ON t.title_id = f.title_id
WHERE f.microdrama_score >= 80
ORDER BY f.microdrama_score DESC;
```

## Console Output

```
Starting batch format fit analysis...

Configuration:
  Filter: missing analysis
  Limit: 50
  Budget: $1.00 max

Cost Estimate:
  Titles to process: 50
  Estimated cost: $0.60
  Proceed? (Y/n)

[1/50] Processing "재벌집 막내아들"
       Data completeness: 85%
       ✅ Analyzed
       Scores: Film=78, TV=92, Anim=65, Micro=71, Audio=58
       Best fit: TV Series (92%)
       Cost: $0.012

[2/50] Processing "Solo Leveling"
       Data completeness: 92%
       ✅ Analyzed
       Scores: Film=72, TV=85, Anim=95, Micro=68, Audio=52
       Best fit: Animation (95%)
       Cost: $0.011

...

Summary:
  ✅ Success: 48 titles
  ❌ Failed: 2 titles
  💰 Total cost: $0.58

Format Distribution:
  TV Series: 18 titles (38%)
  Animation: 12 titles (25%)
  Film: 10 titles (21%)
  Microdrama: 6 titles (12%)
  Audio Drama: 2 titles (4%)

High-potential Microdrama Titles (80+):
  - "Title A" (92%)
  - "Title B" (88%)
  - "Title C" (85%)
```

## Database Schema

### title_format_fit

```sql
CREATE TABLE title_format_fit (
  id UUID PRIMARY KEY,
  title_id UUID REFERENCES titles(title_id),
  film_score INTEGER,
  tv_series_score INTEGER,
  animation_score INTEGER,
  microdrama_score INTEGER,
  audio_drama_score INTEGER,
  film_analysis JSONB,
  tv_series_analysis JSONB,
  animation_analysis JSONB,
  microdrama_analysis JSONB,
  audio_drama_analysis JSONB,
  story_deconstruction JSONB,
  data_completeness INTEGER,
  mode_used TEXT,
  processing_time_ms INTEGER,
  cost_estimate NUMERIC,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Error Handling

### Common Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `Insufficient data` | Missing synopsis/genre | Collect data first via /batch-intelligence |
| `API timeout` | GPT-4o slow response | Retry with longer timeout |
| `Rate limit` | Too many requests | Increase delay between requests |

### Data Quality Pre-Check

```sql
-- Check data completeness for target titles
SELECT
  title_name_en,
  CASE
    WHEN synopsis IS NOT NULL AND LENGTH(synopsis) > 100
         AND genre IS NOT NULL
    THEN 'ready'
    ELSE 'needs data'
  END as status
FROM titles t
LEFT JOIN title_format_fit f ON t.title_id = f.title_id
WHERE f.id IS NULL;
```

## Porting Guide

To port this feature to another app (e.g., Creator):

### 1. Service File Template

Create `apps/[app]/src/services/formatFitService.ts`:

```typescript
import { supabase } from '@/integrations/supabase/client';

const FUNCTION_URL = `${import.meta.env.VITE_SUPABASE_URL}/functions/v1/format-fit-engine`;

export interface FormatScores {
  film: number;
  tv_series: number;
  animation: number;
  microdrama: number;
  audio_drama: number;
}

export interface FormatFitResult {
  success: boolean;
  scores: FormatScores;
  analyses: Record<string, any>;
  data_completeness: number;
  mode: 'rich' | 'limited';
  processing_time_ms: number;
  cost_estimate: number;
  error?: string;
}

export async function analyzeFormatFit(titleId: string): Promise<FormatFitResult> {
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

export function getBestFormat(scores: FormatScores): string {
  const formats = Object.entries(scores);
  formats.sort((a, b) => b[1] - a[1]);
  return formats[0][0];
}

export function estimateCost(titleCount: number): number {
  return titleCount * 0.012;
}
```

### 2. UI Component Template

Create `apps/[app]/src/components/FormatFitButton.tsx`:

```typescript
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { analyzeFormatFit } from '@/services/formatFitService';
import { BarChart3, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

interface Props {
  titleId: string;
  hasExistingAnalysis?: boolean;
  onSuccess?: (scores: FormatScores) => void;
}

export function FormatFitButton({ titleId, hasExistingAnalysis, onSuccess }: Props) {
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const result = await analyzeFormatFit(titleId);

      if (result.success) {
        const bestFormat = getBestFormat(result.scores);
        toast.success(`Analysis complete: Best fit is ${bestFormat}`, {
          description: `Score: ${result.scores[bestFormat]}%`
        });
        onSuccess?.(result.scores);
      } else {
        toast.error(result.error || 'Analysis failed');
      }
    } catch (error) {
      toast.error('Failed to analyze format fit');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Button
      variant={hasExistingAnalysis ? 'outline' : 'default'}
      size="sm"
      onClick={handleAnalyze}
      disabled={loading}
      className={hasExistingAnalysis ? 'border-blue-500' : ''}
    >
      {loading ? (
        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
      ) : (
        <BarChart3 className="w-4 h-4 mr-2" />
      )}
      {loading ? 'Analyzing...' : hasExistingAnalysis ? 'Re-analyze' : 'Format Fit'}
    </Button>
  );
}
```

### 3. Scores Display Component

```typescript
import { FormatScores } from '@/services/formatFitService';

interface Props {
  scores: FormatScores;
}

export function FormatScoresDisplay({ scores }: Props) {
  const formats = [
    { key: 'film', label: 'Film', icon: '🎬' },
    { key: 'tv_series', label: 'TV Series', icon: '📺' },
    { key: 'animation', label: 'Animation', icon: '🎨' },
    { key: 'microdrama', label: 'Microdrama', icon: '📱' },
    { key: 'audio_drama', label: 'Audio Drama', icon: '🎧' },
  ];

  return (
    <div className="grid grid-cols-5 gap-4">
      {formats.map(({ key, label, icon }) => (
        <div key={key} className="text-center p-4 bg-gray-50 rounded-lg">
          <div className="text-2xl mb-2">{icon}</div>
          <div className="text-sm font-medium">{label}</div>
          <div className="text-2xl font-bold mt-1">
            {scores[key as keyof FormatScores]}%
          </div>
        </div>
      ))}
    </div>
  );
}
```

## Related Skills

- `/batch-intelligence` - Collect data before analysis for better results
- `/batch-comps` - Generate comps alongside format analysis
- `/title-pipeline` - Orchestrate full workflow
