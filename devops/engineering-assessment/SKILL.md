---
name: engineering-assessment
description: Use to diagnose development practices such as XP, Lean, DevOps, CI/CD, DORA, DDD, architecture, and Team Topologies, and produce improvement proposals or adoption plans. Do not use for ordinary fixes, individual code reviews, conceptual explanations, or adoption implementation.
---

# Diagnose development practices and plan adoption

Investigate the flow for delivering value safely to users and make the first improvement to try concrete. Choose an answer, Issue record, or verified plan for approved implementation according to the requested terminal deliverable. Follow [Plan deliverables](references/assessment.md#plan-deliverables) to save and verify requested records. If implementation is also requested, retain that approval and continue after plan verification; an assessment or Issue alone does not authorize it. Repositories and `docs/` below refer to the diagnosis target.

## Scope and reference material

Check target instructions, user outcomes, services and value flow, constraints, and existing diagnosis Issues. If purposes affecting diagnosis scope or priorities are unclear, ask people and continue material investigation that does not depend on answers.

[Building an adoption plan from evidence](references/assessment.md) is the common procedure for diagnosis/planning. Then select only lenses needed for the requested problem.

| Condition | Additional reference | Do not read |
| --- | --- | --- |
| XP itself, XP second edition, Values / Principles / Practices, or diagnosis primarily of XP | [XP taxonomy](references/xp.md) | Unrelated full DORA / Architecture material |
| Individual XP Values / Principles / Practices as auxiliary lenses in Architecture / DORA / Lean diagnosis | [Lightweight lookup of individual XP items](references/xp-auxiliary.md) | The full `xp.md` taxonomy |
| Domain / Bounded Context, service/repository/team mappings, cross-team dependencies, Microservices, Conway | [Architecture and Organization](references/architecture-and-organization.md) | All unrelated DORA Catalog entries |
| DORA Core / Capability Catalog / delivery metrics, DORA Capability | [DORA capability lens](references/dora.md) | Unrelated full XP taxonomy / Architecture material |
| Diagnosis needing definitions, relationships, or compact guardrails for BDD / ATDD / TDD / DDD / Lean / DevOps / CI / CD | [Relationships among principles](references/principles.md) | Focused references whose conditions do not apply |

Combine lenses only when they actually relate to the problem. When individual XP items merely assist Architecture / DORA / Lean diagnosis, use only needed items from the lightweight lookup rather than reading the full `xp.md` taxonomy. Switch to `xp.md` only when XP itself becomes a diagnosis target. For example, Microservices adoption decisions can center on Architecture / Organization, assisted by DDD and XP Simplicity or Economics. For release-approval waiting alone, focus on Lean / CD and relevant DORA Capabilities.

In limited diagnoses where stakeholders have confirmed definitions, version differences, and compact guardrails and only evidence of current practice is needed, proceed with `assessment.md` alone without requiring `principles.md`. For example, if the CI definition is confirmed, proceed directly to actual evidence of main integration, feedback, failure repair, and similar practices.

Focus limited diagnoses on requested concepts or problems, selecting related lenses only. Comprehensive diagnosis compares perspectives including XP with the target flow, but selects actually relevant lenses rather than reading every reference in sequence. Do not add unrelated perspectives to uncertainty lists merely because topic words appear; confirm changes to the request scope.

## Judgment and completion boundaries

Distinguish the presence of configuration or artifacts from actual practice, and separate observed practices, evidence-based gaps, uncertainties, and reasoned inapplicability. Compare responsibilities, culture, and cognitive load with responsible people's experiences. Do not turn missing data into zero or improvement effects, or use it for individual evaluation or fixed Elite judgments.

Choose small experiments from the most influential constraint, organizing evidence, order and dependencies, roles, acceptance conditions, validation, and reassessment. Do not assume stakeholder agreement or implementation dates; adapt to solo development, legacy systems, multiple teams, and similar conditions. Do not make creating four teams or uniform repository splitting adoption prerequisites.

Set completion conditions from the requested deliverable.

| Requested deliverable | Completion condition |
| --- | --- |
| Answer with diagnosis, improvements, comparison, or proposals | Present evidence, judgments, uncertainties, and proposals as an answer, then stop. Do not implicitly start Issues, document saving, or implementation |
| Issue record of diagnosis/adoption plans only | Save, retrieve, and check agreement and display under [Issue records](references/assessment.md#issue-records), present URL and body, then stop. Distinguish completed diagnosis from unimplemented adoption and leave the Issue open |
| Save a diagnosis report or plan document | Follow [Repository documents](references/assessment.md#repository-documents) for a supporting plan and delivery of the requested report, then stop. Do not implicitly implement improvement measures |
| Implement adoption/improvements | Confirm scope, acceptance conditions, validation, and execution approval under [Implementation scope](references/assessment.md#implementation-scope), and continue only the approved changes |

Even if answer-only diagnosis discovers failing main, include evidence, impact, and recovery priority in the answer without starting recovery. For Issue-record-only terminal deliverables, record the same in the plan and stop. For document terminal deliverables such as diagnosis reports, stop after delivering the document through necessary supporting Issue planning. For simultaneous Issue-record and implementation requests, continue approved implementation after completing plan saving as a supporting artifact. Where posting is prohibited, saving fails, verification is incomplete, or required operations are unavailable, hold the affected work and report the exact gap. Separately present answerable diagnosis results without claiming successful saving or implementation.
