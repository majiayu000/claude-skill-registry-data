---
name: backlink-quality-validator
description: Validate proposed or existing backlinks for relevance, editorial legitimacy, link attributes, spam/toxicity risk, platform compliance, anchor quality, target-page fit, and monitoring evidence. Use this skill when the user asks whether an external link opportunity or placed backlink is safe and useful, and reject toxic, irrelevant, paid-undisclosed, fake, or spam placements.
---

# Backlink Quality Validator

Use this skill after an opportunity is proposed by a scout or after a backlink already exists.

Read `./plans/seo-llm-skill-cluster/authority/white-hat-authority-policy.md`
before validating a placement.

Read [references/validation-rubric.md](references/validation-rubric.md) before producing a verdict.

## Owns

- backlink quality review;
- relevance and target-page fit;
- link attribute review (`follow`, `nofollow`, `ugc`, `sponsored`);
- anchor text risk;
- spam/toxicity risk;
- platform compliance notes;
- approval or rejection recommendation.

## Does Not Own

- finding opportunities;
- posting or editing links;
- paid placement negotiation;
- external outreach;
- Search Console/rank attribution;
- disavow decisions without broader SEO review.

## Workflow

1. Identify source URL, target URL, anchor text, link location, and context.
2. Check relevance and user value.
3. Check link attribute and disclosure expectations.
4. Check platform-rule status.
5. Identify spam, toxicity, PBN, directory, fake review, and paid-undisclosed risk.
6. Score the backlink as `approve`, `revise`, `reject`, or `needs_more_evidence`.
7. Provide exact reason and safe next step.

## Non-Negotiables

- Reject link farms, PBNs, fake reviews, hidden links, irrelevant directories, and paid-undisclosed links.
- Reject anchor text that is misleading or stuffed.
- Do not claim a backlink improves rankings without measurement.
- Do not edit external pages.
- Do not recommend disavow unless the broader context and risk are reviewed.

## Safety And Privacy Boundaries

- Do not store private outreach, account credentials, paid-placement negotiations, or private analytics in reports.
- If source pages include private or sensitive content, summarize without exposing it.
- Mark unknown platform rules as unknown rather than assuming permission.

## Output Shape

Return:

1. Validation verdict.
2. Source/target/anchor/context.
3. Scores and rationale.
4. Link attribute and disclosure notes.
5. Platform-rule status.
6. Risks and required fixes.
7. Monitoring or recheck date.

## Validation

Validate skill edits with:

```bash
python3 <codex-skills-dir>/senior-skill-architect/scripts/lint_production_skill.py ./skills/backlink-quality-validator
python3 ./plans/seo-llm-skill-cluster/scripts/lint_skill_cluster.py .
```

Forward tests live in [evals.json](evals.json).
