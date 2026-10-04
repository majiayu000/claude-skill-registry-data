---
name: infra-kit.workflow.research
description: Research infrastructure topics with source quality, version awareness, and actionable recommendations backed by citations.
---

# Infrastructure Research

Use this skill when the user asks for recommendations that depend on external documentation or evolving ecosystems: cloud features, Kubernetes APIs, Gateway/Ingress behaviors, Terraform provider attributes, security controls, or industry practices.

The output should be a short, cited research brief plus an experiment/validation plan.

## Output Rules

- Always write deliverables to one or more Markdown files in the repo (do not only respond in chat).
- If the research is large, split it into multiple files (e.g., `00-context.md`, `01-options.md`, `02-recommendation.md`, `03-validation-plan.md`).
- Prefer a stable location such as `docs/infra-research/<topic>/`.

## Outcomes

- Produce a recommendation with explicit trade-offs and constraints
- Cite primary sources (vendor docs, upstream project docs, RFC/KEP) and record versions/dates
- Identify what is unknown and propose the smallest test to answer it

## Where This Fits In The Flow

- Use when the right decision depends on versions, vendor defaults, quotas, or subtle behavior.
- Use to de-risk `infra-kit.workflow` planning by producing a cited recommendation plus a validation plan.

## Workflow

1. Clarify the research question:
   - what decision will this inform
   - what environment (cloud, region, k8s distro, versions)
2. Identify constraints and evaluation criteria.
3. Gather sources (prefer in this order):
   - official vendor documentation
   - upstream project docs / release notes
   - standards (RFCs) / Kubernetes KEPs when relevant
   - high-quality third-party writeups only for context, not as authority
4. Extract facts:
   - version-specific behavior
   - limits/quotas
   - security implications
   - operational impacts
5. Compare options and produce a recommendation.
6. Provide a validation plan:
   - how to test (PoC steps)
   - what success looks like
   - what would falsify the recommendation

## Source Quality Rules

- Prefer sources that match the user's version and provider.
- Always include links and (when available) the doc version or last-updated date.
- If sources conflict, say so and propose how to resolve (test, issue tracker, release notes).

## Hallucination Guardrails

- Do not guess provider/resource arguments or defaults; cite docs.
- Do not present third-party blog content as official behavior.
- If sources cannot be fetched, say so and limit output to what is known.

## Research Brief Format

- Question:
- Context (versions, environment):
- Recommendation:
- Key evidence (links):
- Trade-offs:
- Risks:
- Validation plan:
- Open questions:

## References
