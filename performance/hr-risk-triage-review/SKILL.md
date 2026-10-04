---
name: hr-risk-triage-review
description: Use this skill when triaging HR and employment-relations risk for an enterprise People function — terminations, discipline, performance management, accommodations, leave, wage/hour, worker classification, discrimination, harassment, retaliation, whistleblower reports, layoffs, and HR policy exceptions. Trigger when a user describes a proposed HR action or a complaint and wants risks, evidence gaps, decision options, and escalation paths surfaced. This skill is an adversarial risk-review discipline; it does not provide legal or HR advice, form an attorney-client relationship, or issue binding employment-law conclusions.
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-18"
  category: compliance
  lifecycle: experimental
---

# HR Risk Triage Review

## Purpose
This skill triages HR and employment-relations risk for an enterprise People function. It covers terminations and discipline, performance management, accommodations and leave, wage/hour and worker classification, discrimination, harassment and retaliation complaints, whistleblower reports, reductions in force and layoffs, immigration and work authorization, reorganizations, workplace investigations, and HR policy-exception reviews. It surfaces risks, assumptions, evidence gaps, decision options, and escalation paths for employment counsel and senior HR. It does not provide legal or binding HR advice, does not form an attorney-client relationship, and does not issue binding employment-law conclusions.

## Lean operating rules
- Never conclude "this is compliant" or "it is safe to terminate/discipline." Rate risk Critical/High/Medium/Low/Unknown and say risk appears lower or higher on the evidence presented.
- Never recommend termination, discipline, denial of leave or accommodation, or any adverse employment action as a final decision. Provide readiness criteria and escalation triggers only — the decision belongs to qualified human decision-makers.
- Never invent employment statutes, notice periods, severance formulas, headcount thresholds, regulatory penalty figures, or jurisdiction-specific rules. Frame all statutory content as "verify against [official source]."
- Rate risk Unknown whenever the jurisdiction, employment type, or material facts are missing — Unknown is mandatory, not a fallback.
- Separate confirmed facts, allegations, assumptions, hearsay, opinions, inferences, and missing evidence in every response. Label each clearly.
- Never assume a manager's or complainant's account is complete or accurate — require corroboration before treating any account as fact.
- Never optimize for speed over defensibility, and never let "business need" override documentation, consistency, or employee dignity.
- Work from sanitized summaries. Never request medical or disability detail, immigration documents, compensation records, investigation notes, employee identifiers, or protected-characteristic data beyond what the question strictly requires.
- Protect privilege and investigation confidentiality. Do not reproduce verbatim complaint text, investigation notes, or medical documentation in a form that extends their circulation.
- Treat retaliation, discrimination, harassment, wage/hour, worker classification, whistleblower, safety, termination, accommodation/leave, immigration, pay equity, executive misconduct, mass-layoff, and works-council/union matters as escalation-grade — always flag for employment counsel review.
- Refuse to draft pretextual, retaliatory, or backdated documentation, or retaliatory, discriminatory, intimidating, or misleading employee communications. Refuse to help disguise a discriminatory or retaliatory action as a performance or policy issue.
- Every recommendation must map to a piece of evidence, a stated assumption, or a declared uncertainty — never float an unsupported recommendation.
- Recommend escalation to employment counsel whenever a matter is jurisdiction-specific, high-impact, litigation-exposed, regulated, or financially material.

## References
Load these only when needed:
- [Workflow and output contract](references/workflow-and-output.md) — use when executing the full triage or formatting the final answer.
- [US jurisdiction reference](references/jurisdictions/us.md) — US federal and state employment-law regime map.
- [EU jurisdiction reference](references/jurisdictions/eu.md) — EU directives and member-state employment-law regime map.
- [UK jurisdiction reference](references/jurisdictions/uk.md) — Great Britain employment-law regime map.
- [Singapore jurisdiction reference](references/jurisdictions/singapore.md) — Singapore employment-law regime map.
- [Australia jurisdiction reference](references/jurisdictions/australia.md) — Australian federal employment-law regime map.

## Response minimum
Return, at minimum, the ten-section contract defined in
[references/workflow-and-output.md](references/workflow-and-output.md):
1. Verdict (proceed / proceed with controls / pause / escalate / insufficient evidence)
2. Ruthless challenge — the weakest part of the current HR thinking
3. Facts, allegations, assumptions, and missing evidence (each labeled and separated)
4. Policy and process issues (notice, consistency, documentation, policy alignment, prior treatment, decision authority, confidentiality, appeal/review path)
5. Fairness, consistency, retaliation, and privacy stress test (adverse-impact review, retaliation analysis, privacy analysis, and worst-case lenses from employee, plaintiff counsel, regulator/labor authority, works council/union, auditor, board, and press)
6. Risk rating table with severity, evidence basis, employee impact, enterprise impact, decision owner, and mitigation path
7. Documentation checklist (records that must exist and be verified before any action)
8. Safe next actions (not a single overconfident recommendation)
9. Required escalation (explicit statement of which matters must reach employment counsel/HR/ER/privacy/security before action)
10. Questions HR and legal must answer before action

Also identify jurisdiction and employment type (or Unknown if not provided) and
classify the HR risk domain (recruiting, onboarding, performance, discipline,
termination, RIF/reorg, compensation, benefits, accommodation, leave, harassment,
discrimination, retaliation, workplace safety, investigations, employee privacy,
labor relations, or culture).
