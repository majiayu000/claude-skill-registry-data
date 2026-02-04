---
name: documentation-improvement-workflow
description: Systematically improve documentation quality from 7/10 → 9/10 using assessment checklists and transformation patterns. Use when documentation exists but lacks Quick Start, clear prerequisites, or working examples. Optimized for crypto/trading data projects.
---

# Documentation Improvement Workflow

## Overview

This skill provides a systematic 4-step workflow for transforming good-but-frustrating documentation (7/10) into exceptional documentation (9/10) that enables <60 second time-to-first-success. Uses structured assessment checklists and proven transformation patterns to identify gaps and apply targeted improvements.

**Core Pattern**: Assess → Prioritize → Transform → Validate

**Typical Improvements**:
- Add Quick Start section (copy-paste working example)
- Make prerequisites explicit with version numbers
- Replace placeholder content with real URLs/values
- Document 3-5 common troubleshooting errors
- Add table of contents for navigation

## When to Use This Skill

Use this skill when:

1. **Documentation exists but feels incomplete** - Technical information present but hard to use
2. **Time-to-first-success > 3 minutes** - Users spend too long getting started
3. **Examples require editing** - Placeholder URLs, unclear configuration
4. **Prerequisites unclear** - Users must infer versions or dependencies
5. **Common errors undocumented** - Users resort to GitHub Issues for basic problems

**Common Triggers**:
- User feedback: "Your docs are hard to follow"
- GitHub Issues with questions answered in docs (but hard to find)
- README.md rated 7-8/10 (good but improvable)
- New contributors take >10 minutes to run first example

**Not Applicable When**:
- Documentation doesn't exist (write from scratch instead)
- Documentation already exceptional (9-10/10)
- Project is internal-only (lower bar acceptable)

## Workflow

### Step 1: Assess Current Documentation Quality

Use the **5-dimension assessment framework** from `references/quality-assessment-checklist.md`:

| Dimension | Weight | Assessment Question |
|-----------|--------|---------------------|
| Time-to-First-Success | 30% | How long to achieve first successful result? |
| Prerequisites Clarity | 20% | Are all prerequisites explicitly documented? |
| Example Coverage | 25% | Do examples cover primary use cases with working code? |
| Navigation & Structure | 15% | Can users find information quickly? |
| Troubleshooting Coverage | 10% | Are common errors documented with solutions? |

**Action**: Score each dimension 1-10, calculate weighted average.

**Example Assessment**:
```markdown
## Documentation Quality Assessment

**Project**: binance-futures-availability
**Date**: 2025-11-17

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Time-to-First-Success | 5/10 | No Quick Start, must read full README |
| Prerequisites Clarity | 6/10 | Python/DuckDB mentioned but no versions |
| Example Coverage | 7/10 | Examples exist but require editing URLs |
| Navigation & Structure | 8/10 | Good headings, but no TOC |
| Troubleshooting Coverage | 4/10 | Link to TROUBLESHOOTING.md but sparse |

**Overall Score**: 6.2/10 (Good but improvable)
```

**Outcome**: Identifies which dimensions need improvement.

### Step 2: Prioritize Transformation Patterns

Based on assessment scores, select transformation patterns from `references/transformation-patterns.md`:

**Priority 1: Critical Gaps** (dimensions scoring <5/10)
- **Pattern 1**: Add Quick Start section (30 min, +2 pts)
- **Pattern 2**: Make Prerequisites explicit (15 min, +1.5 pts)
- **Pattern 4**: Add Troubleshooting section (60 min, +2 pts)

**Priority 2: High-Impact Improvements** (dimensions scoring 5-7/10)
- **Pattern 3**: Transform abstract examples to concrete (45 min, +2 pts)
- **Pattern 6**: Replace placeholder content (30 min, +1.5 pts)

**Priority 3: Polish** (dimensions scoring 7-8/10)
- **Pattern 5**: Add table of contents (20 min, +1 pt)
- **Pattern 7**: Add expected output (10 min/example, +0.5 pts)

**Action**: Select 3-4 highest-ROI patterns to achieve 9/10 target.

**Example Prioritization**:
```markdown
## Improvement Plan

**Target**: 6.2/10 → 9.0/10 (+2.8 points)

**Phase 1** (Critical, 2 hours):
1. Pattern 1: Add Quick Start with DuckDB query (30 min, +2 pts)
2. Pattern 2: Document prerequisites with versions (15 min, +1.5 pts)
3. Pattern 3: Replace placeholder URLs with jsDelivr (45 min, +2 pts)
4. Pattern 4: Add 5 common troubleshooting errors (30 min, +1 pts)

**Expected Result**: 9.0/10

**Phase 2** (Optional polish, 30 min):
5. Pattern 5: Add table of contents (20 min, +0.5 pts)
6. Pattern 7: Add expected output to examples (10 min, +0.5 pts)

**Total Effort**: 2.5 hours
```

### Step 3: Apply Transformation Patterns

Systematically apply selected patterns using templates from `references/transformation-patterns.md`.

#### Pattern 1: Add Quick Start (Most Important)

**Before** (no Quick Start):
```markdown
# My Project

This project provides tools for analyzing crypto data.

## Installation
...
```

**After** (with Quick Start):
```markdown
# My Project

Query remote Parquet files without downloading using DuckDB.

## Quick Start

Prerequisites: Python 3.8+, install with: `pip install duckdb myproject`

python
import duckdb

# Query remote data (no download required)
conn = duckdb.connect(":memory:")
conn.execute("INSTALL httpfs; LOAD httpfs")

result = conn.execute("""
    SELECT date, symbol, price
    FROM read_parquet('https://cdn.jsdelivr.net/gh/org/repo@v1.0.0/data.parquet')
    WHERE symbol = 'BTCUSDT'
    LIMIT 5
""").fetchall()

print(result)  # Expected: [(2024-01-01, BTCUSDT, 42000), ...]


See [Full Documentation](#installation) for advanced usage.

---

## Installation
...
```

**Impact**: Time-to-first-success: 5 min → 60 sec

#### Pattern 2: Make Prerequisites Explicit

**Before** (unclear):
```markdown
## Installation
pip install myproject
```

**After** (explicit):
```markdown
## Prerequisites

### Required
- **Python**: 3.8 or later ([download](https://www.python.org/downloads/))
- **DuckDB**: 1.0.0+ (installed automatically via pip)

### Verification
bash
python --version  # Should be 3.8+
python -c "import duckdb; print(duckdb.__version__)"  # Should be 1.0.0+


## Installation
bash
pip install myproject

```

**Impact**: Prerequisites clarity: 6/10 → 9/10

#### Pattern 3: Concrete Examples (Not Placeholders)

**Before** (abstract):
```python
result = query_data(url, filters)
```

**After** (concrete):
```python
result = conn.execute("""
    SELECT date, symbol, volume
    FROM read_parquet('https://cdn.jsdelivr.net/gh/org/repo@v1.0.0/data.parquet')
    WHERE symbol = 'BTCUSDT'
      AND date >= '2024-01-01'
""").fetchall()
```

**Impact**: Example coverage: 7/10 → 9/10

#### Pattern 4: Add Troubleshooting Section

**Before** (no troubleshooting):
```markdown
For issues, see GitHub Issues.
```

**After** (5 common errors):
```markdown
## Troubleshooting

### Issue: "DuckDB cannot find httpfs extension"

**Symptom**: Error: Extension "httpfs" not found

**Solution**:
python
conn.execute("INSTALL httpfs FROM 'https://extensions.duckdb.org'")
conn.execute("LOAD httpfs")


---

### Issue: Query downloads full file (not using range requests)

**Symptom**: Query takes 30+ seconds for small result

**Diagnosis**:
bash
curl -I https://your-url/data.parquet | grep "Accept-Ranges"
# Should see: Accept-Ranges: bytes


**Solution**: Use jsDelivr CDN proxy:
python
good_url = "https://cdn.jsdelivr.net/gh/org/repo@v1.0.0/data.parquet"
result = conn.execute(f"SELECT * FROM read_parquet('{good_url}')").fetchall()


[... 3 more common errors ...]
```

**Impact**: Troubleshooting coverage: 4/10 → 8/10

### Step 4: Validate Improvement

After applying transformations, validate with external developer:

**Validation Checklist**:
- ✅ Time-to-first-success <60 seconds? (run Quick Start)
- ✅ Prerequisites clear? (can install without trial-and-error)
- ✅ Examples copy-paste ready? (no placeholder editing required)
- ✅ Common errors documented? (check 3 most recent GitHub Issues)
- ✅ Re-score documentation (should be 9-10/10)

**Re-Assessment**:
```markdown
## Post-Improvement Assessment

| Dimension | Before | After | Delta |
|-----------|--------|-------|-------|
| Time-to-First-Success | 5/10 | 9/10 | +4 |
| Prerequisites Clarity | 6/10 | 9/10 | +3 |
| Example Coverage | 7/10 | 9/10 | +2 |
| Navigation & Structure | 8/10 | 9/10 | +1 |
| Troubleshooting Coverage | 4/10 | 8/10 | +4 |

**Overall**: 6.2/10 → 9.0/10 (+2.8 points)
**Effort**: 2.5 hours
**Validation**: External developer completed Quick Start in 45 seconds ✅
```

## Using Bundled Resources

### `references/quality-assessment-checklist.md`

Comprehensive assessment framework with:
- **10-point rating scale** with descriptions for each level
- **5 assessment dimensions** with weights and scoring criteria
- **Scoring matrix** for calculating overall documentation quality
- **Improvement priority framework** (Critical Gaps → Polish)
- **Assessment worksheet** template for structured evaluation
- **Real-world example** from binance-futures-availability project

**Usage**:
1. Score each dimension (1-10)
2. Calculate weighted average
3. Identify dimensions <7/10
4. Select priority improvements

### `references/transformation-patterns.md`

7 concrete before/after patterns with:
- **Pattern 1**: Add Quick Start section (30 min, +2 pts)
- **Pattern 2**: Make prerequisites explicit (15 min, +1.5 pts)
- **Pattern 3**: Transform abstract examples to concrete (45 min, +2 pts)
- **Pattern 4**: Add troubleshooting section (60 min, +2 pts)
- **Pattern 5**: Add table of contents (20 min, +1 pt)
- **Pattern 6**: Replace placeholder content (30 min, +1.5 pts)
- **Pattern 7**: Add expected output (10 min/example, +0.5 pts)

Each pattern includes:
- Before/after examples
- Effort estimate
- Impact assessment (points gained)
- Specific improvements made

**Usage**: Select 3-4 patterns based on assessment gaps, apply templates.

## Domain Context: Crypto/Trading Data Documentation

This skill is optimized for technical documentation in crypto/trading domains:

**Typical Projects**:
- Historical OHLCV data repositories
- Trade tick databases
- Orderbook snapshot collections
- Market data APIs
- Data availability tracking systems

**Common Documentation Gaps**:
- **Missing Quick Start**: Users don't know how to query Parquet/CSV data
- **Unclear data sources**: Binance Vision, Coinbase Pro, Kraken, etc.
- **Schema undocumented**: Column names, types, nullable fields
- **Performance tips missing**: How to filter by symbol/date efficiently
- **No troubleshooting**: S3 access errors, rate limits, corrupt files

**Domain-Specific Patterns**:
- Always include symbol filtering examples (BTCUSDT, ETHUSDT)
- Document date ranges explicitly (2019-09-25 to present)
- Show aggregation patterns (daily volume, OHLC rollups)
- Include bandwidth optimization tips (column pruning, predicate pushdown)
- Document data completeness (which symbols have full history)

## Tips for Success

1. **Start with Quick Start** - Highest ROI transformation (30 min, +2 pts)
2. **Use real URLs** - jsDelivr CDN for GitHub Releases, actual API endpoints
3. **Make examples copy-paste ready** - Zero placeholder editing required
4. **Validate with external developer** - Confirm <60s time-to-first-success
5. **Document actual errors** - Pull from GitHub Issues, not hypothetical
6. **Show expected output** - Users can verify correctness
7. **Focus on 80/20** - Top 3-4 patterns achieve most improvement

## Common Pitfalls to Avoid

1. **Overengineering** - Don't aim for 10/10, 9/10 is sufficient
2. **Placeholder content** - "YOUR_URL_HERE" frustrates users
3. **Abstract examples** - Users can't run generic code
4. **Missing expected output** - Can't verify correctness
5. **No validation** - Assume improvements work without testing
6. **Ignoring common errors** - GitHub Issues reveal actual problems
7. **Buried Quick Start** - Must be at top of README, not hidden

## Real-World Example: ADR-0014 Transformation

### Initial State
**README.md**: 7.5/10 (good but improvable)
- Technical information comprehensive
- Examples exist but require URL editing
- Prerequisites implied but not explicit
- No Quick Start section

### Assessment
| Dimension | Score | Gap |
|-----------|-------|-----|
| Time-to-First-Success | 5/10 | No Quick Start |
| Prerequisites Clarity | 6/10 | Versions unclear |
| Example Coverage | 7/10 | Placeholder URLs |
| Navigation & Structure | 8/10 | No TOC |
| Troubleshooting Coverage | 4/10 | Sparse |

### Transformation Plan
**Phase 1** (2.5 hours):
1. ✅ Add Quick Start with DuckDB httpfs query (Pattern 1)
2. ✅ Document Python 3.8+, DuckDB 1.0.0+ prerequisites (Pattern 2)
3. ✅ Replace placeholder URLs with jsDelivr CDN (Pattern 3)
4. ✅ Add 5 common troubleshooting errors (Pattern 4)
5. ✅ Add table of contents (Pattern 5)

### Validation
- External developer completed Quick Start in 45 seconds ✅
- Zero placeholder editing required ✅
- Re-score: **9.5/10** (+2.0 points) ✅

### Key Success Factors
- Focused on highest-ROI patterns first (Quick Start, Prerequisites, Examples)
- Used real jsDelivr URLs (not "example.com" placeholders)
- Documented actual GitHub Issues errors (not hypothetical)
- Validated with external developer before finalizing
