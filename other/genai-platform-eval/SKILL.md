---
name: genai-platform-eval
description: Use when evaluating, comparing, researching, or preparing vendor questions for Generative AI platforms, AI services, orchestration layers, agent frameworks, or AI tooling adoption. Provides a structured scope-research-synthesis workflow covering governance, integrations, tenancy, portability, compliance, pricing, accuracy controls, DevOps maturity, and vendor viability across internal enterprise, B2B SaaS embedding, consumer-facing, and hybrid deployment models.
version: 1.0.0
author: Tony Semana
license: MIT
metadata:
  hermes:
    tags: [genai, evaluation, platform-assessment, vendor-research, ai-governance]
    related_skills: []
---

# GenAI Platform Evaluation Framework

## Overview

This skill guides a structured evaluation of Generative AI platforms, orchestration layers, agent frameworks, or AI services. Use it to turn a broad adoption question into a defensible evaluation artifact: scope, research findings, vendor questions, architectural risks, and a prioritized gap list.

The workflow has three phases:

1. **Scope the evaluation** — clarify the deployment model, data stack, target platform, stakeholders, and decision being supported.
2. **Research and document** — work through the evaluation domains in `references/evaluation-domains.md`, separating confirmed evidence from inferred or absent capabilities.
3. **Synthesize and deliver** — produce an internal briefing, vendor-call question package, buy-vs-build analysis, or docx-ready report.

The goal is not a generic feature checklist. The goal is to determine whether the platform fits the organization's actual architecture, risk model, operating model, commercial model, and deployment path.

## When to Use

Use this skill when the user asks to:

- Evaluate, compare, assess, or research an AI platform, AI vendor, agent framework, orchestration tool, LLM gateway, AI governance layer, or GenAI service.
- Prepare for a vendor meeting or diligence call with specific questions.
- Create a technology assessment for AI tooling adoption.
- Build a buy-vs-build analysis for an AI platform capability.
- Assess fit for internal enterprise use, B2B SaaS embedding, consumer-facing AI features, or hybrid deployment models.
- Identify unresolved risks before a pilot, procurement decision, architecture review, or executive briefing.

Do **not** use this skill for:

- Narrow model-quality evaluations where the platform, governance, tenancy, pricing, and operating model are out of scope.
- Pure benchmark work focused only on model metrics.
- General AI market research with no adoption or architecture decision attached.

## Phase 1: Scope the Evaluation

Before researching anything, establish the evaluation context. These inputs determine which domains are primary, secondary, or skippable.

### 1. Identify the deployment model

Ask which deployment model best describes the situation:

- **Internal enterprise** — AI capabilities used by employees, analysts, operations, or internal teams. Governance, identity, compliance, development experience, and data integration are usually primary.
- **B2B SaaS embedding** — AI capabilities embedded inside a product sold to many external customers or tenants. Multi-tenancy, data isolation, API-first architecture, OEM pricing, white-labeling, auditability, and downstream customer assurances become primary. This is usually the most architecturally demanding model.
- **Consumer-facing product** — AI features exposed directly to end users. Latency, accuracy, scale, content safety, cost, and rollback/change management are primary.
- **Hybrid** — Multiple deployment models are in play. Evaluate against the most demanding model first, then check for gaps in the others.

If the user is unsure, proceed with a stated assumption and mark deployment-model uncertainty as an open question.

### 2. Map the data stack

Capture the current or expected data infrastructure. Include:

- Databases and operational systems.
- Data warehouses and data lakes.
- Transformation tools.
- ETL/ELT or ingestion pipelines.
- Event streaming systems.
- Existing AI/ML tools, vector stores, model gateways, or governance layers.
- Identity providers, secrets managers, audit/SIEM systems, and observability tooling.

For each component, note whether it sits at the storage, transformation, movement, streaming, governance, observability, or application layer. This inventory determines which integration and identity questions to prioritize.

### 3. Identify the evaluation target

Gather:

- Vendor name.
- Product or platform name.
- Public documentation URLs.
- Pricing pages, security pages, trust center, API docs, SDK docs, and architecture docs if available.
- Whether the evaluation is single-vendor or comparative.

For multi-vendor comparisons, apply the framework independently to each platform, then synthesize a comparison table only after researching each one on its own terms.

### 4. Define stakeholder context

Clarify:

- Who requested the evaluation.
- Who will read the output.
- What decision it supports: buy/no-buy, pilot scope, architecture review, procurement negotiation, risk acceptance, partner diligence, or build-vs-buy.
- Whether the intended output is a short briefing, a detailed report, a vendor question list, a comparison matrix, or a docx-ready artifact.

## Phase 2: Research and Document

Read `references/evaluation-domains.md` before starting research. It contains the full domain taxonomy, what to look for in each domain, and deployment-specific priority guidance.

For each relevant domain:

1. **Research public materials** — Use public documentation, security pages, pricing pages, changelogs, blog posts, case studies, analyst coverage, marketplace listings, and credible third-party coverage.
2. **Document findings** — Summarize what the evidence shows. Name features, exact product terms, pricing units, certification names, version numbers, API capabilities, or published limits where possible.
3. **Separate confirmed, inferred, and absent** — Use clear labels:
   - **Confirmed** — directly supported by cited public materials.
   - **Not confirmed** — plausible from adjacent evidence, but not explicitly documented.
   - **Not found** — no public evidence found after reasonable search.
4. **Draft follow-up questions** — Target the gap between vendor claims and the organization's requirements.

### Research discipline

- **Distinguish claims from architecture.** Vendor language like “enterprise-grade” or “secure by design” is not enough. Look for where policies are enforced, how identity flows, how audit logs are structured, and which controls are configurable.
- **Note what is absent.** Silence in documentation is itself a finding, especially for tenancy, data training, audit export, pricing, rollback, and exit strategy.
- **Attribute specifics.** Dates, versions, connector counts, pricing tiers, certification names, marketplace listings, and published limits make the assessment useful later.
- **Prefer primary sources.** Use vendor docs and trust-center materials first; use blogs, analyst notes, and third-party coverage as supporting context.
- **Avoid overclaiming.** Do not infer production readiness from demo videos, marketing screenshots, or isolated case studies.

## When to Read the Reference Files

- **`references/evaluation-domains.md`** — Read at the start of Phase 2. Contains the full taxonomy of evaluation domains, what to research in each, and which domains matter most for each deployment model.
- **`references/question-bank.md`** — Read when drafting follow-up questions. Contains proven question patterns organized by domain, drawn from real enterprise AI evaluations.

## Evaluation Domains

Use `references/evaluation-domains.md` as the source of truth for domain details. At minimum, consider these categories:

### Tier 1: Always Evaluate

- Platform identity and market position.
- Development experience.
- Integration and connector ecosystem.
- Governance, policy enforcement, and identity.
- Vendor lock-in, portability, and exit strategy.
- Compliance, data residency, and data training.

### Tier 2: Deployment-Dependent

- Multi-tenancy and data isolation.
- Pricing and commercial model.
- API-first architecture and product embedding.

### Tier 3: Augmented Concerns

- Agent accuracy and hallucination controls.
- Rollback and change management.
- Latency and performance at scale.
- Company maturity and viability.
- Build vs. buy framing.

## Phase 3: Synthesize and Deliver

### 1. Prioritize gaps

After completing domain research, rank unresolved questions by decision impact. The top items should be potential blockers if answered unfavorably. Lower-priority items may still matter, but should not distract from deal-shaping or architecture-shaping gaps.

Weight domains by deployment model using the priority guidance in `references/evaluation-domains.md`. For example:

- B2B SaaS embedding should heavily weight multi-tenancy, data isolation, OEM pricing, API control, white-labeling, audit evidence, and downstream customer assurances.
- Internal enterprise should heavily weight governance, identity, data integration, compliance, development experience, and portability.
- Consumer-facing products should heavily weight latency, accuracy, scale, rollback, safety, and cost behavior.

### 2. Build the evaluation artifact

Produce the requested output format. If the user does not specify a format, default to a structured markdown report that is easy to convert into a document.

Recommended structure:

```text
Title: [Platform Name] Evaluation
Subtitle: [Purpose] | [Organization Name] | [Date]

1. Executive Summary
   - Recommendation or current read
   - Top strengths
   - Top unresolved risks
   - Decision the report supports

2. Platform Overview
   - What the platform is
   - Key components
   - Market positioning
   - Deployment model fit

3. Prepared Questions & Research
   - One section per evaluated domain
   - Each section includes: What We Found, Evidence, Questions for the Vendor

4. Strategic & Architectural Concerns
   - Deeper analysis of domains that intersect with the organization's deployment model and data stack

5. Commercial and Operating Model Considerations
   - Pricing, scale assumptions, support model, procurement concerns, rollout/rollback, ownership

6. Summary: Prioritized Gaps to Resolve
   - Ranked list with impact and why it matters

7. Appendix
   - Source list
   - Assumptions
   - Skipped domains and rationale
```

### 3. Voice and audience

Write as an internal report prepared by an evaluator for colleagues. Use first-person plural when referring to the evaluating organization when appropriate: “we,” “our team,” or the organization’s name. Refer to the vendor by name.

Do not address the reader as “you.” The reader is a colleague, executive, architect, or procurement stakeholder, not a student.

When drafting vendor questions, frame them as discussion points from an informed buyer. Good questions are specific, evidence-driven, and tied to adoption risk.

Examples:

- Weak: “Do you support governance?”
- Strong: “Where in the execution path are policy rules evaluated: before tool invocation, after model output, or both? Can policy decisions and tool-call parameters be exported to our SIEM?”

- Weak: “Is your platform multi-tenant?”
- Strong: “Can a single agent definition serve multiple customer tenants while enforcing tenant, parent-organization, and business-line isolation at runtime? What audit evidence proves isolation was maintained?”

## Output Patterns

### Vendor-call briefing

Use when the user needs to prepare for a meeting. Keep it concise:

- Platform overview.
- What public materials confirm.
- Highest-risk unknowns.
- Meeting questions grouped by domain.
- Follow-up artifacts to request: architecture diagram, security whitepaper, sample audit log, pricing model, API docs, customer references.

### Adoption assessment

Use when the user needs a recommendation:

- Executive summary.
- Fit by deployment model.
- Strengths.
- Risks and gaps.
- Architecture implications.
- Cost/commercial implications.
- Recommendation: proceed, pilot with constraints, hold, or reject.

### Comparison matrix

Use when evaluating multiple platforms:

- Normalize domains across vendors.
- Avoid false precision. Use clear labels: strong, adequate, weak, not confirmed, not found.
- Keep evidence links attached to each cell or row.
- Add a narrative summary explaining tradeoffs rather than relying only on scores.

### Buy-vs-build analysis

Use when the organization could plausibly build the capability:

- Identify which platform capabilities are commodity versus differentiating.
- Estimate integration burden, governance burden, and operational burden.
- Compare dependency risk against engineering cost.
- Identify open standards, open-source components, and exit paths.
- Ask what the organization would lose by building on open standards instead.

## Common Pitfalls

1. **Starting with a feature checklist instead of deployment context.** The same platform can be suitable for internal enterprise use and unsuitable for B2B SaaS embedding. Scope first.

2. **Treating model portability as full portability.** Switching LLM providers is not enough. Agent definitions, policies, knowledge, audit logs, and operational data also need an exit path.

3. **Accepting “enterprise-grade” without enforcement detail.** Governance matters only if the platform can show where policy is evaluated, how identity is propagated, and how violations are prevented before execution.

4. **Underweighting pricing for embedded use cases.** Standard enterprise SaaS pricing often breaks when the buyer is embedding AI capabilities into a product used by many downstream tenants.

5. **Ignoring absent documentation.** If public docs do not mention audit export, rollback, data training commitments, or tenancy isolation, that absence should become a vendor question.

6. **Over-scoring a platform because it has many integrations.** Connector count matters less than depth, auth model, custom connector governance, and fit with the actual data stack.

7. **Mixing confirmed facts with assumptions.** Label inferred capabilities clearly. Do not let plausible assumptions become findings.

8. **Skipping operational maturity.** Rollback, versioning, monitoring, support, and incident response determine whether the platform can be trusted in production.

9. **Writing vendor questions that are too broad.** Questions should be tied to the organization’s deployment model and should force concrete answers, examples, artifacts, or commitments.

10. **Forgetting the source list.** Evaluations age quickly. Include enough citation context for a future reader to understand what evidence existed at the time.

## Verification Checklist

- [ ] Deployment model is identified or assumptions are explicit.
- [ ] Data stack and integration targets are captured.
- [ ] Evaluation target and decision context are clear.
- [ ] `references/evaluation-domains.md` was reviewed before domain research.
- [ ] `references/question-bank.md` was reviewed before drafting vendor questions.
- [ ] Findings are labeled as confirmed, not confirmed, or not found.
- [ ] Vendor questions target evidence gaps and adoption risks.
- [ ] Priority ranking matches the deployment model.
- [ ] Compliance, data training, auditability, portability, and pricing were not skipped.
- [ ] Output uses an internal-report voice and avoids second-person reader address.
- [ ] Source list, assumptions, skipped domains, and unresolved gaps are included.
