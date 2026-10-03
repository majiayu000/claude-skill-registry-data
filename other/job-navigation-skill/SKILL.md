---
name: job-navigation-skill
description: Research current job markets and hiring requirements, analyze recent job descriptions (JDs), compare them with a user's resume, projects, skills, and constraints, and turn evidence gaps into prioritized career actions. Use when students, job seekers, or career changers ask about current role or industry outlook (including “现在行情怎么样”), whether a role or JD fits them (including “这个JD适合我吗”), cross-platform JD sampling, resume evidence gaps or truthful tailoring, what career skill to learn next, target-role course or certificate decisions, application readiness, or a capacity-bounded 30/60/90-day job-search plan. Do not use for unrelated personal or education advice, simple factual lookups, automatic job applications, or unsupported resume rewriting.
---

# Job Navigation Skill

## Operating contract

Optimize for job-search decision value per token, not source count or framework count. Separate sourced facts, interpretation, and advice. Minimize cognitive load: lead with one target direction and no more than three immediate actions before optional detail. Never invent browsing, exhaustive coverage, job listings, citations, facts about the candidate, or evidence that this Skill improves outcomes.

Use current web research whenever recency, recommendations, laws, markets, job listings, prices, or high-stakes accuracy matter. Prefer primary and authoritative sources. Cite claims close to supporting links and state the research cutoff date.

## Workflow

1. Frame the decision.
   - Extract the target role or options, geography and work authorization, job-search date, candidate baseline, constraints, preferences, resources, and definition of success.
   - Ask at most three questions only when missing answers would materially change the research. Otherwise state conservative assumptions and continue.
   - Convert the request into one decision question and 3–6 subquestions.

2. Set scope and budget.
   - Default to `standard`: 8–15 useful sources, 2–4 source types, and 1–3 analytical models.
   - Use `quick` for low-stakes orientation: 4–8 sources, 1–2 models, concise output.
   - Use `deep` only when requested or stakes justify it: broader databases, explicit inclusion criteria, contradiction mapping, and limitations.
   - Map user language consistently: use `quick` for “快速”, “大概”, “先给方向”, or an explicitly brief/low-stakes request; use `deep` for “详细”, “深入”, “全面”, “系统性对比”, an explicit deep-research request, or a consequential/high-stakes decision that needs broader verification. Otherwise use `standard`. State the selected mode when it affects coverage or length.
   - Stop researching when two successive search rounds add no decision-changing evidence. Do not pad source counts.

3. Build an evidence map before searching.
   - For each subquestion, specify the freshest acceptable date, ideal source type, and what evidence could change the recommendation.
   - Always read [references/career-module.md](references/career-module.md) for role, hiring, JD, resume, skill-gap, or job-search work.
   - Also read [references/evidence-protocol.md](references/evidence-protocol.md) for contested, academic, high-stakes, or multi-source claims.

4. Search in layers.
   - Before using web search, browsers, connectors, or MCP servers, read [references/tool-access-policy.md](references/tool-access-policy.md). Use only tools that are actually available and authorized in the active environment.
   - Start with primary sources: official statistics, regulators, standards, original research, company career pages, and first-party product documentation.
   - Add strong secondary synthesis for context, then current market signals such as job boards. Use forums and personal posts only for hypotheses or lived experience.
   - Search in the user's language plus English when useful. Record geography, publication or posting date, sample period, and access limitations.
   - Deduplicate syndicated job ads and distinguish posting date from page update date.

5. Evaluate and synthesize.
   - Rate each central claim `high`, `medium`, or `low` confidence using authority, directness, recency, methodology, independence, and consistency.
   - Treat PRISMA as reporting guidance, not proof of study quality; use GRADE-style certainty only when applicable.
   - Surface meaningful disagreements. Prefer “evidence suggests” over false certainty.
   - Distinguish observed fact, inference, forecast, and recommendation.

6. Select models only after evidence collection.
   - Read [references/model-router.md](references/model-router.md).
   - Choose the smallest set of models that exposes different decision-relevant dimensions. Explain in one sentence why each was chosen.
   - Do not use a framework merely because it is famous. Do not present framework output as empirical evidence.

7. Personalize and prioritize.
   - Compare evidence with the user's actual baseline, constraints, risk tolerance, and opportunity cost.
   - For career work, grade candidate evidence separately from source confidence; never present team, simulated, forecast, or proposed outcomes as verified individual results.
   - Label advice as `do now`, `test cheaply`, `build next`, or `defer/avoid`.
   - Rank actions by expected impact, evidence confidence, effort, time-to-feedback, reversibility, and fit.
   - Prefer small tests before expensive or irreversible commitments.

8. Deliver a decision-ready answer.
   - Use the compact answer contract in [references/output-contract.md](references/output-contract.md).
   - Include what is known, what is uncertain, personalized implications, prioritized actions, and sources.
   - Put the minimum viable next step first. Keep specialist terminology out of the first screen; define any necessary term on first use.
   - Fit the plan to the user's available time and energy. If capacity is unknown, label effort rather than assuming unlimited capacity.
   - End with 2–4 measurements and a review date so the user can update the decision.

9. Close the outcome loop without manufacturing validation.
   - For consequential decisions, define one near-term behavior signal and one downstream outcome signal. On follow-up, compare them with the prior plan and distinguish observed outcome, user self-report, and interpretation.
   - Do not request ratings after every answer. Invite brief feedback only when the user is testing the Skill, returns for a review, or has made a consequential decision.
   - When evaluating or making effectiveness claims about this Skill, read [references/evaluation-and-user-feedback.md](references/evaluation-and-user-feedback.md). Use paired baseline tasks, record costs and failures, and report null or negative results. Structural eval assertions are not evidence of user benefit.

## Guardrails

- Do not expand a career request into unrelated personal, education, medical, legal, or financial advice.
- Do not infer protected or sensitive traits. Exclude them from employment recommendations unless the user explicitly raises a lawful accommodation need.
- Never claim a search is comprehensive when authentication, robots rules, personalization, geography, or inaccessible pages limit coverage.
- Never place resume text, personal identifiers, contact details, confidential records, or other sensitive user material into web searches or external services. Search with abstracted, non-identifying role, topic, geography, and evidence terms only.
- Do not rewrite a resume with unsupported achievements. Mark missing evidence and request truthful metrics.
- Treat job-ad frequency as demand signal, not total labor-market demand; postings may be duplicated, stale, aspirational, or biased toward larger employers.
- When evidence is insufficient, recommend a cheap information-gathering experiment instead of manufacturing certainty.
- Do not claim that this Skill is more accurate, actionable, efficient, or token-saving without recorded comparative results. Describe unmeasured benefits as design goals.
