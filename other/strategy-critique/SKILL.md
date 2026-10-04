---
name: strategy-critique
category: strategy
description: >
  Reads a strategy doc and writes a red-team critique with gaps, risks, and missing
  assumptions. Adopts an adversarial but constructive stance. Use when the user says
  "strategy critique", "red team this", "critique my strategy", "find the holes",
  "stress test this plan", "what am I missing", or provides a strategy document for review.
---

# Strategy Critique

Red-team any strategy document. Find what's missing before reality does.

## Workflow

1. **Read the strategy doc** — Accept a vault path, file path, URL, or inline text. Identify:
   - Stated goals and success metrics
   - Key assumptions (explicit and implicit)
   - Proposed approach and timeline
   - Resource requirements
   - Dependencies and constraints

2. **Identify assumptions** — List every assumption the strategy relies on, including:
   - **Explicit assumptions** — stated in the doc
   - **Implicit assumptions** — unstated but required for the strategy to work
   - **Hidden assumptions** — things the author likely takes for granted

3. **Stress-test each assumption** — For each assumption:
   - How confident should we be? (HIGH / MEDIUM / LOW)
   - What evidence supports it?
   - What would falsify it?
   - What happens to the strategy if it's wrong?

4. **Find gaps** — Look for:
   - **Missing stakeholders** — who is affected but not considered?
   - **Unaddressed risks** — what failure modes aren't covered?
   - **Resource gaps** — what's needed but not budgeted?
   - **Timeline gaps** — what dependencies could cause delays?
   - **Competitive gaps** — how might competitors respond?
   - **Second-order effects** — what downstream consequences are ignored?

5. **Score overall robustness** — Rate the strategy:
   - **Assumption quality**: How solid are the foundations? (1-10)
   - **Completeness**: How many important areas are covered? (1-10)
   - **Adaptability**: How well does it handle surprises? (1-10)
   - **Overall robustness**: Weighted average (1-10)

6. **Write constructive recommendations** — For each major gap or weak assumption, suggest a concrete fix.

## Output Format

```markdown
## Strategy Critique: [Document Title]

### Summary
[2-3 sentence assessment — what's strong, what's concerning]

### Robustness Score: [X]/10
- Assumption quality: [X]/10
- Completeness: [X]/10
- Adaptability: [X]/10

### Assumptions Audit

| # | Assumption | Type | Confidence | If Wrong |
|---|-----------|------|-----------|----------|
| 1 | [assumption] | Explicit | HIGH | [consequence] |
| 2 | [assumption] | Implicit | LOW | [consequence] |

### Gaps Found

#### 1. [Gap Title]
**What's missing**: ...
**Why it matters**: ...
**Suggested fix**: ...

### Strongest Elements
- [What's genuinely well-done — be specific]

### Recommendations
1. [Highest-priority fix]
2. [Second-priority fix]
3. [Third-priority fix]
```

## Behavior

- Be adversarial but constructive — the goal is to strengthen the strategy, not tear it down
- Acknowledge what's genuinely strong before critiquing
- Distinguish between fatal flaws and nice-to-haves
- If the strategy is actually solid, say so — don't manufacture criticisms
- Save output to vault if requested: `vault/decisions/critique-[topic]-[YYYY-MM-DD].md`
