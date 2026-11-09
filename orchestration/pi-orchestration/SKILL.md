---
name: pi-orchestration
description: Route tasks among Pi custom subagents with minimal cost and clear boundaries. Use when the task concerns pi orchestration.
---
# Pi multi-agent orchestration

- Custom roles live in `~/.pi/agent/agents/*.md`, discovered by `pi-subagents`,
  not by base Pi. Install the package explicitly before expecting delegation.
- `engineer`: one implementation owner. `explore`: read-only code paths.
  `research`: current facts with cited sources. `advisor`: material design tradeoff.
  `fixer`: narrow hard blockers. `review`: evidence-based changed-code audit.
  `oracle`: scarce independent opinion for unresolved high-impact uncertainty.
- Use the same provider/model by default; do not hard-code unavailable expensive
  models or run many agents on trivial tasks.
- Read-only roles have tool allowlists. Pass changed diff to `review` because
  it cannot execute Git commands.
- Subagents need explicit context inheritance; settings in role frontmatter
  enable trusted global and repository instructions.
- Do not let independent workers edit the same checkout concurrently; use a
  preapproved worktree per writer if parallel writes are necessary.
