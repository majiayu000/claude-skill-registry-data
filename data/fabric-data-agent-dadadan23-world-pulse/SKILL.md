---
name: "fabric-data-agent"
description: 'Build, configure, and validate conversational data agents on Microsoft Fabric Lakehouses using the Data Agent SDK. Use when creating Fabric data agents, configuring few-shot examples, managing Livy sessions, or validating agent responses against Lakehouse data.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-07-13"
 updated: "2025-07-13"
compatibility:
 languages: ["python", "sql", "pyspark"]
 frameworks: ["microsoft-fabric", "fabric-data-agent-sdk"]
 platforms: ["windows", "linux", "macos"]
prerequisites:
 - "Microsoft Fabric workspace with active capacity"
 - "Fabric MCP Server (ms-fabric-mcp-server)"
 - "fabric-data-agent-sdk (pre-installed in Fabric environment)"
 - "Lakehouse with populated Delta tables"
---

# Fabric Data Agent

> Build conversational data agents that answer natural language questions against Fabric Lakehouses.

## When to Use

- Creating a natural language query interface over Lakehouse data
- Building self-service analytics agents for business users
- Configuring a Data Agent with table selection, joins, and measures
- Validating agent accuracy against known metrics
- Generating reproducible notebooks for agent provisioning

## Decision Tree

```
Building a Fabric Data Agent?
+- First time with this Lakehouse?
| - Start at Phase 1 (Plan) - discover schema and relationships
+- Have an implementation plan already?
| - Start at Phase 2 (Create) - build and publish the agent
+- Agent exists but needs validation?
| - Start at Phase 3 (Validate) - test against expected metrics
+- Need to modify an existing agent?
| +- Schema changes -> Re-run Phase 1 (new plan)
| - Config tweaks -> Phase 2 only (update agent)
- Not sure if Data Agent is right tool?
 +- Users need ad-hoc SQL -> Use Warehouse + SQL endpoint instead
 +- Users need dashboards -> Use Semantic Model + Power BI
 - Users need chat-based Q&A -> Data Agent [PASS]
```

## Workflow Overview

Data Agent development follows a **3-phase workflow** with checkpoint stops between phases:

```
Phase 1: Plan --checkpoint---> Phase 2: Create --checkpoint---> Phase 3: Validate
```

**Critical Rule**: Execute ONE phase per conversation turn to prevent context rot. Use the completion report as a handover document between phases.

### Phase 1: Plan

**Goal**: Analyze the Lakehouse to produce a comprehensive implementation plan.

| Step | Action | Output |
|------|--------|--------|
| 1 | Gather inputs (workspace, lakehouse name, scope) | User requirements |
| 2 | Discover tables and row counts via SQL endpoint | Table inventory |
| 3 | Identify primary/foreign keys and relationships | Relationship map |
| 4 | Calculate baseline metrics for validation | Expected values |
| 5 | Generate implementation plan document | `implementation_plan.md` |

**Checkpoint**: Present plan summary, get user approval before proceeding.

### Phase 2: Create

**Goal**: Execute the plan to create and publish a configured Data Agent.

| Step | Action | Output |
|------|--------|--------|
| 1 | Initialize the Data Agent Management Client | SDK connection |
| 2 | Create agent with name and description | Agent instance |
| 3 | Configure instructions (system prompt for the agent) | Agent knowledge |
| 4 | Add Lakehouse datasources and select tables | Data bindings |
| 5 | Add few-shot examples for common queries | Query templates |
| 6 | Publish the agent | Live agent |
| 7 | Generate reproducible notebook | `agent_creation.ipynb` |

**Checkpoint**: Confirm agent is published and accessible before validation.

### Phase 3: Validate

**Goal**: Verify agent accuracy against the metrics from Phase 1.

| Step | Action | Output |
|------|--------|--------|
| 1 | Initialize the Query Client | SDK connection |
| 2 | Execute test queries from the plan | Query responses |
| 3 | Compare actual vs expected values | Accuracy metrics |
| 4 | Generate validation report | `validation_report.md` |
| 5 | Generate reproducible notebook | `agent_validation.ipynb` |

**Checkpoint**: Present accuracy results and recommendations.

## Core Concepts

### Data Agent Architecture

```
User Question (natural language)
 (down)
Data Agent (instructions + knowledge)
 (down)
SQL Generation (against Lakehouse SQL endpoint)
 (down) 
Query Execution
 (down)
Natural Language Answer
```

### Agent Configuration Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Instructions** | System prompt guiding agent behavior | "You are a sales analytics assistant..." |
| **Datasources** | Lakehouse bindings with table selection | Bronze_LH: [fact_sales, dim_product, ...] |
| **Few-shot examples** | Query-answer pairs for accuracy | Q: "Total sales?" -> SQL: `SELECT SUM(amount)...` |
| **Knowledge** | Additional context documents | Business rules, glossary, KPIs |

### Table Selection Strategy

| Include | Exclude |
|---------|---------|
| Gold-layer fact and dimension tables | Bronze/Silver raw tables |
| Tables with clear business meaning | System/metadata tables |
| Tables with documented relationships | Temp/staging tables |
| Tables referenced in business KPIs | Large log/event tables |

## Few-Shot Example Best Practices

Few-shot examples teach the agent how to generate correct SQL:

### SQL Syntax (Fabric SQL Endpoint = T-SQL)

| Correct (T-SQL) | Incorrect (Spark SQL) |
|-----------------|----------------------|
| `SELECT TOP 10` | `LIMIT 10` |
| `DATEPART(QUARTER, date)` | `QUARTER(date)` |
| `FORMAT(date, 'yyyy-MM')` | `DATE_FORMAT(date, '%Y-%m')` |
| `CONVERT(DATE, value)` | `CAST(value AS DATE)` |
| `ISNULL(col, default)` | `COALESCE(col, default)` |

### Example Quality Checklist

- [ ] Covers the top 10 most common business questions
- [ ] Uses correct T-SQL syntax (not Spark SQL)
- [ ] Includes aggregations (SUM, COUNT, AVG)
- [ ] Includes time-based filters (YTD, MTD, date ranges)
- [ ] Includes joins across fact and dimension tables
- [ ] All examples validated against SQL endpoint before adding
- [ ] Covers edge cases (nulls, empty results, large numbers)

## Livy Session Management

When using Livy for SDK operations (Phase 2 & 3):

```
1. Always check for existing sessions FIRST
2. Reuse idle sessions (state: idle -> reuse)
3. Create only if none exist (cold start: 3-6+ minutes)
4. Never close sessions unless explicitly requested
5. Use timestamped session names: data-agent-{lakehouse}-{timestamp}
6. Check session status before submitting statements
```

## Error Handling

### Retry Protocol

```
Attempt 1 -> Execute operation
 (down) (on failure)
Attempt 2 -> Diagnose error, apply fix, retry
 (down) (on failure)
Attempt 3 -> Try alternative approach
 (down) (on failure)
Escalate to user with error details + options
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|---------|
| Agent creation fails | SDK initialization issue | Verify workspace access and SDK version |
| Table not found in agent | Table not in selected scope | Re-add datasource with correct table list |
| Query returns wrong results | Incorrect few-shot SQL syntax | Validate SQL against endpoint first |
| Session timeout | Livy cold start | Increase timeout, reuse existing sessions |
| Permission denied | Workspace role insufficient | Need Contributor or higher role |

## Output Artifacts

All output goes to timestamped folders:

```
run/{timestamp}_{lakehouse}/
+-- implementation_plan.md # Phase 1 output
+-- agent_creation.ipynb # Phase 2 reproducible notebook
+-- agent_validation.ipynb # Phase 3 reproducible notebook
+-- validation_report.md # Phase 3 accuracy results
-- completion_report.md # Cross-phase handover document
```

## Anti-Patterns

- **Skip planning phase**: Creating agents without understanding schema -> poor accuracy
- **Use Bronze tables**: Raw data with duplicates/nulls -> unreliable answers
- **Spark SQL in few-shots**: Agent generates invalid SQL -> query failures
- **No validation**: Deploying without testing -> users lose trust quickly
- **Monolithic instructions**: Long, unfocused system prompts -> agent confusion
- **Too many tables**: Adding all tables -> slow queries, irrelevant joins

## Boundaries

### Always Do

- Gather workspace and lakehouse inputs before starting
- Discover and verify schema before creating agent
- Validate all few-shot SQL against the SQL endpoint
- Get user approval at checkpoint between phases
- Generate reproducible notebooks for all SDK operations
- Use timestamped output folders (never overwrite)
- Document decisions in completion report

### Ask First

- Creating new Data Agents (confirm name and scope)
- Running expensive queries on large tables
- Modifying existing agent configurations
- Any operation that affects production data

### Never Do

- Proceed without required inputs (workspace, lakehouse)
- Execute modifications without user approval
- Delete Data Agents without confirmation
- Hardcode credentials or connection strings
- Assume table relationships without verification
- Include unvalidated SQL in few-shot examples
- Close Livy sessions that were already open

## Reference Index

| Document | Description |
|----------|-------------|
| [references/agent-sdk-patterns.md](references/agent-sdk-patterns.md) | Data Agent SDK code patterns and API reference |
| [references/instruction-templates.md](references/instruction-templates.md) | System prompt templates for different domains |

## Asset Templates

| File | Description |
|------|-------------|
| [assets/completion-report-template.md](assets/completion-report-template.md) | Cross-phase handover document template |
| [assets/sample-few-shot-queries.sql](assets/sample-few-shot-queries.sql) | Example few-shot query templates |
