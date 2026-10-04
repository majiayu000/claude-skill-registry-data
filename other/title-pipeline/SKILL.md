---
name: title-pipeline
description: Orchestrates full title processing workflow (collect → embed → comps → format-fit). This skill should be used for processing new titles end-to-end, running overnight batch processing on recent additions, or ensuring all titles have complete data and analysis.
---

# Title Pipeline

This skill orchestrates the complete title processing workflow, coordinating data collection, embedding generation, comps generation, and format fit analysis into a single automated pipeline.

## When to Use This Skill

- Processing new titles end-to-end (just added to catalog)
- Overnight batch processing for recent additions
- Ensuring all titles have complete data and analysis
- Re-processing titles after major data updates
- Onboarding large batches of new content
- Porting the pipeline concept to another app

## Pipeline Stages

| Stage | Function | Cost | Duration | Output |
|-------|----------|------|----------|--------|
| 1. Collect | title-intelligence | $0 | 5-30s | Platform metrics, metadata |
| 2. Embed | regenerate-embeddings | ~$0.0001 | 2-3s | Vector embedding (1536-dim) |
| 3. Comps | comps-generator | ~$0.01 | 10-15s | 5-8 Hollywood comparables |
| 4. Format Fit | format-fit-engine | ~$0.01 | 12-20s | 5 format scores + analyses |
| **TOTAL** | | **~$0.02** | **~45s** | Complete title intelligence |

## Commands

```
/title-pipeline --new                     # Process titles added in last 7 days
/title-pipeline --new=14                  # Process titles added in last 14 days
/title-pipeline --title="Title Name"      # Process specific title by name
/title-pipeline --title-id=uuid           # Process specific title by ID
/title-pipeline --missing                 # Process titles missing any stage
/title-pipeline --stage=comps             # Run only specific stage
/title-pipeline --skip=collect            # Skip specific stage(s)
/title-pipeline --limit=50                # Limit batch size
/title-pipeline --cost-estimate           # Estimate cost before running
/title-pipeline --dry-run                 # Preview without executing
/title-pipeline --status                  # Show pipeline queue status
/title-pipeline --report                  # Generate coverage report
```

## Edge Function References

### Stage 1: Title Intelligence (Collect)
**Location**: `supabase/functions/title-intelligence/index.ts`
**Cost**: Free (web scraping)
**Output**: Platform metrics saved to `intelligence_*` tables

### Stage 2: Regenerate Embeddings
**Location**: `supabase/functions/regenerate-embeddings/index.ts`
**Cost**: ~$0.0001 per title
**Output**: `combined_embedding` column updated (1536-dim vector)

### Stage 3: Comps Generator
**Location**: `supabase/functions/comps-generator/index.ts`
**Cost**: ~$0.01 per title
**Output**: `comps` and `comps_analysis` columns updated

### Stage 4: Format Fit Engine
**Location**: `supabase/functions/format-fit-engine/index.ts`
**Cost**: ~$0.01 per title
**Output**: `title_format_fit` table record created

## Pipeline Workflow

### Step 1: Identify Titles to Process

```sql
-- New titles (last 7 days) without complete processing
SELECT t.title_id, t.title_name_en, t.created_at,
  CASE WHEN t.views IS NULL THEN 'missing' ELSE 'done' END as collect_status,
  CASE WHEN t.combined_embedding IS NULL THEN 'missing' ELSE 'done' END as embed_status,
  CASE WHEN t.comps IS NULL OR array_length(t.comps, 1) = 0 THEN 'missing' ELSE 'done' END as comps_status,
  CASE WHEN f.id IS NULL THEN 'missing' ELSE 'done' END as format_fit_status
FROM titles t
LEFT JOIN title_format_fit f ON t.title_id = f.title_id
WHERE t.created_at > NOW() - INTERVAL '7 days'
ORDER BY t.created_at DESC;

-- Titles missing any pipeline stage
SELECT t.title_id, t.title_name_en
FROM titles t
LEFT JOIN title_format_fit f ON t.title_id = f.title_id
WHERE t.views IS NULL
   OR t.combined_embedding IS NULL
   OR t.comps IS NULL
   OR array_length(t.comps, 1) = 0
   OR f.id IS NULL
ORDER BY t.views DESC NULLS LAST
LIMIT 50;
```

### Step 2: Run Pipeline

```javascript
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;

async function runTitlePipeline(titleId, options = {}) {
  const results = {
    title_id: titleId,
    stages: {},
    total_cost: 0,
    total_time_ms: 0,
    success: true
  };

  const stages = [
    { name: 'collect', fn: collectData, skip: options.skipCollect },
    { name: 'embed', fn: regenerateEmbedding, skip: options.skipEmbed },
    { name: 'comps', fn: generateComps, skip: options.skipComps },
    { name: 'format_fit', fn: analyzeFormatFit, skip: options.skipFormatFit }
  ];

  for (const stage of stages) {
    if (stage.skip) {
      results.stages[stage.name] = { status: 'skipped' };
      continue;
    }

    try {
      const startTime = Date.now();
      const stageResult = await stage.fn(titleId);
      const duration = Date.now() - startTime;

      results.stages[stage.name] = {
        status: stageResult.success ? 'success' : 'failed',
        duration_ms: duration,
        cost: stageResult.cost_estimate || 0,
        error: stageResult.error
      };

      results.total_cost += stageResult.cost_estimate || 0;
      results.total_time_ms += duration;

      if (!stageResult.success) {
        results.success = false;
        console.log(`Stage ${stage.name} failed: ${stageResult.error}`);
        // Continue to next stage or break based on options
        if (options.stopOnError) break;
      }

      // Rate limiting between stages
      await delay(1000);

    } catch (error) {
      results.stages[stage.name] = {
        status: 'error',
        error: error.message
      };
      results.success = false;
      if (options.stopOnError) break;
    }
  }

  return results;
}

// Stage implementations
async function collectData(titleId) {
  // Get title URL from database first
  const { data: title } = await supabase
    .from('titles')
    .select('title_url')
    .eq('title_id', titleId)
    .single();

  if (!title?.title_url) {
    return { success: false, error: 'No platform URL found' };
  }

  const parsed = parsePlatformUrl(title.title_url);
  if (!parsed) {
    return { success: false, error: 'Unparseable URL' };
  }

  const response = await fetch(`${SUPABASE_URL}/functions/v1/title-intelligence`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      urls: [{
        platform: parsed.platform,
        platformId: parsed.platformId,
        originalUrl: title.title_url
      }],
      collectedBy: 'title-pipeline',
      contentType: 'webtoon'
    })
  });

  const data = await response.json();
  return { success: data.success, cost_estimate: 0, error: data.error };
}

async function regenerateEmbedding(titleId) {
  const response = await fetch(`${SUPABASE_URL}/functions/v1/regenerate-embeddings`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title_ids: [titleId],
      force: true
    })
  });

  const data = await response.json();
  return {
    success: data.success,
    cost_estimate: 0.0001,
    error: data.error
  };
}

async function generateComps(titleId) {
  const response = await fetch(`${SUPABASE_URL}/functions/v1/comps-generator`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title_id: titleId })
  });

  const data = await response.json();
  return {
    success: data.success,
    cost_estimate: data.cost_estimate || 0.01,
    error: data.error
  };
}

async function analyzeFormatFit(titleId) {
  const response = await fetch(`${SUPABASE_URL}/functions/v1/format-fit-engine`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ title_id: titleId })
  });

  const data = await response.json();
  return {
    success: data.success,
    cost_estimate: data.cost_estimate || 0.012,
    error: data.error
  };
}
```

### Step 3: Batch Pipeline

```javascript
async function runBatchPipeline(titleIds, options = {}) {
  const results = {
    success: [],
    partial: [],
    failed: [],
    total_cost: 0,
    total_time_ms: 0
  };

  // Cost estimation
  if (options.costEstimateOnly) {
    const estimatedCost = titleIds.length * 0.022;
    const estimatedTime = titleIds.length * 45; // seconds
    console.log(`Estimated cost: $${estimatedCost.toFixed(2)} for ${titleIds.length} titles`);
    console.log(`Estimated time: ${Math.round(estimatedTime / 60)} minutes`);
    return { estimatedCost, estimatedTime, titleCount: titleIds.length };
  }

  for (let i = 0; i < titleIds.length; i++) {
    const titleId = titleIds[i];
    console.log(`[${i + 1}/${titleIds.length}] Processing ${titleId}...`);

    const result = await runTitlePipeline(titleId, options);

    if (result.success) {
      results.success.push({ title_id: titleId, ...result });
    } else if (Object.values(result.stages).some(s => s.status === 'success')) {
      results.partial.push({ title_id: titleId, ...result });
    } else {
      results.failed.push({ title_id: titleId, ...result });
    }

    results.total_cost += result.total_cost;
    results.total_time_ms += result.total_time_ms;

    // Rate limiting between titles
    await delay(2000);

    // Budget check
    if (options.maxCost && results.total_cost >= options.maxCost) {
      console.log(`Budget limit reached: $${results.total_cost.toFixed(2)}`);
      break;
    }
  }

  return results;
}
```

## Cost Estimation

**Per Title Pipeline Cost**:
| Stage | Cost | Notes |
|-------|------|-------|
| Collect | $0 | Web scraping, no API |
| Embed | $0.0001 | OpenAI ada-002 |
| Comps | $0.01 | GPT-4o (2 calls) |
| Format Fit | $0.012 | GPT-4o (2 calls) |
| **Total** | **$0.022** | Per title |

**Batch Cost Table**:
| Titles | Est. Time | Est. Cost |
|--------|-----------|-----------|
| 10 | ~8 min | $0.22 |
| 50 | ~40 min | $1.10 |
| 100 | ~1.3 hours | $2.20 |
| 500 | ~6.5 hours | $11.00 |

## Console Output

```
Starting title pipeline...

Configuration:
  Mode: new titles (7 days)
  Titles to process: 12
  Stages: collect → embed → comps → format_fit
  Budget: $5.00 max

Cost Estimate:
  Estimated cost: $0.26
  Estimated time: ~9 minutes
  Proceed? (Y/n)

[1/12] Processing "재벌집 막내아들"
       ├─ Collect: ✅ views=12.3M, rating=9.8 (5.2s, $0)
       ├─ Embed: ✅ 1536-dim vector updated (2.1s, $0.0001)
       ├─ Comps: ✅ 7 comps generated, top: "Succession" (12.3s, $0.011)
       └─ Format Fit: ✅ TV=92, Film=78, Anim=65 (15.1s, $0.012)
       Total: 34.7s, $0.023

[2/12] Processing "Solo Leveling"
       ├─ Collect: ⏭️ skipped (has data)
       ├─ Embed: ✅ updated (2.0s, $0.0001)
       ├─ Comps: ✅ 8 comps, top: "Sword Art Online" (11.8s, $0.010)
       └─ Format Fit: ✅ Anim=95, TV=85, Film=72 (14.2s, $0.011)
       Total: 28.0s, $0.021

[3/12] Processing "Unknown Webnovel"
       ├─ Collect: ❌ No platform URL found
       ├─ Embed: ⚠️ Limited data mode
       ├─ Comps: ⚠️ 4 comps (limited)
       └─ Format Fit: ⚠️ Low confidence scores
       Total: 25.3s, $0.018

...

Summary:
  ✅ Complete: 9 titles
  ⚠️ Partial: 2 titles (missing collect data)
  ❌ Failed: 1 title (no URL)
  💰 Total cost: $0.24
  ⏱️ Duration: 7m 42s

Stage Success Rates:
  Collect: 75% (9/12)
  Embed: 100% (12/12)
  Comps: 92% (11/12)
  Format Fit: 92% (11/12)

Recommendations:
  - 1 title missing platform URL (add manually)
  - 2 titles have limited data (run /batch-intelligence first)
```

## Pipeline Status Report

```sql
-- Coverage report
SELECT
  COUNT(*) as total_titles,
  COUNT(*) FILTER (WHERE views IS NOT NULL) as has_metrics,
  COUNT(*) FILTER (WHERE combined_embedding IS NOT NULL) as has_embedding,
  COUNT(*) FILTER (WHERE comps IS NOT NULL AND array_length(comps, 1) > 0) as has_comps,
  COUNT(*) FILTER (WHERE title_id IN (SELECT title_id FROM title_format_fit)) as has_format_fit,
  ROUND(100.0 * COUNT(*) FILTER (
    WHERE views IS NOT NULL
      AND combined_embedding IS NOT NULL
      AND comps IS NOT NULL
      AND title_id IN (SELECT title_id FROM title_format_fit)
  ) / COUNT(*), 1) as complete_pct
FROM titles;

-- Recent titles pipeline status
SELECT
  t.title_name_en,
  DATE(t.created_at) as added,
  CASE WHEN t.views IS NULL THEN '❌' ELSE '✅' END as collect,
  CASE WHEN t.combined_embedding IS NULL THEN '❌' ELSE '✅' END as embed,
  CASE WHEN t.comps IS NULL THEN '❌' ELSE '✅' END as comps,
  CASE WHEN f.id IS NULL THEN '❌' ELSE '✅' END as format_fit
FROM titles t
LEFT JOIN title_format_fit f ON t.title_id = f.title_id
WHERE t.created_at > NOW() - INTERVAL '14 days'
ORDER BY t.created_at DESC;
```

## Error Handling

### Stage Dependencies

| Stage | Requires | Can Skip |
|-------|----------|----------|
| Collect | Platform URL | Yes (if data exists) |
| Embed | Synopsis or title name | No (always possible) |
| Comps | Synopsis + genre (ideal) | Yes (limited mode) |
| Format Fit | Synopsis + genre (ideal) | Yes (limited mode) |

### Retry Strategy

```javascript
async function runStageWithRetry(stageFn, titleId, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const result = await stageFn(titleId);
      if (result.success) return result;

      // Retryable errors
      if (result.error?.includes('timeout') || result.error?.includes('rate limit')) {
        await delay(5000 * attempt); // Exponential backoff
        continue;
      }

      // Non-retryable error
      return result;

    } catch (error) {
      if (attempt === maxRetries) {
        return { success: false, error: error.message };
      }
      await delay(5000 * attempt);
    }
  }
}
```

### Common Errors

| Error | Stage | Resolution |
|-------|-------|------------|
| `No platform URL found` | Collect | Add URL to title record |
| `Insufficient data` | Comps/Format | Run collect first |
| `API timeout` | Any AI stage | Retry with backoff |
| `Rate limit exceeded` | Any | Increase delay between requests |

## Porting Guide

To port the pipeline concept to another app:

### 1. Pipeline Service Template

Create `apps/[app]/src/services/pipelineService.ts`:

```typescript
import { supabase } from '@/integrations/supabase/client';

const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;

export interface PipelineStage {
  name: string;
  status: 'pending' | 'running' | 'success' | 'failed' | 'skipped';
  duration_ms?: number;
  cost?: number;
  error?: string;
}

export interface PipelineResult {
  title_id: string;
  stages: Record<string, PipelineStage>;
  total_cost: number;
  total_time_ms: number;
  success: boolean;
}

export interface PipelineOptions {
  skipCollect?: boolean;
  skipEmbed?: boolean;
  skipComps?: boolean;
  skipFormatFit?: boolean;
  stopOnError?: boolean;
}

export async function runPipeline(
  titleId: string,
  options: PipelineOptions = {}
): Promise<PipelineResult> {
  const { data: { session } } = await supabase.auth.getSession();
  const token = session?.access_token;

  const result: PipelineResult = {
    title_id: titleId,
    stages: {},
    total_cost: 0,
    total_time_ms: 0,
    success: true
  };

  const stages = [
    { name: 'collect', endpoint: 'title-intelligence', skip: options.skipCollect },
    { name: 'embed', endpoint: 'regenerate-embeddings', skip: options.skipEmbed },
    { name: 'comps', endpoint: 'comps-generator', skip: options.skipComps },
    { name: 'format_fit', endpoint: 'format-fit-engine', skip: options.skipFormatFit }
  ];

  for (const stage of stages) {
    if (stage.skip) {
      result.stages[stage.name] = { name: stage.name, status: 'skipped' };
      continue;
    }

    result.stages[stage.name] = { name: stage.name, status: 'running' };

    try {
      const startTime = Date.now();
      const response = await fetch(
        `${SUPABASE_URL}/functions/v1/${stage.endpoint}`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ title_id: titleId })
        }
      );

      const data = await response.json();
      const duration = Date.now() - startTime;

      result.stages[stage.name] = {
        name: stage.name,
        status: data.success ? 'success' : 'failed',
        duration_ms: duration,
        cost: data.cost_estimate || 0,
        error: data.error
      };

      result.total_cost += data.cost_estimate || 0;
      result.total_time_ms += duration;

      if (!data.success && options.stopOnError) {
        result.success = false;
        break;
      }

    } catch (error: any) {
      result.stages[stage.name] = {
        name: stage.name,
        status: 'failed',
        error: error.message
      };
      result.success = false;
      if (options.stopOnError) break;
    }
  }

  return result;
}

export function estimateCost(titleCount: number): { cost: number; time: number } {
  return {
    cost: titleCount * 0.022,
    time: titleCount * 45 // seconds
  };
}
```

### 2. Pipeline Progress Component

Create `apps/[app]/src/components/PipelineProgress.tsx`:

```typescript
import { PipelineStage } from '@/services/pipelineService';
import { CheckCircle2, XCircle, Loader2, SkipForward } from 'lucide-react';

interface Props {
  stages: Record<string, PipelineStage>;
}

export function PipelineProgress({ stages }: Props) {
  const stageOrder = ['collect', 'embed', 'comps', 'format_fit'];
  const stageLabels: Record<string, string> = {
    collect: 'Collect Data',
    embed: 'Generate Embedding',
    comps: 'Generate Comps',
    format_fit: 'Analyze Format Fit'
  };

  return (
    <div className="space-y-3">
      {stageOrder.map((stageName) => {
        const stage = stages[stageName];
        if (!stage) return null;

        return (
          <div key={stageName} className="flex items-center gap-3">
            {stage.status === 'success' && (
              <CheckCircle2 className="w-5 h-5 text-green-500" />
            )}
            {stage.status === 'failed' && (
              <XCircle className="w-5 h-5 text-red-500" />
            )}
            {stage.status === 'running' && (
              <Loader2 className="w-5 h-5 text-blue-500 animate-spin" />
            )}
            {stage.status === 'skipped' && (
              <SkipForward className="w-5 h-5 text-gray-400" />
            )}
            {stage.status === 'pending' && (
              <div className="w-5 h-5 rounded-full border-2 border-gray-300" />
            )}

            <div className="flex-1">
              <span className="font-medium">{stageLabels[stageName]}</span>
              {stage.duration_ms && (
                <span className="text-sm text-gray-500 ml-2">
                  ({(stage.duration_ms / 1000).toFixed(1)}s)
                </span>
              )}
              {stage.error && (
                <p className="text-sm text-red-500">{stage.error}</p>
              )}
            </div>

            {stage.cost !== undefined && stage.cost > 0 && (
              <span className="text-sm text-gray-500">
                ${stage.cost.toFixed(4)}
              </span>
            )}
          </div>
        );
      })}
    </div>
  );
}
```

### 3. Pipeline Button Component

```typescript
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from '@/components/ui/dialog';
import { runPipeline, PipelineResult, estimateCost } from '@/services/pipelineService';
import { PipelineProgress } from './PipelineProgress';
import { Workflow, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

interface Props {
  titleId: string;
  titleName: string;
  onComplete?: (result: PipelineResult) => void;
}

export function RunPipelineButton({ titleId, titleName, onComplete }: Props) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PipelineResult | null>(null);

  const estimate = estimateCost(1);

  const handleRun = async () => {
    setLoading(true);
    setResult(null);

    try {
      const pipelineResult = await runPipeline(titleId);
      setResult(pipelineResult);

      if (pipelineResult.success) {
        toast.success('Pipeline completed successfully');
      } else {
        toast.warning('Pipeline completed with some errors');
      }

      onComplete?.(pipelineResult);
    } catch (error: any) {
      toast.error(`Pipeline failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm">
          <Workflow className="w-4 h-4 mr-2" />
          Run Pipeline
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Run Title Pipeline</DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <p className="font-medium">{titleName}</p>
            <p className="text-sm text-gray-500 mt-1">
              Est. cost: ${estimate.cost.toFixed(3)} | Est. time: ~{estimate.time}s
            </p>
          </div>

          {result && <PipelineProgress stages={result.stages} />}

          {result && (
            <div className="p-3 bg-gray-100 rounded-lg text-sm">
              <div className="flex justify-between">
                <span>Total cost:</span>
                <span>${result.total_cost.toFixed(4)}</span>
              </div>
              <div className="flex justify-between">
                <span>Total time:</span>
                <span>{(result.total_time_ms / 1000).toFixed(1)}s</span>
              </div>
            </div>
          )}

          <Button
            onClick={handleRun}
            disabled={loading}
            className="w-full"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                Running Pipeline...
              </>
            ) : result ? (
              'Run Again'
            ) : (
              'Start Pipeline'
            )}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
```

## Automation Triggers

### New Title Webhook

Automatically run pipeline when new titles are added:

```typescript
// In handle-new-title edge function
const { title_id, title_name_en } = payload;

// Run pipeline asynchronously
fetch(`${SUPABASE_URL}/functions/v1/title-pipeline`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${SERVICE_ROLE_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title_id,
    mode: 'new_title',
    notify_on_complete: true
  })
});
```

### Scheduled Batch

Run nightly for recent additions:

```sql
-- Cron job query: titles added today without pipeline completion
SELECT title_id FROM titles
WHERE DATE(created_at) = CURRENT_DATE
  AND (
    combined_embedding IS NULL
    OR comps IS NULL
    OR title_id NOT IN (SELECT title_id FROM title_format_fit)
  );
```

## Related Skills

- `/batch-intelligence` - Collect data only (Stage 1)
- `/regenerate-embeddings` - Update embeddings only (Stage 2)
- `/batch-comps` - Generate comps only (Stage 3)
- `/batch-format-fit` - Analyze format fit only (Stage 4)
- `/health-check` - Verify all services before pipeline run
- `/cost-report` - Track pipeline costs over time
