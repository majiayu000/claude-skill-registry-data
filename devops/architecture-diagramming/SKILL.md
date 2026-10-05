---
name: architecture-diagramming
description: This skill should be used when the user asks to "generate architecture diagrams", "create dependency graph", "draw sequence diagram", "visualize system architecture", "C4 model", "Mermaid diagram", "component diagram", "ER diagram", or "data flow diagram". Provides C4 model methodology and Mermaid diagram templates for architecture documentation.
---

# Architecture Diagramming

## Purpose

Provide standardized methodology and templates for generating architecture diagrams from codebase analysis. Uses the C4 Model for hierarchical architecture views and Mermaid for diagram rendering.

## C4 Model Overview

The C4 Model defines four levels of architecture abstraction:

| Level | Name | Shows | When to Use |
|-------|------|-------|-------------|
| 1 | System Context | System + external actors | Always, the "big picture" |
| 2 | Container | Applications, data stores, services | When multiple deployable units exist |
| 3 | Component | Internal modules within a container | When analyzing a specific service |
| 4 | Code | Classes, interfaces | Rarely, only for critical components |

## Diagram Selection Guide

Choose diagrams based on what exists in the codebase:

| What You Find | Diagrams to Generate |
|---------------|---------------------|
| Multiple services/microservices | System Overview (L1), Container (L2), Dependency Graph |
| Database schemas/models | ER Diagram |
| API endpoints | API Interaction Diagram |
| Message queues/events | Event Flow Diagram |
| Multi-step workflows | Sequence Diagrams |
| Docker/K8s configs | Deployment/Infrastructure Diagram |
| Monolith with modules | Component Diagram (L3) |

## Diagram Generation Process

1. Scan project structure to identify components and boundaries
2. Read config files (docker-compose, k8s, CI/CD, infrastructure-as-code)
3. Map entry points, routes, and service communication
4. Identify data stores and their relationships
5. Select appropriate diagram types from the guide above
6. Generate only diagrams relevant to findings, do not include generic templates
7. Use proper Mermaid syntax with styling (subgraphs, colors, labels)

## Mermaid Styling Conventions

```mermaid
%% Color coding for diagram elements:
%% - External actors/users: fill:#e1f5fe (light blue)
%% - External services: fill:#ffebee (light red)
%% - Core services: default styling
%% - Databases: use cylinder notation [( )]
%% - Critical components: fill:#fff3e0 (light orange)
```

## Key Principles

- **Generate only what exists**: Never include components not found in the codebase
- **Label with actual technology**: Use real framework/database names discovered
- **Show actual relationships**: Trace real imports, API calls, and configurations
- **Include risk assessment**: Flag high-risk dependencies and single points of failure

## Additional Resources

### Reference Files

For codebase discovery heuristics at each C4 level, consult:
- **`references/c4-model-guide.md`**: What to look for in code at each C4 level, container identification heuristics, and common architectural layer patterns
