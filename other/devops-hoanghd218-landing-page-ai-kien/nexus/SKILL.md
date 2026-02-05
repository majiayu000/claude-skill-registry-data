---
name: nexus
description: "Kailash Nexus - zero-config multi-channel platform for deploying workflows as API + CLI + MCP simultaneously. Use when asking about 'Nexus', 'multi-channel', 'platform deployment', 'API deployment', 'CLI deployment', 'MCP deployment', 'unified sessions', 'workflow deployment', 'production deployment', 'API gateway', 'FastAPI alternative', 'session management', 'health monitoring', 'enterprise platform', 'plugins', 'event system', or 'workflow registration'."
---

# Kailash Nexus - Multi-Channel Platform Framework

Nexus is a zero-config multi-channel platform built on Kailash Core SDK that deploys workflows as API + CLI + MCP simultaneously.

## Features

Nexus transforms workflows into a complete platform with:

- **Zero Configuration**: Deploy workflows instantly without boilerplate code
- **Multi-Channel Access**: API, CLI, and MCP from single deployment
- **Unified Sessions**: Consistent session management across all channels
- **Enterprise Features**: Health monitoring, plugins, event system, comprehensive logging
- **DataFlow Integration**: Automatic CRUD API generation from database models
- **Production Ready**: Deployment patterns, monitoring, troubleshooting guides
- **FastAPI Alternative**: Workflow-based platform without manual route definition
- **Async-First**: Uses AsyncLocalRuntime by default for optimal performance

## Quick Start

```python
from nexus import Nexus

# Define workflow
workflow = create_my_workflow()

# Deploy to all channels at once
nexus = Nexus([workflow])
nexus.run(port=8000)

# Now available via:
# - HTTP API: POST http://localhost:8000/api/workflow/{workflow_id}
# - CLI: nexus run {workflow_id} --input '{"key": "value"}'
# - MCP: Connect via MCP client (Claude Desktop, etc.)
```

## Reference Documentation

### Getting Started
- **[nexus-quickstart](nexus-quickstart.md)** - Quick start guide
- **[nexus-installation](nexus-installation.md)** - Installation and setup
- **[nexus-architecture](nexus-architecture.md)** - Architecture overview
- **[README](README.md)** - Framework overview
- **[nexus-comparison](nexus-comparison.md)** - Nexus vs FastAPI/Flask

### Core Concepts
- **[nexus-workflow-registration](nexus-workflow-registration.md)** - Registering workflows
- **[nexus-multi-channel](nexus-multi-channel.md)** - Multi-channel architecture
- **[nexus-sessions](nexus-sessions.md)** - Session management
- **[nexus-config-options](nexus-config-options.md)** - Configuration options

### Channel-Specific Patterns
- **[nexus-api-patterns](nexus-api-patterns.md)** - HTTP API patterns
- **[nexus-api-input-mapping](nexus-api-input-mapping.md)** - API input handling
- **[nexus-cli-patterns](nexus-cli-patterns.md)** - CLI usage patterns
- **[nexus-mcp-channel](nexus-mcp-channel.md)** - MCP channel configuration

### Integration
- **[nexus-dataflow-integration](nexus-dataflow-integration.md)** - DataFlow + Nexus patterns
- **[nexus-plugins](nexus-plugins.md)** - Plugin system
- **[nexus-event-system](nexus-event-system.md)** - Event-driven architecture

### Production & Operations
- **[nexus-production-deployment](nexus-production-deployment.md)** - Production deployment
- **[nexus-health-monitoring](nexus-health-monitoring.md)** - Health checks and monitoring
- **[nexus-enterprise-features](nexus-enterprise-features.md)** - Enterprise capabilities
- **[nexus-troubleshooting](nexus-troubleshooting.md)** - Common issues and solutions

## Key Concepts

### Zero-Config Platform
Nexus eliminates boilerplate:
- **No FastAPI routes** - Automatic API generation from workflows
- **No CLI arg parsing** - Automatic CLI creation
- **No MCP server setup** - Automatic MCP integration
- **Unified deployment** - One command for all channels

### Multi-Channel Architecture
Single deployment, three access methods:
1. **HTTP API**: RESTful JSON endpoints
2. **CLI**: Command-line interface
3. **MCP**: Model Context Protocol server

### Unified Sessions
Consistent session management:
- Cross-channel session tracking
- Session state persistence
- Session-scoped workflows
- Concurrent session support

### Enterprise Features
Production-ready capabilities:
- Health monitoring endpoints
- Plugin system for extensibility
- Event system for integrations
- Comprehensive logging and metrics
- Correct channel initialization flow
- Proper workflow registration

## When to Use This Skill

Use Nexus when you need to:
- Deploy workflows as production platforms
- Provide multiple access methods (API/CLI/MCP)
- Build enterprise platforms quickly
- Auto-generate CRUD APIs (with DataFlow)
- Replace FastAPI/Flask with workflow-based platform
- Create multi-channel applications
- Deploy AI agent platforms (with Kaizen)

## Integration Patterns

### With DataFlow (Auto CRUD API)
```python
from nexus import Nexus
from dataflow import DataFlow

# Define models
db = DataFlow(...)
@db.model
class User:
    id: str
    name: str

# Auto-generates CRUD endpoints for all models
nexus = Nexus(db.get_workflows())
nexus.run()

# GET  /api/User/list
# POST /api/User/create
# GET  /api/User/read/{id}
# PUT  /api/User/update/{id}
# DELETE /api/User/delete/{id}
```

### With Kaizen (Agent Platform)
```python
from nexus import Nexus
from kaizen.base import BaseAgent

# Deploy agents via all channels
agent_workflow = create_agent_workflow()
nexus = Nexus([agent_workflow])
nexus.run()

# Agents accessible via API, CLI, and MCP
```

### With Core SDK (Custom Workflows)
```python
from nexus import Nexus
from kailash.workflow.builder import WorkflowBuilder

# Deploy custom workflows
workflows = [
    create_workflow_1(),
    create_workflow_2(),
    create_workflow_3(),
]

nexus = Nexus(workflows)
nexus.run(port=8000)
```

### Standalone Platform
```python
from nexus import Nexus

# Complete platform from workflows
nexus = Nexus(
    workflows=[...],
    plugins=[custom_plugin],
    health_checks=True,
    monitoring=True
)
nexus.run(
    host="0.0.0.0",
    port=8000,
    workers=4
)
```

## Critical Rules

- ✅ Use Nexus instead of FastAPI for workflow platforms
- ✅ Register workflows, not individual routes
- ✅ Leverage unified sessions across channels
- ✅ Enable health monitoring in production
- ✅ Use plugins for custom behavior
- ✅ Nexus uses AsyncLocalRuntime by default (correct for Docker)
- ❌ NEVER mix FastAPI routes with Nexus
- ❌ NEVER implement manual API/CLI/MCP servers when Nexus can do it
- ❌ NEVER skip health checks in production

## Deployment Patterns

### Development
```python
nexus = Nexus(workflows)
nexus.run(port=8000)  # Single process, hot reload
```

### Production (Docker)
```python
from kailash.runtime import AsyncLocalRuntime

nexus = Nexus(
    workflows,
    runtime_factory=lambda: AsyncLocalRuntime()
)
nexus.run(host="0.0.0.0", port=8000, workers=4)
```

### With Load Balancer
```bash
# Deploy multiple Nexus instances behind nginx/traefik
docker-compose up --scale nexus=3
```

## Channel Comparison

| Feature | API | CLI | MCP |
|---------|-----|-----|-----|
| **Access** | HTTP | Terminal | MCP Clients |
| **Input** | JSON | Args/JSON | Structured |
| **Output** | JSON | Text/JSON | Structured |
| **Sessions** | ✓ | ✓ | ✓ |
| **Auth** | ✓ | ✓ | ✓ |
| **Streaming** | ✓ | ✓ | ✓ |

## Related Skills

- **[01-core-sdk](../../01-core-sdk/SKILL.md)** - Core workflow patterns
- **[02-dataflow](../dataflow/SKILL.md)** - Auto CRUD API generation
- **[04-kaizen](../kaizen/SKILL.md)** - AI agent deployment
- **[05-mcp](../mcp/SKILL.md)** - MCP channel details
- **[17-gold-standards](../../17-gold-standards/SKILL.md)** - Best practices

## Support

For Nexus-specific questions, invoke:
- `nexus-specialist` - Nexus implementation and deployment
- `deployment-specialist` - Production deployment patterns
- `framework-advisor` - When to use Nexus vs other approaches
