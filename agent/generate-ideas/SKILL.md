---
metadata:
  name: generate-ideas
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
  description: "Generate ideas and explore multiple approaches when a path isn't clear."
  when_to_use: "Use this skill when the task involves generate ideas"
  triggers: ["brainstorm", "ideate", "explore", "alternatives", "options", "what if"]
  inputs: ["problem statement", "constraints", "context"]
  outputs: ["divergent idea list", "categorized approaches", "recommended direction"]
---

# Generate Ideas

This skill allows the agent to generate a wide range of ideas and explore multiple approaches before converging on the most promising direction. It uses a deliberate diverge-then-converge process to avoid premature narrowing.

## Steps

1. **Frame the problem.** Restate the problem statement in your own words to confirm you understand it. Identify what a successful outcome looks like.
2. **Inventory constraints.** List hard constraints (non-negotiable) and soft constraints (preferences). Hard constraints narrow the solution space; soft ones inform prioritization.
3. **Diverge — generate freely.** Produce at least 5 distinct ideas without filtering. Apply multiple lenses: conventional, unconventional, hybrid, minimal, and maximal approaches.
4. **Categorize.** Group generated ideas by theme, approach type, or effort level.
5. **Converge — score and filter.** Apply a quick feasibility vs. impact filter. Eliminate ideas that violate hard constraints.
6. **Surface the top 1–3 candidates.** For each, provide a one-line rationale for why it's worth exploring.
7. **Output** the full divergent list + categorized view + recommended direction.

## Output Format

```yaml
ideation_result:
  problem_restatement: "<your restatement>"
  hard_constraints:
    - "<constraint>"
  ideas:
    - id: 1
      idea: "<idea>"
      category: "<theme>"
      feasibility: high | medium | low
      impact: high | medium | low
  recommended_direction: "<top 1-3 ideas with rationale>"
```

## Notes
- Never skip the diverge phase — the best solution is often the 4th or 5th idea generated.
- If the problem space is unclear, invoke `analyze-context` first to sharpen the framing.
- Use the `benchmarking` toolbox after this skill to formally compare shortlisted ideas.
