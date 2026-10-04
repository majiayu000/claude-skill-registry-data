---
name: skill-curator
description: |
  Find the best Claude Code Skills for your goals. Searches 117,000+ skills from
  SkillsMP using keyword and AI semantic search via Skill Curator Actor on Apify.
  Returns optimized workflow plans with quality-scored skill recommendations.
  Use when the user wants to find skills, discover skills, recommend skills,
  search for skills, curate skills, or asks "what skills should I use?",
  "find me a skill for...", "which skill can...", "suggest skills for...",
  "help me find tools/skills for my project".
  「スキルを見繕って」「〜したいのに使えるSkillは？」「おすすめのSkillを教えて」
  「〜に使えるスキルを探して」「Skillを検索して」で発動。
argument-hint: [your goal or what you want to achieve]
allowed-tools: mcp__apify__call_actor
---

# Skill Curator — Find the Best Claude Code Skills

Discover the right Skills for any task from 117,000+ options, with **quality verification** powered by GitHub enrichment.

## How It Works

1. **Analyze** your goal and break it into actionable tasks
2. **Search** the SkillsMP database (keyword + AI semantic search)
3. **Verify** each skill's quality via GitHub (stars, freshness, documentation, license)
4. **Score** skills on a 0–100 quality scale
5. **Present** a structured workflow plan with ranked recommendations

## What Makes This Different

Unlike basic keyword search, every result is **enriched with GitHub data** and scored across 4 axes:

| Axis | Weight | What It Measures |
|------|--------|------------------|
| Popularity | 25% | GitHub stars (logarithmic scale) |
| Freshness | 25% | Days since last push |
| Documentation | 35% | SKILL.md quality (frontmatter, description, examples) |
| License | 15% | Open-source license presence |

## Prerequisites

**Required**: Apify MCP configured in your Claude Code environment.

### Setup (one-time, ~3 minutes)

1. **Get an Apify API token** (free tier available)
   - Sign up at https://apify.com
   - Go to Settings → Integrations → API tokens
   - Create a new token and copy it

2. **Add Apify MCP to your Claude Code settings**

   Add the following to your Claude Code MCP settings (`~/.claude/settings.json` or project-level `.claude/settings.json`):

   ```json
   {
     "mcpServers": {
       "apify": {
         "command": "npx",
         "args": ["-y", "@apify/actors-mcp-server"],
         "env": {
           "APIFY_TOKEN": "apify_api_YOUR_TOKEN_HERE"
         }
       }
     }
   }
   ```

3. **Restart Claude Code** to pick up the new MCP server

### Verify Setup

After restarting, you can verify by asking Claude: "List available MCP tools". You should see `mcp__apify__call_actor` in the list.

## Usage

```
/skill-curator [your goal]
```

### Examples

```
/skill-curator Build a REST API with authentication and deploy to AWS
/skill-curator 技術書を執筆してPDF出版したい
/skill-curator Analyze CSV data and create interactive visualizations
/skill-curator Set up a CI/CD pipeline for a monorepo
```

## Pricing

Each search costs approximately **$0.15** on your Apify account (Pay-Per-Event billing).
A typical invocation runs 1–3 searches depending on goal complexity.

| Goal Complexity | Searches | Estimated Cost |
|-----------------|----------|----------------|
| Simple (single task) | 1 | ~$0.15 |
| Moderate (3-5 tasks) | 1–2 | ~$0.15–$0.30 |
| Complex (6+ tasks) | 2–3 | ~$0.30–$0.45 |

---

## Processing Instructions

When the user invokes this skill with `$ARGUMENTS`, follow these steps precisely.

### Step 0: Preflight Check

Before searching, confirm Apify MCP is available by checking that you have access to the `mcp__apify__call_actor` tool. If the tool is not available, inform the user:

> Apify MCP is not configured. Please follow the setup instructions:
>
> 1. Get a free Apify API token at https://apify.com (Settings → Integrations)
> 2. Add the Apify MCP server to your Claude Code settings (see README for details)
> 3. Restart Claude Code
>
> Need help? See: https://github.com/apify/actors-mcp-server

Do NOT proceed without `mcp__apify__call_actor` access.

### Step 1: Goal Analysis

Analyze the user's goal: `$ARGUMENTS`

Identify:
- **Primary objective**: The main thing they want to accomplish
- **Secondary objectives**: Supporting tasks implied by the goal
- **Domain**: Area this falls into (web dev, data, document, DevOps, etc.)
- **Complexity**: Simple (1-2 tasks) / Moderate (3-5) / Complex (6-8)

### Step 2: Search Query Generation

Based on the analysis, generate **1 to 3 search queries** in English:

- **Primary query**: Broad query covering the main goal (ALWAYS run this)
- **Refinement query 1**: Targeted at an under-covered sub-task (only if needed)
- **Refinement query 2**: For a specialized domain aspect (only if needed)

**Guidelines for query generation**:
- Use English for best results (SkillsMP index is English-dominant)
- Keep queries concise: 3-6 words work best for keyword search
- For complex/nuanced goals, enable AI semantic search (`includeAiSearch: true`)
- Use domain-specific terms (e.g., "REST API authentication" not "make secure backend")

### Step 3: Call Skill Curator Actor

For each query, call the Apify Actor using the `mcp__apify__call_actor` tool:

**Parameters**:
- `actorId`: `"C5SaxR8oWbctCy0Ai"`
- `input`: JSON object with:
  - `query` (string, required): The search query
  - `limit` (number, optional, default 10): Max results (1-20)
  - `includeAiSearch` (boolean, optional, default false): Enable AI semantic search for better relevance (adds ~8s latency)
  - `minStars` (number, optional, default 0): Minimum GitHub stars filter

**Example call**:
```
mcp__apify__call_actor({
  actorId: "C5SaxR8oWbctCy0Ai",
  input: {
    "query": "REST API authentication middleware",
    "limit": 10,
    "includeAiSearch": true,
    "minStars": 0
  }
})
```

**Cost optimization**:
- For simple goals: 1 search with `limit: 10`
- For moderate goals: 1-2 searches with `limit: 10`
- For complex goals: 2-3 searches with `limit: 10-15`
- Enable `includeAiSearch` only when keyword results are likely insufficient (natural language queries, niche domains)

**If multiple searches are needed and they are independent, run them in parallel.**

### Step 4: Process Enriched Results

The Actor returns enriched results with this structure per item:

```json
{
  "name": "skill-name",
  "author": "author-name",
  "description": "...",
  "githubUrl": "https://github.com/...",
  "skillUrl": "https://skillsmp.com/...",
  "qualityScore": {
    "overall": 72,
    "popularity": 65,
    "freshness": 80,
    "documentation": 75,
    "license": 100
  },
  "repoMetadata": {
    "stars": 234,
    "forks": 12,
    "openIssues": 3,
    "license": "MIT",
    "lastPush": "2026-01-15T...",
    "topics": ["claude", "skill"]
  },
  "skillMdAnalysis": {
    "hasFrontmatter": true,
    "hasName": true,
    "hasDescription": true,
    "hasAllowedTools": true,
    "bodyLength": 2450,
    "hasExamples": true
  },
  "searchSource": "keyword"
}
```

**Processing**:
1. Aggregate results from all searches
2. Deduplicate by `author/name` (keep the one with higher `qualityScore.overall`)
3. Sort by `qualityScore.overall` descending
4. Map each result to the user's tasks based on description relevance

### Step 5: Skill Selection

For each task in the workflow, select the best skill:

**Selection criteria** (in order of priority):
1. **Relevance**: Does the skill's description match the task?
2. **Quality Score**: Higher `qualityScore.overall` is better
3. **Documentation**: `qualityScore.documentation` ≥ 50 preferred (well-documented skills)
4. **Freshness**: `qualityScore.freshness` ≥ 60 preferred (actively maintained)
5. **Author**: `anthropics` (official) > well-known authors > others

**Quality tiers**:
- 🟢 **80-100**: Excellent — highly recommended
- 🟡 **50-79**: Good — solid choice
- 🟠 **30-49**: Fair — usable but check before relying on it
- 🔴 **0-29**: Low — consider alternatives

### Step 6: Output Generation

**CRITICAL: Language matching rule.**
Detect the language of the user's original prompt (`$ARGUMENTS`). The ENTIRE output — section
headings, table headers, labels, and prose — MUST be written in that same language.
Do NOT copy Japanese labels when the prompt is in English, and vice versa.

Below are two template variants. Use the one matching the detected language.
For languages other than English or Japanese, follow the English template structure
but translate all labels into the detected language.

---

#### Template A: English (use when prompt is in English)

## Best Skills for "$ARGUMENTS"

### Summary

[1-2 sentence summary of the recommended approach]

### Workflow Plan

| # | Task | Recommended Skill | Quality | Stars | Reason | Depends |
|---|------|-------------------|---------|-------|--------|---------|
| 1 | [task] | `/[skill-name]` | 🟢 85 | ⭐ N | [brief reason] | - |
| 2 | [task] | `/[skill-name]` | 🟡 62 | ⭐ N | [brief reason] | #1 |
| ... | ... | ... | ... | ... | ... | ... |

### Skill Details

#### 1. [skill-name] — Quality: [score]/100

| Metric | Score | Details |
|--------|-------|---------|
| Overall | [score]/100 | [tier emoji] |
| Popularity | [score]/100 | ⭐ [stars] stars |
| Freshness | [score]/100 | Last updated: [date] |
| Documentation | [score]/100 | [frontmatter/description/examples status] |
| License | [score]/100 | [license name or "None"] |

- **Author**: [author]
- **Install**: Search "[skill-name]" on [SkillsMP](https://skillsmp.com) or install from [GitHub]([githubUrl])
- **Usage**: `/[skill-name] [typical arguments]`
- **Description**: [description]

[Repeat for each recommended skill]

### Alternatives

| Task | Alternative Skill | Quality | Notes |
|------|-------------------|---------|-------|
| [task] | `/[alt-skill]` | [score] | [when to use instead] |

### Search Summary

| Item | Value |
|------|-------|
| Searches | N |
| Search mode | Keyword / AI / Both |
| Results | N (after dedup) |
| Recommended | N skills |
| Est. cost | ~$X.XX |

---

#### Template B: Japanese (use when prompt is in Japanese)

## 「$ARGUMENTS」に最適なSkills

### 概要

[1-2 sentence summary of the recommended approach]

### Workflow Plan

| # | タスク | 推奨Skill | Quality | Stars | 理由 | 依存 |
|---|--------|-----------|---------|-------|------|------|
| 1 | [task] | `/[skill-name]` | 🟢 85 | ⭐ N | [brief reason] | - |
| 2 | [task] | `/[skill-name]` | 🟡 62 | ⭐ N | [brief reason] | #1 |
| ... | ... | ... | ... | ... | ... | ... |

### Skill Details

#### 1. [skill-name] — Quality: [score]/100

| 指標 | スコア | 詳細 |
|------|--------|------|
| Overall | [score]/100 | [tier emoji] |
| Popularity | [score]/100 | ⭐ [stars] stars |
| Freshness | [score]/100 | Last updated: [date] |
| Documentation | [score]/100 | [frontmatter/description/examples status] |
| License | [score]/100 | [license name or "None"] |

- **Author**: [author]
- **Install**: Search "[skill-name]" on [SkillsMP](https://skillsmp.com) or install from [GitHub]([githubUrl])
- **Usage**: `/[skill-name] [typical arguments]`
- **Description**: [description]

[Repeat for each recommended skill]

### 代替オプション

| タスク | 代替Skill | Quality | 備考 |
|--------|-----------|---------|------|
| [task] | `/[alt-skill]` | [score] | [when to use instead] |

### 検索サマリー

| 項目 | 値 |
|------|------|
| 検索回数 | N 回 |
| 検索方式 | Keyword / AI / Both |
| ヒット数 | N 件 (重複除外後) |
| 推薦Skill数 | N 件 |
| 推定コスト | ~$X.XX |

---

## Notes

- Quality scores are calculated from real-time GitHub data (stars, last push, SKILL.md quality, license)
- AI semantic search is slower (~8s) but finds more relevant results for natural language queries
- Each search costs ~$0.15 on your Apify account
- This skill does NOT call other skills — it recommends them for you to install and use

## Troubleshooting

**"mcp__apify__call_actor not available"**
- Verify Apify MCP is configured in your Claude Code settings
- Check the server name is "apify" (this determines the tool prefix)
- Restart Claude Code after configuration changes

**Actor errors?**
- Check your Apify token is valid at https://console.apify.com
- Ensure you have sufficient Apify credits (each run costs ~$0.15)

**No relevant results?**
- Try rephrasing your goal more specifically
- Enable AI semantic search for better relevance on complex queries
- Use English search terms for broader coverage

**Unexpected quality scores?**
- Quality scores use real-time GitHub data — scores change as repos are updated
- Skills without GitHub repos get lower scores (no enrichment data available)
- New skills may score low on popularity despite being high quality
