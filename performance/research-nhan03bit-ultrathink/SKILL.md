---
name: research
description: Deep research with multi-source gathering, source evaluation, contradiction detection, and structured synthesis
layer: hub
category: workflow
triggers:
  - "/research"
  - "research this"
  - "look into"
  - "find out about"
  - "what is the best way to"
  - "compare options for"
  - "investigate"
inputs:
  - question: The research question or topic to investigate
  - depth: quick | standard | deep (optional, defaults to standard)
  - sources: Preferred sources to check (optional)
  - constraints: Scope limitations (time period, technology, domain)
outputs:
  - findings: Structured research findings with citations
  - sourceEvaluation: Assessment of source quality and reliability
  - synthesis: Integrated conclusions drawn from multiple sources
  - contradictions: Identified disagreements between sources
  - recommendations: Actionable recommendations based on findings
linksTo:
  - plan
  - brainstorm
  - scout
linkedFrom:
  - plan
  - brainstorm
  - cook
  - team
  - ship
  - debug
  - optimize
preferredNextSkills:
  - plan
  - brainstorm
fallbackSkills:
  - scout
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: selective
sideEffects:
  - Performs web searches
  - Fetches documentation via Context7
  - May fetch web pages
  - Produces research report in working memory
---

# Research Skill

## Purpose

Conduct structured research to answer technical questions, evaluate options, and gather evidence for decision-making. This skill goes beyond simple web searching by evaluating sources, detecting contradictions, and synthesizing findings into actionable conclusions.

Good research is not about finding the first answer. It is about finding the RIGHT answer and understanding the confidence level of that answer.

## Workflow

### Phase 1: Question Refinement

1. **Parse the research question** -- What specifically needs to be answered?
   - Is this a factual question? ("What is the max connection limit for PostgreSQL?")
   - Is this an evaluation question? ("Which ORM should we use?")
   - Is this an exploration question? ("What are the options for real-time sync?")
   - Is this a how-to question? ("How do you set up WebSocket auth?")

2. **Decompose into sub-questions** -- Complex questions often have multiple parts:
   - "Which database should we use?" decomposes into:
     - What are the requirements? (data model, scale, query patterns)
     - What are the options? (PostgreSQL, MySQL, MongoDB, etc.)
     - How do they compare on each requirement?
     - What are the operational costs of each?

3. **Identify the decision criteria** -- What matters for this research?
   - Performance? Ease of use? Community support? Cost? Security?
   - Which criteria are must-haves vs. nice-to-haves?

### Phase 2: Source Gathering

4. **Select research sources** based on the question type:

   | Source | Best For | Reliability | Tool |
   |--------|---------|------------|------|
   | Official documentation | API details, configuration, features | High | Context7 |
   | GitHub issues/discussions | Known bugs, workarounds, edge cases | Medium | Web search |
   | Stack Overflow | Common problems, quick solutions | Medium (check dates) | Web search |
   | Blog posts (official) | Architectural guidance, best practices | High | Web search |
   | Blog posts (community) | Real-world experience, tutorials | Varies | Web search |
   | Benchmarks | Performance comparisons | Medium (check methodology) | Web search |
   | Project README / changelog | Current status, breaking changes | High | Context7 / Web |
   | Academic papers | Theoretical foundations, algorithms | High | Web search |

5. **Gather information from multiple sources** -- Never rely on a single source. Use at least 2-3 independent sources for any important finding.

6. **For each source, record**:
   - URL / reference
   - Date published or last updated
   - Author / organization credibility
   - Key claims made
   - Evidence provided for those claims

### Phase 3: Source Evaluation

7. **Assess source quality** using the CRAAP test:
   - **Currency**: How recent is this? Is it still valid? (Technology moves fast -- a 2-year-old article may be outdated)
   - **Relevance**: Does it actually address our question?
   - **Authority**: Who wrote this? Are they credible in this domain?
   - **Accuracy**: Is it supported by evidence? Do other sources agree?
   - **Purpose**: Is there a bias? (Product page vs. independent review)

8. **Rate each source**: High confidence / Medium confidence / Low confidence

9. **Flag outdated information** -- Any source older than 2 years for technology topics should be verified against current documentation.

### Phase 4: Analysis

10. **Identify areas of agreement** -- What do multiple sources agree on? These are your highest-confidence findings.

11. **Identify contradictions** -- Where do sources disagree? For each contradiction:
    - What does Source A claim?
    - What does Source B claim?
    - Which source is more credible for this specific claim?
    - Is the contradiction due to different contexts, versions, or use cases?
    - Can the contradiction be resolved with more specific conditions?

12. **Identify gaps** -- What was NOT found? What questions remain unanswered? These are often as important as what was found.

13. **For evaluation questions**, build a comparison matrix:
    | Criterion | Weight | Option A | Option B | Option C |
    |----------|--------|----------|----------|----------|
    | Performance | High | Good | Excellent | Fair |
    | Ease of use | Medium | Excellent | Fair | Good |
    | Community | Medium | Large | Medium | Small |

### Phase 5: Synthesis

14. **Write the synthesis** -- Integrate findings into a coherent answer:
    - Lead with the conclusion
    - Support with evidence from sources
    - Acknowledge uncertainty and limitations
    - Note where more investigation is needed

15. **Formulate recommendations** -- Based on the findings, what should be done?
    - Primary recommendation with reasoning
    - Alternatives and when to choose them
    - Risks and caveats

16. **Produce the research report** using the template below.

## Research Report Template

```markdown
# Research Report: [Question/Topic]

## TL;DR
[One paragraph answer to the research question]

## Research Question
[The precise question being investigated]

## Methodology
- **Sources consulted**: [count]
- **Depth**: Quick | Standard | Deep
- **Date**: [research date]

---

## Findings

### Finding 1: [Title]
[Description with evidence]
**Sources**: [citation 1], [citation 2]
**Confidence**: High | Medium | Low

### Finding 2: [Title]
[Description with evidence]
**Sources**: [citation]
**Confidence**: High | Medium | Low

---

## Contradictions
| Claim | Source A Says | Source B Says | Resolution |
|-------|-------------|-------------|------------|
| [topic] | [claim] | [counterclaim] | [analysis] |

## Gaps
- [Unanswered question 1]
- [Unanswered question 2]

---

## Comparison (if evaluating options)
| Criterion | Weight | Option A | Option B |
|----------|--------|----------|----------|
| [criterion] | [H/M/L] | [rating] | [rating] |

---

## Recommendations

### Primary Recommendation
[What to do and why]

### Alternatives
- [Option B]: Choose this if [condition]
- [Option C]: Choose this if [condition]

### Risks and Caveats
- [risk 1]
- [risk 2]

---

## Sources
| # | Source | Type | Date | Confidence |
|---|--------|------|------|-----------|
| 1 | [title](url) | Documentation | [date] | High |
| 2 | [title](url) | Blog post | [date] | Medium |
| 3 | [title](url) | GitHub issue | [date] | Medium |
```

## Depth Levels

### Quick (2-3 sources, 5 minutes)
- Check official documentation via Context7
- One web search for recent community discussion
- Best for: Factual questions with clear answers

### Standard (4-6 sources, 15 minutes)
- Official documentation via Context7
- 2-3 web searches with different query angles
- Source evaluation and contradiction detection
- Best for: Evaluation questions, how-to questions

### Deep (8+ sources, 30+ minutes)
- All standard sources plus
- Academic/theoretical background
- Multiple community sources for real-world experience
- Benchmark data if applicable
- Historical context (how did we get here?)
- Best for: Architecture decisions, technology selection, complex trade-offs

## Usage

### Quick factual lookup
```
/research What is the default connection pool size in Prisma?
```

### Technology comparison
```
/research Compare tRPC vs GraphQL for a Next.js app with 20 API endpoints
```

### Best practices
```
/research What are current best practices for handling file uploads in Next.js 14?
```

### Deep investigation
```
/research deep: What are the trade-offs of edge computing vs. traditional server-side rendering for a global e-commerce platform?
```

## Examples

### Example: Technology comparison

**Question**: "Should we use Zustand or Jotai for state management?"

**Research process**:
1. Context7: Get Zustand docs (API, patterns, limitations)
2. Context7: Get Jotai docs (API, patterns, limitations)
3. Web search: "zustand vs jotai 2025 comparison"
4. Web search: "zustand jotai performance benchmark"
5. Web search: "zustand jotai migration experience"

**Synthesis**: Both are lightweight. Zustand for top-down store-based state (like Redux but simpler). Jotai for bottom-up atomic state (like Recoil but simpler). Choose based on mental model preference and existing team experience.

### Example: Resolving a contradiction

**Finding**: Source A says "Next.js middleware runs on every request." Source B says "Next.js middleware only runs on matched routes."

**Resolution**: Both are partially correct. Middleware runs on every request by default, but can be scoped with a `matcher` config. Source B was describing the configured behavior, not the default. Official docs confirm the default-runs-on-all behavior with opt-in matching.

## Guidelines

- **Always cite sources** -- Every factual claim must have a source. No hallucinating.
- **Prefer official documentation** -- Community content is useful but official docs are the ground truth.
- **Check dates** -- Technology changes fast. A 2023 article about a 2025 framework may be wrong.
- **Multiple sources for important findings** -- Never base a recommendation on a single blog post.
- **Acknowledge uncertainty** -- "I could not find reliable data on X" is more valuable than a guess.
- **Separate facts from opinions** -- "PostgreSQL supports JSONB" is a fact. "PostgreSQL is better than MongoDB" is an opinion.
- **Context matters** -- "The best database" depends entirely on the use case. Always frame recommendations within the user's context.
- **Search with specificity** -- "Next.js caching issues 2025" is better than "web framework problems."
- **Use Context7 first** -- For library/framework questions, Context7 provides authoritative documentation. Use web search for community experience and edge cases.
- **Time-box research** -- Research can expand indefinitely. Set a depth level and stick to it. More research is always possible later.
