---
name: dataflow
description: "Kailash DataFlow - zero-config database framework with automatic model-to-node generation. Use when asking about 'database operations', 'DataFlow', 'database models', 'CRUD operations', 'bulk operations', 'database queries', 'database migrations', 'multi-tenancy', 'multi-instance', 'database transactions', 'PostgreSQL', 'MySQL', 'SQLite', 'MongoDB', 'pgvector', 'vector search', 'document database', 'RAG', 'semantic search', 'existing database', 'database performance', 'database deployment', 'database testing', or 'TDD with databases'. DataFlow is NOT an ORM - it generates 11 workflow nodes per SQL model, 8 nodes for MongoDB, and 3 nodes for vector operations."
---

# Kailash DataFlow - Zero-Config Database Framework

DataFlow is a zero-config database framework built on Kailash Core SDK that automatically generates workflow nodes from database models.

## Overview

DataFlow transforms database models into workflow nodes automatically, providing:

- **Automatic Node Generation**: 11 nodes per model (@db.model decorator)
- **Multi-Database Support**: PostgreSQL, MySQL, SQLite (SQL) + MongoDB (Document) + pgvector (Vector Search)
- **Enterprise Features**: Multi-tenancy, multi-instance isolation, transactions
- **Zero Configuration**: String IDs preserved, deferred schema operations
- **Integration Ready**: Works with Nexus for multi-channel deployment
- **Specialized Adapters**: SQL (11 nodes/model), Document (8 nodes), Vector (3 nodes)
L
## 🛠️ Developer Experience Tools

### Enhanced Error System

DataFlow provides comprehensive error enhancement across all database operations, strict mode validation for build-time error prevention, and an intelligent debug agent for automated error diagnosis.

#### Error Enhancement

**What It Is**: Automatic transformation of Python exceptions into rich, actionable error messages with context, root causes, and solutions.

**All DataFlow errors include**:
- **Error codes**: DF-XXX format (DataFlow) or KS-XXX (Core SDK)
- **Context**: Node, parameters, workflow state
- **Root causes**: Why the error occurred (3-5 possibilities with probability scores)
- **Solutions**: How to fix it (with code examples)

**Example**:
```python
# Missing parameter error shows:
# - Error Code: DF-101
# - Missing parameter: "id"
# - 3 solutions with code examples
# - Link to documentation

workflow.add_node("UserCreateNode", "create", {
    "name": "Alice"  # Missing "id" - error enhanced automatically
})
```

**Error Categories**:
- **DF-1XX**: Parameter errors (missing, type mismatch, validation)
- **DF-2XX**: Connection errors (missing, circular, type mismatch)
- **DF-3XX**: Migration errors (schema, constraints)
- **DF-4XX**: Configuration errors (database URL, auth)
- **DF-5XX**: Runtime errors (timeouts, resources)

**Architecture**:
```python
# BaseErrorEnhancer - Shared abstraction
# ├─ CoreErrorEnhancer - KS-501 to KS-508 (Core SDK)
# └─ DataFlowErrorEnhancer - DF-XXX codes (DataFlow)
```

#### Strict Mode Validation

**What It Is**: Build-time validation system with 4 layers to catch errors before workflow execution.

**Validation Layers**:
1. **Model Validation** - Primary keys, auto-fields, reserved fields, field types
2. **Parameter Validation** - Required parameters, types, values, CreateNode structure
3. **Connection Validation** - Source/target nodes, type compatibility, dot notation
4. **Workflow Validation** - Structure, circular dependencies

**Configuration**:
```python
from dataflow import DataFlow
from dataflow.validation.strict_mode import StrictModeConfig

config = StrictModeConfig(
    enabled=True,
    validate_models=True,
    validate_parameters=True,
    validate_connections=True,
    validate_workflows=True,
    fail_fast=True,   # Stop on first error
    verbose=False     # Minimal output
)

db = DataFlow("postgresql://...", strict_mode_config=config)
```

**When to Use**:
- ✅ Development: Catch errors early
- ✅ CI/CD: Validate workflows before deployment
- ✅ Production: Prevent invalid workflow execution

**Documentation**:
- HOW-TO Guide: [`dataflow-strict-mode`](dataflow-strict-mode.md)
- Architecture Guide: [`dataflow-validation-layers`](dataflow-validation-layers.md)

#### Debug Agent

**What It Is**: Intelligent error analysis system that automatically diagnoses errors and provides ranked, actionable solutions.

**5-Stage Pipeline**:
1. **Capture** - Stack traces, context, error chains
2. **Categorize** - 50+ patterns across 5 categories (PARAMETER, CONNECTION, MIGRATION, RUNTIME, CONFIGURATION)
3. **Analyze** - Inspector integration for workflow analysis
4. **Suggest** - 60+ solution templates with relevance scoring
5. **Format** - CLI (color-coded), JSON (machine-readable), dict (programmatic)

**Usage**:
```python
from dataflow.debug.debug_agent import DebugAgent
from dataflow.debug.knowledge_base import KnowledgeBase
from dataflow.platform.inspector import Inspector

# Initialize once (singleton pattern)
kb = KnowledgeBase("patterns.yaml", "solutions.yaml")
inspector = Inspector(db)
debug_agent = DebugAgent(kb, inspector)

# Debug errors automatically
try:
    runtime.execute(workflow.build())
except Exception as e:
    report = debug_agent.debug(e, max_solutions=5, min_relevance=0.3)
    print(report.to_cli_format())  # Rich terminal output
```

**Output Formats**:
```python
# CLI format (color-coded, ANSI)
print(report.to_cli_format())

# JSON format (machine-readable)
json_output = report.to_json()

# Dictionary format (programmatic)
data = report.to_dict()
```

**Performance**: 5-50ms per error, 92%+ confidence for known patterns

**Documentation**:
- Skill Guide: [`dataflow-debug-agent`](dataflow-debug-agent.md)
- User Guide: `docs/guides/debug-agent-user-guide.md`
- Developer Guide: `docs/guides/debug-agent-developer-guide.md`

---

### Build-Time Validation: Catch Errors Early
**Validation Modes**: OFF, WARN (default), STRICT

Catch 80% of configuration errors at model registration time (not runtime):

```python
from dataflow import DataFlow

db = DataFlow("postgresql://...")

# Default: Warn mode (backward compatible)
@db.model
class User:
    id: int  # Validates: primary key named 'id'
    name: str
    email: str

# Strict mode: Raises errors on validation failures
@db.model(strict=True)
class Product:
    id: int
    name: str
    price: float

# Skip validation (advanced users)
@db.model(skip_validation=True)
class Advanced:
    custom_pk: int  # Custom primary key allowed
```

**Validation Checks**:
- **VAL-002**: Missing primary key (error)
- **VAL-003**: Primary key not named 'id' (warning)
- **VAL-004**: Composite primary key (warning)
- **VAL-005**: Auto-managed field conflicts (created_at, updated_at)
- **VAL-006**: DateTime without timezone
- **VAL-007**: String/Text without length
- **VAL-008**: camelCase field names (should be snake_case)
- **VAL-009**: SQL reserved words as field names
- **VAL-010**: Missing delete cascade in relationships

**When to Use Each Mode**:
- **OFF**: Legacy code migration, custom implementations
- **WARN** (default): Development, catches issues without blocking
- **STRICT**: Production deployments, enforce standards

---

### ErrorEnhancer: Actionable Error Messages

Automatic error enhancement with context, root causes, and solutions:

```python
from dataflow import DataFlow
from dataflow.core.error_enhancer import ErrorEnhancer

db = DataFlow("postgresql://...")

# ErrorEnhancer automatically integrated into DataFlow engine
# Enhanced errors show:
# - Error code (DF-101, DF-102, etc.)
# - Context (node, parameters, workflow state)
# - Root causes with probability scores
# - Actionable solutions with code templates
# - Documentation links

try:
    # Missing parameter error
    workflow.add_node("UserCreateNode", "create", {})
except Exception as e:
    # ErrorEnhancer automatically catches and enriches
    # Shows: DF-101 with specific fixes
    pass
```

**Key Features**:
- **40+ Error Codes**: DF-101 (missing parameter) through DF-805 (runtime errors)
- **Pattern Matching**: Automatic error detection and classification
- **Contextual Solutions**: Code templates with variable substitution
- **Color-Coded Output**: Emojis and formatting for readability
- **Documentation Links**: Direct links to relevant guides

**Common Errors Covered**:
- DF-101: Missing required parameter
- DF-102: Type mismatch (expected dict, got str)
- DF-103: Auto-managed field conflict (created_at, updated_at)
- DF-104: Wrong node pattern (CreateNode vs UpdateNode)
- DF-105: Primary key 'id' missing/wrong name
- DF-201: Invalid connection - source output not found
- DF-301: Migration failed - table already exists

**See**: `sdk-users/apps/dataflow/troubleshooting/top-10-errors.md`

---

### Inspector API: Self-Service Debugging

Introspection API for workflows, nodes, connections, and parameters:

```python
from dataflow.platform.inspector import Inspector

inspector = Inspector(dataflow_instance)
inspector.workflow_obj = workflow.build()

# Connection Analysis
connections = inspector.connections()  # List all connections
broken = inspector.find_broken_connections()  # Find issues
validation = inspector.validate_connections()  # Check validity

# Parameter Tracing
trace = inspector.trace_parameter("create_user", "data")
print(f"Source: {trace.source_node}")
dependencies = inspector.parameter_dependencies("create_user")

# Node Analysis
deps = inspector.node_dependencies("create_user")  # Upstream
dependents = inspector.node_dependents("create_user")  # Downstream
order = inspector.execution_order()  # Topological sort

# Workflow Validation
report = inspector.workflow_validation_report()
if not report['is_valid']:
    print(f"Errors: {report['errors']}")
    print(f"Warnings: {report['warnings']}")
    print(f"Suggestions: {report['suggestions']}")

# High-Level Overview
summary = inspector.workflow_summary()
metrics = inspector.workflow_metrics()
```

**Inspector Methods** (18 total):
- **Connection Analysis** (5): connections(), connection_chain(), connection_graph(), validate_connections(), find_broken_connections()
- **Parameter Tracing** (5): trace_parameter(), parameter_flow(), find_parameter_source(), parameter_dependencies(), parameter_consumers()
- **Node Analysis** (5): node_dependencies(), node_dependents(), execution_order(), node_schema(), compare_nodes()
- **Workflow Analysis** (3): workflow_summary(), workflow_metrics(), workflow_validation_report()

**Use Cases**:
- Diagnose "missing parameter" errors
- Find broken connections
- Trace parameter flow through workflows
- Validate workflows before execution
- Generate workflow documentation
- Debug complex workflows

**Performance**: <1ms per method call (cached operations)

---

### CLI Tools: Industry-Standard Workflow Validation

Command-line tools matching pytest/mypy patterns for workflow validation and debugging:

```bash
# Validate workflow structure and connections
dataflow-validate workflow.py --output text
dataflow-validate workflow.py --fix  # Auto-fix common issues
dataflow-validate workflow.py --output json > report.json

# Analyze workflow metrics and complexity
dataflow-analyze workflow.py --verbosity 2
dataflow-analyze workflow.py --format json

# Generate reports and documentation
dataflow-generate workflow.py report --output-dir ./reports
dataflow-generate workflow.py diagram  # ASCII workflow diagram
dataflow-generate workflow.py docs --output-dir ./docs

# Debug workflows with breakpoints
dataflow-debug workflow.py --breakpoint create_user
dataflow-debug workflow.py --inspect-node create_user
dataflow-debug workflow.py --step  # Step-by-step execution

# Profile performance and detect bottlenecks
dataflow-perf workflow.py --bottlenecks
dataflow-perf workflow.py --recommend
dataflow-perf workflow.py --format json > perf.json
```

**CLI Commands** (5 total):
- **dataflow-validate**: Validate workflow structure, connections, and parameters with --fix flag
- **dataflow-analyze**: Workflow metrics, complexity analysis, and execution order
- **dataflow-generate**: Generate reports, diagrams (ASCII), and documentation
- **dataflow-debug**: Interactive debugging with breakpoints and node inspection
- **dataflow-perf**: Performance profiling, bottleneck detection, and recommendations

**Use Cases**:
- CI/CD integration for workflow validation
- Pre-deployment validation checks
- Performance profiling and optimization
- Documentation generation
- Interactive debugging sessions

**Performance**: Industry-standard CLI tool performance (<100ms startup)

---

### Common Pitfalls Guide
**New**: Comprehensive guides for common DataFlow mistakes

**CreateNode vs UpdateNode** (saves 1-2 hours):
- Side-by-side comparison
- Decision tree for node selection
- 10+ working examples
- Common mistakes and fixes
- **See**: `sdk-users/apps/dataflow/guides/create-vs-update.md`

**Top 10 Errors** (saves 30-120 minutes per error):
- Quick fix guide for 90% of issues
- Error code reference (DF-101 through DF-805)
- Diagnosis decision tree
- Prevention checklist
- Inspector commands for debugging
- **See**: `sdk-users/apps/dataflow/troubleshooting/top-10-errors.md`

---

## Quick Start

```python
from dataflow import DataFlow
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

# Initialize DataFlow
db = DataFlow(connection_string="postgresql://user:pass@localhost/db")

# Define model (generates 11 nodes automatically)
@db.model
class User:
    id: str  # String IDs preserved
    name: str
    email: str

# Use generated nodes in workflows
workflow = WorkflowBuilder()
workflow.add_node("User_Create", "create_user", {
    "data": {"name": "John", "email": "john@example.com"}
})

# Execute
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
user_id = results["create_user"]["result"]  # Access pattern
```

## Reference Documentation

### Getting Started
- **[dataflow-quickstart](dataflow-quickstart.md)** - Quick start guide and core concepts
- **[dataflow-installation](dataflow-installation.md)** - Installation and setup
- **[dataflow-models](dataflow-models.md)** - Defining models with @db.model decorator
- **[dataflow-connection-config](dataflow-connection-config.md)** - Database connection configuration

### Core Operations
- **[dataflow-crud-operations](dataflow-crud-operations.md)** - Create, Read, Update, Delete operations
- **[dataflow-queries](dataflow-queries.md)** - Query patterns and filtering
- **[dataflow-bulk-operations](dataflow-bulk-operations.md)** - Batch operations for performance
- **[dataflow-transactions](dataflow-transactions.md)** - Transaction management
- **[dataflow-connection-isolation](dataflow-connection-isolation.md)** - ⚠️ CRITICAL: Connection isolation and ACID guarantees
- **[dataflow-result-access](dataflow-result-access.md)** - Accessing results from nodes

### Advanced Features
- **[dataflow-multi-instance](dataflow-multi-instance.md)** - Multiple database instances
- **[dataflow-multi-tenancy](dataflow-multi-tenancy.md)** - Multi-tenant architectures
- **[dataflow-existing-database](dataflow-existing-database.md)** - Working with existing databases
- **[dataflow-migrations-quick](dataflow-migrations-quick.md)** - Database migrations
- **[dataflow-custom-nodes](dataflow-custom-nodes.md)** - Creating custom database nodes
- **[dataflow-performance](dataflow-performance.md)** - Performance optimization

### Integration & Deployment
- **[dataflow-nexus-integration](dataflow-nexus-integration.md)** - Deploying with Nexus platform
- **[dataflow-deployment](dataflow-deployment.md)** - Production deployment patterns
- **[dataflow-dialects](dataflow-dialects.md)** - Supported database dialects
- **[dataflow-monitoring](dataflow-monitoring.md)** - Monitoring and observability

### Testing & Quality
- **[dataflow-tdd-mode](dataflow-tdd-mode.md)** - Test-driven development with DataFlow
- **[dataflow-tdd-api](dataflow-tdd-api.md)** - Testing API for DataFlow
- **[dataflow-tdd-best-practices](dataflow-tdd-best-practices.md)** - Testing best practices
- **[dataflow-compliance](dataflow-compliance.md)** - Compliance and standards

### Troubleshooting & Debugging
- **[create-vs-update guide](../../../sdk-users/apps/dataflow/guides/create-vs-update.md)** - CreateNode vs UpdateNode comprehensive guide
- **[top-10-errors](../../../sdk-users/apps/dataflow/troubleshooting/top-10-errors.md)** - Quick fix guide for 90% of issues
- **[dataflow-gotchas](dataflow-gotchas.md)** - Common pitfalls and solutions
- **[dataflow-strict-mode](dataflow-strict-mode.md)** - Strict mode validation HOW-TO guide (Week 9)
- **[dataflow-validation-layers](dataflow-validation-layers.md)** - 4-layer validation architecture (Week 9)
- **[dataflow-debug-agent](dataflow-debug-agent.md)** - Intelligent error analysis with 5-stage pipeline (Week 10)
- **ErrorEnhancer**: Automatic error enhancement (integrated in DataFlow engine) - Enhanced in Week 7
- **Inspector API**: Self-service debugging (18 introspection methods)
- **CLI Tools**: Industry-standard command-line validation and debugging tools (5 commands)

## Key Concepts

### Not an ORM
DataFlow is **NOT an ORM**. It's a workflow framework that:
- Generates workflow nodes from models
- Operates within Kailash's workflow execution model
- Uses string-based result access patterns
- Integrates seamlessly with other workflow nodes

### Automatic Node Generation
Each `@db.model` class generates **11 nodes**:
1. `{Model}_Create` - Create single record
2. `{Model}_Read` - Read by ID
3. `{Model}_Update` - Update record
4. `{Model}_Delete` - Delete record
5. `{Model}_List` - List with filters
6. `{Model}_Upsert` - Insert or update (atomic)
7. `{Model}_Count` - Efficient COUNT(*) queries
8. `{Model}_BulkCreate` - Bulk insert
9. `{Model}_BulkUpdate` - Bulk update
10. `{Model}_BulkDelete` - Bulk delete
11. `{Model}_BulkUpsert` - Bulk upsert

### Critical Rules
- ✅ String IDs preserved (no UUID conversion)
- ✅ Deferred schema operations (safe for Docker/FastAPI)
- ✅ Multi-instance isolation (one DataFlow per database)
- ✅ Result access: `results["node_id"]["result"]`
- ❌ NEVER use truthiness checks on filter/data parameters (empty dict `{}` is falsy)
- ❌ ALWAYS use key existence checks: `if "filter" in kwargs` instead of `if kwargs.get("filter")`
- ❌ NEVER use direct SQL when DataFlow nodes exist
- ❌ NEVER use SQLAlchemy/Django ORM alongside DataFlow

### Database Support
- **SQL Databases**: PostgreSQL, MySQL, SQLite (11 nodes per @db.model)
- **Document Database**: MongoDB with flexible schema (8 specialized nodes)
- **Vector Search**: PostgreSQL pgvector for RAG/AI (3 vector nodes)
- **100% Feature Parity**: SQL databases support identical workflows

## When to Use This Skill

Use DataFlow when you need to:
- Perform database operations in workflows
- Generate CRUD APIs automatically (with Nexus)
- Implement multi-tenant systems
- Work with existing databases
- Build database-first applications
- Handle bulk data operations
- Implement enterprise data management

## Integration Patterns

### With Nexus (Multi-Channel)
```python
from dataflow import DataFlow
from nexus import Nexus

db = DataFlow(connection_string="...")
@db.model
class User:
    id: str
    name: str

# Auto-generates API + CLI + MCP
nexus = Nexus(db.get_workflows())
nexus.run()  # Instant multi-channel platform
```

### With Core SDK (Custom Workflows)
```python
from dataflow import DataFlow
from kailash.workflow.builder import WorkflowBuilder

db = DataFlow(connection_string="...")
# Use db-generated nodes in custom workflows
workflow = WorkflowBuilder()
workflow.add_node("User_Create", "user1", {...})
```

## Multi-Database Support Matrix

### SQL Databases (DatabaseAdapter)
- **PostgreSQL**: Full support with advanced features (asyncpg driver, pgvector extension, native arrays)
- **MySQL**: Full support with 100% feature parity (aiomysql driver)
- **SQLite**: Full support for development/testing/mobile (aiosqlite + custom pooling)
- **Nodes Generated**: 11 per @db.model (Create, Read, Update, Delete, List, Upsert, Count, BulkCreate, BulkUpdate, BulkDelete, BulkUpsert)

### Document Databases (MongoDBAdapter)
- **MongoDB**: Complete NoSQL support (Motor async driver)
- **Features**: Flexible schema, aggregation pipelines, text search, geospatial queries
- **Workflow Nodes**: 8 specialized nodes (DocumentInsert, DocumentFind, DocumentUpdate, DocumentDelete, BulkDocumentInsert, Aggregate, CreateIndex, DocumentCount)
- **Use Cases**: E-commerce catalogs, content management, user profiles, event logs

### Vector Databases (PostgreSQLVectorAdapter)
- **PostgreSQL pgvector**: Semantic similarity search for RAG/AI (pgvector extension)
- **Features**: Cosine/L2/inner product distance, HNSW/IVFFlat indexes
- **Workflow Nodes**: 3 vector nodes (VectorSearch, VectorInsert, VectorUpdate)
- **Use Cases**: RAG applications, semantic search, recommendation engines

### Architecture
- **BaseAdapter**: Minimal interface for all adapter types (adapter_type, database_type, health_check)
- **DatabaseAdapter**: SQL-specific (inherits BaseAdapter)
- **MongoDBAdapter**: Document database (inherits BaseAdapter)
- **PostgreSQLVectorAdapter**: Vector operations (inherits DatabaseAdapter)

### Planned Extensions
- **TimescaleDB**: Time-series data optimization (PostgreSQL extension)
- **Qdrant/Milvus**: Dedicated vector databases with advanced filtering
- **Redis**: Caching and key-value operations
- **Neo4j**: Graph database with Cypher queries

## Related Skills

- **[01-core-sdk](../../01-core-sdk/SKILL.md)** - Core workflow patterns
- **[03-nexus](../nexus/SKILL.md)** - Multi-channel deployment
- **[04-kaizen](../kaizen/SKILL.md)** - AI agent integration
- **[17-gold-standards](../../17-gold-standards/SKILL.md)** - Best practices

## Support

For DataFlow-specific questions, invoke:
- `dataflow-specialist` - DataFlow implementation and patterns
- `testing-specialist` - DataFlow testing strategies (NO MOCKING policy)
- `framework-advisor` - Choose between Core SDK and DataFlow
