---
name: grey-haven-llm-project-development
description: "Build LLM-powered applications and pipelines using proven methodology - task-model fit analysis, pipeline architecture, structured outputs, file-based state, and cost estimation. Use when building AI features, data processing pipelines, agents, or any LLM-integrated system. Inspired by Karpathy's methodology and production case studies."
# v2.0.43: Skills to auto-load for LLM project development
skills:
  - grey-haven-code-style
  - grey-haven-data-validation
  - grey-haven-prompt-engineering
# v2.0.74: Tools for LLM project development
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Bash
  - Grep
  - Glob
  - TodoWrite
  - WebFetch
---

# LLM Project Development Skill

Build **production LLM applications** using proven methodology from Karpathy's HN Time Capsule, Vercel d0, Manus, and Anthropic's research.

**Core principle**: Validate manually first, then build deterministic pipelines around the non-deterministic LLM core.

## Supporting Documentation

All files under 500 lines per Anthropic best practices:

- **[references/](references/)** - Methodology foundations
  - [case-studies.md](references/case-studies.md) - Karpathy, Vercel d0, Manus patterns
  - [pipeline-patterns.md](references/pipeline-patterns.md) - Python/TypeScript code patterns
  - [INDEX.md](references/INDEX.md) - Reference navigation

- **[examples/](examples/)** - Grey Haven implementations
  - [tanstack-pipeline.md](examples/tanstack-pipeline.md) - TanStack Start example
  - [fastapi-pipeline.md](examples/fastapi-pipeline.md) - FastAPI backend example
  - [INDEX.md](examples/INDEX.md) - Examples navigation

- **[templates/](templates/)** - Copy-paste starters
  - [pipeline-template.ts](templates/pipeline-template.ts) - TypeScript pipeline
  - [pipeline-template.py](templates/pipeline-template.py) - Python pipeline

- **[checklists/](checklists/)** - Validation
  - [llm-project-checklist.md](checklists/llm-project-checklist.md) - Pre-launch checklist

## The Methodology

### Phase 1: Task-Model Fit Analysis

**Before writing any code, determine if LLMs are the right tool.**

#### LLM-Suited Tasks

| Characteristic | Why LLMs Excel | Grey Haven Example |
|----------------|----------------|-------------------|
| **Synthesis over precision** | Combining context, not calculating | Summarizing tenant activity |
| **Subjective judgment** | No single correct answer | Categorizing support tickets |
| **Error tolerance** | Graceful degradation acceptable | Content recommendations |
| **Human-like processing** | Natural language understanding | Chat-based tenant onboarding |
| **Creative output** | Novel combinations required | Generating marketing copy |

#### LLM-Unsuited Tasks (Use Traditional Code)

| Characteristic | Why LLMs Fail | Better Approach |
|----------------|---------------|-----------------|
| **Precise computation** | Math errors, hallucinations | SQL queries, Python math |
| **Real-time requirements** | Latency too high | Pre-computed indices |
| **Deterministic output** | Need exact same result | Database lookups |
| **Structured data lookup** | LLMs guess, don't retrieve | Drizzle/SQLModel queries |
| **High-frequency calls** | Cost explodes | Caching, batching |

#### The Manual Prototype Step

**CRITICAL**: Before building automation, validate with the target model manually.

```markdown
## Manual Validation Checklist
- [ ] Copy ONE real example into the LLM UI
- [ ] Test with the EXACT model you'll use in production
- [ ] Verify output quality meets requirements
- [ ] Note edge cases and failure modes
- [ ] Estimate cost per operation

## Example: Karpathy's Approach
1. Took ONE Hacker News thread
2. Pasted into ChatGPT with analysis prompt
3. Confirmed Opus 4.5 could do the task
4. THEN built automation pipeline
```

### Phase 2: Pipeline Architecture

**Design principle**: Deterministic stages wrapping one non-deterministic core.

```
┌─────────────────────────────────────────────────────────────────┐
│                    DETERMINISTIC                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ ACQUIRE  │ →  │ PREPARE  │ →  │ PROCESS  │ →  │  RENDER  │  │
│  │ (fetch)  │    │ (format) │    │  (LLM)   │    │ (output) │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│       ↑              ↑               ↑              ↑          │
│  Deterministic  Deterministic  NON-DETERMINISTIC  Deterministic│
│  (retry safe)   (retry safe)   (cache results)   (retry safe) │
└─────────────────────────────────────────────────────────────────┘
```

#### Stage Details

| Stage | Purpose | Grey Haven Implementation |
|-------|---------|--------------------------|
| **Acquire** | Get raw data | Drizzle queries, Firecrawl scraping, API calls |
| **Prepare** | Format for LLM | Jinja templates, TypeScript string builders |
| **Process** | LLM inference | Anthropic SDK, structured outputs |
| **Parse** | Extract from response | Zod schemas, Pydantic models |
| **Render** | Final output | React components, markdown, JSON |

#### TypeScript Pipeline Example (TanStack Start)

```typescript
// lib/pipelines/content-analyzer.ts
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";
import { existsSync, mkdirSync, writeFileSync, readFileSync } from "fs";
import { join } from "path";

// Stage 1: Schema definition
const AnalysisSchema = z.object({
  summary: z.string(),
  sentiment: z.enum(["positive", "neutral", "negative"]),
  topics: z.array(z.string()),
  action_items: z.array(z.string()),
});

type Analysis = z.infer<typeof AnalysisSchema>;

// Stage 2: Acquire - Get data from database
async function acquire(tenant_id: string, content_id: string) {
  const content = await db.query.contents.findFirst({
    where: and(
      eq(contents.tenant_id, tenant_id),
      eq(contents.id, content_id)
    ),
  });

  if (!content) throw new Error(`Content ${content_id} not found`);
  return content;
}

// Stage 3: Prepare - Format prompt
function prepare(content: Content): string {
  return `Analyze this content and provide structured output.

CONTENT:
${content.body}

Respond with JSON matching this schema:
{
  "summary": "2-3 sentence summary",
  "sentiment": "positive" | "neutral" | "negative",
  "topics": ["topic1", "topic2"],
  "action_items": ["action1", "action2"]
}`;
}

// Stage 4: Process - LLM call with caching
async function process(
  prompt: string,
  cacheDir: string,
  cacheKey: string
): Promise<string> {
  const cachePath = join(cacheDir, `${cacheKey}.json`);

  // Check cache first
  if (existsSync(cachePath)) {
    return JSON.parse(readFileSync(cachePath, "utf-8")).response;
  }

  const client = new Anthropic();
  const response = await client.messages.create({
    model: "claude-sonnet-4-20250514",
    max_tokens: 1024,
    messages: [{ role: "user", content: prompt }],
  });

  const text = response.content[0].type === "text"
    ? response.content[0].text
    : "";

  // Cache result
  mkdirSync(cacheDir, { recursive: true });
  writeFileSync(cachePath, JSON.stringify({
    response: text,
    timestamp: new Date().toISOString()
  }));

  return text;
}

// Stage 5: Parse - Validate with Zod
function parse(response: string): Analysis {
  const jsonMatch = response.match(/\{[\s\S]*\}/);
  if (!jsonMatch) throw new Error("No JSON found in response");

  const parsed = JSON.parse(jsonMatch[0]);
  return AnalysisSchema.parse(parsed);
}

// Stage 6: Render - Save to database
async function render(
  tenant_id: string,
  content_id: string,
  analysis: Analysis
) {
  await db.update(contents)
    .set({
      analysis_summary: analysis.summary,
      analysis_sentiment: analysis.sentiment,
      analysis_topics: analysis.topics,
      updated_at: new Date(),
    })
    .where(and(
      eq(contents.tenant_id, tenant_id),
      eq(contents.id, content_id)
    ));

  return analysis;
}

// Main pipeline function
export async function analyzeContent(
  tenant_id: string,
  content_id: string
): Promise<Analysis> {
  const cacheDir = join(process.cwd(), ".cache", "analyses", tenant_id);

  const content = await acquire(tenant_id, content_id);
  const prompt = prepare(content);
  const response = await process(prompt, cacheDir, content_id);
  const analysis = parse(response);
  await render(tenant_id, content_id, analysis);

  return analysis;
}
```

#### Python Pipeline Example (FastAPI)

```python
# app/pipelines/content_analyzer.py
from pathlib import Path
from pydantic import BaseModel
from anthropic import Anthropic
import json

class Analysis(BaseModel):
    summary: str
    sentiment: str  # positive | neutral | negative
    topics: list[str]
    action_items: list[str]

class ContentAnalyzerPipeline:
    def __init__(self, tenant_id: str, cache_dir: Path | None = None):
        self.tenant_id = tenant_id
        self.cache_dir = cache_dir or Path(".cache/analyses") / tenant_id
        self.client = Anthropic()

    async def acquire(self, content_id: str, db: AsyncSession) -> Content:
        """Stage 1: Get content from database."""
        result = await db.execute(
            select(Content).where(
                Content.tenant_id == self.tenant_id,
                Content.id == content_id
            )
        )
        content = result.scalar_one_or_none()
        if not content:
            raise ValueError(f"Content {content_id} not found")
        return content

    def prepare(self, content: Content) -> str:
        """Stage 2: Format prompt."""
        return f"""Analyze this content and provide structured output.

CONTENT:
{content.body}

Respond with JSON:
{{
  "summary": "2-3 sentence summary",
  "sentiment": "positive" | "neutral" | "negative",
  "topics": ["topic1", "topic2"],
  "action_items": ["action1"]
}}"""

    async def process(self, prompt: str, cache_key: str) -> str:
        """Stage 3: LLM call with file-based caching."""
        cache_path = self.cache_dir / f"{cache_key}.json"

        # Check cache
        if cache_path.exists():
            return json.loads(cache_path.read_text())["response"]

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        text = response.content[0].text

        # Cache result
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps({
            "response": text,
            "timestamp": datetime.utcnow().isoformat()
        }))

        return text

    def parse(self, response: str) -> Analysis:
        """Stage 4: Parse and validate with Pydantic."""
        import re
        match = re.search(r'\{[\s\S]*\}', response)
        if not match:
            raise ValueError("No JSON found in response")
        return Analysis.model_validate_json(match.group())

    async def render(
        self,
        content_id: str,
        analysis: Analysis,
        db: AsyncSession
    ) -> Analysis:
        """Stage 5: Save to database."""
        await db.execute(
            update(Content)
            .where(
                Content.tenant_id == self.tenant_id,
                Content.id == content_id
            )
            .values(
                analysis_summary=analysis.summary,
                analysis_sentiment=analysis.sentiment,
                analysis_topics=analysis.topics,
                updated_at=datetime.utcnow()
            )
        )
        await db.commit()
        return analysis

    async def run(self, content_id: str, db: AsyncSession) -> Analysis:
        """Execute full pipeline."""
        content = await self.acquire(content_id, db)
        prompt = self.prepare(content)
        response = await self.process(prompt, content_id)
        analysis = self.parse(response)
        return await self.render(content_id, analysis, db)
```

### Phase 3: File System as State Machine

**Key insight from Karpathy**: File existence determines work state.

```python
# Pipeline state management
def get_pipeline_state(work_dir: Path, item_id: str) -> str:
    """Determine pipeline state from file existence."""
    item_dir = work_dir / item_id

    if not item_dir.exists():
        return "pending"
    if not (item_dir / "raw.json").exists():
        return "acquired"
    if not (item_dir / "prepared.txt").exists():
        return "prepared"
    if not (item_dir / "response.json").exists():
        return "processed"
    if not (item_dir / "analysis.json").exists():
        return "parsed"
    return "complete"

def resume_pipeline(work_dir: Path, item_id: str):
    """Resume from last successful stage."""
    state = get_pipeline_state(work_dir, item_id)

    if state == "pending":
        acquire(item_id)
    if state in ["pending", "acquired"]:
        prepare(item_id)
    if state in ["pending", "acquired", "prepared"]:
        process(item_id)
    if state in ["pending", "acquired", "prepared", "processed"]:
        parse(item_id)

    return load_analysis(item_id)
```

**Benefits**:
- **Idempotent restarts**: Kill and resume anytime
- **Debuggable**: Inspect intermediate files
- **Cost-efficient**: Never re-call LLM for completed work
- **Parallel-safe**: Each item in own directory

### Phase 4: Structured Output Design

**Disclose parsing intent to the model** - models perform better when they know how output will be used.

```markdown
## Good Prompt (Parsing Disclosed)
Analyze this article and provide structured output.

I will parse this programmatically, so respond with valid JSON matching:
{
  "summary": "2-3 sentences",
  "sentiment": "positive" | "neutral" | "negative",
  "topics": ["string array"],
  "confidence": 0.0-1.0
}

Ensure the JSON is complete and parseable.

## Bad Prompt (Parsing Hidden)
Analyze this article. Give me a summary, sentiment, and topics.
```

#### Structured Output Patterns

```typescript
// Pattern 1: Section markers for complex output
const prompt = `Analyze this document.

Respond in this exact format:
===SUMMARY===
[2-3 sentence summary]
===SENTIMENT===
[positive/neutral/negative]
===TOPICS===
[comma-separated topics]
===END===`;

function parse(response: string) {
  const sections = {
    summary: extractSection(response, "SUMMARY"),
    sentiment: extractSection(response, "SENTIMENT"),
    topics: extractSection(response, "TOPICS").split(",").map(s => s.trim()),
  };
  return sections;
}

// Pattern 2: JSON with schema disclosure
const prompt = `Analyze this content.

Respond with a JSON object. I will parse this with Zod, so ensure it matches:
{
  "summary": string (required, 50-200 chars),
  "sentiment": "positive" | "neutral" | "negative" (required),
  "topics": string[] (required, 1-5 items),
  "confidence": number (required, 0.0-1.0)
}`;
```

### Phase 5: Architectural Reduction

**Fewer tools = better performance** (Vercel d0 case study)

| Approach | Tools | Success Rate |
|----------|-------|--------------|
| Full toolset | 17 tools | 80% |
| **Reduced set** | **2 tools** | **100%** |

#### Principles

1. **Start minimal**: Only add tools when demonstrably needed
2. **Combine operations**: One tool that does A+B > two separate tools
3. **Remove unused tools**: If success rate improves, keep it removed
4. **Mask, don't delete**: Keep in context but mark unavailable (KV-cache optimization)

```typescript
// Grey Haven: Minimal tool pattern
const MINIMAL_TOOLS = [
  {
    name: "read_database",
    description: "Query tenant data using Drizzle ORM",
    // Combines: list tables, query table, get schema
  },
  {
    name: "update_record",
    description: "Update a record in the database",
    // Combines: update, insert, upsert operations
  },
];

// NOT: 10 separate CRUD tools
```

### Phase 6: Cost Estimation

**Estimate before building**, adjust architecture based on scale.

```python
def estimate_pipeline_cost(
    num_items: int,
    avg_input_tokens: int,
    avg_output_tokens: int,
    model: str = "claude-sonnet-4-20250514"
) -> dict:
    """Estimate total cost for pipeline run."""

    # Pricing per million tokens (as of Dec 2025)
    PRICING = {
        "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
        "claude-opus-4-5-20251101": {"input": 15.00, "output": 75.00},
        "claude-haiku-3-5-20241022": {"input": 0.80, "output": 4.00},
    }

    rates = PRICING[model]

    total_input = num_items * avg_input_tokens
    total_output = num_items * avg_output_tokens

    input_cost = (total_input / 1_000_000) * rates["input"]
    output_cost = (total_output / 1_000_000) * rates["output"]

    return {
        "items": num_items,
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "input_cost": f"${input_cost:.2f}",
        "output_cost": f"${output_cost:.2f}",
        "total_cost": f"${input_cost + output_cost:.2f}",
        "cost_per_item": f"${(input_cost + output_cost) / num_items:.4f}",
    }

# Example: Karpathy's HN Time Capsule
estimate_pipeline_cost(
    num_items=128,        # articles
    avg_input_tokens=2000, # article + prompt
    avg_output_tokens=500, # analysis
    model="claude-opus-4-5-20251101"
)
# Result: ~$5-10 total, $0.04-0.08 per article
```

## Agent-Assisted Development Workflow

When building LLM features with Claude Code:

### 1. Define the Task
```markdown
"I need to analyze customer support tickets and categorize them
by urgency, topic, and suggested response template."
```

### 2. Validate Manually
```markdown
1. Take one real support ticket
2. Paste into Claude.ai with your prompt
3. Verify the output quality
4. Note token usage for cost estimation
```

### 3. Design Pipeline Stages
```markdown
- Acquire: Query tickets from database (Drizzle)
- Prepare: Format ticket + customer context
- Process: Claude API call with structured output
- Parse: Validate with Zod schema
- Render: Update ticket record, notify agent
```

### 4. Implement with File Caching
```markdown
- Each ticket gets a directory: .cache/tickets/{ticket_id}/
- Stage outputs saved as JSON files
- Pipeline resumes from last successful stage
```

### 5. Estimate and Optimize
```markdown
- 1000 tickets/day × 1500 tokens avg = 1.5M tokens
- Sonnet 4: ~$4.50/day input, ~$22.50/day output
- Consider batching, caching common responses
```

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Better Approach |
|--------------|--------------|-----------------|
| **Skip manual validation** | Build automation for task LLM can't do | Always test one example first |
| **Monolithic prompts** | Can't debug, can't resume | Pipeline with stages |
| **Memory-based state** | Lose progress on crash | File system state |
| **Excessive tools** | Confuses model, lowers success | Minimal tool set |
| **Hidden parsing** | Model doesn't optimize for it | Disclose parsing intent |
| **No cost estimation** | Budget surprise at scale | Estimate before building |
| **Real-time LLM calls** | Latency kills UX | Background processing, caching |

## When to Apply This Skill

Use this skill when:
- Building any LLM-powered feature
- Creating data processing pipelines
- Implementing AI agents or assistants
- Designing chat-based interfaces
- Building content generation systems
- Creating analysis/classification pipelines
- Integrating Claude into Grey Haven apps

## Critical Reminders

1. **Manual prototype first** - Always validate with target model before automation
2. **Pipeline architecture** - Deterministic stages around non-deterministic LLM
3. **File system state** - Use file existence for pipeline progress
4. **Structured outputs** - Disclose parsing intent in prompts
5. **Minimal tools** - Fewer tools = higher success rate
6. **Cost estimation** - Calculate before building at scale
7. **Cache aggressively** - Never re-call LLM for completed work
8. **Tenant isolation** - Include tenant_id in all database queries
9. **Error tolerance** - Design for graceful degradation
10. **Incremental processing** - Build resume-friendly pipelines

## Template Reference

These patterns integrate with Grey Haven templates:
- **cvi-template**: TanStack Start + Claude integration
- **cvi-backend-template**: FastAPI + Anthropic SDK pipelines

**Skill Version**: 1.0
