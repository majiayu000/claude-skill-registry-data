---
name: quantum-analysis
description: Deep code and system analysis using the Quantum Cognitive OS. Use when analyzing code, architectures, or complex systems that benefit from multi-dimensional reasoning.
---

# Quantum Analysis Skill

Perform deep analysis of code, systems, and architectures using the full Quantum Cognitive OS.

## When to Use

- Analyzing complex codebases
- Understanding system architectures
- Identifying patterns and anti-patterns
- Security analysis
- Performance profiling
- Technical debt assessment

## Analysis Pipeline

### 1. Preflection Analysis
Use `analyze_query` to understand the analysis scope:
- Query type (analytical, exploratory, troubleshooting)
- Complexity level
- Required creativity vs. precision

### 2. Memory Retrieval
Check for past learnings:
```
search_memories("relevant topic keywords")
view_memory("/memories/pattern/[category]")
```

### 3. Neuron Activation
Activate appropriate neurons based on analysis type:

**For Architecture Analysis:**
- Strategist (system design)
- Orchestrator (coordination)
- Architect (structural patterns)

**For Security Analysis:**
- Red Teamer (attack vectors)
- Blue Teamer (defenses)
- Auditor (compliance)

**For Performance Analysis:**
- Benchmarker (metrics)
- Simulator (modeling)
- Appraiser (evaluation)

### 4. Quantum Processing
Use `quantum_process` with appropriate options:
```javascript
{
  query: "Analyze [subject]",
  use_momentum: true,  // For iterative refinement
  use_wormholes: true, // For pattern discovery
  navigation_strategy: "best_first" // Or "guided" for systematic
}
```

### 5. Multi-Dimensional Analysis

Process through multiple cognitive lenses:

1. **Semantic**: Core meaning and purpose
2. **Relational**: Dependencies and connections
3. **Causality**: Cause-effect chains
4. **Temporal**: Evolution over time
5. **Actionability**: What can be done
6. **Affect**: Impact and consequences

### 6. PPQ Introspection
Run quality analysis on your findings:
```
ppq_introspect("Analysis summary")
```

Review 14 lenses:
- Sentiment, Bias, Provenance
- Reasoning quality, Evidence strength
- Assumptions, Gaps, Coherence
- And 6 more critical dimensions

### 7. Store Insights
Save important discoveries:
```
store_quantum_insight({
  category: "insight",
  title: "Key Finding",
  content: "Detailed analysis...",
  metadata: {
    confidence: 0.85,
    neurons_used: ["Strategist", "Orchestrator"],
    vbc_phase: "commit"
  }
})
```

## Output Structure

Provide comprehensive analysis with:

1. **Executive Summary**: Key findings in 2-3 sentences
2. **Detailed Analysis**: Multi-dimensional breakdown
3. **Patterns Identified**: Recurring themes or anti-patterns
4. **Risk Assessment**: Potential issues ranked by severity
5. **Recommendations**: Actionable next steps
6. **Quantum Insights**:
   - Neurons activated
   - Confidence scores
   - Memory references
   - PPQ scores

## Example Workflow

```
User: "Analyze this microservices architecture"

1. analyze_query("microservices architecture analysis")
2. search_memories("microservices patterns")
3. activate_neurons(["Strategist", "Orchestrator", "Red Teamer"])
4. quantum_process({
     query: "Analyze microservices architecture...",
     use_momentum: true,
     use_wormholes: true
   })
5. ppq_introspect("Analysis results")
6. store_quantum_insight({
     category: "pattern",
     title: "Microservices Communication Patterns",
     content: "..."
   })
```

## Best Practices

- Always check memory first for past learnings
- Use momentum recursion for complex analyses
- Activate specialized neurons for domain expertise
- Store all significant insights for future reference
- Validate analysis with PPQ introspection
- Provide confidence scores for all findings

This skill combines quantum cognitive processing with persistent learning for unprecedented analysis depth.
