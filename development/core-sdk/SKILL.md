---
name: core-sdk
description: "Kailash Core SDK fundamentals including workflow creation, node patterns, connections, runtime execution, parameter passing, error handling, cyclic workflows, async patterns, MCP integration, and installation. Use when asking about 'workflow basics', 'core sdk', 'create workflow', 'workflow builder', 'node patterns', 'connections', 'runtime', 'parameters', 'imports', 'installation', 'getting started', 'workflow execution', 'async workflows', 'error handling', 'cyclic workflows', 'PythonCode node', 'SwitchNode', or 'MCP integration'."
---

# Kailash Core SDK - Foundational Skills

Comprehensive guide to Kailash Core SDK fundamentals for workflow automation and integration.

## Features

The Core SDK provides the foundational building blocks for creating custom workflows with fine-grained control:

- **110+ Workflow Nodes**: Pre-built nodes for AI, API, database, file operations, logic, and more
- **WorkflowBuilder API**: String-based workflow construction with type safety
- **Dual Runtime Support**: AsyncLocalRuntime (Docker/FastAPI) and LocalRuntime (CLI/scripts)
- **Advanced Patterns**: Cyclic workflows, conditional execution, error handling
- **MCP Integration**: Built-in Model Context Protocol support
- **Parameter Passing**: Flexible data flow between nodes
- **Zero Configuration**: Auto-detection of runtime context
- **Production Ready**: Enterprise features including monitoring, validation, and debugging

## Quick Start

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime.local import LocalRuntime

workflow = WorkflowBuilder()
workflow.add_node("NodeName", "id", {"param": "value"})
runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Reference Documentation

### Getting Started
- **[workflow-quickstart](workflow-quickstart.md)** - Create basic workflows with WorkflowBuilder
- **[kailash-installation](kailash-installation.md)** - Installation and setup guide
- **[kailash-imports](kailash-imports.md)** - Import patterns and module organization

### Core Patterns
- **[node-patterns-common](node-patterns-common.md)** - Common node usage patterns
- **[connection-patterns](connection-patterns.md)** - Linking nodes and data flow
- **[param-passing-quick](param-passing-quick.md)** - Parameter passing strategies
- **[runtime-execution](runtime-execution.md)** - Executing workflows (sync/async)

### Advanced Topics
- **[async-workflow-patterns](async-workflow-patterns.md)** - Asynchronous workflow execution
- **[cycle-workflows-basics](cycle-workflows-basics.md)** - Cyclic workflow patterns
- **[error-handling-patterns](error-handling-patterns.md)** - Error management strategies
- **[switchnode-patterns](switchnode-patterns.md)** - Conditional routing with SwitchNode
- **[pythoncode-best-practices](pythoncode-best-practices.md)** - PythonCode node best practices
- **[mcp-integration-guide](mcp-integration-guide.md)** - Model Context Protocol integration

## Key Concepts

### WorkflowBuilder Pattern
- String-based node API: `workflow.add_node("NodeName", "id", {})`
- Always call `.build()` before execution
- Never `workflow.execute(runtime)` - always `runtime.execute(workflow.build())`

### Runtime Selection
- **AsyncLocalRuntime**: For Docker/FastAPI (async contexts) - async-first, no threading, 10-100x faster
- **LocalRuntime**: For CLI/scripts (sync contexts) - synchronous execution with thread support
- **get_runtime()**: Auto-detection helper that selects appropriate runtime based on context

Both runtimes return identical structure: `(results, run_id)` tuple.

### Runtime Architecture
Both LocalRuntime and AsyncLocalRuntime inherit from BaseRuntime with shared capabilities:

**BaseRuntime Foundation**:
- 29 configuration parameters (debug, enable_cycles, conditional_execution, connection_validation, etc.)
- Execution metadata management
- Common initialization and validation modes (strict, warn, off)

**Shared Mixins**:
- **CycleExecutionMixin**: Cyclic workflow execution with validation
- **ValidationMixin**: Workflow structure validation (5 methods)
- **ConditionalExecutionMixin**: Conditional execution and branching with SwitchNode support

**AsyncLocalRuntime-Specific**:
- WorkflowAnalyzer for optimal execution strategy
- Level-based parallelism for concurrent execution
- Thread pool for sync nodes without blocking
- Semaphore control to prevent resource exhaustion

## Critical Rules

- ✅ ALWAYS: `runtime.execute(workflow.build())`
- ✅ String-based nodes: `workflow.add_node("NodeName", "id", {})`
- ✅ 4-parameter connections: `(source_id, source_param, target_id, target_param)`
- ✅ Docker/FastAPI: Use AsyncLocalRuntime (mandatory)
- ✅ CLI/Scripts: Use LocalRuntime
- ❌ NEVER: `workflow.execute(runtime)`
- ❌ NEVER: Instance-based nodes
- ❌ NEVER: Use LocalRuntime in Docker (causes hangs)

## When to Use This Skill

Use this skill when you need to:
- Create custom workflows from scratch
- Understand workflow fundamentals
- Learn node patterns and connections
- Set up runtime execution
- Handle errors in workflows
- Implement cyclic or async patterns
- Integrate with MCP
- Get started with Kailash SDK

## Related Skills

- **[02-dataflow](../02-dataflow/SKILL.md)** - Database operations framework built on Core SDK
- **[03-nexus](../03-nexus/SKILL.md)** - Multi-channel platform framework built on Core SDK
- **[04-kaizen](../04-kaizen/SKILL.md)** - AI agent framework built on Core SDK
- **[06-cheatsheets](../06-cheatsheets/SKILL.md)** - Quick reference patterns
- **[08-nodes-reference](../08-nodes-reference/SKILL.md)** - Complete node reference
- **[09-workflow-patterns](../09-workflow-patterns/SKILL.md)** - Industry workflow templates
- **[17-gold-standards](../17-gold-standards/SKILL.md)** - Mandatory best practices

## Support

For complex workflows or debugging, invoke:
- `pattern-expert` - Workflow patterns and cyclic debugging
- `sdk-navigator` - Find specific nodes or patterns
- `testing-specialist` - Test workflow implementations
