---
name: parallel-explore
description: Launch four Explore agents in parallel to simultaneously investigate multiple areas of a codebase. Use this skill when multiple independent exploration tasks need to be performed concurrently, such as searching for different patterns, examining various file types, or investigating multiple architectural components at once.
---

# Parallel Explore

## Overview

This skill enables launching four Explore agents in parallel to perform concurrent codebase exploration tasks. By running multiple agents simultaneously, significantly reduce the time required to gather comprehensive information across different areas of a codebase.

## When to Use This Skill

Use this skill when:
- Multiple independent search patterns need investigation simultaneously
- Different areas of the codebase require exploration at the same time
- Time-sensitive exploration requires faster results through parallelization
- Comprehensive codebase analysis benefits from concurrent investigation of multiple aspects

## How to Use

### Basic Usage

To launch four parallel Explore agents, use the Task tool with subagent_type=Explore four times in a single message. Each agent should have a distinct exploration focus.

**Example: Comprehensive codebase exploration**

Launch four agents to explore different aspects:

1. **Authentication patterns**: Search for login flows, token management, session handling
2. **API endpoints**: Find route handlers, REST endpoints, GraphQL resolvers
3. **Database models**: Locate ORM models, migrations, schema definitions
4. **Testing infrastructure**: Find unit tests, integration tests, test utilities

**Implementation:**

```
Send a single message with four Task tool calls:
- Task 1: Explore authentication code (thoroughness: medium)
- Task 2: Explore API endpoints (thoroughness: medium)
- Task 3: Explore database models (thoroughness: medium)
- Task 4: Explore test files (thoroughness: medium)
```

### Thoroughness Levels

Specify the thoroughness level for each agent based on exploration depth needed:
- **quick**: Basic search, fast results
- **medium**: Moderate exploration with reasonable depth (recommended default)
- **very thorough**: Comprehensive analysis across multiple locations and patterns

### Example Scenarios

**Scenario 1: Architecture Investigation**
- Agent 1: Frontend components and UI structure
- Agent 2: Backend services and business logic
- Agent 3: Database and data layer
- Agent 4: Configuration and deployment files

**Scenario 2: Feature Implementation Research**
- Agent 1: Similar existing features in the codebase
- Agent 2: Relevant utility functions and helpers
- Agent 3: Related test patterns
- Agent 4: Documentation and comments about the feature area

**Scenario 3: Dependency Analysis**
- Agent 1: External package imports and usage
- Agent 2: Internal module dependencies
- Agent 3: Type definitions and interfaces
- Agent 4: Build and bundling configuration

**Scenario 4: Error Investigation**
- Agent 1: Error handling patterns
- Agent 2: Logging and monitoring code
- Agent 3: Validation and error messages
- Agent 4: Related bug fixes in git history

## Best Practices

1. **Independent Tasks**: Ensure each agent's task is independent to maximize parallelization benefits
2. **Clear Focus**: Give each agent a specific, well-defined exploration area
3. **Balanced Thoroughness**: Use "medium" thoroughness by default; only use "very thorough" when necessary
4. **Single Message**: Always launch all four agents in a single message to enable true parallelization
5. **Distinct Prompts**: Make each agent's prompt unique and focused on different aspects

## Tips

- After agents return results, synthesize findings across all four explorations
- If one exploration area yields no results, adjust the search strategy for follow-up investigations
- Consider using different thoroughness levels if some areas require deeper analysis than others
- Frame each prompt clearly with the specific goal and focus area for best results
