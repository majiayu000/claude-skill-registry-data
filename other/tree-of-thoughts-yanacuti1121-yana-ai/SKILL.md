---
name: tree-of-thoughts
description: Multi-path reasoning before acting. Agent generates 3 candidate solutions, self-scores each on correctness/token-cost/safety, selects the best branch, and backtracks if it hits a dead end. Use before /deep-heal or any complex fix. Inspired by kyegomez/TreeofThoughts (ToT) — DFS/BFS over solution space.
origin: kyegomez/TreeofThoughts (Apache 2.0) — Tree of Thoughts reasoning algorithm
license: MIT
version: 1.0.0
compatibility: Claude Code, any reasoning-heavy task
---

# tree-of-thoughts

## When to Use

- A bug fix has multiple plausible approaches and choosing wrong wastes tokens
- Architectural decisions with non-obvious tradeoffs
- Before `/deep-heal` or `autonomous-patching-loop` on complex failures
- When the linear "first idea" approach has failed twice
- Triggered by: "think through options", "tree of thoughts", "consider alternatives", "plan 3 approaches", "what's the best fix strategy", "deep reasoning", "self-critique"

## Do NOT use for

- Simple one-liner fixes where the solution is obvious
- Tasks where speed matters more than correctness (use direct approach)
- Pure data retrieval — ToT adds no value over a direct lookup
- See `research-team` for knowledge gathering phase before ToT planning

---

## Tree Structure

```
                Root Problem
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
   Branch A      Branch B      Branch C
  (Approach 1) (Approach 2) (Approach 3)
        │            │            │
   Score: 7.2    Score: 8.8   Score: 5.1
        │            │            │
   [expand]      [SELECT]     [prune]
                     │
              Sub-branch B1
              Sub-branch B2
                     │
              [verify → merge]
```

---

## Phase 1 — Generate Candidate Branches (3 approaches)

```
Prompt template for agent:

"Given: [problem description]
Context: [error message / failing test / design constraint]

Generate exactly 3 distinct approaches to solve this.
For each approach, write:
  Branch: [A|B|C]
  Strategy: [1-sentence description]
  Steps: [numbered list, max 5 steps]
  Token estimate: [rough token cost to implement]
  Risk: [low|medium|high] — explain why
  Reversible: [yes|no] — can we undo without force-push?

Do NOT implement yet. Write branches to L2 only."
```

---

## Phase 2 — Self-Score Each Branch

```python
from dataclasses import dataclass

@dataclass
class ThoughtBranch:
    label: str          # A, B, C
    strategy: str
    steps: list[str]
    token_estimate: int
    risk: str           # low | medium | high
    reversible: bool

def score_branch(branch: ThoughtBranch) -> float:
    """Score 0–10. Higher = better candidate to expand."""
    score = 10.0

    # Penalize by risk
    risk_penalty = {"low": 0, "medium": 1.5, "high": 3.5}
    score -= risk_penalty.get(branch.risk, 0)

    # Penalize non-reversible changes
    if not branch.reversible:
        score -= 2.0

    # Penalize token cost (normalized: >2000 tokens = -1 point)
    score -= min(branch.token_estimate / 2000, 2.0)

    # Penalize too many steps (complexity proxy)
    score -= max(len(branch.steps) - 3, 0) * 0.5

    return round(max(score, 0), 1)
```

---

## Phase 3 — Select Best Branch + Expand

```
Selection rule:
  1. Pick branch with highest score
  2. If top two scores differ by < 0.5 → present both to human for decision
  3. Expand selected branch into detailed implementation plan

Expansion prompt:
  "Branch [X] selected (score: [n]).
   Now expand into a concrete implementation:
   - File paths to modify
   - Exact changes per file (no code yet — describe the change)
   - Test that will confirm fix
   - Rollback plan if verification fails"
```

---

## Phase 4 — Backtrack Protocol

```
Backtrack triggers:
  □ Branch verification fails after 2 attempts
  □ Implementation reveals a hidden constraint (different root cause)
  □ Fix works but introduces a new test failure

Backtrack steps:
  1. git stash (preserve work without committing)
  2. Log: bash core/scripts/secure-logger.sh "tot-backtrack" "Branch $X failed: $reason"
  3. Return to Phase 1 — promote Branch B or C to active
  4. Write lesson to L2: "Branch A failed because <reason> — do not retry"
  5. Maximum backtracks per problem: 2 (after that, escalate to human)
```

---

## L2 Session Storage Format

```markdown
# ToT Session — [timestamp]
Problem: [description]

## Branch A (score: 7.2) — PRUNED
Strategy: ...
Reason pruned: high risk, non-reversible

## Branch B (score: 8.8) — SELECTED → EXPANDED
Strategy: ...
Steps:
  1. ...
  2. ...
Verification: run `npm test -- --grep "cache"`

## Branch C (score: 5.1) — PRUNED
Strategy: ...
Reason pruned: too many steps, high token cost

## Outcome
Result: PASS|FAIL|BACKTRACK
Lesson: [what was learned — promote to L1 if high confidence]
```

---

## Integration with /deep-heal Flow

```
User: /deep-heal "TypeError: Cannot read property 'id' of undefined"
         │
         ▼
research-team  →  gather external knowledge
         │
         ▼
tree-of-thoughts  →  plan 3 fix strategies, score, select best
         │
         ▼
autonomous-patching-loop  →  execute on isolated branch, verify
         │
         ▼
PASS → merge + L1 promotion
FAIL → backtrack to next ToT branch
```

---

## Anti-Fake-Pass Checklist

- [ ] Exactly 3 branches generated before any code is written
- [ ] Each branch scored on 3 axes: risk, token cost, reversibility
- [ ] Selected branch score is the highest (or human chose between tied branches)
- [ ] Branch plans written to L2 (`.claude/session/`) — not just printed to chat
- [ ] Backtrack limit enforced: max 2 backtracks before human escalation
- [ ] ToT session outcome (PASS/FAIL/ESCALATE) logged via `secure-logger.sh`
- [ ] Lesson from failed branches written to L2 for current session context
