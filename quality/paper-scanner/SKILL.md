---
name: "paper-scanner"
description: "Automated academic paper and technical content scanning for the Research department. Discovers relevant papers from arXiv, conference proceedings, and tech blogs. Extracts key findings, scores applicability to CoreMind, and feeds the research self-improvement loop. Use when scanning for new research, evaluating papers, building literature reviews, or running the research UAOP pipeline."
risk: low
tags: [research, academic, papers, trends]
created: 2026-03-23
updated: 2026-03-23
---

# Paper Scanner — Research Department Intelligence Engine

Automated discovery and evaluation of research relevant to CoreMind/AION. UAOP Stage 1 for Research.

## When to use

- Weekly research scan — "anything new in multi-agent systems?"
- Before architecture decisions — "what does the research say?"
- Technology evaluation — "is this approach validated?"
- Building a literature review for a specific topic

## Pipeline

### Step 1: Scan Sources
- arXiv (cs.AI, cs.MA, cs.SE) — last 7/30 days
- Conference proceedings (NeurIPS, ICML, KubeCon, PyCon)
- Tech blogs from relevant companies (Anthropic, OpenAI, Google DeepMind)
- Industry reports (Gartner, a16z, Sequoia)

### Step 2: Filter and Score
For each paper/article:
- Relevance to CoreMind priorities (multi-agent, LLM, governance, financial ML)
- Evidence grade (A/B/C per research/rules.md)
- Applicability score (1-10): can we use this in the next 90 days?
- Implementation complexity (S/M/L)

### Step 3: Produce Research Brief
Per qualifying paper:
- One-paragraph summary (what they did, what they found)
- Key finding applicable to CoreMind
- Implementation proposal (if applicable)
- Evidence grade + confidence level

### Step 4: Self-Improvement Loop
- Track research-to-implementation conversion rate
- Reinforce sources with high conversion
- Adjust scanning keywords based on current priorities

## Cadence
```
WEEKLY:   arXiv scan + tech blog digest
MONTHLY:  Full research brief with top 10 findings
QUARTERLY: Research agenda review based on implementation outcomes
```

## Agents
| Agent | Role |
|-------|------|
| deep-research (L2) | Owns research agenda, executes scans |
| data-analyst (L2) | Evaluates quantitative findings |
| root-cause-analyst (L5) | Validates methodology quality |
| learning-guide (L5) | Creates learning paths from findings |
