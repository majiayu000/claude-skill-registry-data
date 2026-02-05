---
name: HyperFleet Architecture
description: Answers questions about HyperFleet architecture, design patterns, versioning strategies, cluster lifecycle, event-driven architecture, adapter framework, and git workflow by fetching docs from the openshift-hyperfleet/architecture GitHub repository.
---

# HyperFleet Architecture Skill

## When to Use This Skill

Activate this skill when the user asks questions about:

- HyperFleet architecture, design patterns, or principles
- Versioning strategies (API, Sentinel, adapters, config)
- Status aggregation and cluster lifecycle
- Event-driven architecture and CloudEvents
- Adapter framework and config-driven deployment
- Git workflow, branching, or release processes
- Design decisions or trade-offs

## Architecture Documentation Location

All HyperFleet architecture documentation is located in the **architecture repository** on GitHub at:

```
https://github.com/openshift-hyperfleet/architecture
```

### Finding Relevant Documentation

When the user asks about HyperFleet, explore the repository to find relevant markdown files:

1. Start by browsing the repository structure at `https://github.com/openshift-hyperfleet/architecture/tree/main/hyperfleet/`
2. Look in the appropriate subdirectory based on the question:
   - **`architecture/`** - High-level system architecture and design patterns
   - **`components/`** - Detailed component design documents
   - **`docs/`** - Implementation guides, versioning strategies, operational procedures
   - **Other subdirectories** - Explore as needed for additional context
3. Fetch and read the relevant markdown files using raw GitHub URLs: `https://raw.githubusercontent.com/openshift-hyperfleet/architecture/main/hyperfleet/{path-to-file}`
4. Use multiple files if needed to provide comprehensive answers

## How to Use These Docs

1. **Read the relevant doc(s)** based on the user's question
2. **Use the actual content** from these files - they are the single source of truth
3. **Reference specific sections** when answering (e.g., "According to `api-versioning.md`, HyperFleet uses URI-based
   versioning...")
4. **Stay current** - these docs are actively maintained and represent the latest decisions

## HyperFleet Core Principles

When reviewing or answering questions, keep these core architectural principles in mind:

- **Event-driven architecture** - CloudEvents 1.0, AsyncAPI specs
- **Config-driven deployment** - Adapter framework with Helm charts
- **Cloud-agnostic core** - Provider-specific logic isolated to adapters
- **Semantic versioning** - MAJOR.MINOR.PATCH across all components
- **Forward-only migrations** - Expand-contract pattern for breaking changes

## Example Questions This Skill Helps With

- "How does HyperFleet handle API versioning?"
- "What's the adapter config versioning strategy?"
- "How do we version CloudEvents schemas?"
- "What's our Git branching model?"
- "How does the adapter framework work?"
- "What are the cluster lifecycle phases?"
- "How do we handle breaking changes in the API?"

## Instructions

When this skill is invoked:

1. Identify which documentation file(s) are relevant to the user's question
2. Read those file(s) from the architecture repo
3. Provide accurate answers based on the documentation content
4. Reference specific sections or line numbers when helpful
5. If the documentation doesn't cover the topic, say so and offer to help find the answer elsewhere
