---
name: valyu-search
description: Complete Valyu API toolkit with Search, Answer, Contents extraction, and DeepResearch. Use for web/academic/financial search, AI-powered answers, content extraction from URLs, and async deep research reports. Supports syntax like "Valyu(command, args)" for search, answer, contents, and deepresearch operations.
---

# Valyu Complete API Tool

Comprehensive CLI tool for all Valyu APIs: Search, Answer, Contents, and DeepResearch.

## Installation

Requirements:
1. Node.js 18+ (uses built-in fetch)
2. Set environment variable: `export VALYU_API_KEY=your-api-key`
3. Scripts are executable (already set in packaged skill)

## Commands Overview

### 1. SEARCH - Multi-domain search
```bash
scripts/valyu search <type> <query> [maxResults]
```

### 2. ANSWER - AI-powered answers
```bash
scripts/valyu answer <query> [--fast] [--structured <schema>]
```

### 3. CONTENTS - Extract content from URLs
```bash
scripts/valyu contents <url> [--summary [instructions]] [--structured <schema>]
```

### 4. DEEPRESEARCH - Async research reports
```bash
scripts/valyu deepresearch create <query> [--model <fast|lite|heavy>] [--pdf]
scripts/valyu deepresearch status <task-id>
```

## 1. SEARCH API

### Search Types

| Type | Description | Sources |
|------|-------------|---------|
| `web` | General web search | All web sources |
| `finance` | Financial data | Stocks, SEC, earnings, crypto, forex |
| `paper` | Academic papers | arXiv, bioRxiv, medRxiv, PubMed |
| `bio` | Biomedical research | PubMed, clinical trials, drug labels |
| `patent` | Patent databases | Patent filings |
| `sec` | SEC filings | 10-K, 10-Q, 8-K reports |
| `economics` | Economic data | BLS, FRED, World Bank |
| `news` | News articles | News sources |

### Usage Examples

```bash
# Web search
scripts/valyu search web "AI developments 2025" 10

# Academic papers
scripts/valyu search paper "transformer architectures" 15

# Financial data
scripts/valyu search finance "Apple earnings Q4 2024" 8

# Biomedical research
scripts/valyu search bio "cancer immunotherapy clinical trials"
```

### Output Format

```json
{
  "success": true,
  "type": "search",
  "searchType": "web",
  "query": "AI news",
  "resultCount": 10,
  "results": [
    {
      "title": "Article Title",
      "url": "https://example.com",
      "content": "Full content...",
      "source": "web",
      "relevance_score": 0.95
    }
  ],
  "cost": 0.025
}
```

## 2. ANSWER API

AI-powered answers with real-time search integration.

### Basic Usage

```bash
# Simple answer
scripts/valyu answer "What is quantum computing?"

# Fast mode (quicker, less comprehensive)
scripts/valyu answer "Latest AI news" --fast

# With structured output
scripts/valyu answer "Top tech companies 2024" --structured '{
  "type": "object",
  "properties": {
    "companies": {
      "type": "array",
      "items": {"type": "string"}
    },
    "market_summary": {"type": "string"}
  }
}'
```

### Features

- **Fast Mode**: Lower latency, finance and web sources prioritized
- **Structured Output**: Define JSON schema for consistent responses
- **Source Citations**: Returns sources used in the answer
- **Search Integration**: Automatically searches relevant sources

### Output Format

```json
{
  "success": true,
  "type": "answer",
  "query": "What is quantum computing?",
  "answer": "Quantum computing is...",
  "data_type": "unstructured",
  "sources": [
    {
      "title": "Source Title",
      "url": "https://example.com"
    }
  ],
  "cost": 0.032
}
```

## 3. CONTENTS API

Extract clean, structured content from web pages.

### Basic Usage

```bash
# Extract raw content
scripts/valyu contents "https://techcrunch.com/article"

# Extract with AI summary
scripts/valyu contents "https://example.com" --summary

# Extract with custom instructions
scripts/valyu contents "https://example.com" --summary "Summarize key findings in 2 paragraphs"

# Extract structured data
scripts/valyu contents "https://product-page.com" --structured '{
  "type": "object",
  "properties": {
    "product_name": {"type": "string"},
    "price": {"type": "number"},
    "features": {
      "type": "array",
      "items": {"type": "string"}
    }
  },
  "required": ["product_name", "price"]
}'
```

### Features

- **Batch Processing**: Process multiple URLs (up to 10)
- **AI-Powered Summarization**: Generate summaries with custom instructions
- **Structured Extraction**: Extract specific data points using JSON schema
- **Response Length Control**: short (25k), medium (50k), large (100k), max
- **Extract Effort**: normal, high, auto

### Response Length Options

| Length | Characters | Use For |
|--------|-----------|---------|
| `short` | 25,000 | Summaries, key points |
| `medium` | 50,000 | Articles, blog posts (default) |
| `large` | 100,000 | Academic papers, long-form |
| `max` | Unlimited | Full document extraction |

### Output Format

```json
{
  "success": true,
  "type": "contents",
  "urls_requested": 1,
  "urls_processed": 1,
  "urls_failed": 0,
  "results": [
    {
      "title": "Article Title",
      "url": "https://example.com",
      "content": "Extracted content...",
      "data_type": "unstructured",
      "summary_success": true,
      "length": 12840
    }
  ],
  "total_cost": 0.001
}
```

## 4. DEEPRESEARCH API

Asynchronous deep research with comprehensive reports.

### Research Modes

| Mode | Use Case | Typical Time |
|------|----------|--------------|
| `fast` | Quick lookups, simple questions | ~5 minutes |
| `lite` | Balanced research (default) | ~10-20 minutes |
| `heavy` | In-depth analysis, complex research | Up to ~90 minutes |

### Create Research Task

```bash
# Basic research (lite mode, markdown)
scripts/valyu deepresearch create "AI market trends 2024"

# Heavy mode with PDF output
scripts/valyu deepresearch create "Climate change mitigation strategies" --model heavy --pdf

# Fast mode for quick lookup
scripts/valyu deepresearch create "Current Bitcoin price trends" --model fast
```

### Check Task Status

```bash
scripts/valyu deepresearch status f992a8ab-4c91-4322-905f-190107bd5a5b
```

### Output Formats

- **Markdown**: Default, clean formatted report
- **PDF**: Add `--pdf` flag for downloadable PDF
- **JSON Schema**: Custom structured output (advanced)

### Task Lifecycle

```
queued → running → completed/failed
```

**Statuses:**
- `queued`: Waiting to start
- `running`: Actively researching
- `completed`: Research finished
- `failed`: Error occurred
- `cancelled`: User cancelled

### Create Response

```json
{
  "success": true,
  "type": "deepresearch_create",
  "deepresearch_id": "f992a8ab-4c91-4322-905f-190107bd5a5b",
  "status": "queued",
  "query": "AI market trends 2024",
  "model": "lite",
  "created_at": 1759617800000
}
```

### Status Response

```json
{
  "success": true,
  "type": "deepresearch_status",
  "deepresearch_id": "f992a8ab-4c91-4322-905f-190107bd5a5b",
  "status": "completed",
  "query": "AI market trends 2024",
  "output": "# AI Market Trends 2024\n\n## Overview...",
  "pdf_url": "https://storage.valyu.ai/reports/...",
  "sources": [
    {
      "title": "Market Analysis 2024",
      "url": "https://example.com",
      "snippet": "Key findings...",
      "source": "web",
      "word_count": 2500
    }
  ],
  "progress": {
    "current_step": 5,
    "total_steps": 5
  },
  "usage": {
    "search_cost": 0.0075,
    "ai_cost": 0.15,
    "total_cost": 0.1575
  },
  "completed_at": 1759617836483
}
```

## Processing Results

### With jq

```bash
# Get search result titles
scripts/valyu search web "AI" 5 | jq '.results[].title'

# Get answer text
scripts/valyu answer "What is AI?" | jq -r '.answer'

# Get extracted content
scripts/valyu contents "https://example.com" | jq -r '.results[].content'

# Get research output
scripts/valyu deepresearch status <task-id> | jq -r '.output'

# Check if completed
result=$(scripts/valyu deepresearch status <task-id>)
if echo "$result" | jq -e '.status == "completed"' > /dev/null; then
  echo "Research complete!"
fi
```

## Error Handling

All commands return JSON with `success` field:

```json
{
  "success": false,
  "error": "Error message"
}
```

Exit codes:
- `0` - Success
- `1` - Error (check JSON for details)

## Use Cases

### Research Assistant
```bash
# Deep research with PDF
scripts/valyu deepresearch create "Blockchain in healthcare" --model heavy --pdf
```

### News Monitoring
```bash
# Latest news
scripts/valyu search news "AI regulation EU" 20
```

### Content Aggregation
```bash
# Extract and summarize
scripts/valyu contents "https://blog.com/post" --summary "Key takeaways in bullet points"
```

### Quick Q&A
```bash
# Fast answer
scripts/valyu answer "Who won the 2024 election?" --fast
```

### Academic Research
```bash
# Search papers
scripts/valyu search paper "CRISPR gene editing 2024" 15
```

### Financial Analysis
```bash
# Get financial data
scripts/valyu search finance "Tesla stock performance 2024" 10
```

## Requirements

- **Node.js 18+** - For built-in fetch API
- **VALYU_API_KEY** - Environment variable
- **No npm packages** - Direct API calls only

Get API key: https://platform.valyu.ai ($10 free credits)

## API Endpoints Used

- `/v1/search` - Search API
- `/v1/answer` - Answer API  
- `/v1/contents` - Contents API
- `/v1/deepresearch/tasks` - DeepResearch API
- `/v1/deepresearch/tasks/{id}/status` - Task status

## Architecture

```
scripts/
├── valyu          # Bash wrapper
└── valyu.mjs      # Node.js CLI (all APIs)
```

Direct API calls using Node.js built-in `fetch()`, zero external dependencies.
