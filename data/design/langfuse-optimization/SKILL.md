---
name: langfuse-optimization
description: Analyzes writing-ecosystem traces to fix style.yaml, template.yaml, and tools.yaml based on quality issues found in production runs.
allowed-tools: "*"
---

# Writing Ecosystem Config Optimizer

Analyzes Langfuse traces to identify what's wrong with your **style.yaml**, **template.yaml**, and **tools.yaml** files, then tells you exactly how to fix them.

## When to Use This Skill

- "Analyze traces and fix my config files"
- "My checks are failing - what's wrong with style.yaml?"
- "Optimize case 0001 configuration"
- "Why is the research node selecting wrong tools?"

## Required Environment Variables

- `LANGFUSE_PUBLIC_KEY`: Your Langfuse public API key
- `LANGFUSE_SECRET_KEY`: Your Langfuse secret API key
- `LANGFUSE_HOST`: Langfuse host URL (default: https://cloud.langfuse.com)

## What This Skill Does

**Input**: User request + case ID
**Output**: Specific fixes for style.yaml, template.yaml, tools.yaml

**3-Step Process**:
1. **Retrieve traces** from Langfuse for specified case
2. **Extract problems** from trace data (check failures, tool errors, structure issues)
3. **Generate fixes** with exact YAML changes to make

## Workflow

### Step 1: Get User Request & Case ID

Ask for:
- **Case ID** (e.g., "0001", "0002", "The Prep")
- **Time range** (default: last 7 days)
- **Specific focus** (optional: "just style checks", "just tools", "everything")

### Step 2: Retrieve Trace Data

#### Option A: Unified Retrieval (Recommended - Simpler)

Use the unified helper to get traces and observations in one command:

```bash
cd /home/runner/workspace/.claude/skills/langfuse-optimization

# Get last 5 traces with observations for a case (using tags - RECOMMENDED)
python3 helpers/retrieve_traces_and_observations.py \
  --limit 5 \
  --tags "case:0001" \
  --output /tmp/langfuse_analysis/bundle.json

# Filter by metadata (e.g., specific case_id)
python3 helpers/retrieve_traces_and_observations.py \
  --limit 3 \
  --metadata case_id=0001 \
  --output /tmp/langfuse_analysis/case_0001_bundle.json

# Get traces only (skip observations for faster retrieval)
python3 helpers/retrieve_traces_and_observations.py \
  --limit 10 \
  --no-observations \
  --output /tmp/langfuse_analysis/traces_only.json

# Save separate files + unified bundle
python3 helpers/retrieve_traces_and_observations.py \
  --limit 5 \
  --output /tmp/langfuse_analysis/bundle.json \
  --traces-output /tmp/langfuse_analysis/traces.json \
  --observations-output /tmp/langfuse_analysis/observations.json

# **RECOMMENDED**: Strip bloat for 95% size reduction
python3 helpers/retrieve_traces_and_observations.py \
  --tags "case:0001" \
  --limit 1 \
  --filter-essential \
  --output /tmp/langfuse_analysis/filtered_bundle.json
```

**Output**: Single JSON bundle with:
- Query parameters (for reproducibility)
- Traces list
- Observations grouped by trace_id
- Trace count and IDs

**Size Optimization Flags**:

**`--filter-essential`** (Config Optimization):
- Strips: `facts_pack` (391KB+), `validation_report` (45KB+), long text fields
- Replaces with compact summaries (facts count, size, failed checks)
- **Reduction**: ~95% (4.2MB → 200KB)
- **Use case**: Analyzing style.yaml, template.yaml, tools.yaml

**`--filter-research-details`** (Additional Reduction):
- Strips: `structured_citations` (34KB → 700B), `step_status` (8KB → 200B)
- Replaces with counts, domains, tools used, success/failure stats
- **Reduction**: ~70% additional (on top of essential)
- **Use case**: When citation URLs and detailed step logs not needed

**`--filter-all`** (Maximum Reduction):
- Convenience flag: enables both `--filter-essential` + `--filter-research-details`
- **Total reduction**: ~96% (4.2MB → 30KB per trace)
- **Use case**: Large-scale trace collection, config optimization

**Comparison**:
- Without filtering: 4.2MB per trace (slow, all raw data)
- With `--filter-essential`: 200KB per trace (fast, config analysis)
- With `--filter-all`: 30KB per trace (fastest, minimal size)

#### Option A.1: Single Trace Retrieval (Fastest for Individual Analysis)

When you know the exact trace ID you want to analyze, use the single trace helper:

```bash
cd /home/runner/workspace/.claude/skills/langfuse-optimization

# Essential filtering only (95% reduction)
python3 helpers/retrieve_single_trace.py 8fda46d7ac626327396d1a7962690807 --filter-essential

# Maximum filtering (96% reduction) - RECOMMENDED for most cases
python3 helpers/retrieve_single_trace.py 8fda46d7ac626327396d1a7962690807 --filter-all

# Essential + Research details (custom combination)
python3 helpers/retrieve_single_trace.py 8fda46d7ac626327396d1a7962690807 \
  --filter-essential --filter-research-details \
  --output /tmp/langfuse_analysis/single_trace.json

# Without filtering (keep all raw data)
python3 helpers/retrieve_single_trace.py abc123 --output /tmp/langfuse_analysis/trace.json
```

**Benefits over multi-trace retrieval:**
- **10-20x faster**: Only fetches one trace instead of all traces for a case
- **Lower API usage**: Fewer API calls, less rate limiting
- **Cleaner workflow**: No need for client-side extraction
- **Same structure**: Output is identical to `retrieve_traces_and_observations.py`

**Output**: Same bundle structure as Option A (compatible with all analysis tools)

**When to use:**
- Analyzing a specific trace ID from Langfuse dashboard
- Deep-diving into one workflow run
- Following up on a specific error or issue
- Comparing before/after changes to config

#### Option B: Two-Step Retrieval (Advanced - More Control)

For scenarios where you need separate retrieval stages:

```bash
cd /home/runner/workspace/.claude/skills/langfuse-optimization

# Step 1: Get traces for a specific case (using tags)
python3 helpers/retrieve_traces.py \
  --tags "case:0001" \
  --days 7 \
  --limit 10 \
  --output /tmp/langfuse_analysis/traces.json

# Step 2: Get observations for those traces
python3 helpers/retrieve_observations.py \
  --trace-ids-file /tmp/langfuse_analysis/traces.json \
  --output /tmp/langfuse_analysis/observations.json

# Step 2 (with filtering): Strip bloat for 95% size reduction
python3 helpers/retrieve_observations.py \
  --trace-ids-file /tmp/langfuse_analysis/traces.json \
  --filter-essential \
  --output /tmp/langfuse_analysis/filtered_observations.json
```

### Step 2B: Retrieve Annotation Queue Data (Optional)

If you have human annotations/feedback in Langfuse annotation queues:

```bash
cd /home/runner/workspace/.claude/skills/langfuse-optimization

# Get all annotated items from a queue
python3 helpers/retrieve_annotations.py \
  --queue-id <your_queue_id> \
  --output /tmp/langfuse_analysis/annotations.json

# Get only completed annotations (reviewed items)
python3 helpers/retrieve_annotations.py \
  --queue-id <your_queue_id> \
  --status completed \
  --output /tmp/langfuse_analysis/annotations.json

# Limit to recent 100 items
python3 helpers/retrieve_annotations.py \
  --queue-id <your_queue_id> \
  --limit 100
```

**What you get**:
- Human comments/notes on traces
- Manual scores assigned by reviewers
- Issues flagged during quality review
- Trace IDs linked to annotations

**How to use in analysis**:
- Cross-reference annotation comments with trace data
- Identify patterns in human-flagged issues
- Prioritize fixes based on manual feedback frequency
- Validate if automated checks catch the same issues humans flag

### Step 2.5: Using Metadata Filters

Filter traces by metadata fields to focus analysis on specific subsets:

```bash
cd /home/runner/workspace/.claude/skills/langfuse-optimization

# Single metadata filter - analyze specific case
python3 helpers/retrieve_traces_and_observations.py \
  --metadata case_id=0001 \
  --limit 10 \
  --output /tmp/langfuse_analysis/case_0001.json

# Multiple filters (AND logic - trace must match ALL)
python3 helpers/retrieve_traces_and_observations.py \
  --metadata case_id=0001 profile_name="Stock Deep Dive" \
  --limit 5 \
  --output /tmp/langfuse_analysis/filtered.json

# Use dot notation for nested metadata (if applicable)
python3 helpers/retrieve_traces_and_observations.py \
  --metadata workflow_version=1 \
  --output /tmp/langfuse_analysis/v1_workflows.json
```

**How it works**:
- Retrieves all traces from Langfuse within time range
- Applies client-side filtering by metadata fields
- Returns only traces matching ALL specified filters
- Limit applied AFTER filtering (ensures you get requested number of matching traces)

**Common Use Cases**:
- **Analyze specific case**: `--metadata case_id=0001`
- **Compare workflow versions**: `--metadata workflow_version=1` vs `--metadata workflow_version=2`
- **Profile-specific issues**: `--metadata profile_name="The Prep"`
- **Combine filters**: `--metadata case_id=0001 workflow_version=2` (both must match)

**Tips**:
- Metadata values are case-sensitive strings
- Use exact matches only (no wildcards/regex)
- Check available metadata: run without filter first, inspect trace metadata
- Common fields: `case_id`, `profile_name`, `workflow_version`

### Step 3: Extract Problems from Traces

Read `/tmp/langfuse_analysis/bundle.json` (or `observations.json` if using two-step retrieval) and extract:

#### A. Style Check Failures (for style.yaml)

From **edit node** observations, find:
- Which checks failed
- Failure rates (how often each check fails)
- Scores vs thresholds
- Example content that failed

**Map to style.yaml issues**:
- **Vague rubric**: Check description unclear, LLM can't grade consistently
- **Wrong threshold**: Check fails too often (>30%) or never fails
- **Missing check**: Quality issue exists but no check catches it
- **Wrong weight**: Check importance (MINOR/MAJOR/CRITICAL) doesn't match impact

#### B. Template Problems (for template.yaml)

From **write node** observations, find:
- Missing required sections
- Word count violations
- Structure mismatches (bullets vs narrative)

**Map to template.yaml issues**:
- Unclear section descriptions
- Unrealistic word limits
- Missing section definitions

#### C. Tool Selection Issues (for tools.yaml)

From **research node** observations, find:
- Which tools were selected
- Tool failures (API errors, timeouts)
- Wrong tool for topic (should have used X but used Y)
- Loop expansion failures (`for_each` errors)

**Map to tools.yaml issues**:
- Tool not available in pattern
- Wrong research pattern selected
- Loop directive path incorrect
- Missing fallback configuration

### Step 4: Generate Config Fixes

For each problem, create a recommendation:

```markdown
## Fix #N: [Problem description]

**File**: `writing_ecosystem/config/cases/XXXX/[style|template|tools].yaml`

**Problem**:
- [Specific issue found in traces]
- [Evidence: X failures in Y traces]

**Current Config**:
```yaml
[Show current YAML]
```

**Fixed Config**:
```yaml
[Show corrected YAML with inline comments explaining changes]
```

**Why this fixes it**:
- [Explanation of root cause]
- [Expected improvement]
```

### Step 5: Present Simple Report

```markdown
# Config Optimization Report - Case XXXX

**Traces Analyzed**: X traces from [date range]

---

## Problems Found

### style.yaml Issues
1. ❌ `tone_consistency` check failing 30% (vague rubric)
2. ❌ `ttr_constraint` threshold too strict (16% failures)
3. ⚠️ `formality` check never fails (threshold too loose)

### template.yaml Issues
1. ❌ "Context" section missing description
2. ❌ Word limit conflict: max 100 words but needs 5 bullets

### tools.yaml Issues
1. ❌ Research pattern missing `finnhub` for financial topics
2. ❌ Loop directive path wrong: `user.portfolio.symbols` (should be `user.portfolio.summary.symbols`)

---

## Recommended Fixes

### Fix #1: Improve tone_consistency Rubric (style.yaml)

**Problem**: Failing 30% of traces - rubric too vague

**Current**:
```yaml
signatures:
  tone_consistency:
    rubric: "Assess whether tone is consistent. Score 1-10."
    threshold: 7.0
```

**Fixed**:
```yaml
signatures:
  tone_consistency:
    rubric: |
      Check tone consistency across:
      1. FORMALITY: Professional terms only (not "pretty big", "kinda")
      2. OBJECTIVITY: Neutral facts (not "shocked markets")
      3. EXPERTISE: Assumes financial literacy

      Score 9-10: Perfect consistency
      Score 7-8: 1-2 minor lapses
      Score 5-6: Noticeable shifts
      Score <5: Multiple violations
    threshold: 7.0
```

**Why**: Specific dimensions + examples → LLM can grade consistently

---

### Fix #2: Lower TTR Threshold (style.yaml)

**Problem**: Failing 16% - too strict for financial jargon

**Current**:
```yaml
constraints:
  ttr_constraint:
    threshold: 0.55
```

**Fixed**:
```yaml
constraints:
  ttr_constraint:
    threshold: 0.50  # Financial terms naturally repeat
```

**Why**: Domain terminology (Fed, QE, yield curve) lowers lexical diversity

---

### Fix #3: Add Finnhub to Research Pattern (tools.yaml)

**Problem**: Financial topics not getting market data

**Current**:
```yaml
research_patterns:
  default: general_research
  patterns:
    general_research:
      steps:
        - tool: perplexity
```

**Fixed**:
```yaml
research_patterns:
  default: financial_research  # Changed default for case 0001
  patterns:
    financial_research:
      steps:
        - tool: perplexity
          save_as: news
        - tool: finnhub  # Added for market data
          input:
            endpoint: company_news
            symbol: "{{topic}}"  # Extract symbol from topic
          save_as: market_data
```

**Why**: Financial topics need both news (perplexity) + data (finnhub)

---

## Implementation

**1. Backup configs**:
```bash
cd writing_ecosystem/config/cases/0001
cp style.yaml style.yaml.backup
cp template.yaml template.yaml.backup
cp tools.yaml tools.yaml.backup
```

**2. Apply fixes**:
- Open each file in editor
- Apply changes from recommendations above
- Save files

**3. Test**:
```bash
python run_workflow.py --case 0001 --topic "Test topic"
# Check Langfuse trace for improvements
```

**4. Monitor**:
- Run 20-30 workflows
- Re-run this analysis
- Compare before/after failure rates

---

## Expected Results

- `tone_consistency` failures: 30% → ~15%
- `ttr_constraint` failures: 16% → ~8%
- Research quality: +20% (adding finnhub)
- Overall pre-flight score: 7.8 → 8.2

---

**Ready to implement?**
Let me know which fixes to apply first, or if you want to see more detail on any issue.
```

## Analysis Patterns

### For style.yaml Issues

**Look for**:
1. **High failure rate** (>30%) → Vague rubric or wrong threshold
2. **Zero failures** → Threshold too loose or check not working
3. **Inconsistent scores** → Rubric needs examples and clear criteria
4. **Low edit fix rate** (<50%) → Check unclear about what to fix

**Common fixes**:
- Add specific dimensions to rubrics
- Provide good/bad examples
- Adjust thresholds based on domain (finance vs tech vs general)
- Add deterministic pre-checks for obvious violations

### For template.yaml Issues

**Look for**:
1. **Missing sections** in write node output
2. **Word count violations** (consistent over/under)
3. **Structure mismatches** (bullets vs narrative)

**Common fixes**:
- Add clear section descriptions
- Adjust word limits to realistic values
- Clarify format requirements (when to use bullets vs prose)

### For tools.yaml Issues

**Look for**:
1. **Wrong tool selected** for topic type
2. **Missing tools** for domain (finance needs finnhub)
3. **Loop expansion failures** (path errors in `for_each`)
4. **Tool errors** (API failures, timeouts)

**Common fixes**:
- Add domain-specific tools to patterns
- Fix loop directive paths
- Add fallback patterns
- Update default pattern for case

## Key Principles

### 1. Evidence-Based
Every recommendation must show:
- How many traces failed
- Example content that failed
- Why current config caused the failure

### 2. Specific
No generic advice like "improve rubric" - show EXACT YAML changes with inline comments

### 3. Prioritized
Focus on:
- High-frequency issues first (affects >30% of traces)
- Quick wins (threshold adjustments)
- High-impact changes (missing tools for domain)

### 4. Actionable
Every fix includes:
- Exact file path
- Before/after YAML
- Expected improvement
- How to test

## Troubleshooting

**"No traces found"**:
- Verify case ID is correct
- Check trace naming: `writing-workflow-0001` vs `writing-workflow-001`
- Try broader: `--name "writing-workflow"` to see all cases

**"No check failures in traces"**:
- Workflow may be in fallback mode (no LLM)
- Edit node may have been skipped (pre-flight score >8.5)
- Verify edit node ran in observations

**"Can't identify issue"**:
- Read the actual style.yaml/template.yaml/tools.yaml files
- Compare trace output to config requirements
- Look for mismatches

**"Metadata filter returning no traces"**:
- Verify metadata fields exist in your traces (check raw trace JSON)
- Metadata values are case-sensitive strings
- Use exact matches only (no wildcards/regex)
- Try without metadata filter first to see available metadata fields
- Common fields: `case_id`, `profile_name`, `workflow_version`

## Success Criteria

Good recommendations should:
1. ✅ Show exact YAML before/after
2. ✅ Explain WHY issue occurred (root cause)
3. ✅ Quantify impact (X% failure rate → Y% expected)
4. ✅ Be implementable in <5 min per fix
5. ✅ Focus on top 3-5 issues (not 50 minor ones)

---

**Remember**: This skill is about **fixing config files**, not analyzing architecture. Keep it simple:
1. What's broken in the YAML?
2. Here's the fix
3. Here's why it works
