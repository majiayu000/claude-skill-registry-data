---
name: cortivex-knowledge
version: 1.0.0
description: Shared CRDT knowledge graphs across pipeline agents using KnowledgeCurator nodes for deduplication and synthesis
category: coordination
tags: [knowledge-graph, crdt, shared-memory, deduplication, synthesis, agents]
author: Cortivex
requires: [cortivex MCP server]
capabilities: [knowledge-sharing, duplicate-prevention, finding-synthesis, graph-query]
---

# Cortivex Knowledge Graph

This skill covers how KnowledgeCurator nodes maintain shared CRDT knowledge graphs across pipeline agents, preventing duplicate work and synthesizing findings from multiple agents working in parallel.

## Overview

When multiple agents analyze the same codebase, they independently discover facts about files, functions, patterns, and relationships. Without coordination, agents duplicate effort and produce redundant findings. The KnowledgeCurator node solves this by maintaining a shared knowledge graph that all agents can read from and write to.

The knowledge graph uses Conflict-free Replicated Data Types (CRDTs) for eventual consistency. This means:

- Any agent can add knowledge at any time without locks
- Concurrent additions from multiple agents merge automatically without conflicts
- No central coordinator is required for graph updates
- All agents converge to the same view of the graph

## When to Use

- Pipelines with 2+ analysis agents working on the same codebase
- When agents should be aware of what other agents have already discovered
- To prevent multiple agents from analyzing the same file or function
- When downstream nodes need a unified summary of all agent findings
- For long-running pipelines where agents accumulate knowledge over time

You do NOT need a KnowledgeCurator for:

- Single-agent pipelines
- Pipelines where agents work on completely separate files with no overlap
- Simple sequential DAGs where each node receives the full output of the previous one

## How It Works

### Knowledge Node Types

The graph stores five types of knowledge nodes:

| Type | Represents | Examples |
|------|-----------|----------|
| **Entity** | A specific code artifact | `src/auth/login.ts`, `validateJWT()`, `UserModel` |
| **Concept** | An abstract pattern or principle | "repository pattern", "middleware chain", "dependency injection" |
| **Process** | A workflow or operational procedure | "CI/CD pipeline", "database migration", "build process" |
| **Data** | A data structure or schema | "User model", "JWT payload", "API response schema" |
| **Finding** | An analysis result from an agent | "SQL injection in queries.ts:47", "O(n^2) loop in filter.ts:34" |

### Edge Types

Relationships between nodes are typed:

| Edge | Meaning | Example |
|------|---------|---------|
| `uses` | Entity A calls or imports Entity B | `login.ts` uses `validateJWT()` |
| `implements` | Entity implements a Concept | `UserRepository` implements "repository pattern" |
| `depends_on` | A requires B to function | `auth.ts` depends_on `session.ts` |
| `produces` | A Process produces a Data or Entity | "build process" produces `dist/bundle.js` |
| `related_to` | General association | "rate limiting" related_to "middleware chain" |
| `found_in` | A Finding was discovered in an Entity | "SQL injection" found_in `queries.ts` |
| `supersedes` | A newer Finding replaces an older one | "fixed: SQL injection" supersedes "SQL injection" |

### CRDT Merge Semantics

- **Add-only nodes**: Knowledge nodes are never deleted. The graph is a grow-only set.
- **Last-write-wins metadata**: If two agents update the same node's metadata, the latest timestamp wins.
- **Automatic merge**: No manual conflict resolution is needed. The CRDT guarantees convergence.
- **Idempotent additions**: Adding the same node twice has no effect (deduplication is built in).

## Pipeline Configuration

### Adding a KnowledgeCurator to a Pipeline

```yaml
name: knowledge-aware-review
version: "1.0"
description: Multi-agent review with shared knowledge graph
nodes:
  - id: knowledge
    type: KnowledgeCurator
    config:
      graph_id: review-session-1
      persist: true
      dedup_strategy: content-hash
      merge_interval_seconds: 5
      max_nodes: 10000
      max_edges: 50000

  - id: security_scan
    type: SecurityScanner
    depends_on: [knowledge]
    config:
      scan_depth: deep
      knowledge_graph: review-session-1
      skip_known_findings: true

  - id: code_review
    type: CodeReviewer
    depends_on: [knowledge]
    config:
      review_scope: changed_files
      knowledge_graph: review-session-1
      skip_known_findings: true

  - id: bug_hunt
    type: BugHunter
    depends_on: [knowledge]
    config:
      hunt_scope: changed_files
      knowledge_graph: review-session-1
      skip_known_findings: true

  - id: synthesize
    type: KnowledgeCurator
    depends_on: [security_scan, code_review, bug_hunt]
    config:
      graph_id: review-session-1
      action: synthesize
      output_format: structured
```

### How Agents Interact with the Graph

When an agent has `knowledge_graph` configured, it performs these steps during its work:

**Before starting analysis on a file:**

```
cortivex_knowledge({
  action: "query",
  graph_id: "review-session-1",
  query: {
    type: "entity",
    label: "src/auth/login.ts"
  }
})
```

If the file already has findings from another agent, the current agent can skip it or focus on aspects not yet covered.

**After discovering something:**

```
cortivex_knowledge({
  action: "add",
  graph_id: "review-session-1",
  nodes: [
    {
      type: "finding",
      label: "SQL injection vulnerability",
      metadata: {
        file: "src/db/queries.ts",
        line: 47,
        severity: "high",
        agent: "agent-security-scanner-1",
        cwe: "CWE-89"
      }
    }
  ],
  edges: [
    {
      type: "found_in",
      source: "SQL injection vulnerability",
      target: "src/db/queries.ts"
    }
  ]
})
```

**Checking for duplicate work:**

```
cortivex_knowledge({
  action: "check_covered",
  graph_id: "review-session-1",
  files: ["src/auth/login.ts", "src/auth/session.ts"]
})
```

Response:

```json
{
  "src/auth/login.ts": {
    "covered": true,
    "agents": ["agent-code-reviewer-2"],
    "findings_count": 3
  },
  "src/auth/session.ts": {
    "covered": false,
    "agents": [],
    "findings_count": 0
  }
}
```

The agent can then skip `login.ts` and focus on `session.ts`.

### Synthesis

After all analysis agents complete, a KnowledgeCurator in `synthesize` mode produces a unified report:

```
cortivex_knowledge({
  action: "synthesize",
  graph_id: "review-session-1",
  output_format: "structured"
})
```

Response:

```json
{
  "graph_stats": {
    "total_nodes": 47,
    "total_edges": 83,
    "entities": 28,
    "findings": 12,
    "concepts": 4,
    "agents_contributed": 3
  },
  "findings_summary": [
    {
      "severity": "high",
      "count": 2,
      "items": ["SQL injection in queries.ts:47", "XSS in render.ts:112"]
    },
    {
      "severity": "medium",
      "count": 5,
      "items": ["..."]
    }
  ],
  "duplicate_work_prevented": {
    "files_skipped": 8,
    "estimated_savings": "$0.024"
  },
  "architecture_insights": [
    "Repository pattern detected in src/db/",
    "Middleware chain in src/api/middleware/"
  ]
}
```

## Querying the Graph

### Search by Label

```
cortivex_knowledge({
  action: "search",
  graph_id: "review-session-1",
  pattern: "auth|login|jwt",
  case_insensitive: true
})
```

### Get All Connections for a Node

```
cortivex_knowledge({
  action: "neighbors",
  graph_id: "review-session-1",
  node_label: "src/auth/login.ts",
  depth: 2
})
```

### Graph Statistics

```
cortivex_knowledge({
  action: "stats",
  graph_id: "review-session-1"
})
```

## KnowledgeCurator Node Reference

```yaml
- id: knowledge
  type: KnowledgeCurator
  config:
    graph_id: my-graph                  # unique identifier for this graph instance
    persist: true                       # save graph to disk between runs
    storage_path: .cortivex/knowledge/  # directory for persisted graphs
    dedup_strategy: content-hash        # content-hash | label-match | none
    merge_interval_seconds: 5           # how often agents sync with the graph
    max_nodes: 10000                    # cap on graph size
    max_edges: 50000                    # cap on edge count
    action: maintain                    # maintain | synthesize | export
    output_format: structured           # structured | markdown | graphml
    skip_known_findings: true           # agents skip files already analyzed
```

## Quick Reference

| Operation | MCP Tool | Description |
|-----------|----------|-------------|
| Create graph | `cortivex_knowledge({ action: "create", graph_id })` | Initialize a new knowledge graph |
| Add knowledge | `cortivex_knowledge({ action: "add", graph_id, nodes, edges })` | Add nodes and edges |
| Query graph | `cortivex_knowledge({ action: "query", graph_id, query })` | Find specific nodes |
| Search graph | `cortivex_knowledge({ action: "search", graph_id, pattern })` | Regex search on labels |
| Check coverage | `cortivex_knowledge({ action: "check_covered", graph_id, files })` | See if files were analyzed |
| Get neighbors | `cortivex_knowledge({ action: "neighbors", graph_id, node_label })` | Find connected nodes |
| Synthesize | `cortivex_knowledge({ action: "synthesize", graph_id })` | Produce unified report |
| Export graph | `cortivex_knowledge({ action: "export", graph_id, format })` | Export as JSON or GraphML |
| Graph stats | `cortivex_knowledge({ action: "stats", graph_id })` | Node/edge counts by type |

## Best Practices

1. **Use a unique graph_id per pipeline run** to keep knowledge from different runs separate.
2. **Enable skip_known_findings** on analysis agents to avoid redundant work and reduce costs.
3. **Set dedup_strategy to content-hash** for the strongest deduplication, especially when agents may phrase findings differently.
4. **Place the KnowledgeCurator as the first node** so all downstream agents can begin reading the graph immediately.
5. **End with a synthesize step** to produce a single unified output rather than merging separate agent reports manually.
6. **Persist graphs across runs** when iterating on the same codebase so agents can build on previous analysis.
7. **Monitor graph size** with the stats action. Graphs over 10,000 nodes may slow down queries.

## Reasoning Protocol

Before interacting with the knowledge graph, reason through:

1. **Am I adding new knowledge or duplicating existing knowledge?** Always query the graph before adding. If a finding already exists (even phrased differently), the dedup strategy will merge, but checking first saves processing time.
2. **Is this finding specific enough to be useful?** "Code has issues" is too vague. "SQL injection in src/db/queries.ts at line 47 via unsanitized user input in the WHERE clause" is actionable. Only add specific, actionable knowledge.
3. **Should I skip this file or analyze it with fresh eyes?** When `check_covered` shows a file was analyzed by another agent, consider whether your analysis focus is different (e.g., SecurityScanner vs CodeReviewer find different things). Same focus = skip. Different focus = analyze.
4. **Is the graph growing too large?** Check `stats` periodically. Graphs over 10,000 nodes slow down queries. If the graph is growing fast, ensure dedup_strategy is working and reduce `max_nodes` if needed.
5. **Am I connecting nodes with appropriate edge types?** Choose the most specific edge type. Use `found_in` for findings, `uses` for code dependencies, `implements` for pattern detection. Do not default to `related_to` for everything.

## Anti-Patterns

| Anti-Pattern | Consequence | Correct Approach |
|-------------|------------|-----------------|
| Adding vague findings | Graph fills with useless nodes that do not inform decisions | Every finding must include: file, line, severity, and specific description |
| Skipping `check_covered` | Multiple agents analyze the same file, wasting cost | Always check coverage before starting analysis on a file |
| Using `related_to` for all edges | Loses semantic meaning; graph becomes a flat list | Use specific edge types: `uses`, `implements`, `depends_on`, `found_in` |
| Not synthesizing at the end | Agents produce separate reports that must be manually merged | Always end with a KnowledgeCurator in `synthesize` mode |
| Same `graph_id` across different pipeline runs | Knowledge from unrelated runs contaminates each other | Use unique `graph_id` per run; use `persist: true` only for iterative work on the same codebase |
| Querying the graph in a tight loop | Performance degradation on large graphs | Batch queries where possible; cache results within your analysis session |

## Grounding Rules

- **Graph returns no results for a file:** The file has not been analyzed yet. Proceed with your analysis and add findings when done.
- **Multiple agents found the same issue:** The CRDT dedup will handle this if `dedup_strategy: content-hash` is configured. If using `label-match`, ensure agents use consistent labels for the same findings.
- **Synthesis produces an empty report:** Verify that agents are configured with `knowledge_graph` pointing to the correct `graph_id`. If agents did not write to the graph, there is nothing to synthesize.
- **Unsure whether to persist the graph:** Persist when you will iterate on the same codebase (nightly reviews, ongoing development). Do not persist for one-off analyses (PR reviews, ad-hoc audits).

## Advanced Capabilities

This section covers advanced usage patterns for CRDT knowledge graphs including semantic querying, knowledge fusion, temporal reasoning, cross-domain inference, and export workflows.

### Semantic Graph Queries

Semantic queries go beyond label matching by traversing the graph structure and filtering on metadata predicates. Use `cortivex_knowledge_query` to issue structured queries with path expressions and semantic filters.

```json
{
  "tool": "cortivex_knowledge_query",
  "request": {
    "graph_id": "review-session-1",
    "query": {
      "select": ["node", "edges", "metadata"],
      "where": {
        "node_type": "finding",
        "metadata.severity": { "$in": ["high", "critical"] },
        "path": { "$traverses": "found_in -> depends_on", "depth": 3 }
      },
      "order_by": "metadata.timestamp",
      "limit": 20
    }
  }
}
```

Response:

```json
{
  "results": [
    {
      "node": { "type": "finding", "label": "SQL injection vulnerability" },
      "edges": [
        { "type": "found_in", "target": "src/db/queries.ts" },
        { "type": "depends_on", "target": "src/api/handlers.ts" }
      ],
      "metadata": { "severity": "critical", "agent": "agent-security-scanner-1", "timestamp": "2026-03-23T10:04:12Z" }
    }
  ],
  "total": 1,
  "traversal_depth_reached": 2
}
```

### Knowledge Fusion & Deduplication

When multiple agents report overlapping findings, the knowledge curator merges them using configurable strategies. The merge strategy determines how conflicting metadata is resolved and when two nodes are considered duplicates.

```yaml
knowledge_fusion:
  dedup_strategies:
    content-hash:
      algorithm: sha256
      fields: [type, label, "metadata.file", "metadata.line"]
      collision_action: merge_metadata
    semantic-similarity:
      model: embedding-v2
      threshold: 0.92
      merge_policy: keep_highest_confidence
    label-match:
      normalization: [lowercase, strip_whitespace, remove_punctuation]
      match_threshold: 0.85

  merge_rules:
    metadata_conflict: last_write_wins
    severity_conflict: highest_severity_wins
    edge_duplicates: union
    provenance_tracking: true
    max_merge_candidates: 50

  agent_priority:
    - agent_type: SecurityScanner
      weight: 1.0
    - agent_type: CodeReviewer
      weight: 0.8
    - agent_type: BugHunter
      weight: 0.9
```

### Temporal Reasoning & Version History

The CRDT graph retains a full version history for every node, enabling temporal queries that reconstruct the graph state at any past point. Use temporal predicates to track how knowledge evolved during a pipeline run.

```json
{
  "$schema": "https://cortivex.dev/schemas/temporal-query/v1.json",
  "type": "object",
  "properties": {
    "graph_id": { "type": "string" },
    "temporal": {
      "type": "object",
      "properties": {
        "mode": {
          "type": "string",
          "enum": ["snapshot", "diff", "timeline"]
        },
        "at": {
          "type": "string",
          "format": "date-time",
          "description": "ISO 8601 timestamp for snapshot mode"
        },
        "from": {
          "type": "string",
          "format": "date-time",
          "description": "Start of range for diff and timeline modes"
        },
        "to": {
          "type": "string",
          "format": "date-time",
          "description": "End of range for diff and timeline modes"
        },
        "node_filter": {
          "type": "object",
          "properties": {
            "type": { "type": "string" },
            "label_pattern": { "type": "string" }
          }
        }
      },
      "required": ["mode"]
    }
  },
  "required": ["graph_id", "temporal"]
}
```

A diff query returns nodes added, modified, and superseded between two timestamps, enabling agents to process only incremental changes rather than re-reading the entire graph.

### Cross-Domain Inference Patterns

The `cortivex_knowledge_infer` tool derives new edges and findings by applying inference rules across disjoint subgraphs. This enables agents to detect patterns that span security, architecture, and performance domains.

```json
{
  "tool": "cortivex_knowledge_infer",
  "request": {
    "graph_id": "review-session-1",
    "rules": [
      {
        "name": "transitive_dependency_risk",
        "when": {
          "pattern": "(finding:high)-[:found_in]->(A)-[:depends_on*1..3]->(B)",
          "condition": "B.metadata.public_api == true"
        },
        "then": {
          "create_edge": { "type": "risk_propagation", "source": "A", "target": "B" },
          "create_finding": {
            "type": "finding",
            "label": "Transitive risk: high-severity issue reachable from public API",
            "metadata": { "severity": "critical", "inferred": true }
          }
        }
      }
    ]
  }
}
```

Response:

```json
{
  "inferences_created": 2,
  "new_edges": [
    { "type": "risk_propagation", "source": "src/db/queries.ts", "target": "src/api/public/users.ts" }
  ],
  "new_findings": [
    {
      "label": "Transitive risk: high-severity issue reachable from public API",
      "metadata": { "severity": "critical", "inferred": true, "source_finding": "SQL injection vulnerability", "path_length": 2 }
    }
  ]
}
```

### Knowledge Export & Visualization

Export the knowledge graph in various formats for downstream consumption, external tooling integration, or visual rendering. The export format configuration schema controls output structure, filtering, and layout hints.

```json
{
  "$schema": "https://cortivex.dev/schemas/export-config/v1.json",
  "type": "object",
  "properties": {
    "graph_id": { "type": "string" },
    "format": {
      "type": "string",
      "enum": ["json", "graphml", "dot", "cytoscape", "d3-force"]
    },
    "filters": {
      "type": "object",
      "properties": {
        "node_types": { "type": "array", "items": { "type": "string" } },
        "min_severity": { "type": "string", "enum": ["low", "medium", "high", "critical"] },
        "agents": { "type": "array", "items": { "type": "string" } },
        "include_inferred": { "type": "boolean", "default": true }
      }
    },
    "layout": {
      "type": "object",
      "properties": {
        "algorithm": { "type": "string", "enum": ["force-directed", "hierarchical", "radial"] },
        "cluster_by": { "type": "string", "enum": ["node_type", "agent", "directory", "severity"] },
        "collapse_threshold": { "type": "integer", "description": "Collapse clusters with more nodes than this into a summary node" }
      }
    }
  },
  "required": ["graph_id", "format"]
}
```

To trigger an export via the MCP tool:

```typescript
const exportResult = await cortivex_knowledge({
  action: "export",
  graph_id: "review-session-1",
  format: "d3-force",
  filters: {
    node_types: ["finding", "entity"],
    min_severity: "medium",
    include_inferred: true,
  },
  layout: {
    algorithm: "force-directed",
    cluster_by: "severity",
    collapse_threshold: 15,
  },
});
// exportResult.output_path: ".cortivex/knowledge/exports/review-session-1.json"
// exportResult.node_count: 34
// exportResult.edge_count: 61
```

## Security Hardening (OWASP AST10 Aligned)

This section defines security controls for the knowledge graph layer, mapped to the OWASP Agentic Security Threats (AST) taxonomy. These controls protect against data leakage, cross-run contamination, and uncontrolled retention of sensitive information within CRDT knowledge graphs.

### AST09: Data Classification for Knowledge Graph Entries

Every node added to the knowledge graph MUST carry a data classification label. This addresses AST09 (Insufficient Logging and Monitoring) by ensuring that sensitive data is tracked, access-controlled, and auditable throughout its lifecycle in the graph.

```yaml
# knowledge-classification.yaml — AST09 Data Classification
data_classification:
  ast09_compliance: true
  enforce_on_add: true  # reject nodes without a classification label
  default_classification: "internal"  # fallback if agent omits label

  levels:
    - name: "public"
      description: "Non-sensitive findings safe for external reports"
      access: "all_agents"
      export_allowed: true
      retention_days: 365

    - name: "internal"
      description: "Standard findings for pipeline-internal use"
      access: "pipeline_agents_only"
      export_allowed: true
      export_requires_approval: false
      retention_days: 90

    - name: "restricted"
      description: "Sensitive findings containing secrets, PII, or security vulnerabilities"
      access: "originating_agent_and_coordinator"
      export_allowed: false
      export_requires_approval: true
      retention_days: 30
      redact_in_synthesis: true  # replace with placeholder in synthesized reports
      audit_all_access: true     # AST09: log every read of restricted nodes

  classification_rules:
    - match:
        metadata_contains: ["password", "secret", "token", "api_key", "credential"]
      auto_classify: "restricted"
    - match:
        metadata_contains: ["ssn", "social_security", "credit_card", "pii"]
      auto_classify: "restricted"
    - match:
        severity: ["critical", "high"]
        type: "finding"
      auto_classify: "internal"
    - match:
        type: "concept"
      auto_classify: "public"
```

Apply classification when adding nodes via MCP:

```json
{
  "tool": "cortivex_knowledge",
  "request": {
    "action": "add",
    "graph_id": "review-session-1",
    "nodes": [
      {
        "type": "finding",
        "label": "Hardcoded API key in config.ts",
        "classification": "restricted",
        "metadata": {
          "file": "src/config.ts",
          "line": 12,
          "severity": "critical",
          "agent": "agent-security-scanner-1"
        }
      }
    ],
    "ast_risk_id": "AST09",
    "enforce_classification": true
  }
}
```

### Export Controls with Approval Workflow

Knowledge graph exports MUST enforce classification-based access controls. Exporting restricted data to external formats (JSON, GraphML, d3-force) requires explicit approval from the pipeline coordinator. This prevents unauthorized data exfiltration from the knowledge graph.

```json
{
  "$schema": "https://cortivex.dev/schemas/export-controls/v1.json",
  "type": "object",
  "required": ["export_policy"],
  "properties": {
    "export_policy": {
      "type": "object",
      "properties": {
        "public_data": {
          "type": "object",
          "properties": {
            "allowed_formats": { "type": "array", "items": { "type": "string" } },
            "require_approval": { "type": "boolean", "default": false },
            "auto_redact_restricted": { "type": "boolean", "default": true }
          }
        },
        "internal_data": {
          "type": "object",
          "properties": {
            "allowed_formats": { "type": "array", "items": { "type": "string" } },
            "require_approval": { "type": "boolean", "default": false },
            "strip_agent_ids": { "type": "boolean", "default": false }
          }
        },
        "restricted_data": {
          "type": "object",
          "properties": {
            "allowed_formats": { "type": "array", "items": { "type": "string" } },
            "require_approval": { "type": "boolean", "default": true },
            "approval_roles": {
              "type": "array",
              "items": { "type": "string" },
              "default": ["coordinator", "pipeline_owner"]
            },
            "audit_export": { "type": "boolean", "default": true }
          }
        },
        "blocked_destinations": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Paths or URLs where exports are never allowed"
        }
      }
    }
  }
}
```

Request an approved export via MCP:

```json
{
  "tool": "cortivex_knowledge",
  "request": {
    "action": "export",
    "graph_id": "review-session-1",
    "format": "json",
    "include_restricted": true,
    "approval_token": "approval-tx-5f3e2d1c",
    "ast_risk_id": "AST09",
    "audit_export": true
  }
}
```

### PII and Secret Filtering Before Graph Persistence

Before any knowledge node is persisted to disk, a filtering pass MUST scan for PII and secrets. Nodes containing detected sensitive content are either redacted, reclassified as restricted, or rejected entirely. This prevents secrets from leaking into persisted graph storage.

```yaml
# pii-secret-filter.yaml
pii_secret_filter:
  enabled: true
  apply_on: ["persist", "export", "synthesize"]

  secret_patterns:
    - name: api_key_generic
      pattern: "(?i)(api[_-]?key|apikey)\\s*[:=]\\s*['\"]?[a-zA-Z0-9_\\-]{20,}"
      action: redact
    - name: private_key_pem
      pattern: "-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"
      action: reject
    - name: github_token
      pattern: "gh[ps]_[a-zA-Z0-9]{36,}"
      action: redact
    - name: aws_access_key
      pattern: "AKIA[0-9A-Z]{16}"
      action: redact
    - name: jwt_token
      pattern: "eyJ[a-zA-Z0-9_-]{10,}\\.eyJ[a-zA-Z0-9_-]{10,}\\.[a-zA-Z0-9_-]+"
      action: redact

  pii_patterns:
    - name: email_address
      pattern: "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"
      action: hash_and_classify_restricted
    - name: phone_number
      pattern: "\\+?[1-9]\\d{1,14}"
      action: hash_and_classify_restricted
    - name: ssn
      pattern: "\\b\\d{3}-\\d{2}-\\d{4}\\b"
      action: reject  # never persist SSNs

  redaction_config:
    replacement: "[REDACTED:{pattern_name}]"
    preserve_metadata: true  # keep file, line, severity — only redact the sensitive value
    log_redactions: true     # AST09: audit every redaction event
```

Trigger a manual filter scan on an existing graph:

```json
{
  "tool": "cortivex_knowledge",
  "request": {
    "action": "scan_and_filter",
    "graph_id": "review-session-1",
    "filter_config": "pii-secret-filter.yaml",
    "dry_run": false,
    "ast_risk_id": "AST09"
  }
}
```

### Graph Isolation Between Pipeline Runs

Knowledge graphs MUST be isolated between pipeline runs to prevent cross-contamination. A graph from pipeline run A must never be readable or writable by pipeline run B unless explicitly linked through a controlled inheritance mechanism. This prevents data leakage across security boundaries.

```yaml
# graph-isolation.yaml
graph_isolation:
  policy: strict  # strict | shared | inherited
  enforce_run_boundary: true

  strict_mode:
    graph_id_includes_run_id: true  # graph_id = "{user_graph_id}-{run_id}"
    cross_run_read: deny
    cross_run_write: deny
    storage_path_isolation: true    # each run gets its own subdirectory
    cleanup_on_pipeline_end: true

  inherited_mode:
    # Only used when policy is "inherited" — allows controlled read from parent
    allow_read_from_parent: true
    allow_write_to_parent: false
    parent_run_id: null             # must be explicitly set
    inherit_classification_labels: true
    inherit_restricted_nodes: false  # never inherit restricted data

  enforcement:
    reject_cross_run_queries: true
    audit_cross_run_attempts: true  # AST09: log any attempt to access another run's graph
    on_violation: "deny_and_log"
```

Verify isolation at pipeline start:

```typescript
interface GraphIsolationCheck {
  tool: "cortivex_knowledge";
  request: {
    action: "verify_isolation";
    graph_id: string;
    run_id: string;
    expected_policy: "strict" | "shared" | "inherited";
    reject_if_contaminated: boolean;  // abort if graph has data from other runs
    ast_risk_ids: ["AST09"];
  };
}
```

```json
{
  "tool": "cortivex_knowledge",
  "request": {
    "action": "verify_isolation",
    "graph_id": "review-session-1",
    "run_id": "ctx-a1b2c3",
    "expected_policy": "strict",
    "reject_if_contaminated": true,
    "ast_risk_ids": ["AST09"]
  }
}
```

### Temporal Data Retention with Mandatory Expiry

All knowledge graph data MUST have a mandatory expiry policy. Graphs that exceed their retention period are automatically purged. No indefinite retention is permitted for graphs containing internal or restricted data. This limits the blast radius of any data breach involving persisted graph storage.

```yaml
# retention-policy.yaml
temporal_retention:
  enabled: true
  enforce_mandatory_expiry: true

  policies:
    - classification: "public"
      max_retention_days: 365
      auto_purge: true
      archive_before_purge: true
      archive_format: "compressed_jsonl"

    - classification: "internal"
      max_retention_days: 90
      auto_purge: true
      archive_before_purge: false
      warn_before_purge_days: 7

    - classification: "restricted"
      max_retention_days: 30
      auto_purge: true
      archive_before_purge: false  # restricted data is never archived
      secure_delete: true          # overwrite storage, not just unlink
      warn_before_purge_days: 3

  graph_level_expiry:
    max_graph_age_days: 180        # absolute maximum regardless of classification
    max_graph_size_nodes: 50000    # force purge if graph exceeds size limit
    idle_expiry_days: 30           # purge if no reads or writes for 30 days

  audit:
    log_all_purges: true           # AST09: audit every purge event
    log_retention_overrides: true  # log if anyone extends retention
    retention_override_requires: "pipeline_owner"
```

Check retention status and upcoming expirations:

```json
{
  "tool": "cortivex_knowledge",
  "request": {
    "action": "retention_status",
    "graph_id": "review-session-1",
    "include_expiring_soon": true,
    "expiry_horizon_days": 7,
    "ast_risk_id": "AST09"
  }
}
```

Response:

```json
{
  "graph_id": "review-session-1",
  "created_at": "2026-03-10T08:00:00Z",
  "last_accessed_at": "2026-03-24T14:30:00Z",
  "retention_policy": "internal",
  "expires_at": "2026-06-08T08:00:00Z",
  "nodes_expiring_within_7_days": 3,
  "restricted_nodes_count": 5,
  "restricted_earliest_expiry": "2026-04-09T08:00:00Z",
  "purge_scheduled": false,
  "ast_risk_id": "AST09"
}
