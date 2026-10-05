---
slug: shadows-deep-research
version: 1.1.1
displayName: 深度研究（Shadows Deep Research）
summary: 4轮深度研究协议，包括探索、魔鬼代言人、多视角综合和结晶，适用于重大架构决策、技术选择和战略问题。
tags: clawhub
---

# Deep Research — 4-Round Exploration Protocol

**Version**: 1.1.0 | **Author**: Shadows Company | **License**: MIT

---

## WHEN TO TRIGGER

- Major architectural decision (monolith vs microservices, framework choice)
- Technology evaluation (comparing databases, languages, cloud providers)
- Strategic planning requiring deep analysis
- User says "deep research", "explore deeply", "analyze thoroughly"
- Complex problem with no obvious solution

## WHEN NOT TO TRIGGER

- Simple factual questions
- Quick bug fixes or small code changes
- User wants a fast answer, not a deep dive

---

## PREREQUISITES

No binaries required. This skill uses only the agent's reasoning and search capabilities. It does not execute code, access the filesystem, or require any external tools.

---

## PROTOCOL — 4 ROUNDS

### Round 1 — EXPLORER

**Goal**: Map the landscape exhaustively.

1. Search for existing solutions, papers, articles, repos
2. Identify all major approaches and frameworks
3. List key players, tools, and technologies
4. Note emerging trends and experimental approaches
5. Collect data points: performance, adoption, community size

**Output**: Landscape map with 5-10 options discovered.

### Round 2 — DEVIL'S ADVOCATE

**Goal**: Stress-test every option ruthlessly.

For each option from Round 1:
1. What could go wrong? (failure modes)
2. What are the hidden costs? (maintenance, vendor lock-in, learning curve)
3. What are the scaling limits?
4. Who tried it and failed? Why?
5. What does the opposition say?

**Output**: Risk matrix — each option with 3-5 identified weaknesses.

### Round 3 — MULTI-PERSPECTIVE SYNTHESIS

**Goal**: Evaluate from 5 different viewpoints.

Analyze remaining options through these lenses:
1. **Engineer**: Technical merit, DX, testability, performance
2. **Architect**: Scalability, extensibility, integration patterns
3. **Product**: Time-to-market, user impact, iteration speed
4. **Security**: Attack surface, data flow, compliance
5. **Business**: Cost, hiring market, ecosystem maturity

**Output**: Perspective matrix — scores per option per viewpoint.

### Round 4 — CRYSTALLIZE

**Goal**: Produce a clear, actionable recommendation.

1. Synthesize all rounds into a decision framework
2. Rank final options with explicit scoring criteria
3. Declare a primary recommendation with confidence level
4. Define a fallback option
5. List concrete next steps (PoC tasks, benchmarks to run)

**Output**: Decision document with recommendation + action plan.

---

## RULES

1. **Complete all 4 rounds** — never skip, even if answer seems obvious early
2. **Evidence-based** — every claim must cite a source or data point
3. **Contrarian thinking** — actively seek arguments against your preferred option
4. **No premature convergence** — Round 1-2 must remain open, narrowing only in Round 3-4
5. **Actionable output** — final round must include concrete next steps

---

## SECURITY CONSIDERATIONS

This is a pure reasoning and analysis skill. It has zero code execution, zero network access, zero file modification, and zero persistence. The agent uses only its reasoning capabilities and available search tools to gather and synthesize information. This skill carries the lowest possible risk profile.

- **Commands executed**: None
- **Data read**: None (agent reasoning only)
- **Network access**: Only via agent's built-in search tools (not direct)
- **Persistence**: None
- **Credentials**: None required

---

## OUTPUT FORMAT

```markdown
# Deep Research: [Topic]

## Round 1 — Landscape
[Options discovered with brief descriptions]

## Round 2 — Stress Test
[Risk matrix for each option]

## Round 3 — Multi-Perspective Analysis
| Option | Engineer | Architect | Product | Security | Business |
|--------|----------|-----------|---------|----------|----------|
| ...    | ...      | ...       | ...     | ...      | ...      |

## Round 4 — Recommendation
**Primary**: [Option] (Confidence: X/10)
**Fallback**: [Option]
**Next Steps**:
1. [Action item]
2. [Action item]
3. [Action item]
```

---

**Published by Shadows Company — "We work in the shadows to serve the Light."**
