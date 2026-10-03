---
metadata:
  name: synthesize-findings
  class: toolboxes
  type: skill
  version: '1.0'
  schema_version: '1.0'
  freshness:
    status: active
    sync_count: 0
    last_synced_by: daemon
    last_synced: '2026-06-27T00:00:00'
credentials:
  maturity: "functional"
  description: "Merge multiple inputs, analyses, or research findings into a single unified, coherent conclusion or artifact."
  when_to_use: "Use this skill when the task involves synthesize findings"
  triggers: ["synthesize", "combine", "merge", "consolidate", "summarize all", "bring together"]
  inputs: ["multiple source documents or analyses", "synthesis goal", "output format"]
  outputs: ["unified synthesis document", "key insight list", "recommended action"]
---

# Synthesize Findings

This skill allows the agent to merge multiple inputs — from research, analysis, brainstorming, or document reading — into a single unified, coherent output. Synthesis is the final cognitive act that turns parallel work streams into one actionable conclusion.

## Steps

1. **Collect all inputs.** Gather every source document, analysis result, research finding, or data point that feeds into this synthesis. List them explicitly.
2. **Identify the synthesis goal.** What single question or objective should the final output answer? State it in one sentence.
3. **Extract key points per source.** For each input, extract the 2–5 most relevant points that bear on the synthesis goal. Discard noise.
4. **Identify patterns and tensions.** Look across all extracted points for: agreements (reinforcing signals), contradictions (conflicting signals), and gaps (unanswered questions).
5. **Resolve contradictions.** For conflicting data points, determine which is more authoritative or recent. Note the conflict and your resolution rationale.
6. **Draft the unified view.** Write a synthesis that integrates all key points into a coherent whole — not a list of summaries, but a single integrated perspective.
7. **Extract top insights.** Distill the synthesis into 3–5 key insights — the most important takeaways an agent or user must walk away with.
8. **Produce recommended action.** Based on the synthesis, what is the single most important next step?
9. **Output** the full synthesis document.

## Output Format

```yaml
synthesis_result:
  goal: "<synthesis goal>"
  sources_processed: <number>
  key_insights:
    - insight: "<insight>"
      supporting_sources: ["<source 1>", "<source 2>"]
    - insight: "<insight>"
      supporting_sources: ["<source 1>"]
  contradictions_resolved:
    - conflict: "<what conflicted>"
      resolution: "<how resolved>"
  unified_view: "<paragraph integrating all findings>"
  recommended_action: "<single most important next step>"
```

## Notes
- A synthesis is NOT a list of summaries — it must produce a new, integrated perspective.
- If sources contradict each other, resolve explicitly — never paper over conflicts.
- Invoke `communication` toolbox after synthesis to format the output for your target audience.
