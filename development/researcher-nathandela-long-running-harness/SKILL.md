---
name: Researcher
description: Deep research producing structured survey documents for informed decision-making
---

# Researcher Skill

## Overview
Conduct deep research on a topic and produce a structured survey document following the project's research template. This skill spawns parallel research subagents to gather comprehensive information, then synthesizes findings into a PhD-depth document stored in `docs/research/`.

## Methodology
1. Identify the research question, scope, and exclusions
2. Search memory with `ca search` for existing knowledge on the topic
3. Spawn parallel research subagents via Task tool:
   - **Web search specialist**: Uses WebSearch/WebFetch for academic papers, blog posts, benchmarks, and tools
   - **Codebase explorer**: Uses `subagent_type: Explore` to find relevant existing code patterns
   - **Docs scanner**: Reads `docs/` for prior research, ADRs, and standards that inform the topic
4. Collect and deduplicate findings from all subagents
5. Synthesize into TEMPLATE_FOR_RESEARCH.md format:
   - Abstract (2-3 paragraphs)
   - Introduction (problem statement, scope, definitions)
   - Foundations (theoretical background)
   - Taxonomy of Approaches (classification framework, visual table/tree)
   - Analysis (one subsection per approach with theory, evidence, implementations, strengths/limitations)
   - Comparative Synthesis (cross-cutting trade-off table)
   - Open Problems & Gaps
   - Conclusion
   - References (full citations)
   - Practitioner Resources (annotated tools/repos)
6. Store output at `docs/research/<topic-slug>.md` (kebab-case filename)
7. Report key findings back for upstream skill (spec-dev/plan) to act on

## Memory Integration
- Run `ca search` with topic keywords before starting research
- Check for existing research docs in `docs/research/` and `docs/compound/research/` that overlap
- After completion, key findings can be captured via `ca learn`

## Docs Integration
- Scan `docs/research/` and `docs/compound/research/` for prior survey documents on related topics
- Check `docs/decisions/` for ADRs that inform or constrain the research scope
- Reference existing project docs as primary sources where relevant

## Output Format

Every research document MUST follow this exact structure:

# [Topic Title]

*[Date]*

## Abstract
2-3 paragraph summary: what this survey covers, main approaches, key trade-offs.

## 1. Introduction
- Problem statement
- Scope: covered and excluded
- Key definitions

## 2. Foundations
Theoretical background. Assume technical reader, not domain specialist.

## 3. Taxonomy of Approaches
Classification framework. Present visually (table or tree) before details.

## 4. Analysis
One subsection per approach:
### 4.x [Approach Name]
- **Theory & mechanism**
- **Literature evidence**
- **Implementations & benchmarks**
- **Strengths & limitations**

## 5. Comparative Synthesis
Cross-cutting trade-off table. No recommendations.

## 6. Open Problems & Gaps
Unsolved, under-researched, or risky areas.

## 7. Conclusion
Synthesis. No verdict.

## References
Full citations with URLs.

## Practitioner Resources
Annotated tools, repos, articles grouped by category.

## Common Pitfalls
- Shallow treatment: each approach needs theory, evidence, AND implementation examples
- Missing taxonomy: always classify approaches before diving into analysis
- Recommendation bias: present trade-offs, never recommend (ADR process decides)
- Ignoring gaps: explicitly state where evidence is thin or conflicting
- Not deduplicating subagent findings (leads to repetitive content)
- Skipping the comparative synthesis table

## Quality Criteria
- PhD academic depth (reads like a technical survey paper)
- Multiple research subagents were deployed in parallel
- Memory was searched for existing knowledge
- Existing docs/research were checked for overlap
- Every approach has: theory, evidence, implementations, strengths/limitations
- Comparative synthesis table present with clear trade-offs
- Open problems honestly identified
- Full references with URLs
- Practitioner resources annotated
- No recommendations -- landscape presentation only
