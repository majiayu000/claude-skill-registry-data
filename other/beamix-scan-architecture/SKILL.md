---
name: beamix-scan-architecture
last_updated: 2026-05-17
description: "Beamix's GEO scan pipeline: Perplexity research phase, three engine queries (ChatGPT, Gemini, Perplexity), Gemini Flash analysis, result storage in scan_engine_results, and the OPENROUTER_SCAN_KEY vs OPENROUTER_AGENT_KEY API key split. Use when implementing or debugging any scan-related API route or Inngest function."
tags: [ai, beamix-specific, backend, scan]
source: beamix-authored 2026-05-16
risk: low
---

# Beamix Scan Architecture

## Quick reference

> Scan = 1 user click → 1 Inngest event → fan-out to engine adapters → fan-in to `scan_engine_results` → recommendations via Claude Haiku. Never block UI.

## When to use

- Implementing a new scan engine adapter
- Debugging why a scan returned unexpected results
- Adding a new analysis step to the scan pipeline
- Understanding why two API keys are used instead of one

## When NOT to use

- For agent jobs (agent execution is a separate pipeline under `src/inngest/functions/agent-execute.ts`)
- For free scan vs authenticated scan differences — this covers both, but check the specific Inngest function

## Pipeline overview

```
Business URL input
       ↓
[Stage 1] Perplexity research
  — Query: "What is {business_name}? What do they do? What problems do they solve?"
  — Outputs: business_summary, key_services[], target_audience
       ↓
[Stage 2] Three engine queries (parallel Inngest steps)
  engine A: ChatGPT (GPT-4o via OpenRouter)
  engine B: Gemini (gemini-1.5-pro via OpenRouter)
  engine C: Perplexity (pplx-70b-online via OpenRouter)
  — Each query: "Who are the best {category} providers in {location}?"
  — Outputs: is_mentioned, rank_position, sentiment, raw_response
       ↓
[Stage 3] Gemini Flash analysis
  — Reads all three raw_responses
  — Outputs: overall_score (0-100), diagnosis[], recommendations[]
       ↓
[Stage 4] Persist to DB
  — Insert into scan_engine_results (one row per engine)
  — Update scans table with status=complete
```

## API key split (IMPORTANT)

Two separate OpenRouter keys are used to isolate spend and allow per-key rate limiting:

| Key | Purpose | Routes to |
|-----|---------|-----------|
| `OPENROUTER_SCAN_KEY` | Stage 1 + 2 only (Perplexity research + engine queries) | Only the GEO scan functions |
| `OPENROUTER_AGENT_KEY` | Stage 3 + agent jobs (Gemini Flash analysis + all agent recommendations) | Analysis + agent execution |

This split lets you kill `OPENROUTER_SCAN_KEY` without affecting agent jobs, and vice versa. It also makes cost attribution obvious.

## Inngest function structure

```typescript
// src/inngest/functions/scan-manual.ts
export const scanManual = inngest.createFunction(
  { id: 'scan-manual', concurrency: { limit: 10 } },
  { event: 'beamix/scan.manual.requested' },
  async ({ event, step }) => {

    // Stage 1: Perplexity research
    const businessContext = await step.run('perplexity-research', async () => {
      const res = await openrouter.chat({
        model: 'perplexity/llama-3.1-sonar-large-128k-online',
        messages: [{ role: 'user', content: buildResearchPrompt(event.data.businessUrl) }],
        apiKey: process.env.OPENROUTER_SCAN_KEY!,
      });
      return parseBusinessContext(res.choices[0].message.content);
    });

    // Stage 2: Three engines in parallel
    const [chatgptResult, geminiResult, perplexityResult] = await Promise.all([
      step.run('engine-chatgpt', () => queryEngine('chatgpt', businessContext, event.data)),
      step.run('engine-gemini', () => queryEngine('gemini', businessContext, event.data)),
      step.run('engine-perplexity', () => queryEngine('perplexity', businessContext, event.data)),
    ]);

    // Stage 3: Gemini Flash analysis
    const analysis = await step.run('gemini-flash-analysis', async () => {
      const res = await openrouter.chat({
        model: 'google/gemini-flash-1.5',
        messages: [{ role: 'user', content: buildAnalysisPrompt([chatgptResult, geminiResult, perplexityResult]) }],
        apiKey: process.env.OPENROUTER_AGENT_KEY!,  // Agent key for analysis
      });
      return parseAnalysis(res.choices[0].message.content);
    });

    // Stage 4: Persist
    await step.run('persist-results', async () => {
      const adminClient = createAdminSupabaseClient();
      await adminClient.from('scan_engine_results').insert([
        { scan_id: event.data.scanId, engine: 'chatgpt', ...chatgptResult },
        { scan_id: event.data.scanId, engine: 'gemini', ...geminiResult },
        { scan_id: event.data.scanId, engine: 'perplexity', ...perplexityResult },
      ]);
    });

    return { scanId: event.data.scanId, score: analysis.overall_score };
  }
);
```

## scan_engine_results table schema

```sql
CREATE TABLE scan_engine_results (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  scan_id         uuid NOT NULL REFERENCES scans(id),
  business_id     uuid NOT NULL REFERENCES businesses(id),
  engine          text NOT NULL,       -- 'chatgpt' | 'gemini' | 'perplexity'
  rank_position   int,                 -- null if not mentioned
  is_mentioned    boolean NOT NULL,
  sentiment       text,                -- 'positive' | 'neutral' | 'negative' | null
  raw_response    text,                -- store for debugging
  created_at      timestamptz DEFAULT now()
);
```

Note: `scans` table has NO `avg_position` column — compute it client-side from `scan_engine_results`.

## Engine prompt conventions

```typescript
function buildEnginePrompt(engine: string, businessContext: BusinessContext, query: QueryParams): string {
  return `You are a potential customer searching for ${query.category} services in ${query.location}.

Search query: "${query.searchTerm}"

Return your top 5 recommendations. For each, include:
- Business name
- Why you recommend them
- Any notable concerns

Business context (for relevance scoring only — do not mention in response): ${JSON.stringify(businessContext)}`;
}
```

Prompts are identical across engines to ensure comparability of results. Do not add engine-specific framing.

## Free scan vs authenticated scan

| Aspect | Free scan | Authenticated scan |
|--------|-----------|-------------------|
| Inngest function | `scan-free.ts` | `scan-manual.ts` |
| Stored in | `free_scans` (JSONB blob) | `scans` + `scan_engine_results` (normalized) |
| Engines | ChatGPT + Gemini + Perplexity | Same (plan-gated for additional engines) |
| Converted on signup | Yes — `free_scans.converted_user_id = user_id` | N/A |
| API route | `/api/scan/start` with no auth header | `/api/scan/start` with session auth |

## See also

- `llm-app-patterns` — [[llm-app-patterns]]
- `inngest` — [[inngest]]
- `supabase-rls-beamix` — [[supabase-rls-beamix]]
- `prompt-engineering-patterns` — [[prompt-engineering-patterns]]

## Anti-patterns

- Using `OPENROUTER_AGENT_KEY` for engine queries (breaks cost isolation)
- Making engine queries sequential instead of parallel (3x slower)
- Storing `avg_position` in the `scans` table (column does not exist — compute from results)
- Adding engine-specific framing to prompts (skews cross-engine comparison)
- Blocking the `/api/scan/start` route on Inngest enqueueing (return 202 immediately, let Inngest handle async)
- Using `scan_engine_responses` or `scan_result_details` — correct table names are `scans` and `scan_engine_results`
