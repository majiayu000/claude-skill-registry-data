---
name: icaire-research-lead-do-background-research
description: Research a topic, institution, visitor, publication, or policy area for ICAIRE using internal context and provided or discoverable source material. Use when the user asks for background research, a research summary, useful facts, risks, open questions, or talking points.
---

# ICAIRE Research Lead: Background Research

Produce a concise, source-aware research brief that helps ICAIRE understand
why a topic, institution, visitor, publication, or policy area matters and what
to do with it next.

## Contract

- Start from the user's research target and intended audience.
- Use BigBrain or the ICAIRE MCP connector for ICAIRE facts, people, meetings,
  initiatives, relationships, and prior context.
- Use provided source material first. When external facts are needed and source
  material is not provided, search current primary or credible sources and cite
  them.
- Separate sourced facts, ICAIRE relevance, analysis, risks, and open questions.
- Preserve uncertainty. Mark assumptions and missing information clearly.
- Keep the output practical for leadership, research, partnerships, or policy
  use rather than turning it into a generic literature essay.

## Workflow

1. Define the research target.
   - Identify whether the target is a topic, institution, visitor, publication,
     policy area, technology, event, or relationship.
   - Infer the likely use case from the user request when obvious; otherwise
     ask one short clarifying question only if the audience or decision cannot
     be reasonably assumed.
2. Gather ICAIRE context.
   - Search BigBrain or ICAIRE MCP for relevant people, meetings, initiatives,
     partners, prior notes, risks, and open tasks.
   - Do not invent ICAIRE-specific history when internal context is absent.
3. Gather source material.
   - Read all files, links, pasted text, or notes the user provides.
   - For current external facts, use web research and prioritize primary
     sources, official pages, publications, legal texts, or credible institutional
     material.
4. Extract useful facts.
   - Pull out names, dates, roles, claims, programs, relationships,
     publications, funding, mandates, and constraints that may affect ICAIRE.
   - Note source quality and whether the evidence is direct or inferred.
5. Analyze relevance.
   - Explain how the target connects to ICAIRE's research, policy, programs,
     partnerships, events, technology, or leadership priorities.
   - Identify practical opportunities, sensitivities, risks, and missing context.
6. Prepare usable outputs.
   - Include talking points or briefing questions when the target involves a
     meeting, visitor, partner, or decision.
   - Include next research steps when the evidence is incomplete.

## Output

Default to this structure unless the user requested a specific format:

- `Summary`: short answer with the most important finding.
- `Relevant Facts`: sourced facts that matter for ICAIRE.
- `ICAIRE Relevance`: why the topic matters and how it may connect to current
  work.
- `Risks And Sensitivities`: reputation, policy, partner, technical, or factual
  risks.
- `Open Questions`: what still needs confirmation.
- `Talking Points`: optional points or questions for meetings and briefings.
- `Sources`: links, file names, or internal notes used.

## Guardrails

- Do not present unsourced external claims as fact.
- Do not cite BigBrain or internal context as if it were a public source.
- Do not overfit the brief to a single source when multiple sources disagree.
- Do not hardcode ICAIRE project facts into the skill; retrieve them at runtime.
- Do not produce a long report unless the user asked for depth.
- Do not claim completion when source access failed; report what was checked and
  what remains unavailable.
