---
name: site-growth-orchestrator
description: Coordinate SEO, LLM-readable site architecture, UX, content, monitoring, security, and external authority work as a task-plan-driven sequence. Use this skill when the user asks to plan, execute, validate, or route multi-skill website growth work; asks what to do next across semantic core, URL structure, internal linking, schema, llms.txt, UX journeys, analytics, citation monitoring, or white-hat link placement; or wants a central architect that preserves evidence, alarms, handoffs, and tests.
---

# Site Growth Orchestrator

Use this skill as the routing and governance layer for site-growth work. It coordinates specialist skills, task plans, artifacts, validation, and release gates. It does not replace the specialists.

## Core Rule

Own sequence, evidence, handoff quality, and stop conditions. Delegate domain judgments.

- SEO/schema architecture goes to `technical-seo-schema-engineer` or existing `seo-llm-site-architect`.
- Semantic core goes to `semantic-core-architect`.
- URL architecture goes to `information-architecture-seo`.
- Internal linking goes to `internal-link-graph-architect`.
- LLM-readable site layers go to `llm-friendly-site-architect`.
- Validation goes to `seo-regression-validator` and `cluster-consistency-linter`.
- UX journeys go to `ui-ux-llm-product-architect`.
- Security boundaries go to `web-security-architect`.
- External authority placement is approval-first and post-MVP.

Read [references/workflow.md](references/workflow.md) before handling broad multi-step requests.

## Modes

- `triage`: classify a user request, identify owners, blockers, required evidence, and next task.
- `plan`: create or update a TASK-PLAN v2 with dependencies, alarms, test gates, and artifacts.
- `execute`: route work to the next specialist sequence and keep the plan state current.
- `review`: compare outputs against the goal, artifacts, task plan, and validation evidence.
- `release`: decide whether a staged skill/site-growth workflow can be packaged, deployed, or needs rollback.

## Workflow

1. Restate the concrete objective and current artifact state.
2. Identify the primary owner skill and the supporting skills.
3. Check active alarms, unknown credentials, freshness-sensitive facts, and external-action boundaries.
4. Choose the next smallest unblocked task.
5. Prepare a handoff packet using [assets/handoff-packet.template.md](assets/handoff-packet.template.md) when another specialist needs context.
6. Require evidence before marking work complete: file paths, commands, reports, browser checks, live URLs, or source links.
7. Update the task plan and validation artifacts before committing.
8. Stop or defer work that needs secrets, account access, external posting, legal approval, or live production changes not approved by the user.

## Artifact Contract

Use the shared plan artifacts instead of inventing local formats:

- `goal_brief.md`
- `semantic-core.yaml`
- `entity-topic-map.yaml`
- `url-map.yaml`
- `internal-link-graph.yaml`
- `schema-report.json`
- `llm-discovery-report.md`
- `ux-journey-map.md`
- `crawler-access-audit.json`
- `seo-regression-report.json`
- `validation-summary.md`
- `cluster-lint-report.json`

If an artifact is missing, record it as missing. Do not fake it.

## Safety And Refusal Rules

Refuse or escalate requests for hidden bot-only content, doorway pages, fake evidence, spam link placement, account abuse, evasion of access controls, or ranking/citation promises without data.

For current facts about Google, AI crawlers, schema.org, platform policies, Search Console, assistant citation behavior, or crawler IPs, require primary-source verification under the cluster freshness policy.

## Validation

Before a task is done, require one of these:

- deterministic lint output;
- live or fixture audit output;
- browser/screenshot verification for UI changes;
- source-linked research notes for current external facts;
- negative-test result showing a dangerous request is blocked.

Run the local cluster linter after creating or editing staged skills:

```bash
python3 ./plans/seo-llm-skill-cluster/scripts/lint_skill_cluster.py .
```

Forward tests for this skill live in [evals.json](evals.json).

## Output Shape

For broad requests, answer with:

1. Current objective.
2. Primary owner and support owners.
3. Active blockers or alarms.
4. Next task and why it is next.
5. Required artifacts and checks.
6. What will not be touched.
7. Commit or release status when applicable.

