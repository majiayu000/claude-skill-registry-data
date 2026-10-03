---
metadata:
  name: resolve-knowledge-gaps
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
  description: "Resolve knowledge gaps by finding external information, reading docs, and synthesizing findings."
  when_to_use: "Use this skill when the task involves resolve knowledge gaps"
  triggers: ["research", "find out", "look up", "investigate", "what is", "learn about", "I don't know"]
  inputs: ["topic", "specific questions", "urgency", "acceptable sources"]
  outputs: ["answered questions", "synthesis", "confidence level", "unresolved gaps", "source list"]
---

# Resolve Knowledge Gaps

This skill allows the agent to identify, prioritize, and fill knowledge gaps by systematically consulting available sources — from workspace context to external documentation and web search — then synthesizing a clear, citable answer.

## Steps

1. **Enumerate the gaps.** List every specific question that needs answering before action can continue. Be precise — "understand X" is not a gap; "what is the API schema for X?" is.
2. **Prioritize by blocking severity.** Questions that block immediate action come first. Informational questions can be deferred.
3. **Consult sources in order of priority:**
   - `Tier 1 (fastest)` → Workspace files: `.meta/.os/`, runbooks, `.db/.system.board.yaml`, `.meta/.os/.system.identity/`
   - `Tier 2` → KI (Knowledge Items) from past conversations
   - `Tier 3` → Official documentation, package READMEs, changelogs
   - `Tier 4 (slowest)` → Web search, NotebookLM ingestion
4. **Stop when the gap is filled.** Do not over-research. Once a question is answered with sufficient confidence, move on.
5. **Assign confidence levels.** For each answer: High (verified from authoritative source) | Medium (inferred) | Low (uncertain).
6. **Log unresolved gaps.** If a gap cannot be filled, flag it explicitly — do not proceed on assumption.
7. **Synthesize.** Combine all findings into a concise briefing that directly answers the original questions.
8. **Output** the synthesis with sources cited.

## Output Format

```yaml
research_result:
  topic: "<topic>"
  answers:
    - question: "<question>"
      answer: "<answer>"
      confidence: "high | medium | low"
      source: "<where this came from>"
  unresolved_gaps:
    - "<question that could not be answered>"
  synthesis: "<paragraph summarizing all findings>"
```

## Notes
- Always check Tier 1 (workspace) before going external — the answer is often already there.
- For large document corpora, escalate to `notebooklm` toolbox for 1M-token context analysis.
- Low-confidence answers must be flagged to the user before being acted upon.
