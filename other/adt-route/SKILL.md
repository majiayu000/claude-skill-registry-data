---
name: route
description: Route a task to the most fitting skill or agent. Parses user intent, checks installed-skill inventory, and picks the best match (single skill or chain).
triggers:
  - "route this task"
  - "what skill fits"
  - "pick the right skill"
  - "route me to"
---

# Route

Route a task to the most fitting skill or agent. Meta-router above `dispatch`. Parses the user intent, checks the installed-skill inventory, and picks the best match (single skill or chain). If fuzzy, runs `recall` first.

## Purpose

Eliminate ambiguity when a task could fit multiple skills or agents. Route makes the decision, either immediately (high confidence) or after a quick context-pack query (low confidence).

## When to use

- "I need to refactor the auth module but I'm not sure what approach"
- "Is this a testing problem or a design problem?"
- "Which skill handles this better: security-audit or code-review?"

## Decision Protocol

1. **Parse intent** — Extract primary verb (implement, fix, refactor, test, deploy, document, review) and object (code, config, feature, test, docs, infra).
2. **Check skill inventory** — Query `~/.claude/skills/` dirs + `/packages/core/kit/core/skills/` for matching trigger keywords.
3. **Score matches** — Confidence based on trigger word overlap + description relevance.
4. **High confidence (≥0.85)** — Fire the skill immediately, no additional input.
5. **Medium confidence (0.65–0.84)** — Run `recall` to pull context, then decide.
6. **Low confidence (<0.65)** — Ask user for clarification or suggest top 3 candidates.

## Output

- **Single skill** → "Routing to `/security-audit`. Running now." + auto-invoke
- **Chain** → "This needs 2 steps: 1) `code-review`, then 2) `simplify`" + invoke in order, await completion
- **Ambiguous** → "Could be `test-driven-development` or `architecture-patterns`. Which fits?"

## Example Invocations

```
User: "Route: I'm rewriting a REST API to GraphQL"
Route: Queries skill inventory, finds `api-design-principles`, scores 0.89
Output: "Routing to `api-design-principles`. Invoking now."

User: "Route: Weird test timeout, maybe a race condition or a real bug?"
Route: Scores `systematic-debugging` 0.78, `test-driven-development` 0.72
Output: Runs recall("test timeout race condition"), gets pattern context
Output: "Likely a race in beforeEach/afterEach. Routing to `systematic-debugging`."

User: "Route: Need to set up GitHub Actions for monorepo CI"
Route: Finds `ci-watch` (0.82), `turborepo` (0.75), `deploment-automation` (0.71)
Output: "Multiple fits. Suggest: 1) `turborepo` (monorepo structure), 2) `ci-watch` (CI flow), or a chain. Which?"
```

## References

- Skill inventory: `~/.claude/skills/` (local) + `packages/core/kit/core/skills/` (toolkit)
- Auto-invoke rules: `~/.claude/standards/skill-auto-invoke.md`
- Dispatch skill: `dispatch` (lower-level routing)
- Context retrieval: `recall` (pulls RAG index)
