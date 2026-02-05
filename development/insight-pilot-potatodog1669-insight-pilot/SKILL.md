---
name: insight-pilot
description: Literature research automation - search papers, code, and blogs, deduplicate, download PDFs, analyze and generate research reports. Supports incremental updates.
version: 0.3.0
---

# Insight-Pilot Skill

A workflow automation skill for literature research. Searches papers, GitHub repos/code/issues, PubMed, Dev.to, and blogs, deduplicates results, downloads PDFs, analyzes content, and generates incremental research reports.

## Setup

Run the bootstrap script (automatically checks environment, creates and installs if missing):

```bash
bash .codex/skills/insight-pilot/scripts/bootstrap_env.sh
```

The script automatically detects if `~/.insight-pilot-venv` exists and if packages are installed, only installing when necessary. See `--help` for advanced options.

## Usage

Before running commands, activate the environment:

```bash
source ~/.insight-pilot-venv/bin/activate
```

Then use the CLI:

```bash
insight-pilot <command> [options]
```

## CLI Commands

| Command | Purpose | Required Args | Key Optional Args |
|---------|---------|---------------|-------------------|
| `init` | Create research project | `--topic`, `--output` | `--keywords` |
| `search` | Search, merge and dedup | `--project`, `--source`, `--query` | `--limit`, `--since`, `--until` |
| `download` | Download PDFs + convert to Markdown | `--project` | - |
| `analyze` | Analyze papers with LLM | `--project` | `--config`, `--force` |
| `index` | Generate index.md | `--project` | `--template` |
| `status` | Check project state | `--project` | - |
| `sources` | Manage blog/RSS sources | `--project` | `--add`, `--remove`, `--config` |

### JSON Output Mode

Add `--json` flag for structured output (recommended for agents):

```bash
insight-pilot status --json --project ./research/myproject
```

### Blog/RSS Sources Configuration

Create `sources.yaml` in your project root:

```yaml
blogs:
  - name: "Cursor Blog"
    type: "ghost"
    url: "https://cursor.sh/blog"
    api_key: "auto"
  - name: "Example WP Blog"
    type: "wordpress"
    url: "https://blog.example.com"
  - name: "OpenAI Blog"
    type: "rss"
    url: "https://openai.com/blog/rss.xml"
    category: "ai"
```

Manage sources via:

```bash
insight-pilot sources --project ./research/webagent
```

Environment variables:
- `GITHUB_TOKEN` (GitHub API higher rate limit)
- `PUBMED_EMAIL` (required by NCBI)
- `OPENALEX_MAILTO` (OpenAlex polite usage)
- `INSIGHT_PILOT_SOURCES` (override sources.yaml path)

### New Sources Examples

```bash
# GitHub repositories + code + issues
insight-pilot search --project $PROJECT --source github --query "agent framework" --limit 30

# PubMed (requires PUBMED_EMAIL)
insight-pilot search --project $PROJECT --source pubmed --query "clinical agents" --limit 20

# Dev.to articles
insight-pilot search --project $PROJECT --source devto --query "ai agents" --limit 20

# Blogs (Ghost/WordPress/RSS from sources.yaml)
insight-pilot search --project $PROJECT --source blog --query "agents" --limit 20
```

---

## Workflow (Agent + CLI Collaboration)

This is the complete workflow for **Agent + CLI collaboration**.

**Execution Principles**:
- Run CLI commands in sequence as prescribed, no line-by-line confirmation needed.
- Agent intervention is ONLY required in Phase 2 for manual review (checking `items.json` and setting `status`/`exclude_reason`).

### Phase 1: Search and Initial Filtering

Execute the following commands directly, no confirmation needed:

```bash
PROJECT=./research/webagent

# Step 1: Initialize project
insight-pilot init --topic "WebAgent Research" --keywords "web agent,browser agent" --output $PROJECT

# Step 2: Search multiple sources (auto merge & dedup)
insight-pilot search --project $PROJECT --source arxiv openalex github pubmed devto blog --query "web agent" --limit 50
```

### Phase 2: Agent Review (Manual Check)

After deduplication, the Agent needs to review the paper list and remove content unrelated to the research topic.

```bash
# Check current status
insight-pilot status --json --project $PROJECT
```

**Agent Actions**:
1. Read `$PROJECT/.insight/items.json`
2. Check `title` and `abstract` for each paper
3. Mark unrelated papers: set `status` to `"excluded"` and add `exclude_reason`
4. Save the updated `items.json`

```json
{
  "id": "i0023",
  "title": "Unrelated Paper Title",
  "status": "excluded",
  "exclude_reason": "Not related to web agents, focuses on chemical agents"
}
```

### Phase 3: Download PDFs

Execute directly, no confirmation needed:

```bash
# Step 3: Download PDFs (converts to Markdown automatically)
insight-pilot download --project $PROJECT
```

**Download Results**:
- Success: `download_status: "success"`, PDF saved to `papers/`
- Failed: `download_status: "failed"`, recorded in `$PROJECT/.insight/download_failed.json`

Failure list format:
```json
[
  {
    "id": "i0015",
    "title": "Paper Title",
    "url": "https://...",
    "error": "Connection timeout",
    "failed_at": "2026-01-17T10:30:00Z"
  }
]
```

> **Note**: Advanced download (proxy/browser automation for failed items) is not yet implemented.

### Phase 4: Analyze Papers

**Precondition**: Must complete Phase 3 Download PDFs first (`download` command automatically converts PDFs to Markdown).

**MUST try LLM analysis first**. If LLM is configured, run directly:

```bash
# Step 4: LLM Analysis (prefers converted Markdown, falls back to PDF text extraction)
insight-pilot analyze --project $PROJECT
```

**Content Source Priority**:
1. **Markdown** (from `download` auto-conversion via pymupdf4llm)
2. **PDF Extraction** (PyMuPDF)

**LLM Configuration**: Create `.codex/skills/insight-pilot/llm.yaml`:

```yaml
provider: openai  # openai / anthropic / ollama
model: gpt-4o-mini
api_key: sk-xxx   # or set env var OPENAI_API_KEY
```

##### When LLM is not configured: Manual Analysis Required

If no LLM is configured, the Agent needs to analyze manually:

1. Read PDF files in `papers/` directory
2. Extract key information for each paper
3. Write analysis results to `$PROJECT/.insight/analysis/{id}.json`

**Analysis File Format** (`$PROJECT/.insight/analysis/{id}.json`):
```json
{
  "id": "i0001",
  "title": "Paper Title",
  "summary": "One sentence summary",
  "brief_analysis": "2-3 sentences brief analysis",
  "detailed_analysis": "300-500 words detailed analysis",
  "contributions": ["Contribution 1", "Contribution 2"],
  "methodology": "Methodology description",
  "key_findings": ["Finding 1", "Finding 2"],
  "limitations": ["Limitations"],
  "future_work": ["Future work 1"],
  "relevance_score": 8,
  "tags": ["webagent", "benchmark", "multimodal"],
  "analyzed_at": "2026-01-17T12:00:00Z"
}
```

### Phase 5: Generate Incremental Report

```bash
# Step 8: Generate/Update Index
insight-pilot index --project $PROJECT
```

Reports are stored in `$PROJECT/index.md`, showing **only analyzed papers** and linking to `reports/{id}.md` detailed reports.

**Report Structure**:
```markdown
# WebAgent Research

> **Generated**: 2026-01-18 10:30
> **Keywords**: web agent, browser agent
> **Analyzed**: 5 papers

---

## 📚 Analyzed Papers

### [Paper Title](reports/i0001.md)

**Authors**: Author A, Author B et al. | **Date**: 2026-01-15 | **Links**: arXiv/DOI | **Relevance**: 8/10

**Summary**: One sentence summary...

> 2-3 sentences brief analysis...

**Tags**: `webagent` `benchmark` `multimodal`

---

## ⚠️ Papers Not Available

_The following papers could not be downloaded. Only abstracts are shown._

### Paper Title

**Authors**: ... | **Date**: ... | **Links**: ...

> Abstract...

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Papers Analyzed | 5 |
| Download Failed | 1 |
| Total Processed | 6 |
```

---

## Incremental Update Workflow

For daily/weekly updates:

```bash
# 1. Search new papers (use --since for date limit, auto merge & dedup)
insight-pilot search --project $PROJECT --source arxiv openalex --query "web agent" --since 2026-01-17 --limit 20

# 2. [Agent] Review newly added papers

# 3. Download PDFs for new papers
insight-pilot download --project $PROJECT

# 4. [Agent] Analyze new papers, update reports

# 5. Regenerate index
insight-pilot index --project $PROJECT
```

---

## Project Structure

```
research/myproject/
├── .insight/
│   ├── config.yaml          # 项目配置
│   ├── state.json           # 工作流状态
│   ├── items.json           # 论文元数据（含 status, exclude_reason）
│   ├── raw_arxiv.json       # 原始搜索结果
│   ├── raw_openalex.json
│   ├── download_failed.json # 下载失败列表（供高级下载重试）
│   ├── analysis/            # 论文分析结果
│   │   ├── i0001.json
│   │   ├── i0002.json
│   │   └── ...
│   └── markdown/            # PDF 转换结果（pymupdf4llm）
│       ├── i0001/
│       │   ├── i0001.md     # 转换后的 Markdown
│       │   └── metadata.json
│       └── ...
├── papers/                  # 已下载的 PDF
├── reports/                 # 历史报告存档
└── index.md                 # 当前研究报告（增量更新）
```

## Data Schemas

### Item (Paper)

```json
{
  "id": "i0001",
  "type": "paper",
  "title": "Paper Title",
  "authors": ["Author One", "Author Two"],
  "date": "2026-01-15",
  "abstract": "...",
  "status": "active|excluded|pending",
  "exclude_reason": null,
  "identifiers": {
    "doi": "10.1234/example",
    "arxiv_id": "2601.12345",
    "openalex_id": "W1234567890"
  },
  "urls": {
    "abstract": "https://arxiv.org/abs/2601.12345",
    "pdf": "https://arxiv.org/pdf/2601.12345"
  },
  "download_status": "success|pending|failed|unavailable",
  "local_path": "./papers/i0001.pdf",
  "citation_count": 42,
  "source": ["arxiv", "openalex"],
  "collected_at": "2026-01-17T10:00:00Z"
}
```

## Error Codes

| Code | Meaning | Retryable |
|------|---------|-----------|
| `PROJECT_NOT_FOUND` | Project directory doesn't exist | No |
| `NO_INPUT_FILES` | Required input files missing | No |
| `NO_ITEMS_FILE` | items.json not found | No |
| `INVALID_SOURCE` | Unknown data source | No |
| `NETWORK_ERROR` | API request failed | Yes |
| `RATE_LIMITED` | API rate limit hit | Yes |
| `DOWNLOAD_FAILED` | PDF download failed | Yes |
| `CONVERSION_FAILED` | PDF to Markdown conversion failed | Yes |
| `MISSING_DEPENDENCY` | Required package not installed | No |

## Agent Guidelines

**Execution Principles**:
- First run: Run bootstrap script to auto-setup environment
- CLI Commands (init, search, download, analyze, index): Run in sequence, no confirmation needed
- Agent intervention ONLY needed during Phase 2 (Review) and Manual Analysis (if no LLM)

**Specific Guidelines**:
1. **Environment Setup**: Run `bash .codex/skills/insight-pilot/scripts/bootstrap_env.sh` first
2. **Use `--json` flag**: Get structured output for parsing
3. **Execute CLI directly**: Do not ask for confirmation, follow workflow sequence
4. **Review**: Modify `status` and `exclude_reason` in `items.json`
5. **LLM Analysis First**: Use `analyze` command if configured, otherwise manually create `analysis/{id}.json`
6. **Incremental Updates**: Only process new papers, keep existing analysis results
