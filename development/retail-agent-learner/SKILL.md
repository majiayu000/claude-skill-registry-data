---
name: retail-agent-learner
description: Learn ADK concepts and understand the retail agent pipeline. Use when asking how the agent works, what ADK is, wanting to understand the architecture, state flow, or individual agent purposes.
---

# Retail Agent Learner

## Pipeline Overview

This is an 8-agent pipeline for retail site selection analysis:

```
User Query
    ↓
IntakeAgent ────────────→ Extract location + business type
    ↓
MarketResearchAgent ────→ Google Search for demographics
    ↓
CompetitorMappingAgent ─→ Google Maps Places API
    ↓
GapAnalysisAgent ───────→ Python code execution (pandas)
    ↓
StrategyAdvisorAgent ───→ Extended thinking synthesis
    ↓
ParallelAgent ──────────→ Concurrent artifact generation
    ├── ReportGenerator ─→ HTML report
    ├── InfographicAgent → Image generation
    └── AudioOverview ───→ TTS podcast audio
```

## What Each Agent Does

| Agent | Purpose | Key Tool/Feature |
|-------|---------|------------------|
| IntakeAgent | Parse user request | AgentTool pattern |
| MarketResearchAgent | Find market data | `google_search` built-in |
| CompetitorMappingAgent | Map competitors | Google Maps API |
| GapAnalysisAgent | Calculate viability | Code execution (pandas) |
| StrategyAdvisorAgent | Synthesize recommendations | Extended thinking |
| ReportGenerator | Create HTML report | Artifact generation |
| InfographicAgent | Generate visual | Image generation |
| AudioOverview | Create podcast audio | TTS multi-speaker |

## Key ADK Concepts

### Agents
- **LlmAgent**: Single LLM call with tools and instructions
- **SequentialAgent**: Runs sub-agents one after another
- **ParallelAgent**: Runs sub-agents concurrently

### State Flow
Data passes between agents via session state:
```
IntakeAgent → state["target_location"], state["business_type"]
MarketResearchAgent → state["market_research_findings"]
CompetitorMappingAgent → state["competitor_analysis"]
GapAnalysisAgent → state["gap_analysis"]
StrategyAdvisorAgent → state["strategic_report"]
```

### Tools
Functions that agents can call to perform actions. Access state via `ToolContext`.

### Callbacks
Lifecycle hooks: `before_agent_callback` and `after_agent_callback`.

## Learning Path

Start with the 9-part tutorial series:
1. **Part 1**: Setup + First Agent
2. **Part 2**: IntakeAgent
3. **Part 3**: MarketResearchAgent
4. **Part 4**: CompetitorMappingAgent
5. **Part 5**: GapAnalysisAgent (code execution)
6. **Part 6**: StrategyAdvisorAgent (extended thinking)
7. **Part 7**: ArtifactGeneration (parallel outputs)
8. **Part 8**: Testing
9. **Part 9**: Production Deployment

[See references/architecture.md for detailed data flow]
[See references/adk-concepts.md for ADK deep dive]
