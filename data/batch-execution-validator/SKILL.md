---
name: batch-execution-validator
description: Validate production batch execution - trigger daily runs and analyze traces for architecture completeness and result quality
allowed-tools: "*"
---

# Batch Execution Validator Skill

## Purpose

End-to-end validation of production batch execution pipeline:
1. Trigger batch execution for daily frequency via production API
2. Wait for execution to complete
3. Retrieve execution traces from Langfuse using advanced filters
4. Analyze traces for architecture completeness and result quality
5. Report findings with actionable recommendations

## When to Use

- "Run a batch execution test for daily frequency"
- "Validate the production pipeline is working correctly"
- "Check if Langfuse tracing captures all nodes"
- "Test batch execution and analyze results"
- "Verify daily batch runs are generating quality output"

## Required Environment Variables

- `API_SECRET_KEY`: Production API secret key
- `LANGFUSE_PUBLIC_KEY`: Langfuse public API key
- `LANGFUSE_SECRET_KEY`: Langfuse secret API key
- `LANGFUSE_HOST`: Langfuse host URL (default: https://cloud.langfuse.com)

## Workflow

### Step 1: Trigger Batch Execution

Use the api_client.py helper to trigger a batch execution for daily frequency:

```bash
cd .claude/skills/batch-execution-validator/helpers

# Trigger batch execution
python3 api_client.py \
  --api-url https://your-api.com \
  --frequency daily \
  --wait 180

# Output:
# - Batch execution triggered
# - Number of tasks found
# - Started timestamp
# - Task IDs (for trace retrieval)
```

**What it does:**
- POSTs to `/execute/batch` with frequency="daily"
- Extracts task IDs that will be processed
- Waits specified time (default 180s = 3min) for completion
- Returns execution metadata

### Step 2: Retrieve and Analyze Traces

Use the trace_fetcher.py helper to query Langfuse and analyze results:

```bash
# Retrieve traces for the batch execution
python3 trace_fetcher.py \
  --from-timestamp "2025-11-07T14:30:00Z" \
  --tags batch_execution daily \
  --session-ids "task-id-1,task-id-2,task-id-3" \
  --output /tmp/batch_validation_results.json

# Output:
# - Full trace data with nested observations
# - Architecture analysis (node coverage, hierarchy)
# - Quality assessment (sections, citations, performance)
# - Issues and warnings
```

**What it does:**
- Queries Langfuse with advanced filters:
  - `tags`: ["batch_execution", "daily"]
  - `timestamp >= started_at`
  - `session_id in [task_ids]`
- Fetches full trace details + all child observations
- Analyzes trace architecture:
  - Node coverage (router, research, write, edit)
  - Hierarchy validation (parent-child relationships)
  - Metadata completeness
  - Error detection
- Assesses result quality:
  - Output structure (sections, citations)
  - Content completeness
  - Performance metrics (latency)
- Generates analysis report

## Analysis Criteria

### Architecture Validation

**Expected Nodes**:
- `router` - Route strategy selection
- `research` - Evidence gathering
- `write` - Content generation
- `edit` - Validation and refinement

**Checks**:
- ✓ All expected nodes present
- ✓ Trace metadata complete (task_id, frequency, callback_url)
- ✓ Correct trace hierarchy (all observations linked)
- ✓ No ERROR level observations
- ✓ All nodes have start_time, end_time, input, output

### Quality Assessment

**Output Structure**:
- ✓ sections: Array with 2+ sections
- ✓ citations: Array with 3-10 citations
- ✓ metadata: evidence_count, strategy_slug present

**Content Quality**:
- ✓ Sections are substantive (>100 words each)
- ✓ Citations have title, url, snippet
- ✓ No placeholder text ("TBD", "TODO")

**Performance**:
- ✓ Total latency < 90s (warning threshold)
- ✓ Per-node latency reasonable
- ✓ No timeout errors

## Example Usage

```bash
# Full workflow example
cd .claude/skills/batch-execution-validator/helpers

# Step 1: Trigger batch
python3 api_client.py \
  --api-url https://research-agent-api.replit.app \
  --frequency daily \
  --wait 180

# Output shows:
# Batch triggered: 5 tasks found
# Started at: 2025-11-07T14:30:00Z
# Task IDs: abc-123, def-456, ghi-789, jkl-012, mno-345

# Step 2: Fetch and analyze traces (using output from step 1)
python3 trace_fetcher.py \
  --from-timestamp "2025-11-07T14:30:00Z" \
  --tags batch_execution daily \
  --session-ids "abc-123,def-456,ghi-789,jkl-012,mno-345" \
  --output /tmp/batch_validation_results.json

# Output shows:
# Retrieved 5 traces
# Architecture: 5/5 PASS
# Quality: 4 HIGH, 1 MEDIUM
# Issues: 2 warnings
# Report saved to: /tmp/batch_validation_results.json
```

## Output Format

The trace_fetcher.py generates a JSON report with:

```json
{
  "execution_metadata": {
    "triggered_at": "2025-11-07T14:30:00Z",
    "frequency": "daily",
    "tasks_found": 5
  },
  "traces": [
    {
      "trace_id": "abc-123",
      "user_id": "test@example.com",
      "research_topic": "Latest AI developments",
      "architecture": {
        "status": "PASS",
        "nodes_found": ["router", "research", "write", "edit"],
        "metadata_complete": true,
        "errors": []
      },
      "quality": {
        "status": "HIGH",
        "sections_count": 4,
        "citations_count": 7,
        "avg_section_words": 185,
        "total_latency_ms": 48200,
        "issues": []
      }
    }
  ],
  "summary": {
    "total_traces": 5,
    "architecture_pass": 5,
    "architecture_fail": 0,
    "quality_high": 4,
    "quality_medium": 1,
    "quality_low": 0,
    "warnings": 2,
    "errors": 0
  },
  "recommendations": [
    "All traces passed architecture validation",
    "Quality is consistently high (4/5 HIGH)",
    "Warning: Trace ghi-789 has only 2 citations (expected 3-10)"
  ]
}
```

## Interpreting Results

### Architecture Status

- **PASS**: All expected nodes present, no errors, metadata complete
- **FAIL**: Missing nodes, errors, incomplete hierarchy

### Quality Status

- **HIGH**: 3+ sections, 5-10 citations, >150 words/section, <60s latency
- **MEDIUM**: 2-3 sections, 3-5 citations, >100 words/section, <90s latency
- **LOW**: Incomplete sections, few citations, thin content, slow

### Common Issues

**Architecture Issues**:
- Missing nodes: Check if node was skipped or crashed
- ERROR observations: Review node logs and error messages
- Incomplete metadata: Check API payload and tracing setup

**Quality Issues**:
- Low citation count: Research node may have failed or returned poor results
- Thin content: Write node may need prompt tuning
- Slow performance: Identify bottleneck node (research usually)

## Tips

1. **Run during low traffic**: Batch execution uses production resources
2. **Use realistic test data**: Create test subscriptions with diverse topics
3. **Validate after changes**: Run this skill after any deployment
4. **Monitor trends**: Compare results over time to detect regressions
5. **Check callback logs**: Ensure webhooks are being delivered

## Troubleshooting

**"No tasks found for frequency"**:
- Create test subscriptions: `POST /tasks` with frequency="daily"
- Verify subscriptions are active: `GET /tasks?email=test@example.com`

**"No traces retrieved"**:
- Increase wait time (may need >3min for multiple tasks)
- Check Langfuse credentials are correct
- Verify traces have correct tags

**"Architecture validation fails"**:
- Check API logs for node execution errors
- Review Langfuse trace details manually
- Validate LangGraph configuration

**"Quality is LOW"**:
- Check research node is returning evidence
- Validate write node prompts
- Review LLM responses in trace observations

## Next Steps After Validation

1. **If PASS**: System is healthy, ready for optimization
2. **If architecture issues**: Fix tracing, node execution, or configuration
3. **If quality issues**: Tune prompts, improve research, optimize nodes
4. **Optimization**: Use langfuse-optimization skill to analyze specific issues

---

**Remember**: This skill is for validation, not optimization. Use it to confirm the pipeline works end-to-end, then use specialized skills for tuning individual components.
