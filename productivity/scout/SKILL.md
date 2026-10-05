---
name: mk:scout
description: Fast parallel codebase scouting. Spawns multiple Explore subagents to search directories simultaneously, returning a consolidated file map with architecture fingerprint, complexity estimates, and routing suggestions. Use before planning, debugging, or any task spanning multiple directories. NOT for reading a single known file in depth (use Read directly); NOT for semantic find-usages or go-to-definition.
source: local
keywords:
  - scout
  - codebase-search
  - parallel-explore
  - file-mapping
  - architecture-fingerprint
  - routing-suggestions
when_to_use: Use before planning/debugging or any task spanning multiple directories — fast parallel codebase scouting. NOT for reading a single known file (use Read directly) or semantic find-usages.
user-invocable: true
meowkit:
  portability: provider-only
  providers:
    include:
      - claude-code
  requires:
    surfaces:
      - skills
    commands:
      - Agent
      - Grep
      - Glob
  context_cost: medium
owner: research
criticality: medium
status: active
runtime: claude-code
context_cost: medium
---

# Scout

Fast, parallel codebase exploration using Explore subagents. Divides the project into segments, searches them simultaneously, and returns a consolidated report.

## When to Use

- Starting a feature that spans multiple directories
- User asks to "find", "locate", or "search for" files
- Before planning (Phase 1) on complex tasks — understand what exists first
- Debugging session requiring file relationship understanding
- User asks about project structure or where functionality lives

## Workflow Integration

Operates in **Phase 0 (Orient)** and **Phase 1 (Plan)**.

- Orchestrator invokes scout before planner on COMPLEX tasks
- Planner may invoke scout when the technical approach needs codebase understanding
- Developer may invoke scout when implementation touches unfamiliar areas

## Quick Start

```
/mk:scout authentication      → find all auth-related files
/mk:scout database migrations  → find DB migration files
/mk:scout [any search target]  → parallel search across codebase
```

## Scout Process

1. **Analyze** — parse user prompt, identify search targets (keywords, file types)
2. **Determine scale** — calculate SCALE using formula in `references/scouting-strategy.md`
3. **Apply search scope** — include Tier 1 always, Tier 2 if task-relevant, exclude Tier 3 always (see `references/search-scope.md`)
4. **Divide directories** — assign each Explore agent a distinct scope (no overlap)
5. **Spawn agents** — all in a single message for parallel execution (see `references/scouting-strategy.md`)
6. **Collect results** — deduplicate, merge, note gaps/timeouts
7. **Build report** — fill structured template (see `references/report-and-handoff.md`)
8. **Execute handoff** — route to next agent per handoff protocol

## References

Load these **only when executing** the corresponding step — not upfront.

| Reference                                                       | When to load                    | What it contains                                                                                                  |
| --------------------------------------------------------------- | ------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **[search-scope.md](./references/search-scope.md)**             | Step 3 — applying scope rules   | Tier 1/2/3 directory lists, justification, exclusion patterns                                                     |
| **[scouting-strategy.md](./references/scouting-strategy.md)**   | Steps 2, 4, 5 — spawning agents | SCALE formula, directory division rules, Explore agent prompt template, parallel execution, file reading patterns |
| **[report-and-handoff.md](./references/report-and-handoff.md)** | Steps 7, 8 — writing output     | Report template with all sections, handoff protocol per phase, memory integration, context budget                 |

## Constraints

- **Read-only** — scout NEVER modifies files
- **Maximum 6 parallel agents** — beyond this, aggregation cost exceeds benefit
- **3-minute timeout** per agent — skip non-responders, don't retry
- **No external tool dependencies** — uses only the host runtime's built-in Explore
- **Security** — never access .env, credentials, or SSH keys during scouting
- **Tier 3 always excluded** — no exceptions regardless of task

## Gotchas

- **6-agent cap vs 3-agent rule** — `parallel-execution-rules.md` Rule 2 caps parallel agents at 3, but that rule governs write-capable agents (merge-conflict risk). Scout uses read-only Explore subagents which don't produce conflicts, so the 6-agent ceiling here is intentional, not a rule violation.
- **Subagents returning partial results**: Context window exceeded, agent returns truncated output → Set explicit file count limits per subagent; merge results with dedup
- **Missing hidden files in directory scan**: Default glob patterns skip dotfiles → Include dotfiles explicitly when scanning config directories
