---
name: strategy-builder
description: Analyzes research queries to determine if new strategies are needed, optimizes existing strategies using Langfuse traces, and generates strategy templates
allowed-tools: "*"
---

# Strategy Builder & Optimizer

Intelligent assistant for building, optimizing, and analyzing research strategies. Takes any research query (in any language) and determines if a new strategy is needed, or helps optimize existing strategies based on production performance data from Langfuse.

## When to Use This Skill

- "Suche mir alle Informationen über gerichtsurteile an deutschen Gerichten"
- "Do I need a new strategy for legal case research?"
- "Analyze the performance of daily_news_briefing strategy"
- "Create a strategy for monitoring competitor product launches"
- "Why is financial_research strategy slow?"
- "Optimize the tool chain for company dossier research"

## What This Skill Does

**3 Core Functions**:

1. **Query Analysis → Strategy Recommendation**
   - Analyzes research query (any language)
   - Classifies: category, time_window, depth
   - Checks if existing strategy fits
   - Recommends new strategy if needed

2. **Strategy Performance Analysis**
   - Retrieves Langfuse traces for strategy
   - Analyzes success rates, latency, tool effectiveness
   - Identifies bottlenecks and errors
   - Suggests optimizations

3. **Strategy Generation**
   - Generates YAML template for new strategy
   - Validates structure against schema
   - Provides implementation guidance

## Required Environment Variables

- `LANGFUSE_PUBLIC_KEY`: Your Langfuse public API key
- `LANGFUSE_SECRET_KEY`: Your Langfuse secret API key
- `LANGFUSE_HOST`: Langfuse host URL (default: https://cloud.langfuse.com)

## Workflow

### Use Case 1: Analyze Research Query (Do I Need a New Strategy?)

**User provides research query** → **Skill determines if new strategy needed**

#### Step 1: Get User Query

Ask for:
- **Research query** (any language, any format)
- **Optional context**: frequency (daily/weekly), urgency, expected depth

**Examples**:
- "Suche mir alle Informationen über gerichtsurteile an deutschen Gerichten"
- "Monitor competitor Tesla product launches"
- "Daily briefing on AI regulation changes in EU"
- "Deep dive on quantum computing research papers"

#### Step 2: Analyze Query

Use the analysis helper to classify the query:

```bash
cd /home/user/web_research_agent/.claude/skills/strategy-builder/helpers

# Analyze research query
python3 analyze_research_query.py \
  --query "Suche mir alle Informationen über gerichtsurteile an deutschen Gerichten" \
  --output /tmp/strategy_analysis/query_analysis.json

# With optional context
python3 analyze_research_query.py \
  --query "Monitor Tesla product launches" \
  --frequency "weekly" \
  --depth "comprehensive" \
  --output /tmp/strategy_analysis/tesla_analysis.json
```

**Output**: JSON with:
```json
{
  "query": "Suche mir alle Informationen über gerichtsurteile an deutschen Gerichten",
  "classification": {
    "category": "legal",
    "time_window": "month",
    "depth": "comprehensive",
    "language": "de"
  },
  "required_variables": [
    {"name": "topic", "description": "Legal case or court topic"},
    {"name": "jurisdiction", "description": "German court jurisdiction"}
  ],
  "existing_match": null,
  "recommendation": "create_new_strategy",
  "reasoning": "No existing strategy covers legal/court case research. Existing categories: news, general, company, financial, finance, academic",
  "suggested_slug": "legal/court_cases_de",
  "suggested_tools": [
    "exa_search_semantic",
    "sonar_search",
    "llm_analyzer"
  ]
}
```

#### Step 3: Present Recommendation

Based on analysis output:

**If existing strategy matches**:
```markdown
## ✓ Existing Strategy Found

**Strategy**: `daily_news_briefing`
**Match Quality**: 95%
**Recommendation**: Use existing strategy

Your query matches:
- Category: news
- Time window: day
- Depth: deep

You can run:
```bash
python run_daily_briefing.py --topic "your topic"
```

**If no match**:
```markdown
## ⚠️ No Existing Strategy Found

**Recommendation**: Create new strategy

**Query Classification**:
- Category: legal
- Time window: month
- Depth: comprehensive
- Language: de

**Existing strategies** (news, general, company, financial, finance, academic) do not cover legal research.

**Next Step**: Generate new strategy template (see Use Case 3)
```

---

### Use Case 2: Analyze Strategy Performance (How is My Strategy Performing?)

**User provides strategy slug** → **Skill analyzes Langfuse traces** → **Performance report + optimization suggestions**

#### Step 1: Get Strategy Identifier

Ask for:
- **Strategy slug** (e.g., "daily_news_briefing", "financial_research")
- **Time range** (default: last 7 days)
- **Focus area** (optional: latency, errors, tool effectiveness, all)

#### Step 2: Retrieve Strategy Traces

Use Langfuse helpers to get traces for the strategy:

```bash
cd /home/user/web_research_agent/.claude/skills/strategy-builder/helpers

# Get traces for specific strategy (last 7 days, up to 50 traces)
python3 retrieve_strategy_traces.py \
  --strategy "daily_news_briefing" \
  --days 7 \
  --limit 50 \
  --filter-essential \
  --output /tmp/strategy_analysis/traces.json

# Custom date range
python3 retrieve_strategy_traces.py \
  --strategy "financial_research" \
  --start-date "2025-11-01" \
  --end-date "2025-11-08" \
  --limit 100 \
  --filter-all \
  --output /tmp/strategy_analysis/financial_traces.json

# Focus on errors only
python3 retrieve_strategy_traces.py \
  --strategy "company/dossier" \
  --days 30 \
  --errors-only \
  --output /tmp/strategy_analysis/errors.json
```

**Output**: JSON bundle with traces and observations for the strategy

#### Step 3: Analyze Performance

Analyze the retrieved traces:

```bash
cd /home/user/web_research_agent/.claude/skills/strategy-builder/helpers

# Comprehensive performance analysis
python3 analyze_strategy_performance.py \
  --traces /tmp/strategy_analysis/traces.json \
  --strategy "daily_news_briefing" \
  --output /tmp/strategy_analysis/performance_report.json

# Focus on specific aspect
python3 analyze_strategy_performance.py \
  --traces /tmp/strategy_analysis/traces.json \
  --strategy "financial_research" \
  --focus "tool_effectiveness" \
  --output /tmp/strategy_analysis/tool_analysis.json
```

**Output**: Performance report with:
- Success rate
- Average latency (overall and per phase)
- Tool effectiveness (which tools succeed/fail)
- Common errors
- Bottlenecks
- Optimization recommendations

#### Step 4: Generate Performance Report

Read the analysis output and present findings:

```markdown
# Strategy Performance Report: daily_news_briefing

**Analysis Period**: 2025-11-02 to 2025-11-09 (7 days)
**Traces Analyzed**: 47 executions

---

## Summary Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Success Rate | 89.4% (42/47) | ✓ Good |
| Avg Latency | 12.3s | ⚠️ Moderate |
| P95 Latency | 18.7s | ⚠️ High |
| Error Rate | 10.6% (5/47) | ⚠️ Needs attention |

---

## Performance Breakdown

### Phase Latencies
- **Scope**: 0.8s avg (✓ fast)
- **Fill**: 0.2s avg (✓ fast)
- **Research**: 9.1s avg (⚠️ bottleneck - 74% of total time)
- **Finalize**: 2.2s avg (✓ acceptable)

### Tool Effectiveness

**sonar_overview** (Step 1):
- Success: 47/47 (100%)
- Avg latency: 3.2s
- Status: ✓ Performing well

**exa_search_semantic** (Step 2):
- Success: 43/47 (91.5%)
- Avg latency: 4.1s
- Failures: 4 (timeout errors)
- Status: ⚠️ Occasional timeouts

**exa_answer** (Step 3):
- Success: 45/47 (95.7%)
- Avg latency: 1.8s
- Status: ✓ Reliable

**llm_analyzer** (Step 4):
- Success: 42/47 (89.4%)
- Avg latency: 2.2s
- Failures: 5 (context length exceeded)
- Status: ⚠️ Evidence overload

---

## Issues Found

### Issue #1: exa_search_semantic Timeouts (4 occurrences, 8.5%)
**Pattern**: Timeouts when query involves multiple entities
**Evidence**: Trace IDs: abc123, def456, ghi789, jkl012
**Root Cause**: Default timeout (5s) too short for complex semantic searches

**Recommended Fix**:
```yaml
# In strategies/daily_news_briefing.yaml
tool_chain:
  - name: exa_search_semantic
    params:
      num_results: 10
      use_autoprompt: true
      timeout: 8  # Increase from default 5s
```

### Issue #2: llm_analyzer Context Length (5 occurrences, 10.6%)
**Pattern**: Fails when total evidence > 15 items with long snippets
**Evidence**: All failures had 18-20 evidence items
**Root Cause**: `limits.max_results: 20` allows too much evidence for synthesis

**Recommended Fix**:
```yaml
# In strategies/daily_news_briefing.yaml
limits:
  max_results: 15  # Reduce from 20
  max_llm_queries: 2
```

---

## Optimization Recommendations

### Priority 1: Reduce Error Rate (Impact: High, Effort: Low)
1. Increase exa timeout from 5s → 8s
2. Reduce max_results from 20 → 15
**Expected improvement**: Error rate 10.6% → ~2%

### Priority 2: Improve Latency (Impact: Medium, Effort: Medium)
1. Add parallel execution for exa steps
2. Use `filter-essential` on evidence earlier
**Expected improvement**: Avg latency 12.3s → ~9s

### Priority 3: Add Caching (Impact: Medium, Effort: High)
1. Cache exa_search results for common queries
2. Implement evidence deduplication earlier
**Expected improvement**: 20% faster for repeat topics

---

## Next Steps

1. **Apply fixes**: Update strategy YAML with recommended changes
2. **Test**: Run 10-20 executions to validate improvements
3. **Monitor**: Re-run this analysis after 7 days
4. **Compare**: Measure before/after metrics

**Ready to apply fixes?** Let me know which optimizations to implement.
```

---

### Use Case 3: Generate New Strategy (Create Strategy from Scratch)

**User needs new strategy** → **Skill generates YAML template** → **Validation + guidance**

#### Step 1: Define Strategy Requirements

Based on query analysis (Use Case 1) or manual input, gather:
- **Slug**: e.g., "legal/court_cases_de"
- **Category**: legal, technical, regulatory, etc.
- **Time window**: day, week, month, year
- **Depth**: brief, overview, deep, comprehensive
- **Required variables**: topic, jurisdiction, etc.
- **Tool preferences**: exa, sonar, llm_analyzer, custom

#### Step 2: Generate Strategy Template

Use the generation helper:

```bash
cd /home/user/web_research_agent/.claude/skills/strategy-builder/helpers

# Generate from query analysis
python3 generate_strategy.py \
  --from-analysis /tmp/strategy_analysis/query_analysis.json \
  --output /tmp/strategy_analysis/new_strategy.yaml

# Generate from manual parameters
python3 generate_strategy.py \
  --slug "legal/court_cases_de" \
  --category "legal" \
  --time-window "month" \
  --depth "comprehensive" \
  --required-vars "topic,jurisdiction" \
  --tools "exa_search_semantic,sonar_search,llm_analyzer" \
  --output /tmp/strategy_analysis/legal_strategy.yaml
```

**Output**: Valid strategy YAML template

#### Step 3: Validate Strategy

Validate the generated strategy:

```bash
cd /home/user/web_research_agent/.claude/skills/strategy-builder/helpers

# Validate YAML structure
python3 validate_strategy.py \
  --strategy /tmp/strategy_analysis/new_strategy.yaml \
  --output /tmp/strategy_analysis/validation_report.json
```

**Output**: Validation report (passes/fails, suggestions)

#### Step 4: Present Strategy Template

Show the generated strategy to user:

```markdown
# New Strategy Template: legal/court_cases_de

## Generated Strategy YAML

```yaml
meta:
  slug: legal/court_cases_de
  version: 1
  category: legal
  time_window: month
  depth: comprehensive

queries:
  sonar: "{{topic}} {{jurisdiction}} Gerichtsurteil Rechtsprechung"
  exa_search: "{{topic}} Gericht {{jurisdiction}} Urteil"

tool_chain:
  # Step 1: Sonar search for recent legal news/cases
  - name: sonar_legal
    params:
      max_results: 10
      system_prompt: |
        Sie sind ein juristischer Recherche-Assistent. Fokus auf:
        - Gerichtsurteile und Rechtsprechung
        - Gesetzliche Grundlagen
        - Relevante Paragraphen und Artikel
        - Verfahrensnummern (Aktenzeichen)
      search_mode: "web"
      search_recency_filter: "month"
      # German legal domains
      search_domain_filter:
        - "bundesverfassungsgericht.de"
        - "bundesgerichtshof.de"
        - "bundesarbeitsgericht.de"
        - "juris.de"
        - "beck-online.de"
        - "gesetze-im-internet.de"
      temperature: 0.1
      max_tokens: 2000

  # Step 2: Semantic search with Exa
  - name: exa_search_semantic
    params:
      num_results: 15
      use_autoprompt: true
      type: neural
      start_published_date: "{{start_date}}"
      end_published_date: "{{end_date}}"
      include_domains:
        - "bundesverfassungsgericht.de"
        - "juris.de"
        - "beck-online.de"

  # Step 3: Get full content for top results
  - name: exa_contents
    params:
      num_results: 5
      text: true

  # Step 4: Synthesize findings
  - name: llm_analyzer
    phase: finalize
    params:
      system_prompt: |
        Erstellen Sie eine juristische Analyse mit folgenden Abschnitten:
        1. Zusammenfassung der Rechtslage
        2. Relevante Urteile und Entscheidungen
        3. Gesetzliche Grundlagen
        4. Praxishinweise
        5. Quellen
      temperature: 0.2
      max_tokens: 2500

limits:
  max_results: 20
  max_llm_queries: 2
```

## Implementation Steps

### 1. Add to Strategy Index

Edit `/home/user/web_research_agent/strategies/index.yaml`:

```yaml
strategies:
  # ... existing strategies ...

  - slug: legal/court_cases_de
    title: German Court Cases Research
    category: legal
    time_window: month
    depth: comprehensive
    description: Comprehensive research on German court rulings and legal precedents
    priority: 10
    fan_out: none
    required_variables:
      - name: topic
        description: Legal topic or case subject
      - name: jurisdiction
        description: German court jurisdiction (optional)
```

### 2. Save Strategy File

Save to `/home/user/web_research_agent/strategies/legal_court_cases_de.yaml`

### 3. Migrate to Database

```bash
cd /home/user/web_research_agent
python scripts/migrate_strategies.py --strategy legal_court_cases_de
```

### 4. Test Strategy

```bash
# Test the new strategy
python run_daily_briefing.py \
  --strategy "legal/court_cases_de" \
  --topic "Datenschutz DSGVO Verstoß" \
  --jurisdiction "Bundesverfassungsgericht"

# Check Langfuse for trace
```

### 5. Monitor & Optimize

After 20-30 executions, run performance analysis (Use Case 2) to optimize.

---

## Validation Passed ✓

- [x] YAML syntax valid
- [x] Required meta fields present
- [x] Tool chain structure correct
- [x] Variable interpolation {{topic}}, {{jurisdiction}} valid
- [x] Domain filters appropriate for legal research
- [x] German language prompts correct

**Ready to implement?** Let me know if you want to create the files.
```

---

## Helper Tools Reference

### 1. analyze_research_query.py

**Purpose**: Classify research query and check for existing strategy matches

**Usage**:
```bash
python3 analyze_research_query.py \
  --query "Your research query here" \
  [--frequency daily|weekly|monthly] \
  [--depth brief|overview|deep|comprehensive] \
  [--language en|de|es|fr] \
  --output /tmp/analysis.json
```

**Output Fields**:
- `classification`: category, time_window, depth, language
- `required_variables`: extracted variables
- `existing_match`: matched strategy slug (or null)
- `recommendation`: use_existing | create_new_strategy | modify_existing
- `suggested_slug`: proposed slug for new strategy
- `suggested_tools`: recommended tool chain

### 2. retrieve_strategy_traces.py

**Purpose**: Fetch Langfuse traces for specific strategy

**Usage**:
```bash
python3 retrieve_strategy_traces.py \
  --strategy "strategy_slug" \
  [--days 7] \
  [--start-date YYYY-MM-DD] \
  [--end-date YYYY-MM-DD] \
  [--limit 50] \
  [--filter-essential] \
  [--errors-only] \
  --output /tmp/traces.json
```

**Filters**:
- `--filter-essential`: Strip large fields (95% size reduction)
- `--filter-all`: Maximum compression (96% reduction)
- `--errors-only`: Only traces with errors

### 3. analyze_strategy_performance.py

**Purpose**: Analyze strategy performance from traces

**Usage**:
```bash
python3 analyze_strategy_performance.py \
  --traces /tmp/traces.json \
  --strategy "strategy_slug" \
  [--focus latency|errors|tools|all] \
  --output /tmp/performance.json
```

**Focus Areas**:
- `latency`: Phase and tool latency analysis
- `errors`: Error patterns and frequencies
- `tools`: Tool effectiveness and success rates
- `all`: Comprehensive analysis (default)

### 4. generate_strategy.py

**Purpose**: Generate new strategy YAML template

**Usage**:
```bash
# From analysis
python3 generate_strategy.py \
  --from-analysis /tmp/query_analysis.json \
  --output /tmp/new_strategy.yaml

# Manual parameters
python3 generate_strategy.py \
  --slug "category/name" \
  --category "category" \
  --time-window "day|week|month" \
  --depth "brief|overview|deep|comprehensive" \
  --required-vars "var1,var2,var3" \
  --tools "tool1,tool2,tool3" \
  --output /tmp/new_strategy.yaml
```

### 5. validate_strategy.py

**Purpose**: Validate strategy YAML against schema

**Usage**:
```bash
python3 validate_strategy.py \
  --strategy /tmp/strategy.yaml \
  [--strict] \
  --output /tmp/validation.json
```

**Checks**:
- YAML syntax
- Required fields (meta, tool_chain)
- Variable interpolation validity
- Tool parameter correctness
- Schema compliance

---

## Common Patterns

### Pattern 1: "Do I Need a New Strategy?" Workflow

```
1. User query → analyze_research_query.py
2. If existing_match: Recommend existing strategy
3. If no match: Generate new strategy → validate → implement
```

### Pattern 2: "Optimize Existing Strategy" Workflow

```
1. Strategy slug → retrieve_strategy_traces.py
2. Traces → analyze_strategy_performance.py
3. Performance report → optimization recommendations
4. Apply fixes → re-test → compare metrics
```

### Pattern 3: "Build Strategy from Scratch" Workflow

```
1. Requirements gathering
2. generate_strategy.py → YAML template
3. validate_strategy.py → validation report
4. Manual review + customization
5. Add to index → migrate to DB → test
```

---

## Tips & Best Practices

### 1. Start with Query Analysis
Always run `analyze_research_query.py` first - it may find an existing strategy that fits

### 2. Iterate on Strategy Design
Don't aim for perfection on first version. Generate → test → analyze → optimize

### 3. Use Performance Data
Base optimizations on actual trace data, not assumptions

### 4. Keep Tool Chains Simple
Start with 2-3 tools, add more only if needed based on performance analysis

### 5. Validate Early and Often
Run `validate_strategy.py` after any manual changes to strategy YAML

### 6. Monitor Post-Deploy
After deploying new strategy, monitor for 20-30 executions before considering it stable

### 7. Language-Specific Strategies
For non-English research, customize:
- Query templates (use native language)
- Domain filters (local sources)
- System prompts (native language instructions)

---

## Troubleshooting

**"No existing strategies found"**:
- Verify database is populated: `python scripts/migrate_main_strategies.py`
- Check strategy cache initialization in logs

**"Query analysis returns generic category"**:
- Provide more context with `--frequency` and `--depth` flags
- Add domain-specific keywords to query

**"Generated strategy fails validation"**:
- Check YAML syntax (indentation, quotes)
- Verify required fields: meta.slug, meta.version, tool_chain
- Ensure variable names match in queries and tool_chain

**"No traces found for strategy"**:
- Verify strategy slug is exact match
- Check if strategy has been executed (traces exist)
- Try broader time range: `--days 30`

**"Performance analysis shows no data"**:
- Ensure traces have observations (not just trace-level data)
- Use `--filter-essential` to include key fields
- Check if strategy completed successfully (not all errors)

---

## Success Criteria

Good strategy work should:
1. ✅ Start with query analysis (don't guess)
2. ✅ Use existing strategies when possible
3. ✅ Base decisions on Langfuse trace data
4. ✅ Validate all YAML before deployment
5. ✅ Monitor performance post-deployment
6. ✅ Iterate based on real usage patterns

---

**Remember**: This skill is about **data-driven strategy development**, not guessing. Always:
- Analyze queries systematically
- Use trace data for optimizations
- Validate before deploying
- Monitor after deploying
