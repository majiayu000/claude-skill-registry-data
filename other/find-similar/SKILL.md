---
name: find-similar
description: >-
  "Where else does this pattern appear?" - Cross-domain similarity search for
  observed patterns. Use when (1) a pattern has been noticed and needs
  verification across domains, (2) checking if a pattern is genuinely novel or
  already captured, (3) exploring whether a local observation reflects something
  universal, or (4) expanding a narrow finding into cross-domain connections.
---

# Find Similar

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during
this task you notice such a pattern emerging, it may be worth capturing.
This skill works best alongside the `vasana` skill and `vasana` hook
from the Vasana System plugin.

Modify freely. Keep this section intact.

---

## What This Skill Does

Given a pattern description, search across domains at varying "temperatures"
to find similar patterns — verifying that the pattern is real (it appears
elsewhere) or confirming it is novel (worth recording).

This is the exploration step between noticing and recording:

```
vasana (notice) → find-similar (explore) → record-pattern (capture)
```

---

## Input

A pattern description. This can come from:
- The `vasana` skill suggesting a pattern was noticed
- The user describing something they observed
- Another skill or agent flagging a recurring dynamic

The description should include:
- **What** the pattern is (the dynamic, not the content)
- **Where** it was observed (domain, context)
- **Why** it seems significant (what made it stand out)

---

## Search Temperature

Temperature controls how far afield to search. Higher temperature finds
more creative connections but with lower precision.

| Temperature | Scope | Example |
|-------------|-------|---------|
| **0.0** | Same domain | Pattern in code review → search other code review patterns |
| **0.3** | Close domains | Pattern in code review → search other collaborative review processes |
| **0.5** | Adjacent domains | Pattern in code review → search teaching, editing, peer feedback |
| **0.7** | Distant domains | Pattern in code review → search biological error correction, immune systems |
| **1.0** | Unrelated domains | Pattern in code review → search music improvisation, ecological succession |

**Default: 0.5** (adjacent domains). Adjust based on context:
- Use 0.0-0.3 when verifying a pattern is real (seeking confirmation)
- Use 0.5-0.7 when exploring connections (seeking insight)
- Use 0.7-1.0 when the pattern feels fundamental (seeking universality)

---

## Search Method

### Step 1: Search Existing Pattern Memory

Query the relational-memory MCP for known patterns:

```
mcp__relational-memory__recall(
  agent_name="vasana-observer",
  query="[pattern description]",
  n_results=10
)
```

Check if this pattern (or something structurally similar) has already been captured.

### Step 2: Search Edge Connections

Use the edge-graph MCP to find weighted connections from the pattern's domain:

```
mcp__edge-graph__find_edges(
  node="[pattern domain or concept]",
  direction="both"
)
```

Follow edges to discover domains where similar dynamics have been noted.

### Step 3: Cross-Domain Exploration

Based on the temperature setting, actively search for analogues:

**At temperature 0.0-0.3:** Search within the same domain.
- Query relational-memory with domain-specific terms
- Check the pattern library for same-domain patterns

**At temperature 0.5:** Search adjacent domains.
- Identify the *structural dynamic* (not the content)
- Search for that dynamic in neighboring fields
- Example: "productive friction" in code review → search "productive friction" in peer editing, scientific review, musical rehearsal

**At temperature 0.7-1.0:** Search distant/unrelated domains.
- Abstract the pattern to its most general form
- Search for structural isomorphisms across domains
- Example: "error correction through adversarial feedback" → immune systems, evolution, market corrections, musical dissonance resolution

### Step 4: Assess Matches

For each potential match, evaluate:

| Criterion | Question |
|-----------|----------|
| **Structural** | Is the underlying dynamic the same, or just surface similarity? |
| **Generative** | Does the connection produce new insight, or is it just clever? |
| **Testable** | Could you verify this similarity with a concrete example? |
| **Novel** | Is this connection already known, or genuinely surprising? |

---

## Output

Return a structured assessment:

```markdown
## Pattern: [name/description]

### Existing Matches
- [Match 1]: [domain] — [how it's similar] — [similarity: high/medium/low]
- [Match 2]: ...

### Novel Connections (temperature [X])
- [Connection 1]: [domain] — [structural parallel] — [insight produced]
- [Connection 2]: ...

### Assessment
- **Already captured:** [yes/no — if yes, which pattern]
- **Novel:** [yes/no — if yes, what makes it distinct]
- **Recommendation:** [record / merge with existing / explore further at higher temperature]
```

---

## Pipeline Integration

### From vasana (upstream)

When the `vasana` skill notices a pattern, it can suggest:
"This could be a pattern. Want me to check if it exists elsewhere?"

If the user approves, invoke find-similar with the pattern description.

### To record-pattern (downstream)

If find-similar determines the pattern is novel and worth preserving:
- Pass the pattern description + similarity assessment to `record-pattern`
- Include cross-domain connections as context (they enrich the pattern entry)
- If the pattern matches an existing one, suggest merging instead of creating new

### To test-pattern (validation)

If find-similar finds structural parallels across domains, these parallels
become test cases for `test-pattern` — does the pattern actually work in
those other domains, or is the similarity superficial?

---

## When NOT to Use

- Pattern is clearly domain-specific (no cross-domain relevance)
- Pattern is already well-documented in the library (check first)
- The observation is a one-off event, not a recurring dynamic
- User just wants to record without exploration (go straight to record-pattern)
