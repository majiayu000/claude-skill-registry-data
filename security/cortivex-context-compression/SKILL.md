---
name: cortivex-context-compression
version: 1.0.0
description: Compress agent outputs for efficient context handoff between pipeline nodes while preserving actionable information
category: optimization
tags: [compression, context, handoff, tokens, optimization, multi-agent, efficiency]
author: Cortivex
requires: [cortivex MCP server, cortivex-pipeline]
capabilities: [output-compression, decompression-hints, compression-profiles, handoff-optimization]
---

# Cortivex Context Compression

You are a context compression agent that solves the primary scaling bottleneck in multi-agent pipelines: context window exhaustion during agent handoffs. When a SecurityScanner produces 50K tokens of vulnerability data and a downstream AutoFixer only needs the 2K tokens of actionable findings, this skill compresses the handoff to preserve all decision-relevant information while eliminating redundancy, verbose formatting, and low-priority details.

## Overview

In a Cortivex pipeline, every node's output becomes the next node's input. Without compression, a four-node pipeline accumulates context geometrically: Node A produces 20K tokens, Node B receives 20K and produces 30K, Node C receives 50K and produces 25K, and Node D receives 75K -- well past the point where the downstream agent can reason effectively over the input. Context compression breaks this accumulation by reducing each handoff to a structured summary that retains all information the downstream node needs to act.

The compression system operates at three levels:

- **Lossless** -- Structured extraction that reorganizes the output into a compact schema without discarding any data points. Typical reduction: 60-70%.
- **Lossy** -- Priority-weighted summarization that preserves high-severity and actionable items while condensing or dropping informational content. Typical reduction: 85-92%.
- **Digest** -- Critical findings only. Retains only items that require immediate action or block pipeline progress. Typical reduction: 95-98%.

## When to Use

- Pipeline handoff data exceeds 8K tokens and the downstream node does not need the full verbose output
- You observe downstream agents producing lower quality output because their context windows are saturated with upstream data
- Pipeline cost is dominated by input tokens on downstream nodes processing large upstream outputs
- You are chaining more than three nodes and cumulative context is growing past 50K tokens
- Different downstream nodes need different subsets of the same upstream output
- You want to persist pipeline results in a compact format for historical comparison

## When NOT to Use

- The upstream output is already small (under 4K tokens) -- compression overhead exceeds the savings
- The downstream node explicitly requires the full uncompressed output (e.g., AutoFixer needs the exact file paths, line numbers, and code snippets from CodeReviewer)
- You are debugging a pipeline and need to inspect full intermediate outputs -- use the pipeline debugger instead
- The pipeline has only two nodes -- the overhead of configuring compression is not justified

## How It Works

### Compression Pipeline

When compression is triggered (automatically or manually), the following steps execute:

1. **Schema Detection** -- The compressor analyzes the output structure to identify the node type's output schema (e.g., SecurityScanner outputs have `vulnerabilities`, `dependency_issues`, `summary` fields)
2. **Profile Application** -- The compression profile for the node type determines which fields are critical, which are reducible, and which are droppable
3. **Priority Scoring** -- Each item in the output receives a priority score based on severity, actionability, and downstream relevance
4. **Reduction** -- Based on the compression level, items below the priority threshold are condensed or removed
5. **Decompression Hint Generation** -- Metadata is attached describing what was compressed, what was dropped, and how to request the full version
6. **Validation** -- The compressed output is validated to ensure it still satisfies the downstream node's input schema requirements

### Automatic Triggers

Compression activates automatically when any of these thresholds are exceeded:

- Node output exceeds `auto_compress_threshold_tokens` (default: 8192)
- Cumulative pipeline context exceeds `pipeline_context_limit_tokens` (default: 32768)
- A downstream node's total input (all dependencies combined) exceeds `node_input_limit_tokens` (default: 16384)

### Decompression Hints

Every compressed output includes a `_compression` metadata block that tells the downstream agent what was compressed:

```json
{
  "_compression": {
    "original_tokens": 48230,
    "compressed_tokens": 2100,
    "level": "lossy",
    "profile": "SecurityScanner",
    "dropped_fields": ["raw_scan_output", "dependency_tree", "file_contents"],
    "condensed_fields": ["vulnerabilities.recommendation", "dependency_issues.fix_steps"],
    "preserved_fields": ["vulnerabilities.severity", "vulnerabilities.file", "vulnerabilities.line", "summary"],
    "request_full": "cortivex_compress({ action: 'decompress', node_id: 'security_scan', run_id: 'ctx-a1b2c3', fields: ['vulnerabilities.recommendation'] })"
  }
}
```

If a downstream agent determines it needs a field that was compressed or dropped, it can call `cortivex_compress` with the `decompress` action to retrieve the full data for specific fields on demand.

## Pipeline Configuration

### Enabling Compression via YAML

Add a `compress_handoff` block to individual nodes or at the pipeline level:

```yaml
name: pr-review-compressed
version: "1.0"
description: PR review with context compression between nodes
compress_handoff:
  enabled: true
  default_level: lossy
  auto_compress_threshold_tokens: 8192
  pipeline_context_limit_tokens: 32768
  node_input_limit_tokens: 16384

nodes:
  - id: security_scan
    type: SecurityScanner
    compress_handoff:
      level: lossy
      profile: SecurityScanner
      preserve_fields:
        - "vulnerabilities.severity"
        - "vulnerabilities.file"
        - "vulnerabilities.line"
        - "vulnerabilities.type"
        - "summary"
      drop_fields:
        - "raw_scan_output"
        - "dependency_tree"
    config:
      scan_depth: deep
      severity_threshold: low

  - id: code_review
    type: CodeReviewer
    depends_on: [security_scan]
    compress_handoff:
      level: lossy
      profile: CodeReviewer
      priority_weights:
        severity_error: 1.0
        severity_warning: 0.7
        severity_info: 0.3
      min_priority: 0.5
    config:
      review_scope: full
      max_issues: 100

  - id: auto_fix
    type: AutoFixer
    depends_on: [code_review]
    compress_handoff:
      level: lossless
    config:
      fix_categories: [bugs, security]

  - id: summary
    type: PRCreator
    depends_on: [security_scan, code_review, auto_fix]
    compress_handoff:
      level: digest
      profile: PRSummary
    config:
      action: update
      include_summary: true
```

### Per-Node Compression Profiles

Define custom compression profiles that control how each node type's output is compressed:

```yaml
compression_profiles:
  SecurityScanner:
    critical_fields:
      - "vulnerabilities[].severity"
      - "vulnerabilities[].type"
      - "vulnerabilities[].file"
      - "vulnerabilities[].line"
      - "summary"
    reducible_fields:
      - "vulnerabilities[].description"
      - "vulnerabilities[].recommendation"
      - "dependency_issues[].fix_steps"
    droppable_fields:
      - "raw_scan_output"
      - "dependency_tree"
      - "file_contents"
      - "scan_metadata"
    severity_priority:
      critical: 1.0
      high: 0.9
      medium: 0.6
      low: 0.3

  CodeReviewer:
    critical_fields:
      - "issues[].severity"
      - "issues[].category"
      - "issues[].file"
      - "issues[].line"
      - "summary"
      - "overall_quality"
    reducible_fields:
      - "issues[].description"
      - "issues[].suggestion"
    droppable_fields:
      - "issues[].code_context"
      - "issues[].related_files"
    severity_priority:
      error: 1.0
      warning: 0.7
      info: 0.2

  TestRunner:
    critical_fields:
      - "summary.passed"
      - "summary.failed"
      - "summary.coverage"
      - "failed_tests[].name"
      - "failed_tests[].error"
    reducible_fields:
      - "failed_tests[].stack_trace"
      - "failed_tests[].expected_vs_actual"
    droppable_fields:
      - "passed_tests"
      - "timing_details"
      - "coverage_by_file"
```

## MCP Tool Reference

All compression operations use the `cortivex_compress` MCP tool with an `action` parameter.

### Action: compress

Compress a node's output using a specified level and profile.

**Request:**
```json
{
  "tool": "cortivex_compress",
  "arguments": {
    "action": "compress",
    "node_id": "security_scan",
    "level": "lossy",
    "profile": "SecurityScanner",
    "run_id": "ctx-a1b2c3"
  }
}
```

**Response:**
```json
{
  "status": "compressed",
  "node_id": "security_scan",
  "level": "lossy",
  "original_tokens": 48230,
  "compressed_tokens": 2100,
  "compression_ratio": "95.6%",
  "items_preserved": 12,
  "items_condensed": 8,
  "items_dropped": 34,
  "compressed_output": {
    "vulnerabilities": [
      { "severity": "high", "type": "sql_injection", "file": "src/db/queries.ts", "line": 47 },
      { "severity": "high", "type": "xss", "file": "src/api/render.ts", "line": 112 },
      { "severity": "medium", "type": "insecure_random", "file": "src/auth/token.ts", "line": 8 }
    ],
    "dependency_issues_count": 4,
    "dependency_issues_critical": [
      { "package": "lodash", "version": "4.17.15", "cve": "CVE-2021-23337", "severity": "high" }
    ],
    "summary": { "total_issues": 12, "critical": 0, "high": 3, "medium": 5, "low": 4 },
    "_compression": {
      "original_tokens": 48230,
      "compressed_tokens": 2100,
      "level": "lossy",
      "profile": "SecurityScanner",
      "dropped_fields": ["raw_scan_output", "dependency_tree", "file_contents"],
      "condensed_fields": ["vulnerabilities.recommendation", "dependency_issues.fix_steps"],
      "request_full": "cortivex_compress({ action: 'decompress', node_id: 'security_scan', run_id: 'ctx-a1b2c3' })"
    }
  }
}
```

**Request -- compress with custom priority threshold:**
```json
{
  "tool": "cortivex_compress",
  "arguments": {
    "action": "compress",
    "node_id": "code_review",
    "level": "lossy",
    "profile": "CodeReviewer",
    "options": {
      "min_priority": 0.7,
      "max_output_tokens": 3000,
      "preserve_fields": ["issues[].suggestion"]
    },
    "run_id": "ctx-a1b2c3"
  }
}
```

### Action: decompress

Retrieve the full uncompressed data for specific fields that were condensed or dropped during compression.

**Request -- decompress specific fields:**
```json
{
  "tool": "cortivex_compress",
  "arguments": {
    "action": "decompress",
    "node_id": "security_scan",
    "fields": ["vulnerabilities.recommendation", "dependency_issues.fix_steps"],
    "run_id": "ctx-a1b2c3"
  }
}
```

**Response:**
```json
{
  "status": "decompressed",
  "node_id": "security_scan",
  "fields_restored": 2,
  "tokens_added": 3420,
  "data": {
    "vulnerabilities": [
      {
        "file": "src/db/queries.ts",
        "line": 47,
        "recommendation": "Replace string interpolation with parameterized query. Use db.query('SELECT * FROM users WHERE id = $1', [userId]) instead of template literal."
      },
      {
        "file": "src/api/render.ts",
        "line": 112,
        "recommendation": "Sanitize user input before rendering. Use DOMPurify.sanitize(userContent) or escape HTML entities."
      }
    ],
    "dependency_issues": [
      {
        "package": "lodash",
        "fix_steps": "Run npm install lodash@4.17.21. No breaking changes between 4.17.15 and 4.17.21."
      }
    ]
  }
}
```

**Request -- decompress full output (use sparingly):**
```json
{
  "tool": "cortivex_compress",
  "arguments": {
    "action": "decompress",
    "node_id": "security_scan",
    "fields": ["*"],
    "run_id": "ctx-a1b2c3"
  }
}
```

### Action: profile

Create, view, or update compression profiles for node types.

**Request -- view existing profile:**
```json
{
  "tool": "cortivex_compress",
  "arguments": {
    "action": "profile",
    "operation": "get",
    "profile_name": "SecurityScanner"
  }
}
```

**Response:**
```json
{
  "profile_name": "SecurityScanner",
  "critical_fields": ["vulnerabilities[].severity", "vulnerabilities[].type", "vulnerabilities[].file", "vulnerabilities[].line", "summary"],
  "reducible_fields": ["vulnerabilities[].description", "vulnerabilities[].recommendation"],
  "droppable_fields": ["raw_scan_output", "dependency_tree", "file_contents"],
  "severity_priority": { "critical": 1.0, "high": 0.9, "medium": 0.6, "low": 0.3 }
}
```

**Request -- create custom profile:**
```json
{
  "tool": "cortivex_compress",
  "arguments": {
    "action": "profile",
    "operation": "create",
    "profile_name": "BugHunterForAutoFix",
    "definition": {
      "critical_fields": [
        "bugs[].category",
        "bugs[].file",
        "bugs[].line",
        "bugs[].suggested_fix"
      ],
      "reducible_fields": [
        "bugs[].description",
        "bugs[].reproduction"
      ],
      "droppable_fields": [
        "edge_cases",
        "bugs[].confidence_reasoning"
      ],
      "severity_priority": {
        "high": 1.0,
        "medium": 0.8,
        "low": 0.3
      }
    }
  }
}
```

### Action: stats

View compression statistics across pipeline runs to understand token savings and identify nodes that benefit most from compression.

**Request:**
```json
{
  "tool": "cortivex_compress",
  "arguments": {
    "action": "stats",
    "run_id": "ctx-a1b2c3"
  }
}
```

**Response:**
```json
{
  "run_id": "ctx-a1b2c3",
  "pipeline": "pr-review-compressed",
  "compression_summary": {
    "total_original_tokens": 124500,
    "total_compressed_tokens": 18200,
    "overall_reduction": "85.4%",
    "estimated_cost_saved": "$0.031",
    "decompress_requests": 2,
    "decompress_tokens_restored": 5840
  },
  "per_node": [
    {
      "node_id": "security_scan",
      "level": "lossy",
      "original_tokens": 48230,
      "compressed_tokens": 2100,
      "reduction": "95.6%",
      "decompress_requests": 1
    },
    {
      "node_id": "code_review",
      "level": "lossy",
      "original_tokens": 52800,
      "compressed_tokens": 8400,
      "reduction": "84.1%",
      "decompress_requests": 1
    },
    {
      "node_id": "auto_fix",
      "level": "lossless",
      "original_tokens": 23470,
      "compressed_tokens": 7700,
      "reduction": "67.2%",
      "decompress_requests": 0
    }
  ]
}
```

**Request -- aggregate stats across multiple runs:**
```json
{
  "tool": "cortivex_compress",
  "arguments": {
    "action": "stats",
    "pipeline": "pr-review-compressed",
    "aggregate": true,
    "last_n_runs": 10
  }
}
```

## Node Reference

| Node Type | Recommended Level | Typical Reduction | Key Preserved Fields |
|-----------|------------------|-------------------|---------------------|
| SecurityScanner | lossy | 90-96% | severity, type, file, line, summary |
| CodeReviewer | lossy | 80-90% | severity, category, file, line, suggestion |
| BugHunter | lossy | 75-85% | category, file, line, confidence, suggested_fix |
| PerformanceProfiler | lossy | 80-88% | severity, category, file, suggestion |
| ArchitectAnalyzer | lossless | 60-70% | modules, patterns, antipatterns, metrics |
| AutoFixer | lossless | 50-65% | files_modified, fixes_applied, backup_paths |
| TestRunner | digest | 92-98% | passed, failed, coverage, failed_test_names |
| DocWriter | digest | 90-95% | files_generated, sections_updated |
| PRCreator | digest | 85-92% | pr_url, pr_number, status |

## Quick Reference

| Action | Purpose | Key Parameters |
|--------|---------|---------------|
| `compress` | Compress a node's output for downstream handoff | `node_id`, `level`, `profile`, `options` |
| `decompress` | Retrieve full data for specific compressed fields | `node_id`, `fields` |
| `profile` | Create, view, or update compression profiles | `operation`, `profile_name`, `definition` |
| `stats` | View compression statistics and token savings | `run_id`, `pipeline`, `aggregate` |

## Best Practices

1. **Match compression level to downstream needs** -- Use `lossless` when the downstream node needs structured access to all data points (e.g., AutoFixer needs every issue to know what to fix). Use `lossy` when the downstream node only needs high-priority items (e.g., PRCreator summarizing findings). Use `digest` for terminal nodes that only need to report top-level outcomes.

2. **Create node-type-specific profiles** -- Generic compression loses important domain structure. A SecurityScanner profile knows that `severity` and `cwe` are critical fields while `raw_scan_output` is always droppable. A TestRunner profile knows that failed test names and error messages matter while the list of 500 passed tests does not. Build profiles that encode this domain knowledge.

3. **Set auto-compress thresholds conservatively** -- Start with an `auto_compress_threshold_tokens` of 8192. If downstream agents are still producing high-quality output at that threshold, raise it. If they are missing important details, lower it and switch from `lossy` to `lossless`. The goal is the minimum compression that keeps downstream agents effective.

4. **Monitor decompress request frequency** -- If a downstream node is consistently requesting decompression for the same fields, those fields should be promoted from `reducible` to `critical` in the compression profile. Frequent decompression requests indicate the profile is too aggressive for that field.

5. **Use lossless for modification nodes** -- Nodes that modify code (AutoFixer, RefactorAgent, TypeMigrator) generally need precise details -- exact file paths, line numbers, and code context. Compressing their inputs too aggressively causes them to produce incorrect or incomplete fixes. Default to `lossless` for these handoffs.

6. **Compress differently for different consumers** -- When a node's output feeds into multiple downstream nodes, each consumer may need different compression levels. SecurityScanner output going to AutoFixer should be `lossless` (needs full details to fix), while the same output going to PRCreator can be `digest` (only needs the summary counts).

7. **Review stats after pipeline runs** -- Use the `stats` action to identify which nodes produce the most tokens and benefit most from compression. Focus profile tuning on high-volume nodes where small improvements in compression ratio yield large token savings.

## Reasoning Protocol

Before configuring compression for a pipeline, reason through these questions explicitly:

1. **How large are the node outputs?** Check the average output token counts for each node type in your pipeline. If no node exceeds 4K tokens, compression adds overhead without meaningful benefit. Only invest in compression configuration when you have nodes producing 8K+ tokens.

2. **What does each downstream node actually need?** For every edge in the DAG, list the specific fields the downstream node reads from the upstream output. If AutoFixer only reads `issues[].file`, `issues[].line`, and `issues[].suggestion` from CodeReviewer, everything else can be dropped or condensed.

3. **What is the cost of losing information?** For each field you plan to make `reducible` or `droppable`, ask: if this field is missing, will the downstream node produce incorrect output or will it just produce slightly less detailed output? Fields that affect correctness must be `critical`.

4. **Is the compression profile stable or experimental?** New profiles should start at `lossless` level and be tightened to `lossy` only after you have verified that downstream nodes produce equivalent quality output. Never start a new profile at `digest` level.

5. **Are there multiple consumers with different needs?** When a node fans out to multiple downstream nodes, check if a single compression level serves all consumers. If not, configure per-edge compression rather than per-node compression.

6. **What is the expected token savings?** Estimate the reduction ratio using the Node Reference table above. If the expected savings are less than 2K tokens, the compression overhead (profile matching, priority scoring, decompression hint generation) may not be worth it.

## Anti-Patterns

| Anti-Pattern | Consequence | Correct Approach |
|-------------|------------|-----------------|
| Using `digest` level for AutoFixer input | AutoFixer receives only summaries and cannot locate or fix specific issues | Use `lossless` for modification node inputs |
| Same compression profile for all node types | Drops critical fields from some nodes while preserving irrelevant fields from others | Create node-type-specific profiles that encode domain knowledge |
| Setting auto-compress threshold too low (e.g., 1K tokens) | Compresses already-small outputs, adding overhead without savings | Set threshold to 8K+ tokens; do not compress outputs that are already compact |
| Never monitoring decompress request frequency | Downstream nodes waste tokens on repeated decompression requests for fields that should be preserved | Review stats and promote frequently-requested fields to `critical` |
| Compressing inputs to ArchitectAnalyzer | ArchitectAnalyzer needs full codebase context to produce accurate structural analysis | Skip compression for nodes that inherently require comprehensive input |
| Using `lossy` compression without defining priority weights | Default priority scoring may drop domain-critical items | Always define `severity_priority` weights that match the node type's importance hierarchy |
| Compressing outputs under 4K tokens | Compression metadata and decompression hints add overhead that exceeds the savings | Skip compression for small outputs; let them pass through uncompressed |

**WRONG:**
```yaml
# Aggressive compression on a modification node's input
nodes:
  - id: code_review
    type: CodeReviewer
    compress_handoff:
      level: digest        # only summaries passed downstream
  - id: auto_fix
    type: AutoFixer
    depends_on: [code_review]
    # auto_fix receives: "7 issues found, 3 errors, 4 warnings"
    # auto_fix cannot fix anything because it has no file/line/description data
```

**RIGHT:**
```yaml
# Appropriate compression levels per consumer
nodes:
  - id: code_review
    type: CodeReviewer
    compress_handoff:
      level: lossless       # preserve all structured data for auto_fix
  - id: auto_fix
    type: AutoFixer
    depends_on: [code_review]
    compress_handoff:
      level: digest          # only summary needed by pr_create
  - id: pr_create
    type: PRCreator
    depends_on: [auto_fix]
```

**WRONG:**
```yaml
# Compressing tiny outputs
nodes:
  - id: pr_create
    type: PRCreator
    compress_handoff:
      level: lossy           # PRCreator output is ~800 tokens -- compression adds overhead
```

**RIGHT:**
```yaml
# Only compress when output exceeds threshold
compress_handoff:
  enabled: true
  auto_compress_threshold_tokens: 8192
  # PRCreator output (~800 tokens) passes through uncompressed automatically
  # SecurityScanner output (~48K tokens) gets compressed automatically
```

## Grounding Rules

- **Unsure which compression level to use:** Default to `lossless` and measure the downstream node's output quality. Only tighten to `lossy` after confirming the downstream node produces equivalent results with the compressed input. Treat `digest` as a last resort for terminal reporting nodes only.

- **Downstream node quality degraded after enabling compression:** Check which fields were condensed or dropped by inspecting the `_compression` metadata. Promote the missing fields from `reducible` to `critical` in the profile. If quality is still poor, drop the compression level back to `lossless` for that edge.

- **New node type without a compression profile:** Do not attempt to build a profile without first running the node uncompressed and examining its output structure. Run the pipeline once, inspect the output with `cortivex_debug`, identify which fields are critical for downstream consumers, then build the profile from evidence.

- **Cost savings are not significant:** Compression saves cost proportional to input token reduction on downstream nodes. If your pipeline has only two short-output nodes, compression will not produce meaningful savings. Focus compression effort on pipelines with 4+ nodes and at least one node producing over 20K tokens.

- **Conflicting compression needs from multiple consumers:** Configure per-edge compression using separate `compress_handoff` blocks on the consumer nodes rather than the producer node. This allows SecurityScanner to send `lossless` to AutoFixer and `digest` to PRCreator from the same output.

## Advanced Capabilities

### Semantic Chunking Strategies

Semantic chunking splits node output into meaningful segments before compression, allowing mixed compression levels within a single handoff. Each chunk is classified by domain relevance and compressed independently, so critical sections stay at `lossless` while informational sections compress to `digest`.

```json
{
  "tool": "cortivex_compress_chunk",
  "arguments": {
    "action": "compress",
    "node_id": "security_scan",
    "run_id": "ctx-d4e5f6",
    "chunks": [
      { "chunk_id": "vuln_critical", "content_path": "vulnerabilities[?severity=='critical']", "level": "lossless", "semantic_tag": "actionable_findings" },
      { "chunk_id": "vuln_info", "content_path": "vulnerabilities[?severity=='low']", "level": "digest", "semantic_tag": "informational" },
      { "chunk_id": "scan_metadata", "content_path": "scan_metadata", "level": "digest", "semantic_tag": "telemetry" }
    ]
  }
}
```

```json
{
  "status": "chunked_compression_complete",
  "total_original_tokens": 51200,
  "total_compressed_tokens": 4850,
  "chunks": [
    { "chunk_id": "vuln_critical", "original": 8400, "compressed": 8400, "level": "lossless" },
    { "chunk_id": "vuln_info", "original": 22300, "compressed": 680, "level": "digest" },
    { "chunk_id": "scan_metadata", "original": 20500, "compressed": 410, "level": "digest" }
  ]
}
```

### Priority-Based Retention Policies

Retention policies govern how long original and compressed data remains available for decompression. Define TTLs by severity or node type to automatically clean up low-priority data while keeping critical findings rehydratable.

```yaml
retention_policies:
  default:
    uncompressed_ttl: 3600
    compressed_ttl: 86400
    decompression_cache_ttl: 900
  by_severity:
    critical: { uncompressed_ttl: 604800, compressed_ttl: 2592000 }  # 7d / 30d
    high:     { uncompressed_ttl: 86400,  compressed_ttl: 604800 }   # 24h / 7d
    medium:   { uncompressed_ttl: 3600,   compressed_ttl: 86400 }    # 1h / 24h
    low:      { uncompressed_ttl: 600,    compressed_ttl: 3600 }     # 10m / 1h
  by_node_type:
    AutoFixer:  { uncompressed_ttl: 172800 }  # 48h for modification nodes
    PRCreator:  { uncompressed_ttl: 900 }     # terminal nodes need data briefly
```

### Compression Quality Metrics

The quality metrics API evaluates whether compressed output retains sufficient information for downstream consumers. It scores semantic coverage, field completeness, reconstruction fidelity, and actionability to detect overly aggressive compression.

```typescript
interface CompressionQualityAnalysis {
  run_id: string;
  node_id: string;
  metrics: {
    semantic_coverage: number;      // 0.0-1.0, how much meaning was preserved
    field_completeness: number;     // 0.0-1.0, whether critical fields survived
    reconstruction_fidelity: number; // 0.0-1.0, accuracy of recovery from compressed form
    actionability_score: number;    // 0.0-1.0, downstream usefulness of compressed output
  };
  recommendation: "keep_current" | "loosen_compression" | "tighten_compression" | "switch_to_lossless";
  field_warnings: Array<{
    field: string;
    issue: "dropped_critical" | "over_condensed" | "low_fidelity";
  }>;
}
```

### Context Restoration & Rehydration

Context restoration goes beyond raw decompression by reconstructing data in the format the downstream node expects, applying schema transformations for the consumer's input contract. Use `cortivex_compress_restore` with a `merge_strategy` to patch restored fields into the existing compressed handoff.

```json
{
  "tool": "cortivex_compress_restore",
  "arguments": {
    "action": "restore",
    "node_id": "code_review",
    "run_id": "ctx-d4e5f6",
    "restore_fields": ["issues[].description", "issues[].code_context"],
    "target_schema": "AutoFixer.input",
    "merge_strategy": "patch"
  }
}
```

```json
{
  "status": "restored",
  "fields_restored": 2,
  "tokens_before_restore": 3200,
  "tokens_after_restore": 9850,
  "restored_data": {
    "issues": [{
      "file": "src/db/queries.ts", "line": 47,
      "description": "User-controlled input concatenated into SQL query without parameterization.",
      "code_context": "const result = db.query(`SELECT * FROM users WHERE id = ${userId}`);"
    }]
  },
  "rehydration_metadata": { "source_ttl_remaining_seconds": 2940, "restoration_completeness": 1.0 }
}
```

### Adaptive Compression Thresholds

Adaptive thresholds monitor cumulative context growth and automatically adjust compression levels based on observed pipeline pressure. When utilization exceeds the upper trigger, the system tightens compression along the escalation sequence (`lossless` to `lossy` to `digest`). When pressure drops, it loosens to restore information quality. The `cooldown_seconds` parameter prevents thrashing during short token spikes.

```json
{
  "mode": "adaptive",
  "base_thresholds": {
    "auto_compress_tokens": 8192,
    "pipeline_context_limit": 32768,
    "node_input_limit": 16384
  },
  "adaptation_rules": [
    { "trigger": "context_utilization_above", "threshold_value": 0.85, "action": "tighten_one_level", "scope": "pipeline", "cooldown_seconds": 60 },
    { "trigger": "context_utilization_below", "threshold_value": 0.40, "action": "loosen_one_level", "scope": "pipeline", "cooldown_seconds": 120 },
    { "trigger": "decompress_rate_above", "threshold_value": 0.30, "action": "loosen_one_level", "scope": "node", "cooldown_seconds": 90 }
  ],
  "escalation_sequence": ["lossless", "lossy", "digest"]
}

## Security Hardening (OWASP AST10 Aligned)

Security controls for context compression aligned with the OWASP Automated Security Testing Top 10 risk framework.

### AST08: Security Finding Preservation

Critical and high severity findings are never compressed below `lossless`. This addresses AST08 (Insufficient Coverage of Security Artifacts).

```yaml
security_finding_preservation:
  # AST08 -- Security findings at critical/high severity are never lossy-compressed
  rules:
    - { severity: critical, min_compression_level: lossless, override_allowed: false,
        preserve: [severity, type, file, line, description, recommendation, cwe, cvss_score] }
    - { severity: high, min_compression_level: lossless, override_allowed: false,
        preserve: [severity, type, file, line, description, recommendation] }
    - { severity: medium, min_compression_level: lossy, preserve: [severity, type, file, line] }
    - { severity: low, min_compression_level: digest }
  enforcement: compression_interceptor
  ast_reference: "AST08"
```

```json
{
  "tool": "cortivex_compress",
  "request": { "action": "compress", "node_id": "security_scan", "level": "digest", "run_id": "ctx-a1b2c3" },
  "response": {
    "status": "compressed_with_overrides",
    "effective_levels": { "critical_findings": "lossless", "high_findings": "lossless", "medium_findings": "lossy", "low_findings": "digest" },
    "reason": "AST08: Preservation elevated compression for 3 critical and 2 high findings",
    "original_tokens": 48230, "compressed_tokens": 12400
  }
}
```

### AST08: Data Classification-Aware Compression

Restricted data receives `lossless` only. The engine inspects classification labels before selecting a strategy.

```yaml
classification_aware_compression:
  classification_levels:
    - { level: restricted, allowed_compression: lossless, decompression_requires: caller_authorization, ast_reference: "AST08" }
    - { level: confidential, allowed_compression: lossless, decompression_requires: caller_authorization }
    - { level: internal, allowed_compression: lossy }
    - { level: public, allowed_compression: digest }
  label_sources: ["_data_classification", "_sensitivity_tags"]
  default_inference: "SecurityScanner output defaults to 'confidential' if no label present"
  enforcement: pre_compression_gate
```

```typescript
interface ClassificationCompressionPolicy {
  data_classification: "restricted" | "confidential" | "internal" | "public";
  max_compression_level: "lossless" | "lossy" | "digest";
  requires_authorization_for_decompression: boolean;
  auto_label_rules: Array<{ node_type: string; default_classification: string }>;
  ast_reference: "AST08";
}
```

### Compression Artifact Detection

Post-compression validation detects corruption, schema violations, and semantic drift before the handoff reaches downstream nodes.

```yaml
compression_artifact_detection:
  enabled: true
  checks:
    - { id: schema_conformance, method: json_schema_validation, fail_action: reject_compressed_output }
    - { id: field_count_sanity, method: count_comparison, tolerance: 0, fail_action: reject_compressed_output }
    - { id: semantic_hash_check, method: sha256_per_field, scope: critical_fields_only, fail_action: reject_compressed_output }
    - { id: encoding_integrity, method: byte_sequence_validation, fail_action: reject_compressed_output }
    - { id: numeric_drift, method: exact_value_comparison, scope: [cvss_score, line], fail_action: reject_compressed_output }
  on_artifact_detected: { action: fallback_to_lossless, alert: true, log_level: error }
```

```json
{
  "tool": "cortivex_compress",
  "request": { "action": "compress", "node_id": "security_scan", "level": "lossy", "run_id": "ctx-d4e5f6" },
  "response": {
    "status": "artifact_detected_fallback", "original_level": "lossy", "fallback_level": "lossless",
    "artifact_details": { "check_id": "semantic_hash_check", "field": "vulnerabilities[2].cvss_score" },
    "ast_reference": "AST08"
  }
}
```

### Retention Policy Enforcement

Uncompressed sensitive data is wiped after TTL expiry. A background reaper enforces mandatory cleanup.

```yaml
retention_enforcement:
  mandatory_cleanup: { enabled: true, enforcement: background_reaper, scan_interval_seconds: 300 }
  policies:
    - { classification: restricted, uncompressed_max_ttl: 3600, compressed_max_ttl: 86400, cleanup: secure_wipe, ast_reference: "AST08" }
    - { classification: confidential, uncompressed_max_ttl: 14400, compressed_max_ttl: 604800, cleanup: secure_wipe }
    - { classification: internal, uncompressed_max_ttl: 86400, compressed_max_ttl: 2592000, cleanup: standard_delete }
  overdue_handling: { action: force_delete_and_alert, alert_channel: security-ops, escalation_after_minutes: 30 }
  audit: { log_all_deletions: true, retention_extension_requires: security_ops_approval }
```

```json
{
  "tool": "cortivex_compress",
  "request": { "action": "retention_status", "run_id": "ctx-a1b2c3" },
  "response": {
    "nodes": [{ "node_id": "security_scan", "classification": "confidential",
      "uncompressed_status": "expired_and_wiped", "compressed_expires_at": "2026-03-31T10:00:00Z" }],
    "overdue_items": 0, "ast_reference": "AST08"
  }
}
```

### AST08: Decompression Authorization

Restricted/confidential data rehydration requires verified caller identity and role-based access control.

```yaml
decompression_authorization:
  enabled: true
  authorization_model: role_based
  rules:
    - { classification: restricted, roles: [SecurityReviewer, AutoFixer, PipelineAdmin], purpose_required: true, audit: always, ast_reference: "AST08" }
    - { classification: confidential, roles: [SecurityReviewer, AutoFixer, CodeReviewer, PipelineAdmin], audit: always }
    - { classification: internal, roles: [any_verified], audit: on_failure }
    - { classification: public, roles: [any], audit: never }
  caller_verification: { method: signed_request, max_token_age_seconds: 300 }
```

```typescript
interface DecompressionAuthorizationRequest {
  caller_node_id: string;
  target_node_id: string;
  target_fields: string[];
  data_classification: "restricted" | "confidential" | "internal" | "public";
  authorization_token: string;
  ast_reference: "AST08";
}
```

```json
{
  "tool": "cortivex_compress",
  "request": { "action": "decompress", "node_id": "security_scan", "fields": ["vulnerabilities.recommendation"],
    "run_id": "ctx-a1b2c3", "caller_node_id": "pr_summary" },
  "response": {
    "status": "authorization_denied",
    "reason": "AST08: Node 'pr_summary' (PRCreator) not authorized for confidential security findings",
    "required_roles": ["SecurityReviewer", "AutoFixer", "CodeReviewer", "PipelineAdmin"],
    "audit_entry_id": "audit-decomp-denied-9f3a"
  }
}
```
