---
name: research-team
description: Autonomous multi-source research agent group. Given an unknown bug or technology topic, research-team spawns parallel sub-agents to search StackOverflow, GitHub Issues, official docs, and changelogs. Synthesizes findings into a ranked solution report. Inspired by assafelovic/gpt-researcher closed-loop research architecture.
origin: assafelovic/gpt-researcher (Apache 2.0) — multi-source parallel research loop
license: MIT
version: 1.0.0
compatibility: Claude Code, any project
---

# research-team

## When to Use

- An unknown bug has no match in L1 memory — need external knowledge
- A library has released a new version and APIs may have changed
- You need to compare multiple solutions before committing to one
- Triggered by: "research this", "find a fix for", "investigate", "what's the best approach for", "look up", "research team", "autonomous research"

## Do NOT use for

- Known bugs already documented in L1 (`core/memory/L1/`) — read L1 first
- Simple API lookups that a single WebSearch handles
- Tasks requiring code execution — hand off to `autonomous-patching-loop` after research
- See `ingest-repo` for structured code-level repo analysis

---

## Team Roles

```
Researcher-A  → searches StackOverflow + GitHub Issues for the exact error
Researcher-B  → reads official docs / changelog for the library version in use
Researcher-C  → searches for alternative approaches / known workarounds
Synthesizer   → cross-references all 3 findings, ranks solutions by reliability
```

---

## Research Loop Architecture

```python
# Conceptual: multi-agent research pipeline (adapt to Claude Code subagents)

from dataclasses import dataclass
from typing import Callable

@dataclass
class ResearchQuery:
    topic: str
    context: str        # error message / file / line number
    library: str        # e.g. "react@18.3.0"
    max_sources: int = 10

def research_team(query: ResearchQuery, search_fn: Callable) -> dict:
    """
    Parallel research across 3 lanes, then synthesize.
    """
    # Lane A: Stack-style QA
    lane_a = search_fn(f"{query.topic} site:stackoverflow.com OR site:github.com/issues")

    # Lane B: Official docs + changelog
    lane_b = search_fn(f"{query.library} changelog deprecation {query.topic}")

    # Lane C: Alternative approaches
    lane_c = search_fn(f"alternative to {query.topic} {query.library} workaround")

    # Synthesizer: rank by recency + vote count + library version match
    all_results = lane_a + lane_b + lane_c
    ranked = sorted(
        all_results,
        key=lambda r: (r.get("votes", 0) + r.get("recency_score", 0)),
        reverse=True
    )[:query.max_sources]

    return {
        "query": query.topic,
        "sources": len(ranked),
        "top_solution": ranked[0] if ranked else None,
        "alternatives": ranked[1:3],
        "confidence": "high" if len(ranked) >= 5 else "medium",
    }
```

---

## Claude Code Subagent Pattern

```
# ORCHESTRATOR prompt to spawn research-team
Task: Bug in [library]@[version]: [error message]

Spawn 3 parallel research agents:

Agent-A: Search StackOverflow and GitHub Issues for exact error.
  Query: "[error message] [library]"
  Output: top 3 matches with URL + date + vote count → write to .claude/signals/research-a.json

Agent-B: Read official docs/changelog for [library]@[version].
  Focus: breaking changes, deprecated APIs, migration guides.
  Output: relevant section → write to .claude/signals/research-b.json

Agent-C: Find alternative approaches for [topic] that avoid the error.
  Output: top 2 alternatives → write to .claude/signals/research-c.json

Synthesizer (after A+B+C complete):
  Read all 3 signal files.
  Rank solutions by: recency > vote count > version match.
  Write final report to .claude/signals/research-report.md
  Promote confirmed fix to L1: bash core/scripts/add-fact.sh "bug-fix" "<solution>" "high"
```

---

## Output Report Format

```markdown
# Research Report — [topic]
Date: [timestamp]  Sources scanned: [n]  Confidence: high|medium|low

## Recommended Fix
[Solution text + code snippet]
Source: [URL] ([date], [votes] votes)

## Why This Works
[1-2 sentence explanation tied to the library's behavior]

## Alternative Approaches
1. [Alt A] — [tradeoff]
2. [Alt B] — [tradeoff]

## Outdated / Rejected Solutions
- [Stack answer from 2020] — library API changed in v18, no longer applicable

## L1 Promotion
[ ] Promoted to core/memory/L1/ — bash core/scripts/add-fact.sh "bug-fix" "..." "high"
```

---

## Integration with autonomous-patching-loop

```
research-team  →  finds solution
       │
       ▼
autonomous-patching-loop  →  applies fix on isolated branch
       │
       ▼
verify gate passes  →  merge + L1 promotion
```

---

## Anti-Fake-Pass Checklist

- [ ] At least 3 sources consulted (not just 1 web search)
- [ ] Results filtered for library version match — old answers flagged as "may be outdated"
- [ ] Confidence level stated: high (≥5 sources), medium (3–4), low (<3)
- [ ] Rejected/outdated solutions documented — not silently dropped
- [ ] Confirmed fix promoted to L1 via `add-fact.sh`
- [ ] Report written to `.claude/signals/research-report.md` — not left in chat only
- [ ] Agent does NOT apply the fix directly — hands off to `autonomous-patching-loop`
