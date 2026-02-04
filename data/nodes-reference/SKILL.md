---
name: nodes-reference
description: "Comprehensive node reference documentation for all 110+ Kailash SDK nodes organized by category: AI, API, Code, Data, Database, File, Logic, Monitoring, Admin, Transaction, and Transform nodes. Use when asking about 'node reference', 'available nodes', 'node list', 'AI nodes', 'API nodes', 'code nodes', 'data nodes', 'database nodes', 'file nodes', 'logic nodes', 'monitoring nodes', 'transaction nodes', 'transform nodes', 'which nodes', 'node documentation', or 'node capabilities'."
---

# Kailash Nodes - Complete Reference

Comprehensive reference documentation for all 110+ workflow nodes in Kailash SDK, organized by category.

## Overview

Complete node catalog covering:
- **AI Nodes**: LLM, vision, audio, embeddings
- **API Nodes**: HTTP, webhooks, GraphQL
- **Code Nodes**: Python, JavaScript execution
- **Data Nodes**: Processing, transformation, validation
- **Database Nodes**: CRUD, queries, transactions
- **File Nodes**: Reading, writing, manipulation
- **Logic Nodes**: Conditionals, loops, routing
- **Monitoring Nodes**: Logging, metrics, alerts
- **Admin Nodes**: System management
- **Transaction Nodes**: ACID operations
- **Transform Nodes**: Data transformation

## Node Reference Documentation

### Quick Access
- **[nodes-quick-index](nodes-quick-index.md)** - Quick node lookup index

### By Category

#### AI & Machine Learning
- **[nodes-ai-reference](nodes-ai-reference.md)** - AI and LLM nodes
  - LLMNode, AnthropicNode, OpenAINode
  - VisionNode, AudioNode
  - EmbeddingNode, ClassificationNode
  - OllamaNode (local LLMs)

#### API & Integration
- **[nodes-api-reference](nodes-api-reference.md)** - API integration nodes
  - APICallNode, HTTPRequestNode
  - WebhookNode, GraphQLNode
  - RESTClientNode, SOAPNode

#### Code Execution
- **[nodes-code-reference](nodes-code-reference.md)** - Code execution nodes
  - PythonCodeNode (primary)
  - JavaScriptNode, BashNode
  - CodeEvalNode, ScriptNode

#### Data Processing
- **[nodes-data-reference](nodes-data-reference.md)** - Data processing nodes
  - CSVReaderNode, CSVWriterNode
  - JSONParserNode, XMLParserNode
  - DataValidatorNode, DataTransformNode
  - FilterNode, MapNode, ReduceNode

#### Database Operations
- **[nodes-database-reference](nodes-database-reference.md)** - Database nodes
  - SQLQueryNode, AsyncSQLNode
  - DatabaseReadNode, DatabaseWriteNode
  - TransactionNode, BulkInsertNode
  - (Plus DataFlow auto-generated nodes)

#### File Operations
- **[nodes-file-reference](nodes-file-reference.md)** - File system nodes
  - FileReaderNode, FileWriterNode
  - DirectoryReaderNode, DirectoryCreatorNode
  - FileWatcherNode, FileCopyNode
  - ZipNode, UnzipNode

#### Logic & Control Flow
- **[nodes-logic-reference](nodes-logic-reference.md)** - Logic and routing nodes
  - SwitchNode (conditional routing)
  - IfElseNode, LoopNode
  - MergeNode, SplitNode
  - DelayNode, TimeoutNode
  - CycleNode (cyclic workflows)

#### Monitoring & Observability
- **[nodes-monitoring-reference](nodes-monitoring-reference.md)** - Monitoring nodes
  - LoggerNode, MetricsNode
  - AlertNode, HealthCheckNode
  - TracingNode, AuditNode

#### Admin & Management
- **[nodes-admin-reference](nodes-admin-reference.md)** - Admin nodes
  - ConfigNode, SecretManagerNode
  - EnvironmentNode, SchedulerNode
  - CacheNode, QueueNode

#### Transactions
- **[nodes-transaction-reference](nodes-transaction-reference.md)** - Transaction nodes
  - TransactionBeginNode, TransactionCommitNode
  - SagaNode, CompensateNode
  - TwoPhaseCommitNode

#### Data Transformation
- **[nodes-transform-reference](nodes-transform-reference.md)** - Transform nodes
  - MapperNode, AggregatorNode
  - EnrichNode, NormalizeNode
  - FormatNode, ConvertNode

## Node Selection Guide

### By Use Case

**AI & LLM Tasks** → Use AI nodes (`nodes-ai-reference`)
- Text generation: LLMNode, OpenAINode, AnthropicNode
- Vision: VisionNode
- Audio: AudioNode
- Local LLMs: OllamaNode

**API Integration** → Use API nodes (`nodes-api-reference`)
- REST APIs: APICallNode, HTTPRequestNode
- Webhooks: WebhookNode
- GraphQL: GraphQLNode

**Custom Logic** → Use Code nodes (`nodes-code-reference`)
- Python: PythonCodeNode (recommended)
- JavaScript: JavaScriptNode
- Shell: BashNode

**Database Work** → Use Database nodes (`nodes-database-reference`)
- SQL queries: SQLQueryNode, AsyncSQLNode
- CRUD with DataFlow: Auto-generated nodes

**File Operations** → Use File nodes (`nodes-file-reference`)
- Reading files: FileReaderNode
- Bulk operations: DirectoryReaderNode
- File watching: FileWatcherNode

**Conditional Logic** → Use Logic nodes (`nodes-logic-reference`)
- Simple conditions: SwitchNode
- Complex routing: IfElseNode
- Loops: LoopNode, CycleNode

**Data Processing** → Use Data nodes (`nodes-data-reference`)
- CSV: CSVReaderNode, CSVWriterNode
- JSON: JSONParserNode
- Validation: DataValidatorNode

**Monitoring** → Use Monitoring nodes (`nodes-monitoring-reference`)
- Logging: LoggerNode
- Metrics: MetricsNode
- Alerts: AlertNode

## Critical Node Patterns

### String-Based API
```python
workflow.add_node("PythonCodeNode", "node1", {
    "code": "result = input_data * 2"
})
```

### Parameter Passing
```python
workflow.add_connection("node1", "result", "node2", "input_data")
```

### Common Nodes
- **PythonCodeNode**: Most flexible, use for custom logic
- **SwitchNode**: Conditional routing based on values
- **CSVReaderNode**: Reading CSV files
- **APICallNode**: HTTP API calls
- **LoggerNode**: Debug and production logging

## When to Use This Skill

Use this skill when you need to:
- Find the right node for a task
- Understand node capabilities
- Look up node parameters
- See node usage examples
- Compare similar nodes
- Explore available nodes by category

## Related Skills

- **[01-core-sdk](../../01-core-sdk/SKILL.md)** - Core workflow patterns
- **[06-cheatsheets](../cheatsheets/SKILL.md)** - Node usage patterns
- **[07-development-guides](../development-guides/SKILL.md)** - Custom node development
- **[02-dataflow](../../02-dataflow/SKILL.md)** - Auto-generated database nodes

## Support

For node-related questions, invoke:
- `pattern-expert` - Node pattern recommendations
- `sdk-navigator` - Find specific nodes
- `dataflow-specialist` - DataFlow-generated nodes
