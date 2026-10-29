---
name: job-search
description: Search for jobs across multiple boards and company career pages. Use when looking for new positions to apply to.
---

# Job Search Skill

Search for jobs programmatically across Indeed, LinkedIn, Glassdoor, Google, ZipRecruiter, and directly via Greenhouse API.

## Quick Start

When user asks to search for jobs, use the Python scripts in `toolkit/scripts/`:

### Bulk Search (Multiple Boards)

```bash
python toolkit/scripts/job_search.py "ML engineer" --location "San Francisco, CA" --min-salary 200000 --hours 72
```

### Company-Specific Search (Greenhouse)

```bash
python greenhouse_search.py anthropic openai stripe --keyword "engineer" --min-salary 200000
```

## Available Scripts

### 1. `job_search.py` - Multi-board aggregator

Uses JobSpy library to search:
- Indeed
- LinkedIn
- Glassdoor
- Google Jobs
- ZipRecruiter

**Parameters:**
- `search_term` - Job title or keywords
- `--location` - City, State
- `--remote` - Remote jobs only
- `--min-salary` - Filter by minimum salary
- `--hours` - Posted within N hours (default: 72)
- `--results` - Results per site (default: 25)
- `--output` - Save to file

**Example:**
```bash
python job_search.py "software engineer" -l "New York, NY" -s 180000 -r --hours 48
```

### 2. `greenhouse_search.py` - Direct company search

Queries Greenhouse Job Board API (no auth needed for public listings).

**Known companies:** anthropic, openai, deepmind, stripe, databricks, insitro, biohub, czi, and more.

**Parameters:**
- `companies` - One or more company names
- `--keyword` - Filter by keyword in title/description
- `--min-salary` - Minimum salary (extracted from descriptions)
- `--location` - Location filter
- `--list-known` - Show all known board tokens

**Example:**
```bash
python greenhouse_search.py anthropic stripe openai --keyword "senior" --min-salary 250000
```

## Installation

If scripts fail with import errors:
```bash
pip install python-jobspy pandas requests
```

## Workflow

1. **Bulk discovery**: Use `job_search.py` to find positions across boards
2. **Targeted search**: Use `greenhouse_search.py` for specific target companies
3. **Review results**: Jobs are saved to JSON/CSV for review
4. **Apply**: Use `/apply <url>` skill to start application process

## Output Format

Both scripts output:
- Console summary with job details
- JSON file with full data
- CSV file for spreadsheet review

## Notes

- Job boards may rate-limit or block aggressive scraping
- Greenhouse API is public and reliable
- Salary extraction from descriptions is best-effort
- Always verify job details on actual posting
